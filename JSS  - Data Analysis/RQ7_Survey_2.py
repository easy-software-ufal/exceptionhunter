import re
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from nltk.util import ngrams

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from sklearn.feature_extraction.text import CountVectorizer

#additional stop words
#from spacy.lang.en.stop_words import STOP_WORDS

from main import Util

# from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
df_survey2 = pd.read_csv("RQs/RQ7-survey_2/Survey2.csv", header=0, names=["s2_timestamp","s2_q1","s2_q2","s2_q3","s2_q4","s2_q5","s2_q6","s2_q7","s2_q8","s2_q9"])


SHOW_FIGURE = False

sns.set(style="whitegrid")


RQ_NUMBER = "RQ7-survey_2"
OUTPUT_PATH = "RQS/RQ7-survey_2/" + RQ_NUMBER
OUTPUT_FIGURES_PATH = Util.create_new_dirs(OUTPUT_PATH + "/figures/")

fileName = "res_"+RQ_NUMBER+".txt"
f = open(Path(OUTPUT_PATH) / fileName, "w+")


#COLOR_PALETTE = ["#00BA38", "#619CFF", "#F8766D", "#00BFC4", "#B79F00", "#F564E3"]

#ORIGINAL
#COLOR_PALETTE = ["#109618", "#fc4e08", "#00afbb", "#e7b900", "#4d87c4", "#FC4E07"]

#GRAY
COLOR_PALETTE = ["#494848", "#636363", "#909090", "#B4B4B4", "#D4D4D4"]

SIZE_BAR_VALUES = 8
CUSTOM_SIZE_AXES_VALUES = 10
CUSTOM_SIZE_Y_AXE_VALUES = 8

def S2_Q4_countplot():
    #discard everything that is not a numeric value
    df_answers_filtered = df_survey2
    df_answers_filtered["s2_q4_filtered"] = df_survey2["s2_q4"].apply(lambda x: x if x.isnumeric() else "Cannot give an answer")
    total = len(df_answers_filtered)
    fig, ax = plt.subplots(figsize=(3, 1.8))
    # sns.countplot(y="q9", data=df, order=df["q9"].value_counts().index, saturation=1, palette=COLOR_PALETTE,  ax=ax)

    sns.countplot(y="s2_q4_filtered", data=df_answers_filtered, order=[
        "5",
        "10",
        "20",
        "25",
        "40",
        "50",
        "Cannot give an answer"
    ], saturation=1, palette=COLOR_PALETTE, ax=ax)
    ax.set(xlabel='', ylabel='', title='',
           yticklabels=["5%", "10%", "20%", "25%", "40%", "50%", "Cannot give\nan answer"],
           xticks=[0, 1, 2, 3, 4])
    ax.get_yaxis().set_tick_params(labelsize=CUSTOM_SIZE_Y_AXE_VALUES, which="major")
    ax.get_xaxis().set_tick_params(direction='out', labelsize=CUSTOM_SIZE_AXES_VALUES, gridOn=False)
    # ax.yaxis.set_label_position("right")
    # ax.yaxis.tick_right()
    # ax.legend(title="", loc="center right", frameon=False)
    # plt.setp(ax.get_legend().get_texts(), fontsize=Util.SIZE_LEGEND_TEXT)  # for legend text
    # plt.setp(ax.get_legend().get_title(), fontsize=Util.SIZE_LEGEND_TITLE)  # for legend title
    # Valores em cima das barras
    for p in ax.patches:
        width = p.get_width()
        ratio = str("{:.1%}").format(width / total)
        if width > 3:
            pos_x = width - 1.1
            color = "white"
            fontweight = "semibold"
        else:
            pos_x = width + 0.1
            color = "black"
            fontweight = "normal"
        legend = f'{width} ({ratio})'
        ax.text(pos_x, p.get_y() + p.get_height() / 2., legend, color=color, fontweight=fontweight, va="center",
                fontsize=SIZE_BAR_VALUES)

    ax.xaxis.set_ticks_position('bottom')

    # Show graphic
    plt.tight_layout()
    plt.savefig(OUTPUT_FIGURES_PATH / 'Q7_S2_countplot.pdf',  bbox_inches="tight")
    plt.savefig(OUTPUT_FIGURES_PATH / 'Q7_S2_countplot.png',  bbox_inches="tight")
    if (SHOW_FIGURE):
        plt.show()
    plt.clf()


#http://www.albertauyeung.com/post/generating-ngrams-python/
def generate_ngrams(s, n):
    s = s.lower()
    s = re.sub(r'[^a-zA-Z0-9\s]', ' ', s)
    tokens = [token for token in s.split(" ") if token != ""]
    output = list(ngrams(tokens, n))
    return output


def generateWordCloud():
    stopwords = set(STOPWORDS)
    #stopwords.update(["drink", "now", "wine", "flavor", "flavors"])

    text = df_survey2['s2_q6'].astype(str).values.tolist()
    text = ' '.join(text).lower()
    text_list = [text]

    #wordcloud = WordCloud(stopwords=stopwords, collocations=True, collocation_threshold=10, background_color="white", min_word_length=4).generate(text)
    cv = CountVectorizer(stop_words=stopwords, ngram_range=(2, 3))
    # fit transform our text and create a dataframe with the result
    X = cv.fit_transform(text_list)
    X = X.toarray()
    # print(cv.get_feature_names())
    # print(X)
    bow=pd.DataFrame(X, columns=cv.get_feature_names())
    print(bow.shape)

    new_text = bow.iloc[0].sort_values(ascending=False)[:5000]
    # create a dictionary Note: you could pass the pandas Series directoy into the wordcloud object
    text2_dict = bow.iloc[0].sort_values(ascending=False).to_dict()

    wordcloud = WordCloud(min_word_length=5, background_color='white')
    # generate the word cloud
    wordcloud.generate_from_frequencies(text2_dict)
    # plot
    plt.figure(figsize=(8, 4))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()





def nGramAnalysis():
    bigString = ""
    answersList = df_survey2['s2_q6'].astype(str).values.tolist()
    for aux in answersList:
        if aux != 'nan':
            bigString += aux + ' '
    print(bigString)
    generateWordCloud(bigString)
    #ngram = generate_ngrams(bigString, 5)
    #print(ngram)


S2_Q4_countplot()
#S2_Q4_histogram()
#nGramAnalysis()

#generateWordCloud()

#Q1_piechar()