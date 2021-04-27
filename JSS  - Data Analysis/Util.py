import os
import math
from pathlib import Path
from datetime import datetime, timedelta
from calendar import monthrange
from scipy import stats
from numpy import percentile
from pymongo import MongoClient



mongo_client = MongoClient('mongodb://localhost:27017/')
mongo_db = mongo_client['ExceptionHunter']
mongo_collection = mongo_db['ExceptionDB_WithCoverage']

SIZE_AXES_LABELS = "large"
SIZE_AXES_VALUES = "medium"
SIZE_AXES_TITLE = "large"
SIZE_BAR_VALUES = "medium"
SIZE_LEGEND_TITLE = "large"
SIZE_LEGEND_TEXT = "medium"


## ORIGINAL ###
COLOR_PALETTE_COLORFUL = {
    "Frameworks": "#1f77b4",
    "Libraries": "#ff7f0e",
    "Tools": "#2ca02c",
    "Desktop/Server": "#1eae28",
    "Mobile": "#f25e5a",
    "Multi-platform": "#4c88ff"
}

### GRAY ###
COLOR_PALETTE = {
    "Frameworks": "#1f77b4",
    "Libraries": "#ff7f0e",
    "Tools": "#2ca02c",
    "Desktop/Server": "#eeeeee",
    "Mobile": "#bbbbbb",
    "Multi-platform": "#636363"
}

LABELS = ["ZERO", "> ZERO"]

COLOR_DEGRADE = {
    LABELS[0]: "#abd0e6",
    LABELS[1]: "#1b69af",
}

FIGURE_ORDER = ["Desktop/Server", "Mobile", "Multi-platform"]

def create_new_dirs(path):
    output_path = Path(path)
    output_path.mkdir(parents=True, exist_ok=True)
    return output_path

def adjust_domain_name(domain):
    new_domain_name = ""
    if domain == "framework":
        new_domain_name = "Frameworks"
    elif domain == "library":
        new_domain_name = "Libraries"
    elif domain == "tool":
        new_domain_name = "Tools"
    return new_domain_name


def count_number_of_projects_gte_to_ratio(df_aux, column_name, value, f):
    platform_list = df_aux["platform"].unique()
    domain_list = df_aux["domain"].unique()

    df_greater_or_equal_to = df_aux[(df_aux[column_name] >= value)]
    f.write(f'{column_name} >= {value} | Total:  {str(len(df_greater_or_equal_to))} out of {str(len(df_aux))} {str("({:.2%})").format(len(df_greater_or_equal_to) / len(df_aux))}\n')
    for platform in platform_list:
        df_platform_total = df_aux[(df_aux['platform'] == platform)]
        df_greaterOrEqual_aux1 = df_platform_total[(df_platform_total[column_name] >= value)]
        f.write(f'{column_name} >= {value} | {platform} : {str(len(df_greaterOrEqual_aux1))} out of {str(len(df_platform_total))}  {str("({:.2%})").format(len(df_greaterOrEqual_aux1) / len(df_platform_total))}\n')
        for domain in domain_list:
            df_domain_total = df_platform_total[(df_platform_total["domain"] == domain)]
            df_greaterOrEqual_aux2 = df_domain_total[(df_domain_total[column_name] >= value)]
            f.write(f'{column_name} >= {value} | {platform}/{domain} : {str(len(df_greaterOrEqual_aux2))} out of {str(len(df_domain_total))}  {str("({:.2%})").format(len(df_greaterOrEqual_aux2) / len(df_domain_total))}\n')

def evaluate_outliers(df, name_of_column, f):
    f.write('\n*** START OF OUTLIERS EVALUATION *** \n')
    platform_list = df["platform"].unique()
    for platform in platform_list:
        df_aux = df[(df['platform'] == platform)]
        data_full = df_aux[name_of_column]
        data = data_full.dropna()
        stat, p = stats.shapiro(data)
        f.write(platform + " - " + name_of_column + ' | Distribution: Statistics=%.3f, p=%.3f' % (stat, p) + '\n')
        # interpret
        alpha = 0.05
        if p > alpha:
            f.write(platform + " - " + name_of_column + ' | Distribution looks Gaussian (fail to reject H0) \n')
        else:
            f.write(platform + " - " + name_of_column + ' | Distribution does not look Gaussian (reject H0) \n')
        # calculate interquartile range
        q25, q75 = percentile(data, 25), percentile(data, 75)
        iqr = q75 - q25
        f.write(platform + " - " + name_of_column + ' | Percentiles: 25th=%.3f, 75th=%.3f, IQR=%.3f' % (q25, q75, iqr) + '\n')
        # calculate the outlier cutoff
        k = 1.5
        cut_off = iqr * k
        lower, upper = q25 - cut_off, q75 + cut_off
        # identify outliers
        outliers = [x for x in data if x < lower or x > upper]
        outliers_rate = len(outliers)/data_full.size
        #print(data.size)
        f.write(platform + " - " + name_of_column + " | Identified outliers: " + str(sorted(outliers)) + " | Outliers observations: %d" % len(outliers) + " out of " + str(data.size) + str("({:.2%})").format(outliers_rate) + "\n")
        # remove outliers
        outliers_removed = [x for x in data if x >= lower and x <= upper]
        f.write(platform + " - " + name_of_column + ' | Non-outlier observations: %d' % len(outliers_removed) + "\n")
    f.write('\n*** END OF OUTLIERS EVALUATION *** \n')
    return df

def format_to_latex(df_aux, name_of_columns_to_latex, output_path, file_name):
    file_name += ".latex"
    output_file = os.path.join(output_path, file_name)
    f = open(output_file, "w+")
    for index, row in df_aux.iterrows():
        f.write("& & ")
        for key in name_of_columns_to_latex:
            value = row.get(key)
            if index != "count" and "/" in key:
                if math.isnan(value):
                    f.write("NaN")
                else:
                    f.write(str("{:.2%}").format(value).replace("%", "\%").replace(".00", ""))
            elif index != "count":
                if math.isnan(value):
                    f.write("NaN")
                else:
                    f.write(str("{:,.2f}").format(value).replace(".00", ""))
            else:
                f.write(str(value).replace(".0", ""))
            f.write(" & ")
        f.write("{\\bf " + index.replace("%", "\%") + "}\\\\ \n")
    f.close()



def format_to_csv(df, outputdir, table_name, name_prefix, name_of_columns_to_latex):
    table_name += ".csv"
    output_path = create_new_dirs(outputdir)
    df.to_csv(output_path / table_name, index=False, na_rep="NaN", sep=";")
    platformList = df["platform"].unique()
    domainList = df["domain"].unique()
    for platform in platformList:
        filePath = name_prefix + "_" + platform.replace("/", "#") + "_description"
        df_described = df.loc[(df['platform'] == platform)].describe().round(4)
        filePath += ".csv"
        df_described.to_csv(
            output_path / filePath, index=True,
            na_rep="NaN", sep=";")
        format_to_latex(df_described, name_of_columns_to_latex, output_path, filePath)
        for domain in domainList:
            filePath = name_prefix + "_" + platform.replace("/", "#") + "_" + domain + "_description"
            df_described_aux = df.loc[
                (df['platform'] == platform) & (df['domain'] == domain)].describe().round(4)
            filePath += ".csv"
            df_described_aux.to_csv(
                output_path / filePath, index=True,
                na_rep="NaN", sep=";")
            format_to_latex(df_described_aux, name_of_columns_to_latex, output_path, filePath)

#https://stackoverflow.com/questions/7015587/python-difference-of-2-datetimes-in-months
def calculate_month_delta(d1, d2):
    delta = 0
    while True:
        mdays = monthrange(d1.year, d1.month)[1]
        d1 += timedelta(days=mdays)
        if d1 <= d2:
            delta += 1
        else:
            break
    return delta

def autolabelVertical(rects, ax, xpos='center'):
    """
    Attach a text label above each bar in *rects*, displaying its height.

    *xpos* indicates which side to place the text w.r.t. the center of
    the bar. It can be one of the following {'center', 'right', 'left'}.
    """

    xpos = xpos.lower()  # normalize the case of the parameter
    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
    offset = {'center': 0.5, 'right': 0.57, 'left': 0.43}  # x_txt = x + w*off

    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() * offset[xpos], 1.01 * height,
                '{}'.format(height), ha=ha[xpos], va='bottom')

def autolabel_horizontal(rects, ay, ypos='center'):
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
        ay.text(1.01 * width, rect.get_y() + rect.get_height() * offset[ypos],
                '{}'.format(width), va=va[ypos], ha='left')