'''
Created on 2018/04/09

@author: MM12069
'''
import os
from tkinter import *
from tkinter import ttk

import matplotlib as plt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

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
# df=pd.read_csv("C:\DataBase\Discharge_rate_Capability\Discharge_rate_Capability_used-cell.csv",encoding="cp932")
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

Label(root, text="Quit:").grid(row=14,column=0)
Button(root, text='終了', command=root.quit,height=1,width=13).grid(row=14, column=1, sticky=W, pady=4)

root.mainloop()