import tkinter as tk
import os

root = tk.Tk()
root.title('Главная программа')

frame_start = tk.Frame(root)

frame_start.pack()


def func(script_name):
    root.destroy()
    os.system(script_name)


button1 = tk.Button(master=frame_start, text='Lab #1', width=39, command=lambda: os.system('python Lab1.py'))
button2 = tk.Button(master=frame_start, text='Lab #2', width=39, command=lambda: os.system('python Lab2.py'))
button3 = tk.Button(master=frame_start, text='Lab #3', width=39, command=lambda: os.system('python Lab3.py'))

button1.pack()
button2.pack()
button3.pack()

root.mainloop()
