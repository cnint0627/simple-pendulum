from socket import gaierror
import tkinter as tk
from tkinter.ttk import Combobox,Frame
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import matplotlib.font_manager as fm
from PIL import Image, ImageTk

import numpy as np
import time
import math
import threading
import sys




#------------------------------变量初始化-------------------------------#
root=tk.Tk()
root.title('Simple Pendulum')
root.geometry("1080x600")
root.resizable(False,False)
root.option_add("*Font", "黑体 10")


angle_s=-5*(math.pi/180)#初始摆角(rad)
w=0#实时角速度
g=9.80#重力加速度(kg·m/s^2)
l=1.0#绳子长度(m)
m=3.0#小球质量(kg)
r=4#小球半径(px)
t_delta=0.001#时间变化量
f=0#运算频率，数值为时间变化量的倒数
start_time=0#程序开始运行计时
isStart=False#演示是否开始
isDisplayForce=tk.BooleanVar()#受力分析是否开启
isDisplayForce.set(True)

sumF=0
sumTime=0

isMax=False#已经有最大位移
isMin=False#已经有最小位移

listG=[i/100 for i in range(675,1300,25)]

isSim=False
Simed=False


#------------------------------界面控制-------------------------------#
#布局框架
frame_left=Frame(root,width=275,height=500)
frame_center=Frame(root,width=300,height=580)
frame_right=Frame(root,width=485,height=580)

frame_left.place(x=5,y=30)
frame_center.place(x=280,y=10)
frame_right.place(x=590,y=10)


#标题文字
title=tk.Label(frame_left,text='Experiment of Simple Pendulum',width=30)
title.grid(row=0,column=0,columnspan=6,pady=8)

#绳子长度控件
scale_l=tk.Scale(frame_left,variable=l,length=180,tickinterval=1.0,from_=0.5,to=3.5,resolution=0.1,digits=2,showvalue=0,orient='horizontal')
scale_l.set(1.5)
scale_l.grid(row=2,column=0,columnspan=6,pady=8)
label_l=tk.Label(frame_left,text='Length of Pendulum:')
label_l.grid(row=1,column=0,columnspan=3,pady=8)
labelvar_l=tk.Label(frame_left,textvariable=l,width=5)
labelvar_l.grid(row=1,column=3,columnspan=3,pady=8)

#摆角控件
scale_angle=tk.Scale(frame_left,variable=angle_s,length=180,tickinterval=5,from_=0,to=10,showvalue=0,orient='horizontal')
scale_angle.set(5)
scale_angle.grid(row=4,column=0,columnspan=6,pady=8)
label_angle=tk.Label(frame_left,text='Initial Angle:')
label_angle.grid(row=3,column=0,columnspan=3,pady=8)
labelvar_angle=tk.Label(frame_left,textvariable=angle_s,width=5)
labelvar_angle.grid(row=3,column=3,columnspan=3,pady=8)

#重力加速度控件
scale_g=tk.Scale(frame_left,variable=g,length=180,tickinterval=3.0,from_=6.75,to=12.75,digits=4,resolution=0.25,showvalue=0,orient='horizontal')
scale_g.set(9.80)
scale_g.grid(row=6,column=0,columnspan=6,pady=8)
label_g=tk.Label(frame_left,text='Acceleration of Gravity:')
label_g.grid(row=5,column=0,columnspan=3,pady=8)
labelvar_g=tk.Label(frame_left,textvariable=g,width=5)
labelvar_g.grid(row=5,column=3,columnspan=3,pady=8)

#摆球质量控件
scale_m=tk.Scale(frame_left,variable=m,length=180,tickinterval=1.0,from_=1.0,to=5.0,digits=2,resolution=1.0,showvalue=0,orient='horizontal')
scale_m.set(1.0)
scale_m.grid(row=8,column=0,columnspan=6,pady=8)
label_m=tk.Label(frame_left,text='Mass of Pendulum Ball:')
label_m.grid(row=7,column=0,columnspan=3,pady=8)
labelvar_m=tk.Label(frame_left,textvariable=m,width=5)
labelvar_m.grid(row=7,column=3,columnspan=3,pady=8)

#受力分析开启按钮
checkbtn_f=tk.Checkbutton(frame_left,text='Force Analysis',variable=isDisplayForce,onvalue=True,offvalue=False)
checkbtn_f.grid(row=9,column=0,columnspan=6,pady=8)

#演示开始按钮
def Start():
    global isStart
    if isStart==False:
        isStart=True
        btn_sim.config(state='disabled')
        if combobox_lang.get()=='中文':
            btn_start.config(text='停止演示')
        else:
            btn_start.config(text='Stop Demonstration')
    else:
        isStart=False
        if combobox_lang.get()=='中文':
            btn_start.config(text='开始演示')
        else:
            btn_start.config(text='Start Demonstration')
btn_start=tk.Button(frame_left,width=20,text='Start Demonstration',command=Start,relief='groove',bd=4)
btn_start.grid(row=10,column=0,columnspan=6,pady=8,ipady=8)

#快速模拟生成数据控件
def Sim():
    global isSim,isStart,g,Simed
    g=12.25
    btn_sim.config(state='disabled')
    btn_start.config(state='disabled')
    isSim=True
    isStart=True
    Simed=True
     
        
btn_sim=tk.Button(frame_right,width=20,text='Quick Simulation',command=Sim,relief='groove',bd=4)
btn_sim.grid(row=2,column=2,columnspan=2,pady=10,ipady=8)


#拟合曲线控件
def Fit():
    if len(ax_L)<3:
        if combobox_lang.get()=='English':
            tk.messagebox.showinfo("Alert", "Please mark at least three sets of data!")
        else:
            tk.messagebox.showinfo("提醒", "请标记至少三组数据！")
        return
    fit_L=ax_L
    fit_L.append(0)
    fit_T=ax_T
    fit_T.append(0)
    axLT.plot(fit_L,fit_T,color='orange')
    cvsLT.draw()
    
btn_fit=tk.Button(frame_right,text='Scatter Fitting',command=Fit,width=20,relief='groove',bd=4)
btn_fit.grid(row=2,column=0,columnspan=2,pady=10,ipady=8)


#删除标点控件
def DeleteMark():
    global ax_L,ax_T,ax_G,ax_T2
    ax_L=[]
    ax_T=[]
    ax_G=[]
    ax_T2=[]
    markerLT.set_data([],[])
    markerGT.set_data([],[])
    cvsLT.draw()
    cvsGT.draw()
image=Image.open("btn_delete.png")
image=image.resize((30,22))

photo=ImageTk.PhotoImage(image)

btn_delete=tk.Button(frame_right,command=DeleteMark,image=photo,text='Delete Data Marks',compound = tk.LEFT,width=183,relief='groove',bd=4)
btn_delete.grid(row=3,column=2,columnspan=2,pady=10,ipady=8)

#选择语言控件
def ChangeLanguage(event):

    if combobox_lang.get()=='中文':
        root.title('单摆')
        title.config(text='单摆实验')
        label_l.config(text='摆长：')
        label_angle.config(text='初始摆角：')
        label_g.config(text='重力加速度：')
        label_m.config(text='摆球质量：')
        checkbtn_f.config(text='受力分析')
        if isStart:
            btn_start.config(text='停止演示')
        else:
            btn_start.config(text='开始演示')
        label_lang.config(text='语言')
        btn_sim.config(text='快速模拟')
        btn_fit.config(text='散点拟合')
        label_init.config(text='初始化中......')
        btn_delete.config(text='删除数据标记')



    else:
        root.title('Simple Pendulum')
        title.config(text='Experiment of Simple Pendulum')
        label_l.config(text='Length of Pendulum:')
        label_angle.config(text='Initial Angle:')
        label_g.config(text='Acceleration of Gravity:')
        label_m.config(text='Mass of Pendulum Ball:')
        checkbtn_f.config(text='Force Analysis')
        if isStart:
            btn_start.config(text='Stop Demonstration')
        else:
            btn_start.config(text='Start Demonstration')
        label_lang.config(text='Language')
        btn_sim.config(text='Quick Simulation')
        btn_fit.config(text='Scatter Fitting')
        label_init.config(text='Initializing......')
        btn_delete.config(text='Delete Data Marks')


label_lang=tk.Label(frame_right,text='Language')
label_lang.grid(row=3,column=0)
combobox_lang=Combobox(frame_right,width=10,values=['中文','English'],state='readonly')
combobox_lang.set('English')
combobox_lang.bind('<<ComboboxSelected>>',ChangeLanguage)
combobox_lang.grid(row=3,column=1)


#画板控件
canvas=tk.Canvas(frame_center,background='white',width=300,height=580)
canvas.place(x=0,y=0)
top=tk.Canvas(frame_center,background='white',width=296,height=30,highlightthickness=0)
top.place(x=2,y=20)


#位移-时间图像

figXT=plt.figure(figsize=(4.2,2),dpi=90)
axXT=figXT.add_subplot(111)
ax_t=[]
ax_x=[]
axXT.set_xlim(0,10)
axXT.set_ylim(-10,10)
plt.title('Displacement-Time Graph')
plt.xlabel('Time',labelpad=-10)
plt.ylabel('Displacement',labelpad=-5)

markerXT=axXT.plot(())[0]
cvsXT=FigureCanvasTkAgg(figXT,master=frame_right)
cvsXT.get_tk_widget().grid(row=0,column=0,columnspan=4)

#摆长-周期的平方图像
figLT=plt.figure(figsize=(2.0,1.9),dpi=90)
axLT=figLT.add_subplot(111)
ax_T=[]
ax_L=[]
axLT.set_xlim(0,4)
axLT.set_ylim(0,15)
plt.title('Length-Square of Period Graph',fontsize=9)
plt.xlabel('Length',labelpad=-27,alpha=0.2)
plt.ylabel('Square of Period',labelpad=-32,alpha=0.2)
for i in range(1,6):
    plt.hlines(y=i*2.5, xmin=0, xmax=4, linestyles='--',color='black',alpha=0.1)
for i in range(1,8):
    plt.vlines(x=i*0.5,ymin=0,ymax=15,linestyle='--',color='black',alpha=0.1)


markerLT=axLT.plot((),'o',ms=3)[0]
cvsLT=FigureCanvasTkAgg(figLT,master=frame_right)
cvsLT.get_tk_widget().grid(row=1,column=0,columnspan=2,pady=5,ipadx=2,padx=2)

#重力加速度-周期的平方图像
figGT=plt.figure(figsize=(2.0,1.9),dpi=90)
axGT=figGT.add_subplot(111)
ax_T2=[]
ax_G=[]
axGT.set_xlim(6.75,12.75)
plt.xticks([6.75,8.25,9.75,11.25,12.75])
axGT.set_ylim(0,10)
plt.title('g-Square of Period Graph',fontsize=9)
plt.xlabel('g',labelpad=-27,alpha=0.2)
plt.ylabel('Square of Period',labelpad=-35,alpha=0.2)
for i in range(1,10):
    plt.hlines(y=i, xmin=6.75, xmax=12.75, linestyles='--',color='black',alpha=0.1)
for i in range(1,12):
    plt.vlines(x=6.75+i*0.5,ymin=0,ymax=10,linestyle='--',color='black',alpha=0.1)


markerGT=axGT.plot((),'o',ms=3)[0]
cvsGT=FigureCanvasTkAgg(figGT,master=frame_right)
cvsGT.get_tk_widget().grid(row=1,column=2,columnspan=2,pady=5,ipadx=2,padx=2)

#读取已有数据
try:
    with open('LTCoordinates.dat','r') as fileLT:
        for i in fileLT.readlines():
            i=i.rstrip()
            idx=i.find(',')
            ax_L.append(float(i[:idx]))
            ax_T.append(float(i[idx+1:]))
except:
    pass


try:
    with open('gTCoordinates.dat','r') as fileGT:
        for i in fileGT.readlines():
            i=i.rstrip()
            idx=i.find(',')
            ax_G.append(float(i[:idx]))
            ax_T2.append(float(i[idx+1:]))
except:
    pass

markerLT.set_data(ax_L,ax_T)
markerGT.set_data(ax_G,ax_T2)

#退出时自动保存数据
def AutoSave():
    print(ax_L,ax_T)
    print(ax_G,ax_T2)
    with open('LTCoordinates.dat','w+') as fileLT:
        for i in range(len(ax_L)):
            fileLT.write('%.2f,%.2f\n'%(ax_L[i],ax_T[i]))
    with open('gTCoordinates.dat','w+') as fileGT:
        for i in range(len(ax_G)):
            fileGT.write('%.2f,%.2f\n'%(ax_G[i],ax_T2[i]))
    
    root.destroy()
	    
root.protocol('WM_DELETE_WINDOW', AutoSave)

#------------------------------主要函数-------------------------------#
#生成圆的优化函数
def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle = _create_circle



#绘制初始状态单摆模型
def Draw():
    
    canvas.create_line(150,50,150+l*125*math.sin(angle_s),50+l*125*math.cos(angle_s),fill='black',width=2)
    canvas.create_circle(150+l*125*math.sin(angle_s),50+l*125*math.cos(angle_s),r,fill='green',outline='green')
    if isDisplayForce.get():
        G=(g*15-60+(m-1)*5)
        #重力G
        canvas.create_line(150+l*125*math.sin(angle_s),50+l*125*math.cos(angle_s),\
        150+l*125*math.sin(angle_s),50+l*125*math.cos(angle_s)+G,arrow='last',fill='red')
        #拉力T
        canvas.create_line(150+l*125*math.sin(angle_s),50+l*125*math.cos(angle_s),\
        150+l*125*math.sin(angle_s)-(G+10)*math.sin(angle_s),50+l*125*math.cos(angle_s)-(G+10)*math.cos(angle_s),arrow='last',fill='red')
        #重力沿绳子方向分力
        canvas.create_line(150+l*125*math.sin(angle_s),50+l*125*math.cos(angle_s),\
        150+l*125*math.sin(angle_s)+G*math.cos(angle_s)*math.sin(angle_s),50+l*125*math.cos(angle_s)+G*math.cos(angle_s)*math.cos(angle_s),arrow='last',fill='blue',dash=(1,1))
        #重力沿垂直于绳子方向分力
        canvas.create_line(150+l*125*math.sin(angle_s),50+l*125*math.cos(angle_s),\
        150+l*125*math.sin(angle_s)-G*math.sin(angle_s)*math.cos(angle_s),50+l*125*math.cos(angle_s)+G*math.sin(angle_s)*math.sin(angle_s),arrow='last',fill='blue',dash=(1,1))
    

#绘制单摆运动动画
def Move():
    global angle,w,a,f,t_delta,start_time,sumF,sumTime,isMax,isMin,text_max,text_min,text_T,isStart,flag
    
    #if f==0:
    #    start_time=time.time()
    #f+=1
    a=m*g*math.sin(angle)/m#计算切向线加速度
    w-=(a*t_delta)/l#计算角速度
    angle+=w*t_delta#计算摆角
    #实时绘制绳子
    canvas.create_line(150,50,150+l*125*math.sin(angle),50+l*125*math.cos(angle),fill='black',width=2)
    canvas.create_circle(150+l*125*math.sin(angle),50+l*125*math.cos(angle),r,fill='green',outline='green')
    if isDisplayForce.get():
        G=(g*15-60+(m-1)*5)
        #重力G
        canvas.create_line(150+l*125*math.sin(angle),50+l*125*math.cos(angle),\
        150+l*125*math.sin(angle),50+l*125*math.cos(angle_s)+G,arrow='last',fill='red')
        #拉力T
        canvas.create_line(150+l*125*math.sin(angle),50+l*125*math.cos(angle),\
        150+l*125*math.sin(angle)-(G+10)*math.sin(angle),50+l*125*math.cos(angle_s)-(G+10)*math.cos(angle_s),arrow='last',fill='red')
        #重力沿绳子方向分力
        canvas.create_line(150+l*125*math.sin(angle),50+l*125*math.cos(angle),\
        150+l*125*math.sin(angle)+G*math.cos(angle)*math.sin(angle),50+l*125*math.cos(angle)+G*math.cos(angle)*math.cos(angle_s),arrow='last',fill='blue',dash=(1,1))
        #重力沿垂直于绳子方向分力
        canvas.create_line(150+l*125*math.sin(angle),50+l*125*math.cos(angle),\
        150+l*125*math.sin(angle)-G*math.sin(angle)*math.cos(angle),50+l*125*math.cos(angle)+G*math.sin(angle)*math.sin(angle),arrow='last',fill='blue',dash=(1,1))
    #end_time=time.time()
    sumF+=1
    sumTime+=t_delta
    if flag>0:
        flag+=1
        if flag>f//2:
            isStart=False
    if sumF%10==0:
        ax_t.append(sumTime)
        ax_x.append(math.sqrt((50+l*125-(50+l*125*math.cos(angle)))**2+(l*125*math.sin(angle))**2)*(angle/abs(angle))/10)
        if isMax==False and sumF//10>2: 
            if ax_x[-1]<ax_x[-2] and ax_x[-3]<ax_x[-2]:
                text_max=axXT.text(x=ax_t[-2],y=ax_x[-2]+1,s='Max= '+str(round(ax_x[-2],2)),ha='center')
                isMax=True
        if isMax and isMin==False:
            if ax_x[-1]>ax_x[-2] and ax_x[-3]>ax_x[-2]:
                text_min=axXT.text(x=ax_t[-2],y=ax_x[-2]-2,s='Min= '+str(round(ax_x[-2],2)),ha='center')
                text_T=axXT.text(x=ax_t[-2],y=ax_x[-2]-4,s='T= '+str(round(ax_t[-2],2)),ha='center',color='orange')
                if l not in ax_L and g==9.75:
                    ax_L.append(l)
                    ax_T.append(round(ax_t[-2]**2,2))
                    markerLT.set_data(ax_L,ax_T)
                    cvsLT.draw()
                if g not in ax_G and l==1.5:
                    ax_G.append(g)
                    ax_T2.append(round(ax_t[-2]**2,2))
                    markerGT.set_data(ax_G,ax_T2)
                    cvsGT.draw()
                isMin=True
                
                if isSim:
                    flag=1

               

            
    #if end_time-start_time>=1:
    #    t_delta=1/f
    #    print(f)
    #    f=0

        
    

#获取程序运行频率，以确定绘图时使用的刷新率，使图像呈现更准确        
def GetFrequency(isforce):
    f=0
    w=0
    m=1
    angle=-5*(math.pi/180)
    start_time=time.time()
    while True:
        f+=1       
        a=m*g*math.sin(angle)/m#计算切向线加速度
        w-=(a*t_delta)/l#计算角速度
        angle+=w*t_delta#计算摆角
        #实时绘制绳子
        canvas.delete('all')#删除上一个图形
        canvas.create_line(150,50,150+l*125*math.sin(angle),50+l*125*math.cos(angle),fill='white')
        canvas.create_circle(150+l*125*math.sin(angle),50+l*125*math.cos(angle),r,outline='white')  
        #受力分析
        
        if isforce:
            
            G=(g*15-60+(m-1)*5)
            #重力G
            canvas.create_line(150+l*125*math.sin(angle),50+l*125*math.cos(angle),\
            150+l*125*math.sin(angle),50+l*125*math.cos(angle_s)+G,arrow='last',fill='white')
            #拉力T
            canvas.create_line(150+l*125*math.sin(angle),50+l*125*math.cos(angle),\
            150+l*125*math.sin(angle)-(G+10)*math.sin(angle),50+l*125*math.cos(angle_s)-(G+10)*math.cos(angle_s),arrow='last',fill='white')
            #重力沿绳子方向分力
            canvas.create_line(150+l*125*math.sin(angle),50+l*125*math.cos(angle),\
            150+l*125*math.sin(angle)+G*math.cos(angle)*math.sin(angle),50+l*125*math.cos(angle)+G*math.cos(angle)*math.cos(angle_s),arrow='last',fill='white',dash=(1,1))
            #重力沿垂直于绳子方向分力
            canvas.create_line(150+l*125*math.sin(angle),50+l*125*math.cos(angle),\
            150+l*125*math.sin(angle)-G*math.sin(angle)*math.cos(angle),50+l*125*math.cos(angle)+G*math.sin(angle)*math.sin(angle),arrow='last',fill='white',dash=(1,1))
        canvas.update()
        if f%10==0:
            cvsXT.draw() 
        end_time=time.time()
        if end_time-start_time>=1:
            return f

#禁用所有控件
def disable():
    scale_l.config(state='disabled')
    scale_angle.config(state='disabled')
    scale_g.config(state='disabled')
    scale_m.config(state='disabled')
    checkbtn_f.config(state='disabled')
    btn_delete.config(state='disabled')
    


    

#启用所有控件
def enable():
    scale_l.config(state='normal')
    scale_angle.config(state='normal')
    scale_g.config(state='normal')
    scale_m.config(state='normal')
    checkbtn_f.config(state='normal')
    if Simed==False:
        btn_sim.config(state='normal')
    btn_delete.config(state='normal')
 

#------------------------------主程序-------------------------------#
#初始化获取程序运行频率
disable()
btn_sim.config(state='disabled')
btn_start.config(state='disabled')
btn_fit.config(state='disabled')
print('Initializing......0')
label_init=tk.Label(canvas,text='Initializing......',bg='white')
label_init.place(x=150,y=100,anchor='center')
f_noforce=0
f_force=0
for i in range(4):
    if i>0:
        f_noforce+=GetFrequency(False)
    else:
        GetFrequency(False)
    sys.stdout.write("\033[2J\033[1;1H")
    sys.stdout.flush()
    print('Initializing......'+str(i+1))
f_noforce=f_noforce//3
for i in range(4):
    if i>0:
        f_force+=GetFrequency(True)        
    else:
        GetFrequency(True)

    sys.stdout.write("\033[2J\033[1;1H")
    sys.stdout.flush()
    print('Initializing......'+str(i+5))
f_force=f_force//3

label_init.place_forget()
btn_start.config(state='normal')
btn_fit.config(state='normal')
sys.stdout.write("\033[2J\033[1;1H")
sys.stdout.flush()
print('Initialization completed!')
print('Frequency:',f_noforce,'(Without Force Analysis);',f_force,'(With Force Analysis)')

top.create_line(0,28,300,28,fill='brown',width=4)
for i in range(10):
    top.create_line(i*30+10,28,i*30+20,10,fill='brown')




#主循环开始
while True:
    enable()
    st=False
    if isSim:
            
        isStart=True
        g+=0.25
        if g>12.75:
            isSim=False
            Simed=True
            isStart=False
            btn_start.config(state='normal')
  
       
            text_max.set_text('')
            text_min.set_text('')
            text_T.set_text('')
            markerXT.set_data([],[])
            cvsXT.draw()
            
    
            
    while isStart==False:
        canvas.delete('all')#删除上一个图形

        l=scale_l.get()
        angle_s=-scale_angle.get()*(math.pi/180)
        #g=scale_g.get()
        m=scale_m.get()
        r=4+0.6*scale_m.get()
        g=scale_g.get()
        Draw()

        canvas.update()
        

    disable()
    if isDisplayForce.get():
        f=f_force
    else:
        f=f_noforce
    t_delta=1/f
    w=0
    angle=angle_s#实时摆角(rad)
    ax_t=[]
    ax_x=[]
    sumF=0
    sumTime=0
    if isMax:
        text_max.remove()
        isMax=False
    if isMin:
        text_min.remove()
        text_T.remove()
        isMin=False

    flag=0
    while isStart:
        st=True
      
        canvas.delete('all')#删除上一个图形
        
        Move()        
        if sumF%10==0:
            markerXT.set_data(ax_t[:sumF//10],ax_x[:sumF//10])
            cvsXT.draw()                     
        canvas.update()
    


    






