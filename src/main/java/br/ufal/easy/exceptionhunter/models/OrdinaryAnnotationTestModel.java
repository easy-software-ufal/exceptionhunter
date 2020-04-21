package br.ufal.easy.exceptionhunter.models;

import com.google.gson.annotations.Expose;

/**
 * This model is model is for tests that are annotated with @Test
 */
public class OrdinaryAnnotationTestModel extends AbstractOrdinaryModel {


    @Expose
    private String annotation;
    @Expose
    private String testMethodName;

    public String getAnnotation() {
        return annotation;
    }

    public void setAnnotation(String annotation) {
        this.annotation = annotation;
    }

    public String getTestMethodName() {
        return testMethodName;
    }

    public void setTestMethodName(String testMethodName) {
        this.testMethodName = testMethodName;
    }

    @Override
    public String toString() {
        return "OrdinaryAnnotationTestModel{" +
                "testMethodName='" + testMethodName + '\'' +
                ", annotation='" + annotation + '\'' +
                '}';
    }
}
