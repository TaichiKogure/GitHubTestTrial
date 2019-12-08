import tkinter
from tkinter.filedialog import askopenfilenames

import pandas as pd

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
df_S3 = []  # 空っぽ定義
# 繰り返す---------------------------------------------------
# for i in range(Length_Link):
df = pd.read_fwf(File_Link)  # ファイルの読み込み
