from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd
import io
from PIL import Image

def get_word_cloud(title, words_list):
    words = " ".join(words_list)
    # print("Generating word cloud for " + str(words))

    # I don't want to use default stopwords
    stopwords = set()

    # if words_list is empty, return empty image
    if len(words_list) == 0:
        return Image.new('RGB', (800, 800), color = 'white')
    
    wordcloud = WordCloud(width = 800, height = 800,
                    background_color ='white',
                    stopwords = stopwords,
                    min_font_size = 20).generate(words)
    
    # plot the WordCloud image                      
    plt.figure(figsize = (8, 8), facecolor = None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.title(title, fontsize=28, fontweight='bold')
    plt.tight_layout(pad = 0)
    # plt.show()

    # convert plot to PIL image and return
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img = Image.open(buf)

    return img
