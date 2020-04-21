package br.ufal.easy.exceptionhunter.visitors.junit;

import com.github.javaparser.ast.expr.MemberValuePair;
import com.github.javaparser.ast.expr.NormalAnnotationExpr;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;
import br.ufal.easy.exceptionhunter.extractors.CombinedTypeExtractor;
import br.ufal.easy.exceptionhunter.extractors.ModelExtractor;
import br.ufal.easy.exceptionhunter.models.junit.JUnit_ExpectedExceptionTestAnnotationModel;

/**
 *  * This visitor identifies JUnit's expected annotation  constructs
 *
 * @Test(expected=xxxx.class)
 */
public class ExpectedAnnotationVisitor extends VoidVisitorAdapter<Void> {
    private CombinedTypeExtractor cte;
    private ModelExtractor me;
    private String rootPath;

    public ExpectedAnnotationVisitor(CombinedTypeExtractor cte, ModelExtractor me, String rootPath) {
        this.cte = cte;
        this.me = me;
        this.rootPath = rootPath;
    }

    @Override
    public void visit(NormalAnnotationExpr n, Void arg) {
        super.visit(n, null);

        if (n.getNameAsString().equals("Test")) {
            for (MemberValuePair mvp : n.getPairs()) {
                if (mvp.getNameAsString().equals("expected")) {
                    JUnit_ExpectedExceptionTestAnnotationModel model = new JUnit_ExpectedExceptionTestAnnotationModel();
                    model.setRootPath(this.rootPath);
                    me.extractBaseNodeData(mvp, model);
                }
            }
        }

    }

}