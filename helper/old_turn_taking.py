import matplotlib.pyplot as plt
import numpy as np
import io
from PIL import Image

def get_tt_graph(x_list):
    plt.figure(figsize=(10, 3))
    plt.title("Turn Taking", fontsize=16, fontweight='bold')

    x = np.array([0] + x_list[:-1])
    y = np.array([0 if i % 2 == 0 else 1 for i in range(len(x))])

    num_turns = len(x)
    conversation_length = x_list[-1]

    labels = ["SOPHIE", "You"]
    colors = ["red" if y_i else "blue" for y_i in y]

    width = [] * num_turns

    for i in range(num_turns + 1):
        if i > 0 and i < num_turns:
            width.append(x[i] - x[i - 1])
        elif i == num_turns:
            width.append(conversation_length - x[i - 1])

    plt.barh(y, width, left=x, color=colors, edgecolor=colors, align='center', height=1)
    plt.ylim(max(y) + 0.5, min(y) - 0.5)
    plt.yticks(np.arange(y.max() + 1), labels, fontsize=12)
    plt.gca().tick_params(axis='x', labelsize=12)

    plt.xlim(0, conversation_length)

    def format_time(value, pos):
        minutes, seconds = divmod(int(value), 60)
        return f"{minutes}:{seconds:02d}"

    plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(format_time))
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