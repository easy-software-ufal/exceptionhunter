package br.ufal.easy.exceptionhunter;


import java.util.List;

public class ProjectsConfiguration {

    public String windowsProjectsRoot;
    public String unixLikeProjectsRoot;
    public boolean saveToMongoDB;
    public boolean newestTagOnly;
    public boolean tryToExtractCoverage;
    public String mongoConnectionString;
    public String mongoDatabaseName;
    public String mongoCollectionName;
    public List<ProjectConfig> projects;

    public String getWindowsProjectsRoot() {
        return windowsProjectsRoot;
    }

    public void setWindowsProjectsRoot(String windowsProjectsRoot) {
        this.windowsProjectsRoot = windowsProjectsRoot;
    }

    public String getUnixLikeProjectsRoot() {
        return unixLikeProjectsRoot;
    }

    public void setUnixLikeProjectsRoot(String unixLikeProjectsRoot) {
        this.unixLikeProjectsRoot = unixLikeProjectsRoot;
    }

    public boolean isTryToExtractCoverage() {
        return tryToExtractCoverage;
    }

    public void setTryToExtractCoverage(boolean tryToExtractCoverage) {
        this.tryToExtractCoverage = tryToExtractCoverage;
    }

    public boolean isSaveToMongoDB() {
        return saveToMongoDB;
    }

    public void setSaveToMongoDB(boolean saveToMongoDB) {
        this.saveToMongoDB = saveToMongoDB;
    }

    public boolean isNewestTagOnly() {
        return newestTagOnly;
    }

    public void setNewestTagOnly(boolean newestTagOnly) {
        this.newestTagOnly = newestTagOnly;
    }

    public String getMongoConnectionString() {
        return mongoConnectionString;
    }

    public void setMongoConnectionString(String mongoConnectionString) {
        this.mongoConnectionString = mongoConnectionString;
    }

    public String getMongoDatabaseName() {
        return mongoDatabaseName;
    }

    public void setMongoDatabaseName(String mongoDatabaseName) {
        this.mongoDatabaseName = mongoDatabaseName;
    }

    public String getMongoCollectionName() {
        return mongoCollectionName;
    }

    public void setMongoCollectionName(String mongoCollectionName) {
        this.mongoCollectionName = mongoCollectionName;
    }

    public List<ProjectConfig> getProjects() {
        return projects;
    }

    public void setProjects(List<ProjectConfig> projects) {
        this.projects = projects;
    }

    @Override
    public String toString() {
        return "ProjectsConfiguration{" +
                "windowsProjectsRoot='" + windowsProjectsRoot + '\'' +
                ", unixLikeProjectsRoot='" + unixLikeProjectsRoot + '\'' +
                ", saveToMongoDB=" + saveToMongoDB +
                ", newestTagOnly=" + newestTagOnly +
                ", tryToExtractCoverage=" + tryToExtractCoverage +
                ", mongoConnectionString='" + mongoConnectionString + '\'' +
                ", mongoDatabaseName='" + mongoDatabaseName + '\'' +
                ", mongoCollectionName='" + mongoCollectionName + '\'' +
                ", projects=" + projects +
                '}';
    }
}

