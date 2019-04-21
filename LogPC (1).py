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


#Funciones
def animate():
    update_graph()

def toggle_memoria_absoluta():
    global sunk_memoria_absoluta
    global log_memoria_absoluta
    global segundo
    sunk_memoria_absoluta = not sunk_memoria_absoluta;
    if sunk_memoria_absoluta:
        logMemoriaAbsoluta.configure(relief='sunken',text="Registrando datos",bg="red")
        log_memoria_absoluta = open("memoria_absoluta.log",'w')
        segundo=datetime.datetime.now().second
    else:
        log_memoria_absoluta.close()
        log_memoria_absoluta = None
        logMemoriaAbsoluta.configure(relief='raised',text="Registrar datos",bg='green')
        file = asksaveasfilename(filetypes=[("Todos los archivos", "*.*"),("Archivos de texto", "*.txt"),
                                            ("Archivo compatible con Excel","*.csv")])
        if file != "":
            with open("memoria_absoluta.log") as log_memoria_absoluta:
                with open(file,'w') as f:
                    for line in log_memoria_absoluta:
                        f.write(line)
            os.remove("memoria_absoluta.log")
            log_memoria_absoluta=None

def toggle_bytes_rec():
    global sunk_bytes_rec
    global log_bytes_rec
    global segundo
    global bytes_rec
    sunk_bytes_rec = not sunk_bytes_rec;
    if sunk_bytes_rec:
        logBytesRec.configure(relief='sunken',text="Registrando datos",bg="red")
        log_bytes_rec = open("bytes_rec.log",'w')
        segundo=datetime.datetime.now().second
    else:
        log_bytes_rec.close()
        log_bytes_rec = None
        logBytesRec.configure(relief='raised',text="Registrar datos",bg='green')
        file = asksaveasfilename(filetypes=[("Todos los archivos", "*.*"),("Archivos de texto", "*.txt"),
                                            ("Archivo compatible con Excel","*.csv")])
        if file != "":
            with open("bytes_rec.log") as log_bytes_rec:
                with open(file,'w') as f:
                    for line in log_bytes_rec:
                        f.write(line)
            os.remove("bytes_rec.log")
            log_bytes_rec=None       
def toggle_cpu():
    global sunk_cpu
    global log_cpu
    global segundo
    global data_cpu
    sunk_cpu = not sunk_cpu;
    if sunk_cpu:
        logCPU.configure(relief='sunken',text="Registrando datos",bg="red")
        log_cpu = open("cpu.log",'w')
        segundo=datetime.datetime.now().second
    else:
        log_cpu.close()
        log_cpu = None
        logCPU.configure(relief='raised',text="Registrar datos",bg='green')
        file = asksaveasfilename(filetypes=[("Todos los archivos", "*.*"),("Archivos de texto", "*.txt"),
                                            ("Archivo compatible con Excel","*.csv")])
        if file != "":
            with open("cpu.log") as log_bytes_rec:
                with open(file,'w') as f:
                    for line in log_bytes_rec:
                        f.write(line)
            os.remove("cpu.log")
            log_cpu=None             
    
def update_graph():
    global segundo
    global bytes_rec, data_cpu
    global mem_absoluta,log_memoria_absoluta,log_bytes_rec,log_cpu
    segundo_ant = segundo
    bytes_rec_ant = bytes_rec
    bytes_rec = psutil.net_io_counters()[1]/1000
    tiempo = datetime.datetime.now() 
    dia,mes,año = tiempo.day, tiempo.month,tiempo.year
    hora, minuto,segundo = tiempo.hour,tiempo.minute,tiempo.second
    
    #Superior info
    percent.set(psutil.cpu_percent())
    lblpercent.config(text = "Uso del CPU: {:.1f}%  ".format(percent.get()))
    
    memory_free.set(psutil.disk_usage("C:")[2])
    lblfree.config(text="Disco Disponible: {:.2f} GB / {:.2f} GB  ".format(memory_free.get()/1e9,psutil.disk_usage("C:")[0]/1e9))
    
    memory_tot.set(psutil.virtual_memory().total/1e9)
    lblmemory.config(text="Memoria Total: {:.2f} GB  ".format(memory_tot.get()))
   
    memory_uso.set(psutil.virtual_memory().percent)
    lblusomemory.config(text = "Memoria en Uso: {:.2f}%  ".format(memory_uso.get()))
    
    velocpu.set(psutil.cpu_freq().current)
    lblvelocpu.config(text="Velocidad del CPU: {:.2f} Ghz  ".format(velocpu.get()/1e3))
    
    #memoria absoluta
    mem_absoluta_max=psutil.virtual_memory()[0]/1e9
    mem_absoluta_actual=psutil.virtual_memory()[3]/1e9
    if log_memoria_absoluta != None and segundo-segundo_ant==1:
        log_memoria_absoluta.write("{:4}/{:02d}/{:02d}, {:02d}:{:02d}:{:02d},{:.2f}GB\n".format(año,mes,dia,
                                                                                      hora,minuto,segundo,
                                                                                      mem_absoluta_actual))
    mem_absoluta.pop(0)
    mem_absoluta.append(mem_absoluta_actual)
    ax1.cla()
    ax1.grid()
    ax1.plot(mem_absoluta)
    ax1.set_xlim(0,100)
    ax1.set_ylim(0,mem_absoluta_max)
    ax1.set_title("Cantidad de RAM utilizada (GB)")
    
    #Porcentaja del CPU
    data = psutil.cpu_percent()
    if log_cpu != None and segundo-segundo_ant==1:
        log_cpu.write("{:4}/{:02d}/{:02d}, {:02d}:{:02d}:{:02d},{:.1f}%\n".format(año,mes,dia,
                                                                                                hora,minuto,segundo,data))
    data_cpu.pop(0)
    data_cpu.append(data)                                                                                  
    ax2.cla()
    ax2.grid()
    ax2.set_ylim(0, 100)
    ax2.set_xlim(0,100)
    ax2.set_title("Porcentaje de CPU utilizado (%)")
    ax2.set_yticklabels([0, 20, 40, 60, 80, 100])  
    ax2.plot(data_cpu)                                                                                  
    
    
    
    #bytes recibidos
    bytes_recibidos = bytes_rec-bytes_rec_ant
    if log_bytes_rec != None and segundo-segundo_ant==1:
        log_bytes_rec.write("{:4}/{:02d}/{:02d}, {:02d}:{:02d}:{:02d},{:.2f} KB\n".format(año,mes,dia,
                                                                                      hora,minuto,segundo,
                                                                                      bytes_recibidos))
    bytes_list.pop(0)
    bytes_list.append(bytes_recibidos)
    ax3.cla()
    ax3.grid()
    ax3.plot(bytes_list)
    ax3.set_xlim(0,100)
    ax3.set_ylim(0,100)
    ax3.set_title("Cantidad de bytes recibidos(KB)")
    
    #actualizar graficos
    graph1.draw()
    graph2.draw()
    graph3.draw()
    root.after(100,animate)

def salir():
    want_to_quit = askokcancel("Salir", "¿Desea salir de la aplicacion?")
    if want_to_quit:
        root.destroy()

def acercade():
    showinfo("Acerca de...",
            "Monitor PC\n\n\nAutores:Astolfo Romero & Jose Chavez Loli")


#Menu
root = Tk()
root.resizable(0,0)
root.configure(background="white")
root.title("Monitor PC")
root.geometry("900x500+100+100")
main_menu = Menu(root)
root.configure(menu=main_menu)

menu_archivo = Menu(main_menu,tearoff=False)
menu_archivo.add_command(label="Salir",command=salir)

menu_ayuda = Menu(main_menu,tearoff=False)
menu_ayuda.add_command(label="Acerca de...",command=acercade)

main_menu.add_cascade(label="Archivo",menu=menu_archivo)
main_menu.add_cascade(label="Ayuda",menu=menu_ayuda)

#Frames
frame_superior = Frame(root,bg='white', borderwidth = 10, relief = "groove")
frame_superior.pack(side=TOP)

frame_inferior = Frame(root,bg='white', borderwidth = 2, relief = "groove")
frame_inferior.pack(side=BOTTOM)

frame_medio = Frame(root,bg='white',pady=40)
frame_medio.pack(side=BOTTOM)



frm1 = Frame(frame_medio,background="white")
frm11 = Frame(frm1, borderwidth = 10, relief = "groove")
frm12 = Frame(frm1,background="white")

frm2= Frame(frame_medio,background="white")
frm21 = Frame(frm2, borderwidth = 10, relief = "groove")
frm22 = Frame(frm2,background="white")

frm3 = Frame(frame_medio,background="white")
frm31 = Frame(frm3, borderwidth = 10, relief = "groove")
frm32 = Frame(frm3,background="white")

frm1.pack(side=LEFT)
frm11.pack(side=TOP)
frm12.pack(side=BOTTOM)

frm3.pack(side=RIGHT)
frm31.pack(side=TOP)
frm32.pack(side=BOTTOM)

frm2.pack(side=RIGHT)
frm21.pack(side=TOP)
frm22.pack(side=BOTTOM)


#Variables,listas y graficas
percent = DoubleVar(value = 0.0)
memory_uso = DoubleVar(value = 0.0)
memory_tot = DoubleVar(value= 0.0)
memory_free = DoubleVar(value=0.0)
velocpu = DoubleVar(value=0.0)

fig1 = Figure(figsize=(4,3))
fig2 = Figure(figsize=(4,3))
fig3 = Figure(figsize=(4,3))

ax1 = fig1.add_subplot(111)
ax2 = fig2.add_subplot(111)
ax3 = fig3.add_subplot(111)

mem_absoluta=[0]*100
bytes_list=[0]*100
data_cpu=[0]*100
graph1 = FigureCanvasTkAgg(fig1, master=frm11)
graph1.get_tk_widget().pack()

graph2 = FigureCanvasTkAgg(fig2, master=frm21)
graph2.get_tk_widget().pack()

graph3 = FigureCanvasTkAgg(fig3, master=frm31)
graph3.get_tk_widget().pack()

sunk_memoria_absoluta=False
sunk_bytes_rec=False
sunk_cpu= False
log_cpu=None
log_memoria_absoluta = None
log_bytes_rec=None
bytes_rec = psutil.net_io_counters()[1]/1000
segundo=0

#Widgets
logMemoriaAbsoluta= Button(frm12,command=toggle_memoria_absoluta,text="Registrar datos",
                  relief="raised", width=20,bg='green',fg="white",font="Calibri 9")
logMemoriaAbsoluta.pack(pady=15)

logCPU= Button(frm22,command=toggle_cpu,text="Registrar datos",
                  relief="raised", width=20,bg='green',fg="white",font="Calibri 9")
logCPU.pack(pady=15)

logBytesRec= Button(frm32,command=toggle_bytes_rec,text="Registrar datos",
                  relief="raised", width=20,bg='green',fg="white",font="Calibri 9")
logBytesRec.pack(pady=15)

lblpercent = Label(frame_superior, text = "Uso del CPU: {}%".format(percent.get()),
                   bg='white' ,fg='green', height= 4,font="Calibri 9")
lblpercent.grid(row=0,column=0, pady = 7, padx = 10, sticky = W)

lblfree= Label(frame_superior, text = "Disco disponible: {} GB ".format(memory_free.get()),
               bg='white', fg='green', height =4,font="Calibri 9") 
lblfree.grid(row =0, column = 1, pady = 7, padx = 10,sticky = W)

lblmemory = Label(frame_superior, text = "Memoria Total: {} GB".format(memory_tot.get()),
                  bg='white', fg='green', height =4,font="Calibri 9")
lblmemory.grid(row=0,column=2, pady = 7, padx = 10,sticky = W)

lblusomemory = Label(frame_superior, text = "Memoria en Uso: {}%".format(memory_uso.get()),
                     bg='white', fg='green', height =4,font="Calibri 9")
lblusomemory.grid(row=0, column=3, pady = 7, padx = 10,sticky = W)

lblvelocpu = Label(frame_superior, text = "Velocidad del CPU: {:1.2f} Ghz".format(velocpu.get()/1e3),
                   bg = 'white',fg='green', height =4,font="Calibri 9")
lblvelocpu.grid(row =0, column = 4, pady = 7, padx = 10, sticky = W)

status_bar = Label(frame_inferior, text="Listo", bd=1, relief=SUNKEN, anchor=W,width=150,bg='white')
status_bar.pack(side=BOTTOM, expand=True, fill=X)



root.after(100,animate)
root.mainloop()

