import matplotlib.pyplot as plt
from wordcloud import WordCloud

colormaps={'code':'viridis','commits':'plasma','repositories':'inferno','issues':'magma'}
def plot_wordcloud_github(target,tokens):
    text=' '.join(tokens)
    word_cloud=WordCloud(collocations=False,background_color='white',colormap=colormaps[target]).generate(text)
    plt.title(target.capitalize(),fontsize=30,fontweight='bold')
    plt.imshow(word_cloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig("../github_" + target + ".svg")
    plt.show()
