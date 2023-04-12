from collections import Counter
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


def draw_words_freq(tags, topk, out_fname=None, palette="ch:.25", ylabel="Tag"):
    c = Counter(tags)
    c = c.most_common(topk)
    data = []
    for tag, num in c:
        data.append([tag, num])

    df = pd.DataFrame(data, columns=[ylabel, "Number"])
    ax = sns.barplot(y=ylabel, x="Number", palette=palette, data=df)
    ax.figure.subplots_adjust(left=0.21)

    if out_fname:
        ax.figure.savefig(out_fname)
        if out_fname[-3:] == "svg":
            ax.figure.savefig(out_fname[:-3]+"png")
    else:
        plt.show()
    plt.clf()

