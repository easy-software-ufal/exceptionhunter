import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as stats
from scipy.stats import mannwhitneyu
from main import Util

SHOW_FIGURE = False
output_statistics_path = ""

#REFS
#https://machinelearningmastery.com/nonparametric-statistical-significance-tests-in-python/
#https://machinelearningmastery.com/parametric-statistical-significance-tests-in-python/

############################## RQ2 - TTEST ##############################
def compareDataSamples(serie1, serie2, title, outputPath):
    output_statistics_path = Util.create_new_dirs("outputPath")
    fileName = "res_CompareDataSamples_" + title + ".txt"
    f = open(output_statistics_path / fileName, "w+")
    f.write("CompareDataSamples_" + fileName + "\n")
    stat, p1 = stats.shapiro(serie1)
    f.write(' Serie1  Distribution: Statistics=%.5f, p=%.5f' % (stat, p1) + "\n")
    stat, p2 = stats.shapiro(serie2)
    f.write(' Serie2  Distribution: Statistics=%.5f, p=%.5f' % (stat, p2) + "\n")
    diff = serie1 - serie2
    stat, p3 = stats.shapiro(diff)
    f.write(' Diff Distribution: Statistics=%.5f, p=%.5f' % (stat, p3) + "\n")
    # interpret
    alpha = 0.05
    if p1 > alpha and p2 > alpha and p3 > alpha:
        f.write('Distribution looks Gaussian (fail to reject H0). Proceed with Student’s t-test\n')
        TTestEvaluation(serie1, serie2, title, f)
    else:
        f.write('Distribution does not look Gaussian (reject H0). Proceed with Mann-Whitney U\n')
        mannwhitneyuEvaluation(serie1, serie2, title, f)
    f.write("******************")
    f.close()

def TTestEvaluation(serie1, serie2, title, f):
    stat, p = stats.ttest_ind(serie1, serie2, equal_var= False)
    f.write('TTest Result | stat: %.5f, p=%.5f' % (stat, p) + "\n")
    # interpret
    alpha = 0.05
    if p > alpha:
        f.write('Same distributions (fail to reject H0)\n')
    else:
        f.write('Different distributions (reject H0)\n')

def mannwhitneyuEvaluation(serie1, serie2, title, f):
    stat, p = stats.mannwhitneyu(serie1, serie2)
    f.write('MannWhitney Result | stat: %.5f, p=%.5f' % (stat, p)+ "\n")
    # interpret
    alpha = 0.05
    if p > alpha:
        f.write('Same distributions (fail to reject H0)\n')
    else:
        f.write('Different distributions (reject H0)\n')


def evaluateCorrelation(df, column1, column2, checkDomains, f):
    platformList = df["platform"].unique()
    domainList = df["domain"].unique()
    f.write("\n")
    for platform in platformList:
        df_platform = df[df['platform'] == platform]
        correlation, p_value = stats.spearmanr(df_platform[column1], df_platform[column2])
        f.write(platform + "_Correlation (" + column1 + " x " + column2 + "): " + str(
            correlation) + " pvalue: " + str(p_value)  + "\n")
        if checkDomains:
            for domain in domainList:
                df_domain = df_platform[(df_platform["domain"] == domain)]
                correlation, p_value = stats.spearmanr(df_domain[column1], df_domain[column2])
                f.write(platform + "_" + domain + "_Correlation (" + column1 +" x " + column2 + "): " + str(correlation) + " pvalue: " + str(p_value)  + "\n")

