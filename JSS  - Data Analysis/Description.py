import os
import math
from pathlib import Path
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from matplotlib import gridspec
import pandas as pd
import seaborn as sns
from matplotlib.ticker import (MultipleLocator)
from pymongo import MongoClient

from main import Util

np.warnings.filterwarnings('ignore')

sns.set_context("paper")
sns.set_style("whitegrid")
# sns.despine()

SHOW_FIGURE = False

df_RQ = ""

RQ_NUMBER = "description"
OUTPUT_PATH = "RQS/" + RQ_NUMBER
OUTPUT_FIGURES_PATH = Util.create_new_dirs(OUTPUT_PATH + "/figures/")

fileName = "res_"+RQ_NUMBER+".txt"
f = open(Path(OUTPUT_PATH) / fileName, "w+")

CUSTOM_SIZE_Y_AXES_VALUES = "large"
CUSTOM_SIZE_X_AXES_VALUES = 10


############################## TABLE GENERATION ##############################
def generateDataSetDescription():
    global df_RQ
    dataSet = []
    for doc in Util.mongo_collection.find():

        today = datetime.now()
        project = doc["projectName"]
        tagCreatedOn = datetime.strptime(doc["tagCreatedAt"], '%d/%m/%Y %H:%M:%S')
        tagLastUpdatedAt = datetime.strptime(doc["projectDetails"]["lastUpdatedAt"], '%d/%m/%Y %H:%M:%S')
        tagLastUpdateMonths = Util.calculate_month_delta(tagLastUpdatedAt, today)
        tagMonths = Util.calculate_month_delta(tagCreatedOn, today)
        projectCreatedOn = datetime.strptime(doc["projectDetails"]["createdAt"], '%d/%m/%Y %H:%M:%S')
        projectMonths = Util.calculate_month_delta(projectCreatedOn, today)
        platform = doc['projectDetails']["platform"]
        domain = Util.adjust_domain_name(doc['projectDetails']["domain"])
        stars = doc['projectDetails']["stars"]
        loc = doc['projectDetails']["LOC"]
        meanOfCommitsJulToSep2019 = doc['projectDetails']["meanOfCommitsJulToSep2019"]
        contributors = doc['projectDetails']["contributors"]
        NTM = doc["statistics"]['totalNumberOfTestMethods']

        dataSetAux = [project, tagCreatedOn, tagMonths,  projectCreatedOn, projectMonths, tagLastUpdatedAt, tagLastUpdateMonths,meanOfCommitsJulToSep2019, platform, domain, stars, loc,
                      contributors, NTM]
        dataSet.append(dataSetAux)

    df_RQ = pd.DataFrame(dataSet,
                         columns=['project', 'tagCreatedOn', 'tagMonths', 'projectCreatedOn', 'projectMonths','tagLastUpdatedAt', 'tagLastUpdateMonths', 'meanOfCommitsJulToSep2019', 'platform', 'domain', 'stars', 'loc',
                                  'contributors', 'NTM'])

    df_RQ['log10(stars)'] = np.log10(df_RQ['stars'])
    df_RQ['log10(NTM)'] = np.log10(df_RQ['NTM'])
    df_RQ['log10(loc)'] = np.log10(df_RQ['loc'])


def barPlotNumberOfProjects():
    platformList = df_RQ["platform"].unique()
    domainList = df_RQ["domain"].unique()
    sns.set_style("whitegrid")
    fig = plt.subplots(figsize=(6, 3))
    gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1.5], wspace=.02, hspace=.05)
    ax0 = plt.subplot(gs[0])
    ax1 = plt.subplot(gs[1])
    sns.countplot(x="domain", data=df_RQ, hue="platform",
                   hue_order=Util.FIGURE_ORDER,
                   palette=Util.COLOR_PALETTE, ax=ax0, saturation=1)
    sns.countplot(x="platform", data=df_RQ,
                   order=Util.FIGURE_ORDER,
                   palette=Util.COLOR_PALETTE, ax=ax1, saturation=1)

    for p in ax0.patches:
        height = p.get_height()
        ax0.text(p.get_x() + p.get_width() / 2., height + 0.1, height, ha="center", fontsize=Util.SIZE_BAR_VALUES)

    for p in ax1.patches:
        height = p.get_height()
        ax1.text(p.get_x() + p.get_width() / 2., height + 0.1, height, ha="center", fontsize=Util.SIZE_BAR_VALUES)

    ax0.set(xlabel='', ylabel='', title='')
    ax0.set_ylabel(ax0.get_ylabel(), fontsize=Util.SIZE_AXES_LABELS)
    # ax0.set_ylim(0, 0.4)
    # ax0.legend(title="", loc="upper center")
    ax0.legend(title="", loc="upper center", bbox_to_anchor=(0.75, 1.12), ncol=3, frameon=False)
    ax0.yaxis.grid(True, linewidth=1, which="major")
    plt.setp(ax0.get_legend().get_texts(), fontsize=Util.SIZE_LEGEND_TEXT)  # for legend text
    plt.setp(ax0.get_legend().get_title(), fontsize=Util.SIZE_LEGEND_TITLE)  # for legend title
    ax0.get_yaxis().set_tick_params(labelsize=Util.SIZE_AXES_VALUES, which="major")
    ax0.get_xaxis().set_tick_params(direction='out', labelsize=Util.SIZE_AXES_VALUES)
    ax0.xaxis.set_ticks_position('bottom')

    ax1.set(xlabel='', ylabel='', title='', xticks=[1])
    # ax1.set_xticks(5)
    ax1.set_xticklabels(['All'])
    ax1.yaxis.grid(True, linewidth=0, which="major")
    ax1.get_yaxis().set_tick_params(labelsize=Util.SIZE_AXES_VALUES, which="major")
    ax1.get_xaxis().set_tick_params(direction='out', labelsize=Util.SIZE_AXES_VALUES)
    ax1.xaxis.set_ticks_position('bottom')
    ax1.set_yticklabels([])
    # Show graphic
    #plt.tight_layout()
    plt.savefig(OUTPUT_FIGURES_PATH / 'count_domain.pdf')
    plt.savefig(OUTPUT_FIGURES_PATH / 'count_domain.png')
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()

def barPlotNumberOfProjectsSemTotal():
    platformList = df_RQ["platform"].unique()
    domainList = df_RQ["domain"].unique()
    sns.set_style("whitegrid")
    fig, ax = plt.subplots(figsize=(6, 3))
    sns.countplot(x="domain", data=df_RQ, hue="platform",
                   hue_order=Util.FIGURE_ORDER,
                   palette=Util.COLOR_PALETTE, ax=ax, saturation=1)

    ax.set(xlabel='', ylabel='', title='')
    ax.set_ylabel(ax.get_ylabel(), fontsize=CUSTOM_SIZE_Y_AXES_VALUES)
    # ax.set_ylim(0, 0.4)
    # ax.legend(title="", loc="upper center")
    ax.legend(title="", loc="upper center", bbox_to_anchor=(0.5, 1.12), ncol=3, frameon=False)
    ax.yaxis.grid(True, linewidth=1, which="major")
    plt.setp(ax.get_legend().get_texts(), fontsize=Util.SIZE_LEGEND_TEXT)  # for legend text
    plt.setp(ax.get_legend().get_title(), fontsize=Util.SIZE_LEGEND_TITLE)  # for legend title
    ax.get_yaxis().set_tick_params(labelsize=CUSTOM_SIZE_Y_AXES_VALUES, which="major")
    ax.get_xaxis().set_tick_params(direction='out', labelsize=CUSTOM_SIZE_X_AXES_VALUES)
    ax.xaxis.set_ticks_position('bottom')
    # Show graphic
    #plt.tight_layout()
    plt.savefig(OUTPUT_FIGURES_PATH / 'Description_Total_bydomain.pdf')
    plt.savefig(OUTPUT_FIGURES_PATH / 'Description_Total_bydomain.png')
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()


def violinPlotTagAge():
    platformList = df_RQ["platform"].unique()
    domainList = df_RQ["domain"].unique()

    fig, ax = plt.subplots(figsize=(3, 3))
    sns.violinplot(x="platform", y="tagMonths", data=df_RQ, cut=0, inner="box", scale="width",
                   order=Util.FIGURE_ORDER,
                   palette=Util.COLOR_PALETTE, linewidth=1.5, ax=ax, saturation=1)
    ax.set(xlabel='', ylabel='Version Age (months)', title='')
    ax.set_ylabel(ax.get_ylabel(), fontsize=CUSTOM_SIZE_Y_AXES_VALUES)
    ax.yaxis.grid(True, linewidth=1, which="major")
    ax.get_yaxis().set_tick_params(labelsize=CUSTOM_SIZE_Y_AXES_VALUES, which="major")
    ax.get_xaxis().set_tick_params(direction='out', labelsize=CUSTOM_SIZE_X_AXES_VALUES)
    ax.xaxis.set_ticks_position('bottom')
    # Show graphic
    plt.tight_layout()
    plt.savefig(OUTPUT_FIGURES_PATH / 'Description_TagAge.pdf',
                bbox_inches="tight")
    plt.savefig(OUTPUT_FIGURES_PATH / 'Description_TagAge.png',
                bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()

def violinPlotMonthsSinceLastUpdate():
    platformList = df_RQ["platform"].unique()
    domainList = df_RQ["domain"].unique()

    fig, ax = plt.subplots(figsize=(3, 3))
    sns.violinplot(x="platform", y="tagLastUpdateMonths", data=df_RQ, cut=0, inner="box", scale="width",
                   order=Util.FIGURE_ORDER,
                   palette=Util.COLOR_PALETTE, linewidth=1.5, ax=ax, saturation=1)
    ax.set(xlabel='', ylabel='Months', title='')
    ax.set_ylabel(ax.get_ylabel(), fontsize=CUSTOM_SIZE_Y_AXES_VALUES)
    ax.yaxis.grid(True, linewidth=1, which="major")
    ax.get_yaxis().set_tick_params(labelsize=CUSTOM_SIZE_Y_AXES_VALUES, which="major")
    ax.get_xaxis().set_tick_params(direction='out', labelsize=CUSTOM_SIZE_X_AXES_VALUES)
    ax.xaxis.set_ticks_position('bottom')
    # Show graphic
    plt.tight_layout()
    plt.savefig(OUTPUT_FIGURES_PATH / 'Description_LastUpdate.pdf',
                bbox_inches="tight")
    plt.savefig(OUTPUT_FIGURES_PATH / 'Description_LastUpdate.png',
                bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()

def violinPlotProjectAge():
    platformList = df_RQ["platform"].unique()
    domainList = df_RQ["domain"].unique()

    fig, ax = plt.subplots(figsize=(3, 3))
    sns.violinplot(x="platform", y="projectMonths", data=df_RQ, cut=0, inner="box", scale="width",
                   order=Util.FIGURE_ORDER,
                   palette=Util.COLOR_PALETTE, linewidth=1.5, ax=ax, saturation=1)
    ax.set(xlabel='', ylabel='Age (months)', title='')
    ax.set_ylabel(ax.get_ylabel(), fontsize=CUSTOM_SIZE_Y_AXES_VALUES)
    ax.yaxis.grid(True, linewidth=1, which="major")
    ax.get_yaxis().set_tick_params(labelsize=CUSTOM_SIZE_Y_AXES_VALUES, which="major")
    ax.get_xaxis().set_tick_params(direction='out', labelsize=CUSTOM_SIZE_X_AXES_VALUES)
    ax.xaxis.set_ticks_position('bottom')
    # Show graphic
    plt.tight_layout()
    plt.savefig(OUTPUT_FIGURES_PATH / 'Description_RepositoryAge.pdf',
                bbox_inches="tight")
    plt.savefig(OUTPUT_FIGURES_PATH / 'Description_RepositoryAge.png',
                bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()

def violinPlotContributors():
    platformList = df_RQ["platform"].unique()
    domainList = df_RQ["domain"].unique()

    fig, ax = plt.subplots(figsize=(3, 3))
    sns.violinplot(x="platform", y="contributors", data=df_RQ, cut=0, inner="box", scale="width",
                   order=Util.FIGURE_ORDER,
                   palette=Util.COLOR_PALETTE, linewidth=1.5, ax=ax, saturation=1)
    ax.set(xlabel='', ylabel='Contributors', title='')
    ax.set_ylabel(ax.get_ylabel(), fontsize=CUSTOM_SIZE_Y_AXES_VALUES)
    ax.yaxis.grid(True, linewidth=1, which="major")
    ax.get_yaxis().set_tick_params(labelsize=CUSTOM_SIZE_Y_AXES_VALUES, which="major")
    ax.get_xaxis().set_tick_params(direction='out', labelsize=CUSTOM_SIZE_X_AXES_VALUES)
    ax.xaxis.set_ticks_position('bottom')
    # Show graphic
    plt.tight_layout()
    plt.savefig(OUTPUT_FIGURES_PATH / 'Description_Contributors.pdf',
                bbox_inches="tight")
    plt.savefig(OUTPUT_FIGURES_PATH / 'Description_Contributors.png',
                bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()

def violinPlotStars():
    platformList = df_RQ["platform"].unique()
    domainList = df_RQ["domain"].unique()

    fig, ax = plt.subplots(figsize=(3, 3))
    sns.violinplot(x="platform", y="stars", data=df_RQ, cut=0, inner="box", scale="width",
                   order=Util.FIGURE_ORDER,
                   palette=Util.COLOR_PALETTE, linewidth=1.5, ax=ax, saturation=1)
    ax.set(xlabel='', ylabel='Stars', title='')
    ax.set_ylabel(ax.get_ylabel(), fontsize=CUSTOM_SIZE_Y_AXES_VALUES)
    ax.yaxis.grid(True, linewidth=1, which="major")
    ax.get_yaxis().set_tick_params(labelsize=CUSTOM_SIZE_Y_AXES_VALUES, which="major")
    ax.get_xaxis().set_tick_params(direction='out', labelsize=CUSTOM_SIZE_X_AXES_VALUES)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_major_formatter(ticker.EngFormatter())
    #ax.set_yscale('log')
    # Show graphic
    plt.tight_layout()
    plt.savefig(OUTPUT_FIGURES_PATH / 'Description_Stars.pdf',
                bbox_inches="tight")
    plt.savefig(OUTPUT_FIGURES_PATH / 'Description_Stars.png',
                bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()

def violinPlotLOC():
    platformList = df_RQ["platform"].unique()
    domainList = df_RQ["domain"].unique()

    fig, ax = plt.subplots(figsize=(3, 3))
    sns.violinplot(x="platform", y="log10(loc)", data=df_RQ, cut=0, inner="box", scale="width",
                   order=Util.FIGURE_ORDER,
                   palette=Util.COLOR_PALETTE, linewidth=1.5, ax=ax, saturation=1)
    ax.set(xlabel='', ylabel='log10(LOC)', title='')
    ax.set_ylabel(ax.get_ylabel(), fontsize=CUSTOM_SIZE_Y_AXES_VALUES)
    ax.yaxis.grid(True, linewidth=1, which="major")
    ax.get_yaxis().set_tick_params(labelsize=CUSTOM_SIZE_Y_AXES_VALUES, which="major")
    ax.get_xaxis().set_tick_params(direction='out', labelsize=CUSTOM_SIZE_X_AXES_VALUES)
    #ax.yaxis.set_major_formatter(ticker.EngFormatter())
    ax.xaxis.set_ticks_position('bottom')
    #ax.set_yscale('log')
    # Show graphic
    plt.tight_layout()
    plt.savefig(OUTPUT_FIGURES_PATH / 'Description_LOC.pdf',
                bbox_inches="tight")
    plt.savefig(OUTPUT_FIGURES_PATH / 'Description_LOC.png',
                bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()

def violinPlotCommitsMean2019():
    platformList = df_RQ["platform"].unique()
    domainList = df_RQ["domain"].unique()

    fig, ax = plt.subplots(figsize=(3, 3))
    sns.violinplot(x="platform", y="meanOfCommitsJulToSep2019", data=df_RQ, cut=0, inner="box", scale="width",
                   order=Util.FIGURE_ORDER,
                   palette=Util.COLOR_PALETTE, linewidth=1.5, ax=ax, saturation=1)
    ax.set(xlabel='', ylabel='Activity (Jul to Sep)', title='')
    ax.set_ylabel(ax.get_ylabel(), fontsize=CUSTOM_SIZE_Y_AXES_VALUES)
    ax.yaxis.grid(True, linewidth=1, which="major")
    ax.get_yaxis().set_tick_params(labelsize=CUSTOM_SIZE_Y_AXES_VALUES, which="major")
    ax.get_xaxis().set_tick_params(direction='out', labelsize=CUSTOM_SIZE_X_AXES_VALUES)
    ax.yaxis.set_major_formatter(ticker.EngFormatter())
    ax.xaxis.set_ticks_position('bottom')
    #ax.set_yscale('log')
    # Show graphic
    plt.tight_layout()
    plt.savefig(OUTPUT_FIGURES_PATH / 'Description_commitsMean3MonthsIn2019.pdf',
                bbox_inches="tight")
    plt.savefig(OUTPUT_FIGURES_PATH / 'Description_commitsMean3MonthsIn2019.png',
                bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()

def violinPlotNTM():
    platformList = df_RQ["platform"].unique()
    domainList = df_RQ["domain"].unique()

    fig, ax = plt.subplots(figsize=(3, 3))
    sns.violinplot(x="platform", y="log10(NTM)", data=df_RQ, cut=0, inner="box", scale="width",
                   order=Util.FIGURE_ORDER,
                   palette=Util.COLOR_PALETTE, linewidth=1.5, ax=ax, saturation=1,)
    ax.set(xlabel='', ylabel='log10(NTM)', title='')
    ax.set_ylabel(ax.get_ylabel(), fontsize=CUSTOM_SIZE_Y_AXES_VALUES)
    #ax.get_legend().remove()
    ax.yaxis.grid(True, linewidth=1, which="major")
    ax.get_yaxis().set_tick_params(labelsize=CUSTOM_SIZE_Y_AXES_VALUES, which="major")
    ax.get_xaxis().set_tick_params(direction='out', labelsize=CUSTOM_SIZE_X_AXES_VALUES)
    #ax.set_yscale('log')
    #ax.yaxis.set_major_formatter(ticker.EngFormatter())
    ax.xaxis.set_ticks_position('bottom')
    # Show graphic
    plt.tight_layout()
    plt.savefig(OUTPUT_FIGURES_PATH / 'Description_NTM.pdf',
                bbox_inches="tight")
    plt.savefig(OUTPUT_FIGURES_PATH / 'Description_NTM.png',
                bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()


# Generating Tables
generateDataSetDescription()
barPlotNumberOfProjects()
#barPlotNumberOfProjectsSemTotal()


violinPlotTagAge()
violinPlotProjectAge()
violinPlotMonthsSinceLastUpdate()
violinPlotContributors()
violinPlotStars()
violinPlotLOC()
violinPlotCommitsMean2019()

violinPlotNTM()
