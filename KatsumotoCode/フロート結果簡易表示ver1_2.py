'''
Created on 2018/05/16

@author: MM12069
'''
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilenames

import matplotlib as plt
import matplotlib.pyplot as plt
import pandas as pd

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

Label(root, text="Quit:").grid(row=14,column=0)
Button(root, text='終了', command=root.quit,height=1,width=13).grid(row=14, column=1, sticky=W, pady=4)

root.mainloop()
