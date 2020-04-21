package br.ufal.easy.exceptionhunter.models.testng;

import com.google.gson.annotations.Expose;
import br.ufal.easy.exceptionhunter.models.AbstractOrdinaryModel;

import java.util.LinkedList;
import java.util.List;

/**
 * Salva o nome da exceção encontrada no @Test(expected=XXX.class)
 */
public class TestNG_ExpectedExceptionsTestAnnotationModel extends AbstractOrdinaryModel {

    @Expose
    private List<String> expectedExceptionsNames;


    public TestNG_ExpectedExceptionsTestAnnotationModel() {
        super();
        this.expectedExceptionsNames = new LinkedList<>();
    }


    public List<String> getExpectedExceptionsNames() {
        return expectedExceptionsNames;
    }

    public void setExpectedExceptionsNames(List<String> expectedExceptionsNames) {
        this.expectedExceptionsNames = expectedExceptionsNames;
    }

    @Override
    public String toString() {
        return "TestNG_ExpectedExceptionsTestAnnotationModel{" +
                "expectedExceptionsNames=" + expectedExceptionsNames +
                '}';
    }
}

