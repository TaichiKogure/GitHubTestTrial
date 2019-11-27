'''
Created on 2018/05/28

@author: MM12069
'''
import datetime
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilenames

import numpy as np
import pandas as pd

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