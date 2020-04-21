package br.ufal.easy.exceptionhunter.models.junit;

import com.google.gson.annotations.Expose;
import br.ufal.easy.exceptionhunter.models.AbstractOrdinaryModel;

/**
 * Salva o nome da exceção encontrada no @Test(expected=XXX.class)
 */
public class JUnit_ExpectedExceptionTestAnnotationModel extends AbstractOrdinaryModel {

    @Expose
    private String expectedExceptionName;


    public JUnit_ExpectedExceptionTestAnnotationModel() {

        super();
    }

    public String getExpectedExceptionName() {
        return expectedExceptionName;
    }

    public void setExpectedExceptionName(String expectedExceptionName) {
        this.expectedExceptionName = expectedExceptionName;
    }

    @Override
    public String toString() {
        return "JUnit_ExpectedExceptionTestAnnotationModel{" +
                "expectedExceptionName='" + expectedExceptionName + '\'' +
                '}' + " " + super.toString();
    }
}

