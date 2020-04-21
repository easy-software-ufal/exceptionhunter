from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
from matplotlib.ticker import (MultipleLocator)
from pymongo import MongoClient

from main import Util

SHOW_FIGURE = False

df_T = ""

RQ_NUMBER = "threats"
OUTPUT_PATH = "RQS/" + RQ_NUMBER
OUTPUT_FIGURES_PATH = Util.create_new_dirs(OUTPUT_PATH + "/figures/")

fileName = "res_"+RQ_NUMBER+".txt"
f = open(Path(OUTPUT_PATH) / fileName, "w+")

############################## TABLE GENERATION ##############################
def generateDataSetThreats():
    global df_T

    numberOfProjectsWithoutExceptionsUse = 0
    numberOfProjectsWithoutJUnitTests = 0
    numberOfProjectsWithLesssJUnitTestsThanOther = 0
    dataSet = []

    for doc in Util.mongo_collection.find():
        # if doc["statistics"]['totalNumberOfJUnitTests'] == 0:
        #     numberOfProjectsWithoutJUnitTests += 1
        #     continue
        #
        # if doc["statistics"]['totalNumberOfJUnitTests'] < doc["statistics"]['totalNumberOfTestNGTests'] or \
        #         doc["statistics"]['totalNumberOfJUnitTests'] < doc["statistics"]['totalNumberOfNotIdentifiedTests']:
        #     numberOfProjectsWithLesssJUnitTestsThanOther += 1
        #     continue
        #
        # if doc["statistics"]['totalNumberOfCustomExceptionsUses'] == 0 and doc["statistics"][
        #     'totalNumberOfStandardOrThirdPartyExceptionsUses'] == 0:
        #     numberOfProjectsWithoutExceptionsUse += 1
        #     continue

        project = doc["projectName"]
        platform = doc['projectDetails']["platform"]
        domain = Util.adjust_domain_name(doc['projectDetails']["domain"])
        totalNumberOfJUnitTests = doc["statistics"]['totalNumberOfTestsWithJUnitImports']
        totalNumberOfTestNGTests = doc["statistics"]['totalNumberOfTestsWithTestNGImports']
        totalNumberOfNotIdentifiedTests = doc["statistics"]['totalNumberOfTestsWithNotIdentifiedImports']
        NNIEU = doc["statistics"]['totalNumberOfNotIdentifiedExceptionsUses']
        NEU = doc["statistics"]['totalNumberOfExceptionsUses']
        NNIEU_NEU = round(NNIEU/NEU, 4)
        NNIETM = doc["statistics"]['totalNumberOfNotIdentifiedExceptionsTestMethods']
        NEBTM = doc["statistics"]['totalNumberOfExceptionalBehaviorTestMethods']
        if NEBTM > 0:
            NNIETM_NEBTM = round(NNIETM / NEBTM, 4)
        else:
            NNIETM_NEBTM = float("NaN")
        dataSetRQ3 = [project, platform, domain, totalNumberOfJUnitTests, totalNumberOfTestNGTests, totalNumberOfNotIdentifiedTests,  NNIEU, NEU, NNIEU_NEU, NNIETM, NEBTM, NNIETM_NEBTM]
        dataSet.append(dataSetRQ3)

    df_T = pd.DataFrame(dataSet, columns=['project', 'platform', 'domain','totalNumberOfJUnitTests','totalNumberOfTestNGTests', 'totalNumberOfNotIdentifiedTests',  'NNIEU', 'NEU', 'NNIEU_NEU', 'NNIETM', 'NEBTM', 'NNIETM_NEBTM'])
    output_path = Util.create_new_dirs("RQs/threats/")
    df_T.to_csv(output_path / 'threats.csv', sep=";", index=False, na_rep="NaN")
    #Util.format_to_csv(df_T, "RQs/" + RQ_NUMBER + "/", "table" + RQ_NUMBER, RQ_NUMBER, [])

############################## THREATS - PART 1 ##############################
def violinPlotRatio_NNIEU_NEU():
    labels = ['']
    fig, ax = plt.subplots(figsize=(8,8))
    ax.violinplot(df_T['NNIEU/NEU'].tolist(), showmeans=False, showmedians=False)
    ax.minorticks_on()
    ax.yaxis.grid(True, linewidth=1, which="major")
    ax.yaxis.grid(True, linewidth=0.5, which="minor", linestyle='--')
    ax.yaxis.set_major_locator(MultipleLocator(0.1))
    ax.yaxis.set_minor_locator(MultipleLocator(0.05))
    ax.get_yaxis().set_tick_params(labelsize=25, which="major")
    ax.get_xaxis().set_tick_params(direction='out',labelsize=23)
    ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1, decimals=0))
    ax.xaxis.set_ticks_position('bottom')
    ax.set_xticks(np.arange(1, len(labels) + 1))
    ax.set_xticklabels(labels)
    ax.set_xlim(0.25, len(labels) + 0.75)
    # Show graphic
    plt.tight_layout()
    plt.savefig('threats\\figures\\ratio_NNIEU_NEU_ViolinPlot.eps', bbox_inches="tight")
    plt.savefig('threats\\figures\\ratio_NNIEU_NEU_ViolinPlot.png', bbox_inches="tight")
    if(SHOW_FIGURE):
        plt.show()
    plt.clf()

def boxPlotRatio_NNIEU_NEU():
    labels = ['']
    fig, ax = plt.subplots(figsize=(8,8))
    ax.boxplot(df_T['NNIEU/NEU'].tolist())
    ax.minorticks_on()
    ax.yaxis.grid(True, linewidth=1, which="major")
    ax.yaxis.grid(True, linewidth=0.5, which="minor", linestyle='--')
    ax.yaxis.set_major_locator(MultipleLocator(0.1))
    #ax.yaxis.set_major_formatter(FormatStrFormatter('%d'))
    ax.yaxis.set_minor_locator(MultipleLocator(0.05))
    ax.get_yaxis().set_tick_params(labelsize=25, which="major")
    ax.get_xaxis().set_tick_params(direction='out',labelsize=23)
    ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1, decimals=0))
    ax.xaxis.set_ticks_position('bottom')
    ax.set_xticks(np.arange(1, len(labels) + 1))
    ax.set_xticklabels(labels)
    ax.set_xlim(0.25, len(labels) + 0.75)
    # Show graphic
    plt.tight_layout()
    plt.savefig('threats\\figures\\ratio_NNIEU_NEU_BoxPlot.eps', bbox_inches="tight")
    plt.savefig('threats\\figures\\ratio_NNIEU_NEU_BoxPlot.png', bbox_inches="tight")
    if(SHOW_FIGURE):
        plt.show()
    plt.clf()


############################## THREATS - PART 2 ##############################
def violinPlotRatio_NNIETM_NEBTM():
    labels = ['']
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.violinplot(df_T['NNIETM/NEBTM'].tolist(), showmeans=False, showmedians=False)
    ax.minorticks_on()
    ax.yaxis.grid(True, linewidth=1, which="major")
    ax.yaxis.grid(True, linewidth=0.5, which="minor", linestyle='--')
    ax.yaxis.set_major_locator(MultipleLocator(0.1))
    ax.yaxis.set_minor_locator(MultipleLocator(0.05))
    ax.get_yaxis().set_tick_params(labelsize=25, which="major")
    ax.get_xaxis().set_tick_params(direction='out', labelsize=23)
    ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1, decimals=0))
    ax.xaxis.set_ticks_position('bottom')
    ax.set_xticks(np.arange(1, len(labels) + 1))
    ax.set_xticklabels(labels)
    ax.set_xlim(0.25, len(labels) + 0.75)
    # Show graphic
    plt.tight_layout()
    plt.savefig('threats\\figures\\ratio_NNIETM_NEBTM_ViolinPlot.eps', bbox_inches="tight")
    plt.savefig('threats\\figures\\ratio_NNIETM_NEBTM_ViolinPlot.png', bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()


def boxPlotRatio_NNIETM_NEBTM():
    labels = ['']
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.boxplot(df_T['NNIETM/NEBTM'].tolist())
    ax.minorticks_on()
    ax.yaxis.grid(True, linewidth=1, which="major")
    ax.yaxis.grid(True, linewidth=0.5, which="minor", linestyle='--')
    ax.yaxis.set_major_locator(MultipleLocator(0.1))
    # ax.yaxis.set_major_formatter(FormatStrFormatter('%d'))
    ax.yaxis.set_minor_locator(MultipleLocator(0.05))
    ax.get_yaxis().set_tick_params(labelsize=25, which="major")
    ax.get_xaxis().set_tick_params(direction='out', labelsize=23)
    ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1, decimals=0))
    ax.xaxis.set_ticks_position('bottom')
    ax.set_xticks(np.arange(1, len(labels) + 1))
    ax.set_xticklabels(labels)
    ax.set_xlim(0.25, len(labels) + 0.75)
    # Show graphic
    plt.tight_layout()
    plt.savefig('threats\\figures\\ratio_NIETM_NEBTM_BoxPlot.eps', bbox_inches="tight")
    plt.savefig('threats\\figures\\ratio_NNIETM_NEBTM_BoxPlot.png', bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()


########################################END #####################
def autolabelHorizontal(rects, ay, ypos='center'):
    """
    Attach a text label above each bar in *rects*, displaying its height.

    *xpos* indicates which side to place the text w.r.t. the center of
    the bar. It can be one of the following {'center', 'right', 'left'}.
    """

    ypos = ypos.lower()  # normalize the case of the parameter
    va = {'center': 'center', 'top': 'bottom', 'bottom': 'top'}
    offset = {'center': 0.5, 'top': 0.57, 'bottom': 0.43}  # y_txt = y + w*off

    for rect in rects:
        width = rect.get_width()
        ay.text( 1.01*width, rect.get_y() + rect.get_height()*offset[ypos],
                '{}'.format(width), va=va[ypos], ha='left')



generateDataSetThreats()


def findProjectsUsingOtherTestingFrameworkThanJunit():
    df_usingJunit = df_T[(df_T['totalNumberOfJUnitTests'] > 0)]
    df_usingTestNG = df_T[(df_T['totalNumberOfTestNGTests'] > 0)]
    df_notIdentified = df_T[(df_T['totalNumberOfNotIdentifiedTests'] > 0)]

    print(f'JUnit Total: {len(df_usingJunit)} | TestNG Total: {len(df_usingTestNG)} | Not identified total: {len(df_notIdentified)}')
    print(df_usingTestNG['project'])
    print(df_notIdentified['project'])



def calculateRatios(df, description):
    totalNNIEU = df['NNIEU'].sum()
    totalNEU = df['NEU'].sum()
    ratio_NNIEU_NEU = round((totalNNIEU / totalNEU) * 100, 4)
    print(f'{description}_ratio_NNIEU_NEU: {totalNNIEU} / {totalNEU} = {ratio_NNIEU_NEU}')


    totalNNIETM = df['NNIETM'].sum()
    totalNEBTM = df['NEBTM'].sum()
    ratio_NNIETM_NEBTM = round((totalNNIETM / totalNEBTM) * 100, 4)
    print(f'{description}_ratio_NNIETM_NEBTM: {totalNNIETM} / {totalNEBTM} = {ratio_NNIETM_NEBTM}')


def calculateRatiosOfThreat():
    platformList = df_T["platform"].unique()
    domainList = df_T["domain"].unique()

    calculateRatios(df_T, "Total")
    for platform in platformList:
        df_platform = df_T[(df_T['platform'] == platform)]
        calculateRatios(df_platform, platform)
        for domain in domainList:
            df_domain = df_platform[(df_platform['domain'] == domain)]
            calculateRatios(df_domain, f'{platform}_{domain}')

calculateRatiosOfThreat()

findProjectsUsingOtherTestingFrameworkThanJunit()

#part1
#violinPlotRatio_NNIEU_NEU()
#boxPlotRatio_NNIEU_NEU()

#part2
#violinPlotRatio_NNIETM_NEBTM()
#boxPlotRatio_NNIETM_NEBTM()