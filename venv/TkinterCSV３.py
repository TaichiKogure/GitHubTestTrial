import tkinter
from tkinter.filedialog import askopenfilename

import pandas as pd

# フォルダの指定--------------------------------------------
root = tkinter.Tk()
root.withdraw()
file = askopenfilename(
    filetypes=(("All files", "*.*"), ("HTML files", "*.html;*.htm"), ("csv files", "*.csv")))  # ファイルを選択
df = pd.read_csv(file)

# df = pd.read_csv('C:/Users/auror/Downloads/AirPassengers.csv')
# Length_Link = len(File_Link)  # ファイルの長さを計算
# 繰り返す---------------------------------------------------
# for i in range(Length_Link):
# df = pd.read_csv(File_Link)  # ファイルの読み込み
# df = pd.read_csv(File_Link)
# df = pd.read_csv(io.BytesIO(File_Link), parse_dates=["Month"], index_col=["Month"], dtype={'#Passengers': 'float'})


print(df)

