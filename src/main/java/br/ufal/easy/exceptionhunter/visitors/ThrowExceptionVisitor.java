package br.ufal.easy.exceptionhunter.visitors;

import com.github.javaparser.ast.stmt.ThrowStmt;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;
import br.ufal.easy.exceptionhunter.extractors.CombinedTypeExtractor;
import br.ufal.easy.exceptionhunter.extractors.ModelExtractor;
import br.ufal.easy.exceptionhunter.models.ThrowExceptionModel;

/**
 * This visitor identifies the lines where do exists Throw instructions
 */
public class ThrowExceptionVisitor extends VoidVisitorAdapter<Void> {
    private CombinedTypeExtractor cte;
    private ModelExtractor me;
    private String rootPath;

    public ThrowExceptionVisitor(CombinedTypeExtractor cte, ModelExtractor me, String rootPath) {
        this.cte = cte;
        this.me = me;
        this.rootPath = rootPath;
    }

    @Override
    public void visit(ThrowStmt n, Void arg) {
        super.visit(n, null);
        //System.out.println(n.toString());
        ThrowExceptionModel model = new ThrowExceptionModel();
        model.setRootPath(rootPath);
        me.extractBaseNodeData(n, model);
    }
}