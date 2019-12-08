# https://stjun.hatenablog.com/entry/2019/07/27/193233
# ↑から引用

import tkinter as tk
import tkinter.filedialog as fl
import tkinter.messagebox as mb

import numpy as np

root = tk.Tk()


# ファイルパスをマウスで選ぶ
# ユーザー名にお使いのPCの名前を入れてください
def get():
    filetype = [("all file", "*")]
    path = fl.askopenfilename(initialdir="C:/Users/ユーザー名/Desktop", filetypes=filetype)
    mb.showinfo("pathの表示", path)

    # 以下は前回と同じ、CSVファイルのデータを読み込み表示させる
    data_1, data_2, data_3 = np.loadtxt(fname=path, skiprows=2, unpack=True)
    print(data_1)
    print(data_2)
    print(data_3)


button = tk.Button(text="開く", command=get)
button.pack()

root.mainloop()
