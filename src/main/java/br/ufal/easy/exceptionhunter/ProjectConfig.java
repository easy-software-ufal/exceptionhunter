package br.ufal.easy.exceptionhunter;

import com.google.gson.annotations.Expose;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;
import java.util.Map;

public class ProjectConfig {

    private String projectName;
    @Expose
    private String gitRepo;
    @Expose
    private String projectOwner;
    @Expose
    private String includedAt;
    @Expose
    private int stars;

    private Map<String, String> tags;
    @Expose
    private String description;
    @Expose
    private String createdAt;
    @Expose
    private String lastUpdatedAt;
    @Expose
    private int size;
    @Expose
    private String domain;
    @Expose
    private String platform;
    @Expose
    private int contributors;

    private String fullPath;

    @Expose
    private List<String> sourceRoots;

    private boolean active;

    public ProjectConfig(String projectName, String gitRepo, String projectOwner, String includedAt, int stars, Map<String, String> tags, String description, String createdAt, String lastUpdatedAt, int size, String domain, String platform, int contributors, String fullPath, List<String> sourceRoots, boolean active) throws ParseException {
        this.projectName = projectName;
        this.gitRepo = gitRepo;
        this.projectOwner = projectOwner;
        this.includedAt =  includedAt;
        this.stars = stars;
        this.tags = tags;
        this.description = description;
        this.createdAt = createdAt;
        this.lastUpdatedAt = lastUpdatedAt;
        this.size = size;
        this.domain = domain;
        this.platform = platform;
        this.contributors = contributors;
        this.fullPath = fullPath;
        this.sourceRoots = sourceRoots;
        this.active = active;
    }

    public String getGitRepo() {
        return gitRepo;
    }

    public void setGitRepo(String gitRepo) {
        this.gitRepo = gitRepo;
    }

    public String getProjectName() {
        return projectName;
    }

    public void setProjectName(String projectName) {
        this.projectName = projectName;
    }

    public boolean isActive() {
        return active;
    }

    public void setActive(boolean active) {
        this.active = active;
    }

    public String getFullPath() {
        return fullPath;
    }

    public void setFullPath(String fullPath) {
        this.fullPath = fullPath;
    }

    public Map<String, String> getTags() {
        return tags;
    }

    public void setTags(Map<String, String> tags) {
        this.tags = tags;
    }

    public String getProjectOwner() {
        return projectOwner;
    }

    public void setProjectOwner(String projectOwner) {
        this.projectOwner = projectOwner;
    }

    public List<String> getSourceRoots() {
        return sourceRoots;
    }

    public void setSourceRoots(List<String> sourceRoots) {
        this.sourceRoots = sourceRoots;
    }

    public int getStars() {
        return stars;
    }

    public void setStars(int stars) {
        this.stars = stars;
    }

    public String getIncludedAt() {
        return includedAt;
    }

    public void setIncludedAt(String includedAt) {
        this.includedAt = includedAt;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(String createdAt) {
        this.createdAt = createdAt;
    }

    public String getLastUpdatedAt() {
        return lastUpdatedAt;
    }

    public void setLastUpdatedAt(String lastUpdatedAt) {
        this.lastUpdatedAt = lastUpdatedAt;
    }

    public int getSize() {
        return size;
    }

    public void setSize(int size) {
        this.size = size;
    }

    public String getDomain() {
        return domain;
    }

    public void setDomain(String domain) {
        this.domain = domain;
    }

    public int getContributors() {
        return contributors;
    }

    public void setContributors(int contributors) {
        this.contributors = contributors;
    }

    public String getPlatform() {
        return platform;
    }

    public void setPlatform(String platform) {
        this.platform = platform;
    }

}

