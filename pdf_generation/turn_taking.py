import matplotlib.pyplot as plt
import numpy as np

x = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])
y = np.array([0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1])

labels = ["SOPHIE", "You"]
colors = ["red" if y_i else "blue" for y_i in y]
plt.barh(y, [1]*len(x), left=x, color = colors, edgecolor = colors, align='center', height=1)
plt.ylim(max(y)+0.5, min(y)-0.5)
plt.yticks(np.arange(y.max()+1), labels)
plt.show()