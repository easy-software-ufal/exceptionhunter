package br.ufal.easy.exceptionhunter.models;

import com.google.gson.annotations.Expose;


public class ThrowsExceptionModel extends AbstractOrdinaryModel {

    @Expose
    private String exception;

    public String getException() {
        return exception;
    }

    public void setException(String exception) {
        this.exception = exception;
    }

    @Override
    public String toString() {
        return "ThrowsExceptionModel{" +
                "exception='" + exception + '\'' +
                '}' + " " + super.toString();
    }
}
