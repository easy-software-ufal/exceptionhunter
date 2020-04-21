package br.ufal.easy.exceptionhunter.models;

import com.google.gson.annotations.Expose;

/**
 * This model is for tests that extends TestCase
 */
public class OrdinaryExtendedTestModel extends AbstractOrdinaryModel {


    @Expose
    private String testMethodName;

    public String getTestMethodName() {
        return testMethodName;
    }

    public void setTestMethodName(String testMethodName) {
        this.testMethodName = testMethodName;
    }

    @Override
    public String toString() {
        return "OrdinaryExtendedTestModel{" +
                "testMethodName='" + testMethodName + '\'' +
                '}';
    }
}
