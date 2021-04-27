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

CUSTOM_SIZE_Y_AXES_VALUES = "large"
CUSTOM_SIZE_X_AXES_VALUES = 10

SHOW_FIGURE = False

df_RQ = ""

# columnsToLatex = ['NTSSTPE', 'NTSCE', 'NTSNIE', 'NTS', 'NTSSTPE/NTS', 'NTSCE/NTS', 'NTSNIE/NTS', 'NCTSSTPE',
#                                   'NCTSCE', 'NCTNIE', 'NCTS', 'NCTSSTPE/NCTS', 'NCTNIE/NCTS', 'NCTSCE/NCTS', 'NCTSCE/NTSCE', 'NCTSSTPE/NTSSTPE', 'NCTSSTPE/NTSSTPE_REAL']

columnsToLatex = ['NCTS', 'NTS', 'NCTS/NTS', 'tagCoverage']
#columnsToLatex = ['NCTSCE', 'NTSCE', 'NCTSCE/NTSCE', 'NCTSSTPE', 'NTSSTPE', 'NCTSSTPE/NTSSTPE']

RQ_NUMBER = "RQ3_RQ4"
OUTPUT_PATH = "RQS/" + RQ_NUMBER
OUTPUT_FIGURES_PATH = Util.create_new_dirs(OUTPUT_PATH + "/figures/")

fileName = "res_"+RQ_NUMBER+".txt"
f = open(Path(OUTPUT_PATH) / fileName, "w+")


############################## TABLE GENERATION ##############################
def generateDataSet():
    global df_RQ
    dataSet = []
    for doc in Util.mongo_collection.find():
        if doc['tagCoverageWithProblems'] is True or doc['tagCoverage'] is None or doc['tagCoverage'] == 0.0:
        #if doc['tagCoverage'] is None or doc['tagCoverage'] == 0.0:
            continue
        project = doc["projectName"]
        tagCreatedOn = datetime.strptime(doc["tagCreatedAt"], '%d/%m/%Y %H:%M:%S').year
        tagCoverage = doc['tagCoverage']/100
        projectCreatedOn = datetime.strptime(doc["projectDetails"]["createdAt"], '%d/%m/%Y %H:%M:%S').year
        platform = doc['projectDetails']["platform"]
        domain = Util.adjust_domain_name(doc['projectDetails']["domain"])
        stars = doc['projectDetails']["stars"]
        contributors = doc['projectDetails']["contributors"]
        NTSSTPE = doc["statistics"]['totalNumberOfThrowStatementsStandardOrThirdPartyExceptions']
        NTSCE = doc["statistics"]['totalNumberOfThrowStatementCustomExceptions']
        NTSNIE = doc["statistics"]['totalNumberOfThrowStatementNotIdentifiedExceptions']
        NTS = doc["statistics"]['totalNumberOfThrowStatements']
        NTSSTPE_NTS = round(np.float64(NTSSTPE) / NTS, 4)
        NTSCE_NTS = round(np.float64(NTSCE) / NTS, 4)
        NTSNIE_NTS = round(np.float64(NTSNIE) / NTS, 4)
        NEBTM = doc["statistics"]['totalNumberOfExceptionalBehaviorTestMethods']
        NTM = doc["statistics"]['totalNumberOfTestMethods']
        NEBTM_NTM = round(np.float64(NEBTM) / np.float64(NTM), 4)

        #Tested and Used Exceptions
        NDTE = doc["statistics"]['totalNumberOfDistinctTestedExceptions']  # distinct used and tested exceptions
        NDUE = doc["statistics"]['totalNumberOfDistinctUsedExceptions']  # distinct used exceptions
        NDTE_NDUE = round(np.float64(NDTE) / np.float64(NDUE), 4)


        # Only covered exceptions
        NCTSSTPE = doc["statistics"]['totalNumberOfCoveredThrowStatementsStandardOrThirdPartyExceptions']
        NCTSCE = doc["statistics"]['totalNumberOfCoveredThrowStatementCustomExceptions']
        NCTNIE = doc["statistics"]['totalNumberOfCoveredThrowStatementNotIdentifiedExceptions']
        NCTS = doc["statistics"]['totalNumberOfCoveredThrowStatements']
        NCTSSTPE_NCTS = round(np.float64(NCTSSTPE) / NCTS, 4)
        NCTSCE_NCTS = round(np.float64(NCTSCE) / NCTS, 4)
        NCTNIE_NCTS = round(np.float64(NCTNIE) / NCTS, 4)

        NCTS_NTS = round(np.float64(NCTS) / NTS, 4)
        NCTSCE_NTSCE = round(np.float64(NCTSCE) / NTSCE, 4)
        if np.isnan(NCTSCE_NTSCE):
            NCTSSTPE_NTSSTPE = float("NaN")
        else:
            NCTSSTPE_NTSSTPE = round(np.float64(NCTSSTPE) / NTSSTPE, 4)
        NCTSSTPE_NTSSTPE_REAL = round(np.float64(NCTSSTPE) / NTSSTPE, 4)

        dataSetRQ3 = [project, tagCreatedOn, tagCoverage, projectCreatedOn, platform, domain, stars,
                      contributors, NEBTM_NTM, NTSSTPE, NTSCE, NTSNIE, NTS, NTSSTPE_NTS, NTSCE_NTS, NTSNIE_NTS, NCTSSTPE,
                      NCTSCE, NCTNIE, NCTS, NCTSSTPE_NCTS, NCTSCE_NCTS, NCTNIE_NCTS, NCTS_NTS, NCTSCE_NTSCE, NCTSSTPE_NTSSTPE, NCTSSTPE_NTSSTPE_REAL, NDTE_NDUE]
        dataSet.append(dataSetRQ3)

    df_RQ = pd.DataFrame(dataSet,
                         columns=['project', 'tagCreatedOn', 'tagCoverage', 'projectCreatedOn', 'platform', 'domain', 'stars',
                                  'contributors','NEBTM/NTM', 'NTSSTPE', 'NTSCE', 'NTSNIE', 'NTS', 'NTSSTPE/NTS', 'NTSCE/NTS', 'NTSNIE/NTS', 'NCTSSTPE',
                                  'NCTSCE', 'NCTNIE', 'NCTS', 'NCTSSTPE/NCTS', 'NCTNIE/NCTS', 'NCTSCE/NCTS', 'NCTS/NTS', 'NCTSCE/NTSCE', 'NCTSSTPE/NTSSTPE', 'NCTSSTPE/NTSSTPE_REAL', 'NDTE/NDUE'])


    Util.format_to_csv(df_RQ, "RQs/" + RQ_NUMBER + "/", "table" + RQ_NUMBER, RQ_NUMBER, columnsToLatex)


############################## RQ3 - PART 1 ##############################

def barPlotNumberOfProjects():
    platformList = df_RQ["platform"].unique()
    domainList = df_RQ["domain"].unique()

    df_aux = []
    totalDfSize = len(df_RQ)
    f.write(f'Number of projects with coverage data: {totalDfSize}\n')
    for platform in platformList:
        df_platform = df_RQ[(df_RQ['platform'] == platform)]
        totalPlatformDfSize = len(df_platform)
        ratioAux = round(totalPlatformDfSize/totalDfSize, 4)
        f.write(f'{platform}_Number of projects with coverage data: {totalPlatformDfSize} out of {totalDfSize}({ratioAux})\n')
        for domain in domainList:
            df_domain = df_platform[(df_platform["domain"] == domain)]
            totalDomainDfSize = len(df_domain)
            df_aux.append([platform, domain, totalDomainDfSize])
            ratioAux = round(totalDomainDfSize / totalDfSize, 4)
            f.write(f'{platform}_{domain}_Number of projects with coverage data: {totalDomainDfSize} out of {totalDfSize}({ratioAux})\n')

    df_counter = pd.DataFrame(df_aux, columns=["platform", "domain", "count"])
    # g = sns.catplot(x="domain", y="count", col="platform",  data=df_counter, kind="bar",
    #                 palette=Util.COLOR_DEGRADE, legend=False, legend_out=False, col_order=Util.FIGURE_ORDER)
    g = sns.catplot(x="domain", y="count", col="platform",  data=df_counter, kind="bar",
                     legend=False, legend_out=False, col_order=Util.FIGURE_ORDER, color="#1b69af")
    g.fig.subplots_adjust(wspace=.05, hspace=.05)
    g.fig.set_figheight(3)
    g.fig.set_figwidth(6)

    for ax in g.axes.flat:
        # ax.get_yaxis().set_tick_params(labelsize='x-large', which="major")
        # labels ao redor dos graficos
        # ax.set_xlabel(ax.get_xlabel(), fontsize='20')
        ax.set_xlabel("", fontsize=Util.SIZE_AXES_LABELS, rotation=30)
        ax.set_ylabel(ax.get_ylabel(), fontsize=Util.SIZE_AXES_LABELS)

        # títulos em cima dos graficos
        if ax.get_title():
            ax.set_title(ax.get_title().split('=')[1],
                         fontsize=Util.SIZE_AXES_TITLE)
        # Valores em cima das barras
        for p in ax.patches:
            height = p.get_height()
            ax.text(p.get_x() + p.get_width() / 2., height + 0.1, int(height), ha="center", fontsize=Util.SIZE_BAR_VALUES)

        ax.yaxis.grid(True, linewidth=1, which="major")
        ax.get_yaxis().set_tick_params(labelsize=Util.SIZE_AXES_TITLE, which="major")
        ax.get_xaxis().set_tick_params(direction='out', labelsize=Util.SIZE_AXES_TITLE, rotation=20)

    ax_aux = g.axes[0, 0]
    ax_aux.set_xlabel('', fontsize=Util.SIZE_AXES_LABELS)
    ax_aux.set_ylabel('Number of Projects', fontsize=Util.SIZE_AXES_LABELS)
    # Show graphic
    plt.tight_layout()
    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ3_numberOfProjectsWithCoverageData_bar.pdf', bbox_inches="tight")
    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ3_numberOfProjectsWithCoverageData_bar.png', bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()

def violinPlotTagCoverage():
    fig = plt.subplots(figsize=(6, 2))
    gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1.5], wspace=.02, hspace=.05)
    ax0 = plt.subplot(gs[0])
    ax1 = plt.subplot(gs[1])
    df_coverageAboveSixty = df_RQ[(df_RQ['tagCoverage'] >= 0.6)]
    f.write(f'Number of projects with coverage greater or equal to 60%: {len(df_coverageAboveSixty)}\n')
    df_withoutNaN = df_RQ.dropna(subset=['tagCoverage'])
    sns.violinplot(x="domain", y="tagCoverage", data=df_RQ, cut=0, inner="box", hue="platform",
                   hue_order=Util.FIGURE_ORDER, scale="width",
                   palette=Util.COLOR_PALETTE, linewidth=1.5, ax=ax0, saturation=1)
    sns.violinplot(x="platform", y="tagCoverage", data=df_RQ, cut=0, inner="box", scale="width",
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
    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ3_Description_TagCoverage.pdf',
                bbox_inches="tight")
    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ3_Description_TagCoverage.png',
                bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()

def violinPlotRatio_NCTS_NTS():
    platformList = df_RQ["platform"].unique()
    domainList = df_RQ["domain"].unique()

    Util.count_number_of_projects_lte_to_ratio(df_RQ, "tagCoverage", 0.6, f)
    Util.count_number_of_projects_lte_to_ratio(df_RQ, "NCTS/NTS", 0.6, f)

    Util.count_number_of_projects_gte_to_ratio(df_RQ, "tagCoverage", 0.6, f)
    Util.count_number_of_projects_gte_to_ratio(df_RQ, "NCTS/NTS", 0.6, f)

    Util.count_number_of_projects_gte_to_ratio(df_RQ, "tagCoverage", 0.8, f)
    Util.count_number_of_projects_gte_to_ratio(df_RQ, "NCTS/NTS", 0.8, f)

    Util.count_number_of_projects_gte_to_ratio(df_RQ, "tagCoverage", 0.9, f)
    Util.count_number_of_projects_gte_to_ratio(df_RQ, "NCTS/NTS", 0.9, f)

    fig = plt.subplots(figsize=(6, 2))
    gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1.5], wspace=.02, hspace=.05)
    ax0 = plt.subplot(gs[0])
    ax1 = plt.subplot(gs[1])
    df_withoutNaN = df_RQ.dropna(subset=['NCTS/NTS'])

    sns.violinplot(x="domain", y="NCTS/NTS", data=df_RQ, cut=0, inner="box", hue="platform",
                   hue_order=Util.FIGURE_ORDER, scale="width",
                   palette=Util.COLOR_PALETTE, linewidth=1.5, ax=ax0, saturation=1)
    sns.violinplot(x="platform", y="NCTS/NTS", data=df_RQ, cut=0, inner="box", scale="width",
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
    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ3_NCTS_NTS_platform.pdf',
                bbox_inches="tight")
    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ3_NCTS_NTS_platform.png',
                bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()

def violinPlotRatio_Overall_NCTS_NTS():
    ax = sns.violinplot(y="NCTS/NTS", data=df_RQ, cut=0, inner="box",
                   linewidth=1.5, saturation=1)
    ax.set(xlabel='', ylabel='', title='', yticks=[0, 0.2, 0.4, 0.6, 0.8, 1])
    ax.set_ylabel(ax.get_ylabel(), fontsize=Util.SIZE_AXES_LABELS)
    # ax0.set_ylim(0, 0.4)
    # ax0.legend(title="", loc="upper center")
    #ax.legend(title="", loc="upper center", bbox_to_anchor=(0.75, 1.20), ncol=3, frameon=False)
    ax.yaxis.grid(True, linewidth=1, which="major")
    plt.setp(ax.get_legend().get_texts(), fontsize=Util.SIZE_LEGEND_TEXT)  # for legend text
    plt.setp(ax.get_legend().get_title(), fontsize=Util.SIZE_LEGEND_TITLE)  # for legend title
    ax.get_yaxis().set_tick_params(labelsize=Util.SIZE_AXES_VALUES, which="major")
    ax.get_xaxis().set_tick_params(direction='out', labelsize=Util.SIZE_AXES_VALUES)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1, decimals=0))

    # Show graphic
    plt.tight_layout()
    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ3_NCTS_NTS_overall.pdf',
                bbox_inches="tight")
    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ3_NCTS_NTS_overall.png',
                bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()

def pairPlotCoverages():
    g = sns.lmplot(data=df_RQ,
                      x='NCTS/NTS', y='tagCoverage', hue="platform", fit_reg=False, palette=Util.COLOR_PALETTE_COLORFUL, legend=False, hue_order=Util.FIGURE_ORDER)
    #plt.tight_layout()
    ax_aux = g.axes[0, 0]
    ax_aux.legend(title="", loc="upper center", bbox_to_anchor=(0.5, 1.1), ncol=3, frameon=False)
    ax_aux.set_xlabel('NCTS/NTS', fontsize=Util.SIZE_AXES_LABELS)
    ax_aux.set_ylabel('Line Coverage', fontsize=Util.SIZE_AXES_LABELS)
    ax_aux.xaxis.set_major_formatter(ticker.PercentFormatter(xmax=1, decimals=0))
    ax_aux.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1, decimals=0))
    plt.setp(ax_aux.get_legend().get_texts(), fontsize=Util.SIZE_LEGEND_TEXT)  # for legend text
    plt.setp(ax_aux.get_legend().get_title(), fontsize=Util.SIZE_LEGEND_TITLE)  # for legend title

    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ3_pairPlot.pdf',
                bbox_inches="tight")
    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ3_pairPlot.png',
                bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()

def pairPlotRatioOfMethodsxCoverage():
    g = sns.lmplot(data=df_RQ,
                      x='NEBTM/NTM', y='NCTS/NTS', hue="platform",   fit_reg=False, palette=Util.COLOR_PALETTE_COLORFUL, legend=False,  markers=["o", "x", "+"], hue_order=Util.FIGURE_ORDER)
    #col="platform"
    #plt.tight_layout()
    ax_aux = g.axes[0, 0]
    ax_aux.legend(title="", loc="upper center", bbox_to_anchor=(0.5, 1.1), ncol=3, frameon=False)
    ax_aux.set_xlabel('NEBTM/NTM', fontsize=Util.SIZE_AXES_LABELS)
    ax_aux.set_ylabel('Throw Statement Line Coverage', fontsize=Util.SIZE_AXES_LABELS)
    ax_aux.xaxis.set_major_formatter(ticker.PercentFormatter(xmax=1, decimals=0))
    ax_aux.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1, decimals=0))
    plt.setp(ax_aux.get_legend().get_texts(), fontsize=Util.SIZE_LEGEND_TEXT)  # for legend text
    plt.setp(ax_aux.get_legend().get_title(), fontsize=Util.SIZE_LEGEND_TITLE)  # for legend title

    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ3_pairPlotTestMethodsCoverage.pdf',
                bbox_inches="tight")
    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ3_pairPlotTestMethodsCoverage.png',
                bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()


def pairPlotTestedExceptionsxCoverage():
    g = sns.lmplot(data=df_RQ,
                      x='NDTE/NDUE', y='NCTS/NTS', hue="platform",   fit_reg=False, palette=Util.COLOR_PALETTE_COLORFUL, legend=False,  markers=["o", "x", "+"], hue_order=Util.FIGURE_ORDER)
    #col="platform"
    #plt.tight_layout()
    ax_aux = g.axes[0, 0]
    ax_aux.legend(title="", loc="upper center", bbox_to_anchor=(0.5, 1.1), ncol=3, frameon=False)
    ax_aux.set_xlabel('NDTE/NDUE', fontsize=Util.SIZE_AXES_LABELS)
    ax_aux.set_ylabel('Throw Statement Line Coverage', fontsize=Util.SIZE_AXES_LABELS)
    ax_aux.xaxis.set_major_formatter(ticker.PercentFormatter(xmax=1, decimals=0))
    ax_aux.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1, decimals=0))
    plt.setp(ax_aux.get_legend().get_texts(), fontsize=Util.SIZE_LEGEND_TEXT)  # for legend text
    plt.setp(ax_aux.get_legend().get_title(), fontsize=Util.SIZE_LEGEND_TITLE)  # for legend title

    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ3_pairPlotTestedExceptionsxCoverage.pdf',
                bbox_inches="tight")
    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ3_pairPlotTestedExceptionsxCoverage.png',
                bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()

def barPlotCoverages():
    f, ax = plt.subplots(figsize=(5, 10))
    df_sorted = df_RQ.sort_values("tagCoverage", ascending=False)
    #sns.set_color_codes("muted")
    sns.barplot(data=df_sorted,
                      x='tagCoverage', y='project', color='#494848', label='Line Coverage')

    #sns.set_color_codes("pastel")
    kwargs = {'alpha': 0.7}
    sns.barplot(data=df_sorted,
                      x='NCTS/NTS', y='project', color='#D4D4D4', **kwargs, label='Throw Statement Line Coverage')

    ax.legend(title="", loc="upper center", bbox_to_anchor=(0.5, 1.03), ncol=2, frameon=False)
    #ax.set_xlabel('NCTS/NTS', fontsize=Util.SIZE_AXES_LABELS)
    ax.set_xlabel('', fontsize=Util.SIZE_AXES_LABELS)
    ax.set_ylabel('', fontsize=Util.SIZE_AXES_LABELS)
    #ax.set_ylabel('Line Coverage', fontsize=Util.SIZE_AXES_LABELS)
    ax.get_xaxis().set_tick_params(direction='out', labelsize=Util.SIZE_AXES_VALUES, gridOn=True)
    ax.xaxis.set_ticks_position('bottom')
    ax.xaxis.set_major_formatter(ticker.PercentFormatter(xmax=1, decimals=0))

    ytickslabels = []
    for p in ax.get_yticklabels():
        flag = ''
        platformAux = df_RQ.loc[df_RQ['project'] == p.get_text(), ['platform']].values[0][0]
        if platformAux == 'Desktop/Server':
            flag = '*'
        elif platformAux == 'Mobile':
            flag = '**'
        elif platformAux == 'Multi-platform':
            flag = '***'
        else:
            flag = '???'
        ytickslabels.append(p.get_text() + flag)
    ax.set_yticklabels(ytickslabels)

    #ax.text(0.73, 45.3, '*  Desktop/Server\n** Mobile\n***Multi-platform', style='italic', fontsize=Util.SIZE_AXES_VALUES,
    ax.text(0.73, 45.45, '*  Desktop/Server\n** Mobile\n***Multi-platform', style='italic', fontsize=Util.SIZE_AXES_VALUES,
            bbox={'facecolor': 'gray', 'alpha': 0.2, 'pad': 10})


    plt.setp(ax.get_legend().get_texts(), fontsize=Util.SIZE_LEGEND_TEXT)  # for legend text
    plt.setp(ax.get_legend().get_title(), fontsize=Util.SIZE_LEGEND_TITLE)  # for legend title
    #sns.despine(left=False, right=True)

    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ3_barPlotCoverageRatios.pdf',
                bbox_inches="tight")
    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ3_barPlotCoverageRatios.png',
                bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()

def barPlotCoveragesSideBySide():
    f, ax = plt.subplots(figsize=(5, 10))
    df_sorted = df_RQ.sort_values('tagCoverage', ascending=False)
    #df_aux = df_sorted[['project', 'tagCoverage', 'NCTS/NTS']].set_index('project')
    df_sorted.rename(columns={'tagCoverage': 'Line Coverage', 'NCTS/NTS': 'Throw Statement Line Coverage'}, inplace=True)
    df_aux = df_sorted.melt(id_vars='project', value_vars=['Line Coverage', 'Throw Statement Line Coverage'])


    sns.barplot(data=df_aux,
                       x='value', y='project', hue='variable', palette=['#494848', '#B4B4B4'])

    # #sns.set_color_codes("muted")
    # sns.barplot(data=df_sorted,
    #                   x='tagCoverage', y='project', color='#494848', label='Line Coverage')
    #
    # #sns.set_color_codes("pastel")
    # kwargs = {'alpha': 0.7}
    # sns.barplot(data=df_sorted,
    #                   x='NCTS/NTS', y='project', color='#D4D4D4', **kwargs, label='Throw Statements Line Coverage')

    ax.legend(title="", loc="upper center", bbox_to_anchor=(0.5, 1.03), ncol=2, frameon=False)
    ax.set_xlabel('', fontsize=Util.SIZE_AXES_LABELS)
    ax.set_ylabel('', fontsize=Util.SIZE_AXES_LABELS)
    #ax.set_ylabel('Line Coverage', fontsize=Util.SIZE_AXES_LABELS)
    ax.get_xaxis().set_tick_params(direction='out', labelsize=Util.SIZE_AXES_VALUES, gridOn=True)
    ax.xaxis.set_ticks_position('bottom')
    ax.xaxis.set_major_formatter(ticker.PercentFormatter(xmax=1, decimals=0))

    ytickslabels = []
    for p in ax.get_yticklabels():
        flag = ''
        platformAux = df_RQ.loc[df_RQ['project'] == p.get_text(), ['platform']].values[0][0]
        if platformAux == 'Desktop/Server':
            flag = '*'
        elif platformAux == 'Mobile':
            flag = '**'
        elif platformAux == 'Multi-platform':
            flag = '***'
        else:
            flag = '???'
        ytickslabels.append(p.get_text() + flag)
    ax.set_yticklabels(ytickslabels)

    #ax.text(0.73, 45.3, '*  Desktop/Server\n** Mobile\n***Multi-platform', style='italic', fontsize=Util.SIZE_AXES_VALUES,
    ax.text(0.73, 37.65, '*  Desktop/Server\n** Mobile\n***Multi-platform', style='italic', fontsize=Util.SIZE_AXES_VALUES,
            bbox={'facecolor': 'gray', 'alpha': 0.2, 'pad': 10})


    ax.get_legend
    plt.setp(ax.get_legend().get_texts(), fontsize=Util.SIZE_LEGEND_TEXT)  # for legend text
    plt.setp(ax.get_legend().get_title(), fontsize=Util.SIZE_LEGEND_TITLE)  # for legend title
    #sns.despine(left=False, right=True)

    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ3_barPlotCoverageRatios_sideBySide.pdf',
                bbox_inches="tight")
    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ3_barPlotCoverageRatios_sideBySide.png',
                bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()

def barPlotCoverages():
    f, ax = plt.subplots(figsize=(5, 10))
    df_sorted = df_RQ.sort_values("tagCoverage", ascending=False)
    #sns.set_color_codes("muted")
    sns.barplot(data=df_sorted,
                      x='tagCoverage', y='project', color='#494848', label='Line Coverage')

    #sns.set_color_codes("pastel")
    kwargs = {'alpha': 0.7}
    sns.barplot(data=df_sorted,
                      x='NCTS/NTS', y='project', color='#D4D4D4', **kwargs, label='Throw Statement Line Coverage')

    ax.legend(title="", loc="upper center", bbox_to_anchor=(0.5, 1.03), ncol=2, frameon=False)
    #ax.set_xlabel('NCTS/NTS', fontsize=Util.SIZE_AXES_LABELS)
    ax.set_xlabel('', fontsize=Util.SIZE_AXES_LABELS)
    ax.set_ylabel('', fontsize=Util.SIZE_AXES_LABELS)
    #ax.set_ylabel('Line Coverage', fontsize=Util.SIZE_AXES_LABELS)
    ax.get_xaxis().set_tick_params(direction='out', labelsize=Util.SIZE_AXES_VALUES, gridOn=True)
    ax.xaxis.set_ticks_position('bottom')
    ax.xaxis.set_major_formatter(ticker.PercentFormatter(xmax=1, decimals=0))

    ytickslabels = []
    for p in ax.get_yticklabels():
        flag = ''
        platformAux = df_RQ.loc[df_RQ['project'] == p.get_text(), ['platform']].values[0][0]
        if platformAux == 'Desktop/Server':
            flag = '*'
        elif platformAux == 'Mobile':
            flag = '**'
        elif platformAux == 'Multi-platform':
            flag = '***'
        else:
            flag = '???'
        ytickslabels.append(p.get_text() + flag)
    ax.set_yticklabels(ytickslabels)

    #ax.text(0.73, 45.3, '*  Desktop/Server\n** Mobile\n***Multi-platform', style='italic', fontsize=Util.SIZE_AXES_VALUES,
    ax.text(0.73, 45.45, '*  Desktop/Server\n** Mobile\n***Multi-platform', style='italic', fontsize=Util.SIZE_AXES_VALUES,
            bbox={'facecolor': 'gray', 'alpha': 0.2, 'pad': 10})


    plt.setp(ax.get_legend().get_texts(), fontsize=Util.SIZE_LEGEND_TEXT)  # for legend text
    plt.setp(ax.get_legend().get_title(), fontsize=Util.SIZE_LEGEND_TITLE)  # for legend title
    #sns.despine(left=False, right=True)

    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ3_barPlotCoverageRatios.pdf',
                bbox_inches="tight")
    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ3_barPlotCoverageRatios.png',
                bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()


def coveredThrowStatementsRatio_histogram():
    bins = np.arange(0, 1, 0.2)
    g = sns.FacetGrid(df_RQ, sharex=False)
    g = (g.map(sns.distplot, "NCTS/NTS", kde=False, rug=True, bins=bins, color="#494848")).set(xticks=[0.0, 0.2, 0.4, 0.6, 0.8, 1])
    for ax in g.axes.flat:
        # ax.get_yaxis().set_tick_params(labelsize='x-large', which="major")
        # labels ao redor dos graficos
        # ax.set_xlabel(ax.get_xlabel(), fontsize='20')
        ax.set_xlabel('Throw Statement Line Coverage', fontsize=Util.SIZE_AXES_LABELS)
        ax.set_ylabel(ax.get_ylabel(), fontsize=Util.SIZE_AXES_LABELS)

        # títulos em cima dos graficos
        if ax.get_title():
            ax.set_title(ax.get_title().split('=')[1],
                         fontsize=Util.SIZE_AXES_TITLE)

        ax.yaxis.grid(True, linewidth=1, which="major")
        ax.get_yaxis().set_tick_params(labelsize=Util.SIZE_AXES_TITLE, which="major")
        ax.get_xaxis().set_tick_params(direction='out', labelsize=Util.SIZE_AXES_TITLE)
        ax.xaxis.set_major_formatter(ticker.PercentFormatter(xmax=1, decimals=0))
    plt.tight_layout()
    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ3_coveredThrowStatementsRatio_histogram.png',
                bbox_inches="tight")
    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ3_coveredThrowStatementsRatio_histogram.pdf', bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()

 ############ RQ4 ####################

def violinPlotRatio_NTSCE_NTS():
    f.write("\n\n ##############  RQ4 - PART 1 ##############\n")

    fig = plt.subplots(figsize=(6, 2))
    gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1.5], wspace=.02, hspace=.05)
    ax0 = plt.subplot(gs[0])
    ax1 = plt.subplot(gs[1])
    sns.violinplot(x="domain", y="NTSCE/NTS", data=df_RQ, cut=0, inner="box", hue="platform",
                   hue_order=Util.FIGURE_ORDER, scale="width",
                   palette=Util.COLOR_PALETTE, linewidth=1.5, ax=ax0, saturation=1)
    sns.violinplot(x="platform", y="NTSCE/NTS", data=df_RQ, cut=0, inner="box", scale="width",
                   order=Util.FIGURE_ORDER,
                   palette=Util.COLOR_PALETTE, linewidth=1.5, ax=ax1, saturation=1)
    ax0.set(xlabel='', ylabel='', title='', yticks=[0, 0.2, 0.4, 0.6, 0.8, 1])
    ax0.set_ylabel(ax0.get_ylabel(), fontsize=Util.SIZE_AXES_LABELS)

    ax0.legend(title="", loc="upper center", bbox_to_anchor=(0.75, 1.20), ncol=3, frameon=False)
    ax0.yaxis.grid(True, linewidth=1, which="major")
    plt.setp(ax0.get_legend().get_texts(), fontsize=Util.SIZE_LEGEND_TEXT)  # for legend text
    plt.setp(ax0.get_legend().get_title(), fontsize=Util.SIZE_LEGEND_TITLE)  # for legend title
    ax0.get_yaxis().set_tick_params(labelsize=Util.SIZE_AXES_VALUES, which="major")
    ax0.get_xaxis().set_tick_params(direction='out', labelsize=Util.SIZE_AXES_VALUES)
    ax0.xaxis.set_ticks_position('bottom')
    ax0.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1, decimals=0))

    ax1.set(xlabel='', ylabel='', title='', xticks=[1], yticks=[0, 0.2, 0.4, 0.6, 0.8, 1])
    ax1.set_xticklabels(['All'])
    ax1.yaxis.grid(True, linewidth=1, which="major")
    ax1.get_yaxis().set_tick_params(labelsize=Util.SIZE_AXES_VALUES, which="major")
    ax1.get_xaxis().set_tick_params(direction='out', labelsize=Util.SIZE_AXES_VALUES)
    ax1.xaxis.set_ticks_position('bottom')
    ax1.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1, decimals=0))
    ax1.set_yticklabels([])
    # Show graphic
    plt.tight_layout()
    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ4_NTSCE_NTS_platform.pdf',
                bbox_inches="tight")
    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ4_NTSCE_NTS_platform.png',
                bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()

def violinPlotRatio_NTSSTPE_NTS():
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
    df_withoutNaN = df_RQ.dropna(subset=['NTSCE/NTS'])
    sns.violinplot(x="domain", y="NTSSTPE/NTS", data=df_RQ, cut=0, inner="box", hue="platform",
                   hue_order=Util.FIGURE_ORDER, scale="width",
                   palette=Util.COLOR_PALETTE, linewidth=1.5, ax=ax0, saturation=1)
    sns.violinplot(x="platform", y="NTSSTPE/NTS", data=df_RQ, cut=0, inner="box", scale="width",
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
    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ4_NTSSTPE_NTS_platform.pdf',
                bbox_inches="tight")
    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ4_NTSSTPE_NTS_platform.png',
                bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()


def countProjectsWhere_NTSCE_RATIO_isBigger(df_aux):
    df_clean = df_aux[(df_aux['NTSCE/NTS'] > df_aux['NTSSTPE/NTS'])]
    f.write(f'Number of projects where NTSCE/NTS > NTSSTPE/NTS = {len(df_clean)} :  {df_clean["project"].values.tolist()}\n')

def violinPlotRatio_NTSCE_NTS_NTSSTPE_NTS_MELTED():
    fig, ax = plt.subplots(figsize=(6, 2))
    countProjectsWhere_NTSCE_RATIO_isBigger(df_RQ.dropna(subset=['project', 'NTSCE/NTS', 'NTSSTPE/NTS']))

    df_withoutNaN = df_RQ.dropna(subset=['NTSCE/NTS', 'NTSSTPE/NTS'])
    df_melted = pd.melt(df_withoutNaN, id_vars=["project", "platform"], value_vars=['NTSCE/NTS', 'NTSSTPE/NTS'])
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
    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ4_NTSCE_NTS_NTSSTPE_NTS_MELTED_platform.pdf',
                bbox_inches="tight")
    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ4_NTSCE_NTS_NTSSTPE_NTS_MELTED_platform.png',
                bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()
############################## RQ4 - PART 2 ##############################
def violinPlotRatio_NCTSCE_NCTS():
    f.write("\n\n ##############  RQ4 - PART 2 ##############\n")
    df_totalSize = len(df_RQ)
    df_aux = df_RQ[(df_RQ['NCTSCE/NCTS'] < 0.5)]
    df_auxSize = len(df_aux)
    f.write(f'Number of projects where NCTSCE/NCTS < 0.5 = {df_auxSize} out of {df_totalSize} ({round(df_auxSize/df_totalSize*100,2)})\n')
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
    df_withoutNaN = df_RQ.dropna(subset=['NCTSCE/NCTS'])
    sns.violinplot(x="domain", y="NCTSCE/NCTS", data=df_RQ, cut=0, inner="box", hue="platform",
                   hue_order=Util.FIGURE_ORDER, scale="width",
                   palette=Util.COLOR_PALETTE, linewidth=1.5, ax=ax0, saturation=1)
    sns.violinplot(x="platform", y="NCTSCE/NCTS", data=df_RQ, cut=0, inner="box", scale="width",
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
    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ4_NCTSCE_NCTS_platform.pdf',
                bbox_inches="tight")
    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ4_NCTSCE_NCTS_platform.png',
                bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()

def violinPlotRatio_NCTSSTPE_NCTS():
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
    df_withoutNaN = df_RQ.dropna(subset=['NCTSSTPE/NCTS'])
    sns.violinplot(x="domain", y="NCTSSTPE/NCTS", data=df_RQ, cut=0, inner="box", hue="platform",
                   hue_order=Util.FIGURE_ORDER, scale="width",
                   palette=Util.COLOR_PALETTE, linewidth=1.5, ax=ax0, saturation=1)
    sns.violinplot(x="platform", y="NCTSSTPE/NCTS", data=df_RQ, cut=0, inner="box", scale="width",
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
    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ4_NCTSSTPE_NCTS_platform.pdf',
                bbox_inches="tight")
    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ4_NCTSSTPE_NCTS_platform.png',
                bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()



def violinPlotRatio_NCTSCE_NCTS_NCTSSTPE_NCTS_MELTED():
    fig, ax = plt.subplots(figsize=(6, 2))
    df_withoutNaN = df_RQ.dropna(subset=['NCTSCE/NCTS', 'NCTSSTPE/NCTS'])

    df_melted = pd.melt(df_withoutNaN, id_vars=["project", "platform"], value_vars=['NCTSCE/NCTS', 'NCTSSTPE/NCTS'])
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
    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ4_NCTSCE_NCTS_NCTSSTPE_NCTS_MELTED_platform.pdf',
                bbox_inches="tight")
    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ4_NCTSCE_NCTS_NCTSSTPE_NCTS_MELTED_platform.png',
                bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()
############################## RQ4 - PART 3 ##############################
def calculate_NCTSCE_NTSCE_and_NCTSSTPE_NTSSTPE_ratio(df_aux, column1, column2, description):
    df = df_aux.dropna(subset=['project', column1, column2])
    df_higherThan = df[(df[column1] > df[column2])]
    dfTotalSize = len(df)
    dfHigherThanSize = len(df_higherThan)
    if dfTotalSize == 0:
        f.write(
            f'{description}_NCTSCE/NTSCE > NCTSSTPE/NTSSTPE: {dfHigherThanSize} out of {dfTotalSize})\n')
    else:
        f.write(f'{description}_NCTSCE/NTSCE > NCTSSTPE/NTSSTPE: {dfHigherThanSize} out of {dfTotalSize} ({round(dfHigherThanSize/dfTotalSize*100,2)})\n')


def countProjectsWhere_NCTSCE_NTSCE_and_NCTSSTPE_NTSSTPE_isHigherThanFiftyPercent(df_aux):
    df_clean = df_aux[(df_aux['NCTSCE/NTSCE'] > 0.5) & (df_aux['NCTSSTPE/NTSSTPE'] > 0.5)]
    f.write(f'Number of projects where NCTSCE/NTSCE and NCTSSTPE_NTSSTPE is higher than 50% = {len(df_clean)} out of {len(df_aux)} : {df_clean["project"].values.tolist()} ({round(len(df_clean)/len(df_aux)*100,2)}%)\n')


def violinPlotRatio_NCTSCE_NTSCE():
    f.write("\n\n ##############  RQ4 - PART 3 ##############\n")
    platformList = df_RQ["platform"].unique()
    domainList = df_RQ["domain"].unique()

    df_aux = df_RQ

    #countProjectsWhere_NCTSCE_NTSCE_and_NCTSSTPE_NTSSTPE_isHigherThanFiftyPercent(df_aux.dropna(subset=['project', 'NCTSCE/NTSCE', 'NCTSSTPE/NTSSTPE']))
    countProjectsWhere_NCTSCE_NTSCE_and_NCTSSTPE_NTSSTPE_isHigherThanFiftyPercent(df_aux)
    calculate_NCTSCE_NTSCE_and_NCTSSTPE_NTSSTPE_ratio(df_aux, 'NCTSCE/NTSCE', 'NCTSSTPE/NTSSTPE', "Total")
    for platform in platformList:
        df_platform = df_aux[(df_aux['platform'] == platform)]
        calculate_NCTSCE_NTSCE_and_NCTSSTPE_NTSSTPE_ratio(df_platform, 'NCTSCE/NTSCE', 'NCTSSTPE/NTSSTPE', platform)
        for domain in domainList:
            df_domain = df_platform[(df_platform['domain'] == domain)]
            calculate_NCTSCE_NTSCE_and_NCTSSTPE_NTSSTPE_ratio(df_domain, 'NCTSCE/NTSCE', 'NCTSSTPE/NTSSTPE', f'{platform}_{domain}')

    #Util.evaluateOutliersIQR(df_aux, 'NCTSCE/NTSCE')
    fig = plt.subplots(figsize=(6, 2))
    gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1.5], wspace=.02, hspace=.05)
    ax0 = plt.subplot(gs[0])
    ax1 = plt.subplot(gs[1])
    df_withoutNaN = df_aux.dropna(subset=['NCTSCE/NTSCE'])
    sns.violinplot(x="domain", y="NCTSCE/NTSCE", data=df_aux, cut=0, inner="box", hue="platform",
                   hue_order=Util.FIGURE_ORDER, scale="width",
                   palette=Util.COLOR_PALETTE, linewidth=1.5, ax=ax0, saturation=1)
    sns.violinplot(x="platform", y="NCTSCE/NTSCE", data=df_aux, cut=0, inner="box", scale="width",
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
    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ4_NCTSCE_NTSCE_platform.pdf',
                bbox_inches="tight")
    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ4_NCTSCE_NTSCE_platform.png',
                bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()


def violinPlotRatio_NCTSSTPE_NTSSTPE():
    platformList = df_RQ["platform"].unique()
    domainList = df_RQ["domain"].unique()

    fig = plt.subplots(figsize=(6, 2))
    gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1.5], wspace=.02, hspace=.05)
    ax0 = plt.subplot(gs[0])
    ax1 = plt.subplot(gs[1])
    df_withoutNaN = df_RQ.dropna(subset=['NCTSSTPE/NTSSTPE'])
    sns.violinplot(x="domain", y="NCTSSTPE/NTSSTPE", data=df_RQ, cut=0, inner="box", hue="platform",
                   hue_order=Util.FIGURE_ORDER, scale="width",
                   palette=Util.COLOR_PALETTE, linewidth=1.5, ax=ax0, saturation=1)
    sns.violinplot(x="platform", y="NCTSSTPE/NTSSTPE", data=df_RQ, cut=0, inner="box", scale="width",
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
    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ4_NCTSSTPE_NTSSTPE_platform.pdf',
                bbox_inches="tight")
    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ4_NCTSSTPE_NTSSTPE_platform.png',
                bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()


########################################END #####################

def evaluateStatistics():
    platformList = df_RQ["platform"].unique()

    for platform in platformList:
        df_platform = df_RQ[(df_RQ['platform'] == platform)]
        StatisticalTests.compareDataSamples(df_platform["NCTSCE/NTSCE"].dropna(), df_platform["NCTSSTPE/NTSSTPE"].dropna(),
                                         platform.replace("/", "_") + "_NCTSCE_NTSCE_And_NCTSSTPE_NTSSTPE", "RQs/RQ3/statistics/")

##################################################################
generateDataSet()



#RQ3-PROJECTS
barPlotNumberOfProjects()
violinPlotTagCoverage()
pairPlotCoverages()
barPlotCoverages()
barPlotCoveragesSideBySide()

#RQ3
violinPlotRatio_NCTS_NTS()
#violinPlotRatio_Overall_NCTS_NTS()
pairPlotRatioOfMethodsxCoverage()
pairPlotTestedExceptionsxCoverage()
coveredThrowStatementsRatio_histogram()


# RQ4-PART1
violinPlotRatio_NTSCE_NTS()
violinPlotRatio_NTSSTPE_NTS()
violinPlotRatio_NTSCE_NTS_NTSSTPE_NTS_MELTED()

# RQ4-PART2
violinPlotRatio_NCTSCE_NCTS()
violinPlotRatio_NCTSSTPE_NCTS()
violinPlotRatio_NCTSCE_NCTS_NCTSSTPE_NCTS_MELTED()

# RQ3-PART3
violinPlotRatio_NCTSCE_NTSCE()
violinPlotRatio_NCTSSTPE_NTSSTPE()


#StatisticalTests
#evaluateStatistics()

