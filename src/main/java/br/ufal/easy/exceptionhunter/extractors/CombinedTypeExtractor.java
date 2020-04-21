package br.ufal.easy.exceptionhunter.extractors;

import com.github.javaparser.symbolsolver.resolution.typesolvers.CombinedTypeSolver;
import com.github.javaparser.symbolsolver.resolution.typesolvers.JarTypeSolver;
import com.github.javaparser.symbolsolver.resolution.typesolvers.JavaParserTypeSolver;
import com.github.javaparser.symbolsolver.resolution.typesolvers.ReflectionTypeSolver;
import com.github.javaparser.utils.ProjectRoot;
import com.github.javaparser.utils.SourceRoot;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.File;
import java.io.IOException;

/**
 * Singleton dos solvers usados para identificar relações entre os nós da AST
 */
public class CombinedTypeExtractor {
    private CombinedTypeSolver combinedTypeSolver;
    private String JAR_PATH;
    private Logger logger = LoggerFactory.getLogger("ExceptionHunter");

    public CombinedTypeExtractor(ProjectRoot projectRoot, String jarPath) {
        combinedTypeSolver = new CombinedTypeSolver();
        this.JAR_PATH = jarPath;
        //this.JAR_PATH = "C:\\jars\\";


        for (SourceRoot sRoot : projectRoot.getSourceRoots()) {
            combinedTypeSolver.add(new JavaParserTypeSolver(sRoot.getRoot()));
        }
        combinedTypeSolver.add(new ReflectionTypeSolver());
        try {
            File[] jars = this.finder( JAR_PATH);

            for (File jar : jars) {
                logger.info("Adding " + jar.getAbsolutePath() + " to CombinedTypeSolver");
                combinedTypeSolver.add(new JarTypeSolver(jar.getAbsolutePath()));
            }
        } catch (IOException e) {
            logger.error(e.toString());
        }
    }


    private File[] finder(String dirName) {
        File rootDir = new File(dirName);
        return rootDir.listFiles((dir, filename) -> filename.endsWith(".jar"));
    }

    public CombinedTypeSolver getCombinedTypeSolver() {
        return combinedTypeSolver;
    }
}

