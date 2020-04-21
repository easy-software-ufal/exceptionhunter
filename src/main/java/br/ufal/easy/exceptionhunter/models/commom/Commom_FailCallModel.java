package br.ufal.easy.exceptionhunter.models.commom;


import com.google.gson.annotations.Expose;
import br.ufal.easy.exceptionhunter.models.AbstractOrdinaryModel;

import java.util.ArrayList;
import java.util.List;

/**
 * Armazena dados encontrador a partir dos nós de chamada ao método fail
 */
public class Commom_FailCallModel extends AbstractOrdinaryModel {

    //Argumentos passados na chamada de método. Geralmente são strings de comentários
    @Expose
    public String failCallArgument;

    //Armazena as exceções esperadas pelos catchs
    @Expose
    public List<String> catchedExceptions;

    //Identifica se a chamada ao fail foi realizada dentro do try ou catch
    public String tryCatchScope;

    public Commom_FailCallModel() {
        catchedExceptions = new ArrayList<String>();
    }

    public String getFailCallArgument() {
        return failCallArgument;
    }

    public void setFailCallArgument(String failCallArgument) {
        this.failCallArgument = failCallArgument;
    }

    public String getTryCatchScope() {
        return tryCatchScope;
    }

    public void setTryCatchScope(String tryCatchScope) {
        this.tryCatchScope = tryCatchScope;
    }

    public List<String> getCatchedExceptions() {
        return catchedExceptions;
    }

    public void setCatchedExceptions(List<String> catchedExceptions) {
        this.catchedExceptions = catchedExceptions;
    }

    public void addCatchedException(String exceptionName) {
        this.catchedExceptions.add(exceptionName);
    }


    @Override
    public String toString() {
        return "Commom_FailCallModel{" +
                "failCallArgument='" + failCallArgument + '\'' +
                ", tryCatchScope='" + tryCatchScope + '\'' +
                ", catchedExceptions=" + catchedExceptions +
                '}' + " " + super.toString();
    }
}
