package br.ufal.easy.exceptionhunter.models;

import com.google.gson.annotations.Expose;


public class ThrowExceptionModel extends AbstractOrdinaryModel {

    @Expose
    private String exception;

    @Expose
    //Line that contains the throw statement.
    public int throwStatementLine;

    //This value is the number of times that the line was executed, and “null” implies the line is not relevant.
    @Expose
    public Integer numberOfTimesTheLineWasExecuted;

    //TODO trocar Enum. Identifica o tipo de throw (NEW, RETHROW, STATIC_NEW, e outros)
    @Expose
    private String throwType;

    public String getException() {
        return exception;
    }

    public void setException(String exception) {
        this.exception = exception;
    }

    public String getThrowType() {
        return throwType;
    }

    public void setThrowType(String throwType) {
        this.throwType = throwType;
    }

    public int getThrowStatementLine() {
        return throwStatementLine;
    }

    public void setThrowStatementLine(int throwStatementLine) {
        this.throwStatementLine = throwStatementLine;
    }

    public Integer getNumberOfTimesTheLineWasExecuted() {
        return numberOfTimesTheLineWasExecuted;
    }

    public void setNumberOfTimesTheLineWasExecuted(Integer numberOfTimesTheLineWasExecuted) {
        this.numberOfTimesTheLineWasExecuted = numberOfTimesTheLineWasExecuted;
    }

    @Override
    public String toString() {
        return "ThrowExceptionModel{" +
                "exception='" + exception + '\'' +
                ", lineRange=" + throwStatementLine +
                ", numberOfTimesTheLineWasExecuted=" + numberOfTimesTheLineWasExecuted +
                ", throwType='" + throwType + '\'' +
                '}';
    }
}
