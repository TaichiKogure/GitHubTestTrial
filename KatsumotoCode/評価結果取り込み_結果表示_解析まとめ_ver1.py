'''
Created on 2018/07/10

@author: MM12069
'''
import datetime
import os
import subprocess
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilenames

import matplotlib as plt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

root2 = Tk()
note = ttk.Notebook(root2)

tab_a = Frame(note,height=630,width=1120)
tab_b = Frame(note,height=630,width=1120)
tab_c = Frame(note,height=630,width=1120)
tab_d = Frame(note,height=630,width=1120)
tab_e = Frame(note,height=630,width=1120)

note.add(tab_a, text="Import Data")
note.add(tab_b, text="Result(データベース引用)")
note.add(tab_c, text="Analysis")
note.add(tab_d, text="データ検索")
note.add(tab_e, text="生データ処理")

def import_dis():
    #ファイル読み込みの手法
    today=datetime.datetime.now()
    year=today.year
    month=today.month
    day=today.day
    hour=today.hour
    minute=today.minute
    second=today.second
    if(month<10):
        month=str(0)+str(month)
    else:
        month=str(month)
    if(day<10):
        day=str(0)+str(day)
    else:
        day=str(day)
    if(hour<10):
        hour=str(0)+str(hour)
    else:
        hour=str(hour)
    if(minute<10):
        minute=str(0)+str(minute)
    else:
        minute=str(minute)
    if(second<10):
        second=str(0)+str(second)
    else:
        second=str(second)
    time_stamp=str(year)+month+str(day)+str(hour)+str(minute)+str(second)


    #Listファイルの選択
    root=tkinter.Tk()
    root.withdraw()
    args=askopenfilenames(filetypes=(("All files", "*.*"),("HTML files", "*.html;*.htm"),("csv files", "*.csv") ))
    #データフレームの取り込み
    df1=pd.read_excel(args[0],sheetname="C-V",encodint="cp932",skiprows=1)#容量電圧
    df1_2=pd.read_excel(args[0],sheetname="T-I",encodint="cp932",skiprows=1)#時間電流
    df2=pd.read_excel(args[0],sheetname="Condition",encodint="cp932")#使用データ
    df3=pd.read_excel(args[0],sheetname="Temp_data",encodint="cp932",skiprows=1)#容量温度
    df2=df2.dropna(how="all",axis=0)#NaNがいるとfloat表記になるので、必要に応じてint型へ。
    #条件検索用データ
    start_cyc=np.array(df2["Start_cycle"].values.flatten())#スタートサイクル数
    Finish_cyc=np.array(df2["Finish_cycle"].values.flatten())#フィニッシュサイクル数
    cycle_num=np.array(df2["Cycle_number"].values.flatten())#サイクル数
    Gen_vol=np.array(df2["Gen_vol"].values.flatten())#サイクル数
    #取り込みデータ
    Lot=np.array(df2["Cell-Lot"].values.flatten())#セルロット
    capa_1C=np.array(df2["min_rated_capacity[mAh]"].values.flatten())#1C容量
    temp_data=np.array(df2["temp_data"].values.flatten())#温度データがあるかないか
    Gen=np.array(df2["Gen"].values.flatten())#世代
    size=np.array(df2["size"].values.flatten())#サイズ
    day=np.array(df2["Day"].values.flatten())#日時
    RestC=np.array(df2["Rest_afterC[min]"].values.flatten())#充電後レスト時間
    RestD=np.array(df2["Rest_afterD[min]"].values.flatten())#放電後レスト時間
    Charge_rate=np.array(df2["Charge-rate[C]"].values.flatten())#充電レート
    Charge_vol=np.array(df2["Charge-voltage[V]"].values.flatten())#充電電圧
    Charge_cut_rate=np.array(df2["Charge-cut-rate[C]"].values.flatten())#充電カットレート
    TEMP=np.array(df2["Temp[deg.C]"].values.flatten())#測定データ
    eq=np.array(df2["Test_equipment"].values.flatten())#測定装置
    ch=np.array(df2["ch"].values.flatten())#測定ch
    cut_vol=np.array(df2["Discharge-cut-voltage[V]"].values.flatten())#放電カット電圧
    min_Energy=np.array(df2["min_rated_Energy[Wh]"].values.flatten())#放電カット電圧
    Measurer=np.array(df2["Measurer"].values.flatten())#測定者
    #計算に使う値
    dod=np.arange(0,100.5,0.5)#DOD200point
    Lot_len=len(Lot)#ロットを読み込んだ数
    print("繰り返し数")
    print(Lot_len)
    for i in range(Lot_len):#2×スタートサイクル-1～2×フィニッシュサイクル
        print(Lot[i])
        dF1=df1.iloc[:,1:2*int(Finish_cyc[Lot_len-1])+1]#1列目の削除
        dF1=dF1.iloc[:,2*(int(start_cyc[i])-1):2*int(Finish_cyc[i])]#水準毎に分割
        dF1_2=df1_2.iloc[:,1:2*int(Finish_cyc[Lot_len-1])+1]#1列目の削除
        dF1_2=dF1_2.iloc[:,2*(int(start_cyc[i])-1):2*int(Finish_cyc[i])]#水準毎に分割
        for k in range(int(cycle_num[i])):#サイクル数分データを取得
            C_Rate=np.array(df2[k].values.flatten())[i]
            save_name="save"+str(k)+"_DOD"
            save_raw="save"+str(k)+"_Raw"
            file=np.array(df2[save_name].values.flatten())
            file2=np.array(df2[save_raw].values.flatten())
            save_file=file[i]
            Raw_file=file2[i]
            DF1=dF1.iloc[:,2*(k):2*(k+1)]#kサイクル目の容量電圧データ
            DF1=DF1.dropna(axis=0)
            DF1.columns=["Capacity[mAh]","Voltage[V]"]
            DF1_2=dF1_2.iloc[:,2*(k):2*(k+1)]#kサイクル目の容量電圧データ
            DF1_2=DF1_2.dropna(axis=0)
            DF1_2.columns=["Time[min]","Current[mA]"]
            def DOD_curve(x):#カット電圧におけるDODカーブ、カット電圧ごとのカーブを求めるわけではない。
                capa=np.array(DF1["Capacity[mAh]"].values.flatten())
                vol=np.array(DF1["Voltage[V]"].values.flatten())
                min_vol=min(vol)
                arg_min_vol=np.argmin(vol)
                #最終電圧がカットvoltageと同じ場合
                if(min_vol==cut_vol[x]):
                    capa_cutV=capa[arg_min_vol-1]
                    capa_dod=capa/capa_cutV*100
                    cal_V=np.interp(dod,capa_dod,vol)
                #最終電圧がカットvoltageより小さい場合
                elif(min_vol<cut_vol[x]):
                    capa_cutV=capa[arg_min_vol-1]+(capa[arg_min_vol-2]-capa[arg_min_vol-1])*(cut_vol[x]-vol[arg_min_vol-1])/(vol[arg_min_vol-2]-vol[arg_min_vol-1])
                    capa_dod=capa/capa_cutV*100
                    cal_V=np.interp(dod,capa_dod,vol)
                #最終電圧がカットvoltageより高い場合
                else:
                    print("外挿補間結果です。")
                    capa_cutV=capa[arg_min_vol-1]+(capa[arg_min_vol-2]-capa[arg_min_vol-1])*(cut_vol[x]-vol[arg_min_vol-1])/(vol[arg_min_vol-2]-vol[arg_min_vol-1])
                    capa_dod=capa/capa_cutV*100
                    cal_V=np.interp(dod,capa_dod,vol)
                return cal_V #numpyデータ
            def temp(x,y):
                DF3=df3.iloc[:,1:2*int(Finish_cyc[Lot_len-1])+1]#1列目の削除
                DF3=DF3.iloc[:,2*(int(start_cyc[x])-1):2*int(Finish_cyc[x])]#水準毎に分割
                DF3=DF3.iloc[:,2*(y-1):2*y]#kサイクル目の容量電圧データ
                DF3=DF3.dropna(axis=0)
                DF3.columns=["Capacity[mAh]","Temp[deg.C]"]
                capa=np.array(DF1["Capacity[mAh]"].values.flatten())
                vol=np.array(DF1["Voltage[V]"].values.flatten())
                temp=np.array(DF3["Temp[deg.C]"].values.flatten())
                min_vol=min(vol)
                arg_min_vol=np.argmin(vol)
                #最終電圧がカットvoltageと同じ場合
                if(min_vol==cut_vol[x]):
                    capa_cutV=capa[arg_min_vol-1]
                    capa_dod=capa/capa_cutV*100
                    cal_temp=np.interp(dod,capa_dod,temp)
                #最終電圧がカットvoltageより小さい場合
                elif(min_vol<cut_vol[x]):
                    capa_cutV=capa[arg_min_vol-1]+(capa[arg_min_vol-2]-capa[arg_min_vol-1])*(cut_vol[x]-vol[arg_min_vol-1])/(vol[arg_min_vol-2]-vol[arg_min_vol-1])
                    capa_dod=capa/capa_cutV*100
                    cal_temp=np.interp(dod,capa_dod,temp)
                #最終電圧がカットvoltageより高い場合
                else:
                    print("外挿補間結果です。")
                    capa_cutV=capa[arg_min_vol-1]+(capa[arg_min_vol-2]-capa[arg_min_vol-1])*(cut_vol[x]-vol[arg_min_vol-1])/(vol[arg_min_vol-2]-vol[arg_min_vol-1])
                    capa_dod=capa/capa_cutV*100
                    cal_temp=np.interp(dod,capa_dod,temp)
                return cal_temp#numpyデータ
            def Raw_temp(x,y):
                DF3=df3.iloc[:,1:2*int(Finish_cyc[Lot_len-1])+1]#1列目の削除
                DF3=DF3.iloc[:,2*(int(start_cyc[x])-1):2*int(Finish_cyc[x])]#水準毎に分割
                DF3=DF3.iloc[:,2*y-1:2*y]#kサイクル目の温度データ
                DF3=DF3.dropna(axis=0)
                DF3.columns=["Temp[deg.C]"]
                return DF3

            def dVdQ(x):
                capa=np.array(DF1["Capacity[mAh]"].values.flatten())
                vol=np.array(DF1["Voltage[V]"].values.flatten())
                min_vol=min(vol)
                arg_min_vol=np.argmin(vol)
                dod2=np.arange(-0.25,100.75,0.5)
                #最終電圧がカットvoltageと同じ場合
                if(min_vol==cut_vol[x]):
                    capa_cutV=capa[arg_min_vol-1]
                    capa_dod=capa/capa_cutV*100
                    cal_V=np.interp(dod2,capa_dod,vol)
                    diff_dod=np.diff(dod2)
                    diff_vol=np.diff(cal_V)
                    dVdQ=diff_vol/diff_dod
                #最終電圧がカットvoltageより小さい場合
                elif(min_vol<cut_vol[x]):
                    capa_cutV=capa[arg_min_vol-1]+(capa[arg_min_vol-2]-capa[arg_min_vol-1])*(cut_vol[x]-vol[arg_min_vol-1])/(vol[arg_min_vol-2]-vol[arg_min_vol-1])
                    capa_dod=capa/capa_cutV*100
                    cal_V=np.interp(dod2,capa_dod,vol)
                    diff_dod=np.diff(dod2)
                    diff_vol=np.diff(cal_V)
                    dVdQ=diff_vol/diff_dod
                #最終電圧がカットvoltageより高い場合
                else:
                    print("外挿補間結果です。")
                    capa_cutV=capa[arg_min_vol-1]+(capa[arg_min_vol-2]-capa[arg_min_vol-1])*(cut_vol[x]-vol[arg_min_vol-1])/(vol[arg_min_vol-2]-vol[arg_min_vol-1])
                    capa_dod=capa/capa_cutV*100
                    cal_V=np.interp(dod2,capa_dod,vol)
                    diff_dod=np.diff(dod2)
                    diff_vol=np.diff(cal_V)
                    dVdQ=diff_vol/diff_dod
                return dVdQ #numpyデータ
            def delta_vol(x):
                OCV=pd.read_excel(args[0],sheetname="OCV",encodint="cp932",skiprows=1)
                OCVList=pd.read_excel(args[0],sheetname="OCV_List",encodint="cp932")
                data_num=OCVList[OCVList["Gen_vol"]==Gen_vol[i]]
                data_num=data_num["data_number"].values
                OCV=OCV.iloc[:,2*(data_num[0]-1):2*data_num[0]]
                OCV=OCV.dropna(axis=0)
                OCV.columns=["DOD[%]","Voltage[V]"]
                OCV_dod=np.array(OCV["DOD[%]"])
                OCV_vol=np.array(OCV["Voltage[V]"])
                capa=np.array(DF1["Capacity[mAh]"].values.flatten())
                vol=np.array(DF1["Voltage[V]"].values.flatten())
                min_vol=min(vol)
                arg_min_vol=np.argmin(vol)
                #最終電圧がカットvoltageと同じ場合
                if(min_vol==cut_vol[x]):
                    capa_cutV=capa[arg_min_vol-1]
                    capa_dod=capa/capa_cutV*100
                #最終電圧がカットvoltageより小さい場合
                elif(min_vol<cut_vol[x]):
                    capa_cutV=capa[arg_min_vol-1]+(capa[arg_min_vol-2]-capa[arg_min_vol-1])*(cut_vol[x]-vol[arg_min_vol-1])/(vol[arg_min_vol-2]-vol[arg_min_vol-1])
                    capa_dod=capa/capa_cutV*100
                #最終電圧がカットvoltageより高い場合
                else:
                    print("外挿補間結果です。")
                    capa_cutV=capa[arg_min_vol-1]+(capa[arg_min_vol-2]-capa[arg_min_vol-1])*(cut_vol[x]-vol[arg_min_vol-1])/(vol[arg_min_vol-2]-vol[arg_min_vol-1])
                    capa_dod=capa/capa_cutV*100
                cal_V=np.interp(OCV_dod,capa_dod,vol)
                delta_vol=(OCV_vol-cal_V)*1000
                delta_vol=np.interp(dod,OCV_dod,delta_vol)
                return delta_vol #numpyデータ

            def DC_resistance(x):
                Current=np.array(DF1_2["Current[mA]"].values.flatten())
                OCV=pd.read_excel(args[0],sheetname="OCV",encodint="cp932",skiprows=1)
                OCVList=pd.read_excel(args[0],sheetname="OCV_List",encodint="cp932")
                data_num=OCVList[OCVList["Gen_vol"]==Gen_vol[i]]
                data_num=data_num["data_number"].values
                OCV=OCV.iloc[:,2*(data_num[0]-1):2*data_num[0]]
                OCV=OCV.dropna(axis=0)
                OCV.columns=["DOD[%]","Voltage[V]"]
                OCV_dod=np.array(OCV["DOD[%]"])
                OCV_vol=np.array(OCV["Voltage[V]"])
                capa=np.array(DF1["Capacity[mAh]"].values.flatten())
                vol=np.array(DF1["Voltage[V]"].values.flatten())
                min_vol=min(vol)
                arg_min_vol=np.argmin(vol)
                #最終電圧がカットvoltageと同じ場合
                if(min_vol==cut_vol[x]):
                    capa_cutV=capa[arg_min_vol-1]
                    capa_dod=capa/capa_cutV*100
                #最終電圧がカットvoltageより小さい場合
                elif(min_vol<cut_vol[x]):
                    capa_cutV=capa[arg_min_vol-1]+(capa[arg_min_vol-2]-capa[arg_min_vol-1])*(cut_vol[i]-vol[arg_min_vol-1])/(vol[arg_min_vol-2]-vol[arg_min_vol-1])
                    capa_dod=capa/capa_cutV*100
                #最終電圧がカットvoltageより高い場合
                else:
                    print("外挿補間結果です。")
                    capa_cutV=capa[arg_min_vol-1]+(capa[arg_min_vol-2]-capa[arg_min_vol-1])*(cut_vol[i]-vol[arg_min_vol-1])/(vol[arg_min_vol-2]-vol[arg_min_vol-1])
                    capa_dod=capa/capa_cutV*100
                cal_V=np.interp(OCV_dod,capa_dod,vol)
                Current=np.interp(OCV_dod,capa_dod,Current)
                delta_vol=OCV_vol-cal_V
                DC_resistance=delta_vol/(Current/1000)*1000
                DC_resistance=np.interp(dod,OCV_dod,DC_resistance)
                return DC_resistance #numpyデータ

            def information(x):
                capa=np.array(DF1["Capacity[mAh]"].values.flatten())
                vol=np.array(DF1["Voltage[V]"].values.flatten())
                vol_over30V=np.where(vol>=3.0)#3.0V以上
                capa_over30V=capa[vol_over30V]#3.0V以上の容量
                len_over30V=len(capa_over30V)-1#3.0V以上の長さ,0からはじまるので-1
                vol_over32V=np.where(vol>=3.2)#3.2V以上
                capa_over32V=capa[vol_over32V]#3.2V以上の容量
                len_over32V=len(capa_over32V)-1#3.2V以上の長さ,0からはじまるので-1
                vol_over34V=np.where(vol>=3.4)#3.4V以上
                capa_over34V=capa[vol_over34V]#3.4V以上の容量
                len_over34V=len(capa_over34V)-1#3.4V以上の長さ,0からはじまるので-1
                vol_over36V=np.where(vol>=3.6)#3.6V以上
                capa_over36V=capa[vol_over36V]#3.6V以上の容量
                len_over36V=len(capa_over36V)-1#3.6V以上の長さ,0からはじまるので-1
                vol_over38V=np.where(vol>=3.8)#3.8V以上
                capa_over38V=capa[vol_over38V]#3.8V以上の容量
                len_over38V=len(capa_over38V)-1#3.8V以上の長さ,0からはじまるので-1
                vol_over40V=np.where(vol>=4.0)#4.0V以上
                capa_over40V=capa[vol_over40V]#4.0V以上の容量
                len_over40V=len(capa_over40V)-1#4.0V以上の長さ,0からはじまるので-1
                vol_over275V=np.where(vol>=2.75)#2.75V以上
                capa_over275V=capa[vol_over275V]#2.75V以上の容量
                len_over275V=len(capa_over275V)-1#2.75V以上の長さ,0からはじまるので-1

                if(cut_vol[x]<=2.75):
                    if(cut_vol[x]==2.75):
                        capa_275V=capa[len_over275V]
                        ave_voltage_275V=np.average(vol[vol_over275V])
                        Energy_275V=ave_voltage_275V*capa_275V/1000
                    else:
                        capa_275V=capa[len_over275V]+(capa[len_over275V-1]-capa[len_over275V])*(2.75-vol[len_over275V])/(vol[len_over275V-1]-vol[len_over275V])
                        ave_voltage_275V=np.average(vol[vol_over275V])
                        Energy_275V=ave_voltage_275V*capa_275V/1000
                    capa_30V=capa[len_over30V]+(capa[len_over30V-1]-capa[len_over30V])*(3.0-vol[len_over30V])/(vol[len_over30V-1]-vol[len_over30V])
                    capa_32V=capa[len_over32V]+(capa[len_over32V-1]-capa[len_over32V])*(3.2-vol[len_over32V])/(vol[len_over32V-1]-vol[len_over32V])
                    capa_34V=capa[len_over34V]+(capa[len_over34V-1]-capa[len_over34V])*(3.4-vol[len_over34V])/(vol[len_over34V-1]-vol[len_over34V])
                    capa_36V=capa[len_over36V]+(capa[len_over36V-1]-capa[len_over36V])*(3.6-vol[len_over36V])/(vol[len_over36V-1]-vol[len_over36V])
                    capa_38V=capa[len_over38V]+(capa[len_over38V-1]-capa[len_over38V])*(3.8-vol[len_over38V])/(vol[len_over38V-1]-vol[len_over38V])
                    capa_40V=capa[len_over40V]+(capa[len_over40V-1]-capa[len_over40V])*(4.0-vol[len_over40V])/(vol[len_over40V-1]-vol[len_over40V])

                    ave_voltage_30V=np.average(vol[vol_over30V])
                    Energy_30V=ave_voltage_30V*capa_30V/1000
                    ave_voltage_32V=np.average(vol[vol_over32V])
                    Energy_32V=ave_voltage_32V*capa_32V/1000
                    ave_voltage_34V=np.average(vol[vol_over34V])
                    Energy_34V=ave_voltage_34V*capa_34V/1000
                    ave_voltage_36V=np.average(vol[vol_over36V])
                    Energy_36V=ave_voltage_36V*capa_36V/1000
                    ave_voltage_38V=np.average(vol[vol_over38V])
                    Energy_38V=ave_voltage_38V*capa_38V/1000
                    ave_voltage_40V=np.average(vol[vol_over40V])
                    Energy_40V=ave_voltage_40V*capa_40V/1000

                elif(cut_vol[x]<=3.0):
                    capa_275V=None
                    ave_voltage_275V=None
                    Energy_275V=None
                    if(cut_vol[x]==3.0):
                        capa_30V=capa[len_over30V]
                        ave_voltage_30V=np.average(vol[vol_over30V])
                        Energy_30V=ave_voltage_30V*capa_30V/1000
                    else:
                        capa_30V=capa[len_over30V]+(capa[len_over30V-1]-capa[len_over30V])*(3.0-vol[len_over30V])/(vol[len_over30V-1]-vol[len_over30V])
                        ave_voltage_30V=np.average(vol[vol_over30V])
                        Energy_30V=ave_voltage_30V*capa_30V/1000
                    capa_32V=capa[len_over32V]+(capa[len_over32V-1]-capa[len_over32V])*(3.2-vol[len_over32V])/(vol[len_over32V-1]-vol[len_over32V])
                    capa_34V=capa[len_over34V]+(capa[len_over34V-1]-capa[len_over34V])*(3.4-vol[len_over34V])/(vol[len_over34V-1]-vol[len_over34V])
                    capa_36V=capa[len_over36V]+(capa[len_over36V-1]-capa[len_over36V])*(3.6-vol[len_over36V])/(vol[len_over36V-1]-vol[len_over36V])
                    capa_38V=capa[len_over38V]+(capa[len_over38V-1]-capa[len_over38V])*(3.8-vol[len_over38V])/(vol[len_over38V-1]-vol[len_over38V])
                    capa_40V=capa[len_over40V]+(capa[len_over40V-1]-capa[len_over40V])*(4.0-vol[len_over40V])/(vol[len_over40V-1]-vol[len_over40V])
                    ave_voltage_32V=np.average(vol[vol_over32V])
                    Energy_32V=ave_voltage_32V*capa_32V/1000
                    ave_voltage_34V=np.average(vol[vol_over34V])
                    Energy_34V=ave_voltage_34V*capa_34V/1000
                    ave_voltage_36V=np.average(vol[vol_over36V])
                    Energy_36V=ave_voltage_36V*capa_36V/1000
                    ave_voltage_38V=np.average(vol[vol_over38V])
                    Energy_38V=ave_voltage_38V*capa_38V/1000
                    ave_voltage_40V=np.average(vol[vol_over40V])
                    Energy_40V=ave_voltage_40V*capa_40V/1000

                elif(cut_vol[x]<=3.2):
                    capa_275V=None
                    ave_voltage_275V=None
                    Energy_275V=None
                    capa_30V=None
                    ave_voltage_30V=None
                    Energy_30V=None
                    if(cut_vol[x]==3.2):
                        capa_32V=capa[len_over32V]
                        ave_voltage_32V=np.average(vol[vol_over32V])
                        Energy_32V=ave_voltage_32V*capa_32V/1000
                    else:
                        capa_32V=capa[len_over32V]+(capa[len_over32V-1]-capa[len_over32V])*(3.2-vol[len_over32V])/(vol[len_over32V-1]-vol[len_over32V])
                        ave_voltage_32V=np.average(vol[vol_over32V])
                        Energy_32V=ave_voltage_32V*capa_32V/1000
                    capa_34V=capa[len_over34V]+(capa[len_over34V-1]-capa[len_over34V])*(3.4-vol[len_over34V])/(vol[len_over34V-1]-vol[len_over34V])
                    capa_36V=capa[len_over36V]+(capa[len_over36V-1]-capa[len_over36V])*(3.6-vol[len_over36V])/(vol[len_over36V-1]-vol[len_over36V])
                    capa_38V=capa[len_over38V]+(capa[len_over38V-1]-capa[len_over38V])*(3.8-vol[len_over38V])/(vol[len_over38V-1]-vol[len_over38V])
                    capa_40V=capa[len_over40V]+(capa[len_over40V-1]-capa[len_over40V])*(4.0-vol[len_over40V])/(vol[len_over40V-1]-vol[len_over40V])
                    ave_voltage_34V=np.average(vol[vol_over34V])
                    Energy_34V=ave_voltage_34V*capa_34V/1000
                    ave_voltage_36V=np.average(vol[vol_over36V])
                    Energy_36V=ave_voltage_36V*capa_36V/1000
                    ave_voltage_38V=np.average(vol[vol_over38V])
                    Energy_38V=ave_voltage_38V*capa_38V/1000
                    ave_voltage_40V=np.average(vol[vol_over40V])
                    Energy_40V=ave_voltage_40V*capa_40V/1000

                elif(cut_vol[x]<=3.4):
                    capa_275V=None
                    ave_voltage_275V=None
                    Energy_275V=None
                    capa_30V=None
                    ave_voltage_30V=None
                    Energy_30V=None
                    capa_32V=None
                    ave_voltage_32V=None
                    Energy_32V=None
                    if(cut_vol[x]==3.4):
                        capa_34V=capa[len_over34V]
                        ave_voltage_34V=np.average(vol[vol_over34V])
                        Energy_34V=ave_voltage_34V*capa_34V/1000
                    else:
                        capa_34V=capa[len_over34V]+(capa[len_over34V-1]-capa[len_over34V])*(3.4-vol[len_over34V])/(vol[len_over34V-1]-vol[len_over34V])
                        ave_voltage_34V=np.average(vol[vol_over34V])
                        Energy_34V=ave_voltage_34V*capa_34V/1000
                    capa_36V=capa[len_over36V]+(capa[len_over36V-1]-capa[len_over36V])*(3.6-vol[len_over36V])/(vol[len_over36V-1]-vol[len_over36V])
                    capa_38V=capa[len_over38V]+(capa[len_over38V-1]-capa[len_over38V])*(3.8-vol[len_over38V])/(vol[len_over38V-1]-vol[len_over38V])
                    capa_40V=capa[len_over40V]+(capa[len_over40V-1]-capa[len_over40V])*(4.0-vol[len_over40V])/(vol[len_over40V-1]-vol[len_over40V])
                    ave_voltage_36V=np.average(vol[vol_over36V])
                    Energy_36V=ave_voltage_36V*capa_36V/1000
                    ave_voltage_38V=np.average(vol[vol_over38V])
                    Energy_38V=ave_voltage_38V*capa_38V/1000
                    ave_voltage_40V=np.average(vol[vol_over40V])
                    Energy_40V=ave_voltage_40V*capa_40V/1000

                elif(cut_vol[x]<=3.6):
                    capa_275V=None
                    ave_voltage_275V=None
                    Energy_275V=None
                    capa_30V=None
                    ave_voltage_30V=None
                    Energy_30V=None
                    capa_32V=None
                    ave_voltage_32V=None
                    Energy_32V=None
                    capa_34V=None
                    ave_voltage_34V=None
                    Energy_34V=None
                    if(cut_vol[x]==3.6):
                        capa_36V=capa[len_over36V]
                        ave_voltage_36V=np.average(vol[vol_over36V])
                        Energy_36V=ave_voltage_36V*capa_36V/1000
                    else:
                        capa_36V=capa[len_over36V]+(capa[len_over36V-1]-capa[len_over36V])*(3.6-vol[len_over36V])/(vol[len_over36V-1]-vol[len_over36V])
                        ave_voltage_36V=np.average(vol[vol_over36V])
                        Energy_36V=ave_voltage_36V*capa_36V/1000
                    capa_38V=capa[len_over38V]+(capa[len_over38V-1]-capa[len_over38V])*(3.8-vol[len_over38V])/(vol[len_over38V-1]-vol[len_over38V])
                    capa_40V=capa[len_over40V]+(capa[len_over40V-1]-capa[len_over40V])*(4.0-vol[len_over40V])/(vol[len_over40V-1]-vol[len_over40V])
                    ave_voltage_38V=np.average(vol[vol_over38V])
                    Energy_38V=ave_voltage_38V*capa_38V/1000
                    ave_voltage_40V=np.average(vol[vol_over40V])
                    Energy_40V=ave_voltage_40V*capa_40V/1000

                elif(cut_vol[x]<=3.8):
                    capa_275V=None
                    ave_voltage_275V=None
                    Energy_275V=None
                    capa_30V=None
                    ave_voltage_30V=None
                    Energy_30V=None
                    capa_32V=None
                    ave_voltage_32V=None
                    Energy_32V=None
                    capa_34V=None
                    ave_voltage_34V=None
                    Energy_34V=None
                    capa_36V=None
                    ave_voltage_36V=None
                    Energy_36V=None
                    if(cut_vol[x]==3.8):
                        capa_38V=capa[len_over38V]
                        ave_voltage_38V=np.average(vol[vol_over38V])
                        Energy_38V=ave_voltage_38V*capa_38V/1000
                    else:
                        capa_38V=capa[len_over38V]+(capa[len_over38V-1]-capa[len_over38V])*(3.8-vol[len_over38V])/(vol[len_over38V-1]-vol[len_over38V])
                        ave_voltage_38V=np.average(vol[vol_over38V])
                        Energy_38V=ave_voltage_38V*capa_38V/1000
                    capa_40V=capa[len_over40V]+(capa[len_over40V-1]-capa[len_over40V])*(4.0-vol[len_over40V])/(vol[len_over40V-1]-vol[len_over40V])
                    ave_voltage_40V=np.average(vol[vol_over40V])
                    Energy_40V=ave_voltage_40V*capa_40V/1000
                elif(cut_vol[x]<=4.0):
                    capa_275V=None
                    ave_voltage_275V=None
                    Energy_275V=None
                    capa_30V=None
                    ave_voltage_30V=None
                    Energy_30V=None
                    capa_32V=None
                    ave_voltage_32V=None
                    Energy_32V=None
                    capa_34V=None
                    ave_voltage_34V=None
                    Energy_34V=None
                    capa_36V=None
                    ave_voltage_36V=None
                    Energy_36V=None
                    capa_38V=None
                    ave_voltage_38V=None
                    Energy_38V=None
                    if(cut_vol[x]==4.0):
                        capa_40V=capa[len_over40V]
                        ave_voltage_40V=np.average(vol[vol_over40V])
                        Energy_40V=ave_voltage_40V*capa_40V/1000
                    else:
                        capa_40V=capa[len_over40V]+(capa[len_over40V-1]-capa[len_over40V])*(4.0-vol[len_over40V])/(vol[len_over40V-1]-vol[len_over40V])
                        ave_voltage_40V=np.average(vol[vol_over40V])
                        Energy_40V=ave_voltage_40V*capa_40V/1000
                else:
                    print("容量データは取り込めません。カーブデータのみ取り込みました。")
                    capa_275V=None
                    ave_voltage_275V=None
                    Energy_275V=None
                    capa_30V=None
                    ave_voltage_30V=None
                    Energy_30V=None
                    capa_32V=None
                    ave_voltage_32V=None
                    Energy_32V=None
                    capa_34V=None
                    ave_voltage_34V=None
                    Energy_34V=None
                    capa_36V=None
                    ave_voltage_36V=None
                    Energy_36V=None
                    capa_38V=None
                    ave_voltage_38V=None
                    Energy_38V=None
                    capa_40V=None
                    ave_voltage_40V=None
                    Energy_40V=None
                Try_lot=Lot[x][0:-4]
                info=[Lot[x],#セルロット
                      Try_lot,#水準ロット
                      day[x],#測定日
                      eq[x],#装置
                      ch[x],#チャンネル
                      TEMP[x],#測定温度
                      Gen[x],#世代
                      size[x],#サイズ
                      Charge_vol[x],#充電電圧
                      Charge_rate[x],#充電レート
                      Charge_cut_rate[x],#充電カットレート
                      RestC[x],#充電後休止時間
                      C_Rate,#放電レート
                      cut_vol[x],#放電カットレート
                      RestD[x],#放電後終止時間
                      capa_1C[x],#1C容量[mAh]
                      capa_40V,#4V容量
                      capa_38V,#3.8V容量
                      capa_36V,#3.6V容量
                      capa_34V,#3.4V容量
                      capa_32V,#3.2V容量
                      capa_30V,#3Vcut容量
                      capa_275V,#2.75Vcut容量
                      save_file,#カーブデータ保存先
                      Raw_file,#Rawデータ作成
                      min_Energy[x],#minEnergy
                      ave_voltage_275V,#2.75平均電圧
                      ave_voltage_30V,#3.0平均電圧
                      ave_voltage_32V,#3.2平均電圧
                      ave_voltage_34V,#3.4平均電圧
                      ave_voltage_36V,#3.6平均電圧
                      ave_voltage_38V,#3.8平均電圧
                      ave_voltage_40V,#4.0平均電圧
                      Energy_275V,#2.75エネルギー
                      Energy_30V,#3.0エネルギー
                      Energy_32V,#3.2エネルギー
                      Energy_34V,#3.4エネルギー
                      Energy_36V,#3.6エネルギー
                      Energy_38V,#3.8エネルギー
                      Energy_40V,#4.0エネルギー
                      Measurer[x]]#測定者
                info=pd.Series(info)
                return info
            #生データ
            Raw=pd.concat([DF1,DF1_2],axis=1)
            #curveデータについて
            #DOD
            DOD=pd.DataFrame(dod)
            DOD.columns=["DOD[%]"]
            #voltage
            DOD_curve_np=DOD_curve(i)
            DOD_curve_pd=pd.DataFrame(DOD_curve_np)
            DOD_curve_pd.columns=["Voltage[V]"]
            #dVdQ
            dVdQ=dVdQ(i)
            dVdQ_pd=pd.DataFrame(dVdQ)
            dVdQ_pd.columns=["dVdQ[V/mAh]"]
            #delta_voltage
            delta_vol=delta_vol(i)
            delta_vol_pd=pd.DataFrame(delta_vol)
            delta_vol_pd.columns=["delta_V[mV]"]
            #RC_resistance
            DC_resistance=DC_resistance(i)
            DC_resistance_pd=pd.DataFrame(DC_resistance)
            DC_resistance_pd.columns=["DC_resistance[mohm]"]

            Data=pd.concat([DOD,DOD_curve_pd,dVdQ_pd,delta_vol_pd,DC_resistance_pd],axis=1)
            #温度データがある場合
            if(temp_data[i]==1):
                temp=temp(i,k)
                Raw_temp=Raw_temp(i, k)
                max_temp=max(temp)
                info=information(i)
                info=np.append(info,max_temp)
                info=pd.DataFrame(info)
                info=info.T
                info.columns=["Cell-Lot",#セルロット
                              "Try-lot.",#水準ロット
                              "Day",#測定日
                              "Test_equipment",#装置
                              "ch",#チャンネル
                              "Temp[deg.C]",#測定温度
                              "Gen",#世代
                              "size",#サイズ
                              "Charge-voltage[V]",#充電電圧
                              "Charge-rate[C]",#充電レート
                              "Charge-cut-rate[C]",#充電カットレート
                              "Rest_afterC[min]",#充電後休止時間
                              "Discharge-rate[C]",#放電レート
                              "Discharge-cut-voltage[V]",#放電カットレート
                              "Rest_afterD[min]",#放電後終止時間
                              "min_rated_capacity[mAh]",#1C容量[mAh]
                              "Capacity_4.0V[mAh]",#4V容量
                              "Capacity_3.8V[mAh]",#3.8V容量
                              "Capacity_3.6V[mAh]",#3.6V容量
                              "Capacity_3.4V[mAh]",#3.4V容量
                              "Capacity_3.2V[mAh]",#3.2V容量
                              "Capacity_3.0V[mAh]",#3Vcut容量
                              "Capacity_2.75V[mAh]",#2.75V容量
                              "Curve_Data_Link",#カーブデータ保存先
                              "Raw_Data_Link",#生データ保管場所
                              "min_rated_Energy[Wh]",#minエネルギー
                              "Average-Voltage_2.75V[V]",#平均電圧
                              "Average-Voltage_3.0V[V]",
                              "Average-Voltage_3.2V[V]",
                              "Average-Voltage_3.4V[V]",
                              "Average-Voltage_3.6V[V]",
                              "Average-Voltage_3.8V[V]",
                              "Average-Voltage_4.0V[V]",
                              "Energy_2.75V[Wh]",#エネルギー
                              "Energy_3.0V[Wh]",
                              "Energy_3.2V[Wh]",
                              "Energy_3.4V[Wh]",
                              "Energy_3.6V[Wh]",
                              "Energy_3.8V[Wh]",
                              "Energy_4.0V[Wh]",
                              "Measurer",
                              "Max_cell_temp[deg.C]"]#温度データ
                temp_data=pd.DataFrame(temp)
                temp_data.columns=["Temp[deg.C]"]
                Data2=pd.concat([Data,temp_data],axis=1)
                Raw2=pd.concat([Raw,Raw_temp],axis=1)
            #温度データがない場合
            else:
                print("この水準は温度データは取り込みません")
                info=information(i)
                info=pd.DataFrame(info)
                info=info.T
                info.columns=["Cell-Lot",#セルロット
                              "Try-lot.",#水準ロット
                              "Day",#測定日
                              "Test_equipment",#装置
                              "ch",#チャンネル
                              "Temp[deg.C]",#測定温度
                              "Gen",#世代
                              "size",#サイズ
                              "Charge-voltage[V]",#充電電圧
                              "Charge-rate[C]",#充電レート
                              "Charge-cut-rate[C]",#充電カットレート
                              "Rest_afterC[min]",#充電後休止時間
                              "Discharge-rate[C]",#放電レート
                              "Discharge-cut-voltage[V]",#放電カットレート
                              "Rest_afterD[min]",#放電後終止時間
                              "min_rated_capacity[mAh]",#1C容量[mAh]
                              "Capacity_4.0V[mAh]",#4V容量
                              "Capacity_3.8V[mAh]",#3.8V容量
                              "Capacity_3.6V[mAh]",#3.6V容量
                              "Capacity_3.4V[mAh]",#3.4V容量
                              "Capacity_3.2V[mAh]",#3.2V容量
                              "Capacity_3.0V[mAh]",#3Vcut容量
                              "Capacity_2.75V[mAh]",#2.75V容量
                              "Curve_Data_Link",#カーブデータ保存先
                              "Raw_Data_Link",#生データ保管場所
                              "min_rated_Energy[Wh]",#minエネルギー
                              "Average-Voltage_2.75V[V]",#平均電圧
                              "Average-Voltage_3.0V[V]",
                              "Average-Voltage_3.2V[V]",
                              "Average-Voltage_3.4V[V]",
                              "Average-Voltage_3.6V[V]",
                              "Average-Voltage_3.8V[V]",
                              "Average-Voltage_4.0V[V]",
                              "Energy_2.75V[Wh]",#エネルギー
                              "Energy_3.0V[Wh]",
                              "Energy_3.2V[Wh]",
                              "Energy_3.4V[Wh]",
                              "Energy_3.6V[Wh]",
                              "Energy_3.8V[Wh]",
                              "Energy_4.0V[Wh]",
                              "Measurer"]
                Data2=Data
                Raw2=Raw
            Data2.to_csv(save_file,index=False)
            Raw2.to_csv(Raw_file,index=False)
            info2=pd.read_csv("C:\DataBase\Discharge_rate_Capability\Discharge_rate_Capability_used-cell.csv")
            info3=pd.concat([info2,info],axis=0)
            save_link="C:\DataBase\Discharge_rate_Capability\Cell_information"+"\Discharge_rate_Capability_used-cell"+"_"+time_stamp+".csv"
            info3.to_csv(save_link,index=False)

            #xサイクル目
            cycle=str(k+1)+"cyc目_取り込みok"
            print(cycle)

def Result_dis():

    #usedファイルの結合
    cell_info=os.listdir("C:\DataBase\Discharge_rate_Capability\Cell_information")
    CELL_INFO=[]

    for i in range(len(cell_info)):
        cell_info2="C:\DataBase\Discharge_rate_Capability\Cell_information"+"\\"+cell_info[i]
        CELL_INFO.append(cell_info2)
    cell_info3=[]
    for f in CELL_INFO:
        cell_info3.append(pd.read_csv(f,encoding="cp932"))
    df=pd.concat(cell_info3)
    #まとめデータ読み込み
    #df=pd.read_csv("C:\DataBase\Discharge_rate_Capability\Discharge_rate_Capability_used-cell.csv",encoding="cp932")
    ddf=pd.read_excel("C:\DataBase\Discharge_rate_Capability\Discharge_rate_Capability_Spec.xlsx",sheetname="Spec",encoding="cp932")

    def All1():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        while color_list2.count("")>0:
            color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
                    [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
                    [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
                    [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
                    [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
                    [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
    #len_Lot=len(Lot_List)#ロットのリスト長さ

    #--------------------------------------------------------------------------------------------------------------------
        for i in range(0,1):
        #for i in range(0,Lot_list):
            Rate=Rate_array[i]#ここは変える
            while Rate.count("")>0:
                Rate.remove("")
            len_Rate=len(Rate)
            Lot=Lot_list[i]
            #cm1=color_list1[i]
            C_V="Capacity_"+cut_vol+"[mAh]"
    #--------------------------------------------------------------------------------------------------------------------
            for j in range(0,len_Rate):
                rate=float(Rate[j])#レートの選択
                cm2=color_list2[j]#行のカラー
                df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
                df3=df2[df2["Discharge-rate[C]"]==rate]#
                C_V2=df3[C_V].values#カット電圧時の容量データ
                C_V2=C_V2[0]
                Link=df3["Curve_Data_Link"].values#カーブデータのファイルを開く。
                Link=Link[0]
                DF=pd.read_csv(Link,encoding="cp932")
                x=np.array(DF["DOD[%]"].values.flatten())#x(dod)
                y1=np.array(DF["Voltage[V]"].values.flatten())#y1(vol)
                y2=np.array(DF["dVdQ[V/mAh]"].values.flatten())#y2(dVdQ)
                y3=np.array(DF["delta_V[mV]"].values.flatten())#y3(deltaV)
                y4=np.array(DF["DC_resistance[mohm]"].values.flatten())#y4(DCR)
                if(initial_dod=="DOD"):
                    pass
                elif(initial_dod=="Reference"):
                    if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        C_1C=df3["min_rated_capacity[mAh]"].values
                        x1=C_02[0]
                        x2=C_1C[0]
                        x=x*x1/x2
                    else:#0.2C容量を掛けて、各レートの容量で割る。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        DF3=df2[df2["Discharge-rate[C]"]==float(ref)]#
                        C_V3=DF3[C_V].values#カット電圧時の容量データ
                        C_V3=C_V3[0]
                        x1=C_02[0]
                        x2=C_V3
                        x=x*x1/x2
                else:
                    "正しく選択されていません"

                NAME=Lot+"_"+Rate[j]
                #グラフ左上
                title_size=int(d.get())
                axisN_size=int(e.get())
                axis_size=int(f.get())
                font=g.get()
                plt.subplot(2,2,1)
                plt.title("DOD-voltage",fontsize=title_size,fontname=font)
                plt.plot(x,y1,color=cm2,label=NAME)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(2.95,4.5)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ右上
                plt.subplot(2,2,2)
                plt.title("dVdQ",fontsize=title_size,fontname=font)
                plt.plot(x,y2,color=cm2)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("dV/dQ[V/%]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(0,-0.05)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ左下
                plt.subplot(2,2,3)
                plt.title("delta_V",fontsize=title_size,fontname=font)
                plt.plot(x,y3,color=cm2)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("delta-V[mV]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(-5,505)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ右下
                plt.subplot(2,2,4)
                plt.title("DC-resistance",fontsize=title_size,fontname=font)
                plt.plot(x,y4,color=cm2)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("DC-resistanve[mΩ]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(-5,255)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()

        plt.show()
    def All2():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        while color_list2.count("")>0:
            color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
                    [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
                    [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
                    [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
                    [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
                    [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
    #len_Lot=len(Lot_List)#ロットのリスト長さ

    #--------------------------------------------------------------------------------------------------------------------
        for i in range(1,2):
        #for i in range(0,Lot_list):
            Rate=Rate_array[i]#ここは変える
            while Rate.count("")>0:
                Rate.remove("")
            len_Rate=len(Rate)
            Lot=Lot_list[i]
            #cm1=color_list1[i]
            C_V="Capacity_"+cut_vol+"[mAh]"
    #--------------------------------------------------------------------------------------------------------------------
            for j in range(0,len_Rate):
                rate=float(Rate[j])#レートの選択
                cm2=color_list2[j]#行のカラー
                df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
                df3=df2[df2["Discharge-rate[C]"]==rate]#
                C_V2=df3[C_V].values#カット電圧時の容量データ
                C_V2=C_V2[0]
                Link=df3["Curve_Data_Link"].values#カーブデータのファイルを開く。
                Link=Link[0]
                DF=pd.read_csv(Link,encoding="cp932")
                x=np.array(DF["DOD[%]"].values.flatten())#x(dod)
                y1=np.array(DF["Voltage[V]"].values.flatten())#y1(vol)
                y2=np.array(DF["dVdQ[V/mAh]"].values.flatten())#y2(dVdQ)
                y3=np.array(DF["delta_V[mV]"].values.flatten())#y3(deltaV)
                y4=np.array(DF["DC_resistance[mohm]"].values.flatten())#y4(DCR)
                if(initial_dod=="DOD"):
                    pass
                elif(initial_dod=="Reference"):
                    if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        C_1C=df3["min_rated_capacity[mAh]"].values
                        x1=C_02[0]
                        x2=C_1C[0]
                        x=x*x1/x2
                    else:#0.2C容量を掛けて、各レートの容量で割る。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        DF3=df2[df2["Discharge-rate[C]"]==float(ref)]#
                        C_V3=DF3[C_V].values#カット電圧時の容量データ
                        C_V3=C_V3[0]
                        x1=C_02[0]
                        x2=C_V3
                        x=x*x1/x2
                else:
                    "正しく選択されていません"

                NAME=Lot+"_"+Rate[j]
                #グラフ左上
                title_size=int(d.get())
                axisN_size=int(e.get())
                axis_size=int(f.get())
                font=g.get()
                plt.subplot(2,2,1)
                plt.title("DOD-voltage",fontsize=title_size,fontname=font)
                plt.plot(x,y1,color=cm2,label=NAME)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(2.95,4.5)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ右上
                plt.subplot(2,2,2)
                plt.title("dVdQ",fontsize=title_size,fontname=font)
                plt.plot(x,y2,color=cm2)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("dV/dQ[V/%]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(0,-0.05)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ左下
                plt.subplot(2,2,3)
                plt.title("delta_V",fontsize=title_size,fontname=font)
                plt.plot(x,y3,color=cm2)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("delta-V[mV]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(-5,505)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ右下
                plt.subplot(2,2,4)
                plt.title("DC-resistance",fontsize=title_size,fontname=font)
                plt.plot(x,y4,color=cm2)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("DC-resistanve[mΩ]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(-5,255)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()

        plt.show()
    def All3():

    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        while color_list2.count("")>0:
            color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
                    [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
                    [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
                    [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
                    [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
                    [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
    #len_Lot=len(Lot_List)#ロットのリスト長さ

    #--------------------------------------------------------------------------------------------------------------------
        for i in range(2,3):
        #for i in range(0,Lot_list):
            Rate=Rate_array[i]#ここは変える
            while Rate.count("")>0:
                Rate.remove("")
            len_Rate=len(Rate)
            Lot=Lot_list[i]
            #cm1=color_list1[i]
            C_V="Capacity_"+cut_vol+"[mAh]"
    #--------------------------------------------------------------------------------------------------------------------
            for j in range(0,len_Rate):
                rate=float(Rate[j])#レートの選択
                cm2=color_list2[j]#行のカラー
                df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
                df3=df2[df2["Discharge-rate[C]"]==rate]#
                C_V2=df3[C_V].values#カット電圧時の容量データ
                C_V2=C_V2[0]
                Link=df3["Curve_Data_Link"].values#カーブデータのファイルを開く。
                Link=Link[0]
                DF=pd.read_csv(Link,encoding="cp932")
                x=np.array(DF["DOD[%]"].values.flatten())#x(dod)
                y1=np.array(DF["Voltage[V]"].values.flatten())#y1(vol)
                y2=np.array(DF["dVdQ[V/mAh]"].values.flatten())#y2(dVdQ)
                y3=np.array(DF["delta_V[mV]"].values.flatten())#y3(deltaV)
                y4=np.array(DF["DC_resistance[mohm]"].values.flatten())#y4(DCR)
                if(initial_dod=="DOD"):
                    pass
                elif(initial_dod=="Reference"):
                    if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        C_1C=df3["min_rated_capacity[mAh]"].values
                        x1=C_02[0]
                        x2=C_1C[0]
                        x=x*x1/x2
                    else:#0.2C容量を掛けて、各レートの容量で割る。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        DF3=df2[df2["Discharge-rate[C]"]==float(ref)]#
                        C_V3=DF3[C_V].values#カット電圧時の容量データ
                        C_V3=C_V3[0]
                        x1=C_02[0]
                        x2=C_V3
                        x=x*x1/x2
                else:
                    "正しく選択されていません"

                NAME=Lot+"_"+Rate[j]
                #グラフ左上
                title_size=int(d.get())
                axisN_size=int(e.get())
                axis_size=int(f.get())
                font=g.get()
                plt.subplot(2,2,1)
                plt.title("DOD-voltage",fontsize=title_size,fontname=font)
                plt.plot(x,y1,color=cm2,label=NAME)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(2.95,4.5)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ右上
                plt.subplot(2,2,2)
                plt.title("dVdQ",fontsize=title_size,fontname=font)
                plt.plot(x,y2,color=cm2)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("dV/dQ[V/%]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(0,-0.05)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ左下
                plt.subplot(2,2,3)
                plt.title("delta_V",fontsize=title_size,fontname=font)
                plt.plot(x,y3,color=cm2)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("delta-V[mV]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(-5,505)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ右下
                plt.subplot(2,2,4)
                plt.title("DC-resistance",fontsize=title_size,fontname=font)
                plt.plot(x,y4,color=cm2)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("DC-resistanve[mΩ]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(-5,255)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
        plt.show()
    def All4():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        while color_list2.count("")>0:
            color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
                    [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
                    [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
                    [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
                    [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
                    [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
    #len_Lot=len(Lot_List)#ロットのリスト長さ

    #--------------------------------------------------------------------------------------------------------------------
        for i in range(3,4):
        #for i in range(0,Lot_list):
            Rate=Rate_array[i]#ここは変える
            while Rate.count("")>0:
                Rate.remove("")
            len_Rate=len(Rate)
            Lot=Lot_list[i]
            #cm1=color_list1[i]
            C_V="Capacity_"+cut_vol+"[mAh]"
    #--------------------------------------------------------------------------------------------------------------------
            for j in range(0,len_Rate):
                rate=float(Rate[j])#レートの選択
                cm2=color_list2[j]#行のカラー
                df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
                df3=df2[df2["Discharge-rate[C]"]==rate]#
                C_V2=df3[C_V].values#カット電圧時の容量データ
                C_V2=C_V2[0]
                Link=df3["Curve_Data_Link"].values#カーブデータのファイルを開く。
                Link=Link[0]
                DF=pd.read_csv(Link,encoding="cp932")
                x=np.array(DF["DOD[%]"].values.flatten())#x(dod)
                y1=np.array(DF["Voltage[V]"].values.flatten())#y1(vol)
                y2=np.array(DF["dVdQ[V/mAh]"].values.flatten())#y2(dVdQ)
                y3=np.array(DF["delta_V[mV]"].values.flatten())#y3(deltaV)
                y4=np.array(DF["DC_resistance[mohm]"].values.flatten())#y4(DCR)
                if(initial_dod=="DOD"):
                    pass
                elif(initial_dod=="Reference"):
                    if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        C_1C=df3["min_rated_capacity[mAh]"].values
                        x1=C_02[0]
                        x2=C_1C[0]
                        x=x*x1/x2
                    else:#0.2C容量を掛けて、各レートの容量で割る。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        DF3=df2[df2["Discharge-rate[C]"]==float(ref)]#
                        C_V3=DF3[C_V].values#カット電圧時の容量データ
                        C_V3=C_V3[0]
                        x1=C_02[0]
                        x2=C_V3
                        x=x*x1/x2
                else:
                    "正しく選択されていません"

                NAME=Lot+"_"+Rate[j]
                #グラフ左上
                title_size=int(d.get())
                axisN_size=int(e.get())
                axis_size=int(f.get())
                font=g.get()
                plt.subplot(2,2,1)
                plt.title("DOD-voltage",fontsize=title_size,fontname=font)
                plt.plot(x,y1,color=cm2,label=NAME)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(2.95,4.5)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ右上
                plt.subplot(2,2,2)
                plt.title("dVdQ",fontsize=title_size,fontname=font)
                plt.plot(x,y2,color=cm2)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("dV/dQ[V/%]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(0,-0.05)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ左下
                plt.subplot(2,2,3)
                plt.title("delta_V",fontsize=title_size,fontname=font)
                plt.plot(x,y3,color=cm2)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("delta-V[mV]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(-5,505)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ右下
                plt.subplot(2,2,4)
                plt.title("DC-resistance",fontsize=title_size,fontname=font)
                plt.plot(x,y4,color=cm2)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("DC-resistanve[mΩ]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(-5,255)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()

        plt.show()
    def All5():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        while color_list2.count("")>0:
            color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
                    [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
                    [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
                    [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
                    [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
                    [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
    #len_Lot=len(Lot_List)#ロットのリスト長さ

    #--------------------------------------------------------------------------------------------------------------------
        for i in range(4,5):
        #for i in range(0,Lot_list):
            Rate=Rate_array[i]#ここは変える
            while Rate.count("")>0:
                Rate.remove("")
            len_Rate=len(Rate)
            Lot=Lot_list[i]
            #cm1=color_list1[i]
            C_V="Capacity_"+cut_vol+"[mAh]"
    #--------------------------------------------------------------------------------------------------------------------
            for j in range(0,len_Rate):
                rate=float(Rate[j])#レートの選択
                cm2=color_list2[j]#行のカラー
                df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
                df3=df2[df2["Discharge-rate[C]"]==rate]#
                C_V2=df3[C_V].values#カット電圧時の容量データ
                C_V2=C_V2[0]
                Link=df3["Curve_Data_Link"].values#カーブデータのファイルを開く。
                Link=Link[0]
                DF=pd.read_csv(Link,encoding="cp932")
                x=np.array(DF["DOD[%]"].values.flatten())#x(dod)
                y1=np.array(DF["Voltage[V]"].values.flatten())#y1(vol)
                y2=np.array(DF["dVdQ[V/mAh]"].values.flatten())#y2(dVdQ)
                y3=np.array(DF["delta_V[mV]"].values.flatten())#y3(deltaV)
                y4=np.array(DF["DC_resistance[mohm]"].values.flatten())#y4(DCR)
                if(initial_dod=="DOD"):
                    pass
                elif(initial_dod=="Reference"):
                    if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        C_1C=df3["min_rated_capacity[mAh]"].values
                        x1=C_02[0]
                        x2=C_1C[0]
                        x=x*x1/x2
                    else:#0.2C容量を掛けて、各レートの容量で割る。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        DF3=df2[df2["Discharge-rate[C]"]==float(ref)]#
                        C_V3=DF3[C_V].values#カット電圧時の容量データ
                        C_V3=C_V3[0]
                        x1=C_02[0]
                        x2=C_V3
                        x=x*x1/x2
                else:
                    "正しく選択されていません"

                NAME=Lot+"_"+Rate[j]
                #グラフ左上
                title_size=int(d.get())
                axisN_size=int(e.get())
                axis_size=int(f.get())
                font=g.get()
                plt.subplot(2,2,1)
                plt.title("DOD-voltage",fontsize=title_size,fontname=font)
                plt.plot(x,y1,color=cm2,label=NAME)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(2.95,4.5)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ右上
                plt.subplot(2,2,2)
                plt.title("dVdQ",fontsize=title_size,fontname=font)
                plt.plot(x,y2,color=cm2)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("dV/dQ[V/%]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(0,-0.05)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ左下
                plt.subplot(2,2,3)
                plt.title("delta_V",fontsize=title_size,fontname=font)
                plt.plot(x,y3,color=cm2)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("delta-V[mV]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(-5,505)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ右下
                plt.subplot(2,2,4)
                plt.title("DC-resistance",fontsize=title_size,fontname=font)
                plt.plot(x,y4,color=cm2)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("DC-resistanve[mΩ]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(-5,255)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()

        plt.show()
    def All6():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        while color_list2.count("")>0:
            color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
                    [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
                    [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
                    [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
                    [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
                    [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
    #len_Lot=len(Lot_List)#ロットのリスト長さ

    #--------------------------------------------------------------------------------------------------------------------
        for i in range(5,6):
        #for i in range(0,Lot_list):
            Rate=Rate_array[i]#ここは変える
            while Rate.count("")>0:
                Rate.remove("")
            len_Rate=len(Rate)
            Lot=Lot_list[i]
            #cm1=color_list1[i]
            C_V="Capacity_"+cut_vol+"[mAh]"
    #--------------------------------------------------------------------------------------------------------------------
            for j in range(0,len_Rate):
                rate=float(Rate[j])#レートの選択
                cm2=color_list2[j]#行のカラー
                df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
                df3=df2[df2["Discharge-rate[C]"]==rate]#
                C_V2=df3[C_V].values#カット電圧時の容量データ
                C_V2=C_V2[0]
                Link=df3["Curve_Data_Link"].values#カーブデータのファイルを開く。
                Link=Link[0]
                DF=pd.read_csv(Link,encoding="cp932")
                x=np.array(DF["DOD[%]"].values.flatten())#x(dod)
                y1=np.array(DF["Voltage[V]"].values.flatten())#y1(vol)
                y2=np.array(DF["dVdQ[V/mAh]"].values.flatten())#y2(dVdQ)
                y3=np.array(DF["delta_V[mV]"].values.flatten())#y3(deltaV)
                y4=np.array(DF["DC_resistance[mohm]"].values.flatten())#y4(DCR)
                if(initial_dod=="DOD"):
                    pass
                elif(initial_dod=="Reference"):
                    if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        C_1C=df3["min_rated_capacity[mAh]"].values
                        x1=C_02[0]
                        x2=C_1C[0]
                        x=x*x1/x2
                    else:#0.2C容量を掛けて、各レートの容量で割る。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        DF3=df2[df2["Discharge-rate[C]"]==float(ref)]#
                        C_V3=DF3[C_V].values#カット電圧時の容量データ
                        C_V3=C_V3[0]
                        x1=C_02[0]
                        x2=C_V3
                        x=x*x1/x2
                else:
                    "正しく選択されていません"

                NAME=Lot+"_"+Rate[j]
                #グラフ左上
                title_size=int(d.get())
                axisN_size=int(e.get())
                axis_size=int(f.get())
                font=g.get()
                plt.subplot(2,2,1)
                plt.title("DOD-voltage",fontsize=title_size,fontname=font)
                plt.plot(x,y1,color=cm2,label=NAME)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(2.95,4.5)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ右上
                plt.subplot(2,2,2)
                plt.title("dVdQ",fontsize=title_size,fontname=font)
                plt.plot(x,y2,color=cm2)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("dV/dQ[V/%]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(0,-0.05)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ左下
                plt.subplot(2,2,3)
                plt.title("delta_V",fontsize=title_size,fontname=font)
                plt.plot(x,y3,color=cm2)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("delta-V[mV]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(-5,505)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ右下
                plt.subplot(2,2,4)
                plt.title("DC-resistance",fontsize=title_size,fontname=font)
                plt.plot(x,y4,color=cm2)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("DC-resistanve[mΩ]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(-5,255)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()

        plt.show()
    def All7():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        while color_list2.count("")>0:
            color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
                    [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
                    [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
                    [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
                    [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
                    [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
        len_Lot=len(Lot_list)#ロットのリスト長さ

    #--------------------------------------------------------------------------------------------------------------------
        #for i in range(5,6):
        for i in range(0,len_Lot):
            Rate=Rate_array[i]#ここは変える
            while Rate.count("")>0:
                Rate.remove("")
            #len_Rate=len(Rate)
            Lot=Lot_list[i]
            cm2=color_list1[i]
            C_V="Capacity_"+cut_vol+"[mAh]"
    #--------------------------------------------------------------------------------------------------------------------
            for j in range(0,1):
            #for j in range(0,len_Rate)
                rate=float(Rate[j])#レートの選択
                #cm2=color_list2[j]#行のカラー
                df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
                df3=df2[df2["Discharge-rate[C]"]==rate]#
                C_V2=df3[C_V].values#カット電圧時の容量データ
                C_V2=C_V2[0]
                Link=df3["Curve_Data_Link"].values#カーブデータのファイルを開く。
                Link=Link[0]
                DF=pd.read_csv(Link,encoding="cp932")
                x=np.array(DF["DOD[%]"].values.flatten())#x(dod)
                y1=np.array(DF["Voltage[V]"].values.flatten())#y1(vol)
                y2=np.array(DF["dVdQ[V/mAh]"].values.flatten())#y2(dVdQ)
                y3=np.array(DF["delta_V[mV]"].values.flatten())#y3(deltaV)
                y4=np.array(DF["DC_resistance[mohm]"].values.flatten())#y4(DCR)
                if(initial_dod=="DOD"):
                    pass
                elif(initial_dod=="Reference"):
                    if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        C_1C=df3["min_rated_capacity[mAh]"].values
                        x1=C_02[0]
                        x2=C_1C[0]
                        x=x*x1/x2
                    else:#0.2C容量を掛けて、各レートの容量で割る。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        DF3=df2[df2["Discharge-rate[C]"]==float(ref)]#
                        C_V3=DF3[C_V].values#カット電圧時の容量データ
                        C_V3=C_V3[0]
                        x1=C_02[0]
                        x2=C_V3
                        x=x*x1/x2
                else:
                    "正しく選択されていません"

                NAME=Lot+"_"+Rate[j]
                #グラフ左上
                title_size=int(d.get())
                axisN_size=int(e.get())
                axis_size=int(f.get())
                font=g.get()
                plt.subplot(2,2,1)
                plt.title("DOD-voltage",fontsize=title_size,fontname=font)
                plt.plot(x,y1,color=cm2,label=NAME)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(2.95,4.5)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ右上
                plt.subplot(2,2,2)
                plt.title("dVdQ",fontsize=title_size,fontname=font)
                plt.plot(x,y2,color=cm2)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("dV/dQ[V/%]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(0,-0.05)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ左下
                plt.subplot(2,2,3)
                plt.title("delta_V",fontsize=title_size,fontname=font)
                plt.plot(x,y3,color=cm2)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("delta-V[mV]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(-5,505)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ右下
                plt.subplot(2,2,4)
                plt.title("DC-resistance",fontsize=title_size,fontname=font)
                plt.plot(x,y4,color=cm2)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("DC-resistanve[mΩ]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(-5,255)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()

        plt.show()
    def All8():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        while color_list2.count("")>0:
            color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
                    [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
                    [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
                    [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
                    [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
                    [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
        len_Lot=len(Lot_list)#ロットのリスト長さ

    #--------------------------------------------------------------------------------------------------------------------
        #for i in range(5,6):
        for i in range(0,len_Lot):
            Rate=Rate_array[i]#ここは変える
            while Rate.count("")>0:
                Rate.remove("")
            #len_Rate=len(Rate)
            Lot=Lot_list[i]
            cm2=color_list1[i]
            C_V="Capacity_"+cut_vol+"[mAh]"
    #--------------------------------------------------------------------------------------------------------------------
            for j in range(1,2):
            #for j in range(0,len_Rate)
                rate=float(Rate[j])#レートの選択
                #cm2=color_list2[j]#行のカラー
                df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
                df3=df2[df2["Discharge-rate[C]"]==rate]#
                C_V2=df3[C_V].values#カット電圧時の容量データ
                C_V2=C_V2[0]
                Link=df3["Curve_Data_Link"].values#カーブデータのファイルを開く。
                Link=Link[0]
                DF=pd.read_csv(Link,encoding="cp932")
                x=np.array(DF["DOD[%]"].values.flatten())#x(dod)
                y1=np.array(DF["Voltage[V]"].values.flatten())#y1(vol)
                y2=np.array(DF["dVdQ[V/mAh]"].values.flatten())#y2(dVdQ)
                y3=np.array(DF["delta_V[mV]"].values.flatten())#y3(deltaV)
                y4=np.array(DF["DC_resistance[mohm]"].values.flatten())#y4(DCR)
                if(initial_dod=="DOD"):
                    pass
                elif(initial_dod=="Reference"):
                    if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        C_1C=df3["min_rated_capacity[mAh]"].values
                        x1=C_02[0]
                        x2=C_1C[0]
                        x=x*x1/x2
                    else:#0.2C容量を掛けて、各レートの容量で割る。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        DF3=df2[df2["Discharge-rate[C]"]==float(ref)]#
                        C_V3=DF3[C_V].values#カット電圧時の容量データ
                        C_V3=C_V3[0]
                        x1=C_02[0]
                        x2=C_V3
                        x=x*x1/x2
                else:
                    "正しく選択されていません"

                NAME=Lot+"_"+Rate[j]
                #グラフ左上
                title_size=int(d.get())
                axisN_size=int(e.get())
                axis_size=int(f.get())
                font=g.get()
                plt.subplot(2,2,1)
                plt.title("DOD-voltage",fontsize=title_size,fontname=font)
                plt.plot(x,y1,color=cm2,label=NAME)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(2.95,4.5)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ右上
                plt.subplot(2,2,2)
                plt.title("dVdQ",fontsize=title_size,fontname=font)
                plt.plot(x,y2,color=cm2)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("dV/dQ[V/%]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(0,-0.05)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ左下
                plt.subplot(2,2,3)
                plt.title("delta_V",fontsize=title_size,fontname=font)
                plt.plot(x,y3,color=cm2)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("delta-V[mV]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(-5,505)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ右下
                plt.subplot(2,2,4)
                plt.title("DC-resistance",fontsize=title_size,fontname=font)
                plt.plot(x,y4,color=cm2)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("DC-resistanve[mΩ]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(-5,255)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()

        plt.show()
    def All9():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        while color_list2.count("")>0:
            color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
                    [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
                    [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
                    [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
                    [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
                    [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
        len_Lot=len(Lot_list)#ロットのリスト長さ

    #--------------------------------------------------------------------------------------------------------------------
        #for i in range(5,6):
        for i in range(0,len_Lot):
            Rate=Rate_array[i]#ここは変える
            while Rate.count("")>0:
                Rate.remove("")
            #len_Rate=len(Rate)
            Lot=Lot_list[i]
            cm2=color_list1[i]
            C_V="Capacity_"+cut_vol+"[mAh]"
    #--------------------------------------------------------------------------------------------------------------------
            for j in range(2,3):
            #for j in range(0,len_Rate)
                rate=float(Rate[j])#レートの選択
                #cm2=color_list2[j]#行のカラー
                df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
                df3=df2[df2["Discharge-rate[C]"]==rate]#
                C_V2=df3[C_V].values#カット電圧時の容量データ
                C_V2=C_V2[0]
                Link=df3["Curve_Data_Link"].values#カーブデータのファイルを開く。
                Link=Link[0]
                DF=pd.read_csv(Link,encoding="cp932")
                x=np.array(DF["DOD[%]"].values.flatten())#x(dod)
                y1=np.array(DF["Voltage[V]"].values.flatten())#y1(vol)
                y2=np.array(DF["dVdQ[V/mAh]"].values.flatten())#y2(dVdQ)
                y3=np.array(DF["delta_V[mV]"].values.flatten())#y3(deltaV)
                y4=np.array(DF["DC_resistance[mohm]"].values.flatten())#y4(DCR)
                if(initial_dod=="DOD"):
                    pass
                elif(initial_dod=="Reference"):
                    if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        C_1C=df3["min_rated_capacity[mAh]"].values
                        x1=C_02[0]
                        x2=C_1C[0]
                        x=x*x1/x2
                    else:#0.2C容量を掛けて、各レートの容量で割る。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        DF3=df2[df2["Discharge-rate[C]"]==float(ref)]#
                        C_V3=DF3[C_V].values#カット電圧時の容量データ
                        C_V3=C_V3[0]
                        x1=C_02[0]
                        x2=C_V3
                        x=x*x1/x2
                else:
                    "正しく選択されていません"

                NAME=Lot+"_"+Rate[j]
                #グラフ左上
                title_size=int(d.get())
                axisN_size=int(e.get())
                axis_size=int(f.get())
                font=g.get()
                plt.subplot(2,2,1)
                plt.title("DOD-voltage",fontsize=title_size,fontname=font)
                plt.plot(x,y1,color=cm2,label=NAME)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(2.95,4.5)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ右上
                plt.subplot(2,2,2)
                plt.title("dVdQ",fontsize=title_size,fontname=font)
                plt.plot(x,y2,color=cm2)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("dV/dQ[V/%]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(0,-0.05)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ左下
                plt.subplot(2,2,3)
                plt.title("delta_V",fontsize=title_size,fontname=font)
                plt.plot(x,y3,color=cm2)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("delta-V[mV]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(-5,505)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ右下
                plt.subplot(2,2,4)
                plt.title("DC-resistance",fontsize=title_size,fontname=font)
                plt.plot(x,y4,color=cm2)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("DC-resistanve[mΩ]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(-5,255)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()

        plt.show()
    def All10():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        while color_list2.count("")>0:
            color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
                    [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
                    [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
                    [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
                    [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
                    [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
        len_Lot=len(Lot_list)#ロットのリスト長さ

    #--------------------------------------------------------------------------------------------------------------------
        #for i in range(5,6):
        for i in range(0,len_Lot):
            Rate=Rate_array[i]#ここは変える
            while Rate.count("")>0:
                Rate.remove("")
            #len_Rate=len(Rate)
            Lot=Lot_list[i]
            cm2=color_list1[i]
            C_V="Capacity_"+cut_vol+"[mAh]"
    #--------------------------------------------------------------------------------------------------------------------
            for j in range(3,4):
            #for j in range(0,len_Rate)
                rate=float(Rate[j])#レートの選択
                #cm2=color_list2[j]#行のカラー
                df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
                df3=df2[df2["Discharge-rate[C]"]==rate]#
                C_V2=df3[C_V].values#カット電圧時の容量データ
                C_V2=C_V2[0]
                Link=df3["Curve_Data_Link"].values#カーブデータのファイルを開く。
                Link=Link[0]
                DF=pd.read_csv(Link,encoding="cp932")
                x=np.array(DF["DOD[%]"].values.flatten())#x(dod)
                y1=np.array(DF["Voltage[V]"].values.flatten())#y1(vol)
                y2=np.array(DF["dVdQ[V/mAh]"].values.flatten())#y2(dVdQ)
                y3=np.array(DF["delta_V[mV]"].values.flatten())#y3(deltaV)
                y4=np.array(DF["DC_resistance[mohm]"].values.flatten())#y4(DCR)
                if(initial_dod=="DOD"):
                    pass
                elif(initial_dod=="Reference"):
                    if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        C_1C=df3["min_rated_capacity[mAh]"].values
                        x1=C_02[0]
                        x2=C_1C[0]
                        x=x*x1/x2
                    else:#0.2C容量を掛けて、各レートの容量で割る。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        DF3=df2[df2["Discharge-rate[C]"]==float(ref)]#
                        C_V3=DF3[C_V].values#カット電圧時の容量データ
                        C_V3=C_V3[0]
                        x1=C_02[0]
                        x2=C_V3
                        x=x*x1/x2
                else:
                    "正しく選択されていません"

                NAME=Lot+"_"+Rate[j]
                #グラフ左上
                title_size=int(d.get())
                axisN_size=int(e.get())
                axis_size=int(f.get())
                font=g.get()
                plt.subplot(2,2,1)
                plt.title("DOD-voltage",fontsize=title_size,fontname=font)
                plt.plot(x,y1,color=cm2,label=NAME)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(2.95,4.5)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ右上
                plt.subplot(2,2,2)
                plt.title("dVdQ",fontsize=title_size,fontname=font)
                plt.plot(x,y2,color=cm2)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("dV/dQ[V/%]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(0,-0.05)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ左下
                plt.subplot(2,2,3)
                plt.title("delta_V",fontsize=title_size,fontname=font)
                plt.plot(x,y3,color=cm2)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("delta-V[mV]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(-5,505)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ右下
                plt.subplot(2,2,4)
                plt.title("DC-resistance",fontsize=title_size,fontname=font)
                plt.plot(x,y4,color=cm2)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("DC-resistanve[mΩ]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(-5,255)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()

        plt.show()
    def All11():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        while color_list2.count("")>0:
            color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
                    [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
                    [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
                    [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
                    [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
                    [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
        len_Lot=len(Lot_list)#ロットのリスト長さ

    #--------------------------------------------------------------------------------------------------------------------
        #for i in range(5,6):
        for i in range(0,len_Lot):
            Rate=Rate_array[i]#ここは変える
            while Rate.count("")>0:
                Rate.remove("")
            #len_Rate=len(Rate)
            Lot=Lot_list[i]
            cm2=color_list1[i]
            C_V="Capacity_"+cut_vol+"[mAh]"
    #--------------------------------------------------------------------------------------------------------------------
            for j in range(4,5):
            #for j in range(0,len_Rate)
                rate=float(Rate[j])#レートの選択
                #cm2=color_list2[j]#行のカラー
                df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
                df3=df2[df2["Discharge-rate[C]"]==rate]#
                C_V2=df3[C_V].values#カット電圧時の容量データ
                C_V2=C_V2[0]
                Link=df3["Curve_Data_Link"].values#カーブデータのファイルを開く。
                Link=Link[0]
                DF=pd.read_csv(Link,encoding="cp932")
                x=np.array(DF["DOD[%]"].values.flatten())#x(dod)
                y1=np.array(DF["Voltage[V]"].values.flatten())#y1(vol)
                y2=np.array(DF["dVdQ[V/mAh]"].values.flatten())#y2(dVdQ)
                y3=np.array(DF["delta_V[mV]"].values.flatten())#y3(deltaV)
                y4=np.array(DF["DC_resistance[mohm]"].values.flatten())#y4(DCR)
                if(initial_dod=="DOD"):
                    pass
                elif(initial_dod=="Reference"):
                    if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        C_1C=df3["min_rated_capacity[mAh]"].values
                        x1=C_02[0]
                        x2=C_1C[0]
                        x=x*x1/x2
                    else:#0.2C容量を掛けて、各レートの容量で割る。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        DF3=df2[df2["Discharge-rate[C]"]==float(ref)]#
                        C_V3=DF3[C_V].values#カット電圧時の容量データ
                        C_V3=C_V3[0]
                        x1=C_02[0]
                        x2=C_V3
                        x=x*x1/x2
                else:
                    "正しく選択されていません"

                NAME=Lot+"_"+Rate[j]
                #グラフ左上
                title_size=int(d.get())
                axisN_size=int(e.get())
                axis_size=int(f.get())
                font=g.get()
                plt.subplot(2,2,1)
                plt.title("DOD-voltage",fontsize=title_size,fontname=font)
                plt.plot(x,y1,color=cm2,label=NAME)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(2.95,4.5)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ右上
                plt.subplot(2,2,2)
                plt.title("dVdQ",fontsize=title_size,fontname=font)
                plt.plot(x,y2,color=cm2)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("dV/dQ[V/%]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(0,-0.05)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ左下
                plt.subplot(2,2,3)
                plt.title("delta_V",fontsize=title_size,fontname=font)
                plt.plot(x,y3,color=cm2)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("delta-V[mV]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(-5,505)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ右下
                plt.subplot(2,2,4)
                plt.title("DC-resistance",fontsize=title_size,fontname=font)
                plt.plot(x,y4,color=cm2)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("DC-resistanve[mΩ]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(-5,255)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()

        plt.show()
    def All12():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        while color_list2.count("")>0:
            color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
                    [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
                    [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
                    [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
                    [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
                    [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
        len_Lot=len(Lot_list)#ロットのリスト長さ

    #--------------------------------------------------------------------------------------------------------------------
        #for i in range(5,6):
        for i in range(0,len_Lot):
            Rate=Rate_array[i]#ここは変える
            while Rate.count("")>0:
                Rate.remove("")
            #len_Rate=len(Rate)
            Lot=Lot_list[i]
            cm2=color_list1[i]
            C_V="Capacity_"+cut_vol+"[mAh]"
    #--------------------------------------------------------------------------------------------------------------------
            for j in range(5,6):
            #for j in range(0,len_Rate)
                rate=float(Rate[j])#レートの選択
                #cm2=color_list2[j]#行のカラー
                df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
                df3=df2[df2["Discharge-rate[C]"]==rate]#
                C_V2=df3[C_V].values#カット電圧時の容量データ
                C_V2=C_V2[0]
                Link=df3["Curve_Data_Link"].values#カーブデータのファイルを開く。
                Link=Link[0]
                DF=pd.read_csv(Link,encoding="cp932")
                x=np.array(DF["DOD[%]"].values.flatten())#x(dod)
                y1=np.array(DF["Voltage[V]"].values.flatten())#y1(vol)
                y2=np.array(DF["dVdQ[V/mAh]"].values.flatten())#y2(dVdQ)
                y3=np.array(DF["delta_V[mV]"].values.flatten())#y3(deltaV)
                y4=np.array(DF["DC_resistance[mohm]"].values.flatten())#y4(DCR)
                if(initial_dod=="DOD"):
                    pass
                elif(initial_dod=="Reference"):
                    if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        C_1C=df3["min_rated_capacity[mAh]"].values
                        x1=C_02[0]
                        x2=C_1C[0]
                        x=x*x1/x2
                    else:#0.2C容量を掛けて、各レートの容量で割る。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        DF3=df2[df2["Discharge-rate[C]"]==float(ref)]#
                        C_V3=DF3[C_V].values#カット電圧時の容量データ
                        C_V3=C_V3[0]
                        x1=C_02[0]
                        x2=C_V3
                        x=x*x1/x2
                else:
                    "正しく選択されていません"

                NAME=Lot+"_"+Rate[j]
                #グラフ左上
                title_size=int(d.get())
                axisN_size=int(e.get())
                axis_size=int(f.get())
                font=g.get()
                plt.subplot(2,2,1)
                plt.title("DOD-voltage",fontsize=title_size,fontname=font)
                plt.plot(x,y1,color=cm2,label=NAME)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(2.95,4.5)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ右上
                plt.subplot(2,2,2)
                plt.title("dVdQ",fontsize=title_size,fontname=font)
                plt.plot(x,y2,color=cm2)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("dV/dQ[V/%]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(0,-0.05)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ左下
                plt.subplot(2,2,3)
                plt.title("delta_V",fontsize=title_size,fontname=font)
                plt.plot(x,y3,color=cm2)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("delta-V[mV]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(-5,505)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ右下
                plt.subplot(2,2,4)
                plt.title("DC-resistance",fontsize=title_size,fontname=font)
                plt.plot(x,y4,color=cm2)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("DC-resistanve[mΩ]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(-5,255)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()

        plt.show()

    def d_V_1():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        while color_list2.count("")>0:
            color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
                    [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
                    [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
                    [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
                    [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
                    [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
    #len_Lot=len(Lot_List)#ロットのリスト長さ

    #--------------------------------------------------------------------------------------------------------------------
        for i in range(0,1):
        #for i in range(0,Lot_list):
            Rate=Rate_array[i]#ここは変える
            while Rate.count("")>0:
                Rate.remove("")
            len_Rate=len(Rate)
            Lot=Lot_list[i]
            #cm1=color_list1[i]
            C_V="Capacity_"+cut_vol+"[mAh]"
    #--------------------------------------------------------------------------------------------------------------------
            for j in range(0,len_Rate):
                rate=float(Rate[j])#レートの選択
                cm2=color_list2[j]#行のカラー
                df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
                df3=df2[df2["Discharge-rate[C]"]==rate]#
                C_V2=df3[C_V].values#カット電圧時の容量データ
                C_V2=C_V2[0]
                Link=df3["Curve_Data_Link"].values#カーブデータのファイルを開く。
                Link=Link[0]
                DF=pd.read_csv(Link,encoding="cp932")
                x=np.array(DF["DOD[%]"].values.flatten())#x(dod)
                y1=np.array(DF["Voltage[V]"].values.flatten())#y1(vol)
                y2=np.array(DF["dVdQ[V/mAh]"].values.flatten())#y2(dVdQ)
                y3=np.array(DF["delta_V[mV]"].values.flatten())#y3(deltaV)
                y4=np.array(DF["DC_resistance[mohm]"].values.flatten())#y4(DCR)
                if(initial_dod=="DOD"):
                    pass
                elif(initial_dod=="Reference"):
                    if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        C_1C=df3["min_rated_capacity[mAh]"].values
                        x1=C_02[0]
                        x2=C_1C[0]
                        x=x*x1/x2
                    else:#0.2C容量を掛けて、各レートの容量で割る。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        DF3=df2[df2["Discharge-rate[C]"]==float(ref)]#
                        C_V3=DF3[C_V].values#カット電圧時の容量データ
                        C_V3=C_V3[0]
                        x1=C_02[0]
                        x2=C_V3
                        x=x*x1/x2
                else:
                    "正しく選択されていません"

                NAME=Lot+"_"+Rate[j]
                #グラフ左上
                title_size=int(d.get())
                axisN_size=int(e.get())
                axis_size=int(f.get())
                font=g.get()
                #plt.subplot(2,2,1)
                plt.title("DOD-voltage",fontsize=title_size,fontname=font)
                plt.plot(x,y1,color=cm2,label=NAME)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(2.95,4.5)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ右上
                #plt.subplot(2,2,2)
                #plt.title("dVdQ",fontsize=title_size,fontname=font)
                #plt.plot(x,y2,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("dV/dQ[V/%]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(0,-0.05)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,-0.01,-0.02,-0.03,-0.04,-0.05],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ左下
                #plt.subplot(2,2,3)
                #plt.title("delta_V",fontsize=title_size,fontname=font)
                #plt.plot(x,y3,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("delta-V[mV]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,505)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250,300,350,400,450,500],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右下
                #plt.subplot(2,2,4)
                #plt.title("DC-resistance",fontsize=title_size,fontname=font)
                #plt.plot(x,y4,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("DC-resistanve[mΩ]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,255)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250],fontsize=axis_size,fontname=font)
                #plt.legend()

        plt.show()
    def d_V_2():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        while color_list2.count("")>0:
            color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
                    [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
                    [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
                    [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
                    [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
                    [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
    #len_Lot=len(Lot_List)#ロットのリスト長さ

    #--------------------------------------------------------------------------------------------------------------------
        for i in range(1,2):
        #for i in range(0,Lot_list):
            Rate=Rate_array[i]#ここは変える
            while Rate.count("")>0:
                Rate.remove("")
            len_Rate=len(Rate)
            Lot=Lot_list[i]
            #cm1=color_list1[i]
            C_V="Capacity_"+cut_vol+"[mAh]"
    #--------------------------------------------------------------------------------------------------------------------
            for j in range(0,len_Rate):
                rate=float(Rate[j])#レートの選択
                cm2=color_list2[j]#行のカラー
                df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
                df3=df2[df2["Discharge-rate[C]"]==rate]#
                C_V2=df3[C_V].values#カット電圧時の容量データ
                C_V2=C_V2[0]
                Link=df3["Curve_Data_Link"].values#カーブデータのファイルを開く。
                Link=Link[0]
                DF=pd.read_csv(Link,encoding="cp932")
                x=np.array(DF["DOD[%]"].values.flatten())#x(dod)
                y1=np.array(DF["Voltage[V]"].values.flatten())#y1(vol)
                y2=np.array(DF["dVdQ[V/mAh]"].values.flatten())#y2(dVdQ)
                y3=np.array(DF["delta_V[mV]"].values.flatten())#y3(deltaV)
                y4=np.array(DF["DC_resistance[mohm]"].values.flatten())#y4(DCR)
                if(initial_dod=="DOD"):
                    pass
                elif(initial_dod=="Reference"):
                    if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        C_1C=df3["min_rated_capacity[mAh]"].values
                        x1=C_02[0]
                        x2=C_1C[0]
                        x=x*x1/x2
                    else:#0.2C容量を掛けて、各レートの容量で割る。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        DF3=df2[df2["Discharge-rate[C]"]==float(ref)]#
                        C_V3=DF3[C_V].values#カット電圧時の容量データ
                        C_V3=C_V3[0]
                        x1=C_02[0]
                        x2=C_V3
                        x=x*x1/x2
                else:
                    "正しく選択されていません"

                NAME=Lot+"_"+Rate[j]
                #グラフ左上
                title_size=int(d.get())
                axisN_size=int(e.get())
                axis_size=int(f.get())
                font=g.get()
                #plt.subplot(2,2,1)
                plt.title("DOD-voltage",fontsize=title_size,fontname=font)
                plt.plot(x,y1,color=cm2,label=NAME)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(2.95,4.5)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ右上
                #plt.subplot(2,2,2)
                #plt.title("dVdQ",fontsize=title_size,fontname=font)
                #plt.plot(x,y2,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("dV/dQ[V/%]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(0,-0.05)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,-0.01,-0.02,-0.03,-0.04,-0.05],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ左下
                #plt.subplot(2,2,3)
                #plt.title("delta_V",fontsize=title_size,fontname=font)
                #plt.plot(x,y3,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("delta-V[mV]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,505)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250,300,350,400,450,500],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右下
                #plt.subplot(2,2,4)
                #plt.title("DC-resistance",fontsize=title_size,fontname=font)
                #plt.plot(x,y4,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("DC-resistanve[mΩ]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,255)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250],fontsize=axis_size,fontname=font)
                #plt.legend()

        plt.show()
    def d_V_3():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        while color_list2.count("")>0:
            color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
                    [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
                    [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
                    [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
                    [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
                    [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
    #len_Lot=len(Lot_List)#ロットのリスト長さ

    #--------------------------------------------------------------------------------------------------------------------
        for i in range(2,3):
        #for i in range(0,Lot_list):
            Rate=Rate_array[i]#ここは変える
            while Rate.count("")>0:
                Rate.remove("")
            len_Rate=len(Rate)
            Lot=Lot_list[i]
            #cm1=color_list1[i]
            C_V="Capacity_"+cut_vol+"[mAh]"
    #--------------------------------------------------------------------------------------------------------------------
            for j in range(0,len_Rate):
                rate=float(Rate[j])#レートの選択
                cm2=color_list2[j]#行のカラー
                df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
                df3=df2[df2["Discharge-rate[C]"]==rate]#
                C_V2=df3[C_V].values#カット電圧時の容量データ
                C_V2=C_V2[0]
                Link=df3["Curve_Data_Link"].values#カーブデータのファイルを開く。
                Link=Link[0]
                DF=pd.read_csv(Link,encoding="cp932")
                x=np.array(DF["DOD[%]"].values.flatten())#x(dod)
                y1=np.array(DF["Voltage[V]"].values.flatten())#y1(vol)
                y2=np.array(DF["dVdQ[V/mAh]"].values.flatten())#y2(dVdQ)
                y3=np.array(DF["delta_V[mV]"].values.flatten())#y3(deltaV)
                y4=np.array(DF["DC_resistance[mohm]"].values.flatten())#y4(DCR)
                if(initial_dod=="DOD"):
                    pass
                elif(initial_dod=="Reference"):
                    if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        C_1C=df3["min_rated_capacity[mAh]"].values
                        x1=C_02[0]
                        x2=C_1C[0]
                        x=x*x1/x2
                    else:#0.2C容量を掛けて、各レートの容量で割る。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        DF3=df2[df2["Discharge-rate[C]"]==float(ref)]#
                        C_V3=DF3[C_V].values#カット電圧時の容量データ
                        C_V3=C_V3[0]
                        x1=C_02[0]
                        x2=C_V3
                        x=x*x1/x2
                else:
                    "正しく選択されていません"

                NAME=Lot+"_"+Rate[j]
                #グラフ左上
                title_size=int(d.get())
                axisN_size=int(e.get())
                axis_size=int(f.get())
                font=g.get()
                #plt.subplot(2,2,1)
                plt.title("DOD-voltage",fontsize=title_size,fontname=font)
                plt.plot(x,y1,color=cm2,label=NAME)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(2.95,4.5)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ右上
                #plt.subplot(2,2,2)
                #plt.title("dVdQ",fontsize=title_size,fontname=font)
                #plt.plot(x,y2,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("dV/dQ[V/%]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(0,-0.05)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,-0.01,-0.02,-0.03,-0.04,-0.05],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ左下
                #plt.subplot(2,2,3)
                #plt.title("delta_V",fontsize=title_size,fontname=font)
                #plt.plot(x,y3,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("delta-V[mV]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,505)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250,300,350,400,450,500],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右下
                #plt.subplot(2,2,4)
                #plt.title("DC-resistance",fontsize=title_size,fontname=font)
                #plt.plot(x,y4,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("DC-resistanve[mΩ]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,255)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250],fontsize=axis_size,fontname=font)
                #plt.legend()

        plt.show()
    def d_V_4():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        while color_list2.count("")>0:
            color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
                    [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
                    [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
                    [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
                    [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
                    [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
    #len_Lot=len(Lot_List)#ロットのリスト長さ

    #--------------------------------------------------------------------------------------------------------------------
        for i in range(3,4):
        #for i in range(0,Lot_list):
            Rate=Rate_array[i]#ここは変える
            while Rate.count("")>0:
                Rate.remove("")
            len_Rate=len(Rate)
            Lot=Lot_list[i]
            #cm1=color_list1[i]
            C_V="Capacity_"+cut_vol+"[mAh]"
    #--------------------------------------------------------------------------------------------------------------------
            for j in range(0,len_Rate):
                rate=float(Rate[j])#レートの選択
                cm2=color_list2[j]#行のカラー
                df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
                df3=df2[df2["Discharge-rate[C]"]==rate]#
                C_V2=df3[C_V].values#カット電圧時の容量データ
                C_V2=C_V2[0]
                Link=df3["Curve_Data_Link"].values#カーブデータのファイルを開く。
                Link=Link[0]
                DF=pd.read_csv(Link,encoding="cp932")
                x=np.array(DF["DOD[%]"].values.flatten())#x(dod)
                y1=np.array(DF["Voltage[V]"].values.flatten())#y1(vol)
                y2=np.array(DF["dVdQ[V/mAh]"].values.flatten())#y2(dVdQ)
                y3=np.array(DF["delta_V[mV]"].values.flatten())#y3(deltaV)
                y4=np.array(DF["DC_resistance[mohm]"].values.flatten())#y4(DCR)
                if(initial_dod=="DOD"):
                    pass
                elif(initial_dod=="Reference"):
                    if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        C_1C=df3["min_rated_capacity[mAh]"].values
                        x1=C_02[0]
                        x2=C_1C[0]
                        x=x*x1/x2
                    else:#0.2C容量を掛けて、各レートの容量で割る。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        DF3=df2[df2["Discharge-rate[C]"]==float(ref)]#
                        C_V3=DF3[C_V].values#カット電圧時の容量データ
                        C_V3=C_V3[0]
                        x1=C_02[0]
                        x2=C_V3
                        x=x*x1/x2
                else:
                    "正しく選択されていません"

                NAME=Lot+"_"+Rate[j]
                #グラフ左上
                title_size=int(d.get())
                axisN_size=int(e.get())
                axis_size=int(f.get())
                font=g.get()
                #plt.subplot(2,2,1)
                plt.title("DOD-voltage",fontsize=title_size,fontname=font)
                plt.plot(x,y1,color=cm2,label=NAME)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(2.95,4.5)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ右上
                #plt.subplot(2,2,2)
                #plt.title("dVdQ",fontsize=title_size,fontname=font)
                #plt.plot(x,y2,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("dV/dQ[V/%]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(0,-0.05)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,-0.01,-0.02,-0.03,-0.04,-0.05],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ左下
                #plt.subplot(2,2,3)
                #plt.title("delta_V",fontsize=title_size,fontname=font)
                #plt.plot(x,y3,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("delta-V[mV]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,505)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250,300,350,400,450,500],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右下
                #plt.subplot(2,2,4)
                #plt.title("DC-resistance",fontsize=title_size,fontname=font)
                #plt.plot(x,y4,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("DC-resistanve[mΩ]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,255)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250],fontsize=axis_size,fontname=font)
                #plt.legend()

        plt.show()
    def d_V_5():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        while color_list2.count("")>0:
            color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
                    [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
                    [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
                    [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
                    [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
                    [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
    #len_Lot=len(Lot_List)#ロットのリスト長さ

    #--------------------------------------------------------------------------------------------------------------------
        for i in range(4,5):
        #for i in range(0,Lot_list):
            Rate=Rate_array[i]#ここは変える
            while Rate.count("")>0:
                Rate.remove("")
            len_Rate=len(Rate)
            Lot=Lot_list[i]
            #cm1=color_list1[i]
            C_V="Capacity_"+cut_vol+"[mAh]"
    #--------------------------------------------------------------------------------------------------------------------
            for j in range(0,len_Rate):
                rate=float(Rate[j])#レートの選択
                cm2=color_list2[j]#行のカラー
                df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
                df3=df2[df2["Discharge-rate[C]"]==rate]#
                C_V2=df3[C_V].values#カット電圧時の容量データ
                C_V2=C_V2[0]
                Link=df3["Curve_Data_Link"].values#カーブデータのファイルを開く。
                Link=Link[0]
                DF=pd.read_csv(Link,encoding="cp932")
                x=np.array(DF["DOD[%]"].values.flatten())#x(dod)
                y1=np.array(DF["Voltage[V]"].values.flatten())#y1(vol)
                y2=np.array(DF["dVdQ[V/mAh]"].values.flatten())#y2(dVdQ)
                y3=np.array(DF["delta_V[mV]"].values.flatten())#y3(deltaV)
                y4=np.array(DF["DC_resistance[mohm]"].values.flatten())#y4(DCR)
                if(initial_dod=="DOD"):
                    pass
                elif(initial_dod=="Reference"):
                    if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        C_1C=df3["min_rated_capacity[mAh]"].values
                        x1=C_02[0]
                        x2=C_1C[0]
                        x=x*x1/x2
                    else:#0.2C容量を掛けて、各レートの容量で割る。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        DF3=df2[df2["Discharge-rate[C]"]==float(ref)]#
                        C_V3=DF3[C_V].values#カット電圧時の容量データ
                        C_V3=C_V3[0]
                        x1=C_02[0]
                        x2=C_V3
                        x=x*x1/x2
                else:
                    "正しく選択されていません"

                NAME=Lot+"_"+Rate[j]
                #グラフ左上
                title_size=int(d.get())
                axisN_size=int(e.get())
                axis_size=int(f.get())
                font=g.get()
                #plt.subplot(2,2,1)
                plt.title("DOD-voltage",fontsize=title_size,fontname=font)
                plt.plot(x,y1,color=cm2,label=NAME)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(2.95,4.5)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ右上
                #plt.subplot(2,2,2)
                #plt.title("dVdQ",fontsize=title_size,fontname=font)
                #plt.plot(x,y2,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("dV/dQ[V/%]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(0,-0.05)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,-0.01,-0.02,-0.03,-0.04,-0.05],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ左下
                #plt.subplot(2,2,3)
                #plt.title("delta_V",fontsize=title_size,fontname=font)
                #plt.plot(x,y3,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("delta-V[mV]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,505)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250,300,350,400,450,500],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右下
                #plt.subplot(2,2,4)
                #plt.title("DC-resistance",fontsize=title_size,fontname=font)
                #plt.plot(x,y4,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("DC-resistanve[mΩ]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,255)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250],fontsize=axis_size,fontname=font)
                #plt.legend()

        plt.show()
    def d_V_6():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        while color_list2.count("")>0:
            color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
                    [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
                    [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
                    [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
                    [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
                    [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
    #len_Lot=len(Lot_List)#ロットのリスト長さ

    #--------------------------------------------------------------------------------------------------------------------
        for i in range(5,6):
        #for i in range(0,Lot_list):
            Rate=Rate_array[i]#ここは変える
            while Rate.count("")>0:
                Rate.remove("")
            len_Rate=len(Rate)
            Lot=Lot_list[i]
            #cm1=color_list1[i]
            C_V="Capacity_"+cut_vol+"[mAh]"
    #--------------------------------------------------------------------------------------------------------------------
            for j in range(0,len_Rate):
                rate=float(Rate[j])#レートの選択
                cm2=color_list2[j]#行のカラー
                df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
                df3=df2[df2["Discharge-rate[C]"]==rate]#
                C_V2=df3[C_V].values#カット電圧時の容量データ
                C_V2=C_V2[0]
                Link=df3["Curve_Data_Link"].values#カーブデータのファイルを開く。
                Link=Link[0]
                DF=pd.read_csv(Link,encoding="cp932")
                x=np.array(DF["DOD[%]"].values.flatten())#x(dod)
                y1=np.array(DF["Voltage[V]"].values.flatten())#y1(vol)
                y2=np.array(DF["dVdQ[V/mAh]"].values.flatten())#y2(dVdQ)
                y3=np.array(DF["delta_V[mV]"].values.flatten())#y3(deltaV)
                y4=np.array(DF["DC_resistance[mohm]"].values.flatten())#y4(DCR)
                if(initial_dod=="DOD"):
                    pass
                elif(initial_dod=="Reference"):
                    if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        C_1C=df3["min_rated_capacity[mAh]"].values
                        x1=C_02[0]
                        x2=C_1C[0]
                        x=x*x1/x2
                    else:#0.2C容量を掛けて、各レートの容量で割る。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        DF3=df2[df2["Discharge-rate[C]"]==float(ref)]#
                        C_V3=DF3[C_V].values#カット電圧時の容量データ
                        C_V3=C_V3[0]
                        x1=C_02[0]
                        x2=C_V3
                        x=x*x1/x2
                else:
                    "正しく選択されていません"

                NAME=Lot+"_"+Rate[j]
                #グラフ左上
                title_size=int(d.get())
                axisN_size=int(e.get())
                axis_size=int(f.get())
                font=g.get()
                #plt.subplot(2,2,1)
                plt.title("DOD-voltage",fontsize=title_size,fontname=font)
                plt.plot(x,y1,color=cm2,label=NAME)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(2.95,4.5)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ右上
                #plt.subplot(2,2,2)
                #plt.title("dVdQ",fontsize=title_size,fontname=font)
                #plt.plot(x,y2,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("dV/dQ[V/%]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(0,-0.05)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,-0.01,-0.02,-0.03,-0.04,-0.05],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ左下
                #plt.subplot(2,2,3)
                #plt.title("delta_V",fontsize=title_size,fontname=font)
                #plt.plot(x,y3,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("delta-V[mV]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,505)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250,300,350,400,450,500],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右下
                #plt.subplot(2,2,4)
                #plt.title("DC-resistance",fontsize=title_size,fontname=font)
                #plt.plot(x,y4,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("DC-resistanve[mΩ]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,255)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250],fontsize=axis_size,fontname=font)
                #plt.legend()

        plt.show()
    def d_V_7():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        while color_list2.count("")>0:
            color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
                    [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
                    [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
                    [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
                    [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
                    [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
        len_Lot=len(Lot_list)#ロットのリスト長さ

    #--------------------------------------------------------------------------------------------------------------------
        #for i in range(5,6):
        for i in range(0,len_Lot):
            Rate=Rate_array[i]#ここは変える
            while Rate.count("")>0:
                Rate.remove("")
            #len_Rate=len(Rate)
            Lot=Lot_list[i]
            cm2=color_list1[i]
            C_V="Capacity_"+cut_vol+"[mAh]"
    #--------------------------------------------------------------------------------------------------------------------
            for j in range(0,1):
            #for j in range(0,len_Rate)
                rate=float(Rate[j])#レートの選択
                #cm2=color_list2[j]#行のカラー
                df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
                df3=df2[df2["Discharge-rate[C]"]==rate]#
                C_V2=df3[C_V].values#カット電圧時の容量データ
                C_V2=C_V2[0]
                Link=df3["Curve_Data_Link"].values#カーブデータのファイルを開く。
                Link=Link[0]
                DF=pd.read_csv(Link,encoding="cp932")
                x=np.array(DF["DOD[%]"].values.flatten())#x(dod)
                y1=np.array(DF["Voltage[V]"].values.flatten())#y1(vol)
                y2=np.array(DF["dVdQ[V/mAh]"].values.flatten())#y2(dVdQ)
                y3=np.array(DF["delta_V[mV]"].values.flatten())#y3(deltaV)
                y4=np.array(DF["DC_resistance[mohm]"].values.flatten())#y4(DCR)
                if(initial_dod=="DOD"):
                    pass
                elif(initial_dod=="Reference"):
                    if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        C_1C=df3["min_rated_capacity[mAh]"].values
                        x1=C_02[0]
                        x2=C_1C[0]
                        x=x*x1/x2
                    else:#0.2C容量を掛けて、各レートの容量で割る。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        DF3=df2[df2["Discharge-rate[C]"]==float(ref)]#
                        C_V3=DF3[C_V].values#カット電圧時の容量データ
                        C_V3=C_V3[0]
                        x1=C_02[0]
                        x2=C_V3
                        x=x*x1/x2
                else:
                    "正しく選択されていません"

                NAME=Lot+"_"+Rate[j]
                #グラフ左上
                title_size=int(d.get())
                axisN_size=int(e.get())
                axis_size=int(f.get())
                font=g.get()
                #plt.subplot(2,2,1)
                plt.title("DOD-voltage",fontsize=title_size,fontname=font)
                plt.plot(x,y1,color=cm2,label=NAME)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(2.95,4.5)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ右上
                #plt.subplot(2,2,2)
                #plt.title("dVdQ",fontsize=title_size,fontname=font)
                #plt.plot(x,y2,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("dV/dQ[V/%]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(0,-0.05)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,-0.01,-0.02,-0.03,-0.04,-0.05],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ左下
                #plt.subplot(2,2,3)
                #plt.title("delta_V",fontsize=title_size,fontname=font)
                #plt.plot(x,y3,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("delta-V[mV]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,505)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250,300,350,400,450,500],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右下
                #plt.subplot(2,2,4)
                #plt.title("DC-resistance",fontsize=title_size,fontname=font)
                #plt.plot(x,y4,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("DC-resistanve[mΩ]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,255)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250],fontsize=axis_size,fontname=font)
                #plt.legend()

        plt.show()
    def d_V_8():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        while color_list2.count("")>0:
            color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
                    [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
                    [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
                    [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
                    [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
                    [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
        len_Lot=len(Lot_list)#ロットのリスト長さ

    #--------------------------------------------------------------------------------------------------------------------
        #for i in range(5,6):
        for i in range(0,len_Lot):
            Rate=Rate_array[i]#ここは変える
            while Rate.count("")>0:
                Rate.remove("")
            #len_Rate=len(Rate)
            Lot=Lot_list[i]
            cm2=color_list1[i]
            C_V="Capacity_"+cut_vol+"[mAh]"
    #--------------------------------------------------------------------------------------------------------------------
            for j in range(1,2):
            #for j in range(0,len_Rate)
                rate=float(Rate[j])#レートの選択
                #cm2=color_list2[j]#行のカラー
                df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
                df3=df2[df2["Discharge-rate[C]"]==rate]#
                C_V2=df3[C_V].values#カット電圧時の容量データ
                C_V2=C_V2[0]
                Link=df3["Curve_Data_Link"].values#カーブデータのファイルを開く。
                Link=Link[0]
                DF=pd.read_csv(Link,encoding="cp932")
                x=np.array(DF["DOD[%]"].values.flatten())#x(dod)
                y1=np.array(DF["Voltage[V]"].values.flatten())#y1(vol)
                y2=np.array(DF["dVdQ[V/mAh]"].values.flatten())#y2(dVdQ)
                y3=np.array(DF["delta_V[mV]"].values.flatten())#y3(deltaV)
                y4=np.array(DF["DC_resistance[mohm]"].values.flatten())#y4(DCR)
                if(initial_dod=="DOD"):
                    pass
                elif(initial_dod=="Reference"):
                    if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        C_1C=df3["min_rated_capacity[mAh]"].values
                        x1=C_02[0]
                        x2=C_1C[0]
                        x=x*x1/x2
                    else:#0.2C容量を掛けて、各レートの容量で割る。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        DF3=df2[df2["Discharge-rate[C]"]==float(ref)]#
                        C_V3=DF3[C_V].values#カット電圧時の容量データ
                        C_V3=C_V3[0]
                        x1=C_02[0]
                        x2=C_V3
                        x=x*x1/x2
                else:
                    "正しく選択されていません"

                NAME=Lot+"_"+Rate[j]
                #グラフ左上
                title_size=int(d.get())
                axisN_size=int(e.get())
                axis_size=int(f.get())
                font=g.get()
                #plt.subplot(2,2,1)
                plt.title("DOD-voltage",fontsize=title_size,fontname=font)
                plt.plot(x,y1,color=cm2,label=NAME)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(2.95,4.5)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ右上
                #plt.subplot(2,2,2)
                #plt.title("dVdQ",fontsize=title_size,fontname=font)
                #plt.plot(x,y2,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("dV/dQ[V/%]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(0,-0.05)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,-0.01,-0.02,-0.03,-0.04,-0.05],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ左下
                #plt.subplot(2,2,3)
                #plt.title("delta_V",fontsize=title_size,fontname=font)
                #plt.plot(x,y3,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("delta-V[mV]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,505)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250,300,350,400,450,500],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右下
                #plt.subplot(2,2,4)
                #plt.title("DC-resistance",fontsize=title_size,fontname=font)
                #plt.plot(x,y4,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("DC-resistanve[mΩ]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,255)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250],fontsize=axis_size,fontname=font)
                #plt.legend()

        plt.show()
    def d_V_9():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        while color_list2.count("")>0:
            color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
                    [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
                    [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
                    [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
                    [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
                    [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
        len_Lot=len(Lot_list)#ロットのリスト長さ

    #--------------------------------------------------------------------------------------------------------------------
        #for i in range(5,6):
        for i in range(0,len_Lot):
            Rate=Rate_array[i]#ここは変える
            while Rate.count("")>0:
                Rate.remove("")
            #len_Rate=len(Rate)
            Lot=Lot_list[i]
            cm2=color_list1[i]
            C_V="Capacity_"+cut_vol+"[mAh]"
    #--------------------------------------------------------------------------------------------------------------------
            for j in range(2,3):
            #for j in range(0,len_Rate)
                rate=float(Rate[j])#レートの選択
                #cm2=color_list2[j]#行のカラー
                df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
                df3=df2[df2["Discharge-rate[C]"]==rate]#
                C_V2=df3[C_V].values#カット電圧時の容量データ
                C_V2=C_V2[0]
                Link=df3["Curve_Data_Link"].values#カーブデータのファイルを開く。
                Link=Link[0]
                DF=pd.read_csv(Link,encoding="cp932")
                x=np.array(DF["DOD[%]"].values.flatten())#x(dod)
                y1=np.array(DF["Voltage[V]"].values.flatten())#y1(vol)
                y2=np.array(DF["dVdQ[V/mAh]"].values.flatten())#y2(dVdQ)
                y3=np.array(DF["delta_V[mV]"].values.flatten())#y3(deltaV)
                y4=np.array(DF["DC_resistance[mohm]"].values.flatten())#y4(DCR)
                if(initial_dod=="DOD"):
                    pass
                elif(initial_dod=="Reference"):
                    if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        C_1C=df3["min_rated_capacity[mAh]"].values
                        x1=C_02[0]
                        x2=C_1C[0]
                        x=x*x1/x2
                    else:#0.2C容量を掛けて、各レートの容量で割る。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        DF3=df2[df2["Discharge-rate[C]"]==float(ref)]#
                        C_V3=DF3[C_V].values#カット電圧時の容量データ
                        C_V3=C_V3[0]
                        x1=C_02[0]
                        x2=C_V3
                        x=x*x1/x2
                else:
                    "正しく選択されていません"

                NAME=Lot+"_"+Rate[j]
                #グラフ左上
                title_size=int(d.get())
                axisN_size=int(e.get())
                axis_size=int(f.get())
                font=g.get()
                #plt.subplot(2,2,1)
                plt.title("DOD-voltage",fontsize=title_size,fontname=font)
                plt.plot(x,y1,color=cm2,label=NAME)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(2.95,4.5)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ右上
                #plt.subplot(2,2,2)
                #plt.title("dVdQ",fontsize=title_size,fontname=font)
                #plt.plot(x,y2,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("dV/dQ[V/%]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(0,-0.05)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,-0.01,-0.02,-0.03,-0.04,-0.05],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ左下
                #plt.subplot(2,2,3)
                #plt.title("delta_V",fontsize=title_size,fontname=font)
                #plt.plot(x,y3,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("delta-V[mV]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,505)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250,300,350,400,450,500],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右下
                #plt.subplot(2,2,4)
                #plt.title("DC-resistance",fontsize=title_size,fontname=font)
                #plt.plot(x,y4,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("DC-resistanve[mΩ]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,255)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250],fontsize=axis_size,fontname=font)
                #plt.legend()

        plt.show()
    def d_V_10():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        while color_list2.count("")>0:
            color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
                    [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
                    [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
                    [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
                    [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
                    [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
        len_Lot=len(Lot_list)#ロットのリスト長さ

    #--------------------------------------------------------------------------------------------------------------------
        #for i in range(5,6):
        for i in range(0,len_Lot):
            Rate=Rate_array[i]#ここは変える
            while Rate.count("")>0:
                Rate.remove("")
            #len_Rate=len(Rate)
            Lot=Lot_list[i]
            cm2=color_list1[i]
            C_V="Capacity_"+cut_vol+"[mAh]"
    #--------------------------------------------------------------------------------------------------------------------
            for j in range(3,4):
            #for j in range(0,len_Rate)
                rate=float(Rate[j])#レートの選択
                #cm2=color_list2[j]#行のカラー
                df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
                df3=df2[df2["Discharge-rate[C]"]==rate]#
                C_V2=df3[C_V].values#カット電圧時の容量データ
                C_V2=C_V2[0]
                Link=df3["Curve_Data_Link"].values#カーブデータのファイルを開く。
                Link=Link[0]
                DF=pd.read_csv(Link,encoding="cp932")
                x=np.array(DF["DOD[%]"].values.flatten())#x(dod)
                y1=np.array(DF["Voltage[V]"].values.flatten())#y1(vol)
                y2=np.array(DF["dVdQ[V/mAh]"].values.flatten())#y2(dVdQ)
                y3=np.array(DF["delta_V[mV]"].values.flatten())#y3(deltaV)
                y4=np.array(DF["DC_resistance[mohm]"].values.flatten())#y4(DCR)
                if(initial_dod=="DOD"):
                    pass
                elif(initial_dod=="Reference"):
                    if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        C_1C=df3["min_rated_capacity[mAh]"].values
                        x1=C_02[0]
                        x2=C_1C[0]
                        x=x*x1/x2
                    else:#0.2C容量を掛けて、各レートの容量で割る。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        DF3=df2[df2["Discharge-rate[C]"]==float(ref)]#
                        C_V3=DF3[C_V].values#カット電圧時の容量データ
                        C_V3=C_V3[0]
                        x1=C_02[0]
                        x2=C_V3
                        x=x*x1/x2
                else:
                    "正しく選択されていません"

                NAME=Lot+"_"+Rate[j]
                #グラフ左上
                title_size=int(d.get())
                axisN_size=int(e.get())
                axis_size=int(f.get())
                font=g.get()
                #plt.subplot(2,2,1)
                plt.title("DOD-voltage",fontsize=title_size,fontname=font)
                plt.plot(x,y1,color=cm2,label=NAME)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(2.95,4.5)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ右上
                #plt.subplot(2,2,2)
                #plt.title("dVdQ",fontsize=title_size,fontname=font)
                #plt.plot(x,y2,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("dV/dQ[V/%]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(0,-0.05)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,-0.01,-0.02,-0.03,-0.04,-0.05],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ左下
                #plt.subplot(2,2,3)
                #plt.title("delta_V",fontsize=title_size,fontname=font)
                #plt.plot(x,y3,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("delta-V[mV]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,505)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250,300,350,400,450,500],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右下
                #plt.subplot(2,2,4)
                #plt.title("DC-resistance",fontsize=title_size,fontname=font)
                #plt.plot(x,y4,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("DC-resistanve[mΩ]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,255)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250],fontsize=axis_size,fontname=font)
                #plt.legend()

        plt.show()
    def d_V_11():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        while color_list2.count("")>0:
            color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
                    [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
                    [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
                    [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
                    [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
                    [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
        len_Lot=len(Lot_list)#ロットのリスト長さ

    #--------------------------------------------------------------------------------------------------------------------
        #for i in range(5,6):
        for i in range(0,len_Lot):
            Rate=Rate_array[i]#ここは変える
            while Rate.count("")>0:
                Rate.remove("")
            #len_Rate=len(Rate)
            Lot=Lot_list[i]
            cm2=color_list1[i]
            C_V="Capacity_"+cut_vol+"[mAh]"
    #--------------------------------------------------------------------------------------------------------------------
            for j in range(4,5):
            #for j in range(0,len_Rate)
                rate=float(Rate[j])#レートの選択
                #cm2=color_list2[j]#行のカラー
                df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
                df3=df2[df2["Discharge-rate[C]"]==rate]#
                C_V2=df3[C_V].values#カット電圧時の容量データ
                C_V2=C_V2[0]
                Link=df3["Curve_Data_Link"].values#カーブデータのファイルを開く。
                Link=Link[0]
                DF=pd.read_csv(Link,encoding="cp932")
                x=np.array(DF["DOD[%]"].values.flatten())#x(dod)
                y1=np.array(DF["Voltage[V]"].values.flatten())#y1(vol)
                y2=np.array(DF["dVdQ[V/mAh]"].values.flatten())#y2(dVdQ)
                y3=np.array(DF["delta_V[mV]"].values.flatten())#y3(deltaV)
                y4=np.array(DF["DC_resistance[mohm]"].values.flatten())#y4(DCR)
                if(initial_dod=="DOD"):
                    pass
                elif(initial_dod=="Reference"):
                    if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        C_1C=df3["min_rated_capacity[mAh]"].values
                        x1=C_02[0]
                        x2=C_1C[0]
                        x=x*x1/x2
                    else:#0.2C容量を掛けて、各レートの容量で割る。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        DF3=df2[df2["Discharge-rate[C]"]==float(ref)]#
                        C_V3=DF3[C_V].values#カット電圧時の容量データ
                        C_V3=C_V3[0]
                        x1=C_02[0]
                        x2=C_V3
                        x=x*x1/x2
                else:
                    "正しく選択されていません"

                NAME=Lot+"_"+Rate[j]
                #グラフ左上
                title_size=int(d.get())
                axisN_size=int(e.get())
                axis_size=int(f.get())
                font=g.get()
                #plt.subplot(2,2,1)
                plt.title("DOD-voltage",fontsize=title_size,fontname=font)
                plt.plot(x,y1,color=cm2,label=NAME)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(2.95,4.5)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ右上
                #plt.subplot(2,2,2)
                #plt.title("dVdQ",fontsize=title_size,fontname=font)
                #plt.plot(x,y2,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("dV/dQ[V/%]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(0,-0.05)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,-0.01,-0.02,-0.03,-0.04,-0.05],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ左下
                #plt.subplot(2,2,3)
                #plt.title("delta_V",fontsize=title_size,fontname=font)
                #plt.plot(x,y3,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("delta-V[mV]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,505)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250,300,350,400,450,500],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右下
                #plt.subplot(2,2,4)
                #plt.title("DC-resistance",fontsize=title_size,fontname=font)
                #plt.plot(x,y4,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("DC-resistanve[mΩ]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,255)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250],fontsize=axis_size,fontname=font)
                #plt.legend()

        plt.show()
    def d_V_12():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        while color_list2.count("")>0:
            color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
                    [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
                    [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
                    [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
                    [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
                    [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
        len_Lot=len(Lot_list)#ロットのリスト長さ

    #--------------------------------------------------------------------------------------------------------------------
        #for i in range(5,6):
        for i in range(0,len_Lot):
            Rate=Rate_array[i]#ここは変える
            while Rate.count("")>0:
                Rate.remove("")
            #len_Rate=len(Rate)
            Lot=Lot_list[i]
            cm2=color_list1[i]
            C_V="Capacity_"+cut_vol+"[mAh]"
    #--------------------------------------------------------------------------------------------------------------------
            for j in range(5,6):
            #for j in range(0,len_Rate)
                rate=float(Rate[j])#レートの選択
                #cm2=color_list2[j]#行のカラー
                df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
                df3=df2[df2["Discharge-rate[C]"]==rate]#
                C_V2=df3[C_V].values#カット電圧時の容量データ
                C_V2=C_V2[0]
                Link=df3["Curve_Data_Link"].values#カーブデータのファイルを開く。
                Link=Link[0]
                DF=pd.read_csv(Link,encoding="cp932")
                x=np.array(DF["DOD[%]"].values.flatten())#x(dod)
                y1=np.array(DF["Voltage[V]"].values.flatten())#y1(vol)
                y2=np.array(DF["dVdQ[V/mAh]"].values.flatten())#y2(dVdQ)
                y3=np.array(DF["delta_V[mV]"].values.flatten())#y3(deltaV)
                y4=np.array(DF["DC_resistance[mohm]"].values.flatten())#y4(DCR)
                if(initial_dod=="DOD"):
                    pass
                elif(initial_dod=="Reference"):
                    if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        C_1C=df3["min_rated_capacity[mAh]"].values
                        x1=C_02[0]
                        x2=C_1C[0]
                        x=x*x1/x2
                    else:#0.2C容量を掛けて、各レートの容量で割る。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        DF3=df2[df2["Discharge-rate[C]"]==float(ref)]#
                        C_V3=DF3[C_V].values#カット電圧時の容量データ
                        C_V3=C_V3[0]
                        x1=C_02[0]
                        x2=C_V3
                        x=x*x1/x2
                else:
                    "正しく選択されていません"

                NAME=Lot+"_"+Rate[j]
                #グラフ左上
                title_size=int(d.get())
                axisN_size=int(e.get())
                axis_size=int(f.get())
                font=g.get()
                #plt.subplot(2,2,1)
                plt.title("DOD-voltage",fontsize=title_size,fontname=font)
                plt.plot(x,y1,color=cm2,label=NAME)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(2.95,4.5)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ右上
                #plt.subplot(2,2,2)
                #plt.title("dVdQ",fontsize=title_size,fontname=font)
                #plt.plot(x,y2,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("dV/dQ[V/%]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(0,-0.05)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,-0.01,-0.02,-0.03,-0.04,-0.05],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ左下
                #plt.subplot(2,2,3)
                #plt.title("delta_V",fontsize=title_size,fontname=font)
                #plt.plot(x,y3,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("delta-V[mV]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,505)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250,300,350,400,450,500],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右下
                #plt.subplot(2,2,4)
                #plt.title("DC-resistance",fontsize=title_size,fontname=font)
                #plt.plot(x,y4,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("DC-resistanve[mΩ]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,255)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250],fontsize=axis_size,fontname=font)
                #plt.legend()

        plt.show()

    def dvdq1():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        while color_list2.count("")>0:
            color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
                    [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
                    [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
                    [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
                    [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
                    [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
    #len_Lot=len(Lot_List)#ロットのリスト長さ

    #--------------------------------------------------------------------------------------------------------------------
        for i in range(0,1):
        #for i in range(0,Lot_list):
            Rate=Rate_array[i]#ここは変える
            while Rate.count("")>0:
                Rate.remove("")
            len_Rate=len(Rate)
            Lot=Lot_list[i]
            #cm1=color_list1[i]
            C_V="Capacity_"+cut_vol+"[mAh]"
    #--------------------------------------------------------------------------------------------------------------------
            for j in range(0,len_Rate):
                rate=float(Rate[j])#レートの選択
                cm2=color_list2[j]#行のカラー
                df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
                df3=df2[df2["Discharge-rate[C]"]==rate]#
                C_V2=df3[C_V].values#カット電圧時の容量データ
                C_V2=C_V2[0]
                Link=df3["Curve_Data_Link"].values#カーブデータのファイルを開く。
                Link=Link[0]
                DF=pd.read_csv(Link,encoding="cp932")
                x=np.array(DF["DOD[%]"].values.flatten())#x(dod)
                y1=np.array(DF["Voltage[V]"].values.flatten())#y1(vol)
                y2=np.array(DF["dVdQ[V/mAh]"].values.flatten())#y2(dVdQ)
                y3=np.array(DF["delta_V[mV]"].values.flatten())#y3(deltaV)
                y4=np.array(DF["DC_resistance[mohm]"].values.flatten())#y4(DCR)
                if(initial_dod=="DOD"):
                    pass
                elif(initial_dod=="Reference"):
                    if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        C_1C=df3["min_rated_capacity[mAh]"].values
                        x1=C_02[0]
                        x2=C_1C[0]
                        x=x*x1/x2
                    else:#0.2C容量を掛けて、各レートの容量で割る。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        DF3=df2[df2["Discharge-rate[C]"]==float(ref)]#
                        C_V3=DF3[C_V].values#カット電圧時の容量データ
                        C_V3=C_V3[0]
                        x1=C_02[0]
                        x2=C_V3
                        x=x*x1/x2
                else:
                    "正しく選択されていません"

                NAME=Lot+"_"+Rate[j]
                #グラフ左上
                title_size=int(d.get())
                axisN_size=int(e.get())
                axis_size=int(f.get())
                font=g.get()
                #plt.subplot(2,2,1)
                #plt.title("DOD-voltage",fontsize=title_size,fontname=font)
                #plt.plot(x,y1,color=cm2,label=NAME)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(2.95,4.5)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([3,3.2,3.4,3.6,3.8,4.0,4.2,4.4,4.5],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右上
                #plt.subplot(2,2,2)
                plt.title("dVdQ",fontsize=title_size,fontname=font)
                plt.plot(x,y2,color=cm2,label=NAME)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("dV/dQ[V/%]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(0,-0.05)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ左下
                #plt.subplot(2,2,3)
                #plt.title("delta_V",fontsize=title_size,fontname=font)
                #plt.plot(x,y3,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("delta-V[mV]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,505)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250,300,350,400,450,500],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右下
                #plt.subplot(2,2,4)
                #plt.title("DC-resistance",fontsize=title_size,fontname=font)
                #plt.plot(x,y4,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("DC-resistanve[mΩ]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,255)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250],fontsize=axis_size,fontname=font)
                #plt.legend()

        plt.show()
    def dvdq2():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        while color_list2.count("")>0:
            color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
                    [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
                    [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
                    [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
                    [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
                    [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
    #len_Lot=len(Lot_List)#ロットのリスト長さ

    #--------------------------------------------------------------------------------------------------------------------
        for i in range(1,2):
        #for i in range(0,Lot_list):
            Rate=Rate_array[i]#ここは変える
            while Rate.count("")>0:
                Rate.remove("")
            len_Rate=len(Rate)
            Lot=Lot_list[i]
            #cm1=color_list1[i]
            C_V="Capacity_"+cut_vol+"[mAh]"
    #--------------------------------------------------------------------------------------------------------------------
            for j in range(0,len_Rate):
                rate=float(Rate[j])#レートの選択
                cm2=color_list2[j]#行のカラー
                df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
                df3=df2[df2["Discharge-rate[C]"]==rate]#
                C_V2=df3[C_V].values#カット電圧時の容量データ
                C_V2=C_V2[0]
                Link=df3["Curve_Data_Link"].values#カーブデータのファイルを開く。
                Link=Link[0]
                DF=pd.read_csv(Link,encoding="cp932")
                x=np.array(DF["DOD[%]"].values.flatten())#x(dod)
                y1=np.array(DF["Voltage[V]"].values.flatten())#y1(vol)
                y2=np.array(DF["dVdQ[V/mAh]"].values.flatten())#y2(dVdQ)
                y3=np.array(DF["delta_V[mV]"].values.flatten())#y3(deltaV)
                y4=np.array(DF["DC_resistance[mohm]"].values.flatten())#y4(DCR)
                if(initial_dod=="DOD"):
                    pass
                elif(initial_dod=="Reference"):
                    if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        C_1C=df3["min_rated_capacity[mAh]"].values
                        x1=C_02[0]
                        x2=C_1C[0]
                        x=x*x1/x2
                    else:#0.2C容量を掛けて、各レートの容量で割る。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        DF3=df2[df2["Discharge-rate[C]"]==float(ref)]#
                        C_V3=DF3[C_V].values#カット電圧時の容量データ
                        C_V3=C_V3[0]
                        x1=C_02[0]
                        x2=C_V3
                        x=x*x1/x2
                else:
                    "正しく選択されていません"

                NAME=Lot+"_"+Rate[j]
                #グラフ左上
                title_size=int(d.get())
                axisN_size=int(e.get())
                axis_size=int(f.get())
                font=g.get()
                #plt.subplot(2,2,1)
                #plt.title("DOD-voltage",fontsize=title_size,fontname=font)
                #plt.plot(x,y1,color=cm2,label=NAME)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(2.95,4.5)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([3,3.2,3.4,3.6,3.8,4.0,4.2,4.4,4.5],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右上
                #plt.subplot(2,2,2)
                plt.title("dVdQ",fontsize=title_size,fontname=font)
                plt.plot(x,y2,color=cm2,label=NAME)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("dV/dQ[V/%]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(0,-0.05)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ左下
                #plt.subplot(2,2,3)
                #plt.title("delta_V",fontsize=title_size,fontname=font)
                #plt.plot(x,y3,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("delta-V[mV]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,505)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250,300,350,400,450,500],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右下
                #plt.subplot(2,2,4)
                #plt.title("DC-resistance",fontsize=title_size,fontname=font)
                #plt.plot(x,y4,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("DC-resistanve[mΩ]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,255)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250],fontsize=axis_size,fontname=font)
                #plt.legend()

        plt.show()
    def dvdq3():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        while color_list2.count("")>0:
            color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
                    [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
                    [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
                    [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
                    [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
                    [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
    #len_Lot=len(Lot_List)#ロットのリスト長さ

    #--------------------------------------------------------------------------------------------------------------------
        for i in range(2,3):
        #for i in range(0,Lot_list):
            Rate=Rate_array[i]#ここは変える
            while Rate.count("")>0:
                Rate.remove("")
            len_Rate=len(Rate)
            Lot=Lot_list[i]
            #cm1=color_list1[i]
            C_V="Capacity_"+cut_vol+"[mAh]"
    #--------------------------------------------------------------------------------------------------------------------
            for j in range(0,len_Rate):
                rate=float(Rate[j])#レートの選択
                cm2=color_list2[j]#行のカラー
                df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
                df3=df2[df2["Discharge-rate[C]"]==rate]#
                C_V2=df3[C_V].values#カット電圧時の容量データ
                C_V2=C_V2[0]
                Link=df3["Curve_Data_Link"].values#カーブデータのファイルを開く。
                Link=Link[0]
                DF=pd.read_csv(Link,encoding="cp932")
                x=np.array(DF["DOD[%]"].values.flatten())#x(dod)
                y1=np.array(DF["Voltage[V]"].values.flatten())#y1(vol)
                y2=np.array(DF["dVdQ[V/mAh]"].values.flatten())#y2(dVdQ)
                y3=np.array(DF["delta_V[mV]"].values.flatten())#y3(deltaV)
                y4=np.array(DF["DC_resistance[mohm]"].values.flatten())#y4(DCR)
                if(initial_dod=="DOD"):
                    pass
                elif(initial_dod=="Reference"):
                    if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        C_1C=df3["min_rated_capacity[mAh]"].values
                        x1=C_02[0]
                        x2=C_1C[0]
                        x=x*x1/x2
                    else:#0.2C容量を掛けて、各レートの容量で割る。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        DF3=df2[df2["Discharge-rate[C]"]==float(ref)]#
                        C_V3=DF3[C_V].values#カット電圧時の容量データ
                        C_V3=C_V3[0]
                        x1=C_02[0]
                        x2=C_V3
                        x=x*x1/x2
                else:
                    "正しく選択されていません"

                NAME=Lot+"_"+Rate[j]
                #グラフ左上
                title_size=int(d.get())
                axisN_size=int(e.get())
                axis_size=int(f.get())
                font=g.get()
                #plt.subplot(2,2,1)
                #plt.title("DOD-voltage",fontsize=title_size,fontname=font)
                #plt.plot(x,y1,color=cm2,label=NAME)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(2.95,4.5)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([3,3.2,3.4,3.6,3.8,4.0,4.2,4.4,4.5],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右上
                #plt.subplot(2,2,2)
                plt.title("dVdQ",fontsize=title_size,fontname=font)
                plt.plot(x,y2,color=cm2,label=NAME)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("dV/dQ[V/%]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(0,-0.05)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ左下
                #plt.subplot(2,2,3)
                #plt.title("delta_V",fontsize=title_size,fontname=font)
                #plt.plot(x,y3,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("delta-V[mV]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,505)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250,300,350,400,450,500],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右下
                #plt.subplot(2,2,4)
                #plt.title("DC-resistance",fontsize=title_size,fontname=font)
                #plt.plot(x,y4,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("DC-resistanve[mΩ]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,255)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250],fontsize=axis_size,fontname=font)
                #plt.legend()

        plt.show()
    def dvdq4():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        while color_list2.count("")>0:
            color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
                    [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
                    [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
                    [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
                    [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
                    [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
    #len_Lot=len(Lot_List)#ロットのリスト長さ

    #--------------------------------------------------------------------------------------------------------------------
        for i in range(3,4):
        #for i in range(0,Lot_list):
            Rate=Rate_array[i]#ここは変える
            while Rate.count("")>0:
                Rate.remove("")
            len_Rate=len(Rate)
            Lot=Lot_list[i]
            #cm1=color_list1[i]
            C_V="Capacity_"+cut_vol+"[mAh]"
    #--------------------------------------------------------------------------------------------------------------------
            for j in range(0,len_Rate):
                rate=float(Rate[j])#レートの選択
                cm2=color_list2[j]#行のカラー
                df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
                df3=df2[df2["Discharge-rate[C]"]==rate]#
                C_V2=df3[C_V].values#カット電圧時の容量データ
                C_V2=C_V2[0]
                Link=df3["Curve_Data_Link"].values#カーブデータのファイルを開く。
                Link=Link[0]
                DF=pd.read_csv(Link,encoding="cp932")
                x=np.array(DF["DOD[%]"].values.flatten())#x(dod)
                y1=np.array(DF["Voltage[V]"].values.flatten())#y1(vol)
                y2=np.array(DF["dVdQ[V/mAh]"].values.flatten())#y2(dVdQ)
                y3=np.array(DF["delta_V[mV]"].values.flatten())#y3(deltaV)
                y4=np.array(DF["DC_resistance[mohm]"].values.flatten())#y4(DCR)
                if(initial_dod=="DOD"):
                    pass
                elif(initial_dod=="Reference"):
                    if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        C_1C=df3["min_rated_capacity[mAh]"].values
                        x1=C_02[0]
                        x2=C_1C[0]
                        x=x*x1/x2
                    else:#0.2C容量を掛けて、各レートの容量で割る。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        DF3=df2[df2["Discharge-rate[C]"]==float(ref)]#
                        C_V3=DF3[C_V].values#カット電圧時の容量データ
                        C_V3=C_V3[0]
                        x1=C_02[0]
                        x2=C_V3
                        x=x*x1/x2
                else:
                    "正しく選択されていません"

                NAME=Lot+"_"+Rate[j]
                #グラフ左上
                title_size=int(d.get())
                axisN_size=int(e.get())
                axis_size=int(f.get())
                font=g.get()
                #plt.subplot(2,2,1)
                #plt.title("DOD-voltage",fontsize=title_size,fontname=font)
                #plt.plot(x,y1,color=cm2,label=NAME)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(2.95,4.5)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([3,3.2,3.4,3.6,3.8,4.0,4.2,4.4,4.5],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右上
                #plt.subplot(2,2,2)
                plt.title("dVdQ",fontsize=title_size,fontname=font)
                plt.plot(x,y2,color=cm2,label=NAME)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("dV/dQ[V/%]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(0,-0.05)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ左下
                #plt.subplot(2,2,3)
                #plt.title("delta_V",fontsize=title_size,fontname=font)
                #plt.plot(x,y3,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("delta-V[mV]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,505)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250,300,350,400,450,500],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右下
                #plt.subplot(2,2,4)
                #plt.title("DC-resistance",fontsize=title_size,fontname=font)
                #plt.plot(x,y4,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("DC-resistanve[mΩ]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,255)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250],fontsize=axis_size,fontname=font)
                #plt.legend()

        plt.show()
    def dvdq5():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        while color_list2.count("")>0:
            color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
                    [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
                    [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
                    [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
                    [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
                    [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
    #len_Lot=len(Lot_List)#ロットのリスト長さ

    #--------------------------------------------------------------------------------------------------------------------
        for i in range(4,5):
        #for i in range(0,Lot_list):
            Rate=Rate_array[i]#ここは変える
            while Rate.count("")>0:
                Rate.remove("")
            len_Rate=len(Rate)
            Lot=Lot_list[i]
            #cm1=color_list1[i]
            C_V="Capacity_"+cut_vol+"[mAh]"
    #--------------------------------------------------------------------------------------------------------------------
            for j in range(0,len_Rate):
                rate=float(Rate[j])#レートの選択
                cm2=color_list2[j]#行のカラー
                df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
                df3=df2[df2["Discharge-rate[C]"]==rate]#
                C_V2=df3[C_V].values#カット電圧時の容量データ
                C_V2=C_V2[0]
                Link=df3["Curve_Data_Link"].values#カーブデータのファイルを開く。
                Link=Link[0]
                DF=pd.read_csv(Link,encoding="cp932")
                x=np.array(DF["DOD[%]"].values.flatten())#x(dod)
                y1=np.array(DF["Voltage[V]"].values.flatten())#y1(vol)
                y2=np.array(DF["dVdQ[V/mAh]"].values.flatten())#y2(dVdQ)
                y3=np.array(DF["delta_V[mV]"].values.flatten())#y3(deltaV)
                y4=np.array(DF["DC_resistance[mohm]"].values.flatten())#y4(DCR)
                if(initial_dod=="DOD"):
                    pass
                elif(initial_dod=="Reference"):
                    if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        C_1C=df3["min_rated_capacity[mAh]"].values
                        x1=C_02[0]
                        x2=C_1C[0]
                        x=x*x1/x2
                    else:#0.2C容量を掛けて、各レートの容量で割る。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        DF3=df2[df2["Discharge-rate[C]"]==float(ref)]#
                        C_V3=DF3[C_V].values#カット電圧時の容量データ
                        C_V3=C_V3[0]
                        x1=C_02[0]
                        x2=C_V3
                        x=x*x1/x2
                else:
                    "正しく選択されていません"

                NAME=Lot+"_"+Rate[j]
                #グラフ左上
                title_size=int(d.get())
                axisN_size=int(e.get())
                axis_size=int(f.get())
                font=g.get()
                #plt.subplot(2,2,1)
                #plt.title("DOD-voltage",fontsize=title_size,fontname=font)
                #plt.plot(x,y1,color=cm2,label=NAME)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(2.95,4.5)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([3,3.2,3.4,3.6,3.8,4.0,4.2,4.4,4.5],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右上
                #plt.subplot(2,2,2)
                plt.title("dVdQ",fontsize=title_size,fontname=font)
                plt.plot(x,y2,color=cm2,label=NAME)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("dV/dQ[V/%]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(0,-0.05)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ左下
                #plt.subplot(2,2,3)
                #plt.title("delta_V",fontsize=title_size,fontname=font)
                #plt.plot(x,y3,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("delta-V[mV]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,505)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250,300,350,400,450,500],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右下
                #plt.subplot(2,2,4)
                #plt.title("DC-resistance",fontsize=title_size,fontname=font)
                #plt.plot(x,y4,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("DC-resistanve[mΩ]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,255)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250],fontsize=axis_size,fontname=font)
                #plt.legend()

        plt.show()
    def dvdq6():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        while color_list2.count("")>0:
            color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
                    [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
                    [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
                    [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
                    [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
                    [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
    #len_Lot=len(Lot_List)#ロットのリスト長さ

    #--------------------------------------------------------------------------------------------------------------------
        for i in range(5,6):
        #for i in range(0,Lot_list):
            Rate=Rate_array[i]#ここは変える
            while Rate.count("")>0:
                Rate.remove("")
            len_Rate=len(Rate)
            Lot=Lot_list[i]
            #cm1=color_list1[i]
            C_V="Capacity_"+cut_vol+"[mAh]"
    #--------------------------------------------------------------------------------------------------------------------
            for j in range(0,len_Rate):
                rate=float(Rate[j])#レートの選択
                cm2=color_list2[j]#行のカラー
                df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
                df3=df2[df2["Discharge-rate[C]"]==rate]#
                C_V2=df3[C_V].values#カット電圧時の容量データ
                C_V2=C_V2[0]
                Link=df3["Curve_Data_Link"].values#カーブデータのファイルを開く。
                Link=Link[0]
                DF=pd.read_csv(Link,encoding="cp932")
                x=np.array(DF["DOD[%]"].values.flatten())#x(dod)
                y1=np.array(DF["Voltage[V]"].values.flatten())#y1(vol)
                y2=np.array(DF["dVdQ[V/mAh]"].values.flatten())#y2(dVdQ)
                y3=np.array(DF["delta_V[mV]"].values.flatten())#y3(deltaV)
                y4=np.array(DF["DC_resistance[mohm]"].values.flatten())#y4(DCR)
                if(initial_dod=="DOD"):
                    pass
                elif(initial_dod=="Reference"):
                    if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        C_1C=df3["min_rated_capacity[mAh]"].values
                        x1=C_02[0]
                        x2=C_1C[0]
                        x=x*x1/x2
                    else:#0.2C容量を掛けて、各レートの容量で割る。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        DF3=df2[df2["Discharge-rate[C]"]==float(ref)]#
                        C_V3=DF3[C_V].values#カット電圧時の容量データ
                        C_V3=C_V3[0]
                        x1=C_02[0]
                        x2=C_V3
                        x=x*x1/x2
                else:
                    "正しく選択されていません"

                NAME=Lot+"_"+Rate[j]
                #グラフ左上
                title_size=int(d.get())
                axisN_size=int(e.get())
                axis_size=int(f.get())
                font=g.get()
                #plt.subplot(2,2,1)
                #plt.title("DOD-voltage",fontsize=title_size,fontname=font)
                #plt.plot(x,y1,color=cm2,label=NAME)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(2.95,4.5)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([3,3.2,3.4,3.6,3.8,4.0,4.2,4.4,4.5],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右上
                #plt.subplot(2,2,2)
                plt.title("dVdQ",fontsize=title_size,fontname=font)
                plt.plot(x,y2,color=cm2,label=NAME)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("dV/dQ[V/%]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(0,-0.05)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ左下
                #plt.subplot(2,2,3)
                #plt.title("delta_V",fontsize=title_size,fontname=font)
                #plt.plot(x,y3,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("delta-V[mV]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,505)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250,300,350,400,450,500],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右下
                #plt.subplot(2,2,4)
                #plt.title("DC-resistance",fontsize=title_size,fontname=font)
                #plt.plot(x,y4,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("DC-resistanve[mΩ]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,255)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250],fontsize=axis_size,fontname=font)
                #plt.legend()

        plt.show()
    def dvdq7():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        while color_list2.count("")>0:
            color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
                    [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
                    [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
                    [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
                    [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
                    [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
        len_Lot=len(Lot_list)#ロットのリスト長さ

    #--------------------------------------------------------------------------------------------------------------------
        #for i in range(5,6):
        for i in range(0,len_Lot):
            Rate=Rate_array[i]#ここは変える
            while Rate.count("")>0:
                Rate.remove("")
            #len_Rate=len(Rate)
            Lot=Lot_list[i]
            cm2=color_list1[i]
            C_V="Capacity_"+cut_vol+"[mAh]"
    #--------------------------------------------------------------------------------------------------------------------
            for j in range(0,1):
            #for j in range(0,len_Rate)
                rate=float(Rate[j])#レートの選択
                #cm2=color_list2[j]#行のカラー
                df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
                df3=df2[df2["Discharge-rate[C]"]==rate]#
                C_V2=df3[C_V].values#カット電圧時の容量データ
                C_V2=C_V2[0]
                Link=df3["Curve_Data_Link"].values#カーブデータのファイルを開く。
                Link=Link[0]
                DF=pd.read_csv(Link,encoding="cp932")
                x=np.array(DF["DOD[%]"].values.flatten())#x(dod)
                y1=np.array(DF["Voltage[V]"].values.flatten())#y1(vol)
                y2=np.array(DF["dVdQ[V/mAh]"].values.flatten())#y2(dVdQ)
                y3=np.array(DF["delta_V[mV]"].values.flatten())#y3(deltaV)
                y4=np.array(DF["DC_resistance[mohm]"].values.flatten())#y4(DCR)
                if(initial_dod=="DOD"):
                    pass
                elif(initial_dod=="Reference"):
                    if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        C_1C=df3["min_rated_capacity[mAh]"].values
                        x1=C_02[0]
                        x2=C_1C[0]
                        x=x*x1/x2
                    else:#0.2C容量を掛けて、各レートの容量で割る。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        DF3=df2[df2["Discharge-rate[C]"]==float(ref)]#
                        C_V3=DF3[C_V].values#カット電圧時の容量データ
                        C_V3=C_V3[0]
                        x1=C_02[0]
                        x2=C_V3
                        x=x*x1/x2
                else:
                    "正しく選択されていません"

                NAME=Lot+"_"+Rate[j]
                #グラフ左上
                title_size=int(d.get())
                axisN_size=int(e.get())
                axis_size=int(f.get())
                font=g.get()
                #plt.subplot(2,2,1)
                #plt.title("DOD-voltage",fontsize=title_size,fontname=font)
                #plt.plot(x,y1,color=cm2,label=NAME)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(2.95,4.5)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([3,3.2,3.4,3.6,3.8,4.0,4.2,4.4,4.5],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右上
                #plt.subplot(2,2,2)
                plt.title("dVdQ",fontsize=title_size,fontname=font)
                plt.plot(x,y2,color=cm2,label=NAME)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("dV/dQ[V/%]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(0,-0.05)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ左下
                #plt.subplot(2,2,3)
                #plt.title("delta_V",fontsize=title_size,fontname=font)
                #plt.plot(x,y3,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("delta-V[mV]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,505)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250,300,350,400,450,500],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右下
                #plt.subplot(2,2,4)
                #plt.title("DC-resistance",fontsize=title_size,fontname=font)
                #plt.plot(x,y4,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("DC-resistanve[mΩ]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,255)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250],fontsize=axis_size,fontname=font)
                #plt.legend()

        plt.show()
    def dvdq8():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        while color_list2.count("")>0:
            color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
                    [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
                    [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
                    [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
                    [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
                    [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
        len_Lot=len(Lot_list)#ロットのリスト長さ

    #--------------------------------------------------------------------------------------------------------------------
        #for i in range(5,6):
        for i in range(0,len_Lot):
            Rate=Rate_array[i]#ここは変える
            while Rate.count("")>0:
                Rate.remove("")
            #len_Rate=len(Rate)
            Lot=Lot_list[i]
            cm2=color_list1[i]
            C_V="Capacity_"+cut_vol+"[mAh]"
    #--------------------------------------------------------------------------------------------------------------------
            for j in range(1,2):
            #for j in range(0,len_Rate)
                rate=float(Rate[j])#レートの選択
                #cm2=color_list2[j]#行のカラー
                df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
                df3=df2[df2["Discharge-rate[C]"]==rate]#
                C_V2=df3[C_V].values#カット電圧時の容量データ
                C_V2=C_V2[0]
                Link=df3["Curve_Data_Link"].values#カーブデータのファイルを開く。
                Link=Link[0]
                DF=pd.read_csv(Link,encoding="cp932")
                x=np.array(DF["DOD[%]"].values.flatten())#x(dod)
                y1=np.array(DF["Voltage[V]"].values.flatten())#y1(vol)
                y2=np.array(DF["dVdQ[V/mAh]"].values.flatten())#y2(dVdQ)
                y3=np.array(DF["delta_V[mV]"].values.flatten())#y3(deltaV)
                y4=np.array(DF["DC_resistance[mohm]"].values.flatten())#y4(DCR)
                if(initial_dod=="DOD"):
                    pass
                elif(initial_dod=="Reference"):
                    if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        C_1C=df3["min_rated_capacity[mAh]"].values
                        x1=C_02[0]
                        x2=C_1C[0]
                        x=x*x1/x2
                    else:#0.2C容量を掛けて、各レートの容量で割る。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        DF3=df2[df2["Discharge-rate[C]"]==float(ref)]#
                        C_V3=DF3[C_V].values#カット電圧時の容量データ
                        C_V3=C_V3[0]
                        x1=C_02[0]
                        x2=C_V3
                        x=x*x1/x2
                else:
                    "正しく選択されていません"

                NAME=Lot+"_"+Rate[j]
                #グラフ左上
                title_size=int(d.get())
                axisN_size=int(e.get())
                axis_size=int(f.get())
                font=g.get()
                #plt.subplot(2,2,1)
                #plt.title("DOD-voltage",fontsize=title_size,fontname=font)
                #plt.plot(x,y1,color=cm2,label=NAME)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(2.95,4.5)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([3,3.2,3.4,3.6,3.8,4.0,4.2,4.4,4.5],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右上
                #plt.subplot(2,2,2)
                plt.title("dVdQ",fontsize=title_size,fontname=font)
                plt.plot(x,y2,color=cm2,label=NAME)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("dV/dQ[V/%]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(0,-0.05)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ左下
                #plt.subplot(2,2,3)
                #plt.title("delta_V",fontsize=title_size,fontname=font)
                #plt.plot(x,y3,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("delta-V[mV]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,505)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250,300,350,400,450,500],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右下
                #plt.subplot(2,2,4)
                #plt.title("DC-resistance",fontsize=title_size,fontname=font)
                #plt.plot(x,y4,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("DC-resistanve[mΩ]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,255)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250],fontsize=axis_size,fontname=font)
                #plt.legend()

        plt.show()
    def dvdq9():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        while color_list2.count("")>0:
            color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
                    [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
                    [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
                    [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
                    [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
                    [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
        len_Lot=len(Lot_list)#ロットのリスト長さ

    #--------------------------------------------------------------------------------------------------------------------
        #for i in range(5,6):
        for i in range(0,len_Lot):
            Rate=Rate_array[i]#ここは変える
            while Rate.count("")>0:
                Rate.remove("")
            #len_Rate=len(Rate)
            Lot=Lot_list[i]
            cm2=color_list1[i]
            C_V="Capacity_"+cut_vol+"[mAh]"
    #--------------------------------------------------------------------------------------------------------------------
            for j in range(2,3):
            #for j in range(0,len_Rate)
                rate=float(Rate[j])#レートの選択
                #cm2=color_list2[j]#行のカラー
                df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
                df3=df2[df2["Discharge-rate[C]"]==rate]#
                C_V2=df3[C_V].values#カット電圧時の容量データ
                C_V2=C_V2[0]
                Link=df3["Curve_Data_Link"].values#カーブデータのファイルを開く。
                Link=Link[0]
                DF=pd.read_csv(Link,encoding="cp932")
                x=np.array(DF["DOD[%]"].values.flatten())#x(dod)
                y1=np.array(DF["Voltage[V]"].values.flatten())#y1(vol)
                y2=np.array(DF["dVdQ[V/mAh]"].values.flatten())#y2(dVdQ)
                y3=np.array(DF["delta_V[mV]"].values.flatten())#y3(deltaV)
                y4=np.array(DF["DC_resistance[mohm]"].values.flatten())#y4(DCR)
                if(initial_dod=="DOD"):
                    pass
                elif(initial_dod=="Reference"):
                    if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        C_1C=df3["min_rated_capacity[mAh]"].values
                        x1=C_02[0]
                        x2=C_1C[0]
                        x=x*x1/x2
                    else:#0.2C容量を掛けて、各レートの容量で割る。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        DF3=df2[df2["Discharge-rate[C]"]==float(ref)]#
                        C_V3=DF3[C_V].values#カット電圧時の容量データ
                        C_V3=C_V3[0]
                        x1=C_02[0]
                        x2=C_V3
                        x=x*x1/x2
                else:
                    "正しく選択されていません"

                NAME=Lot+"_"+Rate[j]
                #グラフ左上
                title_size=int(d.get())
                axisN_size=int(e.get())
                axis_size=int(f.get())
                font=g.get()
                #plt.subplot(2,2,1)
                #plt.title("DOD-voltage",fontsize=title_size,fontname=font)
                #plt.plot(x,y1,color=cm2,label=NAME)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(2.95,4.5)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([3,3.2,3.4,3.6,3.8,4.0,4.2,4.4,4.5],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右上
                #plt.subplot(2,2,2)
                plt.title("dVdQ",fontsize=title_size,fontname=font)
                plt.plot(x,y2,color=cm2,label=NAME)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("dV/dQ[V/%]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(0,-0.05)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ左下
                #plt.subplot(2,2,3)
                #plt.title("delta_V",fontsize=title_size,fontname=font)
                #plt.plot(x,y3,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("delta-V[mV]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,505)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250,300,350,400,450,500],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右下
                #plt.subplot(2,2,4)
                #plt.title("DC-resistance",fontsize=title_size,fontname=font)
                #plt.plot(x,y4,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("DC-resistanve[mΩ]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,255)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250],fontsize=axis_size,fontname=font)
                #plt.legend()

        plt.show()
    def dvdq10():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        while color_list2.count("")>0:
            color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
                    [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
                    [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
                    [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
                    [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
                    [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
        len_Lot=len(Lot_list)#ロットのリスト長さ

    #--------------------------------------------------------------------------------------------------------------------
        #for i in range(5,6):
        for i in range(0,len_Lot):
            Rate=Rate_array[i]#ここは変える
            while Rate.count("")>0:
                Rate.remove("")
            #len_Rate=len(Rate)
            Lot=Lot_list[i]
            cm2=color_list1[i]
            C_V="Capacity_"+cut_vol+"[mAh]"
    #--------------------------------------------------------------------------------------------------------------------
            for j in range(3,4):
            #for j in range(0,len_Rate)
                rate=float(Rate[j])#レートの選択
                #cm2=color_list2[j]#行のカラー
                df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
                df3=df2[df2["Discharge-rate[C]"]==rate]#
                C_V2=df3[C_V].values#カット電圧時の容量データ
                C_V2=C_V2[0]
                Link=df3["Curve_Data_Link"].values#カーブデータのファイルを開く。
                Link=Link[0]
                DF=pd.read_csv(Link,encoding="cp932")
                x=np.array(DF["DOD[%]"].values.flatten())#x(dod)
                y1=np.array(DF["Voltage[V]"].values.flatten())#y1(vol)
                y2=np.array(DF["dVdQ[V/mAh]"].values.flatten())#y2(dVdQ)
                y3=np.array(DF["delta_V[mV]"].values.flatten())#y3(deltaV)
                y4=np.array(DF["DC_resistance[mohm]"].values.flatten())#y4(DCR)
                if(initial_dod=="DOD"):
                    pass
                elif(initial_dod=="Reference"):
                    if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        C_1C=df3["min_rated_capacity[mAh]"].values
                        x1=C_02[0]
                        x2=C_1C[0]
                        x=x*x1/x2
                    else:#0.2C容量を掛けて、各レートの容量で割る。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        DF3=df2[df2["Discharge-rate[C]"]==float(ref)]#
                        C_V3=DF3[C_V].values#カット電圧時の容量データ
                        C_V3=C_V3[0]
                        x1=C_02[0]
                        x2=C_V3
                        x=x*x1/x2
                else:
                    "正しく選択されていません"

                NAME=Lot+"_"+Rate[j]
                #グラフ左上
                title_size=int(d.get())
                axisN_size=int(e.get())
                axis_size=int(f.get())
                font=g.get()
                #plt.subplot(2,2,1)
                #plt.title("DOD-voltage",fontsize=title_size,fontname=font)
                #plt.plot(x,y1,color=cm2,label=NAME)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(2.95,4.5)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([3,3.2,3.4,3.6,3.8,4.0,4.2,4.4,4.5],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右上
                #plt.subplot(2,2,2)
                plt.title("dVdQ",fontsize=title_size,fontname=font)
                plt.plot(x,y2,color=cm2,label=NAME)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("dV/dQ[V/%]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(0,-0.05)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ左下
                #plt.subplot(2,2,3)
                #plt.title("delta_V",fontsize=title_size,fontname=font)
                #plt.plot(x,y3,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("delta-V[mV]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,505)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250,300,350,400,450,500],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右下
                #plt.subplot(2,2,4)
                #plt.title("DC-resistance",fontsize=title_size,fontname=font)
                #plt.plot(x,y4,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("DC-resistanve[mΩ]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,255)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250],fontsize=axis_size,fontname=font)
                #plt.legend()

        plt.show()
    def dvdq11():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        while color_list2.count("")>0:
            color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
                    [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
                    [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
                    [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
                    [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
                    [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
        len_Lot=len(Lot_list)#ロットのリスト長さ

    #--------------------------------------------------------------------------------------------------------------------
        #for i in range(5,6):
        for i in range(0,len_Lot):
            Rate=Rate_array[i]#ここは変える
            while Rate.count("")>0:
                Rate.remove("")
            #len_Rate=len(Rate)
            Lot=Lot_list[i]
            cm2=color_list1[i]
            C_V="Capacity_"+cut_vol+"[mAh]"
    #--------------------------------------------------------------------------------------------------------------------
            for j in range(4,5):
            #for j in range(0,len_Rate)
                rate=float(Rate[j])#レートの選択
                #cm2=color_list2[j]#行のカラー
                df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
                df3=df2[df2["Discharge-rate[C]"]==rate]#
                C_V2=df3[C_V].values#カット電圧時の容量データ
                C_V2=C_V2[0]
                Link=df3["Curve_Data_Link"].values#カーブデータのファイルを開く。
                Link=Link[0]
                DF=pd.read_csv(Link,encoding="cp932")
                x=np.array(DF["DOD[%]"].values.flatten())#x(dod)
                y1=np.array(DF["Voltage[V]"].values.flatten())#y1(vol)
                y2=np.array(DF["dVdQ[V/mAh]"].values.flatten())#y2(dVdQ)
                y3=np.array(DF["delta_V[mV]"].values.flatten())#y3(deltaV)
                y4=np.array(DF["DC_resistance[mohm]"].values.flatten())#y4(DCR)
                if(initial_dod=="DOD"):
                    pass
                elif(initial_dod=="Reference"):
                    if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        C_1C=df3["min_rated_capacity[mAh]"].values
                        x1=C_02[0]
                        x2=C_1C[0]
                        x=x*x1/x2
                    else:#0.2C容量を掛けて、各レートの容量で割る。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        DF3=df2[df2["Discharge-rate[C]"]==float(ref)]#
                        C_V3=DF3[C_V].values#カット電圧時の容量データ
                        C_V3=C_V3[0]
                        x1=C_02[0]
                        x2=C_V3
                        x=x*x1/x2
                else:
                    "正しく選択されていません"

                NAME=Lot+"_"+Rate[j]
                #グラフ左上
                title_size=int(d.get())
                axisN_size=int(e.get())
                axis_size=int(f.get())
                font=g.get()
                #plt.subplot(2,2,1)
                #plt.title("DOD-voltage",fontsize=title_size,fontname=font)
                #plt.plot(x,y1,color=cm2,label=NAME)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(2.95,4.5)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([3,3.2,3.4,3.6,3.8,4.0,4.2,4.4,4.5],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右上
                #plt.subplot(2,2,2)
                plt.title("dVdQ",fontsize=title_size,fontname=font)
                plt.plot(x,y2,color=cm2,label=NAME)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("dV/dQ[V/%]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(0,-0.05)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ左下
                #plt.subplot(2,2,3)
                #plt.title("delta_V",fontsize=title_size,fontname=font)
                #plt.plot(x,y3,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("delta-V[mV]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,505)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250,300,350,400,450,500],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右下
                #plt.subplot(2,2,4)
                #plt.title("DC-resistance",fontsize=title_size,fontname=font)
                #plt.plot(x,y4,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("DC-resistanve[mΩ]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,255)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250],fontsize=axis_size,fontname=font)
                #plt.legend()

        plt.show()
    def dvdq12():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        while color_list2.count("")>0:
            color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
                    [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
                    [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
                    [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
                    [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
                    [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
        len_Lot=len(Lot_list)#ロットのリスト長さ

    #--------------------------------------------------------------------------------------------------------------------
        #for i in range(5,6):
        for i in range(0,len_Lot):
            Rate=Rate_array[i]#ここは変える
            while Rate.count("")>0:
                Rate.remove("")
            #len_Rate=len(Rate)
            Lot=Lot_list[i]
            cm2=color_list1[i]
            C_V="Capacity_"+cut_vol+"[mAh]"
    #--------------------------------------------------------------------------------------------------------------------
            for j in range(5,6):
            #for j in range(0,len_Rate)
                rate=float(Rate[j])#レートの選択
                #cm2=color_list2[j]#行のカラー
                df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
                df3=df2[df2["Discharge-rate[C]"]==rate]#
                C_V2=df3[C_V].values#カット電圧時の容量データ
                C_V2=C_V2[0]
                Link=df3["Curve_Data_Link"].values#カーブデータのファイルを開く。
                Link=Link[0]
                DF=pd.read_csv(Link,encoding="cp932")
                x=np.array(DF["DOD[%]"].values.flatten())#x(dod)
                y1=np.array(DF["Voltage[V]"].values.flatten())#y1(vol)
                y2=np.array(DF["dVdQ[V/mAh]"].values.flatten())#y2(dVdQ)
                y3=np.array(DF["delta_V[mV]"].values.flatten())#y3(deltaV)
                y4=np.array(DF["DC_resistance[mohm]"].values.flatten())#y4(DCR)
                if(initial_dod=="DOD"):
                    pass
                elif(initial_dod=="Reference"):
                    if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        C_1C=df3["min_rated_capacity[mAh]"].values
                        x1=C_02[0]
                        x2=C_1C[0]
                        x=x*x1/x2
                    else:#0.2C容量を掛けて、各レートの容量で割る。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        DF3=df2[df2["Discharge-rate[C]"]==float(ref)]#
                        C_V3=DF3[C_V].values#カット電圧時の容量データ
                        C_V3=C_V3[0]
                        x1=C_02[0]
                        x2=C_V3
                        x=x*x1/x2
                else:
                    "正しく選択されていません"

                NAME=Lot+"_"+Rate[j]
                #グラフ左上
                title_size=int(d.get())
                axisN_size=int(e.get())
                axis_size=int(f.get())
                font=g.get()
                #plt.subplot(2,2,1)
                #plt.title("DOD-voltage",fontsize=title_size,fontname=font)
                #plt.plot(x,y1,color=cm2,label=NAME)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(2.95,4.5)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([3,3.2,3.4,3.6,3.8,4.0,4.2,4.4,4.5],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右上
                #plt.subplot(2,2,2)
                plt.title("dVdQ",fontsize=title_size,fontname=font)
                plt.plot(x,y2,color=cm2,label=NAME)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("dV/dQ[V/%]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(0,-0.05)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ左下
                #plt.subplot(2,2,3)
                #plt.title("delta_V",fontsize=title_size,fontname=font)
                #plt.plot(x,y3,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("delta-V[mV]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,505)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250,300,350,400,450,500],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右下
                #plt.subplot(2,2,4)
                #plt.title("DC-resistance",fontsize=title_size,fontname=font)
                #plt.plot(x,y4,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("DC-resistanve[mΩ]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,255)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250],fontsize=axis_size,fontname=font)
                #plt.legend()

        plt.show()

    def delta_V1():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        while color_list2.count("")>0:
            color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
                    [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
                    [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
                    [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
                    [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
                    [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
    #len_Lot=len(Lot_List)#ロットのリスト長さ

    #--------------------------------------------------------------------------------------------------------------------
        for i in range(0,1):
        #for i in range(0,Lot_list):
            Rate=Rate_array[i]#ここは変える
            while Rate.count("")>0:
                Rate.remove("")
            len_Rate=len(Rate)
            Lot=Lot_list[i]
            #cm1=color_list1[i]
            C_V="Capacity_"+cut_vol+"[mAh]"
    #--------------------------------------------------------------------------------------------------------------------
            for j in range(0,len_Rate):
                rate=float(Rate[j])#レートの選択
                cm2=color_list2[j]#行のカラー
                df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
                df3=df2[df2["Discharge-rate[C]"]==rate]#
                C_V2=df3[C_V].values#カット電圧時の容量データ
                C_V2=C_V2[0]
                Link=df3["Curve_Data_Link"].values#カーブデータのファイルを開く。
                Link=Link[0]
                DF=pd.read_csv(Link,encoding="cp932")
                x=np.array(DF["DOD[%]"].values.flatten())#x(dod)
                y1=np.array(DF["Voltage[V]"].values.flatten())#y1(vol)
                y2=np.array(DF["dVdQ[V/mAh]"].values.flatten())#y2(dVdQ)
                y3=np.array(DF["delta_V[mV]"].values.flatten())#y3(deltaV)
                y4=np.array(DF["DC_resistance[mohm]"].values.flatten())#y4(DCR)
                if(initial_dod=="DOD"):
                    pass
                elif(initial_dod=="Reference"):
                    if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        C_1C=df3["min_rated_capacity[mAh]"].values
                        x1=C_02[0]
                        x2=C_1C[0]
                        x=x*x1/x2
                    else:#0.2C容量を掛けて、各レートの容量で割る。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        DF3=df2[df2["Discharge-rate[C]"]==float(ref)]#
                        C_V3=DF3[C_V].values#カット電圧時の容量データ
                        C_V3=C_V3[0]
                        x1=C_02[0]
                        x2=C_V3
                        x=x*x1/x2
                else:
                    "正しく選択されていません"

                NAME=Lot+"_"+Rate[j]
                #グラフ左上
                title_size=int(d.get())
                axisN_size=int(e.get())
                axis_size=int(f.get())
                font=g.get()
                #plt.subplot(2,2,1)
                #plt.title("DOD-voltage",fontsize=title_size,fontname=font)
                #plt.plot(x,y1,color=cm2,label=NAME)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(2.95,4.5)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([3,3.2,3.4,3.6,3.8,4.0,4.2,4.4,4.5],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右上
                #plt.subplot(2,2,2)
                #plt.title("dVdQ",fontsize=title_size,fontname=font)
                #plt.plot(x,y2,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("dV/dQ[V/%]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(0,-0.05)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,-0.01,-0.02,-0.03,-0.04,-0.05],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ左下
                #plt.subplot(2,2,3)
                plt.title("delta_V",fontsize=title_size,fontname=font)
                plt.plot(x,y3,color=cm2,label=NAME)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("delta-V[mV]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(-5,505)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ右下
                #plt.subplot(2,2,4)
                #plt.title("DC-resistance",fontsize=title_size,fontname=font)
                #plt.plot(x,y4,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("DC-resistanve[mΩ]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,255)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250],fontsize=axis_size,fontname=font)
                #plt.legend()

        plt.show()
    def delta_V2():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        while color_list2.count("")>0:
            color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
                    [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
                    [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
                    [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
                    [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
                    [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
    #len_Lot=len(Lot_List)#ロットのリスト長さ

    #--------------------------------------------------------------------------------------------------------------------
        for i in range(1,2):
        #for i in range(0,Lot_list):
            Rate=Rate_array[i]#ここは変える
            while Rate.count("")>0:
                Rate.remove("")
            len_Rate=len(Rate)
            Lot=Lot_list[i]
            #cm1=color_list1[i]
            C_V="Capacity_"+cut_vol+"[mAh]"
    #--------------------------------------------------------------------------------------------------------------------
            for j in range(0,len_Rate):
                rate=float(Rate[j])#レートの選択
                cm2=color_list2[j]#行のカラー
                df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
                df3=df2[df2["Discharge-rate[C]"]==rate]#
                C_V2=df3[C_V].values#カット電圧時の容量データ
                C_V2=C_V2[0]
                Link=df3["Curve_Data_Link"].values#カーブデータのファイルを開く。
                Link=Link[0]
                DF=pd.read_csv(Link,encoding="cp932")
                x=np.array(DF["DOD[%]"].values.flatten())#x(dod)
                y1=np.array(DF["Voltage[V]"].values.flatten())#y1(vol)
                y2=np.array(DF["dVdQ[V/mAh]"].values.flatten())#y2(dVdQ)
                y3=np.array(DF["delta_V[mV]"].values.flatten())#y3(deltaV)
                y4=np.array(DF["DC_resistance[mohm]"].values.flatten())#y4(DCR)
                if(initial_dod=="DOD"):
                    pass
                elif(initial_dod=="Reference"):
                    if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        C_1C=df3["min_rated_capacity[mAh]"].values
                        x1=C_02[0]
                        x2=C_1C[0]
                        x=x*x1/x2
                    else:#0.2C容量を掛けて、各レートの容量で割る。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        DF3=df2[df2["Discharge-rate[C]"]==float(ref)]#
                        C_V3=DF3[C_V].values#カット電圧時の容量データ
                        C_V3=C_V3[0]
                        x1=C_02[0]
                        x2=C_V3
                        x=x*x1/x2
                else:
                    "正しく選択されていません"

                NAME=Lot+"_"+Rate[j]
                #グラフ左上
                title_size=int(d.get())
                axisN_size=int(e.get())
                axis_size=int(f.get())
                font=g.get()
                #plt.subplot(2,2,1)
                #plt.title("DOD-voltage",fontsize=title_size,fontname=font)
                #plt.plot(x,y1,color=cm2,label=NAME)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(2.95,4.5)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([3,3.2,3.4,3.6,3.8,4.0,4.2,4.4,4.5],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右上
                #plt.subplot(2,2,2)
                #plt.title("dVdQ",fontsize=title_size,fontname=font)
                #plt.plot(x,y2,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("dV/dQ[V/%]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(0,-0.05)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,-0.01,-0.02,-0.03,-0.04,-0.05],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ左下
                #plt.subplot(2,2,3)
                plt.title("delta_V",fontsize=title_size,fontname=font)
                plt.plot(x,y3,color=cm2,label=NAME)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("delta-V[mV]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(-5,505)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ右下
                #plt.subplot(2,2,4)
                #plt.title("DC-resistance",fontsize=title_size,fontname=font)
                #plt.plot(x,y4,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("DC-resistanve[mΩ]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,255)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250],fontsize=axis_size,fontname=font)
                #plt.legend()

        plt.show()
    def delta_V3():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        while color_list2.count("")>0:
            color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
                    [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
                    [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
                    [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
                    [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
                    [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
    #len_Lot=len(Lot_List)#ロットのリスト長さ

    #--------------------------------------------------------------------------------------------------------------------
        for i in range(2,3):
        #for i in range(0,Lot_list):
            Rate=Rate_array[i]#ここは変える
            while Rate.count("")>0:
                Rate.remove("")
            len_Rate=len(Rate)
            Lot=Lot_list[i]
            #cm1=color_list1[i]
            C_V="Capacity_"+cut_vol+"[mAh]"
    #--------------------------------------------------------------------------------------------------------------------
            for j in range(0,len_Rate):
                rate=float(Rate[j])#レートの選択
                cm2=color_list2[j]#行のカラー
                df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
                df3=df2[df2["Discharge-rate[C]"]==rate]#
                C_V2=df3[C_V].values#カット電圧時の容量データ
                C_V2=C_V2[0]
                Link=df3["Curve_Data_Link"].values#カーブデータのファイルを開く。
                Link=Link[0]
                DF=pd.read_csv(Link,encoding="cp932")
                x=np.array(DF["DOD[%]"].values.flatten())#x(dod)
                y1=np.array(DF["Voltage[V]"].values.flatten())#y1(vol)
                y2=np.array(DF["dVdQ[V/mAh]"].values.flatten())#y2(dVdQ)
                y3=np.array(DF["delta_V[mV]"].values.flatten())#y3(deltaV)
                y4=np.array(DF["DC_resistance[mohm]"].values.flatten())#y4(DCR)
                if(initial_dod=="DOD"):
                    pass
                elif(initial_dod=="Reference"):
                    if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        C_1C=df3["min_rated_capacity[mAh]"].values
                        x1=C_02[0]
                        x2=C_1C[0]
                        x=x*x1/x2
                    else:#0.2C容量を掛けて、各レートの容量で割る。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        DF3=df2[df2["Discharge-rate[C]"]==float(ref)]#
                        C_V3=DF3[C_V].values#カット電圧時の容量データ
                        C_V3=C_V3[0]
                        x1=C_02[0]
                        x2=C_V3
                        x=x*x1/x2
                else:
                    "正しく選択されていません"

                NAME=Lot+"_"+Rate[j]
                #グラフ左上
                title_size=int(d.get())
                axisN_size=int(e.get())
                axis_size=int(f.get())
                font=g.get()
                #plt.subplot(2,2,1)
                #plt.title("DOD-voltage",fontsize=title_size,fontname=font)
                #plt.plot(x,y1,color=cm2,label=NAME)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(2.95,4.5)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([3,3.2,3.4,3.6,3.8,4.0,4.2,4.4,4.5],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右上
                #plt.subplot(2,2,2)
                #plt.title("dVdQ",fontsize=title_size,fontname=font)
                #plt.plot(x,y2,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("dV/dQ[V/%]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(0,-0.05)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,-0.01,-0.02,-0.03,-0.04,-0.05],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ左下
                #plt.subplot(2,2,3)
                plt.title("delta_V",fontsize=title_size,fontname=font)
                plt.plot(x,y3,color=cm2,label=NAME)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("delta-V[mV]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(-5,505)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ右下
                #plt.subplot(2,2,4)
                #plt.title("DC-resistance",fontsize=title_size,fontname=font)
                #plt.plot(x,y4,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("DC-resistanve[mΩ]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,255)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250],fontsize=axis_size,fontname=font)
                #plt.legend()

        plt.show()
    def delta_V4():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        while color_list2.count("")>0:
            color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
                    [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
                    [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
                    [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
                    [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
                    [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
    #len_Lot=len(Lot_List)#ロットのリスト長さ

    #--------------------------------------------------------------------------------------------------------------------
        for i in range(3,4):
        #for i in range(0,Lot_list):
            Rate=Rate_array[i]#ここは変える
            while Rate.count("")>0:
                Rate.remove("")
            len_Rate=len(Rate)
            Lot=Lot_list[i]
            #cm1=color_list1[i]
            C_V="Capacity_"+cut_vol+"[mAh]"
    #--------------------------------------------------------------------------------------------------------------------
            for j in range(0,len_Rate):
                rate=float(Rate[j])#レートの選択
                cm2=color_list2[j]#行のカラー
                df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
                df3=df2[df2["Discharge-rate[C]"]==rate]#
                C_V2=df3[C_V].values#カット電圧時の容量データ
                C_V2=C_V2[0]
                Link=df3["Curve_Data_Link"].values#カーブデータのファイルを開く。
                Link=Link[0]
                DF=pd.read_csv(Link,encoding="cp932")
                x=np.array(DF["DOD[%]"].values.flatten())#x(dod)
                y1=np.array(DF["Voltage[V]"].values.flatten())#y1(vol)
                y2=np.array(DF["dVdQ[V/mAh]"].values.flatten())#y2(dVdQ)
                y3=np.array(DF["delta_V[mV]"].values.flatten())#y3(deltaV)
                y4=np.array(DF["DC_resistance[mohm]"].values.flatten())#y4(DCR)
                if(initial_dod=="DOD"):
                    pass
                elif(initial_dod=="Reference"):
                    if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        C_1C=df3["min_rated_capacity[mAh]"].values
                        x1=C_02[0]
                        x2=C_1C[0]
                        x=x*x1/x2
                    else:#0.2C容量を掛けて、各レートの容量で割る。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        DF3=df2[df2["Discharge-rate[C]"]==float(ref)]#
                        C_V3=DF3[C_V].values#カット電圧時の容量データ
                        C_V3=C_V3[0]
                        x1=C_02[0]
                        x2=C_V3
                        x=x*x1/x2
                else:
                    "正しく選択されていません"

                NAME=Lot+"_"+Rate[j]
                #グラフ左上
                title_size=int(d.get())
                axisN_size=int(e.get())
                axis_size=int(f.get())
                font=g.get()
                #plt.subplot(2,2,1)
                #plt.title("DOD-voltage",fontsize=title_size,fontname=font)
                #plt.plot(x,y1,color=cm2,label=NAME)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(2.95,4.5)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([3,3.2,3.4,3.6,3.8,4.0,4.2,4.4,4.5],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右上
                #plt.subplot(2,2,2)
                #plt.title("dVdQ",fontsize=title_size,fontname=font)
                #plt.plot(x,y2,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("dV/dQ[V/%]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(0,-0.05)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,-0.01,-0.02,-0.03,-0.04,-0.05],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ左下
                #plt.subplot(2,2,3)
                plt.title("delta_V",fontsize=title_size,fontname=font)
                plt.plot(x,y3,color=cm2,label=NAME)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("delta-V[mV]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(-5,505)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ右下
                #plt.subplot(2,2,4)
                #plt.title("DC-resistance",fontsize=title_size,fontname=font)
                #plt.plot(x,y4,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("DC-resistanve[mΩ]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,255)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250],fontsize=axis_size,fontname=font)
                #plt.legend()

        plt.show()
    def delta_V5():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        while color_list2.count("")>0:
            color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
                    [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
                    [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
                    [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
                    [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
                    [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
    #len_Lot=len(Lot_List)#ロットのリスト長さ

    #--------------------------------------------------------------------------------------------------------------------
        for i in range(4,5):
        #for i in range(0,Lot_list):
            Rate=Rate_array[i]#ここは変える
            while Rate.count("")>0:
                Rate.remove("")
            len_Rate=len(Rate)
            Lot=Lot_list[i]
            #cm1=color_list1[i]
            C_V="Capacity_"+cut_vol+"[mAh]"
    #--------------------------------------------------------------------------------------------------------------------
            for j in range(0,len_Rate):
                rate=float(Rate[j])#レートの選択
                cm2=color_list2[j]#行のカラー
                df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
                df3=df2[df2["Discharge-rate[C]"]==rate]#
                C_V2=df3[C_V].values#カット電圧時の容量データ
                C_V2=C_V2[0]
                Link=df3["Curve_Data_Link"].values#カーブデータのファイルを開く。
                Link=Link[0]
                DF=pd.read_csv(Link,encoding="cp932")
                x=np.array(DF["DOD[%]"].values.flatten())#x(dod)
                y1=np.array(DF["Voltage[V]"].values.flatten())#y1(vol)
                y2=np.array(DF["dVdQ[V/mAh]"].values.flatten())#y2(dVdQ)
                y3=np.array(DF["delta_V[mV]"].values.flatten())#y3(deltaV)
                y4=np.array(DF["DC_resistance[mohm]"].values.flatten())#y4(DCR)
                if(initial_dod=="DOD"):
                    pass
                elif(initial_dod=="Reference"):
                    if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        C_1C=df3["min_rated_capacity[mAh]"].values
                        x1=C_02[0]
                        x2=C_1C[0]
                        x=x*x1/x2
                    else:#0.2C容量を掛けて、各レートの容量で割る。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        DF3=df2[df2["Discharge-rate[C]"]==float(ref)]#
                        C_V3=DF3[C_V].values#カット電圧時の容量データ
                        C_V3=C_V3[0]
                        x1=C_02[0]
                        x2=C_V3
                        x=x*x1/x2
                else:
                    "正しく選択されていません"

                NAME=Lot+"_"+Rate[j]
                #グラフ左上
                title_size=int(d.get())
                axisN_size=int(e.get())
                axis_size=int(f.get())
                font=g.get()
                #plt.subplot(2,2,1)
                #plt.title("DOD-voltage",fontsize=title_size,fontname=font)
                #plt.plot(x,y1,color=cm2,label=NAME)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(2.95,4.5)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([3,3.2,3.4,3.6,3.8,4.0,4.2,4.4,4.5],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右上
                #plt.subplot(2,2,2)
                #plt.title("dVdQ",fontsize=title_size,fontname=font)
                #plt.plot(x,y2,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("dV/dQ[V/%]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(0,-0.05)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,-0.01,-0.02,-0.03,-0.04,-0.05],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ左下
                #plt.subplot(2,2,3)
                plt.title("delta_V",fontsize=title_size,fontname=font)
                plt.plot(x,y3,color=cm2,label=NAME)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("delta-V[mV]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(-5,505)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ右下
                #plt.subplot(2,2,4)
                #plt.title("DC-resistance",fontsize=title_size,fontname=font)
                #plt.plot(x,y4,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("DC-resistanve[mΩ]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,255)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250],fontsize=axis_size,fontname=font)
                #plt.legend()

        plt.show()
    def delta_V6():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        while color_list2.count("")>0:
            color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
                    [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
                    [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
                    [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
                    [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
                    [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
    #len_Lot=len(Lot_List)#ロットのリスト長さ

    #--------------------------------------------------------------------------------------------------------------------
        for i in range(5,6):
        #for i in range(0,Lot_list):
            Rate=Rate_array[i]#ここは変える
            while Rate.count("")>0:
                Rate.remove("")
            len_Rate=len(Rate)
            Lot=Lot_list[i]
            #cm1=color_list1[i]
            C_V="Capacity_"+cut_vol+"[mAh]"
    #--------------------------------------------------------------------------------------------------------------------
            for j in range(0,len_Rate):
                rate=float(Rate[j])#レートの選択
                cm2=color_list2[j]#行のカラー
                df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
                df3=df2[df2["Discharge-rate[C]"]==rate]#
                C_V2=df3[C_V].values#カット電圧時の容量データ
                C_V2=C_V2[0]
                Link=df3["Curve_Data_Link"].values#カーブデータのファイルを開く。
                Link=Link[0]
                DF=pd.read_csv(Link,encoding="cp932")
                x=np.array(DF["DOD[%]"].values.flatten())#x(dod)
                y1=np.array(DF["Voltage[V]"].values.flatten())#y1(vol)
                y2=np.array(DF["dVdQ[V/mAh]"].values.flatten())#y2(dVdQ)
                y3=np.array(DF["delta_V[mV]"].values.flatten())#y3(deltaV)
                y4=np.array(DF["DC_resistance[mohm]"].values.flatten())#y4(DCR)
                if(initial_dod=="DOD"):
                    pass
                elif(initial_dod=="Reference"):
                    if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        C_1C=df3["min_rated_capacity[mAh]"].values
                        x1=C_02[0]
                        x2=C_1C[0]
                        x=x*x1/x2
                    else:#0.2C容量を掛けて、各レートの容量で割る。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        DF3=df2[df2["Discharge-rate[C]"]==float(ref)]#
                        C_V3=DF3[C_V].values#カット電圧時の容量データ
                        C_V3=C_V3[0]
                        x1=C_02[0]
                        x2=C_V3
                        x=x*x1/x2
                else:
                    "正しく選択されていません"

                NAME=Lot+"_"+Rate[j]
                #グラフ左上
                title_size=int(d.get())
                axisN_size=int(e.get())
                axis_size=int(f.get())
                font=g.get()
                #plt.subplot(2,2,1)
                #plt.title("DOD-voltage",fontsize=title_size,fontname=font)
                #plt.plot(x,y1,color=cm2,label=NAME)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(2.95,4.5)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([3,3.2,3.4,3.6,3.8,4.0,4.2,4.4,4.5],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右上
                #plt.subplot(2,2,2)
                #plt.title("dVdQ",fontsize=title_size,fontname=font)
                #plt.plot(x,y2,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("dV/dQ[V/%]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(0,-0.05)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,-0.01,-0.02,-0.03,-0.04,-0.05],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ左下
                #plt.subplot(2,2,3)
                plt.title("delta_V",fontsize=title_size,fontname=font)
                plt.plot(x,y3,color=cm2,label=NAME)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("delta-V[mV]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(-5,505)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ右下
                #plt.subplot(2,2,4)
                #plt.title("DC-resistance",fontsize=title_size,fontname=font)
                #plt.plot(x,y4,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("DC-resistanve[mΩ]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,255)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250],fontsize=axis_size,fontname=font)
                #plt.legend()

        plt.show()
    def delta_V7():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        while color_list2.count("")>0:
            color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
                    [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
                    [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
                    [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
                    [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
                    [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
        len_Lot=len(Lot_list)#ロットのリスト長さ

    #--------------------------------------------------------------------------------------------------------------------
        #for i in range(5,6):
        for i in range(0,len_Lot):
            Rate=Rate_array[i]#ここは変える
            while Rate.count("")>0:
                Rate.remove("")
            #len_Rate=len(Rate)
            Lot=Lot_list[i]
            cm2=color_list1[i]
            C_V="Capacity_"+cut_vol+"[mAh]"
    #--------------------------------------------------------------------------------------------------------------------
            for j in range(0,1):
            #for j in range(0,len_Rate)
                rate=float(Rate[j])#レートの選択
                #cm2=color_list2[j]#行のカラー
                df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
                df3=df2[df2["Discharge-rate[C]"]==rate]#
                C_V2=df3[C_V].values#カット電圧時の容量データ
                C_V2=C_V2[0]
                Link=df3["Curve_Data_Link"].values#カーブデータのファイルを開く。
                Link=Link[0]
                DF=pd.read_csv(Link,encoding="cp932")
                x=np.array(DF["DOD[%]"].values.flatten())#x(dod)
                y1=np.array(DF["Voltage[V]"].values.flatten())#y1(vol)
                y2=np.array(DF["dVdQ[V/mAh]"].values.flatten())#y2(dVdQ)
                y3=np.array(DF["delta_V[mV]"].values.flatten())#y3(deltaV)
                y4=np.array(DF["DC_resistance[mohm]"].values.flatten())#y4(DCR)
                if(initial_dod=="DOD"):
                    pass
                elif(initial_dod=="Reference"):
                    if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        C_1C=df3["min_rated_capacity[mAh]"].values
                        x1=C_02[0]
                        x2=C_1C[0]
                        x=x*x1/x2
                    else:#0.2C容量を掛けて、各レートの容量で割る。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        DF3=df2[df2["Discharge-rate[C]"]==float(ref)]#
                        C_V3=DF3[C_V].values#カット電圧時の容量データ
                        C_V3=C_V3[0]
                        x1=C_02[0]
                        x2=C_V3
                        x=x*x1/x2
                else:
                    "正しく選択されていません"

                NAME=Lot+"_"+Rate[j]
                #グラフ左上
                title_size=int(d.get())
                axisN_size=int(e.get())
                axis_size=int(f.get())
                font=g.get()
                #plt.subplot(2,2,1)
                #plt.title("DOD-voltage",fontsize=title_size,fontname=font)
                #plt.plot(x,y1,color=cm2,label=NAME)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(2.95,4.5)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([3,3.2,3.4,3.6,3.8,4.0,4.2,4.4,4.5],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右上
                #plt.subplot(2,2,2)
                #plt.title("dVdQ",fontsize=title_size,fontname=font)
                #plt.plot(x,y2,color=cm2,label=NAME)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("dV/dQ[V/%]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(0,-0.05)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,-0.01,-0.02,-0.03,-0.04,-0.05],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ左下
                #plt.subplot(2,2,3)
                plt.title("delta_V",fontsize=title_size,fontname=font)
                plt.plot(x,y3,color=cm2,label=NAME)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("delta-V[mV]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(-5,505)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ右下
                #plt.subplot(2,2,4)
                #plt.title("DC-resistance",fontsize=title_size,fontname=font)
                #plt.plot(x,y4,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("DC-resistanve[mΩ]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,255)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250],fontsize=axis_size,fontname=font)
                #plt.legend()

        plt.show()
    def delta_V8():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        while color_list2.count("")>0:
            color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
                    [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
                    [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
                    [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
                    [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
                    [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
        len_Lot=len(Lot_list)#ロットのリスト長さ

    #--------------------------------------------------------------------------------------------------------------------
        #for i in range(5,6):
        for i in range(0,len_Lot):
            Rate=Rate_array[i]#ここは変える
            while Rate.count("")>0:
                Rate.remove("")
            #len_Rate=len(Rate)
            Lot=Lot_list[i]
            cm2=color_list1[i]
            C_V="Capacity_"+cut_vol+"[mAh]"
    #--------------------------------------------------------------------------------------------------------------------
            for j in range(1,2):
            #for j in range(0,len_Rate)
                rate=float(Rate[j])#レートの選択
                #cm2=color_list2[j]#行のカラー
                df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
                df3=df2[df2["Discharge-rate[C]"]==rate]#
                C_V2=df3[C_V].values#カット電圧時の容量データ
                C_V2=C_V2[0]
                Link=df3["Curve_Data_Link"].values#カーブデータのファイルを開く。
                Link=Link[0]
                DF=pd.read_csv(Link,encoding="cp932")
                x=np.array(DF["DOD[%]"].values.flatten())#x(dod)
                y1=np.array(DF["Voltage[V]"].values.flatten())#y1(vol)
                y2=np.array(DF["dVdQ[V/mAh]"].values.flatten())#y2(dVdQ)
                y3=np.array(DF["delta_V[mV]"].values.flatten())#y3(deltaV)
                y4=np.array(DF["DC_resistance[mohm]"].values.flatten())#y4(DCR)
                if(initial_dod=="DOD"):
                    pass
                elif(initial_dod=="Reference"):
                    if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        C_1C=df3["min_rated_capacity[mAh]"].values
                        x1=C_02[0]
                        x2=C_1C[0]
                        x=x*x1/x2
                    else:#0.2C容量を掛けて、各レートの容量で割る。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        DF3=df2[df2["Discharge-rate[C]"]==float(ref)]#
                        C_V3=DF3[C_V].values#カット電圧時の容量データ
                        C_V3=C_V3[0]
                        x1=C_02[0]
                        x2=C_V3
                        x=x*x1/x2
                else:
                    "正しく選択されていません"

                NAME=Lot+"_"+Rate[j]
                #グラフ左上
                title_size=int(d.get())
                axisN_size=int(e.get())
                axis_size=int(f.get())
                font=g.get()
                #plt.subplot(2,2,1)
                #plt.title("DOD-voltage",fontsize=title_size,fontname=font)
                #plt.plot(x,y1,color=cm2,label=NAME)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(2.95,4.5)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([3,3.2,3.4,3.6,3.8,4.0,4.2,4.4,4.5],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右上
                #plt.subplot(2,2,2)
                #plt.title("dVdQ",fontsize=title_size,fontname=font)
                #plt.plot(x,y2,color=cm2,label=NAME)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("dV/dQ[V/%]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(0,-0.05)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,-0.01,-0.02,-0.03,-0.04,-0.05],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ左下
                #plt.subplot(2,2,3)
                plt.title("delta_V",fontsize=title_size,fontname=font)
                plt.plot(x,y3,color=cm2,label=NAME)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("delta-V[mV]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(-5,505)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ右下
                #plt.subplot(2,2,4)
                #plt.title("DC-resistance",fontsize=title_size,fontname=font)
                #plt.plot(x,y4,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("DC-resistanve[mΩ]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,255)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250],fontsize=axis_size,fontname=font)
                #plt.legend()

        plt.show()
    def delta_V9():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        while color_list2.count("")>0:
            color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
                    [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
                    [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
                    [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
                    [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
                    [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
        len_Lot=len(Lot_list)#ロットのリスト長さ

    #--------------------------------------------------------------------------------------------------------------------
        #for i in range(5,6):
        for i in range(0,len_Lot):
            Rate=Rate_array[i]#ここは変える
            while Rate.count("")>0:
                Rate.remove("")
            #len_Rate=len(Rate)
            Lot=Lot_list[i]
            cm2=color_list1[i]
            C_V="Capacity_"+cut_vol+"[mAh]"
    #--------------------------------------------------------------------------------------------------------------------
            for j in range(2,3):
            #for j in range(0,len_Rate)
                rate=float(Rate[j])#レートの選択
                #cm2=color_list2[j]#行のカラー
                df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
                df3=df2[df2["Discharge-rate[C]"]==rate]#
                C_V2=df3[C_V].values#カット電圧時の容量データ
                C_V2=C_V2[0]
                Link=df3["Curve_Data_Link"].values#カーブデータのファイルを開く。
                Link=Link[0]
                DF=pd.read_csv(Link,encoding="cp932")
                x=np.array(DF["DOD[%]"].values.flatten())#x(dod)
                y1=np.array(DF["Voltage[V]"].values.flatten())#y1(vol)
                y2=np.array(DF["dVdQ[V/mAh]"].values.flatten())#y2(dVdQ)
                y3=np.array(DF["delta_V[mV]"].values.flatten())#y3(deltaV)
                y4=np.array(DF["DC_resistance[mohm]"].values.flatten())#y4(DCR)
                if(initial_dod=="DOD"):
                    pass
                elif(initial_dod=="Reference"):
                    if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        C_1C=df3["min_rated_capacity[mAh]"].values
                        x1=C_02[0]
                        x2=C_1C[0]
                        x=x*x1/x2
                    else:#0.2C容量を掛けて、各レートの容量で割る。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        DF3=df2[df2["Discharge-rate[C]"]==float(ref)]#
                        C_V3=DF3[C_V].values#カット電圧時の容量データ
                        C_V3=C_V3[0]
                        x1=C_02[0]
                        x2=C_V3
                        x=x*x1/x2
                else:
                    "正しく選択されていません"

                NAME=Lot+"_"+Rate[j]
                #グラフ左上
                title_size=int(d.get())
                axisN_size=int(e.get())
                axis_size=int(f.get())
                font=g.get()
                #plt.subplot(2,2,1)
                #plt.title("DOD-voltage",fontsize=title_size,fontname=font)
                #plt.plot(x,y1,color=cm2,label=NAME)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(2.95,4.5)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([3,3.2,3.4,3.6,3.8,4.0,4.2,4.4,4.5],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右上
                #plt.subplot(2,2,2)
                #plt.title("dVdQ",fontsize=title_size,fontname=font)
                #plt.plot(x,y2,color=cm2,label=NAME)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("dV/dQ[V/%]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(0,-0.05)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,-0.01,-0.02,-0.03,-0.04,-0.05],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ左下
                #plt.subplot(2,2,3)
                plt.title("delta_V",fontsize=title_size,fontname=font)
                plt.plot(x,y3,color=cm2,label=NAME)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("delta-V[mV]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(-5,505)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ右下
                #plt.subplot(2,2,4)
                #plt.title("DC-resistance",fontsize=title_size,fontname=font)
                #plt.plot(x,y4,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("DC-resistanve[mΩ]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,255)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250],fontsize=axis_size,fontname=font)
                #plt.legend()

        plt.show()
    def delta_V10():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        while color_list2.count("")>0:
            color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
                    [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
                    [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
                    [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
                    [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
                    [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
        len_Lot=len(Lot_list)#ロットのリスト長さ

    #--------------------------------------------------------------------------------------------------------------------
        #for i in range(5,6):
        for i in range(0,len_Lot):
            Rate=Rate_array[i]#ここは変える
            while Rate.count("")>0:
                Rate.remove("")
            #len_Rate=len(Rate)
            Lot=Lot_list[i]
            cm2=color_list1[i]
            C_V="Capacity_"+cut_vol+"[mAh]"
    #--------------------------------------------------------------------------------------------------------------------
            for j in range(3,4):
            #for j in range(0,len_Rate)
                rate=float(Rate[j])#レートの選択
                #cm2=color_list2[j]#行のカラー
                df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
                df3=df2[df2["Discharge-rate[C]"]==rate]#
                C_V2=df3[C_V].values#カット電圧時の容量データ
                C_V2=C_V2[0]
                Link=df3["Curve_Data_Link"].values#カーブデータのファイルを開く。
                Link=Link[0]
                DF=pd.read_csv(Link,encoding="cp932")
                x=np.array(DF["DOD[%]"].values.flatten())#x(dod)
                y1=np.array(DF["Voltage[V]"].values.flatten())#y1(vol)
                y2=np.array(DF["dVdQ[V/mAh]"].values.flatten())#y2(dVdQ)
                y3=np.array(DF["delta_V[mV]"].values.flatten())#y3(deltaV)
                y4=np.array(DF["DC_resistance[mohm]"].values.flatten())#y4(DCR)
                if(initial_dod=="DOD"):
                    pass
                elif(initial_dod=="Reference"):
                    if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        C_1C=df3["min_rated_capacity[mAh]"].values
                        x1=C_02[0]
                        x2=C_1C[0]
                        x=x*x1/x2
                    else:#0.2C容量を掛けて、各レートの容量で割る。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        DF3=df2[df2["Discharge-rate[C]"]==float(ref)]#
                        C_V3=DF3[C_V].values#カット電圧時の容量データ
                        C_V3=C_V3[0]
                        x1=C_02[0]
                        x2=C_V3
                        x=x*x1/x2
                else:
                    "正しく選択されていません"

                NAME=Lot+"_"+Rate[j]
                #グラフ左上
                title_size=int(d.get())
                axisN_size=int(e.get())
                axis_size=int(f.get())
                font=g.get()
                #plt.subplot(2,2,1)
                #plt.title("DOD-voltage",fontsize=title_size,fontname=font)
                #plt.plot(x,y1,color=cm2,label=NAME)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(2.95,4.5)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([3,3.2,3.4,3.6,3.8,4.0,4.2,4.4,4.5],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右上
                #plt.subplot(2,2,2)
                #plt.title("dVdQ",fontsize=title_size,fontname=font)
                #plt.plot(x,y2,color=cm2,label=NAME)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("dV/dQ[V/%]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(0,-0.05)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,-0.01,-0.02,-0.03,-0.04,-0.05],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ左下
                #plt.subplot(2,2,3)
                plt.title("delta_V",fontsize=title_size,fontname=font)
                plt.plot(x,y3,color=cm2,label=NAME)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("delta-V[mV]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(-5,505)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ右下
                #plt.subplot(2,2,4)
                #plt.title("DC-resistance",fontsize=title_size,fontname=font)
                #plt.plot(x,y4,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("DC-resistanve[mΩ]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,255)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250],fontsize=axis_size,fontname=font)
                #plt.legend()

        plt.show()
    def delta_V11():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        while color_list2.count("")>0:
            color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
                    [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
                    [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
                    [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
                    [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
                    [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
        len_Lot=len(Lot_list)#ロットのリスト長さ

    #--------------------------------------------------------------------------------------------------------------------
        #for i in range(5,6):
        for i in range(0,len_Lot):
            Rate=Rate_array[i]#ここは変える
            while Rate.count("")>0:
                Rate.remove("")
            #len_Rate=len(Rate)
            Lot=Lot_list[i]
            cm2=color_list1[i]
            C_V="Capacity_"+cut_vol+"[mAh]"
    #--------------------------------------------------------------------------------------------------------------------
            for j in range(4,5):
            #for j in range(0,len_Rate)
                rate=float(Rate[j])#レートの選択
                #cm2=color_list2[j]#行のカラー
                df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
                df3=df2[df2["Discharge-rate[C]"]==rate]#
                C_V2=df3[C_V].values#カット電圧時の容量データ
                C_V2=C_V2[0]
                Link=df3["Curve_Data_Link"].values#カーブデータのファイルを開く。
                Link=Link[0]
                DF=pd.read_csv(Link,encoding="cp932")
                x=np.array(DF["DOD[%]"].values.flatten())#x(dod)
                y1=np.array(DF["Voltage[V]"].values.flatten())#y1(vol)
                y2=np.array(DF["dVdQ[V/mAh]"].values.flatten())#y2(dVdQ)
                y3=np.array(DF["delta_V[mV]"].values.flatten())#y3(deltaV)
                y4=np.array(DF["DC_resistance[mohm]"].values.flatten())#y4(DCR)
                if(initial_dod=="DOD"):
                    pass
                elif(initial_dod=="Reference"):
                    if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        C_1C=df3["min_rated_capacity[mAh]"].values
                        x1=C_02[0]
                        x2=C_1C[0]
                        x=x*x1/x2
                    else:#0.2C容量を掛けて、各レートの容量で割る。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        DF3=df2[df2["Discharge-rate[C]"]==float(ref)]#
                        C_V3=DF3[C_V].values#カット電圧時の容量データ
                        C_V3=C_V3[0]
                        x1=C_02[0]
                        x2=C_V3
                        x=x*x1/x2
                else:
                    "正しく選択されていません"

                NAME=Lot+"_"+Rate[j]
                #グラフ左上
                title_size=int(d.get())
                axisN_size=int(e.get())
                axis_size=int(f.get())
                font=g.get()
                #plt.subplot(2,2,1)
                #plt.title("DOD-voltage",fontsize=title_size,fontname=font)
                #plt.plot(x,y1,color=cm2,label=NAME)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(2.95,4.5)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([3,3.2,3.4,3.6,3.8,4.0,4.2,4.4,4.5],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右上
                #plt.subplot(2,2,2)
                #plt.title("dVdQ",fontsize=title_size,fontname=font)
                #plt.plot(x,y2,color=cm2,label=NAME)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("dV/dQ[V/%]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(0,-0.05)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,-0.01,-0.02,-0.03,-0.04,-0.05],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ左下
                #plt.subplot(2,2,3)
                plt.title("delta_V",fontsize=title_size,fontname=font)
                plt.plot(x,y3,color=cm2,label=NAME)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("delta-V[mV]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(-5,505)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ右下
                #plt.subplot(2,2,4)
                #plt.title("DC-resistance",fontsize=title_size,fontname=font)
                #plt.plot(x,y4,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("DC-resistanve[mΩ]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,255)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250],fontsize=axis_size,fontname=font)
                #plt.legend()

        plt.show()
    def delta_V12():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        while color_list2.count("")>0:
            color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
                    [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
                    [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
                    [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
                    [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
                    [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
        len_Lot=len(Lot_list)#ロットのリスト長さ

    #--------------------------------------------------------------------------------------------------------------------
        #for i in range(5,6):
        for i in range(0,len_Lot):
            Rate=Rate_array[i]#ここは変える
            while Rate.count("")>0:
                Rate.remove("")
            #len_Rate=len(Rate)
            Lot=Lot_list[i]
            cm2=color_list1[i]
            C_V="Capacity_"+cut_vol+"[mAh]"
    #--------------------------------------------------------------------------------------------------------------------
            for j in range(5,6):
            #for j in range(0,len_Rate)
                rate=float(Rate[j])#レートの選択
                #cm2=color_list2[j]#行のカラー
                df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
                df3=df2[df2["Discharge-rate[C]"]==rate]#
                C_V2=df3[C_V].values#カット電圧時の容量データ
                C_V2=C_V2[0]
                Link=df3["Curve_Data_Link"].values#カーブデータのファイルを開く。
                Link=Link[0]
                DF=pd.read_csv(Link,encoding="cp932")
                x=np.array(DF["DOD[%]"].values.flatten())#x(dod)
                y1=np.array(DF["Voltage[V]"].values.flatten())#y1(vol)
                y2=np.array(DF["dVdQ[V/mAh]"].values.flatten())#y2(dVdQ)
                y3=np.array(DF["delta_V[mV]"].values.flatten())#y3(deltaV)
                y4=np.array(DF["DC_resistance[mohm]"].values.flatten())#y4(DCR)
                if(initial_dod=="DOD"):
                    pass
                elif(initial_dod=="Reference"):
                    if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        C_1C=df3["min_rated_capacity[mAh]"].values
                        x1=C_02[0]
                        x2=C_1C[0]
                        x=x*x1/x2
                    else:#0.2C容量を掛けて、各レートの容量で割る。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        DF3=df2[df2["Discharge-rate[C]"]==float(ref)]#
                        C_V3=DF3[C_V].values#カット電圧時の容量データ
                        C_V3=C_V3[0]
                        x1=C_02[0]
                        x2=C_V3
                        x=x*x1/x2
                else:
                    "正しく選択されていません"

                NAME=Lot+"_"+Rate[j]
                #グラフ左上
                title_size=int(d.get())
                axisN_size=int(e.get())
                axis_size=int(f.get())
                font=g.get()
                #plt.subplot(2,2,1)
                #plt.title("DOD-voltage",fontsize=title_size,fontname=font)
                #plt.plot(x,y1,color=cm2,label=NAME)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(2.95,4.5)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([3,3.2,3.4,3.6,3.8,4.0,4.2,4.4,4.5],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右上
                #plt.subplot(2,2,2)
                #plt.title("dVdQ",fontsize=title_size,fontname=font)
                #plt.plot(x,y2,color=cm2,label=NAME)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("dV/dQ[V/%]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(0,-0.05)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,-0.01,-0.02,-0.03,-0.04,-0.05],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ左下
                #plt.subplot(2,2,3)
                plt.title("delta_V",fontsize=title_size,fontname=font)
                plt.plot(x,y3,color=cm2,label=NAME)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("delta-V[mV]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(-5,505)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()
                #グラフ右下
                #plt.subplot(2,2,4)
                #plt.title("DC-resistance",fontsize=title_size,fontname=font)
                #plt.plot(x,y4,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("DC-resistanve[mΩ]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,255)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250],fontsize=axis_size,fontname=font)
                #plt.legend()

        plt.show()

    def DCR1():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        while color_list2.count("")>0:
            color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
                    [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
                    [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
                    [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
                    [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
                    [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
    #len_Lot=len(Lot_List)#ロットのリスト長さ

    #--------------------------------------------------------------------------------------------------------------------
        for i in range(0,1):
        #for i in range(0,Lot_list):
            Rate=Rate_array[i]#ここは変える
            while Rate.count("")>0:
                Rate.remove("")
            len_Rate=len(Rate)
            Lot=Lot_list[i]
            #cm1=color_list1[i]
            C_V="Capacity_"+cut_vol+"[mAh]"
    #--------------------------------------------------------------------------------------------------------------------
            for j in range(0,len_Rate):
                rate=float(Rate[j])#レートの選択
                cm2=color_list2[j]#行のカラー
                df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
                df3=df2[df2["Discharge-rate[C]"]==rate]#
                C_V2=df3[C_V].values#カット電圧時の容量データ
                C_V2=C_V2[0]
                Link=df3["Curve_Data_Link"].values#カーブデータのファイルを開く。
                Link=Link[0]
                DF=pd.read_csv(Link,encoding="cp932")
                x=np.array(DF["DOD[%]"].values.flatten())#x(dod)
                y1=np.array(DF["Voltage[V]"].values.flatten())#y1(vol)
                y2=np.array(DF["dVdQ[V/mAh]"].values.flatten())#y2(dVdQ)
                y3=np.array(DF["delta_V[mV]"].values.flatten())#y3(deltaV)
                y4=np.array(DF["DC_resistance[mohm]"].values.flatten())#y4(DCR)
                if(initial_dod=="DOD"):
                    pass
                elif(initial_dod=="Reference"):
                    if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        C_1C=df3["min_rated_capacity[mAh]"].values
                        x1=C_02[0]
                        x2=C_1C[0]
                        x=x*x1/x2
                    else:#0.2C容量を掛けて、各レートの容量で割る。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        DF3=df2[df2["Discharge-rate[C]"]==float(ref)]#
                        C_V3=DF3[C_V].values#カット電圧時の容量データ
                        C_V3=C_V3[0]
                        x1=C_02[0]
                        x2=C_V3
                        x=x*x1/x2
                else:
                    "正しく選択されていません"

                NAME=Lot+"_"+Rate[j]
                #グラフ左上
                title_size=int(d.get())
                axisN_size=int(e.get())
                axis_size=int(f.get())
                font=g.get()
                #plt.subplot(2,2,1)
                #plt.title("DOD-voltage",fontsize=title_size,fontname=font)
                #plt.plot(x,y1,color=cm2,label=NAME)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(2.95,4.5)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([3,3.2,3.4,3.6,3.8,4.0,4.2,4.4,4.5],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右上
                #plt.subplot(2,2,2)
                #plt.title("dVdQ",fontsize=title_size,fontname=font)
                #plt.plot(x,y2,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("dV/dQ[V/%]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(0,-0.05)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,-0.01,-0.02,-0.03,-0.04,-0.05],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ左下
                #plt.subplot(2,2,3)
                #plt.title("delta_V",fontsize=title_size,fontname=font)
                #plt.plot(x,y3,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("delta-V[mV]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,505)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250,300,350,400,450,500],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右下
                #plt.subplot(2,2,4)
                plt.title("DC-resistance",fontsize=title_size,fontname=font)
                plt.plot(x,y4,color=cm2,label=NAME)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("DC-resistanve[mΩ]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(-5,255)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()

        plt.show()
    def DCR2():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        while color_list2.count("")>0:
            color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
                    [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
                    [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
                    [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
                    [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
                    [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
    #len_Lot=len(Lot_List)#ロットのリスト長さ

    #--------------------------------------------------------------------------------------------------------------------
        for i in range(1,2):
        #for i in range(0,Lot_list):
            Rate=Rate_array[i]#ここは変える
            while Rate.count("")>0:
                Rate.remove("")
            len_Rate=len(Rate)
            Lot=Lot_list[i]
            #cm1=color_list1[i]
            C_V="Capacity_"+cut_vol+"[mAh]"
    #--------------------------------------------------------------------------------------------------------------------
            for j in range(0,len_Rate):
                rate=float(Rate[j])#レートの選択
                cm2=color_list2[j]#行のカラー
                df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
                df3=df2[df2["Discharge-rate[C]"]==rate]#
                C_V2=df3[C_V].values#カット電圧時の容量データ
                C_V2=C_V2[0]
                Link=df3["Curve_Data_Link"].values#カーブデータのファイルを開く。
                Link=Link[0]
                DF=pd.read_csv(Link,encoding="cp932")
                x=np.array(DF["DOD[%]"].values.flatten())#x(dod)
                y1=np.array(DF["Voltage[V]"].values.flatten())#y1(vol)
                y2=np.array(DF["dVdQ[V/mAh]"].values.flatten())#y2(dVdQ)
                y3=np.array(DF["delta_V[mV]"].values.flatten())#y3(deltaV)
                y4=np.array(DF["DC_resistance[mohm]"].values.flatten())#y4(DCR)
                if(initial_dod=="DOD"):
                    pass
                elif(initial_dod=="Reference"):
                    if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        C_1C=df3["min_rated_capacity[mAh]"].values
                        x1=C_02[0]
                        x2=C_1C[0]
                        x=x*x1/x2
                    else:#0.2C容量を掛けて、各レートの容量で割る。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        DF3=df2[df2["Discharge-rate[C]"]==float(ref)]#
                        C_V3=DF3[C_V].values#カット電圧時の容量データ
                        C_V3=C_V3[0]
                        x1=C_02[0]
                        x2=C_V3
                        x=x*x1/x2
                else:
                    "正しく選択されていません"

                NAME=Lot+"_"+Rate[j]
                #グラフ左上
                title_size=int(d.get())
                axisN_size=int(e.get())
                axis_size=int(f.get())
                font=g.get()
                #plt.subplot(2,2,1)
                #plt.title("DOD-voltage",fontsize=title_size,fontname=font)
                #plt.plot(x,y1,color=cm2,label=NAME)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(2.95,4.5)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([3,3.2,3.4,3.6,3.8,4.0,4.2,4.4,4.5],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右上
                #plt.subplot(2,2,2)
                #plt.title("dVdQ",fontsize=title_size,fontname=font)
                #plt.plot(x,y2,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("dV/dQ[V/%]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(0,-0.05)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,-0.01,-0.02,-0.03,-0.04,-0.05],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ左下
                #plt.subplot(2,2,3)
                #plt.title("delta_V",fontsize=title_size,fontname=font)
                #plt.plot(x,y3,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("delta-V[mV]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,505)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250,300,350,400,450,500],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右下
                #plt.subplot(2,2,4)
                plt.title("DC-resistance",fontsize=title_size,fontname=font)
                plt.plot(x,y4,color=cm2,label=NAME)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("DC-resistanve[mΩ]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(-5,255)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()

        plt.show()
    def DCR3():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        while color_list2.count("")>0:
            color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
                    [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
                    [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
                    [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
                    [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
                    [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
    #len_Lot=len(Lot_List)#ロットのリスト長さ

    #--------------------------------------------------------------------------------------------------------------------
        for i in range(2,3):
        #for i in range(0,Lot_list):
            Rate=Rate_array[i]#ここは変える
            while Rate.count("")>0:
                Rate.remove("")
            len_Rate=len(Rate)
            Lot=Lot_list[i]
            #cm1=color_list1[i]
            C_V="Capacity_"+cut_vol+"[mAh]"
    #--------------------------------------------------------------------------------------------------------------------
            for j in range(0,len_Rate):
                rate=float(Rate[j])#レートの選択
                cm2=color_list2[j]#行のカラー
                df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
                df3=df2[df2["Discharge-rate[C]"]==rate]#
                C_V2=df3[C_V].values#カット電圧時の容量データ
                C_V2=C_V2[0]
                Link=df3["Curve_Data_Link"].values#カーブデータのファイルを開く。
                Link=Link[0]
                DF=pd.read_csv(Link,encoding="cp932")
                x=np.array(DF["DOD[%]"].values.flatten())#x(dod)
                y1=np.array(DF["Voltage[V]"].values.flatten())#y1(vol)
                y2=np.array(DF["dVdQ[V/mAh]"].values.flatten())#y2(dVdQ)
                y3=np.array(DF["delta_V[mV]"].values.flatten())#y3(deltaV)
                y4=np.array(DF["DC_resistance[mohm]"].values.flatten())#y4(DCR)
                if(initial_dod=="DOD"):
                    pass
                elif(initial_dod=="Reference"):
                    if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        C_1C=df3["min_rated_capacity[mAh]"].values
                        x1=C_02[0]
                        x2=C_1C[0]
                        x=x*x1/x2
                    else:#0.2C容量を掛けて、各レートの容量で割る。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        DF3=df2[df2["Discharge-rate[C]"]==float(ref)]#
                        C_V3=DF3[C_V].values#カット電圧時の容量データ
                        C_V3=C_V3[0]
                        x1=C_02[0]
                        x2=C_V3
                        x=x*x1/x2
                else:
                    "正しく選択されていません"

                NAME=Lot+"_"+Rate[j]
                #グラフ左上
                title_size=int(d.get())
                axisN_size=int(e.get())
                axis_size=int(f.get())
                font=g.get()
                #plt.subplot(2,2,1)
                #plt.title("DOD-voltage",fontsize=title_size,fontname=font)
                #plt.plot(x,y1,color=cm2,label=NAME)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(2.95,4.5)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([3,3.2,3.4,3.6,3.8,4.0,4.2,4.4,4.5],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右上
                #plt.subplot(2,2,2)
                #plt.title("dVdQ",fontsize=title_size,fontname=font)
                #plt.plot(x,y2,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("dV/dQ[V/%]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(0,-0.05)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,-0.01,-0.02,-0.03,-0.04,-0.05],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ左下
                #plt.subplot(2,2,3)
                #plt.title("delta_V",fontsize=title_size,fontname=font)
                #plt.plot(x,y3,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("delta-V[mV]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,505)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250,300,350,400,450,500],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右下
                #plt.subplot(2,2,4)
                plt.title("DC-resistance",fontsize=title_size,fontname=font)
                plt.plot(x,y4,color=cm2,label=NAME)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("DC-resistanve[mΩ]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(-5,255)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()

        plt.show()
    def DCR4():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        while color_list2.count("")>0:
            color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
                    [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
                    [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
                    [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
                    [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
                    [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
    #len_Lot=len(Lot_List)#ロットのリスト長さ

    #--------------------------------------------------------------------------------------------------------------------
        for i in range(3,4):
        #for i in range(0,Lot_list):
            Rate=Rate_array[i]#ここは変える
            while Rate.count("")>0:
                Rate.remove("")
            len_Rate=len(Rate)
            Lot=Lot_list[i]
            #cm1=color_list1[i]
            C_V="Capacity_"+cut_vol+"[mAh]"
    #--------------------------------------------------------------------------------------------------------------------
            for j in range(0,len_Rate):
                rate=float(Rate[j])#レートの選択
                cm2=color_list2[j]#行のカラー
                df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
                df3=df2[df2["Discharge-rate[C]"]==rate]#
                C_V2=df3[C_V].values#カット電圧時の容量データ
                C_V2=C_V2[0]
                Link=df3["Curve_Data_Link"].values#カーブデータのファイルを開く。
                Link=Link[0]
                DF=pd.read_csv(Link,encoding="cp932")
                x=np.array(DF["DOD[%]"].values.flatten())#x(dod)
                y1=np.array(DF["Voltage[V]"].values.flatten())#y1(vol)
                y2=np.array(DF["dVdQ[V/mAh]"].values.flatten())#y2(dVdQ)
                y3=np.array(DF["delta_V[mV]"].values.flatten())#y3(deltaV)
                y4=np.array(DF["DC_resistance[mohm]"].values.flatten())#y4(DCR)
                if(initial_dod=="DOD"):
                    pass
                elif(initial_dod=="Reference"):
                    if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        C_1C=df3["min_rated_capacity[mAh]"].values
                        x1=C_02[0]
                        x2=C_1C[0]
                        x=x*x1/x2
                    else:#0.2C容量を掛けて、各レートの容量で割る。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        DF3=df2[df2["Discharge-rate[C]"]==float(ref)]#
                        C_V3=DF3[C_V].values#カット電圧時の容量データ
                        C_V3=C_V3[0]
                        x1=C_02[0]
                        x2=C_V3
                        x=x*x1/x2
                else:
                    "正しく選択されていません"

                NAME=Lot+"_"+Rate[j]
                #グラフ左上
                title_size=int(d.get())
                axisN_size=int(e.get())
                axis_size=int(f.get())
                font=g.get()
                #plt.subplot(2,2,1)
                #plt.title("DOD-voltage",fontsize=title_size,fontname=font)
                #plt.plot(x,y1,color=cm2,label=NAME)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(2.95,4.5)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([3,3.2,3.4,3.6,3.8,4.0,4.2,4.4,4.5],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右上
                #plt.subplot(2,2,2)
                #plt.title("dVdQ",fontsize=title_size,fontname=font)
                #plt.plot(x,y2,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("dV/dQ[V/%]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(0,-0.05)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,-0.01,-0.02,-0.03,-0.04,-0.05],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ左下
                #plt.subplot(2,2,3)
                #plt.title("delta_V",fontsize=title_size,fontname=font)
                #plt.plot(x,y3,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("delta-V[mV]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,505)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250,300,350,400,450,500],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右下
                #plt.subplot(2,2,4)
                plt.title("DC-resistance",fontsize=title_size,fontname=font)
                plt.plot(x,y4,color=cm2,label=NAME)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("DC-resistanve[mΩ]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(-5,255)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()

        plt.show()
    def DCR5():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        while color_list2.count("")>0:
            color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
                    [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
                    [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
                    [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
                    [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
                    [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
    #len_Lot=len(Lot_List)#ロットのリスト長さ

    #--------------------------------------------------------------------------------------------------------------------
        for i in range(4,5):
        #for i in range(0,Lot_list):
            Rate=Rate_array[i]#ここは変える
            while Rate.count("")>0:
                Rate.remove("")
            len_Rate=len(Rate)
            Lot=Lot_list[i]
            #cm1=color_list1[i]
            C_V="Capacity_"+cut_vol+"[mAh]"
    #--------------------------------------------------------------------------------------------------------------------
            for j in range(0,len_Rate):
                rate=float(Rate[j])#レートの選択
                cm2=color_list2[j]#行のカラー
                df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
                df3=df2[df2["Discharge-rate[C]"]==rate]#
                C_V2=df3[C_V].values#カット電圧時の容量データ
                C_V2=C_V2[0]
                Link=df3["Curve_Data_Link"].values#カーブデータのファイルを開く。
                Link=Link[0]
                DF=pd.read_csv(Link,encoding="cp932")
                x=np.array(DF["DOD[%]"].values.flatten())#x(dod)
                y1=np.array(DF["Voltage[V]"].values.flatten())#y1(vol)
                y2=np.array(DF["dVdQ[V/mAh]"].values.flatten())#y2(dVdQ)
                y3=np.array(DF["delta_V[mV]"].values.flatten())#y3(deltaV)
                y4=np.array(DF["DC_resistance[mohm]"].values.flatten())#y4(DCR)
                if(initial_dod=="DOD"):
                    pass
                elif(initial_dod=="Reference"):
                    if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        C_1C=df3["min_rated_capacity[mAh]"].values
                        x1=C_02[0]
                        x2=C_1C[0]
                        x=x*x1/x2
                    else:#0.2C容量を掛けて、各レートの容量で割る。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        DF3=df2[df2["Discharge-rate[C]"]==float(ref)]#
                        C_V3=DF3[C_V].values#カット電圧時の容量データ
                        C_V3=C_V3[0]
                        x1=C_02[0]
                        x2=C_V3
                        x=x*x1/x2
                else:
                    "正しく選択されていません"

                NAME=Lot+"_"+Rate[j]
                #グラフ左上
                title_size=int(d.get())
                axisN_size=int(e.get())
                axis_size=int(f.get())
                font=g.get()
                #plt.subplot(2,2,1)
                #plt.title("DOD-voltage",fontsize=title_size,fontname=font)
                #plt.plot(x,y1,color=cm2,label=NAME)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(2.95,4.5)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([3,3.2,3.4,3.6,3.8,4.0,4.2,4.4,4.5],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右上
                #plt.subplot(2,2,2)
                #plt.title("dVdQ",fontsize=title_size,fontname=font)
                #plt.plot(x,y2,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("dV/dQ[V/%]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(0,-0.05)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,-0.01,-0.02,-0.03,-0.04,-0.05],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ左下
                #plt.subplot(2,2,3)
                #plt.title("delta_V",fontsize=title_size,fontname=font)
                #plt.plot(x,y3,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("delta-V[mV]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,505)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250,300,350,400,450,500],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右下
                #plt.subplot(2,2,4)
                plt.title("DC-resistance",fontsize=title_size,fontname=font)
                plt.plot(x,y4,color=cm2,label=NAME)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("DC-resistanve[mΩ]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(-5,255)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()

        plt.show()
    def DCR6():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        while color_list2.count("")>0:
            color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
                    [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
                    [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
                    [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
                    [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
                    [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
    #len_Lot=len(Lot_List)#ロットのリスト長さ

    #--------------------------------------------------------------------------------------------------------------------
        for i in range(5,6):
        #for i in range(0,Lot_list):
            Rate=Rate_array[i]#ここは変える
            while Rate.count("")>0:
                Rate.remove("")
            len_Rate=len(Rate)
            Lot=Lot_list[i]
            #cm1=color_list1[i]
            C_V="Capacity_"+cut_vol+"[mAh]"
    #--------------------------------------------------------------------------------------------------------------------
            for j in range(0,len_Rate):
                rate=float(Rate[j])#レートの選択
                cm2=color_list2[j]#行のカラー
                df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
                df3=df2[df2["Discharge-rate[C]"]==rate]#
                C_V2=df3[C_V].values#カット電圧時の容量データ
                C_V2=C_V2[0]
                Link=df3["Curve_Data_Link"].values#カーブデータのファイルを開く。
                Link=Link[0]
                DF=pd.read_csv(Link,encoding="cp932")
                x=np.array(DF["DOD[%]"].values.flatten())#x(dod)
                y1=np.array(DF["Voltage[V]"].values.flatten())#y1(vol)
                y2=np.array(DF["dVdQ[V/mAh]"].values.flatten())#y2(dVdQ)
                y3=np.array(DF["delta_V[mV]"].values.flatten())#y3(deltaV)
                y4=np.array(DF["DC_resistance[mohm]"].values.flatten())#y4(DCR)
                if(initial_dod=="DOD"):
                    pass
                elif(initial_dod=="Reference"):
                    if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        C_1C=df3["min_rated_capacity[mAh]"].values
                        x1=C_02[0]
                        x2=C_1C[0]
                        x=x*x1/x2
                    else:#0.2C容量を掛けて、各レートの容量で割る。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        DF3=df2[df2["Discharge-rate[C]"]==float(ref)]#
                        C_V3=DF3[C_V].values#カット電圧時の容量データ
                        C_V3=C_V3[0]
                        x1=C_02[0]
                        x2=C_V3
                        x=x*x1/x2
                else:
                    "正しく選択されていません"

                NAME=Lot+"_"+Rate[j]
                #グラフ左上
                title_size=int(d.get())
                axisN_size=int(e.get())
                axis_size=int(f.get())
                font=g.get()
                #plt.subplot(2,2,1)
                #plt.title("DOD-voltage",fontsize=title_size,fontname=font)
                #plt.plot(x,y1,color=cm2,label=NAME)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(2.95,4.5)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([3,3.2,3.4,3.6,3.8,4.0,4.2,4.4,4.5],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右上
                #plt.subplot(2,2,2)
                #plt.title("dVdQ",fontsize=title_size,fontname=font)
                #plt.plot(x,y2,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("dV/dQ[V/%]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(0,-0.05)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,-0.01,-0.02,-0.03,-0.04,-0.05],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ左下
                #plt.subplot(2,2,3)
                #plt.title("delta_V",fontsize=title_size,fontname=font)
                #plt.plot(x,y3,color=cm2)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("delta-V[mV]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,505)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250,300,350,400,450,500],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右下
                #plt.subplot(2,2,4)
                plt.title("DC-resistance",fontsize=title_size,fontname=font)
                plt.plot(x,y4,color=cm2,label=NAME)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("DC-resistanve[mΩ]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(-5,255)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()

        plt.show()
    def DCR7():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        while color_list2.count("")>0:
            color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
                    [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
                    [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
                    [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
                    [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
                    [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
        len_Lot=len(Lot_list)#ロットのリスト長さ

    #--------------------------------------------------------------------------------------------------------------------
        #for i in range(5,6):
        for i in range(0,len_Lot):
            Rate=Rate_array[i]#ここは変える
            while Rate.count("")>0:
                Rate.remove("")
            #len_Rate=len(Rate)
            Lot=Lot_list[i]
            cm2=color_list1[i]
            C_V="Capacity_"+cut_vol+"[mAh]"
    #--------------------------------------------------------------------------------------------------------------------
            for j in range(0,1):
            #for j in range(0,len_Rate)
                rate=float(Rate[j])#レートの選択
                #cm2=color_list2[j]#行のカラー
                df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
                df3=df2[df2["Discharge-rate[C]"]==rate]#
                C_V2=df3[C_V].values#カット電圧時の容量データ
                C_V2=C_V2[0]
                Link=df3["Curve_Data_Link"].values#カーブデータのファイルを開く。
                Link=Link[0]
                DF=pd.read_csv(Link,encoding="cp932")
                x=np.array(DF["DOD[%]"].values.flatten())#x(dod)
                y1=np.array(DF["Voltage[V]"].values.flatten())#y1(vol)
                y2=np.array(DF["dVdQ[V/mAh]"].values.flatten())#y2(dVdQ)
                y3=np.array(DF["delta_V[mV]"].values.flatten())#y3(deltaV)
                y4=np.array(DF["DC_resistance[mohm]"].values.flatten())#y4(DCR)
                if(initial_dod=="DOD"):
                    pass
                elif(initial_dod=="Reference"):
                    if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        C_1C=df3["min_rated_capacity[mAh]"].values
                        x1=C_02[0]
                        x2=C_1C[0]
                        x=x*x1/x2
                    else:#0.2C容量を掛けて、各レートの容量で割る。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        DF3=df2[df2["Discharge-rate[C]"]==float(ref)]#
                        C_V3=DF3[C_V].values#カット電圧時の容量データ
                        C_V3=C_V3[0]
                        x1=C_02[0]
                        x2=C_V3
                        x=x*x1/x2
                else:
                    "正しく選択されていません"

                NAME=Lot+"_"+Rate[j]
                #グラフ左上
                title_size=int(d.get())
                axisN_size=int(e.get())
                axis_size=int(f.get())
                font=g.get()
                #plt.subplot(2,2,1)
                #plt.title("DOD-voltage",fontsize=title_size,fontname=font)
                #plt.plot(x,y1,color=cm2,label=NAME)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(2.95,4.5)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([3,3.2,3.4,3.6,3.8,4.0,4.2,4.4,4.5],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右上
                #plt.subplot(2,2,2)
                #plt.title("dVdQ",fontsize=title_size,fontname=font)
                #plt.plot(x,y2,color=cm2,label=NAME)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("dV/dQ[V/%]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(0,-0.05)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,-0.01,-0.02,-0.03,-0.04,-0.05],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ左下
                #plt.subplot(2,2,3)
                #plt.title("delta_V",fontsize=title_size,fontname=font)
                #plt.plot(x,y3,color=cm2,label=NAME)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("delta-V[mV]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,505)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250,300,350,400,450,500],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右下
                #plt.subplot(2,2,4)
                plt.title("DC-resistance",fontsize=title_size,fontname=font)
                plt.plot(x,y4,color=cm2,label=NAME)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("DC-resistanve[mΩ]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(-5,255)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()

        plt.show()
    def DCR8():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        while color_list2.count("")>0:
            color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
                    [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
                    [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
                    [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
                    [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
                    [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
        len_Lot=len(Lot_list)#ロットのリスト長さ

    #--------------------------------------------------------------------------------------------------------------------
        #for i in range(5,6):
        for i in range(0,len_Lot):
            Rate=Rate_array[i]#ここは変える
            while Rate.count("")>0:
                Rate.remove("")
            #len_Rate=len(Rate)
            Lot=Lot_list[i]
            cm2=color_list1[i]
            C_V="Capacity_"+cut_vol+"[mAh]"
    #--------------------------------------------------------------------------------------------------------------------
            for j in range(1,2):
            #for j in range(0,len_Rate)
                rate=float(Rate[j])#レートの選択
                #cm2=color_list2[j]#行のカラー
                df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
                df3=df2[df2["Discharge-rate[C]"]==rate]#
                C_V2=df3[C_V].values#カット電圧時の容量データ
                C_V2=C_V2[0]
                Link=df3["Curve_Data_Link"].values#カーブデータのファイルを開く。
                Link=Link[0]
                DF=pd.read_csv(Link,encoding="cp932")
                x=np.array(DF["DOD[%]"].values.flatten())#x(dod)
                y1=np.array(DF["Voltage[V]"].values.flatten())#y1(vol)
                y2=np.array(DF["dVdQ[V/mAh]"].values.flatten())#y2(dVdQ)
                y3=np.array(DF["delta_V[mV]"].values.flatten())#y3(deltaV)
                y4=np.array(DF["DC_resistance[mohm]"].values.flatten())#y4(DCR)
                if(initial_dod=="DOD"):
                    pass
                elif(initial_dod=="Reference"):
                    if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        C_1C=df3["min_rated_capacity[mAh]"].values
                        x1=C_02[0]
                        x2=C_1C[0]
                        x=x*x1/x2
                    else:#0.2C容量を掛けて、各レートの容量で割る。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        DF3=df2[df2["Discharge-rate[C]"]==float(ref)]#
                        C_V3=DF3[C_V].values#カット電圧時の容量データ
                        C_V3=C_V3[0]
                        x1=C_02[0]
                        x2=C_V3
                        x=x*x1/x2
                else:
                    "正しく選択されていません"

                NAME=Lot+"_"+Rate[j]
                #グラフ左上
                title_size=int(d.get())
                axisN_size=int(e.get())
                axis_size=int(f.get())
                font=g.get()
                #plt.subplot(2,2,1)
                #plt.title("DOD-voltage",fontsize=title_size,fontname=font)
                #plt.plot(x,y1,color=cm2,label=NAME)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(2.95,4.5)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([3,3.2,3.4,3.6,3.8,4.0,4.2,4.4,4.5],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右上
                #plt.subplot(2,2,2)
                #plt.title("dVdQ",fontsize=title_size,fontname=font)
                #plt.plot(x,y2,color=cm2,label=NAME)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("dV/dQ[V/%]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(0,-0.05)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,-0.01,-0.02,-0.03,-0.04,-0.05],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ左下
                #plt.subplot(2,2,3)
                #plt.title("delta_V",fontsize=title_size,fontname=font)
                #plt.plot(x,y3,color=cm2,label=NAME)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("delta-V[mV]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,505)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250,300,350,400,450,500],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右下
                #plt.subplot(2,2,4)
                plt.title("DC-resistance",fontsize=title_size,fontname=font)
                plt.plot(x,y4,color=cm2,label=NAME)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("DC-resistanve[mΩ]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(-5,255)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()

        plt.show()
    def DCR9():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        while color_list2.count("")>0:
            color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
                    [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
                    [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
                    [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
                    [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
                    [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
        len_Lot=len(Lot_list)#ロットのリスト長さ

    #--------------------------------------------------------------------------------------------------------------------
        #for i in range(5,6):
        for i in range(0,len_Lot):
            Rate=Rate_array[i]#ここは変える
            while Rate.count("")>0:
                Rate.remove("")
            #len_Rate=len(Rate)
            Lot=Lot_list[i]
            cm2=color_list1[i]
            C_V="Capacity_"+cut_vol+"[mAh]"
    #--------------------------------------------------------------------------------------------------------------------
            for j in range(2,3):
            #for j in range(0,len_Rate)
                rate=float(Rate[j])#レートの選択
                #cm2=color_list2[j]#行のカラー
                df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
                df3=df2[df2["Discharge-rate[C]"]==rate]#
                C_V2=df3[C_V].values#カット電圧時の容量データ
                C_V2=C_V2[0]
                Link=df3["Curve_Data_Link"].values#カーブデータのファイルを開く。
                Link=Link[0]
                DF=pd.read_csv(Link,encoding="cp932")
                x=np.array(DF["DOD[%]"].values.flatten())#x(dod)
                y1=np.array(DF["Voltage[V]"].values.flatten())#y1(vol)
                y2=np.array(DF["dVdQ[V/mAh]"].values.flatten())#y2(dVdQ)
                y3=np.array(DF["delta_V[mV]"].values.flatten())#y3(deltaV)
                y4=np.array(DF["DC_resistance[mohm]"].values.flatten())#y4(DCR)
                if(initial_dod=="DOD"):
                    pass
                elif(initial_dod=="Reference"):
                    if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        C_1C=df3["min_rated_capacity[mAh]"].values
                        x1=C_02[0]
                        x2=C_1C[0]
                        x=x*x1/x2
                    else:#0.2C容量を掛けて、各レートの容量で割る。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        DF3=df2[df2["Discharge-rate[C]"]==float(ref)]#
                        C_V3=DF3[C_V].values#カット電圧時の容量データ
                        C_V3=C_V3[0]
                        x1=C_02[0]
                        x2=C_V3
                        x=x*x1/x2
                else:
                    "正しく選択されていません"

                NAME=Lot+"_"+Rate[j]
                #グラフ左上
                title_size=int(d.get())
                axisN_size=int(e.get())
                axis_size=int(f.get())
                font=g.get()
                #plt.subplot(2,2,1)
                #plt.title("DOD-voltage",fontsize=title_size,fontname=font)
                #plt.plot(x,y1,color=cm2,label=NAME)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(2.95,4.5)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([3,3.2,3.4,3.6,3.8,4.0,4.2,4.4,4.5],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右上
                #plt.subplot(2,2,2)
                #plt.title("dVdQ",fontsize=title_size,fontname=font)
                #plt.plot(x,y2,color=cm2,label=NAME)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("dV/dQ[V/%]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(0,-0.05)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,-0.01,-0.02,-0.03,-0.04,-0.05],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ左下
                #plt.subplot(2,2,3)
                #plt.title("delta_V",fontsize=title_size,fontname=font)
                #plt.plot(x,y3,color=cm2,label=NAME)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("delta-V[mV]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,505)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250,300,350,400,450,500],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右下
                #plt.subplot(2,2,4)
                plt.title("DC-resistance",fontsize=title_size,fontname=font)
                plt.plot(x,y4,color=cm2,label=NAME)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("DC-resistanve[mΩ]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(-5,255)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()

        plt.show()
    def DCR10():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        while color_list2.count("")>0:
            color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
                    [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
                    [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
                    [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
                    [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
                    [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
        len_Lot=len(Lot_list)#ロットのリスト長さ

    #--------------------------------------------------------------------------------------------------------------------
        #for i in range(5,6):
        for i in range(0,len_Lot):
            Rate=Rate_array[i]#ここは変える
            while Rate.count("")>0:
                Rate.remove("")
            #len_Rate=len(Rate)
            Lot=Lot_list[i]
            cm2=color_list1[i]
            C_V="Capacity_"+cut_vol+"[mAh]"
    #--------------------------------------------------------------------------------------------------------------------
            for j in range(3,4):
            #for j in range(0,len_Rate)
                rate=float(Rate[j])#レートの選択
                #cm2=color_list2[j]#行のカラー
                df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
                df3=df2[df2["Discharge-rate[C]"]==rate]#
                C_V2=df3[C_V].values#カット電圧時の容量データ
                C_V2=C_V2[0]
                Link=df3["Curve_Data_Link"].values#カーブデータのファイルを開く。
                Link=Link[0]
                DF=pd.read_csv(Link,encoding="cp932")
                x=np.array(DF["DOD[%]"].values.flatten())#x(dod)
                y1=np.array(DF["Voltage[V]"].values.flatten())#y1(vol)
                y2=np.array(DF["dVdQ[V/mAh]"].values.flatten())#y2(dVdQ)
                y3=np.array(DF["delta_V[mV]"].values.flatten())#y3(deltaV)
                y4=np.array(DF["DC_resistance[mohm]"].values.flatten())#y4(DCR)
                if(initial_dod=="DOD"):
                    pass
                elif(initial_dod=="Reference"):
                    if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        C_1C=df3["min_rated_capacity[mAh]"].values
                        x1=C_02[0]
                        x2=C_1C[0]
                        x=x*x1/x2
                    else:#0.2C容量を掛けて、各レートの容量で割る。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        DF3=df2[df2["Discharge-rate[C]"]==float(ref)]#
                        C_V3=DF3[C_V].values#カット電圧時の容量データ
                        C_V3=C_V3[0]
                        x1=C_02[0]
                        x2=C_V3
                        x=x*x1/x2
                else:
                    "正しく選択されていません"

                NAME=Lot+"_"+Rate[j]
                #グラフ左上
                title_size=int(d.get())
                axisN_size=int(e.get())
                axis_size=int(f.get())
                font=g.get()
                #plt.subplot(2,2,1)
                #plt.title("DOD-voltage",fontsize=title_size,fontname=font)
                #plt.plot(x,y1,color=cm2,label=NAME)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(2.95,4.5)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([3,3.2,3.4,3.6,3.8,4.0,4.2,4.4,4.5],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右上
                #plt.subplot(2,2,2)
                #plt.title("dVdQ",fontsize=title_size,fontname=font)
                #plt.plot(x,y2,color=cm2,label=NAME)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("dV/dQ[V/%]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(0,-0.05)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,-0.01,-0.02,-0.03,-0.04,-0.05],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ左下
                #plt.subplot(2,2,3)
                #plt.title("delta_V",fontsize=title_size,fontname=font)
                #plt.plot(x,y3,color=cm2,label=NAME)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("delta-V[mV]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,505)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250,300,350,400,450,500],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右下
                #plt.subplot(2,2,4)
                plt.title("DC-resistance",fontsize=title_size,fontname=font)
                plt.plot(x,y4,color=cm2,label=NAME)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("DC-resistanve[mΩ]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(-5,255)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()

        plt.show()
    def DCR11():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        while color_list2.count("")>0:
            color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
                    [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
                    [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
                    [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
                    [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
                    [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
        len_Lot=len(Lot_list)#ロットのリスト長さ

    #--------------------------------------------------------------------------------------------------------------------
        #for i in range(5,6):
        for i in range(0,len_Lot):
            Rate=Rate_array[i]#ここは変える
            while Rate.count("")>0:
                Rate.remove("")
            #len_Rate=len(Rate)
            Lot=Lot_list[i]
            cm2=color_list1[i]
            C_V="Capacity_"+cut_vol+"[mAh]"
    #--------------------------------------------------------------------------------------------------------------------
            for j in range(4,5):
            #for j in range(0,len_Rate)
                rate=float(Rate[j])#レートの選択
                #cm2=color_list2[j]#行のカラー
                df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
                df3=df2[df2["Discharge-rate[C]"]==rate]#
                C_V2=df3[C_V].values#カット電圧時の容量データ
                C_V2=C_V2[0]
                Link=df3["Curve_Data_Link"].values#カーブデータのファイルを開く。
                Link=Link[0]
                DF=pd.read_csv(Link,encoding="cp932")
                x=np.array(DF["DOD[%]"].values.flatten())#x(dod)
                y1=np.array(DF["Voltage[V]"].values.flatten())#y1(vol)
                y2=np.array(DF["dVdQ[V/mAh]"].values.flatten())#y2(dVdQ)
                y3=np.array(DF["delta_V[mV]"].values.flatten())#y3(deltaV)
                y4=np.array(DF["DC_resistance[mohm]"].values.flatten())#y4(DCR)
                if(initial_dod=="DOD"):
                    pass
                elif(initial_dod=="Reference"):
                    if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        C_1C=df3["min_rated_capacity[mAh]"].values
                        x1=C_02[0]
                        x2=C_1C[0]
                        x=x*x1/x2
                    else:#0.2C容量を掛けて、各レートの容量で割る。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        DF3=df2[df2["Discharge-rate[C]"]==float(ref)]#
                        C_V3=DF3[C_V].values#カット電圧時の容量データ
                        C_V3=C_V3[0]
                        x1=C_02[0]
                        x2=C_V3
                        x=x*x1/x2
                else:
                    "正しく選択されていません"

                NAME=Lot+"_"+Rate[j]
                #グラフ左上
                title_size=int(d.get())
                axisN_size=int(e.get())
                axis_size=int(f.get())
                font=g.get()
                #plt.subplot(2,2,1)
                #plt.title("DOD-voltage",fontsize=title_size,fontname=font)
                #plt.plot(x,y1,color=cm2,label=NAME)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(2.95,4.5)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([3,3.2,3.4,3.6,3.8,4.0,4.2,4.4,4.5],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右上
                #plt.subplot(2,2,2)
                #plt.title("dVdQ",fontsize=title_size,fontname=font)
                #plt.plot(x,y2,color=cm2,label=NAME)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("dV/dQ[V/%]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(0,-0.05)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,-0.01,-0.02,-0.03,-0.04,-0.05],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ左下
                #plt.subplot(2,2,3)
                #plt.title("delta_V",fontsize=title_size,fontname=font)
                #plt.plot(x,y3,color=cm2,label=NAME)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("delta-V[mV]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,505)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250,300,350,400,450,500],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右下
                #plt.subplot(2,2,4)
                plt.title("DC-resistance",fontsize=title_size,fontname=font)
                plt.plot(x,y4,color=cm2,label=NAME)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("DC-resistanve[mΩ]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(-5,255)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()

        plt.show()
    def DCR12():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        while color_list2.count("")>0:
            color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
                    [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
                    [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
                    [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
                    [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
                    [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
        len_Lot=len(Lot_list)#ロットのリスト長さ

    #--------------------------------------------------------------------------------------------------------------------
        #for i in range(5,6):
        for i in range(0,len_Lot):
            Rate=Rate_array[i]#ここは変える
            while Rate.count("")>0:
                Rate.remove("")
            #len_Rate=len(Rate)
            Lot=Lot_list[i]
            cm2=color_list1[i]
            C_V="Capacity_"+cut_vol+"[mAh]"
    #--------------------------------------------------------------------------------------------------------------------
            for j in range(5,6):
            #for j in range(0,len_Rate)
                rate=float(Rate[j])#レートの選択
                #cm2=color_list2[j]#行のカラー
                df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
                df3=df2[df2["Discharge-rate[C]"]==rate]#
                C_V2=df3[C_V].values#カット電圧時の容量データ
                C_V2=C_V2[0]
                Link=df3["Curve_Data_Link"].values#カーブデータのファイルを開く。
                Link=Link[0]
                DF=pd.read_csv(Link,encoding="cp932")
                x=np.array(DF["DOD[%]"].values.flatten())#x(dod)
                y1=np.array(DF["Voltage[V]"].values.flatten())#y1(vol)
                y2=np.array(DF["dVdQ[V/mAh]"].values.flatten())#y2(dVdQ)
                y3=np.array(DF["delta_V[mV]"].values.flatten())#y3(deltaV)
                y4=np.array(DF["DC_resistance[mohm]"].values.flatten())#y4(DCR)
                if(initial_dod=="DOD"):
                    pass
                elif(initial_dod=="Reference"):
                    if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        C_1C=df3["min_rated_capacity[mAh]"].values
                        x1=C_02[0]
                        x2=C_1C[0]
                        x=x*x1/x2
                    else:#0.2C容量を掛けて、各レートの容量で割る。
                        C2_V2="Capacity_3.0V[mAh]"
                        C_02=df3[C2_V2].values#カット電圧時の容量データ
                        DF3=df2[df2["Discharge-rate[C]"]==float(ref)]#
                        C_V3=DF3[C_V].values#カット電圧時の容量データ
                        C_V3=C_V3[0]
                        x1=C_02[0]
                        x2=C_V3
                        x=x*x1/x2
                else:
                    "正しく選択されていません"

                NAME=Lot+"_"+Rate[j]
                #グラフ左上
                title_size=int(d.get())
                axisN_size=int(e.get())
                axis_size=int(f.get())
                font=g.get()
                #plt.subplot(2,2,1)
                #plt.title("DOD-voltage",fontsize=title_size,fontname=font)
                #plt.plot(x,y1,color=cm2,label=NAME)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(2.95,4.5)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([3,3.2,3.4,3.6,3.8,4.0,4.2,4.4,4.5],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右上
                #plt.subplot(2,2,2)
                #plt.title("dVdQ",fontsize=title_size,fontname=font)
                #plt.plot(x,y2,color=cm2,label=NAME)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("dV/dQ[V/%]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(0,-0.05)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,-0.01,-0.02,-0.03,-0.04,-0.05],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ左下
                #plt.subplot(2,2,3)
                #plt.title("delta_V",fontsize=title_size,fontname=font)
                #plt.plot(x,y3,color=cm2,label=NAME)
                #plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                #plt.ylabel("delta-V[mV]",fontsize=axisN_size,fontname=font)
                #plt.xlim(-5,105)
                #plt.ylim(-5,505)
                #plt.xticks([0,10,20,30,40,50,60,70,80,90,100],fontsize=axis_size,fontname=font)
                #plt.yticks([0,50,100,150,200,250,300,350,400,450,500],fontsize=axis_size,fontname=font)
                #plt.legend()
                #グラフ右下
                #plt.subplot(2,2,4)
                plt.title("DC-resistance",fontsize=title_size,fontname=font)
                plt.plot(x,y4,color=cm2,label=NAME)
                plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
                plt.ylabel("DC-resistanve[mΩ]",fontsize=axisN_size,fontname=font)
                plt.xlim(-5,105)
                plt.ylim(-5,255)
                plt.xticks(fontsize=axis_size,fontname=font)
                plt.yticks(fontsize=axis_size,fontname=font)
                plt.legend()

        plt.show()

    def capa():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        #initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        #color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        #while color_list2.count("")>0:
        #    color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        #Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
        #            [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
        #            [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
        #            [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
        #            [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
        #            [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
        len_Lot=len(Lot_list)#ロットのリスト長さ
    #--------------------------------------------------------------------------------------------------------------------
        for i in range(0,len_Lot):
            cm2=color_list1[i]
            df2=df[df["Cell-Lot"]==Lot_list[i]]
            C_V="Capacity_"+cut_vol+"[mAh]"
            capa=np.array(df2[C_V].values.flatten())
            rate=np.array(df2["Discharge-rate[C]"].values.flatten())
            if(ref=="min_rated_capacity"):
                ref_capa=df2["min_rated_capacity[mAh]"].values
                ref_capa=ref_capa[0]
            else:
                df3=df2[df2["Discharge-rate[C]"]==float(ref)]
                ref_capa=np.array(df3[C_V].values.flatten())
                ref_capa=ref_capa[0]
            x=rate
            y=capa/ref_capa*100
            NAME=Lot_list[i]
            title_size=int(d.get())
            axisN_size=int(e.get())
            axis_size=int(f.get())
            font=g.get()
            plt.title("Capacity",fontsize=title_size,fontname=font)
            plt.plot(x,y,color=cm2,label=NAME,marker="o",mec=cm2,mew=3)
            plt.xlabel("Discharge-rate",fontsize=axisN_size,fontname=font)
            plt.ylabel("Capacity-retention[%]",fontsize=axisN_size,fontname=font)
            plt.xlim(-0.1,2.1)
            plt.ylim(65,105)
            plt.xticks(fontsize=axis_size,fontname=font)
            plt.yticks(fontsize=axis_size,fontname=font)
            plt.legend()
        plt.show()

    def ene():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        #initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        #color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        #while color_list2.count("")>0:
        #    color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        #Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
        #            [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
        #            [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
        #            [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
        #            [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
        #            [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
        len_Lot=len(Lot_list)#ロットのリスト長さ
    #--------------------------------------------------------------------------------------------------------------------
        for i in range(0,len_Lot):
            cm2=color_list1[i]
            df2=df[df["Cell-Lot"]==Lot_list[i]]
            E_V="Energy_"+cut_vol+"[Wh]"
            capa=np.array(df2[E_V].values.flatten())
            rate=np.array(df2["Discharge-rate[C]"].values.flatten())
            if(ref=="min_rated_capacity"):
                ref_capa=df2["min_rated_Energy[Wh]"].values
                ref_capa=ref_capa[0]
            else:
                df3=df2[df2["Discharge-rate[C]"]==float(ref)]
                ref_capa=np.array(df3[E_V].values.flatten())
                ref_capa=ref_capa[0]
            x=rate
            y=capa/ref_capa*100
            NAME=Lot_list[i]
            title_size=int(d.get())
            axisN_size=int(e.get())
            axis_size=int(f.get())
            font=g.get()
            plt.title("Energy",fontsize=title_size,fontname=font)
            plt.plot(x,y,color=cm2,label=NAME,marker="o",mec=cm2,mew=3)
            plt.xlabel("Discharge-rate",fontsize=axisN_size,fontname=font)
            plt.ylabel("Energy-retention[%]",fontsize=axisN_size,fontname=font)
            plt.xlim(-0.1,2.1)
            plt.ylim(65,105)
            plt.xticks(fontsize=axis_size,fontname=font)
            plt.yticks(fontsize=axis_size,fontname=font)
            plt.legend()
        plt.show()

    def Lot_curve():
    #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        #color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        #while color_list2.count("")>0:
        #    color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        #Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
        #            [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
        #            [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
        #            [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
        #            [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
        #            [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
        len_Lot=len(Lot_list)#ロットのリスト長さ
    #--------------------------------------------------------------------------------------------------------------------
        for i in range(0,len_Lot):
            Lot=Lot_list[i]
            cm2=color_list1[i]
            C_V=Lot_list[i]
            df2=df[df["Cell-Lot"]==Lot]#ロットのデータを取得
            C_V="Capacity_"+cut_vol+"[mAh]"
            df3_1=df2[df2["Discharge-rate[C]"]==0.1]#カーブデータのファイルを開く。
            df3_2=df2[df2["Discharge-rate[C]"]==0.2]#カーブデータのファイルを開く
            df3_3=df2[df2["Discharge-rate[C]"]==0.5]#カーブデータのファイルを開く
            df3_4=df2[df2["Discharge-rate[C]"]==1.0]#カーブデータのファイルを開く
            df3_5=df2[df2["Discharge-rate[C]"]==1.5]#カーブデータのファイルを開く
            df3_6=df2[df2["Discharge-rate[C]"]==2.0]#カーブデータのファイルを開く
            Link1=df3_1["Curve_Data_Link"].values
            Link2=df3_2["Curve_Data_Link"].values
            Link3=df3_3["Curve_Data_Link"].values
            Link4=df3_4["Curve_Data_Link"].values
            Link5=df3_5["Curve_Data_Link"].values
            Link6=df3_6["Curve_Data_Link"].values
            Link1=Link1[0]
            Link2=Link2[0]
            Link3=Link3[0]
            Link4=Link4[0]
            Link5=Link5[0]
            Link6=Link6[0]
            DF1=pd.read_csv(Link1,encoding="cp932")
            DF2=pd.read_csv(Link2,encoding="cp932")
            DF3=pd.read_csv(Link3,encoding="cp932")
            DF4=pd.read_csv(Link4,encoding="cp932")
            DF5=pd.read_csv(Link5,encoding="cp932")
            DF6=pd.read_csv(Link6,encoding="cp932")
            NAME=Lot
            NAME1="0.1C"
            NAME2="0.2C"
            NAME3="0.5C"
            NAME4="1.0C"
            NAME5="1.5C"
            NAME6="2.0C"
            title_size=int(d.get())
            axisN_size=int(e.get())
            axis_size=int(f.get())
            font=g.get()
            x=np.array(DF1["DOD[%]"].values.flatten())#x(dod)
            if(initial_dod=="DOD"):
                x1=x
                x2=x
                x3=x
                x4=x
                x5=x
                x6=x
            elif(initial_dod=="Reference"):
                if(ref=="min_rated_capacity"):#0.2C容量を掛けて、1C容量でわる。
                    C2_V2="Capacity_3.0V[mAh]"
                    C_02_1=df3_1[C2_V2].values#カット電圧時の容量データ
                    C_02_2=df3_2[C2_V2].values#カット電圧時の容量データ
                    C_02_3=df3_3[C2_V2].values#カット電圧時の容量データ
                    C_02_4=df3_4[C2_V2].values#カット電圧時の容量データ
                    C_02_5=df3_5[C2_V2].values#カット電圧時の容量データ
                    C_02_6=df3_6[C2_V2].values#カット電圧時の容量データ

                    C_1C_1=df3_1["min_rated_capacity[mAh]"].values
                    C_1C_2=df3_2["min_rated_capacity[mAh]"].values
                    C_1C_3=df3_3["min_rated_capacity[mAh]"].values
                    C_1C_4=df3_4["min_rated_capacity[mAh]"].values
                    C_1C_5=df3_5["min_rated_capacity[mAh]"].values
                    C_1C_6=df3_6["min_rated_capacity[mAh]"].values

                    x1_1=C_02_1[0]
                    x1_2=C_02_2[0]
                    x1_3=C_02_3[0]
                    x1_4=C_02_4[0]
                    x1_5=C_02_5[0]
                    x1_6=C_02_6[0]

                    x2_1=C_1C_1[0]
                    x2_2=C_1C_2[0]
                    x2_3=C_1C_3[0]
                    x2_4=C_1C_4[0]
                    x2_5=C_1C_5[0]
                    x2_6=C_1C_6[0]

                    x1=x*x1_1/x2_1
                    x2=x*x1_2/x2_2
                    x3=x*x1_3/x2_3
                    x4=x*x1_4/x2_4
                    x5=x*x1_5/x2_5
                    x6=x*x1_6/x2_6
                else:#0.2C容量を掛けて、各レートの容量で割る。
                    C2_V2="Capacity_3.0V[mAh]"
                    C_02_1=df3_1[C2_V2].values#カット電圧時の容量データ
                    C_02_2=df3_2[C2_V2].values#カット電圧時の容量データ
                    C_02_3=df3_3[C2_V2].values#カット電圧時の容量データ
                    C_02_4=df3_4[C2_V2].values#カット電圧時の容量データ
                    C_02_5=df3_5[C2_V2].values#カット電圧時の容量データ
                    C_02_6=df3_6[C2_V2].values#カット電圧時の容量データ

                    df4=df2[df2["Discharge-rate[C]"]==float(ref)]#
                    C_V3=df4[C_V].values#カット電圧時の容量データ
                    C_V3=C_V3[0]

                    x1_1=C_02_1[0]
                    x1_2=C_02_2[0]
                    x1_3=C_02_3[0]
                    x1_4=C_02_4[0]
                    x1_5=C_02_5[0]
                    x1_6=C_02_6[0]

                    x2_1=C_V3
                    x2_2=C_V3
                    x2_3=C_V3
                    x2_4=C_V3
                    x2_5=C_V3
                    x2_6=C_V3

                    x1=x*x1_1/x2_1
                    x2=x*x1_2/x2_2
                    x3=x*x1_3/x2_3
                    x4=x*x1_4/x2_4
                    x5=x*x1_5/x2_5
                    x6=x*x1_6/x2_6
            else:
                "正しく選択されていません"
            y1=np.array(DF1["Voltage[V]"].values.flatten())#y1(vol)
            y2=np.array(DF2["Voltage[V]"].values.flatten())#y2(vol)
            y3=np.array(DF3["Voltage[V]"].values.flatten())#y3(vol)
            y4=np.array(DF4["Voltage[V]"].values.flatten())#y4(vol)
            y5=np.array(DF5["Voltage[V]"].values.flatten())#y5(vol)
            y6=np.array(DF6["Voltage[V]"].values.flatten())#y6(vol)

            plt.subplot(2,3,1)
            plt.title(NAME1,fontsize=title_size,fontname=font)
            plt.plot(x1,y1,color=cm2,label=NAME)
            plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
            plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
            plt.xlim(-5,105)
            plt.ylim(2.95,4.5)
            plt.xticks(fontsize=axis_size,fontname=font)
            plt.yticks(fontsize=axis_size,fontname=font)
            plt.legend()

            plt.subplot(2,3,2)
            plt.title(NAME2,fontsize=title_size,fontname=font)
            plt.plot(x2,y2,color=cm2,label=NAME)
            plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
            plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
            plt.xlim(-5,105)
            plt.ylim(2.95,4.5)
            plt.xticks(fontsize=axis_size,fontname=font)
            plt.yticks(fontsize=axis_size,fontname=font)
            plt.legend()

            plt.subplot(2,3,3)
            plt.title(NAME3,fontsize=title_size,fontname=font)
            plt.plot(x3,y3,color=cm2,label=NAME)
            plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
            plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
            plt.xlim(-5,105)
            plt.ylim(2.95,4.5)
            plt.xticks(fontsize=axis_size,fontname=font)
            plt.yticks(fontsize=axis_size,fontname=font)
            plt.legend()

            plt.subplot(2,3,4)
            plt.title(NAME4,fontsize=title_size,fontname=font)
            plt.plot(x4,y4,color=cm2,label=NAME)
            plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
            plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
            plt.xlim(-5,105)
            plt.ylim(2.95,4.5)
            plt.xticks(fontsize=axis_size,fontname=font)
            plt.yticks(fontsize=axis_size,fontname=font)
            plt.legend()

            plt.subplot(2,3,5)
            plt.title(NAME5,fontsize=title_size,fontname=font)
            plt.plot(x5,y5,color=cm2,label=NAME)
            plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
            plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
            plt.xlim(-5,105)
            plt.ylim(2.95,4.5)
            plt.xticks(fontsize=axis_size,fontname=font)
            plt.yticks(fontsize=axis_size,fontname=font)
            plt.legend()

            plt.subplot(2,3,6)
            plt.title(NAME6,fontsize=title_size,fontname=font)
            plt.plot(x6,y6,color=cm2,label=NAME)
            plt.xlabel("DOD[%]",fontsize=axisN_size,fontname=font)
            plt.ylabel("Cell-Voltage[V]",fontsize=axisN_size,fontname=font)
            plt.xlim(-5,105)
            plt.ylim(2.95,4.5)
            plt.xticks(fontsize=axis_size,fontname=font)
            plt.yticks(fontsize=axis_size,fontname=font)
            plt.legend()
        plt.show()


    #GUI---------------------------------------------------------------------------------------------------------
    #リスト

    def capa_spec():
        #選択した値は毎度同じ--------------------------------------------------------------------------------------------------
        ref=a.get()#ref⇒1Cとそれ以外で場合分け
        cut_vol=b.get()#カットvoltage
        #initial_dod=c.get()#DOD基準なのか、各容量基準なのか
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        #color_list2=[color1_1.get(),color1_2.get(),color1_3.get(),color1_4.get(),color1_5.get(),color1_6.get()]#行に並ぶカーブデータ
        #while color_list2.count("")>0:
        #    color_list2.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        #Rate_array=[[Rate1_1.get(),Rate1_2.get(),Rate1_3.get(),Rate1_4.get(),Rate1_5.get(),Rate1_6.get()],
        #            [Rate2_1.get(),Rate2_2.get(),Rate2_3.get(),Rate2_4.get(),Rate2_5.get(),Rate2_6.get()],
        #            [Rate3_1.get(),Rate3_2.get(),Rate3_3.get(),Rate3_4.get(),Rate3_5.get(),Rate3_6.get()],
        #            [Rate4_1.get(),Rate4_2.get(),Rate4_3.get(),Rate4_4.get(),Rate4_5.get(),Rate4_6.get()],
        #            [Rate5_1.get(),Rate5_2.get(),Rate5_3.get(),Rate5_4.get(),Rate5_5.get(),Rate5_6.get()],
        #            [Rate6_1.get(),Rate6_2.get(),Rate6_3.get(),Rate6_4.get(),Rate6_5.get(),Rate6_6.get()]]
    #--------------------------------------------------------------------------------------------------------------------
    #1行目の設定
        len_Lot=len(Lot_list)#ロットのリスト長さ
    #--------------------------------------------------------------------------------------------------------------------
        for i in range(0,len_Lot):
            cm2=color_list1[i]
            df2=df[df["Cell-Lot"]==Lot_list[i]]
            C_V="Capacity_"+cut_vol+"[mAh]"
            capa=np.array(df2[C_V].values.flatten())
            rate=np.array(df2["Discharge-rate[C]"].values.flatten())
            if(ref=="min_rated_capacity"):
                ref_capa=df2["min_rated_capacity[mAh]"].values
                ref_capa=ref_capa[0]
            else:
                df3=df2[df2["Discharge-rate[C]"]==float(ref)]
                ref_capa=np.array(df3[C_V].values.flatten())
                ref_capa=ref_capa[0]
            x=rate
            y=capa/ref_capa*100
            NAME=Lot_list[i]
            title_size=int(d.get())
            axisN_size=int(e.get())
            axis_size=int(f.get())
            font=g.get()
            plt.title("Capacity",fontsize=title_size,fontname=font)
            plt.plot(x,y,color=cm2,label=NAME,marker="o",mec=cm2,mew=3)
            plt.xlabel("Discharge-rate",fontsize=axisN_size,fontname=font)
            plt.ylabel("Capacity-retention[%]",fontsize=axisN_size,fontname=font)
            plt.xlim(-0.1,2.1)
            plt.ylim(65,105)
            plt.xticks(fontsize=axis_size,fontname=font)
            plt.yticks(fontsize=axis_size,fontname=font)
            plt.legend()

        ddf2=ddf[ddf["Spec_Name"]==h.get()]
        spec_x=ddf2["rate"].values
        spec_y=ddf2["spec"].values
        plt.scatter(spec_x,spec_y,marker='*',s=150,c="red",label="Spec")
        plt.legend()
        plt.show()

    List_capa_Reference=["min_rated_capacity",0.05,0.1,0.2,0.5,1.0,1.5,2.0]
    #List_capa_Reference2=[0.05,0.1,0.2,0.5,1.0,1.5,2.0]
    List_capa_Reference2=list(set(list(df["Discharge-rate[C]"])))
    List_capa_Reference2.sort()
    List_curve_Reference=["DOD","min_rated_capacity",0.05,0.1,0.2,0.5,1.0,1.5,2.0]
    List_voltage=["2.75V","3.0V","3.2V","3.4V","3.6V","3.8V","4.0V"]
    #df2=df[df["Discharge-rate[C]"]==0.2]#0.2Cはほとんどあるはずなので、0.2Cの放電データがあるものを基準とする。
    List_cell_Lot=list(set(list(df["Cell-Lot"].values.flatten())))
    List_cell_Lot.sort()
    List_color=['k','b','r','g','orange','darkviolet','aqua','lime']#カラーパレットの作成
    List_dod=["DOD","Reference"]
    fontsize_list=[4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    fontname_list=["serif","sans-serif","cursive","fantasy","monospace"]
    spec_list=list(ddf["Spec_Name"].values.flatten())
    spec_list=list(set(spec_list))

    #GUI
    root = Tk()
    a=StringVar(root)
    b=StringVar(root)
    c=StringVar(root)
    d=StringVar(root)
    e=StringVar(root)
    f=StringVar(root)
    g=StringVar(root)
    h=StringVar(root)
    color1=StringVar(root)
    color2=StringVar(root)
    color3=StringVar(root)
    color4=StringVar(root)
    color5=StringVar(root)
    color6=StringVar(root)
    color1_1=StringVar(root)
    color1_2=StringVar(root)
    color1_3=StringVar(root)
    color1_4=StringVar(root)
    color1_5=StringVar(root)
    color1_6=StringVar(root)
    class1=StringVar(root)
    class2=StringVar(root)
    class3=StringVar(root)
    class4=StringVar(root)
    class5=StringVar(root)
    class6=StringVar(root)
    Rate1_1=StringVar(root)
    Rate1_2=StringVar(root)
    Rate1_3=StringVar(root)
    Rate1_4=StringVar(root)
    Rate1_5=StringVar(root)
    Rate1_6=StringVar(root)
    Rate2_1=StringVar(root)
    Rate2_2=StringVar(root)
    Rate2_3=StringVar(root)
    Rate2_4=StringVar(root)
    Rate2_5=StringVar(root)
    Rate2_6=StringVar(root)
    Rate3_1=StringVar(root)
    Rate3_2=StringVar(root)
    Rate3_3=StringVar(root)
    Rate3_4=StringVar(root)
    Rate3_5=StringVar(root)
    Rate3_6=StringVar(root)
    Rate4_1=StringVar(root)
    Rate4_2=StringVar(root)
    Rate4_3=StringVar(root)
    Rate4_4=StringVar(root)
    Rate4_5=StringVar(root)
    Rate4_6=StringVar(root)
    Rate5_1=StringVar(root)
    Rate5_2=StringVar(root)
    Rate5_3=StringVar(root)
    Rate5_4=StringVar(root)
    Rate5_5=StringVar(root)
    Rate5_6=StringVar(root)
    Rate6_1=StringVar(root)
    Rate6_2=StringVar(root)
    Rate6_3=StringVar(root)
    Rate6_4=StringVar(root)
    Rate6_5=StringVar(root)
    Rate6_6=StringVar(root)

    root.title("Discharge Rate Capacity")
    Label(root, text="Reference:").grid(row=0,column=0)
    box1=ttk.Combobox(root,values=List_capa_Reference,textvariable=a,state="readonly",width=13)
    box1.grid(row=0,column=1)
    box1.set("0.2")
    Label(root, text="Cut-voltage:").grid(row=1,column=0)
    box2=ttk.Combobox(root, values=List_voltage,textvariable=b,state="readonly",width=13)
    box2.grid(row=1,column=1)
    box2.set("3.0V")
    Label(root, text="X-axis:").grid(row=2,column=0)
    Label(root, text="(Curveの基準)").grid(row=2,column=2)
    box3=ttk.Combobox(root, values=List_dod,textvariable=c,state="readonly",width=13)
    box3.grid(row=2,column=1)
    box3.set("DOD")

    Label(root, text="fontsize(タイトル/軸名/軸)").grid(row=0,column=2)
    box4=ttk.Combobox(root, values=fontsize_list,textvariable=d,state="normal",width=10)
    box4.grid(row=0,column=3)
    box4.set("12")
    box5=ttk.Combobox(root, values=fontsize_list,textvariable=e,state="normal",width=10)
    box5.grid(row=0,column=4)
    box5.set("10")
    box6=ttk.Combobox(root, values=fontsize_list,textvariable=f,state="normal",width=10)
    box6.grid(row=0,column=5)
    box6.set("9")
    Label(root, text="fontname").grid(row=1,column=2)
    box7=ttk.Combobox(root, values=fontname_list,textvariable=g,state="normal",width=10)
    box7.grid(row=1,column=3)
    box7.set("serif")

    box8=ttk.Combobox(root, values=spec_list,textvariable=h,state="normal",width=10)
    box8.grid(row=13,column=1)

    Label(root, text="color:").grid(row=3,column=1)
    Label(root, text="Cell-Lot:").grid(row=3,column=2)
    Label(root, text="Rate1").grid(row=2,column=3)
    Label(root, text="Rate2").grid(row=2,column=4)
    Label(root, text="Rate3").grid(row=2,column=5)
    Label(root, text="Rate4").grid(row=2,column=6)
    Label(root, text="Rate5").grid(row=2,column=7)
    Label(root, text="Rate6").grid(row=2,column=8)

    Label(root, text="Class1:").grid(row=4,column=0)
    Label(root, text="Class2:").grid(row=5,column=0)
    Label(root, text="Class3:").grid(row=6,column=0)
    Label(root, text="Class4:").grid(row=7,column=0)
    Label(root, text="Class5:").grid(row=8,column=0)
    Label(root, text="Class6:").grid(row=9,column=0)
    Label(root, text="Capacity:").grid(row=10,column=0)
    Label(root, text="Energy:").grid(row=11,column=0)
    Label(root, text="Curve:").grid(row=12,column=0)
    Label(root, text="Spec:").grid(row=13,column=0)
    Label(root, text="Ref/vol/色/Lot⇒").grid(row=10,column=1)
    Label(root, text="Ref/vol/色/Lot⇒").grid(row=11,column=1)
    Label(root, text="Ref/vol/axis/色/Lot⇒").grid(row=12,column=1)

    Button(root, text='Capacity', command=capa,height=1,width=13).grid(row=10, column=2, sticky=W, pady=4)
    Button(root, text='Energy', command=ene,height=1,width=13).grid(row=11, column=2, sticky=W, pady=4)
    Button(root, text='Lot-curve', command=Lot_curve,height=1,width=13).grid(row=12, column=2, sticky=W, pady=4)
    Button(root, text='Capacity-spec', command=capa_spec,height=1,width=13).grid(row=13, column=2, sticky=W, pady=4)

    color_box1=ttk.Combobox(root, values=List_color,textvariable=color1,state="normal",width=13).grid(row=4,column=1)
    color_box2=ttk.Combobox(root, values=List_color,textvariable=color2,state="normal",width=13).grid(row=5,column=1)
    color_box3=ttk.Combobox(root, values=List_color,textvariable=color3,state="normal",width=13).grid(row=6,column=1)
    color_box4=ttk.Combobox(root, values=List_color,textvariable=color4,state="normal",width=13).grid(row=7,column=1)
    color_box5=ttk.Combobox(root, values=List_color,textvariable=color5,state="normal",width=13).grid(row=8,column=1)
    color_box6=ttk.Combobox(root, values=List_color,textvariable=color6,state="normal",width=13).grid(row=9,column=1)

    color_box1_1=ttk.Combobox(root, values=List_color,textvariable=color1_1,state="normal",width=10).grid(row=3,column=3)
    color_box2_1=ttk.Combobox(root, values=List_color,textvariable=color1_2,state="normal",width=10).grid(row=3,column=4)
    color_box3_1=ttk.Combobox(root, values=List_color,textvariable=color1_3,state="normal",width=10).grid(row=3,column=5)
    color_box4_1=ttk.Combobox(root, values=List_color,textvariable=color1_4,state="normal",width=10).grid(row=3,column=6)
    color_box5_1=ttk.Combobox(root, values=List_color,textvariable=color1_5,state="normal",width=10).grid(row=3,column=7)
    color_box6_1=ttk.Combobox(root, values=List_color,textvariable=color1_6,state="normal",width=10).grid(row=3,column=8)

    class_box1=ttk.Combobox(root, values=List_cell_Lot,textvariable=class1,state="normal",width=16).grid(row=4,column=2)
    class_box2=ttk.Combobox(root, values=List_cell_Lot,textvariable=class2,state="normal",width=16).grid(row=5,column=2)
    class_box3=ttk.Combobox(root, values=List_cell_Lot,textvariable=class3,state="normal",width=16).grid(row=6,column=2)
    class_box4=ttk.Combobox(root, values=List_cell_Lot,textvariable=class4,state="normal",width=16).grid(row=7,column=2)
    class_box5=ttk.Combobox(root, values=List_cell_Lot,textvariable=class5,state="normal",width=16).grid(row=8,column=2)
    class_box6=ttk.Combobox(root, values=List_cell_Lot,textvariable=class6,state="normal",width=16).grid(row=9,column=2)

    Rate_box1_1=ttk.Combobox(root, values=List_capa_Reference2,textvariable=Rate1_1,state="normal",width=10).grid(row=4,column=3)
    Rate_box2_1=ttk.Combobox(root, values=List_capa_Reference2,textvariable=Rate2_1,state="normal",width=10).grid(row=5,column=3)
    Rate_box3_1=ttk.Combobox(root, values=List_capa_Reference2,textvariable=Rate3_1,state="normal",width=10).grid(row=6,column=3)
    Rate_box4_1=ttk.Combobox(root, values=List_capa_Reference2,textvariable=Rate4_1,state="normal",width=10).grid(row=7,column=3)
    Rate_box5_1=ttk.Combobox(root, values=List_capa_Reference2,textvariable=Rate5_1,state="normal",width=10).grid(row=8,column=3)
    Rate_box6_1=ttk.Combobox(root, values=List_capa_Reference2,textvariable=Rate6_1,state="normal",width=10).grid(row=9,column=3)

    Rate_box1_2=ttk.Combobox(root, values=List_capa_Reference2,textvariable=Rate1_2,state="normal",width=10).grid(row=4,column=4)
    Rate_box2_2=ttk.Combobox(root, values=List_capa_Reference2,textvariable=Rate2_2,state="normal",width=10).grid(row=5,column=4)
    Rate_box3_2=ttk.Combobox(root, values=List_capa_Reference2,textvariable=Rate3_2,state="normal",width=10).grid(row=6,column=4)
    Rate_box4_2=ttk.Combobox(root, values=List_capa_Reference2,textvariable=Rate4_2,state="normal",width=10).grid(row=7,column=4)
    Rate_box5_2=ttk.Combobox(root, values=List_capa_Reference2,textvariable=Rate5_2,state="normal",width=10).grid(row=8,column=4)
    Rate_box6_2=ttk.Combobox(root, values=List_capa_Reference2,textvariable=Rate6_2,state="normal",width=10).grid(row=9,column=4)

    Rate_box1_3=ttk.Combobox(root, values=List_capa_Reference2,textvariable=Rate1_3,state="normal",width=10).grid(row=4,column=5)
    Rate_box2_3=ttk.Combobox(root, values=List_capa_Reference2,textvariable=Rate2_3,state="normal",width=10).grid(row=5,column=5)
    Rate_box3_3=ttk.Combobox(root, values=List_capa_Reference2,textvariable=Rate3_3,state="normal",width=10).grid(row=6,column=5)
    Rate_box4_3=ttk.Combobox(root, values=List_capa_Reference2,textvariable=Rate4_3,state="normal",width=10).grid(row=7,column=5)
    Rate_box5_3=ttk.Combobox(root, values=List_capa_Reference2,textvariable=Rate5_3,state="normal",width=10).grid(row=8,column=5)
    Rate_box6_3=ttk.Combobox(root, values=List_capa_Reference2,textvariable=Rate6_3,state="normal",width=10).grid(row=9,column=5)

    Rate_box1_4=ttk.Combobox(root, values=List_capa_Reference2,textvariable=Rate1_4,state="normal",width=10).grid(row=4,column=6)
    Rate_box2_4=ttk.Combobox(root, values=List_capa_Reference2,textvariable=Rate2_4,state="normal",width=10).grid(row=5,column=6)
    Rate_box3_4=ttk.Combobox(root, values=List_capa_Reference2,textvariable=Rate3_4,state="normal",width=10).grid(row=6,column=6)
    Rate_box4_4=ttk.Combobox(root, values=List_capa_Reference2,textvariable=Rate4_4,state="normal",width=10).grid(row=7,column=6)
    Rate_box5_4=ttk.Combobox(root, values=List_capa_Reference2,textvariable=Rate5_4,state="normal",width=10).grid(row=8,column=6)
    Rate_box6_4=ttk.Combobox(root, values=List_capa_Reference2,textvariable=Rate6_4,state="normal",width=10).grid(row=9,column=6)

    Rate_box1_5=ttk.Combobox(root, values=List_capa_Reference2,textvariable=Rate1_5,state="normal",width=10).grid(row=4,column=7)
    Rate_box2_5=ttk.Combobox(root, values=List_capa_Reference2,textvariable=Rate2_5,state="normal",width=10).grid(row=5,column=7)
    Rate_box3_5=ttk.Combobox(root, values=List_capa_Reference2,textvariable=Rate3_5,state="normal",width=10).grid(row=6,column=7)
    Rate_box4_5=ttk.Combobox(root, values=List_capa_Reference2,textvariable=Rate4_5,state="normal",width=10).grid(row=7,column=7)
    Rate_box5_5=ttk.Combobox(root, values=List_capa_Reference2,textvariable=Rate5_5,state="normal",width=10).grid(row=8,column=7)
    Rate_box6_5=ttk.Combobox(root, values=List_capa_Reference2,textvariable=Rate6_5,state="normal",width=10).grid(row=9,column=7)

    Rate_box1_6=ttk.Combobox(root, values=List_capa_Reference2,textvariable=Rate1_6,state="normal",width=10).grid(row=4,column=8)
    Rate_box2_6=ttk.Combobox(root, values=List_capa_Reference2,textvariable=Rate2_6,state="normal",width=10).grid(row=5,column=8)
    Rate_box3_6=ttk.Combobox(root, values=List_capa_Reference2,textvariable=Rate3_6,state="normal",width=10).grid(row=6,column=8)
    Rate_box4_6=ttk.Combobox(root, values=List_capa_Reference2,textvariable=Rate4_6,state="normal",width=10).grid(row=7,column=8)
    Rate_box5_6=ttk.Combobox(root, values=List_capa_Reference2,textvariable=Rate5_6,state="normal",width=10).grid(row=8,column=8)
    Rate_box6_6=ttk.Combobox(root, values=List_capa_Reference2,textvariable=Rate6_6,state="normal",width=10).grid(row=9,column=8)

    Button(root, text='all', command=All1).grid(row=4, column=9, sticky=W, pady=4)
    Button(root, text='all', command=All2).grid(row=5, column=9, sticky=W, pady=4)
    Button(root, text='all', command=All3).grid(row=6, column=9, sticky=W, pady=4)
    Button(root, text='all', command=All4).grid(row=7, column=9, sticky=W, pady=4)
    Button(root, text='all', command=All5).grid(row=8, column=9, sticky=W, pady=4)
    Button(root, text='all', command=All6).grid(row=9, column=9, sticky=W, pady=4)

    Button(root, text='DOD-vol', command=d_V_1).grid(row=4, column=10, sticky=W, pady=4)
    Button(root, text='DOD-vol', command=d_V_2).grid(row=5, column=10, sticky=W, pady=4)
    Button(root, text='DOD-vol', command=d_V_3).grid(row=6, column=10, sticky=W, pady=4)
    Button(root, text='DOD-vol', command=d_V_4).grid(row=7, column=10, sticky=W, pady=4)
    Button(root, text='DOD-vol', command=d_V_5).grid(row=8, column=10, sticky=W, pady=4)
    Button(root, text='DOD-vol', command=d_V_6).grid(row=9, column=10, sticky=W, pady=4)

    Button(root, text='DOD-dVdQ', command=dvdq1).grid(row=4, column=11, sticky=W, pady=4)
    Button(root, text='DOD-dVdQ', command=dvdq2).grid(row=5, column=11, sticky=W, pady=4)
    Button(root, text='DOD-dVdQ', command=dvdq3).grid(row=6, column=11, sticky=W, pady=4)
    Button(root, text='DOD-dVdQ', command=dvdq4).grid(row=7, column=11, sticky=W, pady=4)
    Button(root, text='DOD-dVdQ', command=dvdq5).grid(row=8, column=11, sticky=W, pady=4)
    Button(root, text='DOD-dVdQ', command=dvdq6).grid(row=9, column=11, sticky=W, pady=4)

    Button(root, text='DOD-ΔV', command=delta_V1).grid(row=4, column=12, sticky=W, pady=4)
    Button(root, text='DOD-ΔV', command=delta_V2).grid(row=5, column=12, sticky=W, pady=4)
    Button(root, text='DOD-ΔV', command=delta_V3).grid(row=6, column=12, sticky=W, pady=4)
    Button(root, text='DOD-ΔV', command=delta_V4).grid(row=7, column=12, sticky=W, pady=4)
    Button(root, text='DOD-ΔV', command=delta_V5).grid(row=8, column=12, sticky=W, pady=4)
    Button(root, text='DOD-ΔV', command=delta_V6).grid(row=9, column=12, sticky=W, pady=4)

    Button(root, text='DOD-DCR', command=DCR1).grid(row=4, column=13, sticky=W, pady=4)
    Button(root, text='DOD-DCR', command=DCR2).grid(row=5, column=13, sticky=W, pady=4)
    Button(root, text='DOD-DCR', command=DCR3).grid(row=6, column=13, sticky=W, pady=4)
    Button(root, text='DOD-DCR', command=DCR4).grid(row=7, column=13, sticky=W, pady=4)
    Button(root, text='DOD-DCR', command=DCR5).grid(row=8, column=13, sticky=W, pady=4)
    Button(root, text='DOD-DCR', command=DCR6).grid(row=9, column=13, sticky=W, pady=4)

    Button(root, text='all', command=All7,height=1,width=13).grid(row=10, column=3, sticky=W, pady=4)
    Button(root, text='all', command=All8,height=1,width=13).grid(row=10, column=4, sticky=W, pady=4)
    Button(root, text='all', command=All9,height=1,width=13).grid(row=10, column=5, sticky=W, pady=4)
    Button(root, text='all', command=All10,height=1,width=13).grid(row=10, column=6, sticky=W, pady=4)
    Button(root, text='all', command=All11,height=1,width=13).grid(row=10, column=7, sticky=W, pady=4)
    Button(root, text='all', command=All12,height=1,width=13).grid(row=10, column=8, sticky=W, pady=4)

    Button(root, text='DOD-vol', command=d_V_7,height=1,width=13).grid(row=11, column=3, sticky=W, pady=4)
    Button(root, text='DOD-vol', command=d_V_8,height=1,width=13).grid(row=11, column=4, sticky=W, pady=4)
    Button(root, text='DOD-vol', command=d_V_9,height=1,width=13).grid(row=11, column=5, sticky=W, pady=4)
    Button(root, text='DOD-vol', command=d_V_10,height=1,width=13).grid(row=11, column=6, sticky=W, pady=4)
    Button(root, text='DOD-vol', command=d_V_11,height=1,width=13).grid(row=11, column=7, sticky=W, pady=4)
    Button(root, text='DOD-vol', command=d_V_12,height=1,width=13).grid(row=11, column=8, sticky=W, pady=4)

    Button(root, text='DOD-dVdQ', command=dvdq7,height=1,width=13).grid(row=12, column=3, sticky=W, pady=4)
    Button(root, text='DOD-dVdQ', command=dvdq8,height=1,width=13).grid(row=12, column=4, sticky=W, pady=4)
    Button(root, text='DOD-dVdQ', command=dvdq9,height=1,width=13).grid(row=12, column=5, sticky=W, pady=4)
    Button(root, text='DOD-dVdQ', command=dvdq10,height=1,width=13).grid(row=12, column=6, sticky=W, pady=4)
    Button(root, text='DOD-dVdQ', command=dvdq11,height=1,width=13).grid(row=12, column=7, sticky=W, pady=4)
    Button(root, text='DOD-dVdQ', command=dvdq12,height=1,width=13).grid(row=12, column=8, sticky=W, pady=4)

    Button(root, text='DOD-ΔV', command=delta_V7,height=1,width=13).grid(row=13, column=3, sticky=W, pady=4)
    Button(root, text='DOD-ΔV', command=delta_V8,height=1,width=13).grid(row=13, column=4, sticky=W, pady=4)
    Button(root, text='DOD-ΔV', command=delta_V9,height=1,width=13).grid(row=13, column=5, sticky=W, pady=4)
    Button(root, text='DOD-ΔV', command=delta_V10,height=1,width=13).grid(row=13, column=6, sticky=W, pady=4)
    Button(root, text='DOD-ΔV', command=delta_V11,height=1,width=13).grid(row=13, column=7, sticky=W, pady=4)
    Button(root, text='DOD-ΔV', command=delta_V12,height=1,width=13).grid(row=13, column=8, sticky=W, pady=4)

    Button(root, text='DOD-DCR', command=DCR7,height=1,width=13).grid(row=14, column=3, sticky=W, pady=4)
    Button(root, text='DOD-DCR', command=DCR8,height=1,width=13).grid(row=14, column=4, sticky=W, pady=4)
    Button(root, text='DOD-DCR', command=DCR9,height=1,width=13).grid(row=14, column=5, sticky=W, pady=4)
    Button(root, text='DOD-DCR', command=DCR10,height=1,width=13).grid(row=14, column=6, sticky=W, pady=4)
    Button(root, text='DOD-DCR', command=DCR11,height=1,width=13).grid(row=14, column=7, sticky=W, pady=4)
    Button(root, text='DOD-DCR', command=DCR12,height=1,width=13).grid(row=14, column=8, sticky=W, pady=4)
    root.mainloop()

def import_cha():
    print("a")
def import_distemp():
    print("a")
def import_dcr():
    print("a")
def import_aci():
    #ファイル読み込みの手法
    today=datetime.datetime.now()
    year=today.year
    month=today.month
    day=today.day
    hour=today.hour
    minute=today.minute
    second=today.second
    if(month<10):
        month=str(0)+str(month)
    else:
        month=str(month)
    if(day<10):
        day=str(0)+str(day)
    else:
        day=str(day)
    if(hour<10):
        hour=str(0)+str(hour)
    else:
        hour=str(hour)
    if(minute<10):
        minute=str(0)+str(minute)
    else:
        minute=str(minute)
    if(second<10):
        second=str(0)+str(second)
    else:
        second=str(second)
    time_stamp=str(year)+month+str(day)+str(hour)+str(minute)+str(second)

    def ACI_import():
        #ファイルの読み込み
        #フォルダの指定--------------------------------------------
        root=tkinter.Tk()
        root.withdraw()
        args=askopenfilenames(filetypes=(("All files", "*.*"),("HTML files", "*.html;*.htm"),("csv files", "*.csv") ))
        args_size=len(args)
        capa=float(min_rated_capacity.get())
        EQ=eq.get()
        TEMP=temp.get()
        SIZE=size.get()
        VOLTAGE=voltage.get()
        CONDITION=condition.get()
        GEN=gen.get()
        print("ファイル数")
        print(args_size)
        for i in range(args_size):
            df=pd.read_excel(args[i],sheetname="Data",encoding='cp932',header=1)
            df2=pd.read_excel(args[i],sheetname="Data",encoding='cp932',header=None)
            df2=df2.iloc[0:1]#1列目だけ抽出
            Len_column=len(df.columns)
            Len_column=int(Len_column/6)
            print(args[i])
            print("繰り返し数")
            print(Len_column)
            for j in range(Len_column):
                NAME=df2[6*j+1].values.flatten()
                NAME=NAME[0]
                NAME2=NAME[4:-11]#試作+Lot
                NAME3=NAME[4:-7]#試作+Lot+No
                NAME4=int(NAME[-6:-2])#サイクル数
                save_file="C:\DataBase\ACI\Data"+"\ACI_"+NAME3+"_"+CONDITION+"_"+EQ+"_"+TEMP+"deg.C_"+SIZE+"_"+str(VOLTAGE)+"V_"+str(NAME4)+"cyc_"+str(capa)+"mAh"+"_Data.csv"#Rawデータのリンク
                Raw_file="C:\DataBase\ACI\Raw"+"\ACI_"+NAME3+"_"+CONDITION+"_"+EQ+"_"+TEMP+"deg.C_"+SIZE+"_"+str(VOLTAGE)+"V_"+str(NAME4)+"cyc_"+str(capa)+"mAh"+"_Raw.csv"#Rawデータのリンク
                Lot_cyc=NAME3+"-"+CONDITION
                def Data(x):
                    df3=df.iloc[0:-1,x*6:x*6+6]
                    df3.columns=["A","B","C","D","E","F"]
                    df3=df3.dropna(axis=0)
                    df4=df3.sort_values(by='A')
                    AA=np.arange(-2,5.01,0.01)
                    #interp
                    A=np.array(df4["A"].values.flatten())
                    A=np.log10(A)
                    B=np.array(df4["B"].values.flatten())
                    C=np.array(df4["C"].values.flatten())
                    D=np.array(df4["D"].values.flatten())
                    E=np.array(df4["E"].values.flatten())
                    F=np.array(df4["F"].values.flatten())

                    BB=np.interp(AA,A,B)
                    CC=np.interp(AA,A,C)
                    DD=np.interp(AA,A,D)
                    EE=np.interp(AA,A,E)
                    FF=np.interp(AA,A,F)

                    AAA=10**(AA)
                    AAA=pd.DataFrame(AAA)
                    AAA.columns=["Frequency[Hz]"]
                    logAAA=pd.DataFrame(AA)
                    logAAA.columns=["logf"]
                    BBB=pd.DataFrame(BB)
                    BBB.columns=["Z'[mohm]"]
                    CCC=pd.DataFrame(CC)
                    CCC.columns=["Z''[mohm]"]
                    DDD=pd.DataFrame(DD)
                    DDD.columns=["theta[rad]"]
                    EEE=pd.DataFrame(EE)
                    EEE.columns=["|Z|[mohm]"]
                    FFF=pd.DataFrame(FF)
                    FFF.columns=["delta|Z|/delta(logf)[mohm]"]
                    DF=pd.concat([AAA,logAAA],axis=1)
                    dff=pd.concat([DF,BBB],axis=1)
                    dff=pd.concat([dff,CCC],axis=1)
                    dff=pd.concat([dff,DDD],axis=1)
                    dff=pd.concat([dff,EEE],axis=1)
                    dff=pd.concat([dff,FFF],axis=1)
                    return dff

                def Raw(x):
                    df3=df.iloc[0:-1,x*6:x*6+6]
                    df3.columns=["Frequency[Hz]","Z'[mohm]","Z''[mohm]","theta[rad]","|Z|[mohm]","delta|Z|/delta(logf)[mohm]"]
                    df3=df3.dropna(axis=0)
                    return df3

                Raw=Raw(j)
                Data=Data(j)
                Z_length=np.array(Data["|Z|[mohm]"].values.flatten())
                imp_01Hz=Z_length[100]
                imp_1Hz=Z_length[200]
                imp_10Hz=Z_length[300]
                imp_100Hz=Z_length[400]
                imp_1kHz=Z_length[500]
                imp_10kHz=Z_length[600]

                x1=np.array(Data["Z'[mohm]"].values.flatten())
                y1=np.array(Data["Z''[mohm]"].values.flatten())
                Rs=x1[np.abs(np.asarray(y1)-0).argmin()]
                R2=x1[np.abs(np.asarray(y1[101:401])-0).argmax()]
                R1=R2-Rs
                R1_capa=R1/capa
                info=[EQ,#装置
                      TEMP,#測定温度
                      SIZE,#サイズ
                      VOLTAGE,#測定電圧
                      capa,#min-rated-capacity
                      save_file,#編集データの保存先
                      Raw_file,#Rawデータの保存先
                      NAME2,#試作+水準
                      NAME3,#試作+水準+No
                      NAME4,#サイクル数
                      CONDITION,#条件
                      Lot_cyc,#LotNAME+サイクル名
                      imp_01Hz,#0.1Hzimp
                      imp_1Hz,#1Hzimp
                      imp_10Hz,#10Hzimp
                      imp_100Hz,#100Hzimp
                      imp_1kHz,#1000Hzimp
                      imp_10kHz,#10000Hzimp
                      Rs,#Rs
                      R2,#Rs+Rct
                      R1,#Rct(仮)
                      R1_capa,#Rct/min_rated_capacity
                      GEN]#世代
                info=pd.DataFrame(info)
                info=info.T
                info.columns=["Equipment",
                              "temp[deg.C]",
                              "Size",
                              "Cell-Voltage[V]",
                              "min_rated_capacity[mAh]",
                              "Link_Data",
                              "Link_Raw",
                              "Try-lot.",
                              "Cell-Lot",
                              "Cycle_Number",
                              "Lot-CycleNAME",
                              "Condition",
                              "0.1Hz-imp[mohm]",
                              "1Hz-imp[mohm]",
                              "10Hz-imp[mohm]",
                              "100Hz-imp[mohm]",
                              "1kHz-imp[mohm]",
                              "10kHz-imp[mohm]",
                              "Rs[mohm]",
                              "Rs+R1[mohm]",
                              "R1[mohm]",
                              "R1/min_rated_capacity[mohm/mAh]",
                              "Gen"]

                Data.to_csv(save_file,index=False)
                Raw.to_csv(Raw_file,index=False)
                info2=pd.read_csv("C:\DataBase\ACI\ACI_used-cell.csv")
                info3=pd.concat([info2,info],axis=0)
                save_link="C:\DataBase\ACI\Cell_information"+"\ACI_used-cell"+"_"+time_stamp+".csv"
                info3.to_csv(save_link,index=False)
            print("ファイル終了")
        print("全取り込み終了")
    #GUI
    List_name_cyc=["2G_25degC","2G_35degC","2G_45degC","VAC_25degC","VAC_35degC","VAC_40degC","VAC_45degC"
                            ,"D3x_25degC","D3x_35degC","D3x_45degC","Hw3step_23degC","Hw3step_45degC","Rest_cycle_RT","Rest_cycle_45degC"
                            ,"Hw1.3Cstep_23degC","Hw1.3Cstep_45degC","2G_23degC","2G_RT","0510_25degC","0510_45degC","0910_25degC","after-xx"]
    List_eq_solartron=["5G3F_solartron","4G_solartron","5G4F_solartron"]
    List_temp=["RT",25,-10,0,10,15,35,40,45,50,55,60]
    List_min_rated_capa=[2210,3000,2957,185,224,4120]
    List_size=["343996","4145A1","341922","406787"]
    List_voltage=[4.35,4.40,4.45]
    List_gen=["H9/Gen6","Gen5Plus","Gen6Plus","Gen7","H10"]

    root = Tk()
    eq=StringVar(root)
    temp=StringVar(root)
    min_rated_capacity=StringVar(root)
    size=StringVar(root)
    voltage=StringVar(root)
    condition=StringVar(root)
    gen=StringVar(root)

    Label(root, text="測定装置").grid(row=0,column=0)
    Label(root, text="測定温度[deg.C]").grid(row=1,column=0)
    Label(root, text="min_rated_capacity[mAh]").grid(row=2,column=0)
    Label(root, text="サイズ").grid(row=3,column=0)
    Label(root, text="電圧[V]").grid(row=4,column=0)
    Label(root, text="Condition(サイクル名etc.)").grid(row=5,column=0)
    Label(root, text="世代").grid(row=6,column=0)

    box1=ttk.Combobox(root,values=List_eq_solartron,textvariable=eq,state="normaly",width=20)
    box1.grid(row=0,column=1)
    box1.set("5G3F_solartron")
    box2=ttk.Combobox(root,values=List_temp,textvariable=temp,state="normaly",width=20)
    box2.grid(row=1,column=1)
    box2.set(25)
    box3=ttk.Combobox(root,values=List_min_rated_capa,textvariable=min_rated_capacity,state="normaly",width=20)
    box3.grid(row=2,column=1)
    box3.set(2210)
    box4=ttk.Combobox(root,values=List_size,textvariable=size,state="normaly",width=20)
    box4.grid(row=3,column=1)
    box4.set("343996")
    box5=ttk.Combobox(root,values=List_voltage,textvariable=voltage,state="normaly",width=20)
    box5.grid(row=4,column=1)
    box5.set("4.45")
    box6=ttk.Combobox(root,values=List_name_cyc,textvariable=condition,state="normaly",width=20)
    box6.grid(row=5,column=1)
    box7=ttk.Combobox(root,values=List_gen,textvariable=gen,state="normaly",width=20)
    box7.grid(row=6,column=1)
    box7.set("H9/Gen6")

    button1 =Button(root,text='import',command=ACI_import).grid(row=7,column=1)
    button1 =Button(root,text='終了',command=root.quit).grid(row=8,column=1)

    root.mainloop()

def import_float():
    print("a")
def import_storage():
    print("a")
def import_cyc():
    print("a")
def import_cycsta():
    print("a")
def import_cyc_curve():
    print("a")
def import_static():
    print("a")

def float_result2():
    #Listファイルの選択
    root=tkinter.Tk()
    root.withdraw()
    args=askopenfilenames(filetypes=(("All files", "*.*"),("HTML files", "*.html;*.htm"),("csv files", "*.csv") ))
    #データフレーム
    df1=pd.read_excel(args[0],sheetname="hot",encodint="cp932",index_col=0)#hot
    df1=df1.dropna(axis=0,how="all")
    df2=pd.read_excel(args[0],sheetname="cold",encodint="cp932",index_col=0)#cold
    df2=df2.dropna(axis=0,how="all")

    def hot():
        initial=a.get()
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get(),
                     color7.get(),color8.get(),color9.get(),color10.get(),color11.get(),color12.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get(),
                  class7.get(),class8.get(),class9.get(),class10.get(),class11.get(),class12.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        plate_label="thickness-plate[%]_300g_"+initial
        DF=df1[["Cell-Lot","Floating-time[h]","thickness-plate[%]_300g_initial","thickness-plate[%]_300g_full_Charge-initial"]]
        num=len(Lot_list)
        for i in range(num):
            DF1=DF[DF["Cell-Lot"]==Lot_list[i]]
            x=DF1["Floating-time[h]"].values.flatten()
            y=DF1[plate_label].values.flatten()
            plt.title("Float-Result(hot-state)",fontsize=12)
            plt.plot(x,y,"-o",color=color_list1[i],label=Lot_list[i])
            plt.xlabel("Float-time[h]",fontsize=12)
            plt.ylabel("thickness-plate[%]",fontsize=12)
            plt.xlim(-5,1000)
            plt.ylim(-1,26)
            plt.xticks(fontsize=12)
            plt.yticks(fontsize=12)
            plt.legend()
        plt.show()

    def cold():
        initial=a.get()
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get(),
                     color7.get(),color8.get(),color9.get(),color10.get(),color11.get(),color12.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get(),
                  class7.get(),class8.get(),class9.get(),class10.get(),class11.get(),class12.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        plate_label="thickness-plate[%]_300g_"+initial
        DF=df2[["Cell-Lot","Floating-time[h]","thickness-plate[%]_300g_initial","thickness-plate[%]_300g_full_Charge-initial"]]
        num=len(Lot_list)
        for i in range(num):
            DF1=DF[DF["Cell-Lot"]==Lot_list[i]]
            x=DF1["Floating-time[h]"].values.flatten()
            y=DF1[plate_label].values.flatten()
            plt.title("Float-Result(cold-state)",fontsize=12)
            plt.plot(x,y,"-o",color=color_list1[i],label=Lot_list[i])
            plt.xlabel("Float-time[h]",fontsize=12)
            plt.ylabel("thickness-plate[%]",fontsize=12)
            plt.xlim(-5,1000)
            plt.ylim(-1,26)
            plt.xticks(fontsize=12)
            plt.yticks(fontsize=12)
            plt.legend()
        plt.show()
    def hot_cold():
        initial=a.get()
        color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get(),
                     color7.get(),color8.get(),color9.get(),color10.get(),color11.get(),color12.get()] #列に並ぶカーブデータ
        while color_list1.count("")>0:
            color_list1.remove("")
        Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get(),
                  class7.get(),class8.get(),class9.get(),class10.get(),class11.get(),class12.get()]#Lotのリスト
        while Lot_list.count("")>0:
            Lot_list.remove("")
        plate_label="thickness-plate[%]_300g_"+initial
        num=len(Lot_list)
        ddf1=df1[["Cell-Lot","Floating-time[h]","thickness-plate[%]_300g_initial","thickness-plate[%]_300g_full_Charge-initial"]]
        ddf2=df2[["Cell-Lot","Floating-time[h]","thickness-plate[%]_300g_initial","thickness-plate[%]_300g_full_Charge-initial"]]
        for i in range(num):
            DF1=ddf1[ddf1["Cell-Lot"]==Lot_list[i]]
            x1=DF1["Floating-time[h]"].values.flatten()
            y1=DF1[plate_label].values.flatten()
            plt.subplot(1,2,1)
            plt.title("Float-Result(hot-state)",fontsize=12)
            plt.plot(x1,y1,"-o",color=color_list1[i],label=Lot_list[i])
            plt.xlabel("Float-time[h]",fontsize=12)
            plt.ylabel("thickness-plate[%]",fontsize=12)
            plt.xlim(-5,1000)
            plt.ylim(-1,26)
            plt.xticks(fontsize=12)
            plt.yticks(fontsize=12)
            plt.legend()

            DF2=ddf2[ddf2["Cell-Lot"]==Lot_list[i]]
            x2=DF2["Floating-time[h]"].values.flatten()
            y2=DF2[plate_label].values.flatten()
            plt.subplot(1,2,2)
            plt.title("Float-Result(cold-state)",fontsize=12)
            plt.plot(x2,y2,"-o",color=color_list1[i],label=Lot_list[i])
            plt.xlabel("Float-time[h]",fontsize=12)
            plt.ylabel("thickness-plate[%]",fontsize=12)
            plt.xlim(-10,1000)
            plt.ylim(-1,26)
            plt.xticks(fontsize=12)
            plt.yticks(fontsize=12)
            plt.legend()
        plt.show()
    List_initial=["initial","full_Charge-initial"]
    df1=df1.dropna(subset=["Cell-Lot"])
    List_cell_Lot=list(set(list(df1["Cell-Lot"].values.flatten())))
    List_cell_Lot.sort()
    List_color=['k','b','r','g','orange','darkviolet','aqua','lime']#カラーパレットの作成

    root = Tk()
    a=StringVar(root)
    color1=StringVar(root)
    color2=StringVar(root)
    color3=StringVar(root)
    color4=StringVar(root)
    color5=StringVar(root)
    color6=StringVar(root)
    color7=StringVar(root)
    color8=StringVar(root)
    color9=StringVar(root)
    color10=StringVar(root)
    color11=StringVar(root)
    color12=StringVar(root)
    class1=StringVar(root)
    class2=StringVar(root)
    class3=StringVar(root)
    class4=StringVar(root)
    class5=StringVar(root)
    class6=StringVar(root)
    class7=StringVar(root)
    class8=StringVar(root)
    class9=StringVar(root)
    class10=StringVar(root)
    class11=StringVar(root)
    class12=StringVar(root)

    Label(root, text="Initial:").grid(row=0,column=0)
    Label(root, text="Class1:").grid(row=1,column=0)
    Label(root, text="Class2:").grid(row=2,column=0)
    Label(root, text="Class3:").grid(row=3,column=0)
    Label(root, text="Class4:").grid(row=4,column=0)
    Label(root, text="Class5:").grid(row=5,column=0)
    Label(root, text="Class6:").grid(row=6,column=0)
    Label(root, text="Class7:").grid(row=7,column=0)
    Label(root, text="Class8:").grid(row=8,column=0)
    Label(root, text="Class9:").grid(row=9,column=0)
    Label(root, text="Class10:").grid(row=10,column=0)
    Label(root, text="Class11:").grid(row=11,column=0)
    Label(root, text="Class12:").grid(row=12,column=0)

    box1=ttk.Combobox(root,values=List_initial,textvariable=a,state="normal",width=13)

    box2=ttk.Combobox(root,values=List_color,textvariable=color1,state="normal",width=13)
    box3=ttk.Combobox(root,values=List_color,textvariable=color2,state="normal",width=13)
    box4=ttk.Combobox(root,values=List_color,textvariable=color3,state="normal",width=13)
    box5=ttk.Combobox(root,values=List_color,textvariable=color4,state="normal",width=13)
    box6=ttk.Combobox(root,values=List_color,textvariable=color5,state="normal",width=13)
    box7=ttk.Combobox(root,values=List_color,textvariable=color6,state="normal",width=13)
    box8=ttk.Combobox(root,values=List_color,textvariable=color7,state="normal",width=13)
    box9=ttk.Combobox(root,values=List_color,textvariable=color8,state="normal",width=13)
    box10=ttk.Combobox(root,values=List_color,textvariable=color9,state="normal",width=13)
    box11=ttk.Combobox(root,values=List_color,textvariable=color10,state="normal",width=13)
    box12=ttk.Combobox(root,values=List_color,textvariable=color11,state="normal",width=13)
    box13=ttk.Combobox(root,values=List_color,textvariable=color12,state="normal",width=13)

    box14=ttk.Combobox(root,values=List_cell_Lot,textvariable=class1,state="normal",width=30)
    box15=ttk.Combobox(root,values=List_cell_Lot,textvariable=class2,state="normal",width=30)
    box16=ttk.Combobox(root,values=List_cell_Lot,textvariable=class3,state="normal",width=30)
    box17=ttk.Combobox(root,values=List_cell_Lot,textvariable=class4,state="normal",width=30)
    box18=ttk.Combobox(root,values=List_cell_Lot,textvariable=class5,state="normal",width=30)
    box19=ttk.Combobox(root,values=List_cell_Lot,textvariable=class6,state="normal",width=30)
    box20=ttk.Combobox(root,values=List_cell_Lot,textvariable=class7,state="normal",width=30)
    box21=ttk.Combobox(root,values=List_cell_Lot,textvariable=class8,state="normal",width=30)
    box22=ttk.Combobox(root,values=List_cell_Lot,textvariable=class9,state="normal",width=30)
    box23=ttk.Combobox(root,values=List_cell_Lot,textvariable=class10,state="normal",width=30)
    box24=ttk.Combobox(root,values=List_cell_Lot,textvariable=class11,state="normal",width=30)
    box25=ttk.Combobox(root,values=List_cell_Lot,textvariable=class12,state="normal",width=30)

    box1.grid(row=0,column=1)
    box2.grid(row=1,column=1)
    box3.grid(row=2,column=1)
    box4.grid(row=3,column=1)
    box5.grid(row=4,column=1)
    box6.grid(row=5,column=1)
    box7.grid(row=6,column=1)
    box8.grid(row=7,column=1)
    box9.grid(row=8,column=1)
    box10.grid(row=9,column=1)
    box11.grid(row=10,column=1)
    box12.grid(row=11,column=1)
    box13.grid(row=12,column=1)


    box14.grid(row=1,column=2)
    box15.grid(row=2,column=2)
    box16.grid(row=3,column=2)
    box17.grid(row=4,column=2)
    box18.grid(row=5,column=2)
    box19.grid(row=6,column=2)
    box20.grid(row=7,column=2)
    box21.grid(row=8,column=2)
    box22.grid(row=9,column=2)
    box23.grid(row=10,column=2)
    box24.grid(row=11,column=2)
    box25.grid(row=12,column=2)

    Label(root, text="Graph:").grid(row=13,column=0)
    Button(root, text='hot', command=hot,height=1,width=13).grid(row=13, column=1, sticky=W, pady=4)
    Button(root, text='cold', command=cold,height=1,width=13).grid(row=13, column=2, sticky=W, pady=4)
    Button(root, text='hot-cold', command=hot_cold,height=1,width=13).grid(row=13, column=3, sticky=W, pady=4)

    root.mainloop()


def koka2018_cur():
    path="C:\DataBase\Data_Processing\koka2017\Float_current\Raw_Data"
    dir1=os.listdir(path)#フォルダ名のリスト
    dir2=[f for f in dir1 if os.path.isdir(os.path.join(path,f))]
    ch=[]
    for i in range(len(dir2)):
        path2=path+"\\"+dir2[i]
        CH=os.listdir(path2)#CH名のリスト
        CH2=[f for f in CH if os.path.isdir(os.path.join(path2,f))]
        for j in range(len(CH2)):
            CH3=CH[j]
            ch.append(CH3)
    ch2=list(set(ch))
    ch2.sort()



    def Current_Data():
        Step_List=[DIR1.get(),DIR2.get(),DIR3.get(),DIR4.get(),DIR5.get(),DIR6.get(),DIR7.get(),DIR8.get()]
        while Step_List.count("")>0:
            Step_List.remove("")
        ch_List=[Ch1.get(),Ch2.get(),Ch3.get(),Ch4.get(),Ch5.get(),Ch6.get(),Ch7.get(),Ch8.get()]
        while ch_List.count("")>0:
            ch_List.remove("")
        initial_time=0.0
        time=[]
        current=[]
        Time2=[]
        for k in range(len(Step_List)):
            file_link=path+"\\"+Step_List[k]+"\\"+ch_List[k]+"\\"+"DetailData_CycleNo1.csv"
            df=pd.read_csv(file_link,encoding='cp932')
            Time=df[" ProcTime(s)"].values
            Current=df["Current(mA)"].values
            for l in range(len(Time)):

                time=Time[l]
                hour=float(time[0:-10])
                minute=float(time[-9:-7])
                second=float(time[-6:])
                all_hour=hour+minute/60+second/3600+initial_time
                Time2.append(all_hour)
                current.append(Current[l])
            initial_time=initial_time+max(Time2)

        TIME=pd.DataFrame(Time2)
        CURRENT=pd.DataFrame(current)
        DATA=pd.concat([TIME,CURRENT],axis=1)
        DATA.columns=["Time[min]","Current[mA]"]
        DATA0=pd.read_csv("C:\DataBase\Data_Processing\koka2017\Float_current\Current_Data.csv")
        DATA1=pd.concat([DATA0,DATA],axis=1)
        DATA1.to_csv("C:\DataBase\Data_Processing\koka2017\Float_current\Current_Data.csv",index=False)

    def popen_Data():
        FILE="C:\DataBase\Data_Processing\koka2017\Float_current\Current_Data.csv"
        subprocess.Popen(['C:\Program Files (x86)\Microsoft Office\Office15\EXCEL.EXE', FILE])

    def delete_Data():
        ddf=pd.read_csv("C:\DataBase\Data_Processing\koka2017\Float_current\Current_Data.csv")
        DF=ddf.iloc[:,0:1]
        DF.to_csv("C:\DataBase\Data_Processing\koka2017\Float_current\Current_Data.csv",index=False)

    root = Tk()
    DIR1=StringVar(root)
    DIR2=StringVar(root)
    DIR3=StringVar(root)
    DIR4=StringVar(root)
    DIR5=StringVar(root)
    DIR6=StringVar(root)
    DIR7=StringVar(root)
    DIR8=StringVar(root)
    Ch1=StringVar(root)
    Ch2=StringVar(root)
    Ch3=StringVar(root)
    Ch4=StringVar(root)
    Ch5=StringVar(root)
    Ch6=StringVar(root)
    Ch7=StringVar(root)
    Ch8=StringVar(root)

    Label(root, text="Step1:").grid(row=0,column=0)
    Label(root, text="Step2:").grid(row=1,column=0)
    Label(root, text="Step3:").grid(row=2,column=0)
    Label(root, text="Step4:").grid(row=3,column=0)
    Label(root, text="Step5:").grid(row=4,column=0)
    Label(root, text="Step6:").grid(row=5,column=0)
    Label(root, text="Step7:").grid(row=6,column=0)
    Label(root, text="Step8:").grid(row=7,column=0)

    dir_box1=ttk.Combobox(root,values=dir1,textvariable=DIR1,state="normal",width=35)
    dir_box2=ttk.Combobox(root,values=dir1,textvariable=DIR2,state="normal",width=35)
    dir_box3=ttk.Combobox(root,values=dir1,textvariable=DIR3,state="normal",width=35)
    dir_box4=ttk.Combobox(root,values=dir1,textvariable=DIR4,state="normal",width=35)
    dir_box5=ttk.Combobox(root,values=dir1,textvariable=DIR5,state="normal",width=35)
    dir_box6=ttk.Combobox(root,values=dir1,textvariable=DIR6,state="normal",width=35)
    dir_box7=ttk.Combobox(root,values=dir1,textvariable=DIR7,state="normal",width=35)
    dir_box8=ttk.Combobox(root,values=dir1,textvariable=DIR8,state="normal",width=35)
    dir_box1.grid(row=0,column=1)
    dir_box2.grid(row=1,column=1)
    dir_box3.grid(row=2,column=1)
    dir_box4.grid(row=3,column=1)
    dir_box5.grid(row=4,column=1)
    dir_box6.grid(row=5,column=1)
    dir_box7.grid(row=6,column=1)
    dir_box8.grid(row=7,column=1)

    ch_box1=ttk.Combobox(root,values=ch2,textvariable=Ch1,state="normal",width=13)
    ch_box2=ttk.Combobox(root,values=ch2,textvariable=Ch2,state="normal",width=13)
    ch_box3=ttk.Combobox(root,values=ch2,textvariable=Ch3,state="normal",width=13)
    ch_box4=ttk.Combobox(root,values=ch2,textvariable=Ch4,state="normal",width=13)
    ch_box5=ttk.Combobox(root,values=ch2,textvariable=Ch5,state="normal",width=13)
    ch_box6=ttk.Combobox(root,values=ch2,textvariable=Ch6,state="normal",width=13)
    ch_box7=ttk.Combobox(root,values=ch2,textvariable=Ch7,state="normal",width=13)
    ch_box8=ttk.Combobox(root,values=ch2,textvariable=Ch8,state="normal",width=13)
    ch_box1.grid(row=0,column=2)
    ch_box2.grid(row=1,column=2)
    ch_box3.grid(row=2,column=2)
    ch_box4.grid(row=3,column=2)
    ch_box5.grid(row=4,column=2)
    ch_box6.grid(row=5,column=2)
    ch_box7.grid(row=6,column=2)
    ch_box8.grid(row=7,column=2)

    Label(root, text="データ処理:").grid(row=8,column=0)
    Button(root, text='結合', command=Current_Data,height=1,width=13).grid(row=8, column=1, sticky=W, pady=4)
    Button(root, text='データ展開', command=popen_Data,height=1,width=13).grid(row=9, column=1, sticky=W, pady=4)
    Button(root, text='データ削除', command=delete_Data,height=1,width=13).grid(row=10, column=1, sticky=W, pady=4)
    root.mainloop()
def kouji():
    print("現在作成中のため使用できません。")

#tab-a、impotrについて
Label(tab_a, text="放電負荷特性：",foreground="red").grid(row=0,column=0)
Button(tab_a, text='放電負荷-import', command=import_dis).grid(row=0, column=1, sticky=W, pady=4)

Label(tab_a, text="充電負荷特性：",foreground="red").grid(row=1,column=0)
Button(tab_a, text='充電負荷-import', command=import_cha).grid(row=1, column=1, sticky=W, pady=4)

Label(tab_a, text="放電温度特性：",foreground="red").grid(row=2,column=0)
Button(tab_a, text='放電温特-import', command=import_distemp).grid(row=2, column=1, sticky=W, pady=4)

Label(tab_a, text="DCR：",foreground="red").grid(row=3,column=0)
Button(tab_a, text='DCR-import', command=import_dcr).grid(row=3, column=1, sticky=W, pady=4)

Label(tab_a, text="ACI：",foreground="red").grid(row=4,column=0)
Button(tab_a, text='ACI-import', command=import_aci).grid(row=4, column=1, sticky=W, pady=4)

Label(tab_a, text="フロート：",foreground="red").grid(row=5,column=0)
Button(tab_a, text='フロート-import', command=import_float).grid(row=5, column=1, sticky=W, pady=4)

Label(tab_a, text="保存：",foreground="red").grid(row=6,column=0)
Button(tab_a, text='保存-import', command=import_storage).grid(row=6, column=1, sticky=W, pady=4)

Label(tab_a, text="サイクル：",foreground="red").grid(row=7,column=0)
Button(tab_a, text='サイクル維持率-import', command=import_cyc).grid(row=7, column=1, sticky=W, pady=4)
Button(tab_a, text='サイクル静特性-import', command=import_cycsta).grid(row=8, column=1, sticky=W, pady=4)
Button(tab_a, text='サイクルカーブ-import', command=import_cyc_curve).grid(row=9, column=1, sticky=W, pady=4)

Label(tab_a, text="静特性：",foreground="red").grid(row=10,column=0)
Button(tab_a, text='静特性シート-import', command=import_static).grid(row=10, column=1, sticky=W, pady=4)

Label(tab_a, text="注意点1：",foreground="red").grid(row=11,column=1)
Label(tab_a, text="注意点2：",foreground="red").grid(row=12,column=1)
Label(tab_a, text="注意点3：",foreground="red").grid(row=13,column=1)
Label(tab_a, text="注意点4：",foreground="red").grid(row=14,column=1)

Label(tab_a, text="Cドライブ上にDataBaseフォルダを作成し各評価の必要フォルダを作成 or コピーする。",foreground="red").grid(row=11,column=2)
Label(tab_a, text="所定のExcelフォーマットに記入し、デスクトップ上に保存する。",foreground="red").grid(row=12,column=2)
Label(tab_a, text="取り込むExcelフォーマットは完成したものだけとする。",foreground="red").grid(row=13,column=2)
Label(tab_a, text="取り込みが完了したら「DataBase」フォルダ内の更新フォルダをサーバー上にアップする。",foreground="red").grid(row=14,column=2)

#結果表示タブ項目
Button(tab_b, text='放電負荷-Result', command=Result_dis).grid(row=0, column=0, sticky=W, pady=4)
Button(tab_b, text='充電負荷-Result', command=kouji).grid(row=1, column=0, sticky=W, pady=4)
Button(tab_b, text='放電温特-Result', command=kouji).grid(row=2, column=0, sticky=W, pady=4)
Button(tab_b, text='保存-Result(DataBase)', command=kouji).grid(row=3, column=0, sticky=W, pady=4)
Button(tab_b, text='保存-Result(途中結果)', command=kouji).grid(row=3, column=1, sticky=W, pady=4)
Button(tab_b, text='フロート-Result(DataBase)', command=kouji).grid(row=4, column=0, sticky=W, pady=4)
Button(tab_b, text='フロート-Result(途中結果)', command=float_result2).grid(row=4, column=1, sticky=W, pady=4)
Button(tab_b, text='サイクル-維持率-厚みResult(DataBase)', command=kouji).grid(row=5, column=0, sticky=W, pady=4)
Button(tab_b, text='サイクル-維持率-厚みResult(途中結果)', command=kouji).grid(row=5, column=1, sticky=W, pady=4)
Button(tab_b, text='サイクル-厚み-Result(DataBase)', command=kouji).grid(row=6, column=0, sticky=W, pady=4)
Button(tab_b, text='サイクル-厚み-Result(途中結果)', command=kouji).grid(row=6, column=1, sticky=W, pady=4)
Button(tab_b, text='ACI-Result', command=kouji).grid(row=7, column=0, sticky=W, pady=4)
Button(tab_b, text='静特性-Result(DataBase)', command=kouji).grid(row=8, column=0, sticky=W, pady=4)
Button(tab_b, text='静特性-Result(途中結果)', command=kouji).grid(row=8, column=1, sticky=W, pady=4)

Label(tab_b, text="注意点1：",foreground="red").grid(row=9,column=0)
Label(tab_b, text="注意点2：",foreground="red").grid(row=10,column=0)

Label(tab_b, text="DataBaseフォルダをコピーしてCドライブ上に置く。",foreground="red").grid(row=9,column=1)
Label(tab_b, text="途中結果表示は所定のExcelシートをPC内に置いて指定する。",foreground="red").grid(row=10,column=1)

#解析タブ項目
Label(tab_c, text="dVdQ-Curve",foreground="red").grid(row=0,column=0)
Button(tab_c, text='dVdQ-Graph(all)', command=kouji).grid(row=0, column=1, sticky=W, pady=4)
Button(tab_c, text='dVdQ-Graph(peak)', command=kouji).grid(row=1, column=1, sticky=W, pady=4)
Button(tab_c, text='dVdQ-Graph(by one)', command=kouji).grid(row=2, column=1, sticky=W, pady=4)
#データ加工タブ項目
Label(tab_d, text="工事中",foreground="red").grid(row=0,column=0)
#生データ処理タブ項目
Button(tab_e, text='杭可電子2017-フロート-積算電流値', command=koka2018_cur).grid(row=0, column=0, sticky=W, pady=4)

note.pack()
root2.mainloop()