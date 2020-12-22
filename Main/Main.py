import tkinter as tk
import os

root = tk.Tk()
root.title('Главная программа')

frame_start = tk.Frame(root)

frame_start.pack()


def func(script_name):
    root.destroy()
    os.system(script_name)


button1 = tk.Button(master=frame_start, text='Оценка надежности безошибочного выполнения задач оператором', width=70, command=lambda: os.system('python Lab1.py'))
button2 = tk.Button(master=frame_start, text='Определение оптимального срока службы элементов системы', width=70, command=lambda: os.system('python Lab2.py'))
button3 = tk.Button(master=frame_start, text='Оценка надежности ПО', width=70, command=lambda: os.system('python Lab3.py'))

button1.pack()
button2.pack()
button3.pack()

root.mainloop()
