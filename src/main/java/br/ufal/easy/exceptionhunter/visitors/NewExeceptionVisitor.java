package br.ufal.easy.exceptionhunter.visitors;

import com.github.javaparser.ast.body.ClassOrInterfaceDeclaration;
import com.github.javaparser.ast.type.ClassOrInterfaceType;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;
import br.ufal.easy.exceptionhunter.extractors.CombinedTypeExtractor;
import br.ufal.easy.exceptionhunter.extractors.ModelExtractor;
import br.ufal.easy.exceptionhunter.models.NewExceptionModel;

/**
 * This visitor identifies new classes or interfaces that extends from Exception, Error or Throwable
 */
public class NewExeceptionVisitor extends VoidVisitorAdapter<Void> {

    private CombinedTypeExtractor cte;
    private ModelExtractor me;
    private String rootPath;

    public NewExeceptionVisitor(CombinedTypeExtractor cte, ModelExtractor me, String rootPath) {
        this.cte = cte;
        this.me = me;
        this.rootPath = rootPath;

    }

    @Override
    public void visit(ClassOrInterfaceDeclaration n, Void arg) {
        super.visit(n, null);
        for (ClassOrInterfaceType extendType : n.getExtendedTypes()) {
            if (extendType.getNameAsString().contains("Exception") || extendType.getNameAsString().contains("Error") || extendType.getNameAsString().contains("Throwable")) {
                NewExceptionModel model = new NewExceptionModel();
                model.setRootPath(this.rootPath);
                if(extendType.getNameAsString().contains("Error")){
                    model.setIsAnError(true);
                }
                me.extractBaseNodeData(extendType, model);
            }
        }

    }
}