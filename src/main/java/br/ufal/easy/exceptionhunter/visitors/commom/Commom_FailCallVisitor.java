package br.ufal.easy.exceptionhunter.visitors.commom;

import com.github.javaparser.ast.expr.MethodCallExpr;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;
import br.ufal.easy.exceptionhunter.extractors.CombinedTypeExtractor;
import br.ufal.easy.exceptionhunter.extractors.ModelExtractor;
import br.ufal.easy.exceptionhunter.models.commom.Commom_FailCallModel;

/**
 * This visitor identifies the fail method call. This construct is commom to TestNG, JUnit and AssertJ.
 */
public class Commom_FailCallVisitor extends VoidVisitorAdapter<Void> {

    private CombinedTypeExtractor cte;
    private ModelExtractor me;
    private String rootPath;


    public Commom_FailCallVisitor(CombinedTypeExtractor cte, ModelExtractor me, String rootPath) {
        this.cte = cte;
        this.me = me;
        this.rootPath = rootPath;
    }

    @Override
    public void visit(MethodCallExpr n, Void arg) {

        super.visit(n, null);
        if (n.getNameAsString().equals("fail")) {
            //String qualifiedSignature = "";
            Commom_FailCallModel model = new Commom_FailCallModel();
            model.setRootPath(this.rootPath);
            me.extractBaseNodeData(n, model);
        }
    }
}

