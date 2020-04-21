package br.ufal.easy.exceptionhunter.visitors.assertj;

import br.ufal.easy.exceptionhunter.extractors.CombinedTypeExtractor;
import br.ufal.easy.exceptionhunter.extractors.ModelExtractor;
import br.ufal.easy.exceptionhunter.models.assertj.AssertJ_assertThatModel;
import com.github.javaparser.ast.expr.MethodCallExpr;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;


public class AssertJ_assertThatVisitor extends VoidVisitorAdapter<Void> {
    private CombinedTypeExtractor cte;
    private ModelExtractor me;
    private String rootPath;

    public AssertJ_assertThatVisitor(CombinedTypeExtractor cte, ModelExtractor me, String rootPath) {
        this.cte = cte;
        this.me = me;
        this.rootPath = rootPath;
    }

    @Override
    public void visit(MethodCallExpr n, Void arg) {
        super.visit(n, null);
        if (n.getNameAsString().equals("assertThat")) {
            AssertJ_assertThatModel model = new AssertJ_assertThatModel();
            model.setRootPath(rootPath);
            this.me.extractBaseNodeData(n, model);
        }
    }
}