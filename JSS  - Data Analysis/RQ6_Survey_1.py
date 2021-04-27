import re
from pathlib import Path

from nltk.util import ngrams
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from PIL import Image
#from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

from main import Util

df = pd.read_csv("RQs/RQ6-survey_1/Survey_23-10-2019.csv", header=0, names=["timestamp","q1","q2","q3","q4","q5","q6","q7","q8","q9","q10","q11","q12","q13"])

SHOW_FIGURE = False

sns.set(style="whitegrid")


RQ_NUMBER = "RQ6-survey_1"
OUTPUT_PATH = "RQS/" + RQ_NUMBER
OUTPUT_FIGURES_PATH = Util.create_new_dirs(OUTPUT_PATH + "/figures/")

fileName = "res_"+RQ_NUMBER+".txt"
f = open(Path(OUTPUT_PATH) / fileName, "w+")

COLOR_PALETTE_Q1 = {
    "More than 10 years": "#3c758b",
    "7-10 years": "#4095b6",
    "4-6 years": "#53afc9",
    "1-3 years": "#73c0c4",
    "Less than one year": "#94d1bf"
}

#COLOR_PALETTE = ["#00BA38", "#619CFF", "#F8766D", "#00BFC4", "#B79F00", "#F564E3"]

#ORIGINAL
#COLOR_PALETTE = ["#109618", "#fc4e08", "#00afbb", "#e7b900", "#4d87c4", "#FC4E07"]

#CINZA
COLOR_PALETTE = ["#494848", "#636363", "#909090", "#B4B4B4", "#D4D4D4"]

SIZE_BAR_VALUES = 8
CUSTOM_SIZE_AXES_VALUES = 10
CUSTOM_SIZE_Y_AXE_VALUES = 8

# def Q1_countplot():
#     fig, ax = plt.subplots(figsize=(2, 2))
#     sns.countplot(y="q1", data=df, order=df["q1"].value_counts().index, saturation=1, hue="q1", palette=COLOR_PALETTE_Q1, ax=ax)
#     ax.set(xlabel='', ylabel='', title='', yticklabels=[">10", "7-10", "4-6", "<1"])
#     ax.get_yaxis().set_tick_params(labelsize=Util.SIZE_AXES_VALUES, which="major")
#     ax.get_xaxis().set_tick_params(direction='out', labelsize=Util.SIZE_AXES_VALUES)
#     ax.xaxis.set_ticks_position('bottom')
#     # Show graphic
#     plt.tight_layout()
#     plt.savefig(OUTPUT_FIGURES_PATH / 'Q1_countplot.pdf', bbox_inches="tight")
#     plt.savefig(OUTPUT_FIGURES_PATH / 'Q1_countplot.png', bbox_inches="tight")
#     if (SHOW_FIGURE):
#         plt.show()
#     plt.clf()

def Q1_countplot():
    total = len(df)
    fig, ax = plt.subplots(figsize=(3, 1.8))
    sns.countplot(y="q1", data=df, order=df["q1"].value_counts().index, saturation=1, palette=COLOR_PALETTE, ax=ax)
    ax.set(xlabel='', ylabel='', title='', yticklabels=["> 10 years", "7-10 years", "4-6 years", "< 1 year", "0"],  xticks=[0, 10, 20, 30, 40])
    ax.get_yaxis().set_tick_params(labelsize=CUSTOM_SIZE_Y_AXE_VALUES)
    ax.get_xaxis().set_tick_params(direction='out', labelsize=CUSTOM_SIZE_AXES_VALUES, gridOn=False)
    #ax.legend(title="", loc="center right", frameon=False)
    # plt.setp(ax.get_legend().get_texts(), fontsize=Util.SIZE_LEGEND_TEXT)  # for legend text
    # plt.setp(ax.get_legend().get_title(), fontsize=Util.SIZE_LEGEND_TITLE)  # for legend title
    ax.xaxis.set_ticks_position('bottom')
    for p in ax.patches:
        width = p.get_width()
        ratio = str("{:.1%}").format(width/total)
        if width > 30:
            pos_x = width - 12
            color = "white"
            fontweight = "semibold"
        else:
            pos_x = width + 0.1
            color = "black"
            fontweight = "normal"
        legend = f'{width} ({ratio})'
        ax.text(pos_x, p.get_y() + p.get_height() / 2., legend, color=color, fontweight=fontweight, va="center", fontsize=SIZE_BAR_VALUES)

    # Show graphic
    plt.tight_layout()
    plt.savefig(OUTPUT_FIGURES_PATH / 'Q1_countplot.pdf',  bbox_inches="tight")
    plt.savefig(OUTPUT_FIGURES_PATH / 'Q1_countplot.png',  bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()


def Q4_countplot():
    total = len(df)
    fig, ax = plt.subplots(figsize=(3, 1.8))
    sns.countplot(y="q4", data=df, order=['Very knowledgeable (I know all/most classes and methods of it)',
                                          "Knowledgeable (I am familiar with it)",
                                          "Somewhat knowledgeable (I have a vague idea)",
                                          "Not knowledgeable (I do not know anything)"
                                          ], saturation=1,palette=COLOR_PALETTE, ax=ax)
    #ax.set(xlabel='', ylabel='', title='', yticklabels=["Knowledgeable", "Very\nknowledgeable", "Somewhat\nknowledgeable", "Not\nknowledgeable"], xticks=[0, 10, 20, 30, 40])
    ax.set(xlabel='', ylabel='', title='', yticklabels=["Very\nknowledgeable", "Knowledgeable", "Somewhat\nknowledgeable", "Not\nknowledgeable"], xticks=[0, 10, 20, 30, 40])
    ax.get_yaxis().set_tick_params(labelsize=CUSTOM_SIZE_Y_AXE_VALUES, which="major")
    ax.get_xaxis().set_tick_params(direction='out', labelsize=CUSTOM_SIZE_AXES_VALUES, gridOn=False)
    # ax.yaxis.set_label_position("right")
    # ax.yaxis.tick_right()
    #ax.legend(title="", loc="center right", frameon=False)
    # plt.setp(ax.get_legend().get_texts(), fontsize=Util.SIZE_LEGEND_TEXT)  # for legend text
    # plt.setp(ax.get_legend().get_title(), fontsize=Util.SIZE_LEGEND_TITLE)  # for legend title
    ax.xaxis.set_ticks_position('bottom')
    for p in ax.patches:
        width = p.get_width()
        ratio = str("{:.1%}").format(width/total)
        if width > 35:
            pos_x = width - 17
            color = "white"
            fontweight = "semibold"
        else:
            pos_x = width + 0.1
            color = "black"
            fontweight = "normal"
        legend = f'{width} ({ratio})'
        ax.text(pos_x, p.get_y() + p.get_height() / 2., legend, color=color, fontweight=fontweight, va="center", fontsize=SIZE_BAR_VALUES)

    # Show graphic
    plt.tight_layout()
    plt.savefig(OUTPUT_FIGURES_PATH / 'Q4_countplot.pdf',  bbox_inches="tight")
    plt.savefig(OUTPUT_FIGURES_PATH / 'Q4_countplot.png',  bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()

def Q5_countplot():
    total = len(df)
    fig, ax = plt.subplots(figsize=(3, 1.8))
    df_aux = pd.DataFrame(df["q5"].str.split(';').tolist()).stack()
    df_aux = df_aux.reset_index(drop=True)
    #df_aux.rename(index={0: "q5"})
    sns.countplot(y=df_aux, order=df_aux.value_counts(), saturation=1,palette=COLOR_PALETTE, ax=ax)
    ax.set(xlabel='', ylabel='', title='', yticklabels=["expected\nAttribute", "fail\ncall", "assertThrows\nrule", "ExpectedException\nrule", "None"], xticks=[0, 10, 20, 30, 40])
    ax.get_yaxis().set_tick_params(labelsize=CUSTOM_SIZE_Y_AXE_VALUES, which="major")
    ax.get_xaxis().set_tick_params(direction='out', labelsize=CUSTOM_SIZE_AXES_VALUES, gridOn=False)
    # ax.yaxis.set_label_position("right")
    # ax.yaxis.tick_right()
    #ax.legend(title="", loc="center right", frameon=False)
    # plt.setp(ax.get_legend().get_texts(), fontsize=Util.SIZE_LEGEND_TEXT)  # for legend text
    # plt.setp(ax.get_legend().get_title(), fontsize=Util.SIZE_LEGEND_TITLE)  # for legend title
    ax.xaxis.set_ticks_position('bottom')
    for p in ax.patches:
        width = p.get_width()
        ratio = str("{:.1%}").format(width/total)
        if width > 35:
            pos_x = width - 14
            color = "white"
            fontweight = "semibold"
        else:
            pos_x = width + 0.1
            color = "black"
            fontweight = "normal"
        legend = f'{width} ({ratio})'
        ax.text(pos_x, p.get_y() + p.get_height() / 2., legend, color=color, fontweight=fontweight, va="center", fontsize=SIZE_BAR_VALUES)

    # Show graphic
    plt.tight_layout()
    plt.savefig(OUTPUT_FIGURES_PATH / 'Q5_countplot.pdf',  bbox_inches="tight")
    plt.savefig(OUTPUT_FIGURES_PATH / 'Q5_countplot.png',  bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()

def Q7_countplot():
    total = len(df)
    fig, ax = plt.subplots(figsize=(3, 1.8))
    #sns.countplot(y="q7", data=df, order=df["q7"].value_counts().index, saturation=1, palette=COLOR_PALETTE,  ax=ax)
    sns.countplot(y="q7", data=df, order=["Very Important (I always think about it)",
                                          "Important (I usually think about it)",
                                          "Somewhat Important (I rarely think about it)",
                                          "Not Important (I never think about it)"
                                          ],
                  saturation=1, palette=COLOR_PALETTE,  ax=ax)
    ax.set(xlabel='', ylabel='', title='', yticklabels=["Very\nImportant", "Important", "Somewhat\nImportant", "Not\nImportant"], xticks=[0, 10, 20, 30])
    ax.get_yaxis().set_tick_params(labelsize=CUSTOM_SIZE_Y_AXE_VALUES, which="major")
    ax.get_xaxis().set_tick_params(direction='out', labelsize=CUSTOM_SIZE_AXES_VALUES, gridOn=False)
    # ax.yaxis.set_label_position("right")
    # ax.yaxis.tick_right()
    #ax.legend(title="", loc="center right", frameon=False)
    # plt.setp(ax.get_legend().get_texts(), fontsize=Util.SIZE_LEGEND_TEXT)  # for legend text
    # plt.setp(ax.get_legend().get_title(), fontsize=Util.SIZE_LEGEND_TITLE)  # for legend title
    ax.xaxis.set_ticks_position('bottom')
    for p in ax.patches:
        width = p.get_width()
        ratio = str("{:.1%}").format(width/total)
        if width > 20:
            pos_x = width - 9
            color = "white"
            fontweight = "semibold"
        else:
            pos_x = width + 0.1
            color = "black"
            fontweight = "normal"
        legend = f'{width} ({ratio})'
        ax.text(pos_x, p.get_y() + p.get_height() / 2., legend, color=color, fontweight=fontweight, va="center",
               fontsize=SIZE_BAR_VALUES)
    # Show graphic
    plt.tight_layout()
    plt.savefig(OUTPUT_FIGURES_PATH / 'Q7_countplot.pdf',  bbox_inches="tight")
    plt.savefig(OUTPUT_FIGURES_PATH / 'Q7_countplot.png',  bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()

def Q8_countplot():
    total = len(df)
    fig, ax = plt.subplots(figsize=(3, 1.8))
    sns.countplot(y="q8", data=df, order=df["q8"].value_counts().index, saturation=1, palette=COLOR_PALETTE,  ax=ax)
    ax.set(xlabel='', ylabel='', title='', yticklabels=["Does not\nmatter ", "Custom\nExceptions", "Standard/\nThird-party", "None"], xticks=[0, 10, 20, 30, 40])
    ax.get_yaxis().set_tick_params(labelsize=CUSTOM_SIZE_Y_AXE_VALUES, which="major")
    ax.get_xaxis().set_tick_params(direction='out', labelsize=CUSTOM_SIZE_AXES_VALUES, gridOn=False)
    # ax.yaxis.set_label_position("right")
    # ax.yaxis.tick_right()
    #ax.legend(title="", loc="center right", frameon=False)
    # plt.setp(ax.get_legend().get_texts(), fontsize=Util.SIZE_LEGEND_TEXT)  # for legend text
    # plt.setp(ax.get_legend().get_title(), fontsize=Util.SIZE_LEGEND_TITLE)  # for legend title
    ax.xaxis.set_ticks_position('bottom')
    for p in ax.patches:
        width = p.get_width()
        ratio = str("{:.1%}").format(width/total)
        if width > 25:
            pos_x = width - 12
            color = "white"
            fontweight = "semibold"
        else:
            pos_x = width + 0.1
            color = "black"
            fontweight = "normal"
        legend = f'{width} ({ratio})'
        ax.text(pos_x, p.get_y() + p.get_height() / 2., legend, color=color, fontweight=fontweight, va="center", fontsize=SIZE_BAR_VALUES)
    # Show graphic
    plt.tight_layout()
    plt.savefig(OUTPUT_FIGURES_PATH / 'Q8_countplot.pdf',  bbox_inches="tight")
    plt.savefig(OUTPUT_FIGURES_PATH / 'Q8_countplot.png',  bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()

def Q9_countplot():
    total = len(df)
    fig, ax = plt.subplots(figsize=(3, 1.8))
    #sns.countplot(y="q9", data=df, order=df["q9"].value_counts().index, saturation=1, palette=COLOR_PALETTE,  ax=ax)
    sns.countplot(y="q9", data=df, order=[
        "Strongly agree",
        "Agree",
        "Neutral",
        "Disagree",
        "Strongly Disagree"
    ], saturation=1, palette=COLOR_PALETTE,  ax=ax)
    ax.set(xlabel='', ylabel='', title='', yticklabels=["Strongly\nagree", "Agree ", "Neutral", "Disagree", "Strongly\nDisagree"], xticks=[0, 10, 20, 30])
    ax.get_yaxis().set_tick_params(labelsize=CUSTOM_SIZE_Y_AXE_VALUES, which="major")
    ax.get_xaxis().set_tick_params(direction='out', labelsize=CUSTOM_SIZE_AXES_VALUES, gridOn=False)
    # ax.yaxis.set_label_position("right")
    # ax.yaxis.tick_right()
    #ax.legend(title="", loc="center right", frameon=False)
    # plt.setp(ax.get_legend().get_texts(), fontsize=Util.SIZE_LEGEND_TEXT)  # for legend text
    # plt.setp(ax.get_legend().get_title(), fontsize=Util.SIZE_LEGEND_TITLE)  # for legend title
    # Valores em cima das barras
    for p in ax.patches:
        width = p.get_width()
        ratio = str("{:.1%}").format(width/total)
        if width > 20:
            pos_x = width - 9
            color = "white"
            fontweight = "semibold"
        else:
            pos_x = width + 0.1
            color = "black"
            fontweight = "normal"
        legend = f'{width} ({ratio})'
        ax.text(pos_x, p.get_y() + p.get_height() / 2., legend, color=color, fontweight=fontweight, va="center", fontsize=SIZE_BAR_VALUES)

    ax.xaxis.set_ticks_position('bottom')
    # Show graphic
    plt.tight_layout()
    plt.savefig(OUTPUT_FIGURES_PATH / 'Q9_countplot.pdf',  bbox_inches="tight")
    plt.savefig(OUTPUT_FIGURES_PATH / 'Q9_countplot.png',  bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()
#

def Q6_countContinents():
    f.write("\n\n ##############  SURVEY - Q6 ##############\n")
    continentDict = {"united states" : "North America","usa" : "North America","canada" : "North America","united states of america" : "North America",
                "brazil" : "South America",
                "germany" : "Europe","czech republic": "Europe","ukraine": "Europe","sweden": "Europe","finland": "Europe","switzerland": "Europe","france": "Europe","romania": "Europe","norway": "Europe","austria": "Europe","uk": "Europe","poland": "Europe","greece": "Europe","serbia": "Europe","united kingdom": "Europe","belgium": "Europe","italy": "Europe","netherlands": "Europe", "spain": "Europe",
                "hong kong": "Asia", "israel": "Asia", "japan": "Asia",
                "russia": "Eurasia", "turkey": "Eurasia", "russian federation": "Eurasia",
                "australia": "Oceania"}
    total = len(df)
    continentsCounter = {}
    for country in df['q6']:
        country = country.lower().strip()
        continent = continentDict.get(country)
        if continent is None:
            continent = "Undefined"
            f.write(f'Country not identified: {country}\n')
        aux = continentsCounter.get(continent)
        if aux is None:
            continentsCounter[continent] = 1
        else:
            continentsCounter[continent] = aux + 1
    for key, value in continentsCounter.items():
        ratio = str("{:.2%}").format(value / total)
        f.write(f'{key}: {value} ({ratio})\n')




#http://www.albertauyeung.com/post/generating-ngrams-python/
def generate_ngrams(s, n):
    s = s.lower()
    s = re.sub(r'[^a-zA-Z0-9\s]', ' ', s)
    tokens = [token for token in s.split(" ") if token != ""]
    output = list(ngrams(tokens, n))
    return output


# def generateWordCloud(text):
#     stopwords = set(STOPWORDS)
#     #stopwords.update(["drink", "now", "wine", "flavor", "flavors"])
#     wordcloud = WordCloud(stopwords=stopwords, background_color="white").generate(text)
#
#     # Display the generated image:
#     # the matplotlib way:
#     plt.imshow(wordcloud, interpolation='bilinear')
#     plt.axis("off")
#     #plt.show()


# def nGramAnalysis():
#     bigString = ""
#     answersList = df['q10'].astype(str).values.tolist()
#     for aux in answersList:
#         if aux != 'nan':
#             bigString += aux + ' '
#     print(bigString)
#     generateWordCloud(bigString)
#     ngram = generate_ngrams(bigString, 5)
#     print(ngram)


Q1_countplot()
#Q2_countplot()
Q4_countplot()
#Q5_countplot()
Q7_countplot()
Q8_countplot()
Q9_countplot()

Q6_countContinents()

#nGramAnalysis()

#Q1_piechar()