import tkinter as tk
import sqlite3

data = []

def add():
    sql = f"INSERT INTO elements (name, fault, intensity) VALUES ('{entry_1.get()}', {entry_2.get()}, {entry_3.get()})"
    conn = sqlite3.connect('database.db')
    data = conn.execute(sql)
    conn.commit()
    conn.close()
    window.quit()

window = tk.Tk()
window.title("Новый элемент")

frm_form = tk.Frame(relief=tk.SUNKEN, borderwidth=3)
frm_form.pack()


# Наименование
label_1 = tk.Label(master=frm_form, text="Наименование:")
entry_1 = tk.Entry(master=frm_form, width=50)
label_1.grid(row=0, column=0, sticky="e")
entry_1.grid(row=0, column=1)

# Наработка на отказ
label_2 = tk.Label(master=frm_form, text="Наработка на отказ:")
entry_2 = tk.Entry(master=frm_form, width=50)
label_2.grid(row=1, column=0, sticky="e")
entry_2.grid(row=1, column=1)

#Номинальная интенсивность отказов
label_3 = tk.Label(master=frm_form, text="Номинальная интенсивность отказов:")
entry_3 = tk.Entry(master=frm_form, width=50)
label_3.grid(row=2, column=0, sticky="e")
entry_3.grid(row=2, column=1)

frm_enter = tk.Frame()
frm_enter.pack(side=tk.RIGHT)

ent_btn = tk.Button(master=frm_enter, text='Добавить', command=add)
ent_btn.pack(side=tk.RIGHT)

window.mainloop()