package br.ufal.easy.exceptionhunter.visitors.junit;

import com.github.javaparser.ast.expr.MethodCallExpr;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;
import br.ufal.easy.exceptionhunter.extractors.CombinedTypeExtractor;
import br.ufal.easy.exceptionhunter.extractors.ModelExtractor;
import br.ufal.easy.exceptionhunter.models.junit.JUnit_ExpectExceptionTestCallModel;

/**
 *  This visitor identifies JUnit's expect call  constructs
 */
public class ExpectExceptionCallVisitor extends VoidVisitorAdapter<Void> {

    private CombinedTypeExtractor cte;
    private ModelExtractor me;
    private String rootPath;

    public ExpectExceptionCallVisitor(CombinedTypeExtractor cte, ModelExtractor me, String rootPath) {
        this.cte = cte;
        this.me = me;
        this.rootPath = rootPath;
    }

    @Override
    public void visit(MethodCallExpr n, Void arg) {
        super.visit(n, null);
        if (n.getNameAsString().equals("expect")) {
            //String qualifiedSignature = "";
            JUnit_ExpectExceptionTestCallModel model = new JUnit_ExpectExceptionTestCallModel();
            model.setRootPath(this.rootPath);
            me.extractBaseNodeData(n, model);
        }
    }
}