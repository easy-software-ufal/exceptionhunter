package br.ufal.easy.exceptionhunter.visitors;

import com.github.javaparser.ast.Node;
import com.github.javaparser.ast.body.ClassOrInterfaceDeclaration;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.type.ClassOrInterfaceType;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;
import br.ufal.easy.exceptionhunter.extractors.CombinedTypeExtractor;
import br.ufal.easy.exceptionhunter.extractors.ModelExtractor;
import br.ufal.easy.exceptionhunter.models.OrdinaryAnnotationTestModel;
import br.ufal.easy.exceptionhunter.models.OrdinaryExtendedTestModel;

/**
 * This visitor identifies new TestCases.
 */
public class TestCaseVisitor extends VoidVisitorAdapter<Void> {
    private CombinedTypeExtractor cte;
    private ModelExtractor me;
    private String rootPath;

    public TestCaseVisitor(CombinedTypeExtractor cte, ModelExtractor me, String rootPath) {
        this.cte = cte;
        this.me = me;
        this.rootPath = rootPath;
    }


    @Override
    public void visit(MethodDeclaration n, Void arg) {
        super.visit(n, null);
        boolean nameStartsWithTest = n.getNameAsString().startsWith("test");

        if (n.getAnnotationByName("Test").isPresent()) {
            OrdinaryAnnotationTestModel model = new OrdinaryAnnotationTestModel();
            model.setAnnotation("@Test");
            model.setRootPath(rootPath);
            model.setInsideATestMethod(true);
            model.setTheMethodNameStartingWithTest(nameStartsWithTest);
            me.extractBaseNodeData(n, model);
        } else if (n.getComment().isPresent() && n.getComment().get().toString().contains("@Test")) {
            OrdinaryAnnotationTestModel model = new OrdinaryAnnotationTestModel();
            model.setAnnotation("//@Test");
            model.setRootPath(rootPath);
            model.setInsideATestMethod(true);
            model.setTheMethodNameStartingWithTest(nameStartsWithTest);
            me.extractBaseNodeData(n, model);
        } else if (nameStartsWithTest && isTestCaseInheritance(n)) {
            OrdinaryExtendedTestModel model = new OrdinaryExtendedTestModel();
            model.setTheMethodNameStartingWithTest(nameStartsWithTest);
            model.setInsideATestMethod(true);
            model.setRootPath(rootPath);
            me.extractBaseNodeData(n, model);
        }

    }

    private boolean isTestCaseInheritance(MethodDeclaration n) {
        Node.ParentsVisitor pVisitor = new Node.ParentsVisitor(n);
        Node nextNode;
        while (pVisitor.hasNext()) {
            nextNode = pVisitor.next();
            if (nextNode instanceof ClassOrInterfaceDeclaration) {
                ClassOrInterfaceDeclaration node = (ClassOrInterfaceDeclaration) nextNode;
                for (ClassOrInterfaceType extendType : node.getExtendedTypes()) {
                    if (extendType.getNameAsString().contains("Test")) {
                        return true;
                    }
                }
            }
        }
        return false;
    }


}