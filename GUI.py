import pywhatkit as kit
import tkinter as tk
from tkinter import ttk
from tkinter import *

import sys
import os
import PIL.Image
import PIL.ImageTk
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass


root = tk.Tk()
root.title("Omega")
root.geometry("1200x800")
root.resizable(False,False)



def listen():


    os.system("python recognize-from-microphone.py")

    global image
    global label
    with open('out.txt', 'r') as f:
        lines = f.readlines()
        configfile.insert(INSERT, lines[1])
        configfile.insert(INSERT, lines[2])
        configfile.insert(INSERT, lines[3])
        configfile.insert(INSERT, lines[4])

    configfile.pack(fill="none", expand=False)
    global img
    global panel
    global youtube_button

    def youtube():
        kit.playonyt(lines[5])
        listen_button.config(state='disabled')
    youtube_button = tk.Button(root, text="Watch on Youtube", command=youtube, width=16, height=1, bg='red',fg='white')
    youtube_button.pack(pady=2)

    img = PIL.ImageTk.PhotoImage(PIL.Image.open("example.jpg").resize((300, 300)), master=root)
    panel = tk.Label(root, image=img)
    panel.pack(side="top", fill="both", expand="yes")
    clear.config(state='normal')
    listen_button.config(state='disabled',text='Disabled')






variable1=tk.StringVar(value="Countdown set to 6 seconds")
display=ttk.Label(root,textvariable=variable1).pack(pady=8)

listen_button = tk.Button(root, text="Listen", command=listen,width=11,height=1,activebackground='green')
listen_button.pack(pady=8)

configfile = Text(root, wrap=WORD, width=45, height= 10)

def clear():
    configfile.delete(1.0, END)
    panel.destroy()
    youtube_button.destroy()
    listen_button.config(state='normal',text='Listen')
    clear.config(state='disabled')


clear = Button(root, text='Clear', command=clear,width=11,height=1,state='disabled')
clear.pack()

quit = tk.Button(root, text="Quit", command=root.destroy,width=11,height=1)
quit.pack()






root.mainloop()


