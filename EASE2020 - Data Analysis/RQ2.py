import os
import math
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from matplotlib import gridspec
import pandas as pd
import seaborn as sns
from matplotlib.ticker import (MultipleLocator)
from pymongo import MongoClient

from main import Util
from main import StatisticalTests

np.warnings.filterwarnings('ignore')

sns.set_context("paper")
sns.set_style("whitegrid")
# sns.despine()

SHOW_FIGURE = False

df_RQ = ""


columnsToLatex = ['NDUCE', 'NDUSTE', 'NDUE', 'NDUCE/NDUE', 'NDUSTE/NDUE',
           'NDTCE', 'NDTSTE', 'NDTE', 'NDTCE/NDTE', 'NDTSTE/NDTE', 'NDTCE/NDUCE', 'NDTSTE/NDUSTE']
# 'NDTUCE', 'NDTUSTE', 'NDTUE', 'NDTUCE_NDTE', 'NDTUSTE_NDTE', 'NDTUCE_NDUCE', 'NDTUSTE_NDUSTE']

RQ_NUMBER = "RQ2"
OUTPUT_PATH = "RQS/" + RQ_NUMBER
OUTPUT_FIGURES_PATH = Util.create_new_dirs(OUTPUT_PATH + "/figures/")

fileName = "res_"+RQ_NUMBER+".txt"
f = open(Path(OUTPUT_PATH) / fileName, "w+")

############################## TABLE GENERATION ##############################
def generateDataSet():
    global df_RQ
    dataSet = []
    for doc in Util.mongo_collection.find():

        project = doc["projectName"]
        tagCreatedOn = datetime.strptime(doc["tagCreatedAt"], '%d/%m/%Y %H:%M:%S').year
        projectCreatedOn = datetime.strptime(doc["projectDetails"]["createdAt"], '%d/%m/%Y %H:%M:%S').year
        platform = doc['projectDetails']["platform"]
        domain = Util.adjust_domain_name(doc['projectDetails']["domain"])
        stars = doc['projectDetails']["stars"]
        contributors = doc['projectDetails']["contributors"]
        NEBTM = doc["statistics"]['totalNumberOfExceptionalBehaviorTestMethods']
        NDUCE = doc["statistics"]['totalNumberOfDistinctUsedCustomExceptions']
        NDUSTE = doc["statistics"]['totalNumberOfDistinctUsedStandardOrThirdPartyExceptions']
        NDUE = doc["statistics"]['totalNumberOfDistinctUsedExceptions']
        NDUCE_NDUE = round(np.float64(NDUCE) / NDUE, 4)
        NDUSTE_NDUE = round(np.float64(NDUSTE) / NDUE, 4)

        # Only used exceptions
        NDTCE = doc["statistics"]['totalNumberOfDistinctTestedCustomExceptions']
        NDTSTE = doc["statistics"]['totalNumberOfDistinctTestedStandardOrThirdPartyExceptions']
        NDTE = doc["statistics"]['totalNumberOfDistinctTestedExceptions']
        NDTCE_NDTE = round(np.float64(NDTCE) / NDTE, 4)
        NDTSTE_NDTE = round(np.float64(NDTSTE) / NDTE, 4)
        NDTCE_NDUCE = round(np.float64(NDTCE) / NDUCE, 4)
        # this workaround is necessary to have the same number of subjects in both ratios
        if np.isnan(NDTCE_NDUCE):
            NDTSTE_NDUSTE = float("NaN")
        else:
            NDTSTE_NDUSTE = round(np.float64(NDTSTE) / NDUSTE, 4)
        NDTSTE_NDUSTE_REAL = round(np.float64(NDTSTE) / NDUSTE, 4)
        # # All exceptions
        # NDTUCE = doc["statistics"]['totalNumberOfDistinctTestedAndUsedCustomExceptions']
        # NDTUSTE = doc["statistics"]['totalNumberOfDistinctTestedAndUsedStandardOrThirdPartyExceptions']
        # NDTUE = doc["statistics"]['totalNumberOfDistinctTestedAndUsedExceptions']
        # NDTUCE_NDTE = round(np.float64(NDTUCE) / NDTE, 4)
        # NDTUSTE_NDTE = round(np.float64(NDTUSTE) / NDTE, 4)
        # NDTUCE_NDUCE = round(np.float64(NDTUCE) / NDUCE, 4)
        # NDTUSTE_NDUSTE = round(np.float64(NDTUSTE) / NDUSTE, 4)

        dataSetRQ2 = [project, tagCreatedOn, projectCreatedOn, platform, domain, stars,
                      contributors,NEBTM, NDUCE, NDUSTE, NDUE, NDUCE_NDUE, NDUSTE_NDUE,
                      NDTCE, NDTSTE, NDTE, NDTCE_NDTE, NDTSTE_NDTE, NDTCE_NDUCE, NDTSTE_NDUSTE, NDTSTE_NDUSTE_REAL]
        # ,NDTUCE, NDTUSTE, NDTUE, NDTUCE_NDTE, NDTUSTE_NDTE, NDTUCE_NDUCE, NDTUSTE_NDUSTE]
        dataSet.append(dataSetRQ2)

    df_RQ = pd.DataFrame(dataSet,
                         columns=['project', 'tagCreatedOn', 'projectCreatedOn', 'platform', 'domain', 'stars',
                                  'contributors','NEBTM', 'NDUCE', 'NDUSTE', 'NDUE', 'NDUCE/NDUE', 'NDUSTE/NDUE',
                                  'NDTCE', 'NDTSTE', 'NDTE', 'NDTCE/NDTE', 'NDTSTE/NDTE', 'NDTCE/NDUCE',
                                  'NDTSTE/NDUSTE', 'NDTSTE_NDUSTE_REAL'])
    # ,'NDTUCE', 'NDTUSTE', 'NDTUE', 'NDTUCE_NDTE', 'NDTUSTE_NDTE', 'NDTUCE_NDUCE', 'NDTUSTE_NDUSTE'])

    df_RQ['log10(stars)'] = np.log10(df_RQ['stars'])

    Util.format_to_csv(df_RQ, "RQs/" + RQ_NUMBER + "/", "table" + RQ_NUMBER, RQ_NUMBER, columnsToLatex)


############################## RQ2 - PART 1 ##############################
def violinPlotRatio_NDUCE_NDUE():
    f.write("\n\n ##############  RQ2 - PART 1 ##############\n")
    platformList = df_RQ["platform"].unique()
    domainList = df_RQ["domain"].unique()

    # df_aux = []
    # for platform in platformList:
    #     ratio = 0.2
    #     df_platform_total = df_RQ[(df_RQ['platform'] == platform)]
    #     df_platform_belowTo20 = df_RQ[
    #         (df_RQ['platform'] == platform) & (df_RQ['NEBTM/NTM'] <= ratio)]
    #     f.write("NEBTM_NTM <= 20% | " + platform + ":" + str(len(df_platform_belowTo20)) + " out of " + str(
    #         len(df_platform_total)) + str("({:.2%})").format(len(df_platform_belowTo20) / len(df_platform_total)))
    #     for domain in domainList:
    #         df_domain_total = df_RQ[(df_RQ["domain"] == domain) & (df_RQ['platform'] == platform)]
    #         df_belowTo20 = df_RQ[
    #             (df_RQ["domain"] == domain) & (df_RQ['platform'] == platform) & (df_RQ['NEBTM/NTM'] <= ratio)]
    #         f.write("NEBTM_NTM <= 20% | " + platform + "/" + domain + ":" + str(len(df_belowTo20)) + " out of " + str(
    #             len(df_domain_total)) + str("({:.2%})").format(len(df_belowTo20) / len(df_domain_total)))

    fig = plt.subplots(figsize=(6, 2))
    gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1.5], wspace=.02, hspace=.05)
    ax0 = plt.subplot(gs[0])
    ax1 = plt.subplot(gs[1])
    df_withoutNaN = df_RQ.dropna(subset=['NDUCE/NDUE'])
    sns.violinplot(x="domain", y="NDUCE/NDUE", data=df_RQ, cut=0, inner="box", hue="platform",
                   hue_order=Util.FIGURE_ORDER, scale="width",
                   palette=Util.COLOR_PALETTE, linewidth=1.5, ax=ax0, saturation=1)
    sns.violinplot(x="platform", y="NDUCE/NDUE", data=df_RQ, cut=0, inner="box", scale="width",
                   order=Util.FIGURE_ORDER,
                   palette=Util.COLOR_PALETTE, linewidth=1.5, ax=ax1, saturation=1)
    ax0.set(xlabel='', ylabel='', title='', yticks=[0, 0.2, 0.4, 0.6, 0.8, 1])
    ax0.set_ylabel(ax0.get_ylabel(), fontsize=Util.SIZE_AXES_LABELS)
    # ax0.set_ylim(0, 0.4)
    # ax0.legend(title="", loc="upper center")
    ax0.legend(title="", loc="upper center", bbox_to_anchor=(0.75, 1.20), ncol=3, frameon=False)
    ax0.yaxis.grid(True, linewidth=1, which="major")
    plt.setp(ax0.get_legend().get_texts(), fontsize=Util.SIZE_LEGEND_TEXT)  # for legend text
    plt.setp(ax0.get_legend().get_title(), fontsize=Util.SIZE_LEGEND_TITLE)  # for legend title
    ax0.get_yaxis().set_tick_params(labelsize=Util.SIZE_AXES_VALUES, which="major")
    ax0.get_xaxis().set_tick_params(direction='out', labelsize=Util.SIZE_AXES_VALUES)
    ax0.xaxis.set_ticks_position('bottom')
    ax0.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1, decimals=0))

    ax1.set(xlabel='', ylabel='', title='', xticks=[1], yticks=[0, 0.2, 0.4, 0.6, 0.8, 1])
    # ax1.set_xticks(5)
    ax1.set_xticklabels(['All'])
    ax1.yaxis.grid(True, linewidth=1, which="major")
    ax1.get_yaxis().set_tick_params(labelsize=Util.SIZE_AXES_VALUES, which="major")
    ax1.get_xaxis().set_tick_params(direction='out', labelsize=Util.SIZE_AXES_VALUES)
    ax1.xaxis.set_ticks_position('bottom')
    ax1.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1, decimals=0))
    ax1.set_yticklabels([])
    # ax1.set_ylim(0, 0.4)
    # Show graphic
    plt.tight_layout()
    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ2_NDUCE_NDUE_platform.pdf',
                bbox_inches="tight")
    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ2_NDUCE_NDUE_platform.png',
                bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()

def violinPlotRatio_NDUSTE_NDUE():
    platformList = df_RQ["platform"].unique()
    domainList = df_RQ["domain"].unique()

    # df_aux = []
    # for platform in platformList:
    #     ratio = 0.2
    #     df_platform_total = df_RQ[(df_RQ['platform'] == platform)]
    #     df_platform_belowTo20 = df_RQ[
    #         (df_RQ['platform'] == platform) & (df_RQ['NEBTM/NTM'] <= ratio)]
    #     f.write("NEBTM_NTM <= 20% | " + platform + ":" + str(len(df_platform_belowTo20)) + " out of " + str(
    #         len(df_platform_total)) + str("({:.2%})").format(len(df_platform_belowTo20) / len(df_platform_total)))
    #     for domain in domainList:
    #         df_domain_total = df_RQ[(df_RQ["domain"] == domain) & (df_RQ['platform'] == platform)]
    #         df_belowTo20 = df_RQ[
    #             (df_RQ["domain"] == domain) & (df_RQ['platform'] == platform) & (df_RQ['NEBTM/NTM'] <= ratio)]
    #         f.write("NEBTM_NTM <= 20% | " + platform + "/" + domain + ":" + str(len(df_belowTo20)) + " out of " + str(
    #             len(df_domain_total)) + str("({:.2%})").format(len(df_belowTo20) / len(df_domain_total)))

    fig = plt.subplots(figsize=(6, 2))
    gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1.5], wspace=.02, hspace=.05)
    ax0 = plt.subplot(gs[0])
    ax1 = plt.subplot(gs[1])
    sns.violinplot(x="domain", y="NDUSTE/NDUE", data=df_RQ, cut=0, inner="box", hue="platform",
                   hue_order=Util.FIGURE_ORDER, scale="width",
                   palette=Util.COLOR_PALETTE, linewidth=1.5, ax=ax0, saturation=1)
    sns.violinplot(x="platform", y="NDUSTE/NDUE", data=df_RQ, cut=0, inner="box", scale="width",
                   order=Util.FIGURE_ORDER,
                   palette=Util.COLOR_PALETTE, linewidth=1.5, ax=ax1, saturation=1)
    ax0.set(xlabel='', ylabel='', title='', yticks=[0, 0.2, 0.4, 0.6, 0.8, 1])
    ax0.set_ylabel(ax0.get_ylabel(), fontsize=Util.SIZE_AXES_LABELS)
    # ax0.set_ylim(0, 0.4)
    # ax0.legend(title="", loc="upper center")
    ax0.legend(title="", loc="upper center", bbox_to_anchor=(0.75, 1.20), ncol=3, frameon=False)
    ax0.yaxis.grid(True, linewidth=1, which="major")
    plt.setp(ax0.get_legend().get_texts(), fontsize=Util.SIZE_LEGEND_TEXT)  # for legend text
    plt.setp(ax0.get_legend().get_title(), fontsize=Util.SIZE_LEGEND_TITLE)  # for legend title
    ax0.get_yaxis().set_tick_params(labelsize=Util.SIZE_AXES_VALUES, which="major")
    ax0.get_xaxis().set_tick_params(direction='out', labelsize=Util.SIZE_AXES_VALUES)
    ax0.xaxis.set_ticks_position('bottom')
    ax0.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1, decimals=0))

    ax1.set(xlabel='', ylabel='', title='', xticks=[1], yticks=[0, 0.2, 0.4, 0.6, 0.8, 1])
    # ax1.set_xticks(5)
    ax1.set_xticklabels(['All'])
    ax1.yaxis.grid(True, linewidth=1, which="major")
    ax1.get_yaxis().set_tick_params(labelsize=Util.SIZE_AXES_VALUES, which="major")
    ax1.get_xaxis().set_tick_params(direction='out', labelsize=Util.SIZE_AXES_VALUES)
    ax1.xaxis.set_ticks_position('bottom')
    ax1.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1, decimals=0))
    ax1.set_yticklabels([])
    # ax1.set_ylim(0, 0.4)
    # Show graphic
    plt.tight_layout()
    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ2_NDUSTE_NDUE_platform.pdf',
                bbox_inches="tight")
    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ2_NDUSTE_NDUE_platform.png',
                bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()


def countProjectsWhere_NDUCE_RATIO_isBigger(df_aux):
    df_clean = df_aux[(df_aux['NDUCE/NDUE'] > df_aux['NDUSTE/NDUE'])]
    f.write(f'Number of projects where NDUCE/NDUE > NDUSTE/NDUE = {len(df_clean)} :  {df_clean["project"].values.tolist()} \n')

def violinPlotRatio_NDUCE_NDUE_NDUSTE_NDUE_MELTED():
    fig, ax = plt.subplots(figsize=(6, 2))
    countProjectsWhere_NDUCE_RATIO_isBigger(df_RQ.dropna(subset=['project', 'NDUCE/NDUE', 'NDUSTE/NDUE']))

    df_withoutNaN = df_RQ.dropna(subset=['NDUCE/NDUE', 'NDUSTE/NDUE'])
    df_melted = pd.melt(df_withoutNaN, id_vars=["project", "platform"], value_vars=['NDUCE/NDUE', 'NDUSTE/NDUE'])
    sns.violinplot(x="variable", y="value", data=df_melted, cut=0, inner="box", hue="platform",
                   hue_order=Util.FIGURE_ORDER, scale="width",
                   palette=Util.COLOR_PALETTE, linewidth=1.5, ax=ax, saturation=1)
    ax.set(xlabel='', ylabel='', title='', yticks=[0, 0.2, 0.4, 0.6, 0.8, 1])
    ax.set_ylabel(ax.get_ylabel(), fontsize=Util.SIZE_AXES_LABELS)
    # ax0.set_ylim(0, 0.4)
    # ax0.legend(title="", loc="upper center")
    ax.legend(title="", loc="upper center", bbox_to_anchor=(0.5, 1.20), ncol=3, frameon=False)
    ax.yaxis.grid(True, linewidth=1, which="major")
    plt.setp(ax.get_legend().get_texts(), fontsize=Util.SIZE_LEGEND_TEXT)  # for legend text
    plt.setp(ax.get_legend().get_title(), fontsize=Util.SIZE_LEGEND_TITLE)  # for legend title
    ax.get_yaxis().set_tick_params(labelsize=Util.SIZE_AXES_VALUES, which="major")
    ax.get_xaxis().set_tick_params(direction='out', labelsize=Util.SIZE_AXES_VALUES)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1, decimals=0))
    # Show graphic
    plt.tight_layout()
    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ2_NDUCE_NDUE_NDUSTE_NDUE_MELTED_platform.pdf',
                bbox_inches="tight")
    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ2_NDUCE_NDUE_NDUSTE_NDUE_MELTED_platform.png',
                bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()
############################## RQ2 - PART 2 ##############################
def violinPlotRatio_NDTCE_NDTE():
    f.write("\n\n ##############  RQ2 - PART 2 ##############\n")
    df_totalSize = len(df_RQ[(df_RQ['NEBTM'] > 0)])
    df_aux = df_RQ[(df_RQ['NDTCE/NDTE'] < 0.5)]
    df_auxSize = len(df_aux)
    f.write(f'Number of projects where NDTCE/NDTE < 0.5 = {df_auxSize} out of {df_totalSize} ({round(df_auxSize/df_totalSize*100,2)}) \n')
    # df_aux = []
    # for platform in platformList:
    #     ratio = 0.2
    #     df_platform_total = df_RQ[(df_RQ['platform'] == platform)]
    #     df_platform_belowTo20 = df_RQ[
    #         (df_RQ['platform'] == platform) & (df_RQ['NEBTM/NTM'] <= ratio)]
    #     f.write("NEBTM_NTM <= 20% | " + platform + ":" + str(len(df_platform_belowTo20)) + " out of " + str(
    #         len(df_platform_total)) + str("({:.2%})").format(len(df_platform_belowTo20) / len(df_platform_total)) \n)
    #     for domain in domainList:
    #         df_domain_total = df_RQ[(df_RQ["domain"] == domain) & (df_RQ['platform'] == platform)]
    #         df_belowTo20 = df_RQ[
    #             (df_RQ["domain"] == domain) & (df_RQ['platform'] == platform) & (df_RQ['NEBTM/NTM'] <= ratio)]
    #         f.write("NEBTM_NTM <= 20% | " + platform + "/" + domain + ":" + str(len(df_belowTo20)) + " out of " + str(
    #             len(df_domain_total)) + str("({:.2%})").format(len(df_belowTo20) / len(df_domain_total)) \n)

    fig = plt.subplots(figsize=(6, 2))
    gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1.5], wspace=.02, hspace=.05)
    ax0 = plt.subplot(gs[0])
    ax1 = plt.subplot(gs[1])
    sns.violinplot(x="domain", y="NDTCE/NDTE", data=df_RQ, cut=0, inner="box", hue="platform",
                   hue_order=Util.FIGURE_ORDER, scale="width",
                   palette=Util.COLOR_PALETTE, linewidth=1.5, ax=ax0, saturation=1)
    sns.violinplot(x="platform", y="NDTCE/NDTE", data=df_RQ, cut=0, inner="box", scale="width",
                   order=Util.FIGURE_ORDER,
                   palette=Util.COLOR_PALETTE, linewidth=1.5, ax=ax1, saturation=1)
    ax0.set(xlabel='', ylabel='', title='', yticks=[0, 0.2, 0.4, 0.6, 0.8, 1])
    ax0.set_ylabel(ax0.get_ylabel(), fontsize=Util.SIZE_AXES_LABELS)
    # ax0.set_ylim(0, 0.4)
    # ax0.legend(title="", loc="upper center")
    ax0.legend(title="", loc="upper center", bbox_to_anchor=(0.75, 1.20), ncol=3, frameon=False)
    ax0.yaxis.grid(True, linewidth=1, which="major")
    plt.setp(ax0.get_legend().get_texts(), fontsize=Util.SIZE_LEGEND_TEXT)  # for legend text
    plt.setp(ax0.get_legend().get_title(), fontsize=Util.SIZE_LEGEND_TITLE)  # for legend title
    ax0.get_yaxis().set_tick_params(labelsize=Util.SIZE_AXES_VALUES, which="major")
    ax0.get_xaxis().set_tick_params(direction='out', labelsize=Util.SIZE_AXES_VALUES)
    ax0.xaxis.set_ticks_position('bottom')
    ax0.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1, decimals=0))

    ax1.set(xlabel='', ylabel='', title='', xticks=[1], yticks=[0, 0.2, 0.4, 0.6, 0.8, 1])
    # ax1.set_xticks(5)
    ax1.set_xticklabels(['All'])
    ax1.yaxis.grid(True, linewidth=1, which="major")
    ax1.get_yaxis().set_tick_params(labelsize=Util.SIZE_AXES_VALUES, which="major")
    ax1.get_xaxis().set_tick_params(direction='out', labelsize=Util.SIZE_AXES_VALUES)
    ax1.xaxis.set_ticks_position('bottom')
    ax1.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1, decimals=0))
    ax1.set_yticklabels([])
    # ax1.set_ylim(0, 0.4)
    # Show graphic
    plt.tight_layout()
    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ2_NDTCE_NDTE_platform.pdf',
                bbox_inches="tight")
    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ2_NDTCE_NDTE_platform.png',
                bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()

def violinPlotRatio_NDTSTE_NDTE():
    platformList = df_RQ["platform"].unique()
    domainList = df_RQ["domain"].unique()

    # df_aux = []
    # for platform in platformList:
    #     ratio = 0.2
    #     df_platform_total = df_RQ[(df_RQ['platform'] == platform)]
    #     df_platform_belowTo20 = df_RQ[
    #         (df_RQ['platform'] == platform) & (df_RQ['NEBTM/NTM'] <= ratio)]
    #     f.write("NEBTM_NTM <= 20% | " + platform + ":" + str(len(df_platform_belowTo20)) + " out of " + str(
    #         len(df_platform_total)) + str("({:.2%})").format(len(df_platform_belowTo20) / len(df_platform_total))\n)
    #     for domain in domainList:
    #         df_domain_total = df_RQ[(df_RQ["domain"] == domain) & (df_RQ['platform'] == platform)]
    #         df_belowTo20 = df_RQ[
    #             (df_RQ["domain"] == domain) & (df_RQ['platform'] == platform) & (df_RQ['NEBTM/NTM'] <= ratio)]
    #         f.write("NEBTM_NTM <= 20% | " + platform + "/" + domain + ":" + str(len(df_belowTo20)) + " out of " + str(
    #             len(df_domain_total)) + str("({:.2%})").format(len(df_belowTo20) / len(df_domain_total))\n)

    fig = plt.subplots(figsize=(6, 2))
    gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1.5], wspace=.02, hspace=.05)
    ax0 = plt.subplot(gs[0])
    ax1 = plt.subplot(gs[1])
    sns.violinplot(x="domain", y="NDTSTE/NDTE", data=df_RQ, cut=0, inner="box", hue="platform",
                   hue_order=Util.FIGURE_ORDER, scale="width",
                   palette=Util.COLOR_PALETTE, linewidth=1.5, ax=ax0, saturation=1)
    sns.violinplot(x="platform", y="NDTSTE/NDTE", data=df_RQ, cut=0, inner="box", scale="width",
                   order=Util.FIGURE_ORDER,
                   palette=Util.COLOR_PALETTE, linewidth=1.5, ax=ax1, saturation=1)
    ax0.set(xlabel='', ylabel='', title='', yticks=[0, 0.2, 0.4, 0.6, 0.8, 1])
    ax0.set_ylabel(ax0.get_ylabel(), fontsize=Util.SIZE_AXES_LABELS)
    # ax0.set_ylim(0, 0.4)
    # ax0.legend(title="", loc="upper center")
    ax0.legend(title="", loc="upper center", bbox_to_anchor=(0.75, 1.20), ncol=3, frameon=False)
    ax0.yaxis.grid(True, linewidth=1, which="major")
    plt.setp(ax0.get_legend().get_texts(), fontsize=Util.SIZE_LEGEND_TEXT)  # for legend text
    plt.setp(ax0.get_legend().get_title(), fontsize=Util.SIZE_LEGEND_TITLE)  # for legend title
    ax0.get_yaxis().set_tick_params(labelsize=Util.SIZE_AXES_VALUES, which="major")
    ax0.get_xaxis().set_tick_params(direction='out', labelsize=Util.SIZE_AXES_VALUES)
    ax0.xaxis.set_ticks_position('bottom')
    ax0.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1, decimals=0))

    ax1.set(xlabel='', ylabel='', title='', xticks=[1], yticks=[0, 0.2, 0.4, 0.6, 0.8, 1])
    # ax1.set_xticks(5)
    ax1.set_xticklabels(['All'])
    ax1.yaxis.grid(True, linewidth=1, which="major")
    ax1.get_yaxis().set_tick_params(labelsize=Util.SIZE_AXES_VALUES, which="major")
    ax1.get_xaxis().set_tick_params(direction='out', labelsize=Util.SIZE_AXES_VALUES)
    ax1.xaxis.set_ticks_position('bottom')
    ax1.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1, decimals=0))
    ax1.set_yticklabels([])
    # ax1.set_ylim(0, 0.4)
    # Show graphic
    plt.tight_layout()
    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ2_NDTSTE_NDTE_platform.pdf',
                bbox_inches="tight")
    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ2_NDTSTE_NDTE_platform.png',
                bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()



def violinPlotRatio_NDTCE_NDTE_NDTSTE_NDTE_MELTED():
    fig, ax = plt.subplots(figsize=(6, 2))
    df_withoutNaN = df_RQ.dropna(subset=['NDTCE/NDTE', 'NDTSTE/NDTE'])

    df_melted = pd.melt(df_withoutNaN, id_vars=["project", "platform"], value_vars=['NDTCE/NDTE', 'NDTSTE/NDTE'])
    sns.violinplot(x="variable", y="value", data=df_melted, cut=0, inner="box", hue="platform",
                   hue_order=Util.FIGURE_ORDER, scale="width",
                   palette=Util.COLOR_PALETTE, linewidth=1.5, ax=ax, saturation=1)
    ax.set(xlabel='', ylabel='', title='', yticks=[0, 0.2, 0.4, 0.6, 0.8, 1])
    ax.set_ylabel(ax.get_ylabel(), fontsize=Util.SIZE_AXES_LABELS)
    # ax0.set_ylim(0, 0.4)
    # ax0.legend(title="", loc="upper center")
    ax.legend(title="", loc="upper center", bbox_to_anchor=(0.5, 1.20), ncol=3, frameon=False)
    ax.yaxis.grid(True, linewidth=1, which="major")
    plt.setp(ax.get_legend().get_texts(), fontsize=Util.SIZE_LEGEND_TEXT)  # for legend text
    plt.setp(ax.get_legend().get_title(), fontsize=Util.SIZE_LEGEND_TITLE)  # for legend title
    ax.get_yaxis().set_tick_params(labelsize=Util.SIZE_AXES_VALUES, which="major")
    ax.get_xaxis().set_tick_params(direction='out', labelsize=Util.SIZE_AXES_VALUES)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1, decimals=0))
    # Show graphic
    plt.tight_layout()
    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ2_NDTCE_NDTE_NDTSTE_NDTE_MELTED_platform.pdf',
                bbox_inches="tight")
    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ2_NDTCE_NDTE_NDTSTE_NDTE_MELTED_platform.png',
                bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()
############################## RQ2 - PART 3 ##############################
def calculate_NDTCE_NDUCE_and_NDTSTE_NDUSTE_ratio(df_aux, column1, column2, description):
    df = df_aux.dropna(subset=['project', column1, column2])
    df_higherThan = df[(df[column1] > df[column2])]
    dfTotalSize = len(df)
    dfHigherThanSize = len(df_higherThan)
    f.write(f'{description}_NDTCE/NDUCE > NDTSTE/NDUSTE: {dfHigherThanSize} out of {dfTotalSize} ({round(dfHigherThanSize/dfTotalSize*100,2)})\n')


def countProjectsWhere_NDTCE_NDUCE_and_NDTSTE_NDUSTE_isHigherThanFiftyPercent(df_aux):
    df_clean = df_aux[(df_aux['NDTCE/NDUCE'] > 0.5) & (df_aux['NDTSTE/NDUSTE'] > 0.5)]
    f.write(f'Number of projects where NDTCE/NDUCE and NDTSTE_NDUSTE is higher than 50% = {len(df_clean)} out of {len(df_aux)} : {df_clean["project"].values.tolist()} ({round(len(df_clean)/len(df_aux)*100,2)}%)\n')


def violinPlotRatio_NDTCE_NDUCE():
    f.write("\n\n ##############  RQ2 - PART 3 ##############\n")
    platformList = df_RQ["platform"].unique()
    domainList = df_RQ["domain"].unique()

    df_aux = df_RQ[(df_RQ['NEBTM'] > 0)]

    #countProjectsWhere_NDTCE_NDUCE_and_NDTSTE_NDUSTE_isHigherThanFiftyPercent(df_aux.dropna(subset=['project', 'NDTCE/NDUCE', 'NDTSTE/NDUSTE']))
    countProjectsWhere_NDTCE_NDUCE_and_NDTSTE_NDUSTE_isHigherThanFiftyPercent(df_aux)
    calculate_NDTCE_NDUCE_and_NDTSTE_NDUSTE_ratio(df_aux, 'NDTCE/NDUCE', 'NDTSTE/NDUSTE', "Total")
    for platform in platformList:
        df_platform = df_aux[(df_aux['platform'] == platform)]
        calculate_NDTCE_NDUCE_and_NDTSTE_NDUSTE_ratio(df_platform, 'NDTCE/NDUCE', 'NDTSTE/NDUSTE', platform)
        for domain in domainList:
            df_domain = df_platform[(df_platform['domain'] == domain)]
            calculate_NDTCE_NDUCE_and_NDTSTE_NDUSTE_ratio(df_domain, 'NDTCE/NDUCE', 'NDTSTE/NDUSTE', f'{platform}_{domain}')

    Util.evaluate_outliers(df_aux, 'NDTCE/NDUCE', f)
    fig = plt.subplots(figsize=(6, 2))
    gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1.5], wspace=.02, hspace=.05)
    ax0 = plt.subplot(gs[0])
    ax1 = plt.subplot(gs[1])
    df_withoutNaN = df_aux.dropna(subset=['NDTCE/NDUCE'])
    sns.violinplot(x="domain", y="NDTCE/NDUCE", data=df_aux, cut=0, inner="box", hue="platform",
                   hue_order=Util.FIGURE_ORDER, scale="width",
                   palette=Util.COLOR_PALETTE, linewidth=1.5, ax=ax0, saturation=1)
    sns.violinplot(x="platform", y="NDTCE/NDUCE", data=df_aux, cut=0, inner="box", scale="width",
                   order=Util.FIGURE_ORDER,
                   palette=Util.COLOR_PALETTE, linewidth=1.5, ax=ax1, saturation=1)
    ax0.set(xlabel='', ylabel='', title='', yticks=[0, 0.2, 0.4, 0.6, 0.8, 1])
    ax0.set_ylabel(ax0.get_ylabel(), fontsize=Util.SIZE_AXES_LABELS)
    # ax0.set_ylim(0, 0.4)
    # ax0.legend(title="", loc="upper center")
    ax0.legend(title="", loc="upper center", bbox_to_anchor=(0.75, 1.20), ncol=3, frameon=False)
    ax0.yaxis.grid(True, linewidth=1, which="major")
    plt.setp(ax0.get_legend().get_texts(), fontsize=Util.SIZE_LEGEND_TEXT)  # for legend text
    plt.setp(ax0.get_legend().get_title(), fontsize=Util.SIZE_LEGEND_TITLE)  # for legend title
    ax0.get_yaxis().set_tick_params(labelsize=Util.SIZE_AXES_VALUES, which="major")
    ax0.get_xaxis().set_tick_params(direction='out', labelsize=Util.SIZE_AXES_VALUES)
    ax0.xaxis.set_ticks_position('bottom')
    ax0.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1, decimals=0))

    ax1.set(xlabel='', ylabel='', title='', xticks=[1], yticks=[0, 0.2, 0.4, 0.6, 0.8, 1])
    # ax1.set_xticks(5)
    ax1.set_xticklabels(['All'])
    ax1.yaxis.grid(True, linewidth=1, which="major")
    ax1.get_yaxis().set_tick_params(labelsize=Util.SIZE_AXES_VALUES, which="major")
    ax1.get_xaxis().set_tick_params(direction='out', labelsize=Util.SIZE_AXES_VALUES)
    ax1.xaxis.set_ticks_position('bottom')
    ax1.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1, decimals=0))
    ax1.set_yticklabels([])
    # ax1.set_ylim(0, 0.4)
    # Show graphic
    plt.tight_layout()
    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ2_NDTCE_NDUCE_platform.pdf',
                bbox_inches="tight")
    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ2_NDTCE_NDUCE_platform.png',
                bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()


def violinPlotRatio_NDTSTE_NDUSTE():
    platformList = df_RQ["platform"].unique()
    domainList = df_RQ["domain"].unique()

    fig = plt.subplots(figsize=(6, 2))
    gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1.5], wspace=.02, hspace=.05)
    ax0 = plt.subplot(gs[0])
    ax1 = plt.subplot(gs[1])
    sns.violinplot(x="domain", y="NDTSTE/NDUSTE", data=df_RQ, cut=0, inner="box", hue="platform",
                   hue_order=Util.FIGURE_ORDER, scale="width",
                   palette=Util.COLOR_PALETTE, linewidth=1.5, ax=ax0, saturation=1)
    sns.violinplot(x="platform", y="NDTSTE/NDUSTE", data=df_RQ, cut=0, inner="box", scale="width",
                   order=Util.FIGURE_ORDER,
                   palette=Util.COLOR_PALETTE, linewidth=1.5, ax=ax1, saturation=1)
    ax0.set(xlabel='', ylabel='', title='', yticks=[0, 0.2, 0.4, 0.6, 0.8, 1])
    ax0.set_ylabel(ax0.get_ylabel(), fontsize=Util.SIZE_AXES_LABELS)
    # ax0.set_ylim(0, 0.4)
    # ax0.legend(title="", loc="upper center")
    ax0.legend(title="", loc="upper center", bbox_to_anchor=(0.75, 1.20), ncol=3, frameon=False)
    ax0.yaxis.grid(True, linewidth=1, which="major")
    plt.setp(ax0.get_legend().get_texts(), fontsize=Util.SIZE_LEGEND_TEXT)  # for legend text
    plt.setp(ax0.get_legend().get_title(), fontsize=Util.SIZE_LEGEND_TITLE)  # for legend title
    ax0.get_yaxis().set_tick_params(labelsize=Util.SIZE_AXES_VALUES, which="major")
    ax0.get_xaxis().set_tick_params(direction='out', labelsize=Util.SIZE_AXES_VALUES)
    ax0.xaxis.set_ticks_position('bottom')
    ax0.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1, decimals=0))

    ax1.set(xlabel='', ylabel='', title='', xticks=[1], yticks=[0, 0.2, 0.4, 0.6, 0.8, 1])
    # ax1.set_xticks(5)
    ax1.set_xticklabels(['All'])
    ax1.yaxis.grid(True, linewidth=1, which="major")
    ax1.get_yaxis().set_tick_params(labelsize=Util.SIZE_AXES_VALUES, which="major")
    ax1.get_xaxis().set_tick_params(direction='out', labelsize=Util.SIZE_AXES_VALUES)
    ax1.xaxis.set_ticks_position('bottom')
    ax1.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1, decimals=0))
    ax1.set_yticklabels([])
    # ax1.set_ylim(0, 0.4)
    # Show graphic
    plt.tight_layout()
    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ2_NDTSTE_NDUSTE_platform.pdf',
                bbox_inches="tight")
    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ2_NDTSTE_NDUSTE_platform.png',
                bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()


########################################END #####################

def evaluateStatistics():
    platformList = df_RQ["platform"].unique()
    domainList = df_RQ["domain"].unique()

    for platform in platformList:
        df_platform = df_RQ[(df_RQ['platform'] == platform)]
        StatisticalTests.compareDataSamples(df_platform["NDTCE/NDUCE"].dropna(), df_platform["NDTSTE/NDUSTE"].dropna(),
                                         platform.replace("/", "_") + "_NDTCE_NDUCE_And_NDTSTE_NDUSTE", "RQs/RQ2/statistics/")
        for domain in domainList:
            df_domain = df_platform[(df_platform["domain"] == domain)]
            StatisticalTests.compareDataSamples(df_domain["NDTCE/NDUCE"].dropna(), df_domain["NDTSTE/NDUSTE"].dropna(), platform.replace("/", "_") + "_" + domain + "_NDTCE_NDUCE_And_NDTSTE_NDUSTE", "RQs/RQ2/statistics/")

            # StatisticalTests.TTestEvaluation_NDTCE_NDTE_And_NDTSTE_NDTE(df_RQ)
            # StatisticalTests.TTestEvaluation_NDTCE_NDUCE_And_NDTSTE_NDUSTE(df_RQ)
            # StatisticalTests.mannwhitneyuEvaluation_NDTCE_NDUCE_And_NDTSTE_NDUSTE(df_RQ)


##################################################################
generateDataSet()

# RQ2-PART1
violinPlotRatio_NDUCE_NDUE()
violinPlotRatio_NDUSTE_NDUE()
violinPlotRatio_NDUCE_NDUE_NDUSTE_NDUE_MELTED()


# RQ2-PART2
violinPlotRatio_NDTCE_NDTE()
violinPlotRatio_NDTSTE_NDTE()
violinPlotRatio_NDTCE_NDTE_NDTSTE_NDTE_MELTED()

# RQ2-PART3
violinPlotRatio_NDTCE_NDUCE()
violinPlotRatio_NDTSTE_NDUSTE()

#StatisticalTests
evaluateStatistics()

