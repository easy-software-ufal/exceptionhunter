from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.ticker import (MultipleLocator)
from pymongo import MongoClient

from main import Util

np.warnings.filterwarnings('ignore')
sns.set_context("paper")
sns.set_style("whitegrid")


df_RQ = ""

SHOW_FIGURE = False

RQ_NUMBER = "RQ5"
OUTPUT_PATH = "RQS/" + RQ_NUMBER
OUTPUT_FIGURES_PATH = Util.create_new_dirs(OUTPUT_PATH + "/figures/")

fileName = "res_"+RQ_NUMBER+".txt"
f = open(Path(OUTPUT_PATH) / fileName, "w+")


############################## TABLE GENERATION ##############################

def generateDataSet():
    global df_RQ
    today = datetime.now()
    dataSet = []
    for doc in Util.mongo_collection.find():
        project = doc["projectName"]
        platform = doc['projectDetails']["platform"]
        domain = Util.adjust_domain_name(doc['projectDetails']["domain"])
        projectMonths = Util.calculate_month_delta(datetime.strptime(doc["projectDetails"]["createdAt"], '%d/%m/%Y %H:%M:%S'), today)
        NEBTM = doc["statistics"]['totalNumberOfExceptionalBehaviorTestMethods']

        commom_totalNumberOfFailCalls = doc["statistics"]['commom_totalNumberOfFailCalls']

        junit_totalNumberOfExpectedAttribute = doc["statistics"]['junit_totalNumberOfExpectedAttribute']
        junit_totalNumberOfExpectCalls = doc["statistics"]['junit_totalNumberOfExpectCalls']
        junit_totalNumberOfAssertThrows = doc["statistics"]['junit_totalNumberOfAssertThrows']

        assertj_totalNumberOfAssertThatExceptionName = doc["statistics"]['assertj_totalNumberOfAssertThatExceptionName']
        assertj_totalNumberOfAssertThatExceptionOfType = doc["statistics"]['assertj_totalNumberOfAssertThatExceptionOfType']
        assertj_totalNumberOfAssertThat = doc["statistics"]['assertj_totalNumberOfAssertThat']
        assertj_totalNumberOfAssertThatThrownBy = doc["statistics"]['assertj_totalNumberOfAssertThatThrownBy']

        testNG_totalNumberOfExpectedExceptionsAttribute = doc["statistics"]['testNG_totalNumberOfExpectedExceptionsAttribute']

        #Imports
        junit_imports = doc["statistics"]['totalNumberOfTestsWithJUnitImports']
        assertj_imports = doc["statistics"]['totalNumberOfTestsWithAssertJImports']
        testng_imports = doc["statistics"]['totalNumberOfTestsWithTestNGImports']

        dataSetRQ5 = [project, platform, domain, projectMonths, NEBTM, commom_totalNumberOfFailCalls, junit_totalNumberOfExpectedAttribute, junit_totalNumberOfExpectCalls, junit_totalNumberOfAssertThrows,
                      assertj_totalNumberOfAssertThatExceptionName, assertj_totalNumberOfAssertThatExceptionOfType, assertj_totalNumberOfAssertThat, assertj_totalNumberOfAssertThatThrownBy,
                      testNG_totalNumberOfExpectedExceptionsAttribute, junit_imports, assertj_imports, testng_imports]
        dataSet.append(dataSetRQ5)

    df_RQ = pd.DataFrame(dataSet, columns=['project', 'platform', 'domain', 'projectMonths','NEBTM', 'commom_totalNumberOfFailCalls', 'junit_totalNumberOfExpectedAttribute',
                                           'junit_totalNumberOfExpectCalls', 'junit_totalNumberOfAssertThrows','assertj_totalNumberOfAssertThatExceptionName','assertj_totalNumberOfAssertThatExceptionOfType',
                                           'assertj_totalNumberOfAssertThat', 'assertj_totalNumberOfAssertThatThrownBy', 'testNG_totalNumberOfExpectedExceptionsAttribute', 'junit_imports', 'assertj_imports', 'testng_imports'])
    output_path = Util.create_new_dirs("RQs/RQ5/")
    df_RQ.to_csv(output_path / 'RQ5_exception_testing_constructs.csv', sep=";", index=False, na_rep="NaN")
    #Util.format_to_csv(df_RQ, "RQs/" + RQ_NUMBER + "/", "table" + RQ_NUMBER, RQ_NUMBER, [])

def calculateFrameworkUsage(df_aux, frameworkName):
    dfAuxSize = len(df_aux)
    dfRQSize = len(df_RQ)
    ratio = round(dfAuxSize/dfRQSize, 4)
    f.write(f'Number of projects using {frameworkName}: {dfAuxSize} out of {dfRQSize} ({ratio}%)\n')

def calculateNumberOfProjectsByFramework():
    total = len(df_RQ)
    dataSet = []
    df_junit = df_RQ[(df_RQ['junit_imports'] > 0)]
    calculateFrameworkUsage(df_junit, 'JUnit')
    dataSet.append(["JUnit", len(df_junit)])
    df_assertj = df_RQ[(df_RQ['assertj_imports'] > 0)]
    dataSet.append(["AssertJ", len(df_assertj)])
    calculateFrameworkUsage(df_assertj, 'AssertJ')
    df_testng = df_RQ[(df_RQ['testng_imports'] > 0)]
    calculateFrameworkUsage(df_testng, 'TestNG')
    dataSet.append(["TestNG", len(df_testng)])
    df_aux = pd.DataFrame(dataSet, columns=['Framework/Library', 'Total'])

    f, ax = plt.subplots(figsize=(3, 2))
    sns.barplot(data=df_aux,
                x='Total', y='Framework/Library', color='#494848', label='')

    # ax.legend(title="", loc="upper center", bbox_to_anchor=(0.5, 1.03), ncol=2, frameon=False)
    ax.get_xaxis().set_tick_params(direction='out', labelsize=Util.SIZE_AXES_VALUES, gridOn=False)
    ax.xaxis.set_ticks_position('bottom')
    ax.set_xlabel('', fontsize=Util.SIZE_AXES_LABELS)
    ax.set_ylabel('', fontsize=Util.SIZE_AXES_LABELS)
    # ax.set_ylabel('General Coverage', fontsize=Util.SIZE_AXES_LABELS)
    ax.xaxis.set_major_formatter(ticker.EngFormatter())
    # sns.despine(left=True, bottom=True)
    ax.xaxis.set_ticks_position('bottom')
    for p in ax.patches:
        width = p.get_width()
        ratio = str("{:.2%}").format(width/total)
        if width > 350:
            pos_x = width - 165
            color = "white"
            fontweight = "semibold"
        else:
            pos_x = width + 0.1
            color = "black"
            fontweight = "normal"
        legend = f'{int(width)} ({ratio})'
        ax.text(pos_x, p.get_y() + p.get_height() / 2., legend, color=color, fontweight=fontweight, va="center", fontsize=Util.SIZE_BAR_VALUES)

    fileName = f'RQ5_barPlotTotalOfFrameworkUsage .pdf'
    # plt.savefig(OUTPUT_FIGURES_PATH / fileName + '.pdf',
    #             bbox_inches="tight")
    plt.savefig(OUTPUT_FIGURES_PATH / fileName,
                bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()




def barPlotDataFrame(df_aux, platformName):
    total = df_aux['Total'].sum()
    f, ax = plt.subplots(figsize=(5, 3))
    sns.barplot(data=df_aux.sort_values("Total", ascending=False),
                      x='Total', y='Exception-Testing Construct', color='#494848', label='')

    #ax.legend(title="", loc="upper center", bbox_to_anchor=(0.5, 1.03), ncol=2, frameon=False)
    ax.get_xaxis().set_tick_params(direction='out', labelsize=Util.SIZE_AXES_VALUES, gridOn=False)
    ax.xaxis.set_ticks_position('bottom')
    ax.set_xlabel('', fontsize=Util.SIZE_AXES_LABELS)
    ax.set_ylabel('', fontsize=Util.SIZE_AXES_LABELS)
    #ax.set_ylabel('General Coverage', fontsize=Util.SIZE_AXES_LABELS)
    ax.xaxis.set_major_formatter(ticker.EngFormatter())
    #sns.despine(left=True, bottom=True)
    for p in ax.patches:
        width = p.get_width()
        ratio = str("{:.2%}").format(width / total)
        # if width > 33000:
        #     pos_x = width - 9000
        #     color = "white"
        #     fontweight = "semibold"
        if width > 3600:
            pos_x = width - 900
            color = "white"
            fontweight = "semibold"
        else:
            pos_x = width + 0.1
            color = "black"
            fontweight = "normal"
        legend = f'{int(width)} ({ratio})'
        ax.text(pos_x, p.get_y() + p.get_height() / 2., legend, color=color, fontweight=fontweight, va="center",
                fontsize=Util.SIZE_BAR_VALUES)

    fileName = f'RQ5_barPlotTotalOfExceptionTestingConstructs_{platformName.replace("/", "_")}.pdf'
    # plt.savefig(OUTPUT_FIGURES_PATH / fileName + '.pdf',
    #             bbox_inches="tight")
    plt.savefig(OUTPUT_FIGURES_PATH / fileName,
                bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()

def calculateTotalOfUseExceptionTestingConstructs(df_aux):
    print(f'Tamanho do DF :{len(df_aux)}')
    dataSet = []

    total_commom_totalNumberOfFailCalls = df_aux['commom_totalNumberOfFailCalls'].sum()
    dataSet.append(['(JUnit/TestNG/AssertJ) fail', total_commom_totalNumberOfFailCalls])

    total_junit_totalNumberOfExpectedAttribute = df_aux['junit_totalNumberOfExpectedAttribute'].sum()
    dataSet.append(['(JUnit) expected Attribute', total_junit_totalNumberOfExpectedAttribute])
    total_junit_totalNumberOfExpectCalls = df_aux['junit_totalNumberOfExpectCalls'].sum()
    dataSet.append(['(JUnit) expect', total_junit_totalNumberOfExpectCalls])
    total_junit_totalNumberOfAssertThrows = df_aux['junit_totalNumberOfAssertThrows'].sum()
    dataSet.append(['(JUnit) assertThrows', total_junit_totalNumberOfAssertThrows])

    total_assertj_totalNumberOfAssertThatExceptionName = df_aux['assertj_totalNumberOfAssertThatExceptionName'].sum()
    dataSet.append(['(AssertJ) assertThatExceptionName', total_assertj_totalNumberOfAssertThatExceptionName])
    total_assertj_totalNumberOfAssertThatExceptionOfType = df_aux['assertj_totalNumberOfAssertThatExceptionOfType'].sum()
    dataSet.append(['(AssertJ) assertThatExceptionOfType', total_assertj_totalNumberOfAssertThatExceptionOfType])
    total_assertj_totalNumberOfAssertThat = df_aux['assertj_totalNumberOfAssertThat'].sum()
    dataSet.append(['(AssertJ) assertThat', total_assertj_totalNumberOfAssertThat])
    total_assertj_totalNumberOfAssertThatThrownBy = df_aux['assertj_totalNumberOfAssertThatThrownBy'].sum()
    dataSet.append(['(AssertJ) assertThatThrownBy', total_assertj_totalNumberOfAssertThatThrownBy])

    total_testNG_totalNumberOfExpectedExceptionsAttribute = df_aux['testNG_totalNumberOfExpectedExceptionsAttribute'].sum()
    dataSet.append(['(TestNG) expectedExceptions Attribute', total_testNG_totalNumberOfExpectedExceptionsAttribute])

    df_counterTable = pd.DataFrame(dataSet, columns=['Exception-Testing Construct', 'Total'])

    return df_counterTable


def calculateTotalOfUses():
    platformList = df_RQ["platform"].unique()

    df_counterTable = calculateTotalOfUseExceptionTestingConstructs(df_RQ)
    barPlotDataFrame(df_counterTable, "All")

    df_counterTable = calculateTotalOfUseExceptionTestingConstructs(df_RQ[(df_RQ['projectMonths'] <= 36)])
    barPlotDataFrame(df_counterTable, "3Years")

    for platform in platformList:
        df_platform = df_RQ[(df_RQ['platform'] == platform)]
        df_counterTable = calculateTotalOfUseExceptionTestingConstructs(df_platform)
        barPlotDataFrame(df_counterTable, platform)



# Generating Table V
generateDataSet()

calculateTotalOfUses()

calculateNumberOfProjectsByFramework()




