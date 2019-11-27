import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from scipy.stats import multivariate_normal

# ////////////////////////////////////////
#二次元の正規分布をグラフで表示する
#//////////////////////////////////////////

#データの設定
x, y = np.mgrid[10:100:1, 10:100:1]

pos = np.empty(x.shape + (2, ))

pos[:, :, 0] = x
pos[:, :, 1] = y

#↑はXとYのデータは10から100まで２つづつ作成してposとしてまとめたいもの、正規分布可視化のためにｘとｙでデータを刻んでいるだけ


#多次元正規分布
# それぞれ変数の平均と分散共分散行列を設定
# 以下の例ではｘとｙの平均がそれぞれ50と50、[[100,0],[0,100]]がｘとｙの共分散行列になる。

rv = multivariate_normal([50,50],[[100,0],[0,100]])

#確率密度関数
z = rv.pdf(pos)

fig = plt.figure(dpi = 100)

ax = Axes3D(fig)
ax.plot_wireframe(x,y,z)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

#z軸の表示メモリ痰飲を変更SCIが指数表示、axixで軸を指定scilimits=(n.m)はｎからｍの外にあるものは指数表記
#scilimits = (0,0) はすべて指数表記にするという意味
ax.ticklabel_format(style = 'sci' , axis= 'z', scilimits=(0,0))




