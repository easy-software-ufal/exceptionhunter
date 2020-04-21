package br.ufal.easy.exceptionhunter.visitors;

import com.github.javaparser.ast.body.ConstructorDeclaration;
import com.github.javaparser.ast.type.ReferenceType;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;
import br.ufal.easy.exceptionhunter.extractors.CombinedTypeExtractor;
import br.ufal.easy.exceptionhunter.extractors.ModelExtractor;
import br.ufal.easy.exceptionhunter.models.ThrowsExceptionModel;

/**
 * This visitor identifies classes' constructors that also throws exceptions
 */
public class ThrowsExceptionOnConstructorVisitor extends VoidVisitorAdapter<Void> {
    private CombinedTypeExtractor cte;
    private ModelExtractor me;
    private String rootPath;

    public ThrowsExceptionOnConstructorVisitor(CombinedTypeExtractor cte, ModelExtractor me, String rootPath) {
        this.cte = cte;
        this.me = me;
        this.rootPath = rootPath;
    }

    @Override
    public void visit(ConstructorDeclaration n, Void arg) {

        super.visit(n, null);
        for (ReferenceType exception : n.getThrownExceptions()) {
            ThrowsExceptionModel model = new ThrowsExceptionModel();
            model.setRootPath(rootPath);
            me.extractBaseNodeData(exception.asClassOrInterfaceType(), model);
        }
    }
}