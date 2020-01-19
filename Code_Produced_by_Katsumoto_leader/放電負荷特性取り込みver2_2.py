'''
Created on 2018/04/05

@author: MM12069
'''
import datetime
import tkinter
from tkinter.filedialog import askopenfilenames

import numpy as np
import pandas as pd

# ファイル読み込みの手法
today = datetime.datetime.now()
year = today.year
month = today.month
day = today.day
hour = today.hour
minute = today.minute
second = today.second
if (month < 10):
    month = str(0) + str(month)
else:
    month = str(month)
if (day < 10):
    day = str(0) + str(day)
else:
    day = str(day)
if (hour < 10):
    hour = str(0) + str(hour)
else:
    hour = str(hour)
if (minute < 10):
    minute = str(0) + str(minute)
else:
    minute = str(minute)
if (second < 10):
    second = str(0) + str(second)
else:
    second = str(second)
time_stamp = str(year) + month + str(day) + str(hour) + str(minute) + str(second)

# Listファイルの選択
root = tkinter.Tk()
root.withdraw()
args = askopenfilenames(filetypes=(("All files", "*.*"), ("HTML files", "*.html;*.htm"), ("csv files", "*.csv")))
# データフレームの取り込み
df1 = pd.read_excel(args[0], sheetname="C-V", encodint="cp932", skiprows=1)  # 容量電圧
df1_2 = pd.read_excel(args[0], sheetname="T-I", encodint="cp932", skiprows=1)  # 時間電流
df2 = pd.read_excel(args[0], sheetname="Condition", encodint="cp932")  # 使用データ
df3 = pd.read_excel(args[0], sheetname="Temp_data", encodint="cp932", skiprows=1)  # 容量温度
df2 = df2.dropna(how="all", axis=0)  # NaNがいるとfloat表記になるので、必要に応じてint型へ。
# 条件検索用データ
start_cyc = np.array(df2["Start_cycle"].values.flatten())  # スタートサイクル数
Finish_cyc = np.array(df2["Finish_cycle"].values.flatten())  # フィニッシュサイクル数
cycle_num = np.array(df2["Cycle_number"].values.flatten())  # サイクル数
Gen_vol = np.array(df2["Gen_vol"].values.flatten())  # サイクル数
# 取り込みデータ
Lot = np.array(df2["Cell-Lot"].values.flatten())  # セルロット
capa_1C = np.array(df2["min_rated_capacity[mAh]"].values.flatten())  # 1C容量
temp_data = np.array(df2["temp_data"].values.flatten())  # 温度データがあるかないか
Gen = np.array(df2["Gen"].values.flatten())  # 世代
size = np.array(df2["size"].values.flatten())  # サイズ
day = np.array(df2["Day"].values.flatten())  # 日時
RestC = np.array(df2["Rest_afterC[min]"].values.flatten())  # 充電後レスト時間
RestD = np.array(df2["Rest_afterD[min]"].values.flatten())  # 放電後レスト時間
Charge_rate = np.array(df2["Charge-rate[C]"].values.flatten())  # 充電レート
Charge_vol = np.array(df2["Charge-voltage[V]"].values.flatten())  # 充電電圧
Charge_cut_rate = np.array(df2["Charge-cut-rate[C]"].values.flatten())  # 充電カットレート
TEMP = np.array(df2["Temp[deg.C]"].values.flatten())  # 測定データ
eq = np.array(df2["Test_equipment"].values.flatten())  # 測定装置
ch = np.array(df2["ch"].values.flatten())  # 測定ch
cut_vol = np.array(df2["Discharge-cut-voltage[V]"].values.flatten())  # 放電カット電圧
min_Energy = np.array(df2["min_rated_Energy[Wh]"].values.flatten())  # 放電カット電圧
Measurer = np.array(df2["Measurer"].values.flatten())  # 測定者
# 計算に使う値
dod = np.arange(0, 100.5, 0.5)  # DOD200point
Lot_len = len(Lot)  # ロットを読み込んだ数
print("繰り返し数")
print(Lot_len)
for i in range(Lot_len):  # 2×スタートサイクル-1～2×フィニッシュサイクル
    print(Lot[i])
    dF1 = df1.iloc[:, 1:2 * int(Finish_cyc[Lot_len - 1]) + 1]  # 1列目の削除
    dF1 = dF1.iloc[:, 2 * (int(start_cyc[i]) - 1):2 * int(Finish_cyc[i])]  # 水準毎に分割
    dF1_2 = df1_2.iloc[:, 1:2 * int(Finish_cyc[Lot_len - 1]) + 1]  # 1列目の削除
    dF1_2 = dF1_2.iloc[:, 2 * (int(start_cyc[i]) - 1):2 * int(Finish_cyc[i])]  # 水準毎に分割
    for k in range(int(cycle_num[i])):  # サイクル数分データを取得
        C_Rate = np.array(df2[k].values.flatten())[i]
        save_name = "save" + str(k) + "_DOD"
        save_raw = "save" + str(k) + "_Raw"
        file = np.array(df2[save_name].values.flatten())
        file2 = np.array(df2[save_raw].values.flatten())
        save_file = file[i]
        Raw_file = file2[i]
        DF1 = dF1.iloc[:, 2 * (k):2 * (k + 1)]  # kサイクル目の容量電圧データ
        DF1 = DF1.dropna(axis=0)
        DF1.columns = ["Capacity[mAh]", "Voltage[V]"]
        DF1_2 = dF1_2.iloc[:, 2 * (k):2 * (k + 1)]  # kサイクル目の容量電圧データ
        DF1_2 = DF1_2.dropna(axis=0)
        DF1_2.columns = ["Time[min]", "Current[mA]"]


        def DOD_curve(x):  # カット電圧におけるDODカーブ、カット電圧ごとのカーブを求めるわけではない。
            capa = np.array(DF1["Capacity[mAh]"].values.flatten())
            vol = np.array(DF1["Voltage[V]"].values.flatten())
            min_vol = min(vol)
            arg_min_vol = np.argmin(vol)
            # 最終電圧がカットvoltageと同じ場合
            if (min_vol == cut_vol[x]):
                capa_cutV = capa[arg_min_vol - 1]
                capa_dod = capa / capa_cutV * 100
                cal_V = np.interp(dod, capa_dod, vol)
            # 最終電圧がカットvoltageより小さい場合
            elif (min_vol < cut_vol[x]):
                capa_cutV = capa[arg_min_vol - 1] + (capa[arg_min_vol - 2] - capa[arg_min_vol - 1]) * (
                        cut_vol[x] - vol[arg_min_vol - 1]) / (vol[arg_min_vol - 2] - vol[arg_min_vol - 1])
                capa_dod = capa / capa_cutV * 100
                cal_V = np.interp(dod, capa_dod, vol)
            # 最終電圧がカットvoltageより高い場合
            else:
                print("外挿補間結果です。")
                capa_cutV = capa[arg_min_vol - 1] + (capa[arg_min_vol - 2] - capa[arg_min_vol - 1]) * (
                        cut_vol[x] - vol[arg_min_vol - 1]) / (vol[arg_min_vol - 2] - vol[arg_min_vol - 1])
                capa_dod = capa / capa_cutV * 100
                cal_V = np.interp(dod, capa_dod, vol)
            return cal_V  # numpyデータ


        def temp(x, y):
            DF3 = df3.iloc[:, 1:2 * int(Finish_cyc[Lot_len - 1]) + 1]  # 1列目の削除
            DF3 = DF3.iloc[:, 2 * (int(start_cyc[x]) - 1):2 * int(Finish_cyc[x])]  # 水準毎に分割
            DF3 = DF3.iloc[:, 2 * (y - 1):2 * y]  # kサイクル目の容量電圧データ
            DF3 = DF3.dropna(axis=0)
            DF3.columns = ["Capacity[mAh]", "Temp[deg.C]"]
            capa = np.array(DF1["Capacity[mAh]"].values.flatten())
            vol = np.array(DF1["Voltage[V]"].values.flatten())
            temp = np.array(DF3["Temp[deg.C]"].values.flatten())
            min_vol = min(vol)
            arg_min_vol = np.argmin(vol)
            # 最終電圧がカットvoltageと同じ場合
            if (min_vol == cut_vol[x]):
                capa_cutV = capa[arg_min_vol - 1]
                capa_dod = capa / capa_cutV * 100
                cal_temp = np.interp(dod, capa_dod, temp)
            # 最終電圧がカットvoltageより小さい場合
            elif (min_vol < cut_vol[x]):
                capa_cutV = capa[arg_min_vol - 1] + (capa[arg_min_vol - 2] - capa[arg_min_vol - 1]) * (
                        cut_vol[x] - vol[arg_min_vol - 1]) / (vol[arg_min_vol - 2] - vol[arg_min_vol - 1])
                capa_dod = capa / capa_cutV * 100
                cal_temp = np.interp(dod, capa_dod, temp)
            # 最終電圧がカットvoltageより高い場合
            else:
                print("外挿補間結果です。")
                capa_cutV = capa[arg_min_vol - 1] + (capa[arg_min_vol - 2] - capa[arg_min_vol - 1]) * (
                        cut_vol[x] - vol[arg_min_vol - 1]) / (vol[arg_min_vol - 2] - vol[arg_min_vol - 1])
                capa_dod = capa / capa_cutV * 100
                cal_temp = np.interp(dod, capa_dod, temp)
            return cal_temp  # numpyデータ


        def Raw_temp(x, y):
            DF3 = df3.iloc[:, 1:2 * int(Finish_cyc[Lot_len - 1]) + 1]  # 1列目の削除
            DF3 = DF3.iloc[:, 2 * (int(start_cyc[x]) - 1):2 * int(Finish_cyc[x])]  # 水準毎に分割
            DF3 = DF3.iloc[:, 2 * y - 1:2 * y]  # kサイクル目の温度データ
            DF3 = DF3.dropna(axis=0)
            DF3.columns = ["Temp[deg.C]"]
            return DF3


        def dVdQ(x):
            capa = np.array(DF1["Capacity[mAh]"].values.flatten())
            vol = np.array(DF1["Voltage[V]"].values.flatten())
            min_vol = min(vol)
            arg_min_vol = np.argmin(vol)
            dod2 = np.arange(-0.25, 100.75, 0.5)
            # 最終電圧がカットvoltageと同じ場合
            if (min_vol == cut_vol[x]):
                capa_cutV = capa[arg_min_vol - 1]
                capa_dod = capa / capa_cutV * 100
                cal_V = np.interp(dod2, capa_dod, vol)
                diff_dod = np.diff(dod2)
                diff_vol = np.diff(cal_V)
                dVdQ = diff_vol / diff_dod
            # 最終電圧がカットvoltageより小さい場合
            elif (min_vol < cut_vol[x]):
                capa_cutV = capa[arg_min_vol - 1] + (capa[arg_min_vol - 2] - capa[arg_min_vol - 1]) * (
                        cut_vol[x] - vol[arg_min_vol - 1]) / (vol[arg_min_vol - 2] - vol[arg_min_vol - 1])
                capa_dod = capa / capa_cutV * 100
                cal_V = np.interp(dod2, capa_dod, vol)
                diff_dod = np.diff(dod2)
                diff_vol = np.diff(cal_V)
                dVdQ = diff_vol / diff_dod
            # 最終電圧がカットvoltageより高い場合
            else:
                print("外挿補間結果です。")
                capa_cutV = capa[arg_min_vol - 1] + (capa[arg_min_vol - 2] - capa[arg_min_vol - 1]) * (
                        cut_vol[x] - vol[arg_min_vol - 1]) / (vol[arg_min_vol - 2] - vol[arg_min_vol - 1])
                capa_dod = capa / capa_cutV * 100
                cal_V = np.interp(dod2, capa_dod, vol)
                diff_dod = np.diff(dod2)
                diff_vol = np.diff(cal_V)
                dVdQ = diff_vol / diff_dod
            return dVdQ  # numpyデータ


        def delta_vol(x):
            OCV = pd.read_excel(args[0], sheetname="OCV", encodint="cp932", skiprows=1)
            OCVList = pd.read_excel(args[0], sheetname="OCV_List", encodint="cp932")
            data_num = OCVList[OCVList["Gen_vol"] == Gen_vol[i]]
            data_num = data_num["data_number"].values
            OCV = OCV.iloc[:, 2 * (data_num[0] - 1):2 * data_num[0]]
            OCV = OCV.dropna(axis=0)
            OCV.columns = ["DOD[%]", "Voltage[V]"]
            OCV_dod = np.array(OCV["DOD[%]"])
            OCV_vol = np.array(OCV["Voltage[V]"])
            capa = np.array(DF1["Capacity[mAh]"].values.flatten())
            vol = np.array(DF1["Voltage[V]"].values.flatten())
            min_vol = min(vol)
            arg_min_vol = np.argmin(vol)
            # 最終電圧がカットvoltageと同じ場合
            if (min_vol == cut_vol[x]):
                capa_cutV = capa[arg_min_vol - 1]
                capa_dod = capa / capa_cutV * 100
            # 最終電圧がカットvoltageより小さい場合
            elif (min_vol < cut_vol[x]):
                capa_cutV = capa[arg_min_vol - 1] + (capa[arg_min_vol - 2] - capa[arg_min_vol - 1]) * (
                        cut_vol[x] - vol[arg_min_vol - 1]) / (vol[arg_min_vol - 2] - vol[arg_min_vol - 1])
                capa_dod = capa / capa_cutV * 100
            # 最終電圧がカットvoltageより高い場合
            else:
                print("外挿補間結果です。")
                capa_cutV = capa[arg_min_vol - 1] + (capa[arg_min_vol - 2] - capa[arg_min_vol - 1]) * (
                        cut_vol[x] - vol[arg_min_vol - 1]) / (vol[arg_min_vol - 2] - vol[arg_min_vol - 1])
                capa_dod = capa / capa_cutV * 100
            cal_V = np.interp(OCV_dod, capa_dod, vol)
            delta_vol = (OCV_vol - cal_V) * 1000
            delta_vol = np.interp(dod, OCV_dod, delta_vol)
            return delta_vol  # numpyデータ


        def DC_resistance(x):
            Current = np.array(DF1_2["Current[mA]"].values.flatten())
            OCV = pd.read_excel(args[0], sheetname="OCV", encodint="cp932", skiprows=1)
            OCVList = pd.read_excel(args[0], sheetname="OCV_List", encodint="cp932")
            data_num = OCVList[OCVList["Gen_vol"] == Gen_vol[i]]
            data_num = data_num["data_number"].values
            OCV = OCV.iloc[:, 2 * (data_num[0] - 1):2 * data_num[0]]
            OCV = OCV.dropna(axis=0)
            OCV.columns = ["DOD[%]", "Voltage[V]"]
            OCV_dod = np.array(OCV["DOD[%]"])
            OCV_vol = np.array(OCV["Voltage[V]"])
            capa = np.array(DF1["Capacity[mAh]"].values.flatten())
            vol = np.array(DF1["Voltage[V]"].values.flatten())
            min_vol = min(vol)
            arg_min_vol = np.argmin(vol)
            # 最終電圧がカットvoltageと同じ場合
            if (min_vol == cut_vol[x]):
                capa_cutV = capa[arg_min_vol - 1]
                capa_dod = capa / capa_cutV * 100
            # 最終電圧がカットvoltageより小さい場合
            elif (min_vol < cut_vol[x]):
                capa_cutV = capa[arg_min_vol - 1] + (capa[arg_min_vol - 2] - capa[arg_min_vol - 1]) * (
                        cut_vol[i] - vol[arg_min_vol - 1]) / (vol[arg_min_vol - 2] - vol[arg_min_vol - 1])
                capa_dod = capa / capa_cutV * 100
            # 最終電圧がカットvoltageより高い場合
            else:
                print("外挿補間結果です。")
                capa_cutV = capa[arg_min_vol - 1] + (capa[arg_min_vol - 2] - capa[arg_min_vol - 1]) * (
                        cut_vol[i] - vol[arg_min_vol - 1]) / (vol[arg_min_vol - 2] - vol[arg_min_vol - 1])
                capa_dod = capa / capa_cutV * 100
            cal_V = np.interp(OCV_dod, capa_dod, vol)
            Current = np.interp(OCV_dod, capa_dod, Current)
            delta_vol = OCV_vol - cal_V
            DC_resistance = delta_vol / (Current / 1000) * 1000
            DC_resistance = np.interp(dod, OCV_dod, DC_resistance)
            return DC_resistance  # numpyデータ


        def information(x):
            capa = np.array(DF1["Capacity[mAh]"].values.flatten())
            vol = np.array(DF1["Voltage[V]"].values.flatten())
            vol_over30V = np.where(vol >= 3.0)  # 3.0V以上
            capa_over30V = capa[vol_over30V]  # 3.0V以上の容量
            len_over30V = len(capa_over30V) - 1  # 3.0V以上の長さ,0からはじまるので-1
            vol_over32V = np.where(vol >= 3.2)  # 3.2V以上
            capa_over32V = capa[vol_over32V]  # 3.2V以上の容量
            len_over32V = len(capa_over32V) - 1  # 3.2V以上の長さ,0からはじまるので-1
            vol_over34V = np.where(vol >= 3.4)  # 3.4V以上
            capa_over34V = capa[vol_over34V]  # 3.4V以上の容量
            len_over34V = len(capa_over34V) - 1  # 3.4V以上の長さ,0からはじまるので-1
            vol_over36V = np.where(vol >= 3.6)  # 3.6V以上
            capa_over36V = capa[vol_over36V]  # 3.6V以上の容量
            len_over36V = len(capa_over36V) - 1  # 3.6V以上の長さ,0からはじまるので-1
            vol_over38V = np.where(vol >= 3.8)  # 3.8V以上
            capa_over38V = capa[vol_over38V]  # 3.8V以上の容量
            len_over38V = len(capa_over38V) - 1  # 3.8V以上の長さ,0からはじまるので-1
            vol_over40V = np.where(vol >= 4.0)  # 4.0V以上
            capa_over40V = capa[vol_over40V]  # 4.0V以上の容量
            len_over40V = len(capa_over40V) - 1  # 4.0V以上の長さ,0からはじまるので-1
            vol_over275V = np.where(vol >= 2.75)  # 2.75V以上
            capa_over275V = capa[vol_over275V]  # 2.75V以上の容量
            len_over275V = len(capa_over275V) - 1  # 2.75V以上の長さ,0からはじまるので-1

            if (cut_vol[x] <= 2.75):
                if (cut_vol[x] == 2.75):
                    capa_275V = capa[len_over275V]
                    ave_voltage_275V = np.average(vol[vol_over275V])
                    Energy_275V = ave_voltage_275V * capa_275V / 1000
                else:
                    capa_275V = capa[len_over275V] + (capa[len_over275V - 1] - capa[len_over275V]) * (
                            2.75 - vol[len_over275V]) / (vol[len_over275V - 1] - vol[len_over275V])
                    ave_voltage_275V = np.average(vol[vol_over275V])
                    Energy_275V = ave_voltage_275V * capa_275V / 1000
                capa_30V = capa[len_over30V] + (capa[len_over30V - 1] - capa[len_over30V]) * (
                        3.0 - vol[len_over30V]) / (vol[len_over30V - 1] - vol[len_over30V])
                capa_32V = capa[len_over32V] + (capa[len_over32V - 1] - capa[len_over32V]) * (
                        3.2 - vol[len_over32V]) / (vol[len_over32V - 1] - vol[len_over32V])
                capa_34V = capa[len_over34V] + (capa[len_over34V - 1] - capa[len_over34V]) * (
                        3.4 - vol[len_over34V]) / (vol[len_over34V - 1] - vol[len_over34V])
                capa_36V = capa[len_over36V] + (capa[len_over36V - 1] - capa[len_over36V]) * (
                        3.6 - vol[len_over36V]) / (vol[len_over36V - 1] - vol[len_over36V])
                capa_38V = capa[len_over38V] + (capa[len_over38V - 1] - capa[len_over38V]) * (
                        3.8 - vol[len_over38V]) / (vol[len_over38V - 1] - vol[len_over38V])
                capa_40V = capa[len_over40V] + (capa[len_over40V - 1] - capa[len_over40V]) * (
                        4.0 - vol[len_over40V]) / (vol[len_over40V - 1] - vol[len_over40V])

                ave_voltage_30V = np.average(vol[vol_over30V])
                Energy_30V = ave_voltage_30V * capa_30V / 1000
                ave_voltage_32V = np.average(vol[vol_over32V])
                Energy_32V = ave_voltage_32V * capa_32V / 1000
                ave_voltage_34V = np.average(vol[vol_over34V])
                Energy_34V = ave_voltage_34V * capa_34V / 1000
                ave_voltage_36V = np.average(vol[vol_over36V])
                Energy_36V = ave_voltage_36V * capa_36V / 1000
                ave_voltage_38V = np.average(vol[vol_over38V])
                Energy_38V = ave_voltage_38V * capa_38V / 1000
                ave_voltage_40V = np.average(vol[vol_over40V])
                Energy_40V = ave_voltage_40V * capa_40V / 1000

            elif (cut_vol[x] <= 3.0):
                capa_275V = None
                ave_voltage_275V = None
                Energy_275V = None
                if (cut_vol[x] == 3.0):
                    capa_30V = capa[len_over30V]
                    ave_voltage_30V = np.average(vol[vol_over30V])
                    Energy_30V = ave_voltage_30V * capa_30V / 1000
                else:
                    capa_30V = capa[len_over30V] + (capa[len_over30V - 1] - capa[len_over30V]) * (
                            3.0 - vol[len_over30V]) / (vol[len_over30V - 1] - vol[len_over30V])
                    ave_voltage_30V = np.average(vol[vol_over30V])
                    Energy_30V = ave_voltage_30V * capa_30V / 1000
                capa_32V = capa[len_over32V] + (capa[len_over32V - 1] - capa[len_over32V]) * (
                        3.2 - vol[len_over32V]) / (vol[len_over32V - 1] - vol[len_over32V])
                capa_34V = capa[len_over34V] + (capa[len_over34V - 1] - capa[len_over34V]) * (
                        3.4 - vol[len_over34V]) / (vol[len_over34V - 1] - vol[len_over34V])
                capa_36V = capa[len_over36V] + (capa[len_over36V - 1] - capa[len_over36V]) * (
                        3.6 - vol[len_over36V]) / (vol[len_over36V - 1] - vol[len_over36V])
                capa_38V = capa[len_over38V] + (capa[len_over38V - 1] - capa[len_over38V]) * (
                        3.8 - vol[len_over38V]) / (vol[len_over38V - 1] - vol[len_over38V])
                capa_40V = capa[len_over40V] + (capa[len_over40V - 1] - capa[len_over40V]) * (
                        4.0 - vol[len_over40V]) / (vol[len_over40V - 1] - vol[len_over40V])
                ave_voltage_32V = np.average(vol[vol_over32V])
                Energy_32V = ave_voltage_32V * capa_32V / 1000
                ave_voltage_34V = np.average(vol[vol_over34V])
                Energy_34V = ave_voltage_34V * capa_34V / 1000
                ave_voltage_36V = np.average(vol[vol_over36V])
                Energy_36V = ave_voltage_36V * capa_36V / 1000
                ave_voltage_38V = np.average(vol[vol_over38V])
                Energy_38V = ave_voltage_38V * capa_38V / 1000
                ave_voltage_40V = np.average(vol[vol_over40V])
                Energy_40V = ave_voltage_40V * capa_40V / 1000

            elif (cut_vol[x] <= 3.2):
                capa_275V = None
                ave_voltage_275V = None
                Energy_275V = None
                capa_30V = None
                ave_voltage_30V = None
                Energy_30V = None
                if (cut_vol[x] == 3.2):
                    capa_32V = capa[len_over32V]
                    ave_voltage_32V = np.average(vol[vol_over32V])
                    Energy_32V = ave_voltage_32V * capa_32V / 1000
                else:
                    capa_32V = capa[len_over32V] + (capa[len_over32V - 1] - capa[len_over32V]) * (
                            3.2 - vol[len_over32V]) / (vol[len_over32V - 1] - vol[len_over32V])
                    ave_voltage_32V = np.average(vol[vol_over32V])
                    Energy_32V = ave_voltage_32V * capa_32V / 1000
                capa_34V = capa[len_over34V] + (capa[len_over34V - 1] - capa[len_over34V]) * (
                        3.4 - vol[len_over34V]) / (vol[len_over34V - 1] - vol[len_over34V])
                capa_36V = capa[len_over36V] + (capa[len_over36V - 1] - capa[len_over36V]) * (
                        3.6 - vol[len_over36V]) / (vol[len_over36V - 1] - vol[len_over36V])
                capa_38V = capa[len_over38V] + (capa[len_over38V - 1] - capa[len_over38V]) * (
                        3.8 - vol[len_over38V]) / (vol[len_over38V - 1] - vol[len_over38V])
                capa_40V = capa[len_over40V] + (capa[len_over40V - 1] - capa[len_over40V]) * (
                        4.0 - vol[len_over40V]) / (vol[len_over40V - 1] - vol[len_over40V])
                ave_voltage_34V = np.average(vol[vol_over34V])
                Energy_34V = ave_voltage_34V * capa_34V / 1000
                ave_voltage_36V = np.average(vol[vol_over36V])
                Energy_36V = ave_voltage_36V * capa_36V / 1000
                ave_voltage_38V = np.average(vol[vol_over38V])
                Energy_38V = ave_voltage_38V * capa_38V / 1000
                ave_voltage_40V = np.average(vol[vol_over40V])
                Energy_40V = ave_voltage_40V * capa_40V / 1000

            elif (cut_vol[x] <= 3.4):
                capa_275V = None
                ave_voltage_275V = None
                Energy_275V = None
                capa_30V = None
                ave_voltage_30V = None
                Energy_30V = None
                capa_32V = None
                ave_voltage_32V = None
                Energy_32V = None
                if (cut_vol[x] == 3.4):
                    capa_34V = capa[len_over34V]
                    ave_voltage_34V = np.average(vol[vol_over34V])
                    Energy_34V = ave_voltage_34V * capa_34V / 1000
                else:
                    capa_34V = capa[len_over34V] + (capa[len_over34V - 1] - capa[len_over34V]) * (
                            3.4 - vol[len_over34V]) / (vol[len_over34V - 1] - vol[len_over34V])
                    ave_voltage_34V = np.average(vol[vol_over34V])
                    Energy_34V = ave_voltage_34V * capa_34V / 1000
                capa_36V = capa[len_over36V] + (capa[len_over36V - 1] - capa[len_over36V]) * (
                        3.6 - vol[len_over36V]) / (vol[len_over36V - 1] - vol[len_over36V])
                capa_38V = capa[len_over38V] + (capa[len_over38V - 1] - capa[len_over38V]) * (
                        3.8 - vol[len_over38V]) / (vol[len_over38V - 1] - vol[len_over38V])
                capa_40V = capa[len_over40V] + (capa[len_over40V - 1] - capa[len_over40V]) * (
                        4.0 - vol[len_over40V]) / (vol[len_over40V - 1] - vol[len_over40V])
                ave_voltage_36V = np.average(vol[vol_over36V])
                Energy_36V = ave_voltage_36V * capa_36V / 1000
                ave_voltage_38V = np.average(vol[vol_over38V])
                Energy_38V = ave_voltage_38V * capa_38V / 1000
                ave_voltage_40V = np.average(vol[vol_over40V])
                Energy_40V = ave_voltage_40V * capa_40V / 1000

            elif (cut_vol[x] <= 3.6):
                capa_275V = None
                ave_voltage_275V = None
                Energy_275V = None
                capa_30V = None
                ave_voltage_30V = None
                Energy_30V = None
                capa_32V = None
                ave_voltage_32V = None
                Energy_32V = None
                capa_34V = None
                ave_voltage_34V = None
                Energy_34V = None
                if (cut_vol[x] == 3.6):
                    capa_36V = capa[len_over36V]
                    ave_voltage_36V = np.average(vol[vol_over36V])
                    Energy_36V = ave_voltage_36V * capa_36V / 1000
                else:
                    capa_36V = capa[len_over36V] + (capa[len_over36V - 1] - capa[len_over36V]) * (
                            3.6 - vol[len_over36V]) / (vol[len_over36V - 1] - vol[len_over36V])
                    ave_voltage_36V = np.average(vol[vol_over36V])
                    Energy_36V = ave_voltage_36V * capa_36V / 1000
                capa_38V = capa[len_over38V] + (capa[len_over38V - 1] - capa[len_over38V]) * (
                        3.8 - vol[len_over38V]) / (vol[len_over38V - 1] - vol[len_over38V])
                capa_40V = capa[len_over40V] + (capa[len_over40V - 1] - capa[len_over40V]) * (
                        4.0 - vol[len_over40V]) / (vol[len_over40V - 1] - vol[len_over40V])
                ave_voltage_38V = np.average(vol[vol_over38V])
                Energy_38V = ave_voltage_38V * capa_38V / 1000
                ave_voltage_40V = np.average(vol[vol_over40V])
                Energy_40V = ave_voltage_40V * capa_40V / 1000

            elif (cut_vol[x] <= 3.8):
                capa_275V = None
                ave_voltage_275V = None
                Energy_275V = None
                capa_30V = None
                ave_voltage_30V = None
                Energy_30V = None
                capa_32V = None
                ave_voltage_32V = None
                Energy_32V = None
                capa_34V = None
                ave_voltage_34V = None
                Energy_34V = None
                capa_36V = None
                ave_voltage_36V = None
                Energy_36V = None
                if (cut_vol[x] == 3.8):
                    capa_38V = capa[len_over38V]
                    ave_voltage_38V = np.average(vol[vol_over38V])
                    Energy_38V = ave_voltage_38V * capa_38V / 1000
                else:
                    capa_38V = capa[len_over38V] + (capa[len_over38V - 1] - capa[len_over38V]) * (
                            3.8 - vol[len_over38V]) / (vol[len_over38V - 1] - vol[len_over38V])
                    ave_voltage_38V = np.average(vol[vol_over38V])
                    Energy_38V = ave_voltage_38V * capa_38V / 1000
                capa_40V = capa[len_over40V] + (capa[len_over40V - 1] - capa[len_over40V]) * (
                        4.0 - vol[len_over40V]) / (vol[len_over40V - 1] - vol[len_over40V])
                ave_voltage_40V = np.average(vol[vol_over40V])
                Energy_40V = ave_voltage_40V * capa_40V / 1000
            elif (cut_vol[x] <= 4.0):
                capa_275V = None
                ave_voltage_275V = None
                Energy_275V = None
                capa_30V = None
                ave_voltage_30V = None
                Energy_30V = None
                capa_32V = None
                ave_voltage_32V = None
                Energy_32V = None
                capa_34V = None
                ave_voltage_34V = None
                Energy_34V = None
                capa_36V = None
                ave_voltage_36V = None
                Energy_36V = None
                capa_38V = None
                ave_voltage_38V = None
                Energy_38V = None
                if (cut_vol[x] == 4.0):
                    capa_40V = capa[len_over40V]
                    ave_voltage_40V = np.average(vol[vol_over40V])
                    Energy_40V = ave_voltage_40V * capa_40V / 1000
                else:
                    capa_40V = capa[len_over40V] + (capa[len_over40V - 1] - capa[len_over40V]) * (
                            4.0 - vol[len_over40V]) / (vol[len_over40V - 1] - vol[len_over40V])
                    ave_voltage_40V = np.average(vol[vol_over40V])
                    Energy_40V = ave_voltage_40V * capa_40V / 1000
            else:
                print("容量データは取り込めません。カーブデータのみ取り込みました。")
                capa_275V = None
                ave_voltage_275V = None
                Energy_275V = None
                capa_30V = None
                ave_voltage_30V = None
                Energy_30V = None
                capa_32V = None
                ave_voltage_32V = None
                Energy_32V = None
                capa_34V = None
                ave_voltage_34V = None
                Energy_34V = None
                capa_36V = None
                ave_voltage_36V = None
                Energy_36V = None
                capa_38V = None
                ave_voltage_38V = None
                Energy_38V = None
                capa_40V = None
                ave_voltage_40V = None
                Energy_40V = None
            Try_lot = Lot[x][0:-4]
            info = [Lot[x],  # セルロット
                    Try_lot,  # 水準ロット
                    day[x],  # 測定日
                    eq[x],  # 装置
                    ch[x],  # チャンネル
                    TEMP[x],  # 測定温度
                    Gen[x],  # 世代
                    size[x],  # サイズ
                    Charge_vol[x],  # 充電電圧
                    Charge_rate[x],  # 充電レート
                    Charge_cut_rate[x],  # 充電カットレート
                    RestC[x],  # 充電後休止時間
                    C_Rate,  # 放電レート
                    cut_vol[x],  # 放電カットレート
                    RestD[x],  # 放電後終止時間
                    capa_1C[x],  # 1C容量[mAh]
                    capa_40V,  # 4V容量
                    capa_38V,  # 3.8V容量
                    capa_36V,  # 3.6V容量
                    capa_34V,  # 3.4V容量
                    capa_32V,  # 3.2V容量
                    capa_30V,  # 3Vcut容量
                    capa_275V,  # 2.75Vcut容量
                    save_file,  # カーブデータ保存先
                    Raw_file,  # Rawデータ作成
                    min_Energy[x],  # minEnergy
                    ave_voltage_275V,  # 2.75平均電圧
                    ave_voltage_30V,  # 3.0平均電圧
                    ave_voltage_32V,  # 3.2平均電圧
                    ave_voltage_34V,  # 3.4平均電圧
                    ave_voltage_36V,  # 3.6平均電圧
                    ave_voltage_38V,  # 3.8平均電圧
                    ave_voltage_40V,  # 4.0平均電圧
                    Energy_275V,  # 2.75エネルギー
                    Energy_30V,  # 3.0エネルギー
                    Energy_32V,  # 3.2エネルギー
                    Energy_34V,  # 3.4エネルギー
                    Energy_36V,  # 3.6エネルギー
                    Energy_38V,  # 3.8エネルギー
                    Energy_40V,  # 4.0エネルギー
                    Measurer[x]]  # 測定者
            info = pd.Series(info)
            return info


        # 生データ
        Raw = pd.concat([DF1, DF1_2], axis=1)
        # curveデータについて
        # DOD
        DOD = pd.DataFrame(dod)
        DOD.columns = ["DOD[%]"]
        # voltage
        DOD_curve_np = DOD_curve(i)
        DOD_curve_pd = pd.DataFrame(DOD_curve_np)
        DOD_curve_pd.columns = ["Voltage[V]"]
        # dVdQ
        dVdQ = dVdQ(i)
        dVdQ_pd = pd.DataFrame(dVdQ)
        dVdQ_pd.columns = ["dVdQ[V/mAh]"]
        # delta_voltage
        delta_vol = delta_vol(i)
        delta_vol_pd = pd.DataFrame(delta_vol)
        delta_vol_pd.columns = ["delta_V[mV]"]
        # RC_resistance
        DC_resistance = DC_resistance(i)
        DC_resistance_pd = pd.DataFrame(DC_resistance)
        DC_resistance_pd.columns = ["DC_resistance[mohm]"]

        Data = pd.concat([DOD, DOD_curve_pd, dVdQ_pd, delta_vol_pd, DC_resistance_pd], axis=1)
        # 温度データがある場合
        if (temp_data[i] == 1):
            temp = temp(i, k)
            Raw_temp = Raw_temp(i, k)
            max_temp = max(temp)
            info = information(i)
            info = np.append(info, max_temp)
            info = pd.DataFrame(info)
            info = info.T
            info.columns = ["Cell-Lot",  # セルロット
                            "Try-lot.",  # 水準ロット
                            "Day",  # 測定日
                            "Test_equipment",  # 装置
                            "ch",  # チャンネル
                            "Temp[deg.C]",  # 測定温度
                            "Gen",  # 世代
                            "size",  # サイズ
                            "Charge-voltage[V]",  # 充電電圧
                            "Charge-rate[C]",  # 充電レート
                            "Charge-cut-rate[C]",  # 充電カットレート
                            "Rest_afterC[min]",  # 充電後休止時間
                            "Discharge-rate[C]",  # 放電レート
                            "Discharge-cut-voltage[V]",  # 放電カットレート
                            "Rest_afterD[min]",  # 放電後終止時間
                            "min_rated_capacity[mAh]",  # 1C容量[mAh]
                            "Capacity_4.0V[mAh]",  # 4V容量
                            "Capacity_3.8V[mAh]",  # 3.8V容量
                            "Capacity_3.6V[mAh]",  # 3.6V容量
                            "Capacity_3.4V[mAh]",  # 3.4V容量
                            "Capacity_3.2V[mAh]",  # 3.2V容量
                            "Capacity_3.0V[mAh]",  # 3Vcut容量
                            "Capacity_2.75V[mAh]",  # 2.75V容量
                            "Curve_Data_Link",  # カーブデータ保存先
                            "Raw_Data_Link",  # 生データ保管場所
                            "min_rated_Energy[Wh]",  # minエネルギー
                            "Average-Voltage_2.75V[V]",  # 平均電圧
                            "Average-Voltage_3.0V[V]",
                            "Average-Voltage_3.2V[V]",
                            "Average-Voltage_3.4V[V]",
                            "Average-Voltage_3.6V[V]",
                            "Average-Voltage_3.8V[V]",
                            "Average-Voltage_4.0V[V]",
                            "Energy_2.75V[Wh]",  # エネルギー
                            "Energy_3.0V[Wh]",
                            "Energy_3.2V[Wh]",
                            "Energy_3.4V[Wh]",
                            "Energy_3.6V[Wh]",
                            "Energy_3.8V[Wh]",
                            "Energy_4.0V[Wh]",
                            "Measurer",
                            "Max_cell_temp[deg.C]"]  # 温度データ
            temp_data = pd.DataFrame(temp)
            temp_data.columns = ["Temp[deg.C]"]
            Data2 = pd.concat([Data, temp_data], axis=1)
            Raw2 = pd.concat([Raw, Raw_temp], axis=1)
        # 温度データがない場合
        else:
            print("この水準は温度データは取り込みません")
            info = information(i)
            info = pd.DataFrame(info)
            info = info.T
            info.columns = ["Cell-Lot",  # セルロット
                            "Try-lot.",  # 水準ロット
                            "Day",  # 測定日
                            "Test_equipment",  # 装置
                            "ch",  # チャンネル
                            "Temp[deg.C]",  # 測定温度
                            "Gen",  # 世代
                            "size",  # サイズ
                            "Charge-voltage[V]",  # 充電電圧
                            "Charge-rate[C]",  # 充電レート
                            "Charge-cut-rate[C]",  # 充電カットレート
                            "Rest_afterC[min]",  # 充電後休止時間
                            "Discharge-rate[C]",  # 放電レート
                            "Discharge-cut-voltage[V]",  # 放電カットレート
                            "Rest_afterD[min]",  # 放電後終止時間
                            "min_rated_capacity[mAh]",  # 1C容量[mAh]
                            "Capacity_4.0V[mAh]",  # 4V容量
                            "Capacity_3.8V[mAh]",  # 3.8V容量
                            "Capacity_3.6V[mAh]",  # 3.6V容量
                            "Capacity_3.4V[mAh]",  # 3.4V容量
                            "Capacity_3.2V[mAh]",  # 3.2V容量
                            "Capacity_3.0V[mAh]",  # 3Vcut容量
                            "Capacity_2.75V[mAh]",  # 2.75V容量
                            "Curve_Data_Link",  # カーブデータ保存先
                            "Raw_Data_Link",  # 生データ保管場所
                            "min_rated_Energy[Wh]",  # minエネルギー
                            "Average-Voltage_2.75V[V]",  # 平均電圧
                            "Average-Voltage_3.0V[V]",
                            "Average-Voltage_3.2V[V]",
                            "Average-Voltage_3.4V[V]",
                            "Average-Voltage_3.6V[V]",
                            "Average-Voltage_3.8V[V]",
                            "Average-Voltage_4.0V[V]",
                            "Energy_2.75V[Wh]",  # エネルギー
                            "Energy_3.0V[Wh]",
                            "Energy_3.2V[Wh]",
                            "Energy_3.4V[Wh]",
                            "Energy_3.6V[Wh]",
                            "Energy_3.8V[Wh]",
                            "Energy_4.0V[Wh]",
                            "Measurer"]
            Data2 = Data
            Raw2 = Raw
        Data2.to_csv(save_file, index=False)
        Raw2.to_csv(Raw_file, index=False)
        info2 = pd.read_csv("C:\DataBase\Discharge_rate_Capability\Discharge_rate_Capability_used-cell.csv")
        info3 = pd.concat([info2, info], axis=0)
        save_link = "C:\DataBase\Discharge_rate_Capability\Cell_information" + "\Discharge_rate_Capability_used-cell" + "_" + time_stamp + ".csv"
        info3.to_csv(save_link, index=False)

        # xサイクル目
        cycle = str(k + 1) + "cyc目_取り込みok"
        print(cycle)
