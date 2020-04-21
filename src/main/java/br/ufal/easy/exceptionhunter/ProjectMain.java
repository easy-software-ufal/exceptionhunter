package br.ufal.easy.exceptionhunter;

import br.ufal.easy.exceptionhunter.extractors.CoverageExtractor;
import br.ufal.easy.exceptionhunter.visitors.*;
import br.ufal.easy.exceptionhunter.visitors.commom.Commom_FailCallVisitor;
import br.ufal.easy.exceptionhunter.visitors.junit.AssertThrowsVisitor;
import br.ufal.easy.exceptionhunter.visitors.junit.ExpectExceptionCallVisitor;
import br.ufal.easy.exceptionhunter.visitors.junit.ExpectedAnnotationVisitor;
import com.github.javaparser.ParseResult;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.visitor.VoidVisitor;
import com.github.javaparser.printer.YamlPrinter;
import com.github.javaparser.utils.ParserCollectionStrategy;
import com.github.javaparser.utils.ProjectRoot;
import com.github.javaparser.utils.SourceRoot;
import br.ufal.easy.exceptionhunter.extractors.CombinedTypeExtractor;
import br.ufal.easy.exceptionhunter.extractors.ModelExtractor;
import br.ufal.easy.exceptionhunter.extractors.StatisticsExtractor;
import br.ufal.easy.exceptionhunter.visitors.assertj.AssertJ_assertThatVisitor;
import br.ufal.easy.exceptionhunter.visitors.assertj.AssertJ_assertThatExceptionNameVisitor;
import br.ufal.easy.exceptionhunter.visitors.assertj.AssertJ_assertThatExceptionOfTypeVisitor;
import br.ufal.easy.exceptionhunter.visitors.assertj.AssertJ_assertThatThrownByVisitor;
import br.ufal.easy.exceptionhunter.visitors.testng.TestNG_ExpectedExceptionsAnnotationVisitor;
import org.eclipse.jgit.api.Git;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.*;
import java.util.stream.Collectors;

import static java.util.Collections.singleton;

public class ProjectMain {

    private Logger logger = LoggerFactory.getLogger("ExceptionHunter");
    private String allowedCharacters = "[^A-Za-z0-9()\\-_.\\[\\]]";
    private ProjectsConfiguration projectsConfiguration;
    private ProjectsManagerSingleton projectsManagerSingleton;

    public ProjectMain(ProjectsConfiguration projectsConfiguration) {
        this.projectsConfiguration = projectsConfiguration;
        projectsManagerSingleton = ProjectsManagerSingleton.getProjectsManagerSingleton();
        if(projectsConfiguration.isSaveToMongoDB()){
            projectsManagerSingleton.setSaveToMongo(projectsConfiguration.isSaveToMongoDB());
            projectsManagerSingleton.configureMongoDB(projectsConfiguration.getMongoConnectionString(), projectsConfiguration.getMongoDatabaseName(), projectsConfiguration.getMongoCollectionName());
        }
    }

    public Map<String, List<ProjectsDataWrapper>> proceedWithAnalysis(){
        Map<String, List<ProjectsDataWrapper>> projectsDataWrapper = new HashMap<String, List<ProjectsDataWrapper>>();

        for (ProjectConfig projectRootPath : projectsConfiguration.getProjects()) {
            //verifica se o projeto esta marcado como ativo no json
            logger.info("Starting the analysis of Project " + projectRootPath.getProjectName());
            if (!projectRootPath.isActive()) {
                logger.info("Project " + projectRootPath.getProjectName() + " is marked as inactive. Skipping");
                continue;
            }
            projectsDataWrapper.put(projectRootPath.getProjectName(), startAnalysis(projectRootPath));
        }
        return projectsDataWrapper;
    }



    private List<ProjectsDataWrapper> startAnalysis(ProjectConfig projectRootPath) {
        List<ProjectsDataWrapper> projectsDataWrappers = new ArrayList<>();
        Map<String, String> tagList = null;

        if(projectsConfiguration.isNewestTagOnly()){
            String newestTag = "";
            Date newestTagDate = new GregorianCalendar(1970, 0, 1).getTime();
            for (String tag : projectRootPath.getTags().keySet()){
                Date tagDate = null;
                try {
                    tagDate = new SimpleDateFormat("dd/MM/yyyy hh:mm:ss").parse(projectRootPath.getTags().get(tag));
                } catch (ParseException e) {
                    e.printStackTrace();
                }
                if(tagDate.after(newestTagDate)){
                    newestTagDate = tagDate;
                    newestTag = tag;
                }
                tagList = new HashMap<>();
                tagList.put(newestTag, newestTagDate.toString());
            }
        } else {
            tagList = projectRootPath.getTags();
        }

        for (String tag : tagList.keySet()) {

            String adjustedTagName = tag.replace("#", ".");

            if (projectsConfiguration.isSaveToMongoDB() && ProjectsManagerSingleton.getProjectsManagerSingleton().checkIfAlreadyExists(projectRootPath.getProjectName(), adjustedTagName)) {
                logger.info("Project " + projectRootPath.getProjectName() + "-" + adjustedTagName + " is already in the database. Skipping!");
                continue;
            }


            prepareProject(projectRootPath, adjustedTagName);

            String tagPath = projectRootPath.getFullPath() + "-" + "["+clearTag(adjustedTagName)+"]";


            Path root = Paths.get(tagPath);

            ProjectRoot projectRoot = null;
            CombinedTypeExtractor cte = null;
            ModelExtractor me = null;

            try {
                //projectRoot = new ParserCollectionStrategy().collect(root);
                projectRoot = new ParserCollectionStrategy().collect(root);
                //cte = new CombinedTypeExtractor(projectRoot, ProjectsManagerSingleton.getProjectsManagerSingleton().getJAR_PATH());
                me = new ModelExtractor(cte, projectsConfiguration.isSaveToMongoDB());
            } catch (Exception e){
                e.printStackTrace();
            }

            boolean skipPathFlag = true;

            for (SourceRoot sRoot : projectRoot.getSourceRoots()) {
                String sourceRootPath = sRoot.getRoot().toString().replace(root.toString(), "");

                List<String> jsonSourceRoots = projectRootPath.getSourceRoots();
                if (!jsonSourceRoots.get(0).equals("all")) {
                    skipPathFlag = true;
                    for (String jsonSourceRoot : jsonSourceRoots) {
                        if (sourceRootPath.contains(File.separator + jsonSourceRoot)) {
                            skipPathFlag = false;
                            break;
                        }
                    }
                    if (skipPathFlag) {
                        logger.info("*** Skipping the analysis of Source Root: " + sourceRootPath + " ***");
                        continue;
                    }

                }
                logger.info("*** Starting the analysis of Source Root: " + sourceRootPath + " ***");

                List<CompilationUnit> allCus = new LinkedList<>();
                List<ParseResult<CompilationUnit>> parseResults = null;
                try {
                    parseResults = sRoot.tryToParse();
                    List<CompilationUnit> parsialCus = parseResults.stream()
                            .filter(ParseResult::isSuccessful)
                            .map(r -> r.getResult().get())
                            .collect(Collectors.toList());
                    allCus.addAll(parsialCus);
                } catch (IOException e) {
                    logger.error(e.toString());
                } catch (Exception e) {
                    logger.error(e.toString());
                }


                startVisitors(allCus, cte, me, sourceRootPath);

                logger.info("*** The analysis of Source " + sourceRootPath + " is complete. ***");
                System.gc();
            }
            logger.info("*** The analysis of project " + projectRootPath.getProjectName() + " is complete. ***");

            Double tagCoverage = null;
            if(projectsConfiguration.isTryToExtractCoverage()){
                CoverageExtractor coverageExtractor = new CoverageExtractor(projectRootPath, tagPath, me, projectsConfiguration.isSaveToMongoDB(), false);
                coverageExtractor.tryToExtractCoverage();
                tagCoverage = coverageExtractor.getTagCoverage();
            }
            StatisticsExtractor allProjectStatistics = getStatistics(cte, me, projectsConfiguration.isSaveToMongoDB());
            ProjectsDataWrapper dataWrapper = new ProjectsDataWrapper(projectRootPath, projectRootPath.getProjectName(), tagPath, adjustedTagName, tagCoverage ,projectRootPath.getTags().get(tag), projectRootPath.getSourceRoots(), me, allProjectStatistics);
            ProjectsManagerSingleton.prettyPrintOutputToJsonToFile(dataWrapper, projectRootPath.getProjectName() + "-" + clearTag(adjustedTagName), tagPath);
            if (projectsConfiguration.isSaveToMongoDB()) {
                ProjectsManagerSingleton.getProjectsManagerSingleton().saveToMongoDB(dataWrapper);
            } else {
                projectsDataWrappers.add(dataWrapper);
            }
            allProjectStatistics = null;
            dataWrapper = null;

        }

        return projectsDataWrappers;
    }


    private void prepareProject(ProjectConfig projectRootPath, String tag) {
        Path tagPath = Paths.get( projectRootPath.getFullPath() + '-' + "[" +clearTag(tag) + "]");
        logger.info("Checking if the project has already been downloaded " + tagPath.toString());

        if (Files.exists(tagPath)) {
            logger.info("The project " + tagPath.toString() + " already exists!\n\n");
            if(projectsConfiguration.isSaveToMongoDB()){
                projectsManagerSingleton.updateProjectDownloadStatus(projectRootPath.getProjectName(), tag, "success", "Project already exists", tagPath.toString());
            }
            return;
        }

        logger.info("Project " + tagPath.toString() + " does not exists. Downloading repository.");
        Git git = null;
        try {
            git = Git.cloneRepository()
                    .setURI(projectRootPath.getGitRepo())
                    .setDirectory(tagPath.toFile())
                    .setBranchesToClone(singleton(tag))
                    .setBranch(tag)
                    .call();
        } catch (Exception e) {
            logger.error("Download of project " + tagPath.toString() + " failed!");
            logger.error(e.toString());
            if(projectsConfiguration.isSaveToMongoDB()){
                projectsManagerSingleton.updateProjectDownloadStatus(projectRootPath.getProjectName(), tag, "failure", e.toString(), tagPath.toString());
            }
        }


        if(git != null){
            logger.info("Download of project " + tagPath.toString() + " successfully finished.\n\n");
            if(projectsConfiguration.isSaveToMongoDB()){
                projectsManagerSingleton.updateProjectDownloadStatus(projectRootPath.getProjectName(), tag, "success", "download complete.", tagPath.toString());
            }
            git.getRepository().close();
            git.close();
        }


    }


    public String clearTag(String tag) {
        //used to remove invalid characters to be used in windows paths
        String clearTagName = tag.replaceAll(allowedCharacters, "");
        return clearTagName;

    }

    public void startDownload() {
        for (ProjectConfig projectRootPath : projectsConfiguration.getProjects()) {
            for (String tag : projectRootPath.getTags().keySet()) {
                prepareProject(projectRootPath,tag.replace("#", "."));
            }
        }
    }

    private StatisticsExtractor getStatistics(CombinedTypeExtractor cte, ModelExtractor me, boolean saveToMongoDB) {
        StatisticsExtractor statistics = new StatisticsExtractor(cte, me, saveToMongoDB);
        statistics.calculateStatistics();
        return statistics;

    }

    private void prettyPrint(CompilationUnit cu) {
        YamlPrinter printer = new YamlPrinter(true);
        logger.info(printer.output(cu));
    }


    private void startVisitors(List<CompilationUnit> allCus, CombinedTypeExtractor cte, ModelExtractor me, String sourceRootPath) {
        List<VoidVisitor<Void>> visitors = new LinkedList<>();
        visitors.add(new NewExeceptionVisitor(cte, me, sourceRootPath));
        visitors.add(new ExpectedAnnotationVisitor(cte, me, sourceRootPath));
        visitors.add(new ExpectExceptionCallVisitor(cte, me, sourceRootPath));
        visitors.add(new Commom_FailCallVisitor(cte, me, sourceRootPath));
        visitors.add(new TestCaseVisitor(cte, me, sourceRootPath));
        visitors.add(new ThrowsExceptionOnMethodVisitor(cte, me, sourceRootPath));
        visitors.add(new ThrowsExceptionOnConstructorVisitor(cte, me, sourceRootPath));
        visitors.add(new ThrowExceptionVisitor(cte, me, sourceRootPath));
        visitors.add(new CatchVisitor(cte, me, sourceRootPath));
        visitors.add(new AssertThrowsVisitor(cte, me, sourceRootPath));
        visitors.add(new AssertJ_assertThatThrownByVisitor(cte, me, sourceRootPath));
        visitors.add(new AssertJ_assertThatExceptionOfTypeVisitor(cte, me, sourceRootPath));
        visitors.add(new AssertJ_assertThatExceptionNameVisitor(cte, me, sourceRootPath));
        visitors.add(new AssertJ_assertThatVisitor(cte, me, sourceRootPath));
        visitors.add(new TestNG_ExpectedExceptionsAnnotationVisitor(cte, me, sourceRootPath));


        for (CompilationUnit cu : allCus) {
            for (VoidVisitor<Void> visitor : visitors) {
                visitor.visit(cu, null);
            }

        }


    }
}
