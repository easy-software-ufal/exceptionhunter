package br.ufal.easy.exceptionhunter.models;

import com.github.javaparser.ast.Node;
import com.google.gson.annotations.Expose;

import java.io.File;
import java.util.HashMap;
import java.util.Map;

/**
 * Essa classe é usada como modelo para todas as outras. Nela estão as variáveis que são comuns a todos os modelos.
 * Aqui estão armazenados informações mais genéricas a respeito dos testes
 */
public abstract class AbstractOrdinaryModel {

    //identifies the file name. E.g., /src/app/Class.java
    @Expose
    private String fullFilePath;
    //Identfica uma lista de classes "mães", pois é possível haver um classe dentro de uma classe que está dentro de outra classe.
    //A organização é ClasseA( onde está o nó alvo da busca do visitor), ClasseB (mãe de A), ClasseC (mãe de B) (de 0 a n)
    @Expose
    private Map<Integer, String> parentClassName;
    //Identfica uma lista de métodos "mães", pois é possível haver um método dentro de outro
    //A organização é MétodoA( onde está o nó alvo da busca do visitor), MétodoB (mãe de A), MétodoC (mãe de B)
    @Expose
    private Map<Integer, String> parentMethodName;
    //Armazena o NÓ retornado pelo visitor para possibilitar o análises posteriores - Ao armazenar o Nó uma grande
    //quantidade de memoria é usada. Por isso, apesar deste campo existir, nao esta sendo setado no ModeleExtractor
    @Expose
    private Node node;
    //Identifica o pacote onde está o nó alvo
    @Expose
    private String packageName;
    //Armazena o diretorio onde o SourceRoot ou TestRoot é iniciado
    @Expose
    private String rootPath;
    //flag que identifica se o nó alvo está dentro de método com anotação @Test
    @Expose
    private boolean isInsideATestMethod = false;

    //Flag que identifica instruções que estão em algum lugar dentro de um TestRoot
    @Expose
    private boolean isInsideATestFolder = false;

    //flag que identifica os métodos que começam com "test"
    @Expose
    private boolean isTheMethodNameStartingWithTest = false;

    @Expose
    private boolean hasModelCoverageData = false;

    //Identifica a classe mae
    @Expose
    private String extendsFrom;

    //Identifica os pacotes
    @Expose
    private boolean importsFromJUnit;

    //Identifica os pacotes
    @Expose
    private boolean importsFromTestNG;

    //Identifica os pacotes
    private boolean importsFromAssertJ;
    @Expose
    Boolean isAnError = false;


    public AbstractOrdinaryModel() {
        parentMethodName = new HashMap<>();
        parentClassName = new HashMap<>();
    }

    public Node getNode() {
        return node;
    }

    public void setNode(Node node) {
        this.node = node;
    }

    public void addParentMethodName(String methodName) {
        this.parentMethodName.put(this.parentMethodName.size(), methodName);
    }

    public void addParentClassName(String className) {

        this.parentClassName.put(this.parentClassName.size(), className);
    }

    public Map<Integer, String> getParentMethodName() {
        return parentMethodName;
    }

    public String getParentMethodName(int index) {
        return parentMethodName.get(new Integer(index));
    }


    public String getPackageName() {
        return packageName;
    }

    public void setPackageName(String packageName) {
        this.packageName = packageName;
    }

    public boolean isInsideATest() {
        if (isInsideATestFolder || isInsideATestMethod) {
            return true;
        }
        return false;
    }

    public boolean isInsideAJUnitTest() {
        if (importsFromJUnit && isInsideATest()) {
            return true;
        }
        return false;
    }

    public boolean isInsideATestNGTest() {
        if (importsFromTestNG && isInsideATest()) {
            return true;
        }
        return false;
    }

    public boolean isInsideAAssertJTest(){
       if (importsFromAssertJ && isInsideATest()){
           return true;
       }
       return false;
    }


    public Boolean isAnError() {
        return isAnError;
    }

    public void setIsAnError(Boolean bool) {
        isAnError = bool;
    }


    public boolean isInsideATestMethod() {
        return isInsideATestMethod;
    }

    public boolean isInsideATestFolder() {
        return isInsideATestFolder;
    }

    public void setInsideATestMethod(boolean bool) {
        isInsideATestMethod = bool;
    }

    public boolean isMethodNameStartingWithTest() {
        return isTheMethodNameStartingWithTest;
    }

    public void setTheMethodNameStartingWithTest(boolean theMethodNameStartingWithTest) {
        this.isTheMethodNameStartingWithTest = theMethodNameStartingWithTest;
    }

    public String getExtendsFrom() {
        return extendsFrom;
    }

    public void setExtendsFrom(String extendsFrom) {
        this.extendsFrom = extendsFrom;
    }


    public void setInsideATestFolder(boolean insideATestFolder) {
        this.isInsideATestFolder = insideATestFolder;
    }

    public String getRootPath() {
        return rootPath;
    }

    public void setRootPath(String rootPath) {
        //identifica que o SourceRoot é na realidade um TestRoot (está dentro de um /test/
        if (rootPath.contains(File.separator + "test")) {
            this.setInsideATestFolder(true);
            //Com a instrução abaixo, tudo que estiver dentro de um diretório /test/ será considerado como parte de um test
            //Assim, exceções usadas de forma auxiliar, não serão contabilizadas no projeto final
            //this.setInsideATestMethod(true);
        }
        this.rootPath = rootPath;
    }

    public Map<Integer, String> getParentClassName() {
        return parentClassName;
    }

    public String getParentClassName(int index) {
        return parentClassName.get(new Integer(index));
    }

    public void setParentClassName(Map<Integer, String> parentClassName) {
        this.parentClassName = parentClassName;
    }

    public void setParentMethodName(Map<Integer, String> parentMethodName) {
        this.parentMethodName = parentMethodName;
    }

    public boolean isImportsFromJUnit() {
        return importsFromJUnit;
    }

    public void setImportsFromJUnit(boolean importsFromJUnit) {
        this.importsFromJUnit = importsFromJUnit;
    }

    public boolean isImportsFromTestNG() {
        return importsFromTestNG;
    }

    public void setImportsFromTestNG(boolean importsFromTestNG) {
        this.importsFromTestNG = importsFromTestNG;
    }

    public boolean isImportsFromAssertJ() {
        return importsFromAssertJ;
    }

    public void setImportsFromAssertJ(boolean importsFromAssertJ) {
        this.importsFromAssertJ = importsFromAssertJ;
    }

    public Boolean getAnError() {
        return isAnError;
    }

    public void setAnError(Boolean anError) {
        isAnError = anError;
    }

    public String getFullFilePath() {
        return fullFilePath;
    }

    public void setFullFilePath(String fullFilePath) {
        this.fullFilePath = fullFilePath;
    }

    public String getFullClassPackagePath(){
        return  this.packageName + "." + this.parentClassName.get(0);
    }


    @Override
    public String toString() {
        return "AbstractOrdinaryModel{" +
                "fullFilePath='" + fullFilePath + '\'' +
                ", parentClassName=" + parentClassName +
                ", parentMethodName=" + parentMethodName +
                ", node=" + node +
                ", packageName='" + packageName + '\'' +
                ", rootPath='" + rootPath + '\'' +
                ", isInsideATestMethod=" + isInsideATestMethod +
                ", isInsideATestFolder=" + isInsideATestFolder +
                ", isTheMethodNameStartingWithTest=" + isTheMethodNameStartingWithTest +
                ", hasModelCoverageData=" + hasModelCoverageData +
                ", extendsFrom='" + extendsFrom + '\'' +
                ", importsFromJUnit=" + importsFromJUnit +
                ", importsFromTestNG=" + importsFromTestNG +
                ", importsFromAssertJ=" + importsFromAssertJ +
                ", isAnError=" + isAnError +
                '}';
    }

    public boolean isTheMethodNameStartingWithTest() {
        return isTheMethodNameStartingWithTest;
    }

    public boolean isHasModelCoverageData() {
        return hasModelCoverageData;
    }

    public void setHasModelCoverageData(boolean hasModelCoverageData) {
        this.hasModelCoverageData = hasModelCoverageData;
    }
}
