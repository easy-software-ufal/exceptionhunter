package br.ufal.easy.exceptionhunter.extractors;

import br.ufal.easy.exceptionhunter.models.*;
import br.ufal.easy.exceptionhunter.models.assertj.AssertJ_assertThatExceptionNameModel;
import br.ufal.easy.exceptionhunter.models.assertj.AssertJ_assertThatExceptionOfTypeModel;
import br.ufal.easy.exceptionhunter.models.assertj.AssertJ_assertThatModel;
import br.ufal.easy.exceptionhunter.models.assertj.AssertJ_assertThatThrownByModel;
import br.ufal.easy.exceptionhunter.models.commom.Commom_FailCallModel;
import br.ufal.easy.exceptionhunter.models.junit.JUnit_ExpectExceptionTestCallModel;
import br.ufal.easy.exceptionhunter.models.junit.JUnit_ExpectedExceptionTestAnnotationModel;
import br.ufal.easy.exceptionhunter.models.junit.JUnit_assertThrowsModel;
import br.ufal.easy.exceptionhunter.models.testng.TestNG_ExpectedExceptionsTestAnnotationModel;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.Node;
import com.github.javaparser.ast.body.ClassOrInterfaceDeclaration;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.expr.Expression;
import com.github.javaparser.ast.expr.MemberValuePair;
import com.github.javaparser.ast.expr.MethodCallExpr;
import com.github.javaparser.ast.stmt.CatchClause;
import com.github.javaparser.ast.stmt.ThrowStmt;
import com.github.javaparser.ast.stmt.TryStmt;
import com.github.javaparser.ast.type.ClassOrInterfaceType;
import com.google.gson.annotations.Expose;

import java.util.LinkedList;
import java.util.List;

/**
 * Classe que é chamada pelos visitors, realiza a extração dos dados e armazena nos models.
 * <p>
 * Os visitors requisitam essa classe através do getModelExtractor (Singleton). Os visitor chamam o
 * metodo extractBaseNodeData, que faz o tratamento do nó inicial passado pelo visitor. Em seguida, o método
 * extractBaseNodeData chama o método extractParentData que faz a coleta de dados dos nós superiores
 */
public class ModelExtractor {

    @Expose
    public List<TestNG_ExpectedExceptionsTestAnnotationModel> testNG_expectedExceptionsTestAnnotationModels;
    @Expose
    public List<JUnit_ExpectedExceptionTestAnnotationModel> expectedExceptionAnnotationModels;
    @Expose
    public List<JUnit_ExpectExceptionTestCallModel> expectExceptionCallModels;
    @Expose
    public List<Commom_FailCallModel> failCallModels;
    @Expose
    public List<JUnit_assertThrowsModel> JUnitassertThrowsModels;
    @Expose
    public List<CatchModel> catchModels;
    @Expose
    public List<OrdinaryAnnotationTestModel> ordinaryAnnotationTestModels;
    @Expose
    public List<NewExceptionModel> newExceptionModels;
    @Expose
    public List<ThrowsExceptionModel> throwsExceptionModels;
    @Expose
    public List<ThrowExceptionModel> throwExceptionModels;
    @Expose
    public List<OrdinaryExtendedTestModel> ordinaryExtendedTestModels;
    @Expose
    public List<AssertJ_assertThatExceptionOfTypeModel> assertJAssertThatExceptionOfTypeModels;
    @Expose
    public List<AssertJ_assertThatThrownByModel> assertJAssertThatThrownByModels;
    @Expose
    public List<AssertJ_assertThatExceptionNameModel> assertJAssertThatExceptionNameModels;
    @Expose
    public List<AssertJ_assertThatModel> assertJAssertThatModels;

    //Se essa flag estiver true, entao todos os pontos (.) das strings serao trocados por underlines (.)
    //Isso é necessário porque o mongoDB não aceita pontos em chaves
    private boolean adjustStringToMongoDB;

    private CombinedTypeExtractor cte;

    public ModelExtractor(CombinedTypeExtractor cte, boolean adjustStringToMongoDB) {
        this.cte = cte;
        this.testNG_expectedExceptionsTestAnnotationModels = new LinkedList<>();
        this.expectedExceptionAnnotationModels = new LinkedList<>();
        this.failCallModels = new LinkedList<>();
        this.expectExceptionCallModels = new LinkedList<>();
        this.ordinaryAnnotationTestModels = new LinkedList<>();
        this.newExceptionModels = new LinkedList<>();
        this.throwsExceptionModels = new LinkedList<>();
        this.throwExceptionModels = new LinkedList<>();
        this.ordinaryExtendedTestModels = new LinkedList<>();
        this.JUnitassertThrowsModels = new LinkedList<>();
        this.assertJAssertThatThrownByModels = new LinkedList<>();
        this.assertJAssertThatExceptionOfTypeModels = new LinkedList<>();
        this.assertJAssertThatExceptionNameModels = new LinkedList<>();
        this.assertJAssertThatModels = new LinkedList<>();
        this.catchModels = new LinkedList<>();
        this.adjustStringToMongoDB = adjustStringToMongoDB;
    }


    /**
     * Converte uma string comum com pontos em uma string SEM PONTOS. Isso é necessário para evitar a possibilidade
     * de haver pontos nas chaves do MongoDB, o que é proibido
     * <p>
     * Porém, essa conversão só é realizada se a flag adjustStringToMongoDB for true
     *
     * @param stringWithDots
     * @return
     */
    private String adjustStringToMongoDBRestrictions(String stringWithDots) {
        if (adjustStringToMongoDB) {
            return stringWithDots.replace(".", "#");
        }
        return stringWithDots;
    }

    private String extractOnlyTheExceptionName(String fullName) {
        String newName = fullName.replace(".class", "").replace("{", "").replace("}", "").trim();
        return newName;

    }

    public void extractBaseNodeData(MemberValuePair node, TestNG_ExpectedExceptionsTestAnnotationModel model) {
        //model.setNode((Node) node);
        String[] exceptions = node.getValue().toString().split(",");
        List<String> clearExceptionsNames = new LinkedList<>();
        for (String exceptionName : exceptions){
            String aux = extractOnlyTheExceptionName(exceptionName);
            aux = adjustStringToMongoDBRestrictions(aux);
            clearExceptionsNames.add(aux);
        }
        model.setExpectedExceptionsNames(clearExceptionsNames);
        extractParentData((Node) node, model);
        if(model.isInsideATestNGTest()){
            this.testNG_expectedExceptionsTestAnnotationModels.add(model);
        }
    }

    public void extractBaseNodeData(MemberValuePair node, JUnit_ExpectedExceptionTestAnnotationModel model) {
        //model.setNode((Node) node);
        String aux = extractOnlyTheExceptionName(node.getValue().toString());
        aux = adjustStringToMongoDBRestrictions(aux);
        model.setExpectedExceptionName(aux);
        extractParentData((Node) node, model);
        if(model.isInsideAJUnitTest()){
            this.expectedExceptionAnnotationModels.add(model);
        }
    }

    //expect
    public void extractBaseNodeData(MethodCallExpr node, JUnit_ExpectExceptionTestCallModel model) {
        //verificar se o metodo expect é realmente da Classe ExpectedException
        //model.setNode((Node) node);
        if (!node.getArguments().isEmpty()) {
            String arguments = node.getArgument(0).toString();
            if (arguments.endsWith(".class")) {
                String aux = extractOnlyTheExceptionName(arguments);
                aux = adjustStringToMongoDBRestrictions(aux);
                model.setExpectedExceptionName(aux);
                extractParentData((Node) node, model);
                if(model.isInsideAJUnitTest()) {
                    this.expectExceptionCallModels.add(model);
                }
            }
        }
    }

    public void extractBaseNodeData(MethodCallExpr node, Commom_FailCallModel model) {
        //model.setNode((Node) node);
        String arguments = "";
        if (node.getArguments().size() > 0) {
            arguments = node.getArguments().get(0).toString();
        }
        model.setFailCallArgument(arguments);
        model.setTryCatchScope("OUTSIDE");
        extractParentData((Node) node, model);
        if(model.isInsideATest()) {
            this.failCallModels.add(model);
        }

    }

    public void extractBaseNodeData(MethodCallExpr node, AssertJ_assertThatThrownByModel model) {
        Node nextNode;
        Node.ParentsVisitor pVisitor = new Node.ParentsVisitor(node);
        String exceptionName = "NOT IDENTIFIED";
        while (pVisitor.hasNext()) {
            nextNode = pVisitor.next();
            if (nextNode instanceof MethodCallExpr) {
                MethodCallExpr methodCall = (MethodCallExpr) nextNode;
                String methodCallArgument;
                if(methodCall.getArguments().isNonEmpty()){
                    methodCallArgument = methodCall.getArguments().get(0).toString();
                    if(methodCallArgument.contains(".class")){
                        exceptionName = methodCallArgument;
                    }
                    if(methodCall.getNameAsString().equals("isInstanceOf")){
                        break;
                    }

                }
            }
        }

        String aux = extractOnlyTheExceptionName(exceptionName);
        aux = adjustStringToMongoDBRestrictions(aux);
        model.setExpectedExceptionName(aux);
        extractParentData((Node) node, model);
        if(model.isInsideAJUnitTest()) {
            this.assertJAssertThatThrownByModels.add(model);
        }

    }

    public void extractBaseNodeData(MethodCallExpr node, AssertJ_assertThatModel model) {
        Node nextNode;
        Node.ParentsVisitor pVisitor = new Node.ParentsVisitor(node);
        String exceptionName = "NOT IDENTIFIED";
        while (pVisitor.hasNext()) {
            nextNode = pVisitor.next();
            if (nextNode instanceof MethodCallExpr) {
                MethodCallExpr methodCall = (MethodCallExpr) nextNode;
                String methodCallArgument;
                if(methodCall.getArguments().isNonEmpty()){
                    methodCallArgument = methodCall.getArguments().get(0).toString();
                    if(methodCallArgument.contains(".class") && (methodCallArgument.contains("Exception") || methodCallArgument.contains("Error") || methodCallArgument.contains("Throwable"))){
                        exceptionName = methodCallArgument;
                    }
                    if(methodCall.getNameAsString().contains("InstanceOf")){
                        String aux = extractOnlyTheExceptionName(exceptionName);
                        aux = adjustStringToMongoDBRestrictions(aux);
                        model.setExpectedExceptionName(aux);
                        extractParentData((Node) node, model);
                        if(model.isInsideAJUnitTest()) {
                            this.assertJAssertThatModels.add(model);
                        }
                        break;
                    }
                }
            }
        }

    }

    public void extractBaseNodeData(MethodCallExpr node, AssertJ_assertThatExceptionOfTypeModel model) {
        String exceptionName = "NOT IDENTIFIED";
        if (node.getArguments().get(0).toString().contains(".class")) {
            exceptionName = node.getArguments().get(0).toString();
        }
        String aux = extractOnlyTheExceptionName(exceptionName);
        aux = adjustStringToMongoDBRestrictions(aux);
        model.setExpectedExceptionName(aux);
        extractParentData((Node) node, model);
        if(model.isInsideAJUnitTest()) {
            this.assertJAssertThatExceptionOfTypeModels.add(model);
        }

    }

    public void extractBaseNodeData(MethodCallExpr node, AssertJ_assertThatExceptionNameModel model) {
        String exceptionName = (node.getNameAsString().replace("assertThat", ""));
        String aux = extractOnlyTheExceptionName(exceptionName);
        aux = adjustStringToMongoDBRestrictions(aux);
        model.setExpectedExceptionName(aux);
        extractParentData((Node) node, model);
        if(model.isInsideAJUnitTest()) {
            this.assertJAssertThatExceptionNameModels.add(model);
        }

    }

    public void extractBaseNodeData(MethodCallExpr node, JUnit_assertThrowsModel model) {
        //model.setNode((Node) node);
        //Essa manobra abaixo é necessária porque o ElasticSearch tem uma implementação propria do
        //AssertThrows que inverte a ordem dos parametros
        String exceptionName;
        if (node.getArguments().get(0).toString().contains(".class")) {
            exceptionName = node.getArguments().get(0).toString();
        } else if (node.getArguments().size() > 1 && node.getArguments().get(1).toString().contains(".class")) {
            exceptionName = node.getArguments().get(1).toString();
        } else {
            exceptionName = "NOT IDENTIFIED";
        }
        String aux = extractOnlyTheExceptionName(exceptionName);
        aux = adjustStringToMongoDBRestrictions(aux);
        model.setExpectedExceptionName(aux);
        if (node.getArguments().contains(2)) {
            model.setMessage(node.getArguments().get(2).toString());
        }
        extractParentData((Node) node, model);
        if(model.isInsideAJUnitTest()) {
            this.JUnitassertThrowsModels.add(model);
        }

    }

    public void extractBaseNodeData(MethodDeclaration node, OrdinaryAnnotationTestModel model) {
        //model.setNode((Node) node);
        //model.setTestMethodName(node.getDeclarationAsString(false,false, true));
        String aux = node.getSignature().toString();
        aux = adjustStringToMongoDBRestrictions(aux);
        model.setTestMethodName(aux);
        extractParentData((Node) node, model);
        this.ordinaryAnnotationTestModels.add(model);

    }

    public void extractBaseNodeData(MethodDeclaration node, OrdinaryExtendedTestModel model) {
        //model.setNode((Node) node);
        //model.setTestMethodName(node.getDeclarationAsString(false,false, true));
        String aux = node.getSignature().toString();
        aux = adjustStringToMongoDBRestrictions(aux);
        model.setTestMethodName(aux);
        extractParentData((Node) node, model);
        this.ordinaryExtendedTestModels.add(model);

    }

    public void extractBaseNodeData(ClassOrInterfaceType node, NewExceptionModel model) {
        //model.setNode((Node) node);
        String aux = extractOnlyTheExceptionName(node.toString());
        aux = adjustStringToMongoDBRestrictions(aux);
        model.setExtendsFrom(aux);
        extractParentData((Node) node, model);
        this.newExceptionModels.add(model);

    }


    public void extractBaseNodeData(ClassOrInterfaceType node, ThrowsExceptionModel model) {
        //model.setNode((Node) node);
        String aux = extractOnlyTheExceptionName(node.getNameAsString());
        aux = adjustStringToMongoDBRestrictions(aux);
        if (aux.length() == 1) {
            model.setException("NOT IDENTIFIED");
        } else {
            model.setException(aux);
        }
        extractParentData((Node) node, model);
        this.throwsExceptionModels.add(model);

    }

    public void extractBaseNodeData(ThrowStmt node, ThrowExceptionModel model) {

        String qualifiedSignature = "";

        model.setNode((Node) node);
        if(node.getRange().isPresent()){
            int lineNumber = node.getBegin().get().line;
            model.setThrowStatementLine(lineNumber);
            model.setNumberOfTimesTheLineWasExecuted(null);
        }
        Expression exp = node.getExpression();
        if (exp.isObjectCreationExpr()) {
            //caso padrao
            String aux = extractOnlyTheExceptionName(exp.asObjectCreationExpr().getType().getNameAsString());
            aux = adjustStringToMongoDBRestrictions(aux);
            if (aux.length() == 1) {
                model.setException("NOT IDENTIFIED");
            } else {
                model.setException(aux);
            }
            model.setThrowType("NEW");
        } else if (exp.isNameExpr()) {
            /*
            nao necessariamente as excecoes que estao aqui sao RETHROW... Ex:
            UnknownHostException unknownHost = new UnknownHostException();
            unknownHost.initCause(e);
            throw unknownHost;
            */
            String[] objectType = qualifiedSignature.split("\\.");
            //model.setException(objectType[objectType.length-1]);
            model.setException("NOT IDENTIFIED");
            model.setThrowType("RETHROW");
        } else if (exp.isMethodCallExpr()) {
            //metodos estaticos quebram ex: public static AssertionError assertionError(String message, Exception e)
            String[] objectType = qualifiedSignature.split("\\.");
            model.setException("NOT IDENTIFIED");
            model.setThrowType("STATIC_NEW");

        } else if (exp.isCastExpr()) {
            String aux = extractOnlyTheExceptionName(exp.asCastExpr().getType().asClassOrInterfaceType().getNameAsString());
            aux = adjustStringToMongoDBRestrictions(aux);
            if (aux.length() == 1) {
                model.setException("NOT IDENTIFIED");
            } else {
                model.setException(aux);
            }
            model.setThrowType("CAST");
        } else {
            //Casos nao previstos ou que nao valem a pena o esforço de implementação
            //Ex: throw e.getCause() instanceof EOFException ? new NoSuchElementException() : e;
            model.setException("NOT IDENTIFIED");
            model.setThrowType("NOT IDENTIFIED");
        }

        extractParentData((Node) node, model);
        this.throwExceptionModels.add(model);

    }

    /**
     * Extrator de excecoes dos catchs
     *
     * @param node
     * @param md
     */
    public void extractBaseNodeData(CatchClause node, CatchModel md) {
        extractData(node, md);
        extractParentData((Node) node, md);
        this.catchModels.add(md);
    }


    private void extractData(TryStmt node, AbstractOrdinaryModel md) {
        if (md instanceof Commom_FailCallModel) {
            Commom_FailCallModel aux = (Commom_FailCallModel) md;
            if (aux.getTryCatchScope().equals("OUTSIDE")) {
                aux.setTryCatchScope("try");
                for (CatchClause cc : node.getCatchClauses()) {
                    extractData(cc, md);
                }
            }
        }

    }

    /**
     * Método extrator das exceções, separadas, iniciado pelo ExtractBaseNodeData do TryStmt
     *
     * @param node
     * @param md
     */
    public void extractData(CatchClause node, AbstractOrdinaryModel md) {
        if (md instanceof Commom_FailCallModel) {
            Commom_FailCallModel fcm = (Commom_FailCallModel) md;
            if (fcm.getTryCatchScope().equals("OUTSIDE")) {
                fcm.setTryCatchScope("catch");
            }
            for (String aux : node.getParameter().getTypeAsString().split("\\|")) {
                if (aux.length() == 1) {
                    fcm.addCatchedException("NOT IDENTIFIED");
                } else {
                    aux = extractOnlyTheExceptionName(aux);
                    aux = adjustStringToMongoDBRestrictions(aux);
                    fcm.addCatchedException(aux);
                }
            }
        } else if (md instanceof CatchModel) {
            CatchModel tcm = (CatchModel) md;
            String aux = extractOnlyTheExceptionName(node.getParameter().toString());
            aux = adjustStringToMongoDBRestrictions(aux);
            if (aux.length() == 1) {
                tcm.addParentCatch("NOT IDENTIFIED");
            } else {
                tcm.addParentCatch(aux);
            }
            for (String type : node.getParameter().getTypeAsString().split("\\|")) {
                //o if abaixo serve para impedir que as excecoes capturadas por "catchs pais" sejam adicionadas
                if (tcm.getParentCatch().size() == 1) {
                    String aux2 = extractOnlyTheExceptionName(type);
                    aux2 = adjustStringToMongoDBRestrictions(aux2);
                    if (aux2.length() == 1) {
                        tcm.addCatchedException("NOT IDENTIFIED");
                    } else {
                        tcm.addCatchedException(aux2);
                    }

                }
            }
        }

    }


    /**
     * @param node que já foi analisado
     * @param md   classe abstrata mae de todos os modelos (usado para o polimorfismo)
     */
    private void extractParentData(Node node, AbstractOrdinaryModel md) {
        Node nextNode;
        //Faz uma lista de todos os nós acima do nó inicial na AST
        Node.ParentsVisitor pVisitor = new Node.ParentsVisitor(node);
        while (pVisitor.hasNext()) {
            nextNode = pVisitor.next();
            if (nextNode instanceof MethodDeclaration) {
                extractData((MethodDeclaration) nextNode, md);
            } else if (nextNode instanceof ClassOrInterfaceDeclaration) {
                extractData((ClassOrInterfaceDeclaration) nextNode, md);
            } else if (nextNode instanceof CompilationUnit) {
                extractData((CompilationUnit) nextNode, md);
            } else if (nextNode instanceof TryStmt) {
                extractData((TryStmt) nextNode, md);
            } else if (nextNode instanceof CatchClause) {
                extractData((CatchClause) nextNode, md);
            } else {
                //Tudo que não tem um tratamento especifico, cai neste caso.
                extractData(nextNode, md);
            }
        }
    }


    /**
     * Identifica os nós que estão abaixo de um anotação @Test ou que tenha um @Test comentado
     *
     * @param node
     * @param md
     */

    private void extractData(MethodDeclaration node, AbstractOrdinaryModel md) {
        md.addParentMethodName(node.getSignature().toString());
        if (node.getAnnotationByName("Test").isPresent()) {
            md.setInsideATestMethod(true); //Identifica testes @Test
        } else if (node.getComment().isPresent() && node.getComment().get().toString().contains("@Test")) {
            md.setInsideATestMethod(true); //Identifica testes com @Test comentado
        }

        if (node.getNameAsString().startsWith("test")) {
            //identifica que o metodo comeca com test. Porem, ainda é preciso checar se há herança de TestCase
            md.setTheMethodNameStartingWithTest(true);
        }
    }
//    private void extractData(MethodDeclaration node, AbstractOrdinaryModel md) {
//        md.addParentMethodName(node.getSignature().toString());
//        CombinedTypeSolver combinedTypeSolver = cte.getCombinedTypeSolver();
//        JavaParserFacade javaParserFacade = JavaParserFacade.get(combinedTypeSolver);
//        if (node.getAnnotationByName("Test").isPresent()) {
//            SymbolReference<ResolvedAnnotationDeclaration> solvedType = javaParserFacade.solve(node.getAnnotationByName("Test").get());
//            if(solvedType.isSolved()){
//                String fqdn = solvedType.getCorrespondingDeclaration().getQualifiedName();
//                if(fqdn.equals("org.junit.Test") || fqdn.equals("org.junit.jupiter.api.Test")){
//                    md.setInsideATestMethod(true); //Identifica testes @Test
//                }
//            }
//        } else if (node.getComment().isPresent() && node.getComment().get().toString().contains("@Test")) {
//            md.setInsideATestMethod(true); //Identifica testes com @Test comentado
//        }
//
//        if (node.getNameAsString().startsWith("test")) {
//            //identifica que o metodo comeca com test. Porem, ainda é preciso checar se há herança de TestCase
//            md.setMethodNameStartsWithTest(true);
//        }
//    }

    /**
     * Cria a hierarquia de classes do nó
     *
     * @param node
     * @param md
     */
    private void extractData(ClassOrInterfaceDeclaration node, AbstractOrdinaryModel md) {
        if (md.isMethodNameStartingWithTest()) {
            if (node.getExtendedTypes().isNonEmpty() && node.getExtendedTypes().get(0).getName().asString().contains("Test")) {
                md.setExtendsFrom(node.getExtendedTypes().get(0).getName().asString());
                md.setInsideATestMethod(true);
            }
        }
        String aux = adjustStringToMongoDBRestrictions(node.getNameAsString());
        md.addParentClassName(aux);

    }


    /**
     * @param node representa o arquivo .java
     * @param md
     */
    private void extractData(CompilationUnit node, AbstractOrdinaryModel md) {
        if (node.getPackageDeclaration().isPresent()) {
            md.setPackageName(node.getPackageDeclaration().get().getName().asString());
        }
        String filePath = node.getStorage().get().getPath().toString().split("]")[1];
        md.setFullFilePath(filePath);

        String imports = node.getImports().toString();
        if(imports.contains("junit")){
            md.setImportsFromJUnit(true);
        }

        if(imports.contains("testng")){
            md.setImportsFromTestNG(true);
        }

        if(imports.contains("assertj")){
            md.setImportsFromAssertJ(true);
        }

    }

    /**
     * Tudo que não tem um tratamento especifico cai aqui dentro para ser impresso
     *
     * @param node
     * @param md
     */
    private void extractData(Node node, AbstractOrdinaryModel md) {
        //System.out.println(node.getMetaModel().getTypeName());
        return;
    }

    public List<JUnit_ExpectedExceptionTestAnnotationModel> getExpectedExceptionAnnotationModels() {
        return expectedExceptionAnnotationModels;
    }

    public List<Commom_FailCallModel> getFailCallModels() {
        return failCallModels;
    }

    public List<JUnit_ExpectExceptionTestCallModel> getExpectExceptionCallModels() {
        return expectExceptionCallModels;
    }

    public List<NewExceptionModel> getNewExceptionModels() {
        return newExceptionModels;
    }

    public List<OrdinaryAnnotationTestModel> getOrdinaryAnnotationTestModels() {
        return ordinaryAnnotationTestModels;
    }

    public List<ThrowsExceptionModel> getThrowsExceptionModels() {
        return throwsExceptionModels;
    }

    public List<ThrowExceptionModel> getThrowExceptionModels() {
        return throwExceptionModels;
    }

    public List<OrdinaryExtendedTestModel> getOrdinaryExtendedTestModels() {
        return ordinaryExtendedTestModels;
    }

    public List<JUnit_assertThrowsModel> getJUnitassertThrowsModels() {
        return JUnitassertThrowsModels;
    }

    public List<CatchModel> getCatchModels() {
        return catchModels;
    }

    public List<AssertJ_assertThatExceptionOfTypeModel> getAssertJAssertThatExceptionOfTypeModels() {
        return assertJAssertThatExceptionOfTypeModels;
    }

    public List<AssertJ_assertThatThrownByModel> getAssertJAssertThatThrownByModels() {
        return assertJAssertThatThrownByModels;
    }

    public List<AssertJ_assertThatExceptionNameModel> getAssertJAssertThatExceptionNameModels() {
        return assertJAssertThatExceptionNameModels;
    }

    public List<AssertJ_assertThatModel> getAssertJAssertThatModels() {
        return assertJAssertThatModels;
    }

    public List<TestNG_ExpectedExceptionsTestAnnotationModel> getTestNG_expectedExceptionsTestAnnotationModels() {
        return testNG_expectedExceptionsTestAnnotationModels;
    }
}
