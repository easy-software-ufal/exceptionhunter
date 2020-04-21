package br.ufal.easy.exceptionhunter.visitors.testng;

import br.ufal.easy.exceptionhunter.extractors.CombinedTypeExtractor;
import br.ufal.easy.exceptionhunter.extractors.ModelExtractor;
import br.ufal.easy.exceptionhunter.models.testng.TestNG_ExpectedExceptionsTestAnnotationModel;
import com.github.javaparser.ast.expr.MemberValuePair;
import com.github.javaparser.ast.expr.NormalAnnotationExpr;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;

/**
 * This visitor identifies TestNG's Exception Testing constructs
 *
 * @Test(expectedExceptions=xxxx.class, yyyy.class)
 */
public class TestNG_ExpectedExceptionsAnnotationVisitor extends VoidVisitorAdapter<Void> {
    private CombinedTypeExtractor cte;
    private ModelExtractor me;
    private String rootPath;

    public TestNG_ExpectedExceptionsAnnotationVisitor(CombinedTypeExtractor cte, ModelExtractor me, String rootPath) {
        this.cte = cte;
        this.me = me;
        this.rootPath = rootPath;
    }

    @Override
    public void visit(NormalAnnotationExpr n, Void arg) {
        super.visit(n, null);

        if (n.getNameAsString().equals("Test")) {
            for (MemberValuePair mvp : n.getPairs()) {
                if (mvp.getNameAsString().equals("expectedExceptions")) {
                    TestNG_ExpectedExceptionsTestAnnotationModel model = new TestNG_ExpectedExceptionsTestAnnotationModel();
                    model.setRootPath(this.rootPath);
                    me.extractBaseNodeData(mvp, model);
                }
            }
        }

    }

}