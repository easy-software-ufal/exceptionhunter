package br.ufal.easy.exceptionhunter;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.util.List;

/**
 * The Main class that starts the analysis process
 */
public class ExceptionHunterMain {

    public static void main(String[] args) throws IOException {
        Logger logger = LoggerFactory.getLogger("ExceptionHunter");


        boolean downloadOnly = false;
        String jsonPath = ProjectsManagerSingleton.class.getClassLoader().getResource("projects.json").getPath();


        if (args.length == 1){
            jsonPath = args[0];
            logger.info("JSON's default path changed to " + jsonPath);
        }

        logger.info("Starting the analysis of the projects in the file  " + jsonPath);

        ProjectsConfiguration projectsConfiguration = ProjectsManagerSingleton.getProjectsManagerSingleton().getProjectsConfiguration(jsonPath);
        List<ProjectConfig> projects = projectsConfiguration.getProjects();

        logger.info("Should the data be saved on MongoDB? " + projectsConfiguration.isSaveToMongoDB());
        logger.info("Should try to extract coverage data? " + projectsConfiguration.isTryToExtractCoverage());

        ProjectMain pjMain = new ProjectMain(projectsConfiguration);
        if(downloadOnly){
            //In this case, the repository is only downloaded, but not analyzed
            pjMain.startDownload();
        } else {
            pjMain.proceedWithAnalysis();
        }

    }


}

