package br.ufal.easy.exceptionhunter.extractors;

import br.ufal.easy.exceptionhunter.models.ThrowExceptionModel;
import com.google.gson.Gson;
import com.google.gson.JsonParser;
import com.google.gson.stream.JsonReader;
import br.ufal.easy.exceptionhunter.ProjectConfig;
import org.eclipse.jgit.api.Git;
import org.eclipse.jgit.lib.Constants;
import org.eclipse.jgit.lib.Repository;
import org.jsoup.Connection;
import org.jsoup.HttpStatusException;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.*;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.net.ConnectException;
import java.net.HttpURLConnection;
import java.net.SocketTimeoutException;
import java.net.URL;
import java.util.*;

public class CoverageExtractor {

    private ProjectConfig projectConfig;

    private String tagPath;

    private Double tagCoverage;

    private ModelExtractor models;

    private boolean saveToMongoDB;

    private String buildCommitSha;

    private Logger logger;

    private Boolean coverageByAspects;


    public CoverageExtractor(ProjectConfig projectRootPath, String tagPath, ModelExtractor me, boolean saveToMongoDB, boolean coverageByAspects) {
        this.projectConfig = projectRootPath;
        this.tagPath = tagPath;
        this.models = me;
        this.saveToMongoDB = saveToMongoDB;
        this.logger = LoggerFactory.getLogger("ExceptionHunter");
        this.tagCoverage = null;
        this.coverageByAspects = coverageByAspects;
        this.buildCommitSha = getGitBuildCommitSha(tagPath);

    }

    public void tryToExtractCoverage(){
        logger.info("*** Starting to extract coverage ***");
        if(!coverageByAspects){
            boolean coverallsResult = extractFromCoveralls();
            if (!coverallsResult){
                extractFromCodecov();
            }
        } else {
            extractFromAspectJson();
        }

    }

    private void extractFromAspectJson() {
        String filePath = tagPath + File.separator + "exception_testing_log" + File.separator + "coverage.json";
        Gson gson = new Gson();
        JsonReader reader = null;
        Map<String, Map<String, Integer>> map = null;
        try {
            reader = new JsonReader(new FileReader(filePath));
            map = gson.fromJson(reader, Map.class);
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }

        for (ThrowExceptionModel model : models.getThrowExceptionModels()){
            if(model.isInsideATest()){
                continue;
            }

            try {
                logger.info("*** Updating model with coverage data ***");
                updateModelWithCoverage(model, map);
            } catch (IOException e) {
                logger.error("*** Could not update model with coverage data ***");
                e.printStackTrace();
            }
        }

    }

    private boolean extractFromCodecov() {
        tagCoverage = downloadCodecovTagCoverageReport();
        if(tagCoverage == null){
            return false;
        }
        Set alreadySavedModels = new HashSet();
        String filePath;
        String newFilePath;
        File coverageOutputFile;
        for (ThrowExceptionModel model : models.getThrowExceptionModels()){
            if(model.isInsideATest()){
                continue;
            }
            filePath = model.getFullFilePath();
            newFilePath = tagPath + File.separator + "coverage" + File.separator + filePath.replace(".java", ".txt");
            coverageOutputFile = new File(newFilePath);
            logger.info("*** Trying to download coverage report of " + filePath + " class ***");
            if(!alreadySavedModels.contains(filePath) && !coverageOutputFile.exists() ){
                try {
                    downloadIndividualCodecovCoverageReport(filePath, coverageOutputFile);
                    logger.info("*** Coverage Report of " + filePath + " downloaded! ***");
                } catch (IOException e) {
                    logger.error("*** Coverage Report of " + filePath + " could not be downloaded! ***");
                }
                alreadySavedModels.add(filePath);
            } else {
                logger.info("*** Coverage Report of " + filePath + " already exists. Skipping! ***");
            }


            try {
                logger.info("*** Updating model with coverage data ***");
                updateModelWithCoverage(model, coverageOutputFile);
            } catch (IOException e) {
                logger.error("*** Could not update model with coverage data ***");
                e.printStackTrace();
            }
        }
        return true;
    }


    private boolean extractFromCoveralls() {
        tagCoverage = downloadCoverallsTagCoverageReport();

        if(tagCoverage == null){
            return false;
        }

        Set alreadySavedModels = new HashSet();
        String filePath;
        String newFilePath;
        File coverageOutputFile;
        for (ThrowExceptionModel model : models.getThrowExceptionModels()){
            if(model.isInsideATest()){
                continue;
            }
            filePath = model.getFullFilePath();
            newFilePath = tagPath + File.separator + "coverage" + File.separator + filePath.replace(".java", ".txt");
            coverageOutputFile = new File(newFilePath);
            logger.info("*** Trying to download coverage report of " + filePath + " class ***");
            if(!alreadySavedModels.contains(filePath) && !coverageOutputFile.exists() ){
                try {
                    downloadIndividualCoverallsCoverageReport(buildCommitSha, filePath, coverageOutputFile);
                    logger.info("*** Coverage Report of " + filePath + " downloaded! ***");
                } catch (IOException e) {
                    logger.error("*** Coverage Report of " + filePath + " could not be downloaded! ***");
                }
                alreadySavedModels.add(filePath);
            } else {
                logger.info("*** Coverage Report of " + filePath + " already exists. Skipping! ***");
            }

            try {
                logger.info("*** Updating model with coverage data ***");
                updateModelWithCoverage(model, coverageOutputFile);
            } catch (IOException e) {
                logger.error("*** Could not update model with coverage data ***");
                e.printStackTrace();
            }
        }
        return true;
    }

    private Double downloadCodecovTagCoverageReport() {
        String baseURL = "https://codecov.io/gh/" + this.projectConfig.getProjectOwner() + "/" + this.projectConfig.getProjectName() + "/tree/" + buildCommitSha;
        Document codecovPage = null;
        Double tagCoverageValue = null;
        Element coverageTable = null;
        try {
            Connection connection = Jsoup.connect(baseURL);
            connection.userAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64)");
            connection.timeout(25000);
            connection.maxBodySize(0);
            connection.referrer("no-referrer-when-downgrade");
            codecovPage = connection.get();
            coverageTable = codecovPage.getElementById("tree");
            if (coverageTable == null){
                logger.info("*** This Tag does not have associated coverage report: " + baseURL + " ***");
                return null;
            }
        } catch (HttpStatusException e) {
            logger.info("*** This Tag does not have associated coverage report: " + baseURL + " responded with code " + e.getStatusCode() + " ***");
            return null;
        } catch (ConnectException | SocketTimeoutException e){
            logger.error("*** Connection timeout! Please check your connection and try again.***");
            return null;
        } catch (IOException e) {
            e.printStackTrace();
        }

        Element tableFoot = coverageTable.select("tfoot").first();
        Elements tableFootCoverageCell = tableFoot.select("[title=Coverage Ratio]");
        tagCoverageValue = Double.valueOf(tableFootCoverageCell.text().replace("%",""));
        logger.info("*** This Tag does have associated coverage report: " + baseURL + "  - Tag's Coverage:" + tagCoverageValue + "***");
        return tagCoverageValue;

    }

    private Double downloadCoverallsTagCoverageReport() {
        String baseURL = "https://coveralls.io/builds/" + buildCommitSha + ".json";
        URL urlForGetRequest = null;
        String readLine = null;
        HttpURLConnection connection = null;
        Double tagCoverageValue = null;
        try {
            urlForGetRequest = new URL(baseURL);
            connection = (HttpURLConnection) urlForGetRequest.openConnection();
            connection.setRequestProperty("Accept", "application/json");
            connection.setRequestMethod("GET");
            int responseCode = connection.getResponseCode();
            if (responseCode == HttpURLConnection.HTTP_OK) {
                BufferedReader in = new BufferedReader(
                        new InputStreamReader(connection.getInputStream()));
                StringBuffer response = new StringBuffer();
                while ((readLine = in.readLine()) != null) {
                    response.append(readLine);
                } in.close();
                String tagCoverageReport = new JsonParser().parse(response.toString()).getAsJsonObject().get("covered_percent").getAsString();
                tagCoverageValue = new BigDecimal(tagCoverageReport).setScale(2, RoundingMode.HALF_UP).doubleValue();
                logger.info("*** This Tag does have associated coverage report: " + urlForGetRequest + "  - Tag's Coverage:" + tagCoverageValue + "***");
            } else {
                logger.info("*** This Tag does not have associated coverage report: " + urlForGetRequest + " responded with code " + responseCode + "***");
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return tagCoverageValue;
    }

    private void downloadIndividualCodecovCoverageReport(String filePath, File coverageOutputFile) throws IOException {

        String baseURL = "https://codecov.io/gh/" + this.projectConfig.getProjectOwner() + "/" + this.projectConfig.getProjectName() + "/src/" + buildCommitSha + "/";
        if(filePath.startsWith("/") || filePath.startsWith("\\")){
            filePath = filePath.substring(1);
        }
        String fullFileURL = baseURL + filePath.replace("\\", "/");
        Document codecovPage = null;
        try {
            Connection connection = Jsoup.connect(fullFileURL);
            connection.userAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64)");
            connection.timeout(25000);
            connection.maxBodySize(0);
            connection.referrer("no-referrer-when-downgrade");
            codecovPage = connection.get();
        } catch (HttpStatusException e) {
            String message = "*** Download failure! Get " + fullFileURL + " responded with code " + e.getStatusCode() + " ***";
            logger.info(message);
            throw new IOException(message);
        }
        Element coverageTable = codecovPage.getElementById("pjax-inner");
        if(coverageTable.toString().contains("File path not found.")){
            return;
        }

        List srcLinesCoverage = new LinkedList<String>();
        Element tableBody = coverageTable.select("tbody").first();

        for (Element tableRow : tableBody.children()){
             Element rowCell = tableRow.select(".src-d").first();
             String lineHits = "";
             for(Element cell : rowCell.children()){
                 if (cell.attr("title").equals("complexity")) {
                     continue;
                 }
                 lineHits = cell.text();
             }
            if (lineHits.isEmpty()) {
                lineHits = "null";
            }
            srcLinesCoverage.add(lineHits.trim());
        }
        writeCoverageReportToDisk(coverageOutputFile, srcLinesCoverage.toString());

    }


    private void downloadIndividualCoverallsCoverageReport(String buildCommitSha, String filePath, File coverageOutputFile) throws IOException {

        //String baseURL = "https://coveralls.io/builds/b2ad54355472650281e7bb728301ee803db63658/source.json";
        String baseURL = "https://coveralls.io/builds/" + buildCommitSha + "/source.json";

        if(filePath.startsWith("/") || filePath.startsWith("\\")){
            filePath = filePath.substring(1);
        }
        URL urlForGetRequest = new URL(baseURL + "?filename=" + filePath.replaceAll("[/\\\\]", "%2F"));
        String readLine = null;
        HttpURLConnection connection = (HttpURLConnection) urlForGetRequest.openConnection();
        connection.setRequestProperty("Accept", "text/plain");
        connection.setRequestMethod("GET");
        int responseCode = connection.getResponseCode();
        if (responseCode == HttpURLConnection.HTTP_OK) {
            BufferedReader in = new BufferedReader(
                    new InputStreamReader(connection.getInputStream()));
            StringBuffer response = new StringBuffer();
            while ((readLine = in.readLine()) != null) {
                response.append(readLine);
            } in.close();
           // System.out.println("JSON String Result " + response.toString());
            writeCoverageReportToDisk(coverageOutputFile, response.toString());
        } else {
            logger.info("***Download failure! Get " + urlForGetRequest + " responded with code " + responseCode + "***");
        }
    }

    private String getGitBuildCommitSha(String gitPath) {
        String lastCommitHash = "";
        try {
            Repository gitRepo = Git.open(new File(gitPath)).getRepository();
            lastCommitHash = gitRepo.resolve(Constants.HEAD).getName();
        } catch (IOException | NullPointerException e) {
            //e.printStackTrace();
        }
        return lastCommitHash;
    }

    private void writeCoverageReportToDisk(File coverageOutputFile, String report) {
        coverageOutputFile.getParentFile().mkdirs();
        BufferedWriter writer = null;
        report = report.replace(" ", "");
        try {
            writer = new BufferedWriter(new FileWriter(coverageOutputFile));
            writer.write(report);
            writer.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void updateModelWithCoverage(ThrowExceptionModel model, Map<String, Map<String, Integer>> map) throws IOException {
        String key = model.getFullClassPackagePath() + "["+model.throwStatementLine+"]";
        Map<String, Integer> secondMap = map.get(model.getException());
        Integer lineCoverageValue = null;
        if(secondMap != null){
            Object aux = secondMap.get(key);
            if(aux != null){
                lineCoverageValue = Double.valueOf(aux.toString().trim()).intValue();
            }

        }
        lineCoverageValue = lineCoverageValue == null ? Integer.valueOf(0) : lineCoverageValue;
        model.setNumberOfTimesTheLineWasExecuted(lineCoverageValue);
    }

    private void updateModelWithCoverage(ThrowExceptionModel model, File coverageOutputFile) throws IOException {
        if (!coverageOutputFile.exists()){
            logger.info("*** Coverage data of " + coverageOutputFile.toString() + " does not exists. Skipping!");
            return;
        }
        BufferedReader br = new BufferedReader(new FileReader(coverageOutputFile));

        StringBuffer coverageReport = new StringBuffer();
        String st = "";
        while ((st = br.readLine()) != null){
            coverageReport.append(st);
        }
        String coverageReportArray = coverageReport.toString().replace("[", "").replace("]", "");
        String[] individualLineReport = coverageReportArray.split(",");
        String lineCoverageValueAux = individualLineReport[model.getThrowStatementLine() - 1];
        Integer lineCoverageValue;
        if(lineCoverageValueAux.equals("null")){
            lineCoverageValue = null;
            //logger.error("***Invalid Coverage Value! " + coverageOutputFile + " line  " + model.throwStatementLine + "***");
        } else{
            lineCoverageValue = Integer.valueOf(lineCoverageValueAux);
        }
        model.setNumberOfTimesTheLineWasExecuted(lineCoverageValue);
        br.close();
    }

    public ProjectConfig getProjectConfig() {
        return projectConfig;
    }

    public void setProjectConfig(ProjectConfig projectConfig) {
        this.projectConfig = projectConfig;
    }

    public String getTagPath() {
        return tagPath;
    }

    public void setTagPath(String tagPath) {
        this.tagPath = tagPath;
    }

    public Double getTagCoverage() {
        return tagCoverage;
    }

    public void setTagCoverage(Double tagCoverage) {
        this.tagCoverage = tagCoverage;
    }

    public ModelExtractor getModels() {
        return models;
    }

    public void setModels(ModelExtractor models) {
        this.models = models;
    }

    public boolean isSaveToMongoDB() {
        return saveToMongoDB;
    }

    public void setSaveToMongoDB(boolean saveToMongoDB) {
        this.saveToMongoDB = saveToMongoDB;
    }

    public String getBuildCommitSha() {
        return buildCommitSha;
    }

    public void setBuildCommitSha(String buildCommitSha) {
        this.buildCommitSha = buildCommitSha;
    }

    public Logger getLogger() {
        return logger;
    }

    public void setLogger(Logger logger) {
        this.logger = logger;
    }

    @Override
    public String toString() {
        return "CoverageExtractor{" +
                "projectConfig=" + projectConfig +
                ", tagPath='" + tagPath + '\'' +
                ", tagCoverage=" + tagCoverage +
                ", models=" + models +
                ", saveToMongoDB=" + saveToMongoDB +
                ", buildCommitSha='" + buildCommitSha + '\'' +
                '}';
    }
}
