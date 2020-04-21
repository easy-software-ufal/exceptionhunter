package br.ufal.easy.exceptionhunter.extractors;

import br.ufal.easy.exceptionhunter.models.*;
import br.ufal.easy.exceptionhunter.models.assertj.AssertJ_assertThatExceptionNameModel;
import br.ufal.easy.exceptionhunter.models.assertj.AssertJ_assertThatExceptionOfTypeModel;
import br.ufal.easy.exceptionhunter.models.assertj.AssertJ_assertThatModel;
import br.ufal.easy.exceptionhunter.models.assertj.AssertJ_assertThatThrownByModel;
import br.ufal.easy.exceptionhunter.models.commom.Commom_FailCallModel;
import br.ufal.easy.exceptionhunter.models.junit.JUnit_ExpectExceptionTestCallModel;
import br.ufal.easy.exceptionhunter.models.junit.JUnit_ExpectedExceptionTestAnnotationModel;
import br.ufal.easy.exceptionhunter.models.junit.JUnit_assertThrowsModel;
import br.ufal.easy.exceptionhunter.models.testng.TestNG_ExpectedExceptionsTestAnnotationModel;
import com.google.gson.annotations.Expose;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.*;

/**
 * This is a HUGE GOD Class that does all the counts
 */
public class StatisticsExtractor {


    private ModelExtractor models;

    private CombinedTypeExtractor combinedTypeExtractor;

    //flag to tells when the tests are already counted by framework
    private boolean isFrameworksCounted = false;

    //In the first loop, this list is filled with all the Custom Exceptions
    @Expose
    private List<String> customCreatedExceptions;

    //@Expose
    private Set<String> setOfTestFiles;

    @Expose
    private Map<String, Integer> throwsStandardOrThirdPartyExceptionsCounter;

    @Expose
    private Map<String, Integer> throwsCustomExceptionsCounter;

    @Expose
    private Map<String, Integer> throwsNotIdentifiedExceptionsCounter;

    @Expose
    private Map<String, Integer> throwStandardOrThirdPartyExceptionsExceptionsCounter;

    @Expose
    private Map<String, Integer> throwCustomExceptionsCounter;

    @Expose
    private Map<String, Integer> throwNotIdentifiedExceptionsCounter;

    @Expose
    private Map<String, Integer> catchStandardOrThirdPartyExceptionsCounter;

    @Expose
    private Map<String, Integer> catchCustomExceptionsCounter;

    @Expose
    private Map<String, Integer> catchNotIdentifiedExceptionsCounter;

    @Expose
    private Map<String, Integer> standardOrThirdPartyExceptionsUsed;

    @Expose
    private Map<String, Integer> customExceptionsUsed;

    @Expose
    private Map<String, Integer> notIdentifiedExceptionsUsed;

    @Expose
    private Map<String, Integer> testedStandardOrThirdPartyExceptionsCounter;

    @Expose
    private Map<String, Integer> testedCustomExceptionsCounter;

    @Expose
    private Map<String, Integer> testedAndUsedStandardOrThirdPartyExceptionsCounter;

    @Expose
    private Map<String, Integer> testedAndUsedCustomExceptionsCounter;
    @Expose
    private Map<String, Integer> testedNotIdentifiedExceptionsCounter;

    @Expose
    private Map<String, Integer> customExceptionsTestMethodCounter;

    @Expose
    private Map<String, Integer> standardOrThirdPartyExceptionsTestMethodCounter;

    @Expose
    private Map<String, Integer> notIdentifiedExceptionsTestMethodCounter;

    @Expose
    private Map<String, Integer> distinctExceptionsTestMethodCounter;

    @Expose
    private Map<String, Map<String, Integer>> throwCustomExceptionsCoverageCounter;

    @Expose
    private Map<String, Map<String, Integer>> throwStandardOrThirdPartyExceptionsCoverageCounter;

    @Expose
    private Map<String, Map<String, Integer>> throwNotIdentifiedExceptionsCoverageCounter;


    /**************** METRICS *********************/
    @Expose
    private Integer totalNumberOfTestsByAnnotation;
    @Expose
    private Integer totalNumberOfTestsByInheritance;
    @Expose
    private Integer totalNumberOfTestsWithJUnitImports;
    @Expose
    private Integer totalNumberOfTestsWithTestNGImports;
    @Expose
    private Integer totalNumberOfTestsWithAssertJImports;
    @Expose
    private Integer totalNumberOfTestsWithNotIdentifiedImports;
    @Expose
    private Integer totalNumberOfTestMethods;
    @Expose
    private Integer totalNumberOfCreatedCustomExceptions;
    @Expose
    private Integer totalNumberOfDistinctUsedCustomExceptions;
    @Expose
    private Integer totalNumberOfDistinctUsedNotIdentifiedExceptions;
    @Expose
    private Integer totalNumberOfDistinctUsedStandardOrThirdPartyExceptions;
    @Expose
    private Integer totalNumberOfDistinctUsedExceptions;
    @Expose
    private Integer totalNumberOfThrowsStatementsStandardOrThirdPartyExceptions;
    @Expose
    private Integer totalNumberOfThrowsStatementCustomExceptions;
    @Expose
    private Integer totalNumberOfThrowsStatementNotIdentifiedExceptions;
    @Expose
    private Integer totalNumberOfThrowsStatements;
    @Expose
    private Integer totalNumberOfThrowStatementsStandardOrThirdPartyExceptions;
    @Expose
    private Integer totalNumberOfThrowStatementCustomExceptions;
    @Expose
    private Integer totalNumberOfThrowStatementNotIdentifiedExceptions;
    @Expose
    private Integer totalNumberOfThrowStatements;
    @Expose
    private Integer totalNumberOfCoveredThrowStatementsStandardOrThirdPartyExceptions;
    @Expose
    private Integer totalNumberOfCoveredThrowStatementCustomExceptions;
    @Expose
    private Integer totalNumberOfCoveredThrowStatementNotIdentifiedExceptions;
    @Expose
    private Integer totalNumberOfCoveredThrowStatements;

    //consider the exceptions within the test suite
    @Expose
    private Integer totalNumberOfAllTestedNotIdentifiedExceptions;
    //consider the exceptions within the test suite
    @Expose
    private Integer totalNumberOfAllTestedStandardOrThirdPartyExceptions;
    //consider the exceptions within the test suite
    @Expose
    private Integer totalNumberOfAllTestedCustomExceptions;
    //consider the exceptions within the test suite
    @Expose
    private Integer totalNumberOfAllTestedExceptions;

    @Expose
    private Integer totalNumberOfDistinctTestedStandardOrThirdPartyExceptions;
    @Expose
    private Integer totalNumberOfDistinctTestedCustomExceptions;
    @Expose
    private Integer totalNumberOfDistinctTestedExceptions;
    @Expose
    private Integer totalNumberOfDistinctCoveredStandardOrThirdPartyExceptions;
    @Expose
    private Integer totalNumberOfDistinctCoveredCustomExceptions;
    @Expose
    private Integer totalNumberOfDistinctCoveredExceptions;
    @Expose
    private Integer totalNumberOfCustomExceptionsTestMethods;
    @Expose
    private Integer totalNumberOfStandardOrThirdPartyExceptionsTestMethods;
    @Expose
    private Integer totalNumberOfNotIdentifiedExceptionsTestMethods;

    //has repeated methods
    @Expose
    private Integer totalNumberOfExceptionTests;
    //distinct methods
    @Expose
    private Integer totalNumberOfExceptionalBehaviorTestMethods;

    /************** commom **************/
    @Expose
    private Integer commom_totalNumberOfFailInsideTryScope;
    @Expose
    private Integer commom_totalNumberOfFailInsideCatchScope;
    @Expose
    private Integer commom_totalNumberOfFailOutsideTryCatchScope;
    @Expose
    private Integer commom_totalNumberOfFailCalls;

    /************** JUNIT **************/
    @Expose
    private Integer junit_totalNumberOfExpectedAttribute;
    @Expose
    private Integer junit_totalNumberOfExpectCalls;
    @Expose
    private Integer junit_totalNumberOfAssertThrows;

    /************** ASSERTJ **************/
    @Expose
    private Integer assertj_totalNumberOfAsserts;
    @Expose
    private Integer assertj_totalNumberOfAssertThatExceptionName;
    @Expose
    private Integer assertj_totalNumberOfAssertThatExceptionOfType;
    @Expose
    private Integer assertj_totalNumberOfAssertThat;
    @Expose
    private Integer assertj_totalNumberOfAssertThatThrownBy;

    /************** TESTNG **************/
    @Expose
    private Integer testNG_totalNumberOfExpectedExceptionsAttribute;

    //CATCHS
    @Expose
    private Integer totalNumberOfCatchStatementCustomExceptions;
    @Expose
    private Integer totalNumberOfCatchStatementsStandardOrThirdPartyExceptions;
    @Expose
    private Integer totalNumberOfCatchStatementNotIdentifiedExceptions;
    @Expose
    private Integer totalNumberOfCatchStatements;

    //USES
    @Expose
    private Integer totalNumberOfCustomExceptionsUses;
    @Expose
    private Integer totalNumberOfStandardOrThirdPartyExceptionsUses;
    @Expose
    private Integer totalNumberOfNotIdentifiedExceptionsUses;
    @Expose
    private Integer totalNumberOfExceptionsUses;



    //If this flag is true, all dots (.) will be changed to #.
    private boolean adjustStringToMongoDB;

    //Flag to control the execution flow
    private boolean isTestedExceptionsCalculated;


    public StatisticsExtractor(CombinedTypeExtractor combinedTypeExtractor, ModelExtractor models, boolean adjustStringToMongoDB) {
        this.models = models;
        this.combinedTypeExtractor = combinedTypeExtractor;
        this.isTestedExceptionsCalculated = false;

        this.setOfTestFiles = new HashSet<>();

        this.testedStandardOrThirdPartyExceptionsCounter = new HashMap<String, Integer>();
        this.testedCustomExceptionsCounter = new HashMap<String, Integer>();
        this.testedNotIdentifiedExceptionsCounter = new HashMap<String, Integer>();
        this.testedAndUsedStandardOrThirdPartyExceptionsCounter = new HashMap<String, Integer>();
        this.testedAndUsedCustomExceptionsCounter = new HashMap<String, Integer>();
        this.throwsStandardOrThirdPartyExceptionsCounter = new HashMap<String, Integer>();
        this.throwsCustomExceptionsCounter = new HashMap<String, Integer>();
        this.throwsNotIdentifiedExceptionsCounter = new HashMap<String, Integer>();
        this.throwStandardOrThirdPartyExceptionsExceptionsCounter = new HashMap<String, Integer>();
        this.throwCustomExceptionsCounter = new HashMap<String, Integer>();
        this.throwNotIdentifiedExceptionsCounter = new HashMap<String, Integer>();
        this.throwCustomExceptionsCoverageCounter = new HashMap<String, Map<String, Integer>>();
        this.throwNotIdentifiedExceptionsCoverageCounter = new HashMap<String, Map<String, Integer>>();
        this.throwStandardOrThirdPartyExceptionsCoverageCounter = new HashMap<String, Map<String, Integer>>();
        this.catchCustomExceptionsCounter = new HashMap<String, Integer>();
        this.catchStandardOrThirdPartyExceptionsCounter = new HashMap<String, Integer>();
        this.catchNotIdentifiedExceptionsCounter = new HashMap<String, Integer>();
        this.customCreatedExceptions = new LinkedList<>();

        this.customExceptionsUsed = new HashMap<String, Integer>();
        this.notIdentifiedExceptionsUsed = new HashMap<String, Integer>();
        this.standardOrThirdPartyExceptionsUsed = new HashMap<String, Integer>();
        this.customExceptionsTestMethodCounter = new HashMap<String, Integer>();
        this.standardOrThirdPartyExceptionsTestMethodCounter = new HashMap<String, Integer>();
        this.notIdentifiedExceptionsTestMethodCounter = new HashMap<String, Integer>();
        this.distinctExceptionsTestMethodCounter = new HashMap<String, Integer>();

       this.adjustStringToMongoDB = adjustStringToMongoDB;
    }



    private String adjustStringToMongoDBRestrictions(String stringWithDots) {
        if (adjustStringToMongoDB) {
            return stringWithDots.replace(".", "#");
        }
        return stringWithDots;
    }


    private void increaseMapCounter(String key, Map<String, Integer> map) {
        int currentSize;
        if (map.containsKey(key)) {
            currentSize = map.get(key);
            map.put(key, ++currentSize);
        } else {
            map.put(key, 1);
        }
    }

    private int sumAllMapValues(Map<String, Integer> map) {
        int total = 0;
        for (String key : map.keySet()) {
            total += map.get(key);
        }
        return total;
    }



    public List<String> calculateCustomExceptionsCreatedCounter() {
        if (customCreatedExceptions.isEmpty()) {
            for (NewExceptionModel model : models.getNewExceptionModels()) {
                customCreatedExceptions.add(model.getParentClassName(0));
            }
        }
        return customCreatedExceptions;
    }

    public Map<String, Integer> calculateTotalOfThrowsCustomExceptions() {
        if (throwsCustomExceptionsCounter.isEmpty()) {
            for (ThrowsExceptionModel model : models.getThrowsExceptionModels()) {
                if (!model.isInsideATest() && calculateCustomExceptionsCreatedCounter().contains(model.getException())) {
                    increaseMapCounter(model.getException(), throwsCustomExceptionsCounter);
                }
            }
        }
        return throwsCustomExceptionsCounter;
    }

    public Map<String, Integer> calculateTotalOfThrowStatementsStandardOrThirdPartyExceptions() {
        if (throwStandardOrThirdPartyExceptionsExceptionsCounter.isEmpty()) {
            for (ThrowExceptionModel model : models.getThrowExceptionModels()) {
                if (!model.isInsideATest() && !calculateCustomExceptionsCreatedCounter().contains(model.getException()) && !model.getException().equals("NOT IDENTIFIED")) {
                    increaseMapCounter(model.getException(), throwStandardOrThirdPartyExceptionsExceptionsCounter);
                    updateCoverage(model, throwStandardOrThirdPartyExceptionsCoverageCounter);
                }
            }
        }
        return throwStandardOrThirdPartyExceptionsExceptionsCounter;
    }

    public Map<String, Integer> calculateTotalOfThrowStatementsCustomExceptions() {
        if (throwCustomExceptionsCounter.isEmpty()) {
            for (ThrowExceptionModel model : models.getThrowExceptionModels()) {
                if (!model.isInsideATest() && calculateCustomExceptionsCreatedCounter().contains(model.getException())) {
                    increaseMapCounter(model.getException(), throwCustomExceptionsCounter);
                    updateCoverage(model, throwCustomExceptionsCoverageCounter);
                }
            }
        }
        return throwCustomExceptionsCounter;
    }

    private void updateCoverage(ThrowExceptionModel model, Map<String, Map<String, Integer>> exceptionCverageCounterMap) {
        String signature = model.getFullClassPackagePath() + '[' + model.getThrowStatementLine() + ']';
        signature = adjustStringToMongoDBRestrictions(signature);
        //String signature = model.getFullFilePath() + '[' + model.getLineRange() + ']';
        //adds the full path to the throw exception and the boolean value corresponding if the line is covered or not
        if(!exceptionCverageCounterMap.containsKey(model.getException())){
            exceptionCverageCounterMap.put(model.getException(), new HashMap<String, Integer>());
        }
        exceptionCverageCounterMap.get(model.getException()).put(signature, model.getNumberOfTimesTheLineWasExecuted());
    }

    public Map<String, Integer> calculateTotalOfThrowStatementsNotIdentifiedExceptions() {
        if (throwNotIdentifiedExceptionsCounter.isEmpty()) {
            for (ThrowExceptionModel model : models.getThrowExceptionModels()) {
                if (!model.isInsideATest() && model.getException().equals("NOT IDENTIFIED")) {
                    increaseMapCounter(model.getException(), throwNotIdentifiedExceptionsCounter);
                    updateCoverage(model, throwNotIdentifiedExceptionsCoverageCounter);
                }
            }
        }
        return throwNotIdentifiedExceptionsCounter;
    }


    public Map<String, Integer> calculateTotalOfCatchStandardOrThirdPartyExceptions() {
        if (catchStandardOrThirdPartyExceptionsCounter.isEmpty()) {
            for (CatchModel model : models.getCatchModels()) {
                if (!model.isInsideATest()) {
                    for (String exception : model.getCatchedExceptions()) {
                        if (!calculateCustomExceptionsCreatedCounter().contains(exception) && !exception.equals("NOT IDENTIFIED")) {
                            increaseMapCounter(exception, catchStandardOrThirdPartyExceptionsCounter);
                        }
                    }
                }
            }
        }
        return catchStandardOrThirdPartyExceptionsCounter;
    }

    public Map<String, Integer> calculateTotalOfCatchStatementsCustomExceptions() {
        if (catchCustomExceptionsCounter.isEmpty()) {
            for (CatchModel model : models.getCatchModels()) {
                if (!model.isInsideATest()) {
                    for (String exception : model.getCatchedExceptions()) {
                        if (calculateCustomExceptionsCreatedCounter().contains(exception)) {
                            increaseMapCounter(exception, catchCustomExceptionsCounter);
                        }
                    }
                }
            }
        }
        return catchCustomExceptionsCounter;
    }

    public Map<String, Integer> calculateTotalOfCatchStatementsNotIdentifiedExceptions() {
        if (catchNotIdentifiedExceptionsCounter.isEmpty()) {
            for (CatchModel model : models.getCatchModels()) {
                if (!model.isInsideATest()) {
                    for (String exception : model.getCatchedExceptions()) {
                        if (exception.equals("NOT IDENTIFIED")) {
                            increaseMapCounter(exception, catchNotIdentifiedExceptionsCounter);
                        }
                    }
                }
            }
        }
        return catchNotIdentifiedExceptionsCounter;
    }


    /**
     * If we have throws Exception1, Exception2. Each exception will be counted as different throws instruction
     * @return
     */
    public Map<String, Integer> calculateTotalOfThrowsStandardOrThirdPartyExceptions() {
        if (throwsStandardOrThirdPartyExceptionsCounter.isEmpty()) {
            for (ThrowsExceptionModel model : models.getThrowsExceptionModels()) {
                if (!model.isInsideATest() && !calculateCustomExceptionsCreatedCounter().contains(model.getException()) && !model.getException().equals("NOT IDENTIFIED")) {
                    increaseMapCounter(model.getException(), throwsStandardOrThirdPartyExceptionsCounter);
                }
            }
        }
        return throwsStandardOrThirdPartyExceptionsCounter;
    }

    /**
     * If we have throws Exception1, Exception2. Each exception will be counted as different throws instruction
     * @return
     */
    public Map<String, Integer> calculateTotalOfThrowsNotIdentifiedExceptions() {
        if (throwsNotIdentifiedExceptionsCounter.isEmpty()) {
            for (ThrowsExceptionModel model : models.getThrowsExceptionModels()) {
                if (!model.isInsideATest() && model.getException().equals("NOT IDENTIFIED")) {
                    increaseMapCounter(model.getException(), throwsNotIdentifiedExceptionsCounter);
                }
            }
        }
        return throwsNotIdentifiedExceptionsCounter;
    }


    /**
     * What are the Exception Testing Constructs?
     * 1 - Em @Test(Expected=Exception.class)
     * 2 - Em fail()...Catch(Exception | OutraException e )
     * 3 - Obj.expect(Exception.class) ou Obj.expect("Algum texto")
     * 4 - AssertThrow(Exception.class)
     * 5 - AssertJ
     * 6 - TestNG
     * <p>
     */
    public void calculateTestedExceptionsCounter() {


        if (!this.isTestedExceptionsCalculated) {

            for (JUnit_ExpectedExceptionTestAnnotationModel model : models.getExpectedExceptionAnnotationModels()) {
                String signature = model.getPackageName() + "." + model.getParentClassName().get(0) + "." + model.getParentMethodName(0);
                //signature = signature.replace("(","").replace(")","");
                signature = adjustStringToMongoDBRestrictions(signature);
                if (calculateCustomExceptionsCreatedCounter().contains(model.getExpectedExceptionName())) {
                    increaseMapCounter(signature, customExceptionsTestMethodCounter);
                    increaseMapCounter(adjustStringToMongoDBRestrictions(model.getExpectedExceptionName()), testedCustomExceptionsCounter);
                } else if (isAValidException(model.getExpectedExceptionName())){
                    increaseMapCounter(signature, standardOrThirdPartyExceptionsTestMethodCounter);
                    increaseMapCounter(adjustStringToMongoDBRestrictions(model.getExpectedExceptionName()), testedStandardOrThirdPartyExceptionsCounter);
                } else {
                    increaseMapCounter(signature, notIdentifiedExceptionsTestMethodCounter);
                    increaseMapCounter("NOT IDENTIFIED", testedNotIdentifiedExceptionsCounter);
                }

            }

            for (Commom_FailCallModel model : models.getFailCallModels()) {
                if (model.getTryCatchScope().equals("catch") || model.getTryCatchScope().equals("OUTSIDE")) {
                    continue;
                }
                for (String exception : model.getCatchedExceptions()) {
                    String signature = model.getPackageName() + "." + model.getParentClassName(0) + "." + model.getParentMethodName(0);
                    signature = adjustStringToMongoDBRestrictions(signature);
                    if (calculateCustomExceptionsCreatedCounter().contains(exception)) {
                        increaseMapCounter(signature, customExceptionsTestMethodCounter);
                        increaseMapCounter(adjustStringToMongoDBRestrictions(exception), testedCustomExceptionsCounter);
                    } else if (isAValidException(exception)){
                        increaseMapCounter(signature, standardOrThirdPartyExceptionsTestMethodCounter);
                        increaseMapCounter(adjustStringToMongoDBRestrictions(exception), testedStandardOrThirdPartyExceptionsCounter);
                    } else {
                        increaseMapCounter(signature, notIdentifiedExceptionsTestMethodCounter);
                        increaseMapCounter("NOT IDENTIFIED", testedNotIdentifiedExceptionsCounter);
                    }
                }

            }

            //Not always in a expect call we have an Exception
            for (JUnit_ExpectExceptionTestCallModel model : models.getExpectExceptionCallModels()) {
                String signature = model.getPackageName() + "." + model.getParentClassName(0) + "." + model.getParentMethodName(0);
                //signature = signature.replace("(","").replace(")","");
                signature = adjustStringToMongoDBRestrictions(signature);
                if (calculateCustomExceptionsCreatedCounter().contains(model.getExpectedExceptionName())) {
                    increaseMapCounter(signature, customExceptionsTestMethodCounter);
                    increaseMapCounter(adjustStringToMongoDBRestrictions(model.getExpectedExceptionName()), testedCustomExceptionsCounter);
                } else if (isAValidException(model.getExpectedExceptionName())) {
                    increaseMapCounter(signature, standardOrThirdPartyExceptionsTestMethodCounter);
                    increaseMapCounter(adjustStringToMongoDBRestrictions(model.getExpectedExceptionName()), testedStandardOrThirdPartyExceptionsCounter);
                } else {
                    increaseMapCounter(signature, notIdentifiedExceptionsTestMethodCounter);
                    increaseMapCounter("NOT IDENTIFIED", testedNotIdentifiedExceptionsCounter);
                }
            }

            for (JUnit_assertThrowsModel model : models.getJUnitassertThrowsModels()) {
                String signature = model.getPackageName() + "." + model.getParentClassName(0) + "." + model.getParentMethodName(0);
                //signature = signature.replace("(","").replace(")","");
                signature = adjustStringToMongoDBRestrictions(signature);
                if (calculateCustomExceptionsCreatedCounter().contains(model.getExpectedExceptionName())) {
                    increaseMapCounter(signature, customExceptionsTestMethodCounter);
                    increaseMapCounter(adjustStringToMongoDBRestrictions(model.getExpectedExceptionName()), testedCustomExceptionsCounter);
                } else if (isAValidException(model.getExpectedExceptionName())){
                    increaseMapCounter(signature, standardOrThirdPartyExceptionsTestMethodCounter);
                    increaseMapCounter(adjustStringToMongoDBRestrictions(model.getExpectedExceptionName()), testedStandardOrThirdPartyExceptionsCounter);
                } else {
                    increaseMapCounter(signature, notIdentifiedExceptionsTestMethodCounter);
                    increaseMapCounter("NOT IDENTIFIED", testedNotIdentifiedExceptionsCounter);
                }
            }

            for (AssertJ_assertThatModel model : models.getAssertJAssertThatModels()) {
                String signature = model.getPackageName() + "." + model.getParentClassName(0) + "." + model.getParentMethodName(0);
                //signature = signature.replace("(","").replace(")","");
                signature = adjustStringToMongoDBRestrictions(signature);
                if (calculateCustomExceptionsCreatedCounter().contains(model.getExpectedExceptionName())) {
                    increaseMapCounter(signature, customExceptionsTestMethodCounter);
                    increaseMapCounter(adjustStringToMongoDBRestrictions(model.getExpectedExceptionName()), testedCustomExceptionsCounter);
                } else if (isAValidException(model.getExpectedExceptionName())) {
                    increaseMapCounter(signature, standardOrThirdPartyExceptionsTestMethodCounter);
                    increaseMapCounter(adjustStringToMongoDBRestrictions(model.getExpectedExceptionName()), testedStandardOrThirdPartyExceptionsCounter);
                } else {
                    increaseMapCounter(signature, notIdentifiedExceptionsTestMethodCounter);
                    increaseMapCounter("NOT IDENTIFIED", testedNotIdentifiedExceptionsCounter);
                }
            }

            for (AssertJ_assertThatExceptionNameModel model : models.getAssertJAssertThatExceptionNameModels()) {
                String signature = model.getPackageName() + "." + model.getParentClassName(0) + "." + model.getParentMethodName(0);
                //signature = signature.replace("(","").replace(")","");
                signature = adjustStringToMongoDBRestrictions(signature);
                if (calculateCustomExceptionsCreatedCounter().contains(model.getExpectedExceptionName())) {
                    increaseMapCounter(signature, customExceptionsTestMethodCounter);
                    increaseMapCounter(adjustStringToMongoDBRestrictions(model.getExpectedExceptionName()), testedCustomExceptionsCounter);
                } else if (isAValidException(model.getExpectedExceptionName())) {
                    increaseMapCounter(signature, standardOrThirdPartyExceptionsTestMethodCounter);
                    increaseMapCounter(adjustStringToMongoDBRestrictions(model.getExpectedExceptionName()), testedStandardOrThirdPartyExceptionsCounter);
                } else {
                    increaseMapCounter(signature, notIdentifiedExceptionsTestMethodCounter);
                    increaseMapCounter("NOT IDENTIFIED", testedNotIdentifiedExceptionsCounter);
                }
            }

            for (AssertJ_assertThatExceptionOfTypeModel model : models.getAssertJAssertThatExceptionOfTypeModels()) {
                String signature = model.getPackageName() + "." + model.getParentClassName(0) + "." + model.getParentMethodName(0);
                //signature = signature.replace("(","").replace(")","");
                signature = adjustStringToMongoDBRestrictions(signature);
                if (calculateCustomExceptionsCreatedCounter().contains(model.getExpectedExceptionName())) {
                    increaseMapCounter(signature, customExceptionsTestMethodCounter);
                    increaseMapCounter(adjustStringToMongoDBRestrictions(model.getExpectedExceptionName()), testedCustomExceptionsCounter);
                } else if (isAValidException(model.getExpectedExceptionName())) {
                    increaseMapCounter(signature, standardOrThirdPartyExceptionsTestMethodCounter);
                    increaseMapCounter(adjustStringToMongoDBRestrictions(model.getExpectedExceptionName()), testedStandardOrThirdPartyExceptionsCounter);
                } else {
                    increaseMapCounter(signature, notIdentifiedExceptionsTestMethodCounter);
                    increaseMapCounter("NOT IDENTIFIED", testedNotIdentifiedExceptionsCounter);
                }
            }

            for (AssertJ_assertThatThrownByModel model : models.getAssertJAssertThatThrownByModels()) {
                String signature = model.getPackageName() + "." + model.getParentClassName(0) + "." + model.getParentMethodName(0);
                //signature = signature.replace("(","").replace(")","");
                signature = adjustStringToMongoDBRestrictions(signature);
                if (calculateCustomExceptionsCreatedCounter().contains(model.getExpectedExceptionName())) {
                    increaseMapCounter(signature, customExceptionsTestMethodCounter);
                    increaseMapCounter(adjustStringToMongoDBRestrictions(model.getExpectedExceptionName()), testedCustomExceptionsCounter);
                } else if (isAValidException(model.getExpectedExceptionName())) {
                    increaseMapCounter(signature, standardOrThirdPartyExceptionsTestMethodCounter);
                    increaseMapCounter(adjustStringToMongoDBRestrictions(model.getExpectedExceptionName()), testedStandardOrThirdPartyExceptionsCounter);
                } else {
                    increaseMapCounter(signature, notIdentifiedExceptionsTestMethodCounter);
                    increaseMapCounter("NOT IDENTIFIED", testedNotIdentifiedExceptionsCounter);
                }
            }

            for(TestNG_ExpectedExceptionsTestAnnotationModel model : models.getTestNG_expectedExceptionsTestAnnotationModels()){
                String signature = model.getPackageName() + "." + model.getParentClassName(0) + "." + model.getParentMethodName(0);
                signature = adjustStringToMongoDBRestrictions(signature);
                for(String exceptionName : model.getExpectedExceptionsNames()){
                    if (calculateCustomExceptionsCreatedCounter().contains(exceptionName)) {
                        increaseMapCounter(signature, customExceptionsTestMethodCounter);
                        increaseMapCounter(adjustStringToMongoDBRestrictions(exceptionName), testedCustomExceptionsCounter);
                    } else if (isAValidException(exceptionName)) {
                        increaseMapCounter(signature, standardOrThirdPartyExceptionsTestMethodCounter);
                        increaseMapCounter(adjustStringToMongoDBRestrictions(exceptionName), testedStandardOrThirdPartyExceptionsCounter);
                    } else {
                        increaseMapCounter(signature, notIdentifiedExceptionsTestMethodCounter);
                        increaseMapCounter("NOT IDENTIFIED", testedNotIdentifiedExceptionsCounter);
                    }
                }

            }

            this.isTestedExceptionsCalculated = true;
        }

    }

    private boolean isAValidException(String exceptionName){
        if (exceptionName.contains("Exception") || exceptionName.contains("Error") || exceptionName.contains("Throwable")){
            return true;
        }
        return false;

    }

    public void calculateTestedAndUsedExceptionsCounter() {
        for (Map.Entry<String, Integer> entry : testedStandardOrThirdPartyExceptionsCounter.entrySet()) {
            if (standardOrThirdPartyExceptionsUsed.containsKey(entry.getKey())) {
                testedAndUsedStandardOrThirdPartyExceptionsCounter.put(entry.getKey(), entry.getValue());
            }
        }

        for (Map.Entry<String, Integer> entry : testedCustomExceptionsCounter.entrySet()) {
            if (customExceptionsUsed.containsKey(entry.getKey())) {
                testedAndUsedCustomExceptionsCounter.put(entry.getKey(), entry.getValue());
            }
        }

    }


    public int getTotalNumberOfDistinctUsedNotIdentifiedExceptions() {
        if (totalNumberOfDistinctUsedNotIdentifiedExceptions != null) {
            return totalNumberOfDistinctUsedNotIdentifiedExceptions;
        }

        mergeMap(calculateTotalOfThrowsNotIdentifiedExceptions(), notIdentifiedExceptionsUsed);
        mergeMap(calculateTotalOfThrowStatementsNotIdentifiedExceptions(), notIdentifiedExceptionsUsed);
        mergeMap(calculateTotalOfCatchStatementsNotIdentifiedExceptions(), notIdentifiedExceptionsUsed);

        return notIdentifiedExceptionsUsed.size();
    }


    public int getTotalNumberOfNotIdentifiedExceptionsUses() {
        if (totalNumberOfNotIdentifiedExceptionsUses != null) {
            return totalNumberOfNotIdentifiedExceptionsUses;
        }
        int total = 0;
        total += this.getTotalNumberOfThrowsStatementNotIdentifiedExceptions();
        total += this.getTotalNumberOfThrowStatementNotIdentifiedExceptions();
        total += this.getTotalNumberOfCatchStatementNotIdentifiedExceptions();

        return total;
    }


    public int getTotalNumberOfCustomExceptionsUses() {
        if (totalNumberOfCustomExceptionsUses != null) {
            return totalNumberOfCustomExceptionsUses;
        }
        int total = 0;
        total += this.getTotalNumberOfThrowsStatementCustomExceptions();
        total += this.getTotalNumberOfThrowStatementCustomExceptions();
        total += this.getTotalNumberOfCatchStatementCustomExceptions();

        return total;
    }


    public int getTotalNumberOfStandardOrThirdPartyExceptionsUses() {
        if (totalNumberOfStandardOrThirdPartyExceptionsUses != null) {
            return totalNumberOfStandardOrThirdPartyExceptionsUses;
        }
        int total = 0;
        total += this.getTotalNumberOfThrowsStatementsStandardOrThirdPartyExceptions();
        total += this.getTotalNumberOfThrowStatementsStandardOrThirdPartyExceptions();
        total += this.getTotalNumberOfCatchStatementsStandardOrThirdPartyExceptions();


        return total;
    }

    public int getTotalNumberOfExceptionsUses() {
        if (totalNumberOfExceptionsUses != null) {
            return totalNumberOfExceptionsUses;
        }
        int total = 0;
        total += this.getTotalNumberOfStandardOrThirdPartyExceptionsUses();
        total += this.getTotalNumberOfCustomExceptionsUses();
        total += this.getTotalNumberOfNotIdentifiedExceptionsUses();

        return total;
    }

    public int getTotalNumberOfDistinctUsedStandardOrThirdPartyExceptions() {
        if (totalNumberOfDistinctUsedStandardOrThirdPartyExceptions != null) {
            return totalNumberOfDistinctUsedStandardOrThirdPartyExceptions;
        }

        mergeMap(calculateTotalOfThrowsStandardOrThirdPartyExceptions(), standardOrThirdPartyExceptionsUsed);
        mergeMap(calculateTotalOfThrowStatementsStandardOrThirdPartyExceptions(), standardOrThirdPartyExceptionsUsed);
        mergeMap(calculateTotalOfCatchStandardOrThirdPartyExceptions(), standardOrThirdPartyExceptionsUsed);
        return standardOrThirdPartyExceptionsUsed.size();
    }

    public int getTotalNumberOfDistinctUsedCustomExceptions() {
        if (totalNumberOfDistinctUsedCustomExceptions != null) {
            return totalNumberOfDistinctUsedCustomExceptions;
        }
        mergeMap(calculateTotalOfThrowsCustomExceptions(), customExceptionsUsed);
        mergeMap(calculateTotalOfThrowStatementsCustomExceptions(), customExceptionsUsed);
        mergeMap(calculateTotalOfCatchStatementsCustomExceptions(), customExceptionsUsed);
        return customExceptionsUsed.size();
    }


    public int getTotalNumberOfCreatedCustomExceptions() {
        if (totalNumberOfCreatedCustomExceptions != null) {
            return totalNumberOfCreatedCustomExceptions;
        }
        return calculateCustomExceptionsCreatedCounter().size();
    }

    public int getTestNG_totalNumberOfExpectedExceptionsAttribute() {
        if (testNG_totalNumberOfExpectedExceptionsAttribute != null) {
            return testNG_totalNumberOfExpectedExceptionsAttribute;
        }
        return models.getTestNG_expectedExceptionsTestAnnotationModels().size();
    }

    public int getJunit_totalNumberOfExpectedAttribute() {
        if (junit_totalNumberOfExpectedAttribute != null) {
            return junit_totalNumberOfExpectedAttribute;
        }
        return models.getExpectedExceptionAnnotationModels().size();
    }

    public int getJunit_totalNumberOfExpectCalls() {
        if (junit_totalNumberOfExpectCalls != null) {
            return junit_totalNumberOfExpectCalls;
        }
        return models.getExpectExceptionCallModels().size();
    }


    public int getTotalNumberOfStandardOrThirdPartyExceptionsTestMethods() {
        if (totalNumberOfStandardOrThirdPartyExceptionsTestMethods != null) {
            return totalNumberOfStandardOrThirdPartyExceptionsTestMethods;
        }
        return standardOrThirdPartyExceptionsTestMethodCounter.size();
    }

    public int getTotalNumberOfCustomExceptionsTestMethods() {
        if (totalNumberOfCustomExceptionsTestMethods != null) {
            return totalNumberOfCustomExceptionsTestMethods;
        }
        return customExceptionsTestMethodCounter.size();
    }

    public int getTotalNumberOfNotIdentifiedExceptionsTestMethods() {
        if (totalNumberOfNotIdentifiedExceptionsTestMethods != null) {
            return totalNumberOfNotIdentifiedExceptionsTestMethods;
        }
        return notIdentifiedExceptionsTestMethodCounter.size();
    }

    public int getTotalNumberOfAllTestedStandardOrThirdPartyExceptions() {
        if (totalNumberOfAllTestedStandardOrThirdPartyExceptions != null) {
            return totalNumberOfAllTestedStandardOrThirdPartyExceptions;
        }
        return testedStandardOrThirdPartyExceptionsCounter.size();
    }

    public int getTotalNumberOfAllTestedNotIdentifiedExceptions() {
        if (totalNumberOfAllTestedNotIdentifiedExceptions != null) {
            return totalNumberOfAllTestedNotIdentifiedExceptions;
        }
        calculateTestedAndUsedExceptionsCounter();
        return testedNotIdentifiedExceptionsCounter.size();
    }


    public int getTotalNumberOfAllTestedCustomExceptions() {
        if (totalNumberOfAllTestedCustomExceptions != null) {
            return totalNumberOfAllTestedCustomExceptions;
        }
        return testedCustomExceptionsCounter.size();
    }

    private Integer getNumberOfDistinctCoveredExceptions(Map<String, Map<String, Integer>> mapAux){
        boolean exceptionHasCoverageData = false;
        Integer numberOfDistinctCoveredExceptions = null;
        for(String exceptionName : mapAux.keySet()){
            exceptionHasCoverageData = false;
            for (Map.Entry<String, Integer> entry : mapAux.get(exceptionName).entrySet()){
                Integer entryValue = entry.getValue();
                if (entryValue != null){
                    exceptionHasCoverageData = true;
                    if(numberOfDistinctCoveredExceptions == null){
                        numberOfDistinctCoveredExceptions = 0;
                    }
                    if (entry.getValue() > 0){
                        numberOfDistinctCoveredExceptions++;
                        break;
                    }
                }
            }
        }
        return numberOfDistinctCoveredExceptions;
    }

    public Integer getTotalNumberOfDistinctCoveredStandardOrThirdPartyExceptions() {
        if (totalNumberOfDistinctCoveredStandardOrThirdPartyExceptions != null) {
            return totalNumberOfDistinctCoveredStandardOrThirdPartyExceptions;
        }
        return getNumberOfDistinctCoveredExceptions(throwStandardOrThirdPartyExceptionsCoverageCounter);
    }

    public Integer getTotalNumberOfDistinctCoveredCustomExceptions() {
        if (totalNumberOfDistinctCoveredCustomExceptions != null) {
            return totalNumberOfDistinctCoveredCustomExceptions;
        }
        return getNumberOfDistinctCoveredExceptions(throwCustomExceptionsCoverageCounter);
    }

    public Integer getTotalNumberOfDistinctCoveredExceptions() {
        if (totalNumberOfDistinctCoveredExceptions != null) {
            return totalNumberOfDistinctCoveredExceptions;
        }
        Integer aux1;
        Integer aux2;

        if(getTotalNumberOfDistinctCoveredStandardOrThirdPartyExceptions() == null && getTotalNumberOfDistinctCoveredCustomExceptions() == null){
            return null;
        } else {
            if (getTotalNumberOfDistinctCoveredStandardOrThirdPartyExceptions() == null){
                aux1 = 0;
            } else {
                aux1 = getTotalNumberOfDistinctCoveredStandardOrThirdPartyExceptions();
            }
            if (getTotalNumberOfDistinctCoveredCustomExceptions() == null){
                aux2 = 0;
            } else {
                aux2 = getTotalNumberOfDistinctCoveredCustomExceptions();
            }
        }
        return aux1 + aux2;
    }


    public int getTotalNumberOfDistinctTestedStandardOrThirdPartyExceptions() {
        if (totalNumberOfDistinctTestedStandardOrThirdPartyExceptions != null) {
            return totalNumberOfDistinctTestedStandardOrThirdPartyExceptions;
        }
        calculateTestedAndUsedExceptionsCounter();
        return testedAndUsedStandardOrThirdPartyExceptionsCounter.size();
    }

    public int getTotalNumberOfDistinctTestedCustomExceptions() {
        if (totalNumberOfDistinctTestedCustomExceptions != null) {
            return totalNumberOfDistinctTestedCustomExceptions;
        }
        calculateTestedAndUsedExceptionsCounter();
        return testedAndUsedCustomExceptionsCounter.size();
    }

    public int getTotalNumberOfDistinctTestedExceptions() {
        if (totalNumberOfDistinctTestedExceptions != null) {
            return totalNumberOfDistinctTestedExceptions;
        }
        calculateTestedAndUsedExceptionsCounter();
        return testedAndUsedCustomExceptionsCounter.size() + testedAndUsedStandardOrThirdPartyExceptionsCounter.size();
    }


    public int getTotalNumberOfTestMethods() {
        if (totalNumberOfTestMethods != null) {
            return totalNumberOfTestMethods;
        }
        return models.getOrdinaryAnnotationTestModels().size() + models.getOrdinaryExtendedTestModels().size();
    }

    public int getCommom_totalNumberOfFailCalls() {
        if (commom_totalNumberOfFailCalls != null) {
            return commom_totalNumberOfFailCalls;
        }
        return models.getFailCallModels().size();
    }

    public int getCommom_totalNumberOfFailInsideCatchScope() {
        if (commom_totalNumberOfFailInsideCatchScope != null) {
            return commom_totalNumberOfFailInsideCatchScope;
        }
        int counter = 0;
        for (Commom_FailCallModel md : models.getFailCallModels()) {
            if (md.getTryCatchScope().equals("catch")) {
                counter++;
            }
        }
        return counter;
    }

    public int getCommom_totalNumberOfFailInsideTryScope() {
        if (commom_totalNumberOfFailInsideTryScope != null) {
            return commom_totalNumberOfFailInsideTryScope;
        }
        int counter = 0;
        for (Commom_FailCallModel md : models.getFailCallModels()) {
            if (md.getTryCatchScope().equals("try")) {
                counter++;
            }
        }
        return counter;
    }

    public int getCommom_totalNumberOfFailOutsideTryCatchScope() {
        if (commom_totalNumberOfFailOutsideTryCatchScope != null) {
            return commom_totalNumberOfFailOutsideTryCatchScope;
        }
        int counter = 0;
        for (Commom_FailCallModel md : models.getFailCallModels()) {
            if (md.getTryCatchScope().equals("OUTSIDE")) {
                counter++;
            }
        }
        return counter;
    }

    public int getJunit_totalNumberOfAssertThrows() {
        if (junit_totalNumberOfAssertThrows != null) {
            return junit_totalNumberOfAssertThrows;
        }
        return models.getJUnitassertThrowsModels().size();
    }

    public int getAssertj_totalNumberOfAsserts() {
        if (assertj_totalNumberOfAsserts != null) {
            return assertj_totalNumberOfAsserts;
        }
        return models.getAssertJAssertThatExceptionOfTypeModels().size()
                + models.getAssertJAssertThatThrownByModels().size()
                + models.getAssertJAssertThatExceptionNameModels().size()
                + models.getAssertJAssertThatModels().size();
    }

    public int getAssertj_totalNumberOfAssertThat() {
        if (assertj_totalNumberOfAssertThat != null) {
            return assertj_totalNumberOfAssertThat;

        }
        return models.getAssertJAssertThatModels().size();
    }

    public int getAssertj_totalNumberOfAssertThatExceptionName() {
        if (assertj_totalNumberOfAssertThatExceptionName != null) {
            return assertj_totalNumberOfAssertThatExceptionName;

        }
        return models.getAssertJAssertThatExceptionNameModels().size();
    }

    public int getAssertj_totalNumberOfAssertThatExceptionOfType() {
        if (assertj_totalNumberOfAssertThatExceptionOfType != null) {
            return assertj_totalNumberOfAssertThatExceptionOfType;

        }
        return models.getAssertJAssertThatExceptionOfTypeModels().size();
    }

    public int getAssertj_totalNumberOfAssertThatThrownBy() {
        if (assertj_totalNumberOfAssertThatThrownBy != null) {
            return assertj_totalNumberOfAssertThatThrownBy;

        }
        return models.getAssertJAssertThatThrownByModels().size();
    }

    public int getTotalNumberOfThrowStatementCustomExceptions() {
        if (totalNumberOfThrowStatementCustomExceptions != null) {
            return totalNumberOfThrowStatementCustomExceptions;
        }
        return sumAllMapValues(calculateTotalOfThrowStatementsCustomExceptions());
    }

    public int getTotalNumberOfThrowStatementsStandardOrThirdPartyExceptions() {
        if (totalNumberOfThrowStatementsStandardOrThirdPartyExceptions != null) {
            return totalNumberOfThrowStatementsStandardOrThirdPartyExceptions;
        }
        return sumAllMapValues(calculateTotalOfThrowStatementsStandardOrThirdPartyExceptions());
    }

    public int getTotalNumberOfThrowStatementsNotIdentifiedExceptions() {
        if (totalNumberOfThrowStatementNotIdentifiedExceptions != null) {
            return totalNumberOfThrowStatementNotIdentifiedExceptions;
        }
        return sumAllMapValues(calculateTotalOfThrowStatementsNotIdentifiedExceptions());
    }

    public int getTotalNumberOfThrowStatements() {
        if (totalNumberOfThrowStatements != null) {
            return totalNumberOfThrowStatements;
        }
        return getTotalNumberOfThrowStatementCustomExceptions() +
                getTotalNumberOfThrowStatementsStandardOrThirdPartyExceptions() +
                getTotalNumberOfThrowStatementsNotIdentifiedExceptions();
    }

    private int sumAllCoverageMapValues(Map<String, Map<String, Integer>> coverageMap) {
        int numberOfCoveredThrowsStatements = 0;
        Map<String, Integer> lineMap = null;
        for(String exceptionName : coverageMap.keySet()){
            lineMap = coverageMap.get(exceptionName);
            for(String fullPathToThrowStatement : lineMap.keySet()){
                Integer coverageHits = lineMap.get(fullPathToThrowStatement);
                if(coverageHits != null && coverageHits > 0){
                    numberOfCoveredThrowsStatements++;
                }
            }
        }
        return numberOfCoveredThrowsStatements;
    }



    public int getTotalNumberOfCoveredThrowStatementCustomExceptions() {
        if (totalNumberOfCoveredThrowStatementCustomExceptions != null) {
            return totalNumberOfCoveredThrowStatementCustomExceptions;
        }
        return sumAllCoverageMapValues(throwCustomExceptionsCoverageCounter);
    }

    public int getTotalNumberOfCoveredThrowStatementsStandardOrThirdPartyExceptions() {
        if (totalNumberOfCoveredThrowStatementsStandardOrThirdPartyExceptions != null) {
            return totalNumberOfCoveredThrowStatementsStandardOrThirdPartyExceptions;
        }
        return sumAllCoverageMapValues(throwStandardOrThirdPartyExceptionsCoverageCounter);
    }

    public int getTotalNumberOfCoveredThrowStatementsNotIdentifiedExceptions() {
        if (totalNumberOfCoveredThrowStatementNotIdentifiedExceptions != null) {
            return totalNumberOfCoveredThrowStatementNotIdentifiedExceptions;
        }
        return sumAllCoverageMapValues(throwNotIdentifiedExceptionsCoverageCounter);
    }

    public int getTotalNumberOfCoveredThrowStatements() {
        if (totalNumberOfCoveredThrowStatements != null) {
            return totalNumberOfCoveredThrowStatements;
        }
        return getTotalNumberOfCoveredThrowStatementCustomExceptions() +
                getTotalNumberOfCoveredThrowStatementsStandardOrThirdPartyExceptions() +
                getTotalNumberOfCoveredThrowStatementsNotIdentifiedExceptions();
    }

    public int getTotalNumberOfThrowsStatementCustomExceptions() {
        if (totalNumberOfThrowsStatementCustomExceptions != null) {
            return totalNumberOfThrowsStatementCustomExceptions;
        }
        return sumAllMapValues(calculateTotalOfThrowsCustomExceptions());
    }

    public int getTotalNumberOfThrowsStatementNotIdentifiedExceptions() {
        if (totalNumberOfThrowsStatementNotIdentifiedExceptions != null) {
            return totalNumberOfThrowsStatementNotIdentifiedExceptions;
        }
        return sumAllMapValues(calculateTotalOfThrowsNotIdentifiedExceptions());
    }

    public int getTotalNumberOfThrowsStatementsStandardOrThirdPartyExceptions() {
        if (totalNumberOfThrowsStatementsStandardOrThirdPartyExceptions != null) {
            return totalNumberOfThrowsStatementsStandardOrThirdPartyExceptions;
        }
        return sumAllMapValues(calculateTotalOfThrowsStandardOrThirdPartyExceptions());
    }

    public int getTotalNumberOfThrowsStatements() {
        if (totalNumberOfThrowsStatements != null) {
            return totalNumberOfThrowsStatements;
        }
        return getTotalNumberOfThrowsStatementCustomExceptions() +
                getTotalNumberOfThrowsStatementsStandardOrThirdPartyExceptions() +
                getTotalNumberOfThrowsStatementNotIdentifiedExceptions();
    }

    public int getTotalNumberOfCatchStatementCustomExceptions() {
        if (totalNumberOfCatchStatementCustomExceptions != null) {
            return totalNumberOfCatchStatementCustomExceptions;
        }
        return sumAllMapValues(calculateTotalOfCatchStatementsCustomExceptions());
    }

    public int getTotalNumberOfCatchStatementsStandardOrThirdPartyExceptions() {
        if (totalNumberOfCatchStatementsStandardOrThirdPartyExceptions != null) {
            return totalNumberOfCatchStatementsStandardOrThirdPartyExceptions;
        }
        return sumAllMapValues(calculateTotalOfCatchStandardOrThirdPartyExceptions());
    }

    public int getTotalNumberOfCatchStatementsNotIdentifiedExceptions() {
        if (totalNumberOfCatchStatementNotIdentifiedExceptions != null) {
            return totalNumberOfCatchStatementNotIdentifiedExceptions;
        }
        return sumAllMapValues(calculateTotalOfCatchStatementsNotIdentifiedExceptions());
    }

    public int getTotalNumberOfCatchStatements() {
        if (totalNumberOfCatchStatements != null) {
            return totalNumberOfCatchStatements;
        }
        return getTotalNumberOfCatchStatementCustomExceptions() +
                getTotalNumberOfCatchStatementsStandardOrThirdPartyExceptions() +
                getTotalNumberOfCatchStatementsNotIdentifiedExceptions();
    }


    public int getTotalNumberOfTestsByAnnotation() {
        if (this.totalNumberOfTestsByAnnotation != null) {
            return totalNumberOfTestsByAnnotation;
        }
        return this.models.getOrdinaryAnnotationTestModels().size();
    }

    public int getTotalNumberOfTestsByInheritance() {
        if (this.totalNumberOfTestsByInheritance != null) {
            return totalNumberOfTestsByInheritance;
        }
        return this.models.getOrdinaryExtendedTestModels().size();
    }

    public int getTotalNumberOfTestsWithJUnitImports() {
        if (!isFrameworksCounted) {
            setNumberOfImportsByFrameworks();
        }
        return totalNumberOfTestsWithJUnitImports;
    }

    public int getTotalNumberOfTestsWithTestNGImports() {
        if (!isFrameworksCounted) {
            setNumberOfImportsByFrameworks();
        }
        return totalNumberOfTestsWithTestNGImports;
    }

    public int getTotalNumberOfTestsWithNotIdentifiedImports() {
        if (!isFrameworksCounted) {
            setNumberOfImportsByFrameworks();
        }
        return totalNumberOfTestsWithNotIdentifiedImports;
    }

    private void setNumberOfImportsByFrameworks(){
        if(isFrameworksCounted){
            return;
        }
        Map<String, Integer> mapOfTestsByFramework = new HashMap<String, Integer>();
        mapOfTestsByFramework.put("JUnit", 0);
        mapOfTestsByFramework.put("testNg", 0);
        mapOfTestsByFramework.put("assertJ", 0);
        mapOfTestsByFramework.put("others", 0);

        for(OrdinaryExtendedTestModel model : this.models.getOrdinaryExtendedTestModels()){
            countImportsByFramework(model, mapOfTestsByFramework);
            setOfTestFiles.add(model.getFullClassPackagePath());
        }
        for(OrdinaryAnnotationTestModel model : this.models.getOrdinaryAnnotationTestModels()){
            countImportsByFramework(model, mapOfTestsByFramework);
            setOfTestFiles.add(model.getFullClassPackagePath());
        }


        this.totalNumberOfTestsWithJUnitImports = mapOfTestsByFramework.get("JUnit");
        this.totalNumberOfTestsWithAssertJImports = mapOfTestsByFramework.get("assertJ");
        this.totalNumberOfTestsWithTestNGImports = mapOfTestsByFramework.get("testNg");
        this.totalNumberOfTestsWithNotIdentifiedImports = mapOfTestsByFramework.get("others");
        this.isFrameworksCounted = true;

    }

    private void countImportsByFramework(AbstractOrdinaryModel model, Map<String, Integer> mapOfTestsByFramework) {
        int frameworksCounter = 0;
        if(model.isInsideAJUnitTest()) {
            mapOfTestsByFramework.put("JUnit", mapOfTestsByFramework.get("JUnit") + 1);
            frameworksCounter++;
        }
        if (model.isInsideATestNGTest()) {
            mapOfTestsByFramework.put("testNg", mapOfTestsByFramework.get("testNg") + 1);
            frameworksCounter++;
        }
        if (model.isInsideAAssertJTest()) {
            mapOfTestsByFramework.put("assertJ", mapOfTestsByFramework.get("assertJ") + 1);
            frameworksCounter++;
        }
        if (frameworksCounter == 0){
            mapOfTestsByFramework.put("others", mapOfTestsByFramework.get("others") + 1);
        }
    }


    public void calculateStatistics() {
        this.totalNumberOfTestsByAnnotation = this.getTotalNumberOfTestsByAnnotation();
        this.totalNumberOfTestsByInheritance = this.getTotalNumberOfTestsByInheritance();
        this.totalNumberOfTestMethods = this.getTotalNumberOfTestMethods();
        this.totalNumberOfCreatedCustomExceptions = this.getTotalNumberOfCreatedCustomExceptions();
        /*** Hybrid ***/
        this.commom_totalNumberOfFailInsideCatchScope = this.getCommom_totalNumberOfFailInsideCatchScope();
        this.commom_totalNumberOfFailInsideTryScope = this.getCommom_totalNumberOfFailInsideTryScope();
        this.commom_totalNumberOfFailOutsideTryCatchScope = this.getCommom_totalNumberOfFailOutsideTryCatchScope();
        this.commom_totalNumberOfFailCalls = this.getCommom_totalNumberOfFailCalls();
        /*** JUnit ***/
        this.junit_totalNumberOfExpectedAttribute = this.getJunit_totalNumberOfExpectedAttribute();
        this.junit_totalNumberOfExpectCalls = this.getJunit_totalNumberOfExpectCalls();
        this.junit_totalNumberOfAssertThrows = this.getJunit_totalNumberOfAssertThrows();
        /*** AssertJ ***/
        this.assertj_totalNumberOfAsserts = this.getAssertj_totalNumberOfAsserts();
        this.assertj_totalNumberOfAssertThatThrownBy = this.getAssertj_totalNumberOfAssertThatThrownBy();
        this.assertj_totalNumberOfAssertThatExceptionOfType = this.getAssertj_totalNumberOfAssertThatExceptionOfType();
        this.assertj_totalNumberOfAssertThat = this.getAssertj_totalNumberOfAssertThat();
        this.assertj_totalNumberOfAssertThatExceptionName = this.getAssertj_totalNumberOfAssertThatExceptionName();
        /*** TestNG ***/
        this.testNG_totalNumberOfExpectedExceptionsAttribute = this.getTestNG_totalNumberOfExpectedExceptionsAttribute();

        /*** SUT ***/
        this.totalNumberOfThrowsStatementsStandardOrThirdPartyExceptions = this.getTotalNumberOfThrowsStatementsStandardOrThirdPartyExceptions();
        this.totalNumberOfThrowsStatementCustomExceptions = this.getTotalNumberOfThrowsStatementCustomExceptions();
        this.totalNumberOfThrowsStatementNotIdentifiedExceptions = this.getTotalNumberOfThrowsStatementNotIdentifiedExceptions();
        this.totalNumberOfThrowsStatements = this.getTotalNumberOfThrowsStatements();
        this.totalNumberOfThrowStatementsStandardOrThirdPartyExceptions = this.getTotalNumberOfThrowStatementsStandardOrThirdPartyExceptions();
        this.totalNumberOfThrowStatementCustomExceptions = this.getTotalNumberOfThrowStatementCustomExceptions();
        this.totalNumberOfThrowStatementNotIdentifiedExceptions = this.getTotalNumberOfThrowStatementsNotIdentifiedExceptions();
        this.totalNumberOfThrowStatements = this.getTotalNumberOfThrowStatements();
        this.totalNumberOfCatchStatementsStandardOrThirdPartyExceptions = this.getTotalNumberOfCatchStatementsStandardOrThirdPartyExceptions();
        this.totalNumberOfCatchStatementCustomExceptions = this.getTotalNumberOfCatchStatementCustomExceptions();
        this.totalNumberOfCatchStatementNotIdentifiedExceptions = this.getTotalNumberOfCatchStatementsNotIdentifiedExceptions();
        this.totalNumberOfCatchStatements = this.getTotalNumberOfCatchStatements();
        this.totalNumberOfDistinctUsedCustomExceptions = this.getTotalNumberOfDistinctUsedCustomExceptions();
        this.totalNumberOfDistinctUsedNotIdentifiedExceptions = this.getTotalNumberOfDistinctUsedNotIdentifiedExceptions();
        this.totalNumberOfDistinctUsedStandardOrThirdPartyExceptions = this.getTotalNumberOfDistinctUsedStandardOrThirdPartyExceptions();
        this.totalNumberOfDistinctUsedExceptions = this.getTotalNumberOfDistinctUsedExceptions();
        //uses
        this.totalNumberOfCustomExceptionsUses = this.getTotalNumberOfCustomExceptionsUses();
        this.totalNumberOfStandardOrThirdPartyExceptionsUses = this.getTotalNumberOfStandardOrThirdPartyExceptionsUses();
        this.totalNumberOfNotIdentifiedExceptionsUses = this.getTotalNumberOfNotIdentifiedExceptionsUses();
        this.totalNumberOfExceptionsUses = this.getTotalNumberOfExceptionsUses();
        //coverage
        this.totalNumberOfCoveredThrowStatementsStandardOrThirdPartyExceptions = this.getTotalNumberOfCoveredThrowStatementsStandardOrThirdPartyExceptions();
        this.totalNumberOfCoveredThrowStatementCustomExceptions = this.getTotalNumberOfCoveredThrowStatementCustomExceptions();
        this.totalNumberOfCoveredThrowStatementNotIdentifiedExceptions = this.getTotalNumberOfCoveredThrowStatementsNotIdentifiedExceptions();
        this.totalNumberOfCoveredThrowStatements = this.getTotalNumberOfCoveredThrowStatements();


        //One method may test multiple exceptions. If it happens, the method will be counted multiple times.
        calculateTestedExceptionsCounter();
        //used and tested
        this.totalNumberOfDistinctTestedStandardOrThirdPartyExceptions = this.getTotalNumberOfDistinctTestedStandardOrThirdPartyExceptions();
        this.totalNumberOfDistinctTestedCustomExceptions = this.getTotalNumberOfDistinctTestedCustomExceptions();
        this.totalNumberOfDistinctTestedExceptions = this.getTotalNumberOfDistinctTestedExceptions();

        //Coverage
        this.totalNumberOfDistinctCoveredStandardOrThirdPartyExceptions = this.getTotalNumberOfDistinctCoveredStandardOrThirdPartyExceptions();
        this.totalNumberOfDistinctCoveredCustomExceptions = this.getTotalNumberOfDistinctCoveredCustomExceptions();
        this.totalNumberOfDistinctCoveredExceptions = this.getTotalNumberOfDistinctCoveredExceptions();

        this.totalNumberOfCustomExceptionsTestMethods = this.getTotalNumberOfCustomExceptionsTestMethods();
        this.totalNumberOfStandardOrThirdPartyExceptionsTestMethods = this.getTotalNumberOfStandardOrThirdPartyExceptionsTestMethods();
        this.totalNumberOfNotIdentifiedExceptionsTestMethods = this.getTotalNumberOfNotIdentifiedExceptionsTestMethods();
        this.totalNumberOfExceptionTests = this.getTotalNumberOfExceptionTests();
        this.totalNumberOfExceptionalBehaviorTestMethods = this.getTotalNumberOfExceptionalBehaviorTestMethods();

        this.totalNumberOfAllTestedStandardOrThirdPartyExceptions = this.getTotalNumberOfAllTestedStandardOrThirdPartyExceptions();
        this.totalNumberOfAllTestedNotIdentifiedExceptions = this.getTotalNumberOfAllTestedNotIdentifiedExceptions();
        this.totalNumberOfAllTestedCustomExceptions = this.getTotalNumberOfAllTestedCustomExceptions();
        this.totalNumberOfAllTestedExceptions = this.totalNumberOfAllTestedStandardOrThirdPartyExceptions  + this.totalNumberOfAllTestedCustomExceptions;

        //Count how many times each framework is imported
        setNumberOfImportsByFrameworks();


    }


    private double formatDecimalOutput(double value) {
        BigDecimal bd = new BigDecimal(value);
        bd = bd.setScale(2, RoundingMode.HALF_UP);
        return bd.doubleValue();
    }


    public int getTotalNumberOfExceptionTests() {
        return this.getTotalNumberOfStandardOrThirdPartyExceptionsTestMethods() +
                this.getTotalNumberOfCustomExceptionsTestMethods() +
                this.getTotalNumberOfNotIdentifiedExceptionsTestMethods();

    }

    public int getTotalNumberOfExceptionalBehaviorTestMethods() {
        mergeMap(getStandardOrThirdPartyExceptionsTestMethodCounter(), distinctExceptionsTestMethodCounter);
        mergeMap(getCustomExceptionsTestMethodCounter(), distinctExceptionsTestMethodCounter);
        mergeMap(getNotIdentifiedExceptionsTestMethodCounter(), distinctExceptionsTestMethodCounter);
        return distinctExceptionsTestMethodCounter.size();

    }

    public int getTotalNumberOfDistinctUsedExceptions() {
        return this.getTotalNumberOfDistinctUsedCustomExceptions() +
                this.getTotalNumberOfDistinctUsedStandardOrThirdPartyExceptions();
    }

    public void mergeMap(Map<String, Integer> fromMap, Map<String, Integer> toMap) {
        for (Map.Entry<String, Integer> entry : fromMap.entrySet()) {
            if (toMap.containsKey(entry.getKey())) {
                toMap.put(entry.getKey(), entry.getValue() + toMap.get(entry.getKey()));
            } else {

                toMap.put(entry.getKey(), entry.getValue());
            }
        }
    }


    public Map<String, Integer> getTestedStandardOrThirdPartyExceptionsCounter() {
        return testedStandardOrThirdPartyExceptionsCounter;
    }

    public Map<String, Integer> getTestedCustomExceptionsCounter() {
        return testedCustomExceptionsCounter;
    }

    public Map<String, Integer> getThrowsStandardOrThirdPartyExceptionsCounter() {
        return throwsStandardOrThirdPartyExceptionsCounter;
    }

    public Map<String, Integer> getThrowsCustomExceptionsCounter() {
        return throwsCustomExceptionsCounter;
    }

    public Map<String, Integer> getThrowStandardOrThirdPartyExceptionsExceptionsCounter() {
        return throwStandardOrThirdPartyExceptionsExceptionsCounter;
    }

    public Map<String, Integer> getThrowCustomExceptionsCounter() {
        return throwCustomExceptionsCounter;
    }

    public List<String> getCustomCreatedExceptions() {
        return customCreatedExceptions;
    }

    public Map<String, Integer> getCatchStandardOrThirdPartyExceptionsCounter() {
        return catchStandardOrThirdPartyExceptionsCounter;
    }

    public Map<String, Integer> getCatchCustomExceptionsCounter() {
        return catchCustomExceptionsCounter;
    }

    public Map<String, Integer> getStandardOrThirdPartyExceptionsUsed() {
        return standardOrThirdPartyExceptionsUsed;
    }

    public Map<String, Integer> getCustomExceptionsUsed() {
        return customExceptionsUsed;
    }

    public Map<String, Integer> getThrowNotIdentifiedExceptionsCounter() {
        return throwNotIdentifiedExceptionsCounter;
    }

    public Map<String, Integer> getTestedNotIdentifiedExceptionsCounter() {
        return testedNotIdentifiedExceptionsCounter;
    }

    public Map<String, Integer> getCustomExceptionsTestMethodCounter() {
        return customExceptionsTestMethodCounter;
    }

    public Map<String, Integer> getStandardOrThirdPartyExceptionsTestMethodCounter() {
        return standardOrThirdPartyExceptionsTestMethodCounter;
    }

    public Map<String, Integer> getNotIdentifiedExceptionsTestMethodCounter() {
        return notIdentifiedExceptionsTestMethodCounter;
    }

    public int getTotalNumberOfThrowStatementNotIdentifiedExceptions() {
        return totalNumberOfThrowStatementNotIdentifiedExceptions;
    }

    public int getTotalNumberOfCatchStatementNotIdentifiedExceptions() {
        return totalNumberOfCatchStatementNotIdentifiedExceptions;
    }

    public Map<String, Integer> getThrowsNotIdentifiedExceptionsCounter() {
        return throwsNotIdentifiedExceptionsCounter;
    }

    public Map<String, Integer> getCatchNotIdentifiedExceptionsCounter() {
        return catchNotIdentifiedExceptionsCounter;
    }

    public Map<String, Integer> getNotIdentifiedExceptionsUsed() {
        return notIdentifiedExceptionsUsed;
    }


}
