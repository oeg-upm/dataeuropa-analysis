import matplotlib.pyplot as plt
from wordcloud import WordCloud

colormaps={'code':'viridis','commits':'plasma','repositories':'inferno','issues':'magma'}
def plot_wordcloud_github(target,tokens,outFname=None):
    text=' '.join(tokens)
    word_cloud=WordCloud(collocations=False,background_color='white',colormap=colormaps[target]).generate(text)
    plt.title(target.capitalize(),fontsize=30,fontweight='bold')
    plt.imshow(word_cloud, interpolation='bilinear')
    plt.axis("off")
    if outFname:
        plt.savefig(outFname)
    else:
        plt.show()
    plt.clf()
