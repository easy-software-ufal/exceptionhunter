package br.ufal.easy.exceptionhunter.models.junit;

import com.google.gson.annotations.Expose;
import br.ufal.easy.exceptionhunter.models.AbstractOrdinaryModel;

/**
 * Salva o nome da exceção passada como argumento ao metoodo assertThrows
 */
public class JUnit_assertThrowsModel extends AbstractOrdinaryModel {


    @Expose
    private String expectedExceptionName;
    @Expose
    private String message;


    public JUnit_assertThrowsModel() {

        super();
    }

    public String getExpectedExceptionName() {
        return expectedExceptionName;
    }

    public void setExpectedExceptionName(String expectedExceptionName) {
        this.expectedExceptionName = expectedExceptionName;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    @Override
    public String toString() {
        return "JUnit_assertThrowsModel{" +
                "expectedExceptionName='" + expectedExceptionName + '\'' +
                ", message='" + message + '\'' +
                '}';
    }
}

