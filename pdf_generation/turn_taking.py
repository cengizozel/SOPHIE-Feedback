import matplotlib.pyplot as plt
import numpy as np
import io
from PIL import Image

def get_tt_graph():
    plt.figure(figsize=(10, 3))
    plt.title("Turn Taking", fontsize=16, fontweight='bold')

    # ending points of each turn
    x = np.array([0, 2, 6, 7, 9, 10, 12, 13])
    # 0 means sophie, 1 means you
    y = np.array([0, 1, 0, 1, 0, 1, 0, 1])

    num_turns = len(x)
    conversation_length = 15

    labels = ["SOPHIE", "You"]
    colors = ["red" if y_i else "blue" for y_i in y]

    # example width array
    # width = [2, 4, 1, 2, 1, 2, 1, 2]
    # width should have length of x
    width = [] * num_turns

    for i in range(num_turns+1):
        if i > 0 and i < num_turns:
            width.append(x[i] - x[i-1])
        elif i == num_turns:
            width.append(conversation_length - x[i-1])

    # print(width)

    plt.barh(y, width, left=x, color = colors, edgecolor = colors, align='center', height=1)
    plt.ylim(max(y)+0.5, min(y)-0.5)
    plt.yticks(np.arange(y.max()+1), labels, fontsize=12)
    plt.gca().tick_params(axis='x', labelsize=12)
    # x should start at 0 and end at the last x value + 1
    plt.xlim(0, conversation_length)

    # plt.show()

    # convert plot to PIL image and return
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img = Image.open(buf)

    # resize image
    # img = img.resize((int(width/4), int(height/4)), Image.ANTIALIAS)

    # show image
    # img.show()
    # print(img.size)

    return img

# get_tt_graph()