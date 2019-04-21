# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#%%
import psutil
from tkinter import *
from tkinter.messagebox import showinfo, askokcancel
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import datetime
from tkinter.messagebox import showinfo, askokcancel
from tkinter.filedialog import asksaveasfilename, asksaveasfile
import os


root = Tk()
root.resizable(0,0)
root.configure(background="white")
root.title("Monitor PC")
menu = Menu(root)
root.configure(menu=menu)
frm1 = Frame(root,background="white")
frm11 = Frame(frm1)
frm12 = Frame(frm1,background="white")

frm2= Frame(root)

frm3 = Frame(root)
frm31 = Frame(frm3)
frm32 = Frame(frm3)

frm1.pack(side=LEFT)
frm11.pack(side=TOP)
frm12.pack(side=BOTTOM)

frm3.pack(side=RIGHT)
frm31.pack(side=TOP)
frm32.pack(side=BOTTOM)

frm2.pack(side=RIGHT)

fig = Figure()

ax = fig.add_subplot(111)    # facecolor='black'
mem=[0]*100
graph = FigureCanvasTkAgg(fig, master=frm11)
graph.get_tk_widget().pack()
sunk=False
log = None
segundo=0
def animate():
    update_graph()

def toggle():
    global sunk
    global log
    global segundo
    sunk = not sunk;
    if sunk:
        logMemoria.configure(relief='sunken',text="Registrando datos",bg="red")
        log = open("memoria.tmp",'w')
        segundo=datetime.datetime.now().second
    else:
        log.close()
        logMemoria.configure(relief='raised',text="Registrar datos",bg='green')
        file = asksaveasfilename(filetypes=[("Todos los archivos", "*.*"),("Archivos de texto", "*.txt"),
                                            ("Archivo compatible con Excel","*.csv")])
        if file != "":
            with open("memoria.tmp") as log:
                with open(file,'w') as f:
                    for line in log:
                        f.write(line)
            os.remove("memoria.tmp")
            log=None
            
    
def update_graph():
    global segundo
    global mem,log
    segundo_ant = segundo
    tiempo = datetime.datetime.now() 
    dia,mes,año = tiempo.day, tiempo.month,tiempo.year
    hora, minuto,segundo = tiempo.hour,tiempo.minute,tiempo.second
    mem_max=psutil.virtual_memory()[0]/1e9
    mem_actual=psutil.virtual_memory()[3]/1e9
    if log != None and segundo-segundo_ant==1:
        log.write("{:4}/{:02d}/{:02d}, {:02d}:{:02d}:{:02d}, Memoria utilizada={:.2f}GB\n".format(año,mes,dia,
                                                                                      hora,minuto,segundo,
                                                                                      mem_actual))
    mem.pop(0)
    mem.append(mem_actual)
    ax.cla()
    ax.plot(mem)
    ax.set_xticklabels([60,50,40,30,20,0])
    ax.set_xlim(0,100)
    ax.set_ylim(0,mem_max)
    ax.set_title("Memoria RAM")
    graph.draw()
    root.after(100,animate)

logMemoria=Button(frm12,command=toggle,text="Registrar datos",
                  relief="raised", width=20,bg='green',fg="white")
logMemoria.pack(pady=15)
    

root.after(100,animate)
root.mainloop()

