#共焦点XRDを読み込んでグラフを書いてみる。s

import tkinter
from tkinter.filedialog import askopenfilenames

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# フォルダの指定--------------------------------------------
root = tkinter.Tk()
root.withdraw()
File_Link = askopenfilenames(
    filetypes=(("All files", "*.*"), ("HTML files", "*.html;*.htm"), ("out files", "*.out")))  # ファイルを選択
Length_Link = len(File_Link)  # ファイルの長さを計算
# -----------------------------------------------------------
DATA = []
df_S1S2 = []
df_S1 = []
df_S2 = []
df_S3 = []#空っぽ定義
# 繰り返す---------------------------------------------------
for i in range(Length_Link):
    df = pd.read_fwf(File_Link[i])  # ファイルの読み込み
    # データフレームで処理されるので以下でnumpyやリストに加工する。
    data = df        #フラットにはしないのでこれはカット　.values.flatten()
    # ここから↓に処理を記載。
    Gr = data[(data['space_d'] > 3.330) & (data['space_d'] < 3.365)]
    Stage1 = data[(data['space_d'] > 3.65) & (data['space_d'] < 3.71)]
    Stage2 = data[(data['space_d'] > 3.48) & (data['space_d'] < 3.55)]
    Stage3 = data[(data['space_d'] > 3.437) & (data['space_d'] < 3.497)]
    Grmax = np.max(Gr['counts'])
    S1max = np.max(Stage1['counts'])
    S2max = np.max(Stage2['counts'])
    S3max = np.max(Stage3['counts'])
    S1S2ratio = S1max/S2max

    sns.set()
    sns.set_palette("hls",50,desat=0.6,)
    plt.plot(data['space_d'], data['counts']+200*i)
    plt.ylabel('Intensity')
    plt.xlabel('d space/nm')
    plt.show()

    # 何か出力を保存したい場合はリストに追加する。
    df_S1.append(S1max)
    df_S2.append(S2max)
    df_S3.append(S3max)
    df_S1S2.append(S1S2ratio)
    DATA.append(data)
    # これでfor文で追加した内容がリストに追加されていきます。

plt.figure()#ここから↓のグラフは別口につくる。
plt.subplot(221)
plt.plot(df_S1)
plt.xlabel('sample No.')
# plt.ylabel('Stage 1 Intensity')

plt.subplot(222)
plt.plot(df_S2)
plt.xlabel('Sample No.')
plt.ylabel('Stage 2 Intensity')

plt.subplot(223)
plt.plot(df_S3)
plt.xlabel('Sample No.')
plt.ylabel('Stage 3 Intensity')

plt.subplot(224)
plt.plot(df_S1S2)
plt.xlabel('Sample No.')
plt.ylabel('Stage1/Stage2 Ratio')

plt.show()

# 最後にDATAを保存すればok。pandasに直してcsv保管など・・・。
