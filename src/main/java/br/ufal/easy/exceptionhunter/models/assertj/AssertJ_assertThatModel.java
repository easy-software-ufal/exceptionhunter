package br.ufal.easy.exceptionhunter.models.assertj;

import com.google.gson.annotations.Expose;
import br.ufal.easy.exceptionhunter.models.AbstractOrdinaryModel;

/**
 * Salva o nome da exceção passada como argumento ao metoodo assertThatThrownBy do AssertJ
 */
public class AssertJ_assertThatModel extends AbstractOrdinaryModel {


    @Expose
    private String expectedExceptionName;


    public AssertJ_assertThatModel() {

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
        return "AssertJ_assertThatModel{" +
                "expectedExceptionName='" + expectedExceptionName + '\'' +
                '}';
    }
}

