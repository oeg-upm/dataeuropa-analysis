from collections import Counter
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


def draw_words_freq(tags, topk, out_fname=None, palette="ch:.25"):
    c = Counter(tags)
    c = c.most_common(topk)
    data = []
    for tag, num in c:
        data.append([tag, num])

    df = pd.DataFrame(data, columns=["tag", "num"])
    ax = sns.barplot(y="tag", x="num", palette=palette, data=df)
    ax.figure.subplots_adjust(left=0.21)

    if out_fname:
        ax.figure.savefig(out_fname)
    else:
        plt.show()
    plt.clf()

