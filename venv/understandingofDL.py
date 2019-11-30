# 9月号　ディープラーニングの本質を理解する。　87ページ

import matplotlib.pyplot as plt
import numpy as np

#from IPython.display import set_matplotlib_formats
#set_matplotlib_formats('png','pdf')

#学習データの設定
data = np.array([[166,58.7],[176,75.7],[171,62.1],[173,70.4],[169,60.1]])

plt.scatter(data[:,0],data[:,1],s = 40, c='b')
plt.grid
plt.show()
