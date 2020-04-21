package br.ufal.easy.exceptionhunter.models;

import com.google.gson.annotations.Expose;

/**
 * This model identifies CustomExceptions
 */
public class NewExceptionModel extends AbstractOrdinaryModel {

    @Expose
    String type = "NewExceptionModel";

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    @Override
    public String toString() {
        return "NewExceptionModel{" +
                "type='" + type + '\'' +
                '}';
    }
}
