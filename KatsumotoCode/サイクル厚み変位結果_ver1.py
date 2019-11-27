'''
Created on 2018/07/06

@author: MM12069
'''
import os
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilenames

import matplotlib as plt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#フォルダの指定--------------------------------------------
root=tkinter.Tk()
root.withdraw()
File_Link=askopenfilenames(filetypes=(("All files", "*.*"),("HTML files", "*.html;*.htm"),("csv files", "*.csv") ))#ファイルを選択
Length_Link=len(File_Link)#ファイルの長さを計算
cell_info=[]
#繰り返す---------------------------------------------------
for i in range(Length_Link):
    cell_info.append(File_Link[i])
cell_info2=[]
for f in cell_info:
    cell_info2.append(pd.read_excel(f,sheetname="Data_Sheet",encoding="cp932"))
df=pd.concat(cell_info2)

#saveデータのフォルダ一覧
path = "C:\DataBase\Cycle_Performance\Thickness\Save_Data"
File_dir= os.listdir(path)
path2 = "C:\DataBase\Cycle_Performance\Thickness\Raw_Data"
File_dir2= os.listdir(path2)

def Graph():
    Cycle_min=float(min1.get())
    thickness_min=float(min2.get())
    delta_thickness_min=float(min3.get())
    per_thickness_min=float(min4.get())
    Cycle_max=float(max1.get())
    thickness_max=float(max2.get())
    delta_thickness_max=float(max3.get())
    per_thickness_max=float(max4.get())

    title_size=int(a.get())
    axisN_size=int(b.get())
    axis_size=int(c.get())
    font=d.get()

    Graph1=graph1.get()
    Graph2=graph2.get()
    Graph3=graph3.get()
    Graph4=graph4.get()

    #グラフの種類
    Thickness1=thickness1.get()
    Thickness2=thickness2.get()
    Thickness3=thickness3.get()
    Thickness4=thickness4.get()

    title1=Graph1[0:-4]+"-"+Thickness1
    title2=Graph2[0:-4]+"-"+Thickness2
    title3=Graph3[0:-4]+"-"+Thickness3
    title4=Graph4[0:-4]+"-"+Thickness4

    Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get(),class7.get(),class8.get(),
              class9.get(),class10.get(),class11.get(),class12.get(),class13.get(),class14.get(),class15.get(),class16.get(),
              class17.get(),class18.get(),class19.get(),class20.get()]

    color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get(),color7.get(),color8.get(),color9.get(),color10.get(),
                 color11.get(),color12.get(),color13.get(),color14.get(),color15.get(),color16.get(),color17.get(),color18.get(),color19.get(),color20.get()]

    Legend_list=[Legend1.get(),Legend2.get(),Legend3.get(),Legend4.get(),Legend5.get(),Legend6.get()]#Lot名のリスト

    marker_list=[marker1.get(),marker2.get(),marker3.get(),marker4.get(),marker5.get(),marker6.get()]#マーカーのリスト
    for i in range(20):
        if(Lot_list[i]==""):
            pass
        else:
            if(Legend_list[i]==""):
                Legend_Name=Lot_list[i]
            elif(Legend_list[i]=="No-Name"):
                Legend_Name=Lot_list[i]
            else:
                Legend_Name=Legend_list[i]

            df2=df[df["Cell-Lot"]==Lot_list[i]]
            x_data=df2["Cycle_Number"].values.flatten()
            y1_data=df2[Graph1].values.flatten()
            y2_data=df2[Graph2].values.flatten()
            y3_data=df2[Graph3].values.flatten()
            y4_data=df2[Graph4].values.flatten()

            #厚みを定義
            x=x_data
            if(Thickness1=="thickness[mm]"):
                y1=y1_data
                y1_min=thickness_min
                y1_max=thickness_max
                inter1=float(interval2.get())
            elif(Thickness1=="delta_thickness"):
                y_standard_data=df2[df2["Cycle_Number"]==0]
                y_standard_data=y_standard_data[Graph1].values.flatten()
                y_standard=float(y_standard_data[0])
                y1=(y1_data-y_standard)*1000
                y1_min=delta_thickness_min
                y1_max=delta_thickness_max
                title2=title2+"µm"
                inter1=float(interval3.get())
            elif(Thickness1=="thickness[%]"):
                y_standard_data=df2[df2["Cycle_Number"]==0]
                y_standard_data=y_standard_data[Graph1].values.flatten()
                y_standard=float(y_standard_data[0])
                y1=(y1_data/y_standard-1.0)*100.0
                y1_min=per_thickness_min
                y1_max=per_thickness_max
                inter1=float(interval4.get())
            else:
                pass

            if(Thickness2=="thickness[mm]"):
                y2=y2_data
                y2_min=thickness_min
                y2_max=thickness_max
                inter2=float(interval2.get())
            elif(Thickness2=="delta_thickness"):
                y_standard_data=df2[df2["Cycle_Number"]==0]
                y_standard_data=y_standard_data[Graph1].values.flatten()
                y_standard=float(y_standard_data[0])
                y2=(y2_data-y_standard)*1000
                y2_min=delta_thickness_min
                y2_max=delta_thickness_max
                title2=title2+"µm"
                inter2=float(interval3.get())
            elif(Thickness2=="thickness[%]"):
                y_standard_data=df2[df2["Cycle_Number"]==0]
                y_standard_data=y_standard_data[Graph1].values.flatten()
                y_standard=float(y_standard_data[0])
                y2=(y2_data/y_standard-1.0)*100.0
                y2_min=per_thickness_min
                y2_max=per_thickness_max
                inter2=float(interval4.get())
            else:
                pass

            if(Thickness3=="thickness[mm]"):
                y3=y3_data
                y3_min=thickness_min
                y3_max=thickness_max
                inter3=float(interval2.get())
            elif(Thickness3=="delta_thickness"):
                y_standard_data=df2[df2["Cycle_Number"]==0]
                y_standard_data=y_standard_data[Graph1].values.flatten()
                y_standard=float(y_standard_data[0])
                y3=(y3_data-y_standard)*1000
                y3_min=delta_thickness_min
                y3_max=delta_thickness_max
                title2=title2+"µm"
                inter3=float(interval3.get())
            elif(Thickness3=="thickness[%]"):
                y_standard_data=df2[df2["Cycle_Number"]==0]
                y_standard_data=y_standard_data[Graph1].values.flatten()
                y_standard=float(y_standard_data[0])
                y3=(y3_data/y_standard-1.0)*100.0
                y3_min=per_thickness_min
                y3_max=per_thickness_max
                inter3=float(interval4.get())
            else:
                pass

            if(Thickness4=="thickness[mm]"):
                y4=y4_data
                y4_min=thickness_min
                y4_max=thickness_max
                inter4=float(interval2.get())
            elif(Thickness4=="delta_thickness"):
                y_standard_data=df2[df2["Cycle_Number"]==0]
                y_standard_data=y_standard_data[Graph1].values.flatten()
                y_standard=float(y_standard_data[0])
                y4=(y4_data-y_standard)*1000
                y4_min=delta_thickness_min
                y4_max=delta_thickness_max
                title2=title2+"µm"
                inter4=float(interval3.get())
            elif(Thickness4=="thickness[%]"):
                y_standard_data=df2[df2["Cycle_Number"]==0]
                y_standard_data=y_standard_data[Graph1].values.flatten()
                y_standard=float(y_standard_data[0])
                y4=(y4_data/y_standard-1.0)*100.0
                y4_min=per_thickness_min
                y4_max=per_thickness_max
                inter4=float(interval4.get())
            else:
                pass
            cm2=color_list1[i]

            plt.subplot(221)
            plt.title(title1,fontsize=title_size,fontname=font)
            plt.plot(x,y1,color=cm2,marker=marker_list[i],label=Legend_Name)
            plt.xlabel("Cycle-Number[-]",fontsize=axisN_size,fontname=font)
            plt.ylabel(title1,fontsize=axisN_size,fontname=font)
            plt.xlim(Cycle_min-5,Cycle_max+5)
            plt.ylim(y1_min,y1_max)
            plt.xticks(np.arange(Cycle_min,Cycle_max+float(interval1.get()),float(interval1.get())))
            plt.xticks(fontsize=axis_size,fontname=font)
            plt.yticks(np.arange(y1_min,y1_max+inter1,inter1))
            plt.yticks(fontsize=axis_size,fontname=font)
            plt.grid(True)
            plt.legend()

            plt.subplot(222)
            plt.title(title2,fontsize=title_size,fontname=font)
            plt.plot(x,y2,color=cm2,marker=marker_list[i],label=Legend_Name)
            plt.xlabel("Cycle-Number[-]",fontsize=axisN_size,fontname=font)
            plt.ylabel(title2,fontsize=axisN_size,fontname=font)
            plt.xlim(Cycle_min-5,Cycle_max+5)
            plt.ylim(y2_min,y2_max)
            plt.xticks(np.arange(Cycle_min,Cycle_max+float(interval1.get()),float(interval1.get())))
            plt.xticks(fontsize=axis_size,fontname=font)
            plt.yticks(np.arange(y2_min,y2_max+inter2,inter2))
            plt.yticks(fontsize=axis_size,fontname=font)
            plt.grid(True)
            plt.legend()

            plt.subplot(223)
            plt.title(title3,fontsize=title_size,fontname=font)
            plt.plot(x,y3,color=cm2,marker=marker_list[i],label=Legend_Name)
            plt.xlabel("Cycle-Number[-]",fontsize=axisN_size,fontname=font)
            plt.ylabel(title3,fontsize=axisN_size,fontname=font)
            plt.xlim(Cycle_min-5,Cycle_max+5)
            plt.ylim(y3_min,y3_max)
            plt.xticks(np.arange(Cycle_min,Cycle_max+float(interval1.get()),float(interval1.get())))
            plt.xticks(fontsize=axis_size,fontname=font)
            plt.yticks(np.arange(y3_min,y3_max+inter3,inter3))
            plt.yticks(fontsize=axis_size,fontname=font)
            plt.grid(True)
            plt.legend()

            plt.subplot(224)
            plt.title(title4,fontsize=title_size,fontname=font)
            plt.plot(x,y4,color=cm2,marker=marker_list[i],label=Legend_Name)
            plt.xlabel("Cycle-Number[-]",fontsize=axisN_size,fontname=font)
            plt.ylabel(title4,fontsize=axisN_size,fontname=font)
            plt.xlim(Cycle_min-5,Cycle_max+5)
            plt.ylim(y4_min,y4_max)
            plt.xticks(np.arange(Cycle_min,Cycle_max+float(interval1.get()),float(interval1.get())))
            plt.xticks(fontsize=axis_size,fontname=font)
            plt.yticks(np.arange(y4_min,y4_max+inter4,inter4))
            plt.yticks(fontsize=axis_size,fontname=font)
            plt.grid(True)
            plt.legend()

    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    plt.show()

def save():
    Lot_list=[class1.get(),class2.get(),class3.get(),class4.get(),class5.get(),class6.get(),class7.get(),class8.get(),
              class9.get(),class10.get(),class11.get(),class12.get(),class13.get(),class14.get(),class15.get(),class16.get(),
              class17.get(),class18.get(),class19.get(),class20.get()]

    color_list1=[color1.get(),color2.get(),color3.get(),color4.get(),color5.get(),color6.get(),color7.get(),color8.get(),color9.get(),color10.get(),
                 color11.get(),color12.get(),color13.get(),color14.get(),color15.get(),color16.get(),color17.get(),color18.get(),color19.get(),color20.get()]

    if(Legend1.get()==""):
        legend1=class1.get()
    else:
        legend1=Legend1.get()

    if(Legend2.get()==""):
        legend2=class2.get()
    else:
        legend2=Legend2.get()

    if(Legend3.get()==""):
        legend3=class3.get()
    else:
        legend3=Legend3.get()

    if(Legend4.get()==""):
        legend4=class4.get()
    else:
        legend4=Legend4.get()

    if(Legend5.get()==""):
        legend5=class5.get()
    else:
        legend5=Legend5.get()

    if(Legend6.get()==""):
        legend6=class6.get()
    else:
        legend6=Legend6.get()

    if(Legend7.get()==""):
        legend7=class7.get()
    else:
        legend7=Legend7.get()

    if(Legend8.get()==""):
        legend8=class8.get()
    else:
        legend8=Legend8.get()

    if(Legend9.get()==""):
        legend9=class9.get()
    else:
        legend9=Legend9.get()

    if(Legend10.get()==""):
        legend10=class10.get()
    else:
        legend10=Legend10.get()

    if(Legend11.get()==""):
        legend11=class11.get()
    else:
        legend11=Legend11.get()

    if(Legend12.get()==""):
        legend12=class12.get()
    else:
        legend12=Legend12.get()

    if(Legend13.get()==""):
        legend13=class13.get()
    else:
        legend13=Legend13.get()

    if(Legend14.get()==""):
        legend14=class14.get()
    else:
        legend14=Legend14.get()

    if(Legend15.get()==""):
        legend15=class15.get()
    else:
        legend15=Legend15.get()

    if(Legend16.get()==""):
        legend16=class16.get()
    else:
        legend16=Legend16.get()

    if(Legend17.get()==""):
        legend17=class17.get()
    else:
        legend17=Legend17.get()

    if(Legend18.get()==""):
        legend18=class18.get()
    else:
        legend18=Legend18.get()

    if(Legend19.get()==""):
        legend19=class19.get()
    else:
        legend19=Legend19.get()

    if(Legend20.get()==""):
        legend20=class20.get()
    else:
        legend20=Legend20.get()

    Legend_list=[legend1,legend2,legend3,legend4,legend5,legend6,legend7,legend8,legend9,legend10,
                 legend11,legend12,legend13,legend14,legend15,legend16,legend17,legend18,legend19,legend20]#Lot名のリスト

    marker_list=[marker1.get(),marker2.get(),marker3.get(),marker4.get(),marker5.get(),marker6.get()]#マーカーのリスト

    d1=pd.DataFrame(Lot_list)
    d2=pd.DataFrame(color_list1)
    d3=pd.DataFrame(Legend_list)
    d4=pd.DataFrame(marker_list)
    d1.columns=["Lot_list"]
    d2.columns=["color_list"]
    d3.columns=["Legend_list"]
    d4.columns=["marker_list"]

    ddf=pd.concat([d1,d2,d3,d4],axis=1)

    data_csv=SaveFile.get()[-4:]
    if(data_csv==".csv"):
        save_link=path+"\\"+SaveFile.get()
    else:
        save_link=path+"\\"+SaveFile.get()+".csv"

    ddf.to_csv(save_link,index=False)
    print("データ保存完了")

def call():
    Cycle_min=float(min1.get())
    thickness_min=float(min2.get())
    delta_thickness_min=float(min3.get())
    per_thickness_min=float(min4.get())
    Cycle_max=float(max1.get())
    thickness_max=float(max2.get())
    delta_thickness_max=float(max3.get())
    per_thickness_max=float(max4.get())

    title_size=int(a.get())
    axisN_size=int(b.get())
    axis_size=int(c.get())
    font=d.get()

    Graph1=graph1.get()
    Graph2=graph2.get()
    Graph3=graph3.get()
    Graph4=graph4.get()

    #グラフの種類
    Thickness1=thickness1.get()
    Thickness2=thickness2.get()
    Thickness3=thickness3.get()
    Thickness4=thickness4.get()

    title1=Graph1[0:-4]+"-"+Thickness1
    title2=Graph2[0:-4]+"-"+Thickness2
    title3=Graph3[0:-4]+"-"+Thickness3
    title4=Graph4[0:-4]+"-"+Thickness4

    data_csv=SaveFile.get()[-4:]
    if(data_csv==".csv"):
        save_link=path+"\\"+SaveFile.get()
    else:
        save_link=path+"\\"+SaveFile.get()+".csv"
    ddf=pd.read_csv(save_link,encoding='cp932',engine='python')

    d1=ddf["Lot_list"]
    d2=ddf["color_list"]
    d3=ddf["Legend_list"]
    d4=ddf["marker_list"]
    d1=d1.dropna(axis=0,how="all")

    Lot_list=list(d1.values.flatten())
    Len_Lot=len(Lot_list)
    color_list1=list(d2.values.flatten())
    Legend_list=list(d3.values.flatten())
    marker_list=list(d4.values.flatten())

    for i in range(Len_Lot):
        if(Lot_list[i]==""):
            pass
        else:
            if(Legend_list[i]==""):
                Legend_Name=Lot_list[i]
            elif(Legend_list[i]=="No-Name"):
                Legend_Name=Lot_list[i]
            else:
                Legend_Name=Legend_list[i]

            df2=df[df["Cell-Lot"]==Lot_list[i]]
            x_data=df2["Cycle_Number"].values.flatten()
            y1_data=df2[Graph1].values.flatten()
            y2_data=df2[Graph2].values.flatten()
            y3_data=df2[Graph3].values.flatten()
            y4_data=df2[Graph4].values.flatten()

            #厚みを定義
            x=x_data
            if(Thickness1=="thickness[mm]"):
                y1=y1_data
                y1_min=thickness_min
                y1_max=thickness_max
                inter1=float(interval2.get())
            elif(Thickness1=="delta_thickness"):
                y_standard_data=df2[df2["Cycle_Number"]==0]
                y_standard_data=y_standard_data[Graph1].values.flatten()
                y_standard=float(y_standard_data[0])
                y1=(y1_data-y_standard)*1000
                y1_min=delta_thickness_min
                y1_max=delta_thickness_max
                title2=title2+"µm"
                inter1=float(interval3.get())
            elif(Thickness1=="thickness[%]"):
                y_standard_data=df2[df2["Cycle_Number"]==0]
                y_standard_data=y_standard_data[Graph1].values.flatten()
                y_standard=float(y_standard_data[0])
                y1=(y1_data/y_standard-1.0)*100.0
                y1_min=per_thickness_min
                y1_max=per_thickness_max
                inter1=float(interval4.get())
            else:
                pass

            if(Thickness2=="thickness[mm]"):
                y2=y2_data
                y2_min=thickness_min
                y2_max=thickness_max
                inter2=float(interval2.get())
            elif(Thickness2=="delta_thickness"):
                y_standard_data=df2[df2["Cycle_Number"]==0]
                y_standard_data=y_standard_data[Graph1].values.flatten()
                y_standard=float(y_standard_data[0])
                y2=(y2_data-y_standard)*1000
                y2_min=delta_thickness_min
                y2_max=delta_thickness_max
                title2=title2+"µm"
                inter2=float(interval3.get())
            elif(Thickness2=="thickness[%]"):
                y_standard_data=df2[df2["Cycle_Number"]==0]
                y_standard_data=y_standard_data[Graph1].values.flatten()
                y_standard=float(y_standard_data[0])
                y2=(y2_data/y_standard-1.0)*100.0
                y2_min=per_thickness_min
                y2_max=per_thickness_max
                inter2=float(interval4.get())
            else:
                pass

            if(Thickness3=="thickness[mm]"):
                y3=y3_data
                y3_min=thickness_min
                y3_max=thickness_max
                inter3=float(interval2.get())
            elif(Thickness3=="delta_thickness"):
                y_standard_data=df2[df2["Cycle_Number"]==0]
                y_standard_data=y_standard_data[Graph1].values.flatten()
                y_standard=float(y_standard_data[0])
                y3=(y3_data-y_standard)*1000
                y3_min=delta_thickness_min
                y3_max=delta_thickness_max
                title2=title2+"µm"
                inter3=float(interval3.get())
            elif(Thickness3=="thickness[%]"):
                y_standard_data=df2[df2["Cycle_Number"]==0]
                y_standard_data=y_standard_data[Graph1].values.flatten()
                y_standard=float(y_standard_data[0])
                y3=(y3_data/y_standard-1.0)*100.0
                y3_min=per_thickness_min
                y3_max=per_thickness_max
                inter3=float(interval4.get())
            else:
                pass

            if(Thickness4=="thickness[mm]"):
                y4=y4_data
                y4_min=thickness_min
                y4_max=thickness_max
                inter4=float(interval2.get())
            elif(Thickness4=="delta_thickness"):
                y_standard_data=df2[df2["Cycle_Number"]==0]
                y_standard_data=y_standard_data[Graph1].values.flatten()
                y_standard=float(y_standard_data[0])
                y4=(y4_data-y_standard)*1000
                y4_min=delta_thickness_min
                y4_max=delta_thickness_max
                title2=title2+"µm"
                inter4=float(interval3.get())
            elif(Thickness4=="thickness[%]"):
                y_standard_data=df2[df2["Cycle_Number"]==0]
                y_standard_data=y_standard_data[Graph1].values.flatten()
                y_standard=float(y_standard_data[0])
                y4=(y4_data/y_standard-1.0)*100.0
                y4_min=per_thickness_min
                y4_max=per_thickness_max
                inter4=float(interval4.get())
            else:
                pass
            cm2=color_list1[i]

            plt.subplot(221)
            plt.title(title1,fontsize=title_size,fontname=font)
            plt.plot(x,y1,color=cm2,marker=marker_list[i],label=Legend_Name)
            plt.xlabel("Cycle-Number[-]",fontsize=axisN_size,fontname=font)
            plt.ylabel(title1,fontsize=axisN_size,fontname=font)
            plt.xlim(Cycle_min-5,Cycle_max+5)
            plt.ylim(y1_min,y1_max)
            plt.xticks(np.arange(Cycle_min,Cycle_max+float(interval1.get()),float(interval1.get())))
            plt.xticks(fontsize=axis_size,fontname=font)
            plt.yticks(np.arange(y1_min,y1_max+inter1,inter1))
            plt.yticks(fontsize=axis_size,fontname=font)
            plt.grid(True)
            plt.legend()

            plt.subplot(222)
            plt.title(title2,fontsize=title_size,fontname=font)
            plt.plot(x,y2,color=cm2,marker=marker_list[i],label=Legend_Name)
            plt.xlabel("Cycle-Number[-]",fontsize=axisN_size,fontname=font)
            plt.ylabel(title2,fontsize=axisN_size,fontname=font)
            plt.xlim(Cycle_min-5,Cycle_max+5)
            plt.ylim(y2_min,y2_max)
            plt.xticks(np.arange(Cycle_min,Cycle_max+float(interval1.get()),float(interval1.get())))
            plt.xticks(fontsize=axis_size,fontname=font)
            plt.yticks(np.arange(y2_min,y2_max+inter2,inter2))
            plt.yticks(fontsize=axis_size,fontname=font)
            plt.grid(True)
            plt.legend()

            plt.subplot(223)
            plt.title(title3,fontsize=title_size,fontname=font)
            plt.plot(x,y3,color=cm2,marker=marker_list[i],label=Legend_Name)
            plt.xlabel("Cycle-Number[-]",fontsize=axisN_size,fontname=font)
            plt.ylabel(title3,fontsize=axisN_size,fontname=font)
            plt.xlim(Cycle_min-5,Cycle_max+5)
            plt.ylim(y3_min,y3_max)
            plt.xticks(np.arange(Cycle_min,Cycle_max+float(interval1.get()),float(interval1.get())))
            plt.xticks(fontsize=axis_size,fontname=font)
            plt.yticks(np.arange(y3_min,y3_max+inter3,inter3))
            plt.yticks(fontsize=axis_size,fontname=font)
            plt.grid(True)
            plt.legend()

            plt.subplot(224)
            plt.title(title4,fontsize=title_size,fontname=font)
            plt.plot(x,y4,color=cm2,marker=marker_list[i],label=Legend_Name)
            plt.xlabel("Cycle-Number[-]",fontsize=axisN_size,fontname=font)
            plt.ylabel(title4,fontsize=axisN_size,fontname=font)
            plt.xlim(Cycle_min-5,Cycle_max+5)
            plt.ylim(y4_min,y4_max)
            plt.xticks(np.arange(Cycle_min,Cycle_max+float(interval1.get()),float(interval1.get())))
            plt.xticks(fontsize=axis_size,fontname=font)
            plt.yticks(np.arange(y4_min,y4_max+inter4,inter4))
            plt.yticks(fontsize=axis_size,fontname=font)
            plt.grid(True)
            plt.legend()

    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    plt.show()


List_Legend=["No-Name"]
df2=df.dropna(axis=0,how='all')
List_cell_Lot=list(set(list(df2["Cell-Lot"].values.flatten())))
List_cell_Lot.sort()
List_color=['k','b','r','g','orange','darkviolet','aqua','lime']#カラーパレットの作成
marker_list=[".", ",", "o", "v", "^", "<", ">", "1", "2", "3","4", "8", "s", "p", "*", "h", "H", "+", "x", "D","d", "|", "_", "None"]
fontsize_list=[4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
fontname_list=["serif","sans-serif","cursive","fantasy","monospace"]
graph_list=["thickness_plate[mm]","thickness_Al[mm]","thickness_Ni[mm]","thickness_Center[mm]","50g-thickness_plate[mm]",
            "emboss[mm]","flat[mm]","point1[mm]","point2[mm]","point3[mm]","point4[mm]","point5[mm]","point6[mm]",
            "point7[mm]","point8[mm]","point9[mm]","point10[mm]","point11[mm]","point12[mm]","plate-bottomside[mm]","plate-topside[mm]"]
thickness_list=["thickness[mm]","delta_thickness","thickness[%]"]
#GUI
root = Tk()
root.title("Thickness-of Cycle Performance-Result")

a=StringVar(root)
b=StringVar(root)
c=StringVar(root)
d=StringVar(root)
graph1=StringVar(root)
graph2=StringVar(root)
graph3=StringVar(root)
graph4=StringVar(root)
thickness1=StringVar(root)
thickness2=StringVar(root)
thickness3=StringVar(root)
thickness4=StringVar(root)
Legend1=StringVar(root)
Legend2=StringVar(root)
Legend3=StringVar(root)
Legend4=StringVar(root)
Legend5=StringVar(root)
Legend6=StringVar(root)
Legend7=StringVar(root)
Legend8=StringVar(root)
Legend9=StringVar(root)
Legend10=StringVar(root)
Legend11=StringVar(root)
Legend12=StringVar(root)
Legend13=StringVar(root)
Legend14=StringVar(root)
Legend15=StringVar(root)
Legend16=StringVar(root)
Legend17=StringVar(root)
Legend18=StringVar(root)
Legend19=StringVar(root)
Legend20=StringVar(root)
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
color13=StringVar(root)
color14=StringVar(root)
color15=StringVar(root)
color16=StringVar(root)
color17=StringVar(root)
color18=StringVar(root)
color19=StringVar(root)
color20=StringVar(root)
marker1=StringVar(root)
marker2=StringVar(root)
marker3=StringVar(root)
marker4=StringVar(root)
marker5=StringVar(root)
marker6=StringVar(root)
marker7=StringVar(root)
marker8=StringVar(root)
marker9=StringVar(root)
marker10=StringVar(root)
marker11=StringVar(root)
marker12=StringVar(root)
marker13=StringVar(root)
marker14=StringVar(root)
marker15=StringVar(root)
marker16=StringVar(root)
marker17=StringVar(root)
marker18=StringVar(root)
marker19=StringVar(root)
marker20=StringVar(root)
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
class13=StringVar(root)
class14=StringVar(root)
class15=StringVar(root)
class16=StringVar(root)
class17=StringVar(root)
class18=StringVar(root)
class19=StringVar(root)
class20=StringVar(root)
SaveFile=StringVar(root)


Label(root, text="fontsize(タイトル)").grid(row=0,column=0)
Label(root, text="fontsize(軸名)").grid(row=1,column=0)
Label(root, text="fontsize(軸)").grid(row=2,column=0)
Label(root, text="fontname").grid(row=3,column=0)
box1=ttk.Combobox(root, values=fontsize_list,textvariable=a,state="normal",width=10)
box1.grid(row=0,column=1)
box1.set("12")
box2=ttk.Combobox(root, values=fontsize_list,textvariable=b,state="normal",width=10)
box2.grid(row=1,column=1)
box2.set("10")
box3=ttk.Combobox(root, values=fontsize_list,textvariable=c,state="normal",width=10)
box3.grid(row=2,column=1)
box3.set("9")
box4=ttk.Combobox(root, values=fontname_list,textvariable=d,state="normal",width=10)
box4.grid(row=3,column=1)
box4.set("serif")

Label(root, text="cyc/min/max/inter").grid(row=0,column=2)
Label(root, text="thick/min/max/inter").grid(row=1,column=2)
Label(root, text="delta/min/max/inter").grid(row=2,column=2)
Label(root, text="%/min/max/inter").grid(row=3,column=2)

min1=Entry(root,width=8)
min2=Entry(root,width=8)
min3=Entry(root,width=8)
min4=Entry(root,width=8)
max1=Entry(root,width=8)
max2=Entry(root,width=8)
max3=Entry(root,width=8)
max4=Entry(root,width=8)
interval1=Entry(root,width=8)
interval2=Entry(root,width=8)
interval3=Entry(root,width=8)
interval4=Entry(root,width=8)


min1.grid(row=0, column=3)
min1.insert(0,0)
min2.grid(row=1, column=3)
min2.insert(0,3.0)
min3.grid(row=2, column=3)
min3.insert(0,0)
min4.grid(row=3, column=3)
min4.insert(0,0)

max1.grid(row=0, column=4)
max1.insert(0,1000)
max2.grid(row=1, column=4)
max2.insert(0,4.0)
max3.grid(row=2, column=4)
max3.insert(0,500)
max4.grid(row=3, column=4)
max4.insert(0,20)

interval1.grid(row=0,column=5)
interval2.grid(row=1,column=5)
interval3.grid(row=2,column=5)
interval4.grid(row=3,column=5)
interval1.insert(0,50)
interval2.insert(0,0.2)
interval3.insert(0,50)
interval4.insert(0,2.5)

Label(root, text="Graph1:").grid(row=0,column=6)
Label(root, text="Graph2:").grid(row=1,column=6)
Label(root, text="Graph3:").grid(row=2,column=6)
Label(root, text="Graph4:").grid(row=3,column=6)
graph_box1=ttk.Combobox(root, values=graph_list,textvariable=graph1,state="normal",width=13)
graph_box1.set("thickness_plate[mm]")
graph_box1.grid(row=0,column=7)
graph_box2=ttk.Combobox(root, values=graph_list,textvariable=graph2,state="normal",width=13)
graph_box2.set("thickness_Al[mm]")
graph_box2.grid(row=1,column=7)
graph_box3=ttk.Combobox(root, values=graph_list,textvariable=graph3,state="normal",width=13)
graph_box3.set("thickness_Ni[mm]")
graph_box3.grid(row=2,column=7)
graph_box4=ttk.Combobox(root, values=graph_list,textvariable=graph4,state="normal",width=13)
graph_box4.set("thickness_Center[mm]")
graph_box4.grid(row=3,column=7)
thickness_box1=ttk.Combobox(root, values=thickness_list,textvariable=thickness1,state="normal",width=13)
thickness_box1.set("thickness[%]")
thickness_box1.grid(row=0,column=8)
thickness_box2=ttk.Combobox(root, values=thickness_list,textvariable=thickness2,state="normal",width=13)
thickness_box2.set("thickness[%]")
thickness_box2.grid(row=1,column=8)
thickness_box3=ttk.Combobox(root, values=thickness_list,textvariable=thickness3,state="normal",width=13)
thickness_box3.set("thickness[%]")
thickness_box3.grid(row=2,column=8)
thickness_box4=ttk.Combobox(root, values=thickness_list,textvariable=thickness4,state="normal",width=13)
thickness_box4.set("thickness[%]")
thickness_box4.grid(row=3,column=8)

Label(root, text="Color").grid(row=4,column=1)
Label(root, text="marker").grid(row=4,column=2)
Label(root, text="Legend").grid(row=4,column=3)
Label(root, text="Lot-Name").grid(row=4,column=4)
Label(root, text="Color").grid(row=4,column=6)
Label(root, text="marker").grid(row=4,column=7)
Label(root, text="Legend").grid(row=4,column=8)
Label(root, text="Lot-Name").grid(row=4,column=9)

Label(root, text="Lot1:").grid(row=5,column=0)
Label(root, text="Lot2:").grid(row=6,column=0)
Label(root, text="Lot3:").grid(row=7,column=0)
Label(root, text="Lot4:").grid(row=8,column=0)
Label(root, text="Lot5:").grid(row=9,column=0)
Label(root, text="Lot6:").grid(row=10,column=0)
Label(root, text="Lot7:").grid(row=11,column=0)
Label(root, text="Lot8:").grid(row=12,column=0)
Label(root, text="Lot9:").grid(row=13,column=0)
Label(root, text="Lot10:").grid(row=14,column=0)
Label(root, text="Lot11:").grid(row=5,column=5)
Label(root, text="Lot12:").grid(row=6,column=5)
Label(root, text="Lot13:").grid(row=7,column=5)
Label(root, text="Lot14:").grid(row=8,column=5)
Label(root, text="Lot15:").grid(row=9,column=5)
Label(root, text="Lot16:").grid(row=10,column=5)
Label(root, text="Lot17:").grid(row=11,column=5)
Label(root, text="Lot18:").grid(row=12,column=5)
Label(root, text="Lot19:").grid(row=13,column=5)
Label(root, text="Lot20:").grid(row=14,column=5)

color_box1=ttk.Combobox(root, values=List_color,textvariable=color1,state="normal",width=10).grid(row=5,column=1)
color_box2=ttk.Combobox(root, values=List_color,textvariable=color2,state="normal",width=10).grid(row=6,column=1)
color_box3=ttk.Combobox(root, values=List_color,textvariable=color3,state="normal",width=10).grid(row=7,column=1)
color_box4=ttk.Combobox(root, values=List_color,textvariable=color4,state="normal",width=10).grid(row=8,column=1)
color_box5=ttk.Combobox(root, values=List_color,textvariable=color5,state="normal",width=10).grid(row=9,column=1)
color_box6=ttk.Combobox(root, values=List_color,textvariable=color6,state="normal",width=10).grid(row=10,column=1)
color_box7=ttk.Combobox(root, values=List_color,textvariable=color7,state="normal",width=10).grid(row=11,column=1)
color_box8=ttk.Combobox(root, values=List_color,textvariable=color8,state="normal",width=10).grid(row=12,column=1)
color_box9=ttk.Combobox(root, values=List_color,textvariable=color9,state="normal",width=10).grid(row=13,column=1)
color_box10=ttk.Combobox(root, values=List_color,textvariable=color10,state="normal",width=10).grid(row=14,column=1)
color_box11=ttk.Combobox(root, values=List_color,textvariable=color11,state="normal",width=10).grid(row=5,column=6)
color_box12=ttk.Combobox(root, values=List_color,textvariable=color12,state="normal",width=10).grid(row=6,column=6)
color_box13=ttk.Combobox(root, values=List_color,textvariable=color13,state="normal",width=10).grid(row=7,column=6)
color_box14=ttk.Combobox(root, values=List_color,textvariable=color14,state="normal",width=10).grid(row=8,column=6)
color_box15=ttk.Combobox(root, values=List_color,textvariable=color15,state="normal",width=10).grid(row=9,column=6)
color_box16=ttk.Combobox(root, values=List_color,textvariable=color16,state="normal",width=10).grid(row=10,column=6)
color_box17=ttk.Combobox(root, values=List_color,textvariable=color17,state="normal",width=10).grid(row=11,column=6)
color_box18=ttk.Combobox(root, values=List_color,textvariable=color18,state="normal",width=10).grid(row=12,column=6)
color_box19=ttk.Combobox(root, values=List_color,textvariable=color19,state="normal",width=10).grid(row=13,column=6)
color_box20=ttk.Combobox(root, values=List_color,textvariable=color20,state="normal",width=10).grid(row=14,column=6)

marker_box1=ttk.Combobox(root, values=marker_list,textvariable=marker1,state="normal",width=13)
marker_box1.set("o")
marker_box1.grid(row=5,column=2)
marker_box2=ttk.Combobox(root, values=marker_list,textvariable=marker2,state="normal",width=13)
marker_box2.set("o")
marker_box2.grid(row=6,column=2)
marker_box3=ttk.Combobox(root, values=marker_list,textvariable=marker3,state="normal",width=13)
marker_box3.set("o")
marker_box3.grid(row=7,column=2)
marker_box4=ttk.Combobox(root, values=marker_list,textvariable=marker4,state="normal",width=13)
marker_box4.grid(row=8,column=2)
marker_box5=ttk.Combobox(root, values=marker_list,textvariable=marker5,state="normal",width=13)
marker_box5.grid(row=9,column=2)
marker_box6=ttk.Combobox(root, values=marker_list,textvariable=marker6,state="normal",width=13)
marker_box6.grid(row=10,column=2)
marker_box7=ttk.Combobox(root, values=marker_list,textvariable=marker7,state="normal",width=13)
marker_box7.grid(row=11,column=2)
marker_box8=ttk.Combobox(root, values=marker_list,textvariable=marker8,state="normal",width=13)
marker_box8.grid(row=12,column=2)
marker_box9=ttk.Combobox(root, values=marker_list,textvariable=marker9,state="normal",width=13)
marker_box9.grid(row=13,column=2)
marker_box10=ttk.Combobox(root, values=marker_list,textvariable=marker10,state="normal",width=13)
marker_box10.grid(row=14,column=2)
marker_box11=ttk.Combobox(root, values=marker_list,textvariable=marker11,state="normal",width=13)
marker_box11.grid(row=5,column=7)
marker_box12=ttk.Combobox(root, values=marker_list,textvariable=marker12,state="normal",width=13)
marker_box12.grid(row=6,column=7)
marker_box13=ttk.Combobox(root, values=marker_list,textvariable=marker13,state="normal",width=13)
marker_box13.grid(row=7,column=7)
marker_box14=ttk.Combobox(root, values=marker_list,textvariable=marker14,state="normal",width=13)
marker_box14.grid(row=8,column=7)
marker_box15=ttk.Combobox(root, values=marker_list,textvariable=marker15,state="normal",width=13)
marker_box15.grid(row=9,column=7)
marker_box16=ttk.Combobox(root, values=marker_list,textvariable=marker16,state="normal",width=13)
marker_box16.grid(row=10,column=7)
marker_box17=ttk.Combobox(root, values=marker_list,textvariable=marker17,state="normal",width=13)
marker_box17.grid(row=11,column=7)
marker_box18=ttk.Combobox(root, values=marker_list,textvariable=marker18,state="normal",width=13)
marker_box18.grid(row=12,column=7)
marker_box19=ttk.Combobox(root, values=marker_list,textvariable=marker19,state="normal",width=13)
marker_box19.grid(row=13,column=7)
marker_box20=ttk.Combobox(root, values=marker_list,textvariable=marker20,state="normal",width=13)
marker_box20.grid(row=14,column=7)

Legend_box1=ttk.Combobox(root, values=List_Legend,textvariable=Legend1,state="normal",width=13).grid(row=5,column=3)
Legend_box2=ttk.Combobox(root, values=List_Legend,textvariable=Legend2,state="normal",width=13).grid(row=6,column=3)
Legend_box3=ttk.Combobox(root, values=List_Legend,textvariable=Legend3,state="normal",width=13).grid(row=7,column=3)
Legend_box4=ttk.Combobox(root, values=List_Legend,textvariable=Legend4,state="normal",width=13).grid(row=8,column=3)
Legend_box5=ttk.Combobox(root, values=List_Legend,textvariable=Legend5,state="normal",width=13).grid(row=9,column=3)
Legend_box6=ttk.Combobox(root, values=List_Legend,textvariable=Legend6,state="normal",width=13).grid(row=10,column=3)
Legend_box7=ttk.Combobox(root, values=List_Legend,textvariable=Legend7,state="normal",width=13).grid(row=11,column=3)
Legend_box8=ttk.Combobox(root, values=List_Legend,textvariable=Legend8,state="normal",width=13).grid(row=12,column=3)
Legend_box9=ttk.Combobox(root, values=List_Legend,textvariable=Legend9,state="normal",width=13).grid(row=13,column=3)
Legend_box10=ttk.Combobox(root, values=List_Legend,textvariable=Legend10,state="normal",width=13).grid(row=14,column=3)
Legend_box11=ttk.Combobox(root, values=List_Legend,textvariable=Legend11,state="normal",width=13).grid(row=5,column=8)
Legend_box12=ttk.Combobox(root, values=List_Legend,textvariable=Legend12,state="normal",width=13).grid(row=6,column=8)
Legend_box13=ttk.Combobox(root, values=List_Legend,textvariable=Legend13,state="normal",width=13).grid(row=7,column=8)
Legend_box14=ttk.Combobox(root, values=List_Legend,textvariable=Legend14,state="normal",width=13).grid(row=8,column=8)
Legend_box15=ttk.Combobox(root, values=List_Legend,textvariable=Legend15,state="normal",width=13).grid(row=9,column=8)
Legend_box16=ttk.Combobox(root, values=List_Legend,textvariable=Legend16,state="normal",width=13).grid(row=10,column=8)
Legend_box17=ttk.Combobox(root, values=List_Legend,textvariable=Legend17,state="normal",width=13).grid(row=11,column=8)
Legend_box18=ttk.Combobox(root, values=List_Legend,textvariable=Legend18,state="normal",width=13).grid(row=12,column=8)
Legend_box19=ttk.Combobox(root, values=List_Legend,textvariable=Legend19,state="normal",width=13).grid(row=13,column=8)
Legend_box20=ttk.Combobox(root, values=List_Legend,textvariable=Legend20,state="normal",width=13).grid(row=14,column=8)

class_box1=ttk.Combobox(root, values=List_cell_Lot,textvariable=class1,state="normal",width=28).grid(row=5,column=4)
class_box2=ttk.Combobox(root, values=List_cell_Lot,textvariable=class2,state="normal",width=28).grid(row=6,column=4)
class_box3=ttk.Combobox(root, values=List_cell_Lot,textvariable=class3,state="normal",width=28).grid(row=7,column=4)
class_box4=ttk.Combobox(root, values=List_cell_Lot,textvariable=class4,state="normal",width=28).grid(row=8,column=4)
class_box5=ttk.Combobox(root, values=List_cell_Lot,textvariable=class5,state="normal",width=28).grid(row=9,column=4)
class_box6=ttk.Combobox(root, values=List_cell_Lot,textvariable=class6,state="normal",width=28).grid(row=10,column=4)
class_box7=ttk.Combobox(root, values=List_cell_Lot,textvariable=class7,state="normal",width=28).grid(row=11,column=4)
class_box8=ttk.Combobox(root, values=List_cell_Lot,textvariable=class8,state="normal",width=28).grid(row=12,column=4)
class_box9=ttk.Combobox(root, values=List_cell_Lot,textvariable=class9,state="normal",width=28).grid(row=13,column=4)
class_box10=ttk.Combobox(root, values=List_cell_Lot,textvariable=class10,state="normal",width=28).grid(row=14,column=4)
class_box11=ttk.Combobox(root, values=List_cell_Lot,textvariable=class11,state="normal",width=28).grid(row=5,column=9)
class_box12=ttk.Combobox(root, values=List_cell_Lot,textvariable=class12,state="normal",width=28).grid(row=6,column=9)
class_box13=ttk.Combobox(root, values=List_cell_Lot,textvariable=class13,state="normal",width=28).grid(row=7,column=9)
class_box14=ttk.Combobox(root, values=List_cell_Lot,textvariable=class14,state="normal",width=28).grid(row=8,column=9)
class_box15=ttk.Combobox(root, values=List_cell_Lot,textvariable=class15,state="normal",width=28).grid(row=9,column=9)
class_box16=ttk.Combobox(root, values=List_cell_Lot,textvariable=class16,state="normal",width=28).grid(row=10,column=9)
class_box17=ttk.Combobox(root, values=List_cell_Lot,textvariable=class17,state="normal",width=28).grid(row=11,column=9)
class_box18=ttk.Combobox(root, values=List_cell_Lot,textvariable=class18,state="normal",width=28).grid(row=12,column=9)
class_box19=ttk.Combobox(root, values=List_cell_Lot,textvariable=class19,state="normal",width=28).grid(row=13,column=9)
class_box20=ttk.Combobox(root, values=List_cell_Lot,textvariable=class10,state="normal",width=28).grid(row=14,column=9)
Label(root, text="グラフ表示:").grid(row=15,column=0)
Button(root, text='Graph', command=Graph).grid(row=15, column=1, sticky=W, pady=4)
Label(root, text="save/call:").grid(row=16,column=0)

SaveBox=ttk.Combobox(root, values=File_dir,textvariable=SaveFile,state="normal",width=10).grid(row=16,column=1)

Button(root, text='Save', command=save).grid(row=16, column=2, sticky=W, pady=4)
Button(root, text='Call', command=call).grid(row=16, column=3, sticky=W, pady=4)

Label(root, text="Quit:").grid(row=17,column=0)
Button(root, text='終了', command=root.quit,height=1,width=13).grid(row=17, column=1, sticky=W, pady=4)
root.mainloop()