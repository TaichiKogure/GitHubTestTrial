'''
Created on 2018/08/10

@author: MM12069
'''
import os
import subprocess
from tkinter import *
from tkinter import ttk

import pandas as pd

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
    DF=ddf[:,0:1]
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
Label(root, text="Quit:").grid(row=11,column=0)
Button(root, text='終了', command=root.quit,height=1,width=13).grid(row=11, column=1, sticky=W, pady=4)
root.mainloop()
