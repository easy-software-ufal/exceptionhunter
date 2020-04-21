package br.ufal.easy.exceptionhunter.visitors.junit;

import com.github.javaparser.ast.expr.MethodCallExpr;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;
import br.ufal.easy.exceptionhunter.extractors.CombinedTypeExtractor;
import br.ufal.easy.exceptionhunter.extractors.ModelExtractor;
import br.ufal.easy.exceptionhunter.models.junit.JUnit_assertThrowsModel;

/**
 * This visitor identifies JUnit5's AsserThrows Exception Testing constructs
 */
public class AssertThrowsVisitor extends VoidVisitorAdapter<Void> {
    private CombinedTypeExtractor cte;
    private ModelExtractor me;
    private String rootPath;

    public AssertThrowsVisitor(CombinedTypeExtractor cte, ModelExtractor me, String rootPath) {
        this.cte = cte;
        this.me = me;
        this.rootPath = rootPath;
    }

    @Override
    public void visit(MethodCallExpr n, Void arg) {
        super.visit(n, null);
        if (n.getNameAsString().equals("assertThrows")) {
            JUnit_assertThrowsModel model = new JUnit_assertThrowsModel();
            model.setRootPath(rootPath);
            this.me.extractBaseNodeData(n, model);
        }
    }
}