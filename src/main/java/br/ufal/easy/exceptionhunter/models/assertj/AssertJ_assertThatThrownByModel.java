package br.ufal.easy.exceptionhunter.models.assertj;

import com.google.gson.annotations.Expose;
import br.ufal.easy.exceptionhunter.models.AbstractOrdinaryModel;

/**
 * Salva o nome da exceção passada como argumento ao metoodo assertThatThrownBy do AssertJ
 */
public class AssertJ_assertThatThrownByModel extends AbstractOrdinaryModel {


    @Expose
    private String expectedExceptionName;


    public AssertJ_assertThatThrownByModel() {

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
        return "AssertJModel{" +
                "expectedExceptionName='" + expectedExceptionName + '\'' +
                '}';
    }
}

