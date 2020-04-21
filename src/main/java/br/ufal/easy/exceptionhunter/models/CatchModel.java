package br.ufal.easy.exceptionhunter.models;


import com.google.gson.annotations.Expose;

import java.util.ArrayList;
import java.util.List;

/**
 * Armazena dados encontrador a partir dos nós de um Try...Catch
 */
public class CatchModel extends AbstractOrdinaryModel {

    //Armazena as exceções esperadas pelos catchs
    @Expose
    public List<String> catchedExceptions;
    //Identfica uma lista de catchs "mães", pois é possível haver um catch dentro de um outro catch que está dentro de outro catch.
    //A organização é CatchA( onde está o nó alvo da busca do visitor), CatchB (mãe de A), CatchC (mãe de B)
    @Expose
    private List<String> parentCatch;

    public CatchModel() {
        parentCatch = new ArrayList<String>();
        catchedExceptions = new ArrayList<String>();
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

    public void addParentCatch(String catchName) {
        this.parentCatch.add(catchName);
    }

    public List<String> getParentCatch() {
        return parentCatch;
    }

    public void setParentCatch(List<String> parentCatch) {
        this.parentCatch = parentCatch;
    }

    @Override
    public String toString() {
        return "CatchModel{" +
                "parentCatch=" + parentCatch +
                ", catchedExceptions=" + catchedExceptions +
                '}';
    }
}
