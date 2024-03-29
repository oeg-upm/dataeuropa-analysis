from collections import Counter
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


def draw_cat_per_sub(d, out_fname=None, palette="mako"):
    data = []
    for sub in d:
        for cat in d[sub]['categories']:
            val = d[sub]['categories'][cat]

            line = [sub, cat, val]
            data.append(line)

    df = pd.DataFrame(data, columns=["Subreddit", "Category", "Occurrences"])
    ax = sns.barplot(y="Occurrences", x="Subreddit", hue="Category", palette=palette, data=df)
    ax.figure.subplots_adjust(bottom=0.5)
    plt.xticks(rotation=90)
    if out_fname:
        ax.figure.savefig(out_fname)
        if out_fname[-3:] == "svg":
            ax.figure.savefig(out_fname[:-3]+"png")
    else:
        plt.show()
    plt.clf()


def draw_count(cat_counter, out_fname=None, palette="mako", rotation=0, margins={'bottom': 0.1}):
    data = []
    for cat in cat_counter:
        val = cat_counter[cat]
        line = [cat, val]
        data.append(line)

    df = pd.DataFrame(data, columns=["Category", "Occurrences"])
    ax = sns.barplot(y="Occurrences", x="Category", palette=palette, data=df)
    if margins:
        print("margins: ")
        print(margins)
        ax.figure.subplots_adjust(**margins)
        #ax.figure.subplots_adjust(bottom=0.55)
    plt.xticks(rotation=rotation)
    if out_fname:
        ax.figure.savefig(out_fname)
        if out_fname[-3:] == "svg":
            ax.figure.savefig(out_fname[:-3]+"png")
    else:
        plt.show()
    plt.clf()
