from collections import Counter
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


def draw_cat_per_sub(d, out_fname=None):
    data = []
    for sub in d:
        for cat in d[sub]['categories']:
            val = d[sub]['categories'][cat]

            line = [sub, cat, val]
            data.append(line)

    df = pd.DataFrame(data, columns=["subreddit", "Category", "Occurrences"])
    ax = sns.barplot(y="Occurrences", x="subreddit", hue="Category", palette="viridis", data=df)
    ax.figure.subplots_adjust(left=0.2)

    if out_fname:
        ax.figure.savefig(out_fname)
    else:
        plt.show()
