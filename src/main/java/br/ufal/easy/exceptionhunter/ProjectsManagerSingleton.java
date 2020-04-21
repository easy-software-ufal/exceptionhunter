package br.ufal.easy.exceptionhunter;

import com.github.javaparser.ast.Node;
import com.github.javaparser.printer.YamlPrinter;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.mongodb.BasicDBObject;
import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoClients;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import org.bson.Document;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.*;
import java.util.ArrayList;
import java.util.List;

public class ProjectsManagerSingleton {

    private static Logger logger = LoggerFactory.getLogger("ExceptionHunter");
    private static ProjectsManagerSingleton projectManager;
    private boolean saveToMongo = false;
    private String OS_NAME;
    private String JAR_PATH;
    private List<ProjectConfig> fullProjectsPath;
    // Creating a Mongo client
    private MongoClient mongoClient;
    private MongoDatabase mongoDatabase;
    private MongoCollection<Document> analysisMongoCollection;
    private MongoCollection<Document> downloadMongoCollection;

    private ProjectsManagerSingleton() {
        OS_NAME = System.getProperty("os.name");
        fullProjectsPath = new ArrayList<>();

    }

    public boolean checkIfAlreadyExists(String projectName, String tag){
        BasicDBObject whereQuery = new BasicDBObject();
        whereQuery.put("projectName", projectName);
        whereQuery.put("tag", tag);
        Document myDoc = analysisMongoCollection.find(whereQuery).first();
        if( myDoc != null){
            return true;
        }
        return false;
    }

    public void updateProjectDownloadStatus(String projectName, String tag, String status, String message, String path){
        //MongoCollection<Document> gitCloneCollection = mongoDatabase.getCollection("GitCloneStatus_top100_per_domain");
        Document doc = new Document("projectName", projectName)
                .append("tag", tag)
                .append("status", status)
                .append("message", message)
                .append("path", path);
        downloadMongoCollection.insertOne(doc);
        logger.info("Download status of " + projectName + "[" + tag + "]" +" saved to mongo successfully.");
    }

    public static ProjectsManagerSingleton getProjectsManagerSingleton() {
        if (projectManager == null) {
            projectManager = new ProjectsManagerSingleton();
        }
        return projectManager;
    }

    public static void prettyPrintNodeYaml(Node node) {
        YamlPrinter printer = new YamlPrinter(true);
        //System.out.println(printer.output(node));

    }

    public static void prettyPrintOutputToJson(ProjectsDataWrapper se) {
        Gson gson = new GsonBuilder().excludeFieldsWithoutExposeAnnotation().serializeNulls().setPrettyPrinting().create();
        String result = gson.toJson(se);

    }

    public void saveToMongoDB(ProjectsDataWrapper se) {
        Gson gson = new GsonBuilder().excludeFieldsWithoutExposeAnnotation().serializeNulls().setPrettyPrinting().create();
        String result = gson.toJson(se);
        Document doc = Document.parse(result);
        analysisMongoCollection.insertOne(doc);
        logger.info("New document inserted in mongoDB.");

    }

    public static void prettyPrintOutputToJsonToFile(ProjectsDataWrapper se, String fileName, String path) {
        String fullPath = path + File.separator + fileName + ".json";
        try (Writer writer = new FileWriter(fullPath)) {
            Gson gson = new GsonBuilder().excludeFieldsWithoutExposeAnnotation().serializeNulls().setPrettyPrinting().create();
            gson.toJson(se, writer);
            logger.info("Saving the results to " + fullPath);
        } catch (IOException e) {
            e.printStackTrace();
        }

    }

    public ProjectsConfiguration getProjectsConfiguration(String projectsJsonPath) {
        logger.info("Trying to read the configuration file " + projectsJsonPath);
        List<ProjectConfig> fullProjectsPath = new ArrayList<>();
        String projectsRoot = null;
        Gson gson = new GsonBuilder().create();
        ProjectsConfiguration projectsConfiguration = null;


        try {
            //Reader reader = new InputStreamReader(ProjectsManagerSingleton.class.getClass().getResourceAsStream(projectsJsonPath), "UTF-8");
            projectsConfiguration = gson.fromJson(new FileReader(projectsJsonPath), ProjectsConfiguration.class);
        } catch (FileNotFoundException e) {
            e.printStackTrace();
            logger.info(e.getMessage());
        } catch (NullPointerException e){
            e.printStackTrace();
            logger.info(e.getMessage());
        }

        if (OS_NAME.contains("Windows")) {
            projectsRoot = projectsConfiguration.getWindowsProjectsRoot();
        } else {
            projectsRoot = projectsConfiguration.getUnixLikeProjectsRoot();
        }

        for (ProjectConfig project : projectsConfiguration.getProjects()) {
            try{
                project.setFullPath(projectsRoot + File.separator + project.getProjectName());
                fullProjectsPath.add(project);
            } catch (Exception e){
                e.printStackTrace();
            }

        }
        projectsConfiguration.setProjects(fullProjectsPath);

        return projectsConfiguration;
    }


    public void configureMongoDB(String mongoConnectionString, String mongoDatabaseName, String mongoCollectionName) {
//        mongoClient = MongoClients.create("mongodb://localhost:27017");
//        mongoDatabase = mongoClient.getDatabase("ExceptionHunter");
//        mongoCollection = mongoDatabase.getCollection("MongoDB_Top100_per_domain");
        mongoClient = MongoClients.create(mongoConnectionString);
        mongoDatabase = mongoClient.getDatabase(mongoDatabaseName);
        analysisMongoCollection = mongoDatabase.getCollection(mongoCollectionName);
        downloadMongoCollection = mongoDatabase.getCollection("GitCloneStatus_" + mongoCollectionName);
    }

    public boolean isSaveToMongo() {
        return saveToMongo;
    }

    public void setSaveToMongo(boolean saveToMongo) {
        this.saveToMongo = saveToMongo;
    }
}
