import br.ufal.easy.exceptionhunter.ProjectMain;
import br.ufal.easy.exceptionhunter.ProjectsConfiguration;
import br.ufal.easy.exceptionhunter.ProjectsDataWrapper;
import br.ufal.easy.exceptionhunter.ProjectsManagerSingleton;
import br.ufal.easy.exceptionhunter.extractors.StatisticsExtractor;
import org.junit.BeforeClass;
import org.junit.Test;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;

public class IntegrationTests {

    public static Map<String, List<ProjectsDataWrapper>> projectsStatistics = new HashMap<>();

    @BeforeClass
    public static void analyzeProject() {
        String jsonPath = ProjectsManagerSingleton.class.getClassLoader().getResource("testProjects.json").getPath();

        ProjectsConfiguration projectsConfiguration = ProjectsManagerSingleton.getProjectsManagerSingleton().getProjectsConfiguration(jsonPath);

        ProjectMain pjMain = new ProjectMain(projectsConfiguration);
        projectsStatistics = pjMain.proceedWithAnalysis();

    }

    private ProjectsDataWrapper getProjectStatistics(String projectName, String tagName) {
        List<ProjectsDataWrapper> projectStatistics = IntegrationTests.projectsStatistics.get(projectName);
        ProjectsDataWrapper projectTag = null;
        for (ProjectsDataWrapper project : projectStatistics) {
            if (project.getTag().equals(tagName)) {
                projectTag = project;
            }
        }
        return projectTag;
    }


    @Test
    public void testIntegrationWebAuthProject_Tag_v1_0() {
        StatisticsExtractor statistic = getProjectStatistics("test-webauth", "v1.0").getStatistics();

        //@Test com comentarios
        assertEquals(27, statistic.getTotalNumberOfTestsByAnnotation());
        //extends TestCase
        assertEquals(1, statistic.getTotalNumberOfTestsByInheritance());
        //soma das duas de cima
        assertEquals(28, statistic.getTotalNumberOfTestMethods());
        //extends.*Exception
        assertEquals(2, statistic.getTotalNumberOfCreatedCustomExceptions());
        //busca pelo nome das novas exceçoes criadas
        assertEquals(2, statistic.getTotalNumberOfDistinctUsedCustomExceptions());
        //busca por throw, throws e catch
        assertEquals(24, statistic.getTotalNumberOfDistinctUsedStandardOrThirdPartyExceptions());
        //soma das duas de cima
        assertEquals(26, statistic.getTotalNumberOfDistinctUsedExceptions());
        //@Test.*expected (ainda assim falha em casos onde há mais de uma anotação)
        assertEquals(1, statistic.getJunit_totalNumberOfExpectedAttribute());
        //fail(
        assertEquals(15, statistic.getCommom_totalNumberOfFailCalls());

        //Inserido manualmente
        assertEquals(2, statistic.getTotalNumberOfCustomExceptionsTestMethods());
        //Inserido manualmente
        assertEquals(4, statistic.getTotalNumberOfStandardOrThirdPartyExceptionsTestMethods());
        //Inserido manualmente
        assertEquals(0, statistic.getTotalNumberOfNotIdentifiedExceptionsTestMethods());
        //Inserido manualmente (considera excecoes nao identificadas)
        assertEquals(6, statistic.getTotalNumberOfExceptionTests());

        //porcentagens
        //Absolutas ao total de testes criados
//        assertEquals(0.04, statistic.getTotalAbsolutPercentegeOfNotIdentifiedExceptionsTestMethods(), 0.01);
//        assertEquals(0.14, statistic.getTotalAbsolutPercentageOfStandardOrThirdPartyExceptionsTestMethods(), 0.01);
//        assertEquals(0.07, statistic.getTotalAbsolutPercentageCustomExceptionsTestMethods(), 0.01);
//        assertEquals(0.25, statistic.getTotalAbsolutPercentageExceptionsTestMethods(), 0.01);
//        assertEquals(0.08, statistic.getTotalAbsolutPercentageOfStandardOrThirdPartyExceptionsTested(), 0.01);
//        assertEquals(0.04, statistic.getTotalAbsolutPercentegeOfNotIdentifiedExceptionsTested(), 0.01);
//        assertEquals(0.04, statistic.getTotalAbsolutPercentageCustomExceptionsTested(), 0.01);
//        assertEquals(0.12, statistic.getTotalAbsolutPercentageExceptionsTested(), 0.01);
//        //Relativas ao total de excecoes usadas
//        assertEquals(0.08, statistic.getTotalRelativePercentageOfStandardOrThirdPartyExceptionsTested(), 0.01);
//        assertEquals(0.5, statistic.getTotalRelativePercentageCustomExceptionsTested(), 0.01);
//        assertEquals(1, statistic.getTotalRelativePercentegeOfNotIdentifiedExceptionsTested(), 0.01);

        //Lists
        List<String> ec = statistic.getCustomCreatedExceptions();
        //extends .*Exception
        assertTrue(ec.contains("ResponseException"));
        assertTrue(ec.contains("WebAuthnException"));
        assertEquals(2, ec.size());

        /*** Throws ***/

        //throws nome das novas excecoes
        assertEquals(20, statistic.getTotalNumberOfThrowsStatementCustomExceptions());
        //numero de throws (sem comentarios) - throws com excecoes novas. Lebrando que throws exception1, exception2
        //é contado como se fossem 2 throws distintos
        assertEquals(92, statistic.getTotalNumberOfThrowsStatementsStandardOrThirdPartyExceptions());
        //soma dos dois de cima
        assertEquals(112, statistic.getTotalNumberOfThrowsStatements());
        //Total - as custom - nao identificada
        assertEquals(81, statistic.getTotalNumberOfThrowStatementsStandardOrThirdPartyExceptions());

        Map<String, Integer> a1 = statistic.getThrowsStandardOrThirdPartyExceptionsCounter();
        assertEquals(37, (int) a1.get("ServletException"));
        assertEquals(6, (int) a1.get("OAuthRequestException"));
        assertEquals(14, (int) a1.get("CborException"));
        assertEquals(30, (int) a1.get("IOException"));
        assertEquals(3, (int) a1.get("NoSuchAlgorithmException"));
        assertEquals(2, (int) a1.get("InvalidKeySpecException"));
        assertEquals(6, a1.size());

        Map<String, Integer> a2 = statistic.getThrowsCustomExceptionsCounter();
        assertEquals(7, (int) a2.get("WebAuthnException"));
        assertEquals(13, (int) a2.get("ResponseException"));
        assertEquals(2, a2.size());

        /*** Throw ***/

        //throw .*Excecao...
        assertEquals(26, statistic.getTotalNumberOfThrowStatementCustomExceptions());
        //throw .* (qualquer coisa que nao comece com new)
        assertEquals(1, statistic.getTotalNumberOfThrowStatementNotIdentifiedExceptions());
        //busca por throw .*
        assertEquals(108, statistic.getTotalNumberOfThrowStatements());

        Map<String, Integer> a3 = statistic.getThrowStandardOrThirdPartyExceptionsExceptionsCounter();
        assertEquals(58, (int) a3.get("ServletException"));
        assertEquals(12, (int) a3.get("InvalidParameterException"));
        assertEquals(6, (int) a3.get("OAuthRequestException"));
        assertEquals(5, (int) a3.get("IllegalArgumentException"));
        assertEquals(4, a3.size());

        Map<String, Integer> a4 = statistic.getThrowCustomExceptionsCounter();
        assertEquals(10, (int) a4.get("WebAuthnException"));
        assertEquals(16, (int) a4.get("ResponseException"));
        assertEquals(2, a4.size());

        Map<String, Integer> a5 = statistic.getThrowNotIdentifiedExceptionsCounter();
        assertEquals(1, (int) a5.get("NOT IDENTIFIED"));
        assertEquals(1, a5.size());

        /*** Catch ***/

        Map<String, Integer> a6 = statistic.getCatchStandardOrThirdPartyExceptionsCounter();
        assertEquals(2, (int) a6.get("IllegalStateException"));
        assertEquals(1, (int) a6.get("InvalidAlgorithmParameterException"));
        assertEquals(9, (int) a6.get("CborException"));
        assertEquals(1, (int) a6.get("GeneralSecurityException"));
        assertEquals(1, (int) a6.get("NumberFormatException"));
        assertEquals(2, (int) a6.get("CertificateException"));
        assertEquals(1, (int) a6.get("IOException"));
        assertEquals(2, (int) a6.get("SignatureException"));
        assertEquals(7, (int) a6.get("NoSuchAlgorithmException"));
        assertEquals(2, (int) a6.get("InvalidKeyException"));
        assertEquals(2, (int) a6.get("JsonParseException"));
        assertEquals(1, (int) a6.get("SSLException"));
        assertEquals(3, (int) a6.get("Exception"));
        assertEquals(1, (int) a6.get("DecoderException"));
        assertEquals(2, (int) a6.get("JsonSyntaxException"));
        assertEquals(1, (int) a6.get("RuntimeException"));
        assertEquals(7, (int) a6.get("NullPointerException"));
        assertEquals(3, (int) a6.get("ClassCastException"));
        assertEquals(3, (int) a6.get("InvalidKeySpecException"));
        assertEquals(1, (int) a6.get("NoSuchProviderException"));
        assertEquals(20, a6.size());

        Map<String, Integer> a7 = statistic.getCatchCustomExceptionsCounter();
        assertEquals(6, (int) a7.get("WebAuthnException"));
        assertEquals(10, (int) a7.get("ResponseException"));
        assertEquals(2, a7.size());


        /*** Exceptions Use ***/

        //Basta procurar pelo nome da exceção, qualquer coisa que não for um comentário, uma declaração de classe
        //, um construtor, um método, interface, um extends ou um import é um uso
        // Regex para excluir import: ^(?!import).*IOException
        Map<String, Integer> a8 = statistic.getStandardOrThirdPartyExceptionsUsed();
        assertEquals(2, (int) a8.get("IllegalStateException"));
        assertEquals(12, (int) a8.get("OAuthRequestException"));
        assertEquals(1, (int) a8.get("InvalidAlgorithmParameterException"));
        assertEquals(23, (int) a8.get("CborException"));
        assertEquals(1, (int) a8.get("GeneralSecurityException"));
        assertEquals(1, (int) a8.get("NumberFormatException"));
        assertEquals(2, (int) a8.get("CertificateException"));
        assertEquals(31, (int) a8.get("IOException"));
        assertEquals(10, (int) a8.get("NoSuchAlgorithmException"));
        assertEquals(2, (int) a8.get("SignatureException"));
        assertEquals(2, (int) a8.get("InvalidKeyException"));
        assertEquals(2, (int) a8.get("JsonParseException"));
        assertEquals(1, (int) a8.get("SSLException"));
        assertEquals(3, (int) a8.get("Exception"));
        assertEquals(95, (int) a8.get("ServletException"));
        assertEquals(12, (int) a8.get("InvalidParameterException"));
        assertEquals(1, (int) a8.get("DecoderException"));
        assertEquals(2, (int) a8.get("JsonSyntaxException"));
        assertEquals(1, (int) a8.get("RuntimeException"));
        assertEquals(7, (int) a8.get("NullPointerException"));
        assertEquals(3, (int) a8.get("ClassCastException"));
        assertEquals(5, (int) a8.get("InvalidKeySpecException"));
        assertEquals(1, (int) a8.get("NoSuchProviderException"));
        assertEquals(5, (int) a8.get("IllegalArgumentException"));
        assertEquals(24, a8.size());

        Map<String, Integer> a9 = statistic.getCustomExceptionsUsed();
        assertEquals(23, (int) a9.get("WebAuthnException"));
        assertEquals(39, (int) a9.get("ResponseException"));
        assertEquals(2, a9.size());

        /*** Tested Exceptions ***/
        //exceções dentro de expected, expect ou assertThrows
        Map<String, Integer> a10 = statistic.getTestedStandardOrThirdPartyExceptionsCounter();
        assertEquals(2, (int) a10.get("NullPointerException"));
        assertEquals(2, (int) a10.get("CborException"));
        assertEquals(2, a10.size());

        Map<String, Integer> a11 = statistic.getTestedCustomExceptionsCounter();
        assertEquals(2, (int) a11.get("WebAuthnException"));
        assertEquals(1, a11.size());

        //Geralmente isso aqui vai ser um .expect("ALGUM TEXTO NO LUGAR DA EXCECAO")
        Map<String, Integer> a12 = statistic.getTestedNotIdentifiedExceptionsCounter();
        assertEquals(null, a12.get("NOT IDENTIFIED"));
        assertEquals(0, a12.size());

        //Extraido do numero de excecoes do teste a10
        assertEquals(2, statistic.getTotalNumberOfAllTestedStandardOrThirdPartyExceptions());
        //Extraido do numero de excecoes do teste a11
        assertEquals(1, statistic.getTotalNumberOfAllTestedCustomExceptions());

        /*** Methods with exceptions' test ***/
        //Procura pelo nome das excecoes conhecidas
        Map<String, Integer> a13 = statistic.getCustomExceptionsTestMethodCounter();
        assertEquals(1, (int) a13.get("com.google.webauthn.gaedemo.custom.StrangeCasesTest.testAssertThrowsWebAuthnException()"));
        assertEquals(1, (int) a13.get("com.google.webauthn.gaedemo.custom.StrangeCasesTest.testExpectMethodCallCustomException()"));
        assertEquals(2, a13.size());

        //Inspecao manual nos assertThrows, Expected e expect
        Map<String, Integer> a14 = statistic.getStandardOrThirdPartyExceptionsTestMethodCounter();
        assertEquals(1, (int) a14.get("com.google.webauthn.gaedemo.custom.StrangeCasesTest.testExpectedAnnotationStandardException()"));
        assertEquals(1, (int) a14.get("com.google.webauthn.gaedemo.custom.StrangeCasesTest.testAssertThrowsCborException()"));
        assertEquals(1, (int) a14.get("com.google.webauthn.gaedemo.custom.StrangeCasesTest.testExpectMethodCallStandardException()"));
        assertEquals(1, (int) a14.get("com.google.webauthn.gaedemo.custom.StrangeCasesTest.testEncode()"));
        assertEquals(4, a14.size());

        //Inspecao manual nos assertThrows, Expected e expect
        Map<String, Integer> a15 = statistic.getNotIdentifiedExceptionsTestMethodCounter();
        assertEquals(null, a15.get("com.google.webauthn.gaedemo.custom.StrangeCasesTest.testExpectMethodCallNoException()"));
        assertEquals(0, a15.size());

    }

    @Test
    public void testIntegrationWebAuthProject_Tag_v1_2() {
        StatisticsExtractor statistic = getProjectStatistics("test-webauth", "v1.2").getStatistics();


        //@Test com comentarios
        assertEquals(28, statistic.getTotalNumberOfTestsByAnnotation());
        //extends TestCase
        assertEquals(1, statistic.getTotalNumberOfTestsByInheritance());
        //soma das duas de cima
        assertEquals(29, statistic.getTotalNumberOfTestMethods());
        //extends.*Exception
        assertEquals(2, statistic.getTotalNumberOfCreatedCustomExceptions());
        //busca pelo nome das novas exceçoes criadas
        assertEquals(2, statistic.getTotalNumberOfDistinctUsedCustomExceptions());
        //busca por throw, throws e catch
        assertEquals(27, statistic.getTotalNumberOfDistinctUsedStandardOrThirdPartyExceptions());
        //soma das duas de cima
        assertEquals(29, statistic.getTotalNumberOfDistinctUsedExceptions());
        //@Test.*expected (ainda assim falha em casos onde há mais de uma anotação)
        assertEquals(1, statistic.getJunit_totalNumberOfExpectedAttribute());
        //fail(
        assertEquals(16, statistic.getCommom_totalNumberOfFailCalls());

        //Inserido manualmente
        assertEquals(2, statistic.getTotalNumberOfCustomExceptionsTestMethods());
        //Inserido manualmente
        assertEquals(5, statistic.getTotalNumberOfStandardOrThirdPartyExceptionsTestMethods());
        //Inserido manualmente
        assertEquals(0, statistic.getTotalNumberOfNotIdentifiedExceptionsTestMethods());
        //Inserido manualmente (considera excecoes nao identificadas)
        assertEquals(7, statistic.getTotalNumberOfExceptionTests());

        //porcentagens
        //Absolutas ao total de testes criados
//        assertEquals(0.03, statistic.getTotalAbsolutPercentegeOfNotIdentifiedExceptionsTestMethods(), 0.01);
//        assertEquals(0.17, statistic.getTotalAbsolutPercentageOfStandardOrThirdPartyExceptionsTestMethods(), 0.01);
//        assertEquals(0.07, statistic.getTotalAbsolutPercentageCustomExceptionsTestMethods(), 0.01);
//        assertEquals(0.28, statistic.getTotalAbsolutPercentageExceptionsTestMethods(), 0.01);
//        assertEquals(0.1, statistic.getTotalAbsolutPercentageOfStandardOrThirdPartyExceptionsTested(), 0.01);
//        assertEquals(0.03, statistic.getTotalAbsolutPercentegeOfNotIdentifiedExceptionsTested(), 0.01);
//        assertEquals(0.03, statistic.getTotalAbsolutPercentageCustomExceptionsTested(), 0.01);
//        assertEquals(0.14, statistic.getTotalAbsolutPercentageExceptionsTested(), 0.01);
//        //Relativas ao total de excecoes usadas
//        assertEquals(0.11, statistic.getTotalRelativePercentageOfStandardOrThirdPartyExceptionsTested(), 0.01);
//        assertEquals(0.5, statistic.getTotalRelativePercentageCustomExceptionsTested(), 0.01);
//        assertEquals(1, statistic.getTotalRelativePercentegeOfNotIdentifiedExceptionsTested(), 0.01);

        //Lists
        List<String> ec = statistic.getCustomCreatedExceptions();
        //extends .*Exception
        assertTrue(ec.contains("ResponseException"));
        assertTrue(ec.contains("WebAuthnException"));
        assertEquals(2, ec.size());

        /*** Throws ***/

        //throws nome das novas excecoes
        assertEquals(20, statistic.getTotalNumberOfThrowsStatementCustomExceptions());
        //numero de throws (sem comentarios) - throws com excecoes novas. Lebrando que throws exception1, exception2
        //é contado como se fossem 2 throws distintos
        assertEquals(93, statistic.getTotalNumberOfThrowsStatementsStandardOrThirdPartyExceptions());
        //soma dos dois de cima
        assertEquals(113, statistic.getTotalNumberOfThrowsStatements());
        //Total - as custom - nao identificada
        assertEquals(84, statistic.getTotalNumberOfThrowStatementsStandardOrThirdPartyExceptions());

        Map<String, Integer> a1 = statistic.getThrowsStandardOrThirdPartyExceptionsCounter();
        assertEquals(37, (int) a1.get("ServletException"));
        assertEquals(6, (int) a1.get("OAuthRequestException"));
        assertEquals(14, (int) a1.get("CborException"));
        assertEquals(30, (int) a1.get("IOException"));
        assertEquals(3, (int) a1.get("NoSuchAlgorithmException"));
        assertEquals(2, (int) a1.get("InvalidKeySpecException"));
        assertEquals(1, (int) a1.get("JsonParseException"));
        assertEquals(7, a1.size());

        Map<String, Integer> a2 = statistic.getThrowsCustomExceptionsCounter();
        assertEquals(7, (int) a2.get("WebAuthnException"));
        assertEquals(13, (int) a2.get("ResponseException"));
        assertEquals(2, a2.size());

        /*** Throw ***/

        //throw .*Excecao...
        assertEquals(26, statistic.getTotalNumberOfThrowStatementCustomExceptions());
        //throw .* (qualquer coisa que nao comece com new)
        assertEquals(2, statistic.getTotalNumberOfThrowStatementNotIdentifiedExceptions());
        //busca por throw .*
        assertEquals(112, statistic.getTotalNumberOfThrowStatements());

        Map<String, Integer> a3 = statistic.getThrowStandardOrThirdPartyExceptionsExceptionsCounter();
        assertEquals(58, (int) a3.get("ServletException"));
        assertEquals(12, (int) a3.get("InvalidParameterException"));
        assertEquals(6, (int) a3.get("OAuthRequestException"));
        assertEquals(5, (int) a3.get("IllegalArgumentException"));
        assertEquals(2, (int) a3.get("JsonParseException"));
        assertEquals(1, (int) a3.get("NoSuchElementException"));
        assertEquals(6, a3.size());

        Map<String, Integer> a4 = statistic.getThrowCustomExceptionsCounter();
        assertEquals(10, (int) a4.get("WebAuthnException"));
        assertEquals(16, (int) a4.get("ResponseException"));
        assertEquals(2, a4.size());

        Map<String, Integer> a5 = statistic.getThrowNotIdentifiedExceptionsCounter();
        assertEquals(2, (int) a5.get("NOT IDENTIFIED"));
        assertEquals(1, a5.size());

        /*** Catch ***/

        Map<String, Integer> a6 = statistic.getCatchStandardOrThirdPartyExceptionsCounter();
        assertEquals(2, (int) a6.get("IllegalStateException"));
        assertEquals(1, (int) a6.get("InvalidAlgorithmParameterException"));
        assertEquals(9, (int) a6.get("CborException"));
        assertEquals(1, (int) a6.get("GeneralSecurityException"));
        assertEquals(1, (int) a6.get("NumberFormatException"));
        assertEquals(2, (int) a6.get("CertificateException"));
        assertEquals(1, (int) a6.get("IOException"));
        assertEquals(2, (int) a6.get("SignatureException"));
        assertEquals(7, (int) a6.get("NoSuchAlgorithmException"));
        assertEquals(2, (int) a6.get("InvalidKeyException"));
        assertEquals(3, (int) a6.get("JsonParseException"));
        assertEquals(1, (int) a6.get("SSLException"));
        assertEquals(3, (int) a6.get("Exception"));
        assertEquals(1, (int) a6.get("DecoderException"));
        assertEquals(2, (int) a6.get("JsonSyntaxException"));
        assertEquals(1, (int) a6.get("RuntimeException"));
        assertEquals(7, (int) a6.get("NullPointerException"));
        assertEquals(3, (int) a6.get("ClassCastException"));
        assertEquals(3, (int) a6.get("InvalidKeySpecException"));
        assertEquals(1, (int) a6.get("NoSuchProviderException"));
        assertEquals(1, (int) a6.get("StackOverflowError"));
        assertEquals(1, (int) a6.get("OutOfMemoryError"));
        assertEquals(22, a6.size());

        Map<String, Integer> a7 = statistic.getCatchCustomExceptionsCounter();
        assertEquals(6, (int) a7.get("WebAuthnException"));
        assertEquals(10, (int) a7.get("ResponseException"));
        assertEquals(2, a7.size());


        /*** Exceptions Use ***/

        //Basta procurar pelo nome da exceção, qualquer coisa que não for um comentário, uma declaração de classe
        //, um construtor, um método, interface, um extends ou um import é um uso
        // Regex para excluir import: ^(?!import).*IOException
        Map<String, Integer> a8 = statistic.getStandardOrThirdPartyExceptionsUsed();
        assertEquals(2, (int) a8.get("IllegalStateException"));
        assertEquals(12, (int) a8.get("OAuthRequestException"));
        assertEquals(1, (int) a8.get("InvalidAlgorithmParameterException"));
        assertEquals(23, (int) a8.get("CborException"));
        assertEquals(1, (int) a8.get("GeneralSecurityException"));
        assertEquals(1, (int) a8.get("NumberFormatException"));
        assertEquals(2, (int) a8.get("CertificateException"));
        assertEquals(31, (int) a8.get("IOException"));
        assertEquals(10, (int) a8.get("NoSuchAlgorithmException"));
        assertEquals(2, (int) a8.get("SignatureException"));
        assertEquals(2, (int) a8.get("InvalidKeyException"));
        assertEquals(6, (int) a8.get("JsonParseException"));
        assertEquals(1, (int) a8.get("SSLException"));
        assertEquals(3, (int) a8.get("Exception"));
        assertEquals(95, (int) a8.get("ServletException"));
        assertEquals(12, (int) a8.get("InvalidParameterException"));
        assertEquals(1, (int) a8.get("DecoderException"));
        assertEquals(2, (int) a8.get("JsonSyntaxException"));
        assertEquals(1, (int) a8.get("RuntimeException"));
        assertEquals(7, (int) a8.get("NullPointerException"));
        assertEquals(3, (int) a8.get("ClassCastException"));
        assertEquals(5, (int) a8.get("InvalidKeySpecException"));
        assertEquals(1, (int) a8.get("NoSuchProviderException"));
        assertEquals(5, (int) a8.get("IllegalArgumentException"));
        assertEquals(1, (int) a8.get("NoSuchElementException"));
        assertEquals(1, (int) a8.get("StackOverflowError"));
        assertEquals(1, (int) a8.get("OutOfMemoryError"));
        assertEquals(27, a8.size());

        Map<String, Integer> a9 = statistic.getCustomExceptionsUsed();
        assertEquals(23, (int) a9.get("WebAuthnException"));
        assertEquals(39, (int) a9.get("ResponseException"));
        assertEquals(2, a9.size());

        /*** Tested Exceptions ***/
        //exceções dentro de expected, expect ou assertThrows
        Map<String, Integer> a10 = statistic.getTestedStandardOrThirdPartyExceptionsCounter();
        assertEquals(2, (int) a10.get("NullPointerException"));
        assertEquals(3, (int) a10.get("CborException"));
        assertEquals(1, (int) a10.get("IOException"));
        assertEquals(3, a10.size());

        Map<String, Integer> a11 = statistic.getTestedCustomExceptionsCounter();
        assertEquals(2, (int) a11.get("WebAuthnException"));
        assertEquals(1, a11.size());

        //Geralmente isso aqui vai ser um .expect("ALGUM TEXTO NO LUGAR DA EXCECAO")
        Map<String, Integer> a12 = statistic.getTestedNotIdentifiedExceptionsCounter();
        assertEquals(null, a12.get("NOT IDENTIFIED"));
        assertEquals(0, a12.size());

        //Extraido do numero de excecoes do teste a10
        assertEquals(3, statistic.getTotalNumberOfAllTestedStandardOrThirdPartyExceptions());
        //Extraido do numero de excecoes do teste a11
        assertEquals(1, statistic.getTotalNumberOfAllTestedCustomExceptions());

        /*** Methods with exceptions' test ***/
        //Procura pelo nome das excecoes conhecidas
        Map<String, Integer> a13 = statistic.getCustomExceptionsTestMethodCounter();
        assertEquals(1, (int) a13.get("com.google.webauthn.gaedemo.custom.StrangeCasesTest.testAssertThrowsWebAuthnException()"));
        assertEquals(1, (int) a13.get("com.google.webauthn.gaedemo.custom.StrangeCasesTest.testExpectMethodCallCustomException()"));
        assertEquals(2, a13.size());

        //Inspecao manual nos assertThrows, Expected e expect
        Map<String, Integer> a14 = statistic.getStandardOrThirdPartyExceptionsTestMethodCounter();
        assertEquals(1, (int) a14.get("com.google.webauthn.gaedemo.custom.StrangeCasesTest.testExpectedAnnotationStandardException()"));
        assertEquals(1, (int) a14.get("com.google.webauthn.gaedemo.custom.StrangeCasesTest.testAssertThrowsCborException()"));
        assertEquals(1, (int) a14.get("com.google.webauthn.gaedemo.custom.StrangeCasesTest.testExpectMethodCallStandardException()"));
        assertEquals(1, (int) a14.get("com.google.webauthn.gaedemo.custom.StrangeCasesTest.testEncode()"));
        assertEquals(2, (int) a14.get("com.google.webauthn.gaedemo.custom.StrangeCasesTest.testEncodeTwo()"));
        assertEquals(5, a14.size());

        //Inspecao manual nos assertThrows, Expected e expect
        Map<String, Integer> a15 = statistic.getNotIdentifiedExceptionsTestMethodCounter();
        assertEquals(null, a15.get("com.google.webauthn.gaedemo.custom.StrangeCasesTest.testExpectMethodCallNoException()"));
        assertEquals(0, a15.size());

    }


}
