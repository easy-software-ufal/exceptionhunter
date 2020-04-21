package br.ufal.easy.exceptionhunter;

import com.google.gson.annotations.Expose;
import br.ufal.easy.exceptionhunter.extractors.ModelExtractor;
import br.ufal.easy.exceptionhunter.extractors.StatisticsExtractor;

import java.util.List;

public class ProjectsDataWrapper {
    @Expose
    public String projectName;

    public String sourceRootPath;

    @Expose
    public String tag;

    @Expose
    public Double tagCoverage;

    @Expose
    public String tagCreatedAt;

    public List<String> sourcesPaths;

    @Expose
    private ProjectConfig projectDetails;

    //@Expose
    private ModelExtractor models;

    @Expose
    private StatisticsExtractor statistics;



    public ProjectsDataWrapper(ProjectConfig projectRootPath, String projectName, String sourceRootPath, String tag, Double tagCoverage, String tagCreatedAt, List<String> sourcesPaths, ModelExtractor models, StatisticsExtractor statistics) {
        this.projectDetails = projectRootPath;
        this.projectName = projectName;
        this.sourceRootPath = sourceRootPath;
        this.tag = tag;
        this.tagCoverage = tagCoverage;
        this.sourcesPaths = sourcesPaths;
        this.models = models;
        this.statistics = statistics;
        this.tagCreatedAt = tagCreatedAt;
    }

    public String getProjectName() {
        return projectName;
    }

    public void setProjectName(String projectName) {
        this.projectName = projectName;
    }

    public String getSourceRootPath() {
        return sourceRootPath;
    }

    public void setSourceRootPath(String sourceRootPath) {
        this.sourceRootPath = sourceRootPath;
    }

    public String getTag() {
        return tag;
    }

    public void setTag(String tag) {
        this.tag = tag;
    }

    public List<String> getSourcesPaths() {
        return sourcesPaths;
    }

    public void setSourcesPaths(List<String> sourcesPaths) {
        this.sourcesPaths = sourcesPaths;
    }

    public ModelExtractor getModels() {
        return models;
    }

    public void setModels(ModelExtractor models) {
        this.models = models;
    }

    public StatisticsExtractor getStatistics() {
        return statistics;
    }

    public void setStatistics(StatisticsExtractor statistics) {
        this.statistics = statistics;
    }

    public ProjectConfig getProjectDetails() {
        return projectDetails;
    }

    public void setProjectDetails(ProjectConfig projectDetails) {
        this.projectDetails = projectDetails;
    }

    public String getTagCreatedAt() {
        return tagCreatedAt;
    }

    public void setTagCreatedAt(String tagCreatedAt) {
        this.tagCreatedAt = tagCreatedAt;
    }

    public Double getTagCoverage() {
        return tagCoverage;
    }

    public void setTagCoverage(Double tagCoverage) {
        this.tagCoverage = tagCoverage;
    }

    @Override
    public String toString() {
        return "ProjectsDataWrapper{" +
                "projectName='" + projectName + '\'' +
                ", sourceRootPath='" + sourceRootPath + '\'' +
                ", tag='" + tag + '\'' +
                ", tagCoverage=" + tagCoverage +
                ", tagCreatedAt='" + tagCreatedAt + '\'' +
                ", sourcesPaths=" + sourcesPaths +
                ", projectDetails=" + projectDetails +
                ", models=" + models +
                ", statistics=" + statistics +
                '}';
    }
}
