package br.ufal.easy.exceptionhunter.models.junit;

import com.google.gson.annotations.Expose;
import br.ufal.easy.exceptionhunter.models.AbstractOrdinaryModel;

/**
 * Salva o nome da exceção encontrada como parametro na chamada ao método expect(XXX.class)
 */
public class JUnit_ExpectExceptionTestCallModel extends AbstractOrdinaryModel {

    @Expose
    private String expectedExceptionName;


    public JUnit_ExpectExceptionTestCallModel() {

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
        return "JUnit_ExpectExceptionTestCallModel{" +
                "expectedExceptionName='" + expectedExceptionName + '\'' +
                '}' + " " + super.toString();
    }
}

