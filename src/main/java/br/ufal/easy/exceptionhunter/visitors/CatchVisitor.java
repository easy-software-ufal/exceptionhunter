package br.ufal.easy.exceptionhunter.visitors;

import com.github.javaparser.ast.stmt.CatchClause;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;
import br.ufal.easy.exceptionhunter.extractors.CombinedTypeExtractor;
import br.ufal.easy.exceptionhunter.extractors.ModelExtractor;
import br.ufal.easy.exceptionhunter.models.CatchModel;

/**
 * This visitor extracts the exceptions in catch blocks
 */
public class CatchVisitor extends VoidVisitorAdapter<Void> {

    private CombinedTypeExtractor cte;
    private ModelExtractor me;
    private String rootPath;

    public CatchVisitor(CombinedTypeExtractor cte, ModelExtractor me, String rootPath) {
        this.cte = cte;
        this.me = me;
        this.rootPath = rootPath;
    }

    @Override
    public void visit(CatchClause n, Void arg) {
        super.visit(n, null);
        CatchModel model = new CatchModel();
        model.setRootPath(rootPath);
        me.extractBaseNodeData(n, model);
    }
}