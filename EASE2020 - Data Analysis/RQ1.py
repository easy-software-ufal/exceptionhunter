from datetime import datetime

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import gridspec
from scipy import stats

from main import StatisticalTests
from main import Util
from pathlib import Path

np.warnings.filterwarnings('ignore')

sns.set_context("paper")
sns.set_style("whitegrid")
# sns.despine()

SHOW_FIGURE = False
df_RQ = ""
columnsToLatex = ["NEBTM", "NTM", "NEBTM/NTM", "NDUE", "NADTE", "NADTE/NDUE"]
RQ_NUMBER = "RQ1"
OUTPUT_PATH = "RQS/" + RQ_NUMBER
OUTPUT_FIGURES_PATH = Util.create_new_dirs(OUTPUT_PATH + "/figures/")

fileName = "res_"+RQ_NUMBER+".txt"
f = open(Path(OUTPUT_PATH) / fileName, "w+")


# ############################## TABLE GENERATION ##############################
def generateDataSet():

    global df_RQ
    today = datetime.now()
    dataSet = []
    for doc in Util.mongo_collection.find():

        project = doc["projectName"]
        tagCreatedOn = datetime.strptime(doc["tagCreatedAt"], '%d/%m/%Y %H:%M:%S').year
        projectCreatedOn = datetime.strptime(doc["projectDetails"]["createdAt"], '%d/%m/%Y %H:%M:%S').year
        projectMonths = Util.calculate_month_delta(datetime.strptime(doc["projectDetails"]["createdAt"], '%d/%m/%Y %H:%M:%S'), today)
        platform = doc['projectDetails']["platform"]
        domain = Util.adjust_domain_name(doc['projectDetails']["domain"])
        description = "'" + doc['projectDetails']["description"] + "'"
        gitRepo = doc['projectDetails']["gitRepo"]
        stars = doc['projectDetails']["stars"]
        contributors = doc['projectDetails']["contributors"]
        NEBTM = doc["statistics"]['totalNumberOfExceptionalBehaviorTestMethods']
        NTM = doc["statistics"]['totalNumberOfTestMethods']
        NEBTM_NTM = round(np.float64(NEBTM) / np.float64(NTM), 4)
        NADTE = doc["statistics"]['totalNumberOfAllTestedExceptions']
        NDTE = doc["statistics"]['totalNumberOfDistinctTestedExceptions']  # distinct used and tested exceptions
        NDUE = doc["statistics"]['totalNumberOfDistinctUsedExceptions']  # distinct used exceptions
        NEU = doc["statistics"]['totalNumberOfExceptionsUses']  # general number of exceptions
        NADTE_NDUE = round(np.float64(NADTE) / np.float64(NDUE), 4)
        NDTE_NDUE = round(np.float64(NDTE) / np.float64(NDUE), 4)

        dataSetRQ = [project, description, gitRepo, tagCreatedOn, projectCreatedOn, projectMonths, platform, domain, stars,
                      contributors, NEBTM, NTM,
                      NEBTM_NTM, NADTE, NDTE, NDUE, NEU, NADTE_NDUE, NDTE_NDUE]
        dataSet.append(dataSetRQ)

    df_RQ = pd.DataFrame(dataSet,
                         columns=['project', 'description', 'gitRepo', 'tagCreatedOn', 'projectCreatedOn', 'projectMonths', 'platform', 'domain', 'stars',
                                   'contributors', 'NEBTM', 'NTM', 'NEBTM/NTM', 'NADTE', 'NDTE', 'NDUE', 'NEU',
                                   'NADTE/NDUE',
                                   'NDTE/NDUE'])
    df_RQ['log10(NTM)'] = np.log10(df_RQ['NTM'] + 1)
    df_RQ['log10(NEU)'] = np.log10(df_RQ['NEU'] + 1)
    df_RQ['log10(NEBTM)'] = np.log10(df_RQ['NEBTM'] + 1)
    df_RQ['log10(NTM-NEBTM)'] = np.log10(df_RQ['NTM'] + 1 - df_RQ['NEBTM'] + 1)
    df_RQ['NTM-NEBTM'] = df_RQ['NTM'] - df_RQ['NEBTM']
    df_RQ['log10(stars)'] = np.log10(df_RQ['stars'])
    totalNumberOfTestMethods = df_RQ['NTM'].sum()
    f.write("totalNumberOfTestMethods: " + str(totalNumberOfTestMethods) + "\n")
    Util.format_to_csv(df_RQ, "RQs/" + RQ_NUMBER + "/", "table" + RQ_NUMBER, RQ_NUMBER, columnsToLatex)


############################## RQ1 - PART 1 ##############################


def visaoGeralDF(printAll=False):
    # by platform
    ax = sns.pairplot(data=df_RQ,
                      vars=['projectCreatedAt', 'tagCreatedAt', 'stars', 'contributors', 'NEBTM/NTM', 'NADTE/NDUE',
                            'NDTE/NDUE'], hue="platform", palette=Util.COLOR_PALETTE)
    # ax = sns.pairplot(data=df_RQ, hue="platform", palette=Util.COLOR_PALETTE)
    plt.savefig(OUTPUT_FIGURES_PATH / 'VisaoGeralDF_PLATFORM.png', bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()
    if (printAll):
        # by domain
        ax = sns.pairplot(data=df_RQ, hue="domain", palette=Util.COLOR_PALETTE)
        plt.savefig(OUTPUT_FIGURES_PATH / 'VisaoGeralDF_DOMAIN.png', bbox_inches="tight")
        if (SHOW_FIGURE):
            plt.show()
        plt.clf()
        # only domain Mobile by platform
        df_mobile = df_RQ.loc[df_RQ['platform'] == "Mobile"]
        ax = sns.pairplot(data=df_mobile, hue="domain", palette=Util.COLOR_PALETTE)
        plt.savefig(OUTPUT_FIGURES_PATH / 'VisaoGeraldf_mobile_DOMAIN.png', bbox_inches="tight")
        if (SHOW_FIGURE):
            plt.show()
        plt.clf()
        # only domain Desktop/Server by platform
        df_desktopServers = df_RQ.loc[df_RQ['platform'] == 'Desktop/Server']
        ax = sns.pairplot(data=df_desktopServers, hue="domain", palette=Util.COLOR_PALETTE)
        plt.savefig(OUTPUT_FIGURES_PATH / 'VisaoGeralDF_DESKTOP-SERVERS_DOMAIN.png', bbox_inches="tight")
        if (SHOW_FIGURE):
            plt.show()
        plt.clf()
        # only domain Desktop/Server by platform
        df_desktopServers = df_RQ.loc[df_RQ['platform'] == 'Multi-platform']
        ax = sns.pairplot(data=df_desktopServers, hue="domain", palette=Util.COLOR_PALETTE)
        plt.savefig(OUTPUT_FIGURES_PATH / 'VisaoGeralDF_Multi-platform_DOMAIN.png', bbox_inches="tight")
        if (SHOW_FIGURE):
            plt.show()
        plt.clf()


def corrfunc(x, y, **kws):
    if kws['label'] == 'other':
        r_label = 'rO'
        pos_x = 0
    elif kws['label'] == 'Libraries':
        r_label = 'rL'
        pos_x = 0.3
    elif kws['label'] == 'Frameworks':
        r_label = 'rF'
        pos_x = 0.6
    elif kws['label'] == 'Tools':
        r_label = 'rF'
        pos_x = 0.9
    # r, p = stats.spearmanr(x, y)
    r, p = stats.spearmanr(x, y)
    p_stars = ''
    if p <= 0.05:
        p_stars = '*'
    if p <= 0.01:
        p_stars = '**'
    if p <= 0.001:
        p_stars = '***'
    ax = plt.gca()
    ax.annotate(r_label + ' = {:.2f}'.format(r) + p_stars,
                xy=(pos_x, 1.015), xycoords=ax.transAxes, fontweight='bold')


# https://stackoverflow.com/questions/48139899/correlation-matrix-plot-with-coefficients-on-one-side-scatterplots-on-another
def correlationRQ1_pairplot():
    for platform in df_RQ['platform'].unique():
        df_desktopServers = df_RQ.loc[df_RQ['platform'] == platform]
        g = sns.pairplot(data=df_desktopServers,
                         x_vars=['log10(NEBTM)', 'NEBTM/NTM', 'NADTE/NDUE',
                                 'NDTE/NDUE'],
                         y_vars=['projectCreatedOn', 'tagCreatedOn', 'log10(stars)', 'contributors', 'log10(NEU)',
                                 'log10(NTM)'], hue='domain', palette=Util.COLOR_PALETTE)
        g.map(corrfunc)
        g.fig.set_figheight(16)
        g.fig.set_figwidth(12)
        g.fig.suptitle(platform, fontsize='xx-large', y=1.00)  # y= some height>1

        # for i in range(len(g.fig.get_children()[-1].texts)):
        #     label = g.fig.get_children()[-1].texts[i].get_text()
        #     if label == 'other':
        #         replacement = 'other (rO)'
        #     elif label == 'Libraries':
        #         replacement = 'Libraries (rL)'
        #     elif label == 'Frameworks':
        #         replacement = 'Frameworks (rF)'
        #     g.fig.get_children()[-1].texts[i].set_text(replacement)
        #
        # g._legend.set_bbox_to_anchor((1.008, 0.55))

        g._legend.remove()

        handles = g._legend_data.values()
        labels = list(g._legend_data.keys())
        for i in range(len(labels)):
            label = labels[i]
            if label == 'other':
                replacement = 'other (rO)'
            elif label == 'Libraries':
                replacement = 'Libraries (rL)'
            elif label == 'Frameworks':
                replacement = 'Frameworks (rF)'
            labels[i] = replacement

        g.fig.legend(handles=handles, labels=labels, loc='upper center', bbox_to_anchor=(0.5, 0.99), ncol=3,
                     fontsize="large", frameon=True)
        g.fig.subplots_adjust(top=0.95)

        for ax in g.axes.flat:
            # ax.get_yaxis().set_tick_params(labelsize='x-large', which="major")
            # labels ao redor dos graficos
            # ax.set_xlabel(ax.get_xlabel(), fontsize='20')
            ax.set_xlabel(ax.get_xlabel(), fontsize=Util.SIZE_AXES_LABELS)
            y_label = ax.get_ylabel()
            if y_label == 'projectCreatedOn':
                y_label = 'project created on'
            elif y_label == 'tagCreatedOn':
                y_label = 'tag created on'
            ax.set_ylabel(y_label, fontsize=Util.SIZE_AXES_LABELS)
            ax.yaxis.grid(True, linewidth=1, which="major")
            if ax.rowNum > 1:
                # ax.xaxis.set_major_formatter(ticker.EngFormatter())
                ax.yaxis.set_major_formatter(ticker.EngFormatter())
            ax.get_yaxis().set_tick_params(labelsize=Util.SIZE_AXES_TITLE, which="major")
            ax.get_xaxis().set_tick_params(direction='out', labelsize=Util.SIZE_AXES_TITLE)

        figure_name = 'VisaoGeralDF_' + platform.replace("/", "-") + '.png'
        plt.savefig(OUTPUT_FIGURES_PATH / figure_name)
        if (SHOW_FIGURE):
            plt.show()
        plt.clf()


def correlationRQ1_heatmap():
    # by platform
    ax = sns.pairplot(data=df_RQ,
                      x_vars=['NEBTM', 'NEBTM/NTM', 'NADTE/NDUE',
                              'NDTE/NDUE'],
                      y_vars=['projectCreatedOn', 'tagCreatedOn', 'stars', 'contributors', 'NEU'],
                      hue="platform", palette=Util.COLOR_PALETTE)
    sns.heatmap(df_RQ.corr(), annot=True, fmt=".2f")
    plt.savefig(OUTPUT_FIGURES_PATH / 'VisaoGeralDF_PLATFORM.png')
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()


def pairPlotProjectDates():
    bins = np.arange(2007, 2020, 1)
    g = sns.FacetGrid(df_RQ, col="platform", sharex=True, sharey=True, hue="platform", palette=Util.COLOR_PALETTE, height=3,
                      aspect=1.5)
    g = (g.map(sns.distplot, "projectCreatedOn", kde=False, rug=False, bins=bins)).set(
        xticks=[2007, 2010, 2013, 2016, 2019], yticks=[0, 10, 20, 30])
    g.axes[0, 0].get_yaxis().set_tick_params(labelsize=Util.SIZE_AXES_VALUES, which="major")
    g.axes[0, 0].get_xaxis().set_tick_params(labelsize=Util.SIZE_AXES_VALUES)
    g.axes[0, 1].get_yaxis().set_tick_params(labelsize=Util.SIZE_AXES_VALUES, which="major")
    g.axes[0, 1].get_xaxis().set_tick_params(labelsize=Util.SIZE_AXES_VALUES)

    g.fig.subplots_adjust(wspace=.05, hspace=.05)

    for ax in g.axes.flat:
        # ax.get_yaxis().set_tick_params(labelsize='x-large', which="major")
        # labels ao redor dos graficos
        # ax.set_xlabel(ax.get_xlabel(), fontsize='20')
        ax.set_xlabel("", fontsize=Util.SIZE_AXES_LABELS)
        ax.set_ylabel(ax.get_ylabel(), fontsize=Util.SIZE_AXES_LABELS)

        # títulos em cima dos graficos
        if ax.get_title():
            ax.set_title(ax.get_title().split('=')[1],
                         fontsize=Util.SIZE_AXES_TITLE)

        # ax.set(xlabel='', ylabel='', title='')
        # plt.setp(ax.get_legend().get_texts(), fontsize='18')  # for legend text
        # plt.setp(ax.get_legend().get_title(), fontsize='20')  # for legend title
        ax.yaxis.grid(True, linewidth=1, which="major")
        ax.get_yaxis().set_tick_params(labelsize=Util.SIZE_AXES_TITLE, which="major")
        ax.get_xaxis().set_tick_params(direction='out', labelsize=Util.SIZE_AXES_TITLE)
    plt.tight_layout()
    plt.savefig(OUTPUT_FIGURES_PATH / 'pairPlotProjectDates.png', bbox_inches="tight")
    plt.savefig(OUTPUT_FIGURES_PATH / 'pairPlotProjectDates.pdf', bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()





def violinPlot_ProjectCreatedOn():
    fig, ax = plt.subplots(figsize=(6, 7))
    ax = sns.violinplot(x="domain", y="projectCreatedOn", data=df_RQ, cut=0, hue="platform", inner="box",
                        scale="count", palette=Util.COLOR_PALETTE, linewidth=1.5, ax=ax)
    ax.set(xlabel='', ylabel='', title='')
    ax.legend(title="platform", loc="lower center")
    ax.yaxis.grid(True, linewidth=1, which="major")
    plt.setp(ax.get_legend().get_texts(), fontsize=Util.SIZE_LEGEND_TEXT)  # for legend text
    plt.setp(ax.get_legend().get_title(), fontsize=Util.SIZE_LEGEND_TITLE)  # for legend title
    ax.get_yaxis().set_tick_params(labelsize=Util.SIZE_AXES_VALUES, which="major")
    ax.get_xaxis().set_tick_params(direction='out', labelsize=Util.SIZE_AXES_VALUES)
    ax.xaxis.set_ticks_position('bottom')
    # Show graphic
    plt.tight_layout()
    plt.savefig(OUTPUT_FIGURES_PATH / 'violinPlot_ProjectCreatedOn.pdf', bbox_inches="tight")
    plt.savefig(OUTPUT_FIGURES_PATH / 'violinPlot_ProjectCreatedOn.png', bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()


def violinPlot_TagCreatedOn():
    fig, ax = plt.subplots(figsize=(6, 7))
    ax = sns.violinplot(x="domain", y="tagCreatedOn", data=df_RQ, cut=0, hue="platform", inner="box", scale="count",
                        palette=Util.COLOR_PALETTE, linewidth=1.5, ax=ax)
    ax.set(xlabel='', ylabel='', title='')
    ax.legend(title="platform", loc="lower center")
    ax.yaxis.grid(True, linewidth=1, which="major")
    plt.setp(ax.get_legend().get_texts(), fontsize=Util.SIZE_LEGEND_TEXT)  # for legend text
    plt.setp(ax.get_legend().get_title(), fontsize=Util.SIZE_LEGEND_TITLE)  # for legend title
    ax.get_yaxis().set_tick_params(labelsize=Util.SIZE_AXES_VALUES, which="major")
    ax.get_xaxis().set_tick_params(direction='out', labelsize=Util.SIZE_AXES_VALUES)
    ax.xaxis.set_ticks_position('bottom')
    # Show graphic
    plt.tight_layout()
    plt.savefig(OUTPUT_FIGURES_PATH / 'violinPlot_TagCreatedOn.pdf', bbox_inches="tight")
    plt.savefig(OUTPUT_FIGURES_PATH / 'violinPlot_TagCreatedOn.png', bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()


def violinPlotRatio_Contributors():
    fig, ax = plt.subplots(figsize=(6, 7))
    ax = sns.violinplot(x="domain", y="contributors", data=df_RQ, cut=0, hue="platform", inner="box", scale="count",
                        palette=Util.COLOR_PALETTE, linewidth=1.5, ax=ax)
    # ax = sns.swarmplot(x="domain", y="contributors", data=df_RQ, hue="platform")
    ax.set(xlabel='', ylabel='', title='')
    ax.legend(title="platform", loc="upper center")
    ax.yaxis.grid(True, linewidth=1, which="major")
    plt.setp(ax.get_legend().get_texts(), fontsize=Util.SIZE_LEGEND_TEXT)  # for legend text
    plt.setp(ax.get_legend().get_title(), fontsize=Util.SIZE_LEGEND_TITLE)  # for legend title
    ax.get_yaxis().set_tick_params(labelsize=Util.SIZE_AXES_VALUES, which="major")
    ax.get_xaxis().set_tick_params(direction='out', labelsize=Util.SIZE_AXES_VALUES)
    ax.xaxis.set_ticks_position('bottom')
    # Show graphic
    plt.tight_layout()
    plt.savefig(OUTPUT_FIGURES_PATH / 'violinPlot_Contributors.pdf', bbox_inches="tight")
    plt.savefig(OUTPUT_FIGURES_PATH / 'violinPlot_Contributors.png', bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()


def violinPlotRatio_Stars():
    fig, ax = plt.subplots(figsize=(6, 7))
    # ax.set(yscale="log")
    # ax = sns.swarmplot(x="domain", y="stars", data=df_RQ, hue="platform")
    ax = sns.violinplot(x="domain", y="stars", data=df_RQ, cut=0, hue="platform", inner="box", scale="count",
                        palette=Util.COLOR_PALETTE, linewidth=1.5, ax=ax)
    ax.set(xlabel='', ylabel='', title='')
    ax.set_ylabel(ax.get_ylabel(), fontsize=Util.SIZE_AXES_LABELS)
    ax.set_yticks([3000, 5000, 10000, 20000, 30000, 40000, 50000])
    ax.yaxis.grid(True, linewidth=1, which="major")
    plt.setp(ax.get_legend().get_texts(), fontsize=Util.SIZE_LEGEND_TEXT)  # for legend text
    plt.setp(ax.get_legend().get_title(), fontsize=Util.SIZE_LEGEND_TITLE)  # for legend title
    # ax.set_yscale('log')
    ax.get_yaxis().set_tick_params(labelsize=Util.SIZE_AXES_VALUES, which="major")
    ax.get_xaxis().set_tick_params(direction='out', labelsize=Util.SIZE_AXES_VALUES)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_major_formatter(ticker.EngFormatter())
    # Show graphic
    plt.tight_layout()
    plt.savefig(OUTPUT_FIGURES_PATH / 'violinPlotRatio_Stars.pdf', bbox_inches="tight")
    plt.savefig(OUTPUT_FIGURES_PATH / 'violinPlotRatio_Stars.png', bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()


def numberOfTestMethodsPerProject_histogram():
    bins = np.arange(0, 6, 0.5)
    g = sns.FacetGrid(df_RQ, col="platform", sharex=False, hue="platform", palette=Util.COLOR_PALETTE)
    g = (g.map(sns.distplot, "log10(NTM)", kde=False, rug=True, bins=bins)).set(xticks=[0, 1, 2, 3, 4, 5],
                                                                                yticks=[10, 20, 30, 40])
    for ax in g.axes.flat:
        # ax.get_yaxis().set_tick_params(labelsize='x-large', which="major")
        # labels ao redor dos graficos
        # ax.set_xlabel(ax.get_xlabel(), fontsize='20')
        ax.set_xlabel(ax.get_xlabel(), fontsize=Util.SIZE_AXES_LABELS)
        ax.set_ylabel(ax.get_ylabel(), fontsize=Util.SIZE_AXES_LABELS)

        # títulos em cima dos graficos
        if ax.get_title():
            ax.set_title(ax.get_title().split('=')[1],
                         fontsize=Util.SIZE_AXES_TITLE)

        ax.yaxis.grid(True, linewidth=1, which="major")
        ax.get_yaxis().set_tick_params(labelsize=Util.SIZE_AXES_TITLE, which="major")
        ax.get_xaxis().set_tick_params(direction='out', labelsize=Util.SIZE_AXES_TITLE)
    plt.tight_layout()
    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ1_Fig1_numberOfTestMethodsPerProject_bar.png',
                bbox_inches="tight")
    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ1_Fig1_numberOfTestMethodsPerProject_bar.pdf', bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()


def numberOfExceptionalBehaviorTestMethodsPerProject_histogram():
    bins = np.arange(0, 5, 0.5)
    g = sns.FacetGrid(df_RQ, col="platform", sharex=False, hue="platform", palette=Util.COLOR_PALETTE)
    g = (g.map(sns.distplot, "log10(NEBTM)", kde=False, rug=True, bins=bins)).set(xticks=[0, 1, 2, 3, 4],
                                                                                  yticks=[10, 20, 30, 40, 50])

    for ax in g.axes.flat:
        # ax.get_yaxis().set_tick_params(labelsize='x-large', which="major")
        # labels ao redor dos graficos
        # ax.set_xlabel(ax.get_xlabel(), fontsize='20')
        ax.set_xlabel(ax.get_xlabel(), fontsize=Util.SIZE_AXES_LABELS)
        ax.set_ylabel(ax.get_ylabel(), fontsize=Util.SIZE_AXES_LABELS)

        # títulos em cima dos graficos
        if ax.get_title():
            ax.set_title(ax.get_title().split('=')[1],
                         fontsize=Util.SIZE_AXES_TITLE)

        ax.yaxis.grid(True, linewidth=1, which="major")
        ax.get_yaxis().set_tick_params(labelsize=Util.SIZE_AXES_TITLE, which="major")
        ax.get_xaxis().set_tick_params(direction='out', labelsize=Util.SIZE_AXES_TITLE)

    plt.tight_layout()
    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ1_Fig2_numberOfExceptionalBehaviorExceptionTestMethodsPerProject_bar.png',
                bbox_inches="tight")
    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ1_Fig2_numberOfExceptionalBehaviorExceptionTestMethodsPerProject_bar.pdf',
                bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()


def numberOfExceptionalBehaviorTestMethodsPerProjectXNumberOfTestMethods_scatterplot():
    bins = np.arange(0, 5, 0.5)
    g = sns.FacetGrid(df_RQ, col="platform", sharex=False, hue="domain", palette=Util.COLOR_PALETTE)
    g = (g.map(plt.scatter, "log10(NTM)",
               "log10(NEBTM)")).add_legend()  # .set(xticks=[0, 1, 2, 3, 4], yticks=[0, 20, 40, 60])
    g.axes[0, 0].get_yaxis().set_tick_params(labelsize=14, which="major")
    # g.axes[0, 1].get_yaxis().set_tick_params(labelsize=14, which="major")
    # g.map(corrfunc)

    # plt.tight_layout()
    plt.savefig(
        OUTPUT_FIGURES_PATH / 'Fig1_numberOfExceptionalBehaviorTestMethodsPerProjectXNumberOfTestMethods_scatterplot.png',
        bbox_inches="tight")
    # plt.savefig(output_figures_path / 'Fig1_numberOfExceptionalBehaviorTestMethodsPerProject_bar.pdf', bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()


def numberOfExceptionalBehaviorTestMethodsPerProjectXNumberOfTestMethods_linearregression():
    df_mobile = df_RQ[df_RQ['platform'] == "Mobile"]
    # df_mobile = df_mobile[['log10(NTM)', 'log10(NEBTM)']]
    mobile_correlation, mobile_p_value = stats.spearmanr(df_mobile['NTM-NEBTM'], df_mobile['NEBTM'])

    df_desktopservers = df_RQ[df_RQ['platform'] == 'Desktop/Server']
    desktopservers_correlation, desktopservers_p_value = stats.spearmanr(df_desktopservers['NTM-NEBTM'],
                                                                         df_desktopservers['NEBTM'])

    df_multiplatform = df_RQ[df_RQ['platform'] == 'Multi-platform']
    multiplatform_correlation, multiplatform_p_value = stats.spearmanr(df_multiplatform['NTM-NEBTM'],
                                                                         df_multiplatform['NEBTM'])
    # df_desktopservers = df_desktopservers[['log10(NTM)', 'log10(NEBTM)']]
    f.write("Mobile Correlation: " + str(mobile_correlation) + " pvalue: " + str(mobile_p_value) + "\n")
    f.write("Desktop/Server Correlation: " + str(desktopservers_correlation) + " pvalue: " + str(desktopservers_p_value) + "\n")
    f.write("Multi-platform Correlation: " + str(multiplatform_correlation) + " pvalue: " + str(multiplatform_p_value) + "\n")
    # f.write("Mobile correlation: " + df_mobile.corr()  + "\n")
    # f.write("Desktop/Server correlation: " + df_desktopservers.corr()  + "\n")

    g = sns.lmplot(y="log10(NTM-NEBTM)", x="log10(NEBTM)", hue="domain", col="platform",
                   col_order=Util.FIGURE_ORDER, palette=Util.COLOR_PALETTE,
                   data=df_RQ, legend=False).set(xticks=[0, 1, 2, 3, 4, 5], yticks=[0, 1, 2, 3, 4, 5, 6])
    # .set(yticks=[-1, 0, 1, 2, 3, 4, 5], xticks=[-2, -1, 0, 1, 2, 3, 4, 5])

    # Legend
    ax_aux = g.axes[0, 1]
    ax_aux.legend(title="", loc="upper left")
    plt.setp(ax_aux.get_legend().get_texts(), fontsize=Util.SIZE_LEGEND_TEXT)  # for legend text
    plt.setp(ax_aux.get_legend().get_title(), fontsize=Util.SIZE_LEGEND_TITLE)  # for legend title

    for ax in g.axes.flat:
        ax.set_xlim(-1, 5)
        ax.set_ylim(-1, 6)
        # ax.get_yaxis().set_tick_params(labelsize='x-large', which="major")
        # labels ao redor dos graficos
        # ax.set_xlabel(ax.get_xlabel(), fontsize='20')
        ax.set_xlabel(ax.get_xlabel(), fontsize=Util.SIZE_AXES_LABELS)
        ax.set_ylabel(ax.get_ylabel(), fontsize=Util.SIZE_AXES_LABELS)

        # títulos em cima dos graficos
        if ax.get_title():
            ax.set_title(ax.get_title().split('=')[1],
                         fontsize=Util.SIZE_AXES_TITLE)

        ax.yaxis.grid(True, linewidth=1, which="major")
        ax.get_yaxis().set_tick_params(labelsize=Util.SIZE_AXES_TITLE, which="major")
        ax.get_xaxis().set_tick_params(direction='out', labelsize=Util.SIZE_AXES_TITLE)

    # plt.tight_layout()
    plt.savefig(
        OUTPUT_FIGURES_PATH / 'G1-Q1-Fig2_numberOfExceptionalBehaviorTestMethodsPerProjectXNumberOfTestMethods_regressao.png',
        bbox_inches="tight")
    plt.savefig(
        OUTPUT_FIGURES_PATH / 'G1-Q1-Fig2_numberOfExceptionalBehaviorTestMethodsPerProjectXNumberOfTestMethods_regressao.pdf',
        bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()


def numberOfExceptionalBehaviorTestMethodsPerProjectXNumberOfExceptionsUses_linearregression():
    df_mobile = df_RQ[df_RQ['platform'] == 'Mobile']
    # df_mobile = df_mobile[['log10(NTM)', 'log10(NEBTM)']]
    mobile_correlation, mobile_p_value = stats.spearmanr(df_mobile['log10(NEU)'], df_mobile['log10(NEBTM)'])
    df_desktopservers = df_RQ[df_RQ['platform'] == 'Desktop/Server']
    desktopservers_correlation, desktopservers_p_value = stats.spearmanr(df_desktopservers['log10(NEU)'],
                                                                         df_desktopservers['log10(NEBTM)'])
    df_multiplatform = df_RQ[df_RQ['platform'] == 'Multi-platform']
    multiplatform_correlation, multiplatform_p_value = stats.spearmanr(df_multiplatform['log10(NEU)'],
                                                                         df_multiplatform['log10(NEBTM)'])
    # df_desktopservers = df_desktopservers[['log10(NTM)', 'log10(NEBTM)']]
    f.write("Mobile Correlation (exception uses x exception tests): " + str(mobile_correlation) + " pvalue: " + str(
        mobile_p_value) + "\n")
    f.write("Desktop/Server Correlation (exception uses x exception tests): " + str(
        desktopservers_correlation) + " pvalue: " + str(desktopservers_p_value) + "\n")
    f.write("Multi-platform Correlation (exception uses x exception tests): " + str(
        desktopservers_correlation) + " pvalue: " + str(multiplatform_p_value) + "\n")
    # f.write("Mobile correlation: " + df_mobile.corr() + "\n")
    # f.write("Desktop/Server correlation: " + df_desktopservers.corr() + "\n")
    g = sns.lmplot(x="log10(NEU)", y="log10(NEBTM)", hue="domain", col="platform", data=df_RQ, legend=False).set(
        xticks=[-1, 0, 1, 2, 3, 4, 5], yticks=[-4, -3, -2, -1, 0, 1, 2, 3, 4, 5])

    # Legend
    ax_aux = g.axes[0, 1]
    ax_aux.legend(title="domain", loc="upper left")
    plt.setp(ax_aux.get_legend().get_texts(), fontsize=Util.SIZE_LEGEND_TEXT)  # for legend text
    plt.setp(ax_aux.get_legend().get_title(), fontsize=Util.SIZE_LEGEND_TITLE)  # for legend title

    for ax in g.axes.flat:
        # ax.get_yaxis().set_tick_params(labelsize='x-large', which="major")
        # labels ao redor dos graficos
        # ax.set_xlabel(ax.get_xlabel(), fontsize='20')
        ax.set_xlabel(ax.get_xlabel(), fontsize=Util.SIZE_AXES_LABELS)
        ax.set_ylabel(ax.get_ylabel(), fontsize=Util.SIZE_AXES_LABELS)

        # títulos em cima dos graficos
        if ax.get_title():
            ax.set_title(ax.get_title().split('=')[1],
                         fontsize=Util.SIZE_AXES_TITLE)

        ax.yaxis.grid(True, linewidth=1, which="major")
        ax.get_yaxis().set_tick_params(labelsize=Util.SIZE_AXES_TITLE, which="major")
        ax.get_xaxis().set_tick_params(direction='out', labelsize=Util.SIZE_AXES_TITLE)

    # plt.tight_layout()
    plt.savefig(
        OUTPUT_FIGURES_PATH / 'Fig1_numberOfExceptionalBehaviorTestMethodsPerProjectXNumberOfExceptionsUses_regressao.png',
        bbox_inches="tight")
    # plt.savefig(output_figures_path / 'Fig1_numberOfExceptionalBehaviorTestMethodsPerProject_bar.pdf', bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()



def calculateCorrelations():
    f.write('\n*** START OF CORRELATIONS EVALUATION *** \n')
    StatisticalTests.evaluateCorrelation(df_RQ, "NTM-NEBTM", "NEBTM", False, f)
    StatisticalTests.evaluateCorrelation(df_RQ, "projectMonths", "NEBTM", False, f)
    StatisticalTests.evaluateCorrelation(df_RQ, "contributors", "NEBTM", False, f)
    StatisticalTests.evaluateCorrelation(df_RQ, "projectMonths", "NEBTM", False, f)
    StatisticalTests.evaluateCorrelation(df_RQ, "contributors", "NEBTM", False, f)
    StatisticalTests.evaluateCorrelation(df_RQ, "projectMonths", "NEBTM/NTM", False, f)
    StatisticalTests.evaluateCorrelation(df_RQ, "contributors", "NEBTM/NTM", False, f)
    StatisticalTests.evaluateCorrelation(df_RQ, "projectMonths", "NDTE/NDUE", False, f)
    StatisticalTests.evaluateCorrelation(df_RQ, "contributors", "NDTE/NDUE", False, f)
    # StatisticalTests.evaluateCorrelation(df_RQ, "NEU", "NEBTM", False, f)
    # StatisticalTests.evaluateCorrelation(df_RQ, "NEU", "NEBTM/NTM", False, f)
    # StatisticalTests.evaluateCorrelation(df_RQ, "NEU", "NDTE/NDUE", False, f)
    f.write('\n*** END OF CORRELATION EVALUATION *** \n\n')

def numberOfExceptionalBehaviorTestMethodsPerProjectXNumberOfContributors_linearregression():
    df_mobile = df_RQ[df_RQ['platform'] == "Mobile"]
    # df_mobile = df_mobile[['log10(NTM)', 'log10(NEBTM)']]
    mobile_correlation, mobile_p_value = stats.spearmanr(df_mobile['contributors'], df_mobile['log10(NEBTM)'])
    df_desktopservers = df_RQ[df_RQ['platform'] == 'Desktop/Server']
    desktopservers_correlation, desktopservers_p_value = stats.spearmanr(df_desktopservers['contributors'],
                                                                         df_desktopservers['log10(NEBTM)'])
    # df_desktopservers = df_desktopservers[['log10(NTM)', 'log10(NEBTM)']]
    f.write("Mobile Correlation (contributors x exception tests): " + str(mobile_correlation) + " pvalue: " + str(
        mobile_p_value) + "\n")
    f.write("Desktop/Server Correlation (contributors x exception tests): " + str(
        desktopservers_correlation) + " pvalue: " + str(desktopservers_p_value) + "\n")
    # f.write("Mobile correlation: " + df_mobile.corr() + "\n")
    # f.write("Desktop/Server correlation: " + df_desktopservers.corr() + "\n")
    g = sns.lmplot(x="contributors", y="log10(NEBTM)", hue="domain", col="platform", data=df_RQ, legend=False).set(
        yticks=[-4, -3, -2, -1, 0, 1, 2, 3, 4, 5])

    # Legend
    ax_aux = g.axes[0, 1]
    ax_aux.legend(title="domain", loc="upper left")
    plt.setp(ax_aux.get_legend().get_texts(), fontsize=Util.SIZE_LEGEND_TEXT)  # for legend text
    plt.setp(ax_aux.get_legend().get_title(), fontsize=Util.SIZE_LEGEND_TITLE)  # for legend title

    for ax in g.axes.flat:
        # ax.get_yaxis().set_tick_params(labelsize='x-large', which="major")
        # labels ao redor dos graficos
        # ax.set_xlabel(ax.get_xlabel(), fontsize='20')
        ax.set_xlabel(ax.get_xlabel(), fontsize=Util.SIZE_AXES_LABELS)
        ax.set_ylabel(ax.get_ylabel(), fontsize=Util.SIZE_AXES_LABELS)

        # títulos em cima dos graficos
        if ax.get_title():
            ax.set_title(ax.get_title().split('=')[1],
                         fontsize=Util.SIZE_AXES_TITLE)

        ax.yaxis.grid(True, linewidth=1, which="major")
        ax.get_yaxis().set_tick_params(labelsize=Util.SIZE_AXES_TITLE, which="major")
        ax.get_xaxis().set_tick_params(direction='out', labelsize=Util.SIZE_AXES_TITLE)

    # plt.tight_layout()
    plt.savefig(
        OUTPUT_FIGURES_PATH / 'Fig1_numberOfExceptionalBehaviorTestMethodsPerProjectXNumberOfContributorss_regressao.png',
        bbox_inches="tight")
    # plt.savefig(output_figures_path / 'Fig1_numberOfExceptionalBehaviorTestMethodsPerProject_bar.pdf', bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()


def numberOfExceptionalBehaviorTestMethodsPerProject_violinPlot():
    fig, ax = plt.subplots(figsize=(6, 7))
    ax = sns.violinplot(x="domain", y="log10(NEBTM)", data=df_RQ, cut=0, hue="platform", inner="box", scale="count",
                        palette=Util.COLOR_PALETTE, ax=ax)
    sns.set_style("whitegrid")
    sns.despine()

    # ax = sns.swarmplot(x="domain", y="contributors", data=df_RQ, hue="platform")
    ax.set(xlabel='', ylabel='', title='')
    ax.legend(loc="upper center")
    ax.yaxis.grid(True, linewidth=1, which="major")
    plt.setp(ax.get_legend().get_texts(), fontsize='18')  # for legend text
    plt.setp(ax.get_legend().get_title(), fontsize='20')  # for legend title
    ax.get_yaxis().set_tick_params(labelsize=25, which="major")
    ax.get_xaxis().set_tick_params(direction='out', labelsize=25)
    ax.xaxis.set_ticks_position('bottom')
    plt.tight_layout()
    plt.savefig(OUTPUT_FIGURES_PATH / 'Fig1_numberOfExceptionalBehaviorExceptionTestMethodsPerProject_violinplot.png',
                bbox_inches="tight")
    plt.savefig(OUTPUT_FIGURES_PATH / 'Fig1_numberOfExceptionalBehaviorExceptionTestMethodsPerProject_violinplot.pdf',
                bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()


def barPlotNumberOfExceptionalTests_barplot():
    f.write("\n\n ##############  RQ1 - PART 1 ##############\n")
    platformList = df_RQ["platform"].unique()
    domainList = df_RQ["domain"].unique()

    df_aux = []
    df_filtered_one_or_more = df_RQ[(df_RQ['NEBTM'] >= 1)]
    totalDfSize = len(df_RQ)
    totalHigherThanZero = len(df_filtered_one_or_more)
    ratioAux = totalHigherThanZero / totalDfSize
    f.write(f'Total_NEBTM > 0: {totalHigherThanZero} out of {totalDfSize}({ratioAux})' + "\n")
    for platform in platformList:
        df_platform = df_RQ[(df_RQ['platform'] == platform)]
        df_filtered_one_or_more_platform = df_platform[(df_platform['NEBTM'] >= 1)]
        totalDfSize = len(df_platform)
        totalHigherThanZero = len(df_filtered_one_or_more_platform)
        ratioAux = totalHigherThanZero/totalDfSize
        f.write(f'{platform}_NEBTM > 0: {totalHigherThanZero} out of {totalDfSize}({ratioAux})' + "\n")
        for domain in domainList:
            df_domain = df_platform[(df_platform["domain"] == domain)]
            df_filtered_zero_domain = df_domain[(df_domain['NEBTM'] == 0)]
            df_filtered_one_or_more_domain = df_domain[(df_domain['NEBTM'] >= 1)]
            df_aux.append([platform, domain, Util.LABELS[0], len(df_filtered_zero_domain)])
            df_aux.append([platform, domain, Util.LABELS[1], len(df_filtered_one_or_more_domain)])
            totalDfSize = len(df_domain)
            totalHigherThanZero = len(df_filtered_one_or_more_domain)
            ratioAux = totalHigherThanZero / totalDfSize
            f.write(f'{platform}_{domain}_NEBTM > 0: {totalHigherThanZero} out of {totalDfSize}({ratioAux})' + "\n")

    df_counter = pd.DataFrame(df_aux, columns=["platform", "domain", "NEBTM", "count"])
    g = sns.catplot(x="domain", y="count", col="platform", hue="NEBTM", data=df_counter, kind="bar",
                    palette=Util.COLOR_DEGRADE, legend=False, legend_out=False, col_order=Util.FIGURE_ORDER)
    g.fig.subplots_adjust(wspace=.05, hspace=.05)
    g.fig.set_figheight(3)
    g.fig.set_figwidth(6)

    # Legend
    ax_aux = g.axes[0, 1]
    ax_aux.legend(title="NEBTM", loc="upper center")
    #ax_aux.legend(title="NEBTM", loc="upper center", bbox_to_anchor=(0.5, 1.20), ncol=2, frameon=False)
    plt.setp(ax_aux.get_legend().get_texts(), fontsize=Util.SIZE_LEGEND_TEXT)  # for legend text
    plt.setp(ax_aux.get_legend().get_title(), fontsize=Util.SIZE_LEGEND_TITLE)  # for legend title

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
    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ1_numberOfExceptionsTests_bar.pdf', bbox_inches="tight")
    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ1_numberOfExceptionsTests_bar.png', bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()



############################## RQ1 - PART 2 ##############################
def calculate_NEBTM_NTM_resume(df):
    df_mobile = df[df['platform'] == 'Mobile']
    f.write(df_mobile.describe() + "\n")
    df_ds = df[df['platform'] == 'Desktop/Server']
    f.write(df_ds.describe() + "\n")
    df_multi = df[df['platform'] == 'Multi-platform']
    f.write(df_multi.describe() + "\n")


def violinsPlot_NEBTM_NTM():
    f.write("\n\n ##############  RQ1 - PART 2 ############## \n")
    df_filtered = df_RQ[(df_RQ['NEBTM'] >= 0)]
    platformList = df_RQ["platform"].unique()
    domainList = df_RQ["domain"].unique()

    ratio = 0.2

    df_aux = []
    df_belowTo20 = df_filtered[(df_filtered['NEBTM/NTM'] <= ratio)]
    df_belowTo10 = df_filtered[(df_filtered['NEBTM/NTM'] <= 0.1)]
    df_belowTo5 = df_filtered[(df_filtered['NEBTM/NTM'] <= 0.05)]
    f.write("NEBTM_NTM <= 20% | Total:" + str(len(df_belowTo20)) + " out of " + str(
        len(df_filtered)) + str("({:.2%})").format(len(df_belowTo20) / len(df_filtered)) + "\n")
    f.write("NEBTM_NTM <= 10% | Total:" + str(len(df_belowTo10)) + " out of " + str(
        len(df_filtered)) + str("({:.2%})").format(len(df_belowTo10) / len(df_filtered)) + "\n")
    f.write("NEBTM_NTM <= 5% | Total:" + str(len(df_belowTo5)) + " out of " + str(
        len(df_filtered)) + str("({:.2%})").format(len(df_belowTo5) / len(df_filtered)) + "\n")
    for platform in platformList:
        df_platform_total = df_filtered[(df_filtered['platform'] == platform)]
        df_platform_belowTo20 = df_platform_total[(df_platform_total['NEBTM/NTM'] <= ratio)]
        df_platform_belowTo10 = df_platform_total[(df_platform_total['NEBTM/NTM'] <= 0.1)]
        df_platform_belowTo5 = df_platform_total[(df_platform_total['NEBTM/NTM'] <= 0.05)]
        f.write("NEBTM_NTM <= 20% | " + platform + ":" + str(len(df_platform_belowTo20)) + " out of " + str(len(df_platform_total)) + str("({:.2%})").format(len(df_platform_belowTo20)/len(df_platform_total)) + "\n")
        f.write("NEBTM_NTM <= 10% | " + platform + ":" + str(len(df_platform_belowTo10)) + " out of " + str(len(df_platform_total)) + str("({:.2%})").format(len(df_platform_belowTo10)/len(df_platform_total)) + "\n")
        f.write("NEBTM_NTM <= 5% | " + platform + ":" + str(len(df_platform_belowTo5)) + " out of " + str(len(df_platform_total)) + str("({:.2%})").format(len(df_platform_belowTo5)/len(df_platform_total)) + "\n")
        for domain in domainList:
            df_domain_total = df_platform_total[(df_platform_total["domain"] == domain)]
            df_belowTo20 = df_domain_total[(df_domain_total['NEBTM/NTM'] <= ratio)]
            f.write("NEBTM_NTM <= 20% | " + platform + "/" + domain + ":" + str(len(df_belowTo20)) + " out of " + str(len(df_domain_total)) + str("({:.2%})").format(len(df_belowTo20)/len(df_domain_total)) + "\n")


    fig = plt.subplots(figsize=(6, 2))
    gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1.5], wspace=.02, hspace=.05)
    ax0 = plt.subplot(gs[0])
    ax1 = plt.subplot(gs[1])
    Util.evaluate_outliers(df_RQ, 'NEBTM/NTM', f)
    sns.violinplot(x="domain", y="NEBTM/NTM", data=df_RQ, cut=0, inner="box", hue="platform",
                   hue_order=Util.FIGURE_ORDER, scale="width",
                   palette=Util.COLOR_PALETTE, linewidth=1.5, ax=ax0, saturation=1)
    sns.violinplot(x="platform", y="NEBTM/NTM", data=df_RQ, cut=0, inner="box", scale="width",
                   order=Util.FIGURE_ORDER,
                   palette=Util.COLOR_PALETTE, linewidth=1.5, ax=ax1, saturation=1)
    # sns.boxplot(x="domain", y="NEBTM/NTM", data=df_RQ, hue="platform",
    #                hue_order=Util.FIGURE_ORDER,
    #                palette=Util.COLOR_PALETTE, linewidth=1.5, ax=ax0, saturation=1)
    # sns.boxplot(x="platform", y="NEBTM/NTM", data=df_RQ,
    #                order=Util.FIGURE_ORDER,
    #                palette=Util.COLOR_PALETTE, linewidth=1.5, ax=ax1, saturation=1)
    ax0.set(xlabel='', ylabel='', title='', yticks=[0, 0.2, 0.4, 0.6, 0.8, 1])
    ax0.set_ylabel(ax0.get_ylabel(), fontsize=Util.SIZE_AXES_LABELS)
    #ax0.set_ylim(0, 0.4)
    #ax0.legend(title="", loc="upper center")
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
    #ax1.set_ylim(0, 0.4)
    # Show graphic
    plt.tight_layout()
    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ1_ratioNumberOfDistinctExceptionTestsViolinPlot_domain.pdf',
                bbox_inches="tight")
    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ1_ratioNumberOfDistinctExceptionTestsViolinPlot_domain.png',
                bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()

# def violinsPlot_NEBTM_NTM():
#     fig = plt.subplots(figsize=(6, 5))
#     gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1.5], wspace=.02, hspace=.05)
#     ax0 = plt.subplot(gs[0])
#     ax1 = plt.subplot(gs[1])
#     evaluateOutliersIQR(df_RQ, 'NEBTM/NTM')
#     sns.violinplot(x="domain", y="NEBTM/NTM", data=df_RQ, cut=0, inner="box", hue="platform",
#                    hue_order=Util.FIGURE_ORDER, scale="count",
#                    palette=Util.COLOR_PALETTE, linewidth=1.5, ax=ax0)
#     sns.violinplot(x="platform", y="NEBTM/NTM", data=df_RQ, cut=0, inner="box", scale="count",
#                    order=Util.FIGURE_ORDER,
#                    palette=Util.COLOR_PALETTE, linewidth=1.5, ax=ax1)
#     ax0.set(xlabel='', ylabel='', title='', yticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
#     ax0.set_ylabel(ax0.get_ylabel(), fontsize=Util.SIZE_AXES_LABELS)
#     #ax0.set_ylim(0, 0.4)
#     ax0.legend(title="", loc="upper right")
#     ax0.yaxis.grid(True, linewidth=1, which="major")
#     plt.setp(ax0.get_legend().get_texts(), fontsize=Util.SIZE_LEGEND_TEXT)  # for legend text
#     plt.setp(ax0.get_legend().get_title(), fontsize=Util.SIZE_LEGEND_TITLE)  # for legend title
#     ax0.get_yaxis().set_tick_params(labelsize=Util.SIZE_AXES_VALUES, which="major")
#     ax0.get_xaxis().set_tick_params(direction='out', labelsize=Util.SIZE_AXES_VALUES)
#     ax0.xaxis.set_ticks_position('bottom')
#     ax0.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1, decimals=0))
#
#     ax1.set(xlabel='', ylabel='', title='', xticks=[1], yticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
#     # ax1.set_xticks(5)
#     ax1.set_xticklabels(['all'])
#     ax1.yaxis.grid(True, linewidth=1, which="major")
#     ax1.get_yaxis().set_tick_params(labelsize=Util.SIZE_AXES_VALUES, which="major")
#     ax1.get_xaxis().set_tick_params(direction='out', labelsize=Util.SIZE_AXES_VALUES)
#     ax1.xaxis.set_ticks_position('bottom')
#     ax1.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1, decimals=0))
#     ax1.set_yticklabels([])
#     #ax1.set_ylim(0, 0.4)
#     # Show graphic
#     plt.tight_layout()
#     plt.savefig(output_figures_path / 'G1-Q2_ratioNumberOfDistinctExceptionTestsViolinPlot_domain.pdf',
#                 bbox_inches="tight")
#     plt.savefig(output_figures_path / 'G1-Q2_ratioNumberOfDistinctExceptionTestsViolinPlot_domain.png',
#                 bbox_inches="tight")
#     if (SHOW_FIGURE):
#         plt.show()
#     plt.clf()


def violinsPlot_NADTE_NDUE():
    f.write("\n\n ############## RQ1 - PART 4 ############## \n")
    df_NADTE = df_RQ[(df_RQ['NADTE'] >= 0)]
    df_diff = df_RQ[(df_RQ['NADTE'] - df_RQ['NDTE'] > 0)]
    ratio = len(df_diff) / len(df_NADTE)
    f.write("Number of Projects where NADTE > NDTE " + str(len(df_diff)) + " de " + str(len(df_NADTE)) + " " + str(ratio) + "\n")
    fig = plt.subplots(figsize=(6, 2))
    gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1.5], wspace=.02, hspace=.05)
    ax0 = plt.subplot(gs[0])
    ax1 = plt.subplot(gs[1])
    Util.evaluate_outliers(df_RQ, 'NADTE/NDUE', f)
    sns.violinplot(x="domain", y="NADTE/NDUE", data=df_RQ, cut=0, inner="box", hue="platform",
                   hue_order=Util.FIGURE_ORDER, scale="width",
                   palette=Util.COLOR_PALETTE, linewidth=1.5, ax=ax0, saturation=1)
    sns.violinplot(x="platform", y="NADTE/NDUE", data=df_RQ, cut=0, inner="box", scale="width",
                   order=Util.FIGURE_ORDER,
                   palette=Util.COLOR_PALETTE, linewidth=1.5, ax=ax1, saturation=1)
    # sns.boxplot(x="domain", y="NADTE/NDUE", data=df_RQ, hue="platform",
    #                hue_order=Util.FIGURE_ORDER,
    #                palette=Util.COLOR_PALETTE, linewidth=1.5, ax=ax0, saturation=1)
    # sns.boxplot(x="platform", y="NADTE/NDUE", data=df_RQ,
    #                order=Util.FIGURE_ORDER,
    #                palette=Util.COLOR_PALETTE, linewidth=1.5, ax=ax1, saturation=1)
    ax0.set(xlabel='', ylabel='', title='', yticks=[0, 0.2, 0.4, 0.6, 0.8, 1, 1.2, 1.4])
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

    ax1.set(xlabel='', ylabel='', title='', xticks=[1], yticks=[0, 0.2, 0.4, 0.6, 0.8, 1, 1.2, 1.4])
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
    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ1_ratioNumberOfTestedExceptionsViolinPlot_domain.pdf',
                bbox_inches="tight")
    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ1_ratioNumberOfTestedExceptionsViolinPlot_domain.png',
                bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()




def violinsPlot_NDTE_NDUE():
    f.write("\n\n ##############  RQ1 - PART 3 ############## \n")
    df_filtered = df_RQ[(df_RQ['NEBTM'] >= 0)]
    platformList = df_RQ["platform"].unique()
    domainList = df_RQ["domain"].unique()
    ratio = 0.10
    df_aux = []
    df_below10 = df_filtered[(df_filtered['NDTE/NDUE'] <= ratio)]
    f.write("NDTE/NDUE <= 10% | Total:" + str(len(df_below10)) + " out of " + str(
        len(df_filtered)) + str("({:.2%})").format(len(df_below10) / len(df_filtered)) + "\n")
    for domain in domainList:
        df_domain_total = df_filtered[(df_filtered["domain"] == domain)]
        df_domain_below10 = df_domain_total[(df_domain_total['NDTE/NDUE'] <= ratio)]
        f.write("NDTE/NDUE <= 10% | " + domain + ":" + str(len(df_domain_below10)) + " out of " + str(
            len(df_domain_total)) + str("({:.2%})").format(len(df_domain_below10) / len(df_domain_total)) + "\n")
    for platform in platformList:
        df_platform_total = df_RQ[(df_RQ['platform'] == platform)]
        df_platform_below10 = df_platform_total[(df_platform_total['NDTE/NDUE'] <= ratio)]
        f.write("NDTE/NDUE <= 10% | " + platform + ":" + str(len(df_platform_below10)) + " out of " + str(len(df_platform_total)) + str("({:.2%})").format(len(df_platform_below10)/len(df_platform_total)) + "\n")
        for domain in domainList:
            df_domain_total = df_platform_total[(df_platform_total["domain"] == domain)]
            df_domain_below10 = df_domain_total[(df_domain_total['NDTE/NDUE'] <= ratio)]
            f.write("NDTE/NDUE <= 10% | " + platform + "/" + domain + ":" + str(len(df_domain_below10)) + " out of " + str(len(df_domain_total)) + str("({:.2%})").format(len(df_domain_below10)/len(df_domain_total)) + "\n")

    fig = plt.subplots(figsize=(6, 2))
    gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1.5], wspace=.02, hspace=.05)
    ax0 = plt.subplot(gs[0])
    ax1 = plt.subplot(gs[1])
    Util.evaluate_outliers(df_RQ, 'NDTE/NDUE', f)
    sns.violinplot(x="domain", y="NDTE/NDUE", data=df_RQ, cut=0, inner="box", hue="platform",
                   hue_order=Util.FIGURE_ORDER, scale="width",
                   palette=Util.COLOR_PALETTE, linewidth=1.5, ax=ax0, saturation=1)
    sns.violinplot(x="platform", y="NDTE/NDUE", data=df_RQ, cut=0, inner="box", scale="width",
                   order=Util.FIGURE_ORDER,
                   palette=Util.COLOR_PALETTE, linewidth=1.5, ax=ax1, saturation=1)
    # sns.boxplot(x="domain", y="NDTE/NDUE", data=df_RQ, hue="platform",
    #                hue_order=Util.FIGURE_ORDER,
    #                palette=Util.COLOR_PALETTE, linewidth=1.5, ax=ax0, saturation=1)
    # sns.boxplot(x="platform", y="NDTE/NDUE", data=df_RQ,
    #                order=Util.FIGURE_ORDER,
    #                palette=Util.COLOR_PALETTE, linewidth=1.5, ax=ax1, saturation=1)
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
    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ1_ratioNumberOfTestedAndUsedExceptionsViolinPlot_domain.pdf',
                bbox_inches="tight")
    plt.savefig(OUTPUT_FIGURES_PATH / 'RQ1_ratioNumberOfTestedAndUsedExceptionsViolinPlot_domain.png',
                bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()


def heatMap():
    fig, ax = plt.subplots(figsize=(10, 10))
    sns.heatmap(df_RQ.corr(), annot=True, fmt=".2f")
    # Show graphic
    # plt.tight_layout()
    # plt.savefig(output_figures_path / 'Fig3_ratioNDTE_NDUE_BoxPlot.pdf', bbox_inches="tight")
    plt.savefig(OUTPUT_FIGURES_PATH / 'VisaoGeral_Correlacao.png')
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()





# Generating Table III
generateDataSet()



#
# RQ1-PART1
barPlotNumberOfExceptionalTests_barplot()
#numberOfTestMethodsPerProject_histogram()
#numberOfExceptionalBehaviorTestMethodsPerProject_histogram()
#numberOfExceptionalBehaviorTestMethodsPerProject_violinPlot()
#numberOfExceptionalBehaviorTestMethodsPerProjectXNumberOfTestMethods_scatterplot()
#numberOfExceptionalBehaviorTestMethodsPerProjectXNumberOfTestMethods_linearregression()
#numberOfExceptionalBehaviorTestMethodsPerProjectXNumberOfExceptionsUses_linearregression()
#numberOfExceptionalBehaviorTestMethodsPerProjectXNumberOfContributors_linearregression()

calculateCorrelations()

# RQ1-PART2
violinsPlot_NEBTM_NTM()
#
# RQ1-PART3
violinsPlot_NDTE_NDUE()
#
# RQ1-PART4
violinsPlot_NADTE_NDUE()


#heatMap()

f.write("******************")
f.close()