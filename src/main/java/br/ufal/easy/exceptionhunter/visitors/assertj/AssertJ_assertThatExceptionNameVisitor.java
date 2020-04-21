package br.ufal.easy.exceptionhunter.visitors.assertj;

import br.ufal.easy.exceptionhunter.extractors.CombinedTypeExtractor;
import br.ufal.easy.exceptionhunter.extractors.ModelExtractor;
import br.ufal.easy.exceptionhunter.models.assertj.AssertJ_assertThatExceptionNameModel;
import com.github.javaparser.ast.expr.MethodCallExpr;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;

import java.util.Arrays;
import java.util.List;


public class AssertJ_assertThatExceptionNameVisitor extends VoidVisitorAdapter<Void> {
    private CombinedTypeExtractor cte;
    private ModelExtractor me;
    private String rootPath;

    public AssertJ_assertThatExceptionNameVisitor(CombinedTypeExtractor cte, ModelExtractor me, String rootPath) {
        this.cte = cte;
        this.me = me;
        this.rootPath = rootPath;
    }

    @Override
    public void visit(MethodCallExpr n, Void arg) {
        super.visit(n, null);
        List<String> methodNames = Arrays.asList("assertThatIllegalArgumentException", "assertThatIllegalStateException", "assertThatIOException", "assertThatNullPointerException");
        String methodName = n.getNameAsString();
        for(String aux : methodNames){
            if(aux.equals(methodName)){
                AssertJ_assertThatExceptionNameModel model = new AssertJ_assertThatExceptionNameModel();
                model.setRootPath(rootPath);
                this.me.extractBaseNodeData(n, model);
            }
        }
    }
}