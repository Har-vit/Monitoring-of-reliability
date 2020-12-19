from time import gmtime, strftime
import tkinter as tk
import os
import sqlite3
import math
import datetime

plan = {}

def solver():
    global plan
    plan = shema_data
    data = {}
    number = len(shema_data.keys())
    p = float(ent_reliability.get())
    p_i = p**(1/number)
    for link in shema_data:
        t = len(shema_data[link])
        if t == 1:
            p_i_j = p_i
            result = - float(math.log(p_i_j) * float(shema_data[link][1]['fault']))
            plan[link][1]['date'] += datetime.timedelta(days=int(result))
        elif t == 2:
            p_i_j = (2 - (4-4*p_i)**(1/2))/2
            result_1 = - float(math.log(p_i_j) * float(shema_data[link][1]['fault']))
            result_2 = - float(math.log(p_i_j) * float(shema_data[link][2]['fault']))
            plan[link][1]['date'] += datetime.timedelta(days=int(result_1))
            plan[link][2]['date'] += datetime.timedelta(days=int(result_2))
        elif t == 3:
            p_i_j_3 = (2 - (4-4*p_i)**(1/2))/2
            p_i_j = ((2 - (4-4*p_i)**(1/2))/2)**(1/2)
            result_1 = - float(math.log(p_i_j) * float(shema_data[link][1]['fault']))
            result_2 = - float(math.log(p_i_j) * float(shema_data[link][2]['fault']))
            result_3 = - float(math.log(p_i_j_3) * float(shema_data[link][3]['fault']))
            plan[link][1]['date'] += datetime.timedelta(days=int(result_1))
            plan[link][2]['date'] += datetime.timedelta(days=int(result_2))
            plan[link][3]['date'] += datetime.timedelta(days=int(result_3))
        elif t == 4:
            p_i_j = ((2 - (4-4*p_i)**(1/2))/2)**(1/2)
            result_1 = - float(math.log(p_i_j) * float(shema_data[link][1]['fault']))
            result_2 = - float(math.log(p_i_j) * float(shema_data[link][2]['fault']))
            result_3 = - float(math.log(p_i_j) * float(shema_data[link][3]['fault']))
            result_4 = - float(math.log(p_i_j) * float(shema_data[link][4]['fault']))
            plan[link][1]['date'] += datetime.timedelta(days=int(result_1))
            plan[link][2]['date'] += datetime.timedelta(days=int(result_2))
            plan[link][3]['date'] += datetime.timedelta(days=int(result_3))
            plan[link][4]['date'] += datetime.timedelta(days=int(result_4))
    for label in frm_4.grid_slaves():
        if int(label.grid_info()["row"]) >= 0:
            label.destroy()
    for link in plan:
        for element in plan[link]:
            if element == 1:
                lbl = tk.Label(master=frm_4, text=f"Звено №_{link} элемент №_{element} Название: {plan[link][element]['name']}: Дата замены: {plan[link][element]['date'].strftime('%d.%m.%y')}")
                lbl.grid(row=link, column=element, padx=5, pady=5, sticky='n')
            else:
                lbl = tk.Label(master=frm_4, text=f"элемен №_{element} Название: {plan[link][element]['name']}: Дата замены: {plan[link][element]['date'].strftime('%d.%m.%y')}")
                lbl.grid(row=link, column=element, padx=5, pady=5, sticky='n')

def run():
    global elements
    global names
    os.system('python add.py')
    for label in frm_com.grid_slaves():
        if int(label.grid_info()["row"]) > 0 and int(label.grid_info()["row"]) < 5:
            label.destroy()
    elements, names = get_elements()

def draw():
    os.system('python graph.py')

window = tk.Tk()
window.title("Определение оптимального срока службы элементов системы")

frm_1 = tk.Frame(master=window, relief=tk.SUNKEN, borderwidth=3)
frm_1.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky='nsew')

window.rowconfigure([0, 1, 2], weight=1, minsize=50)
window.columnconfigure([0, 1, 2], weight=1, minsize=50)

frm_1.rowconfigure([0, 1, 2], weight=0, minsize=20)
frm_1.columnconfigure(0, weight=1, minsize=50)

# Фрейм для конструктора
frm_con = tk.Frame(master=frm_1, relief=tk.SUNKEN, borderwidth=3)
frm_con.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

frm_con.rowconfigure([0, 1, 2, 3, 4], weight=0, minsize=10)
frm_con.columnconfigure(0, weight=1, minsize=25)

# Данные
shema_data = {}

# Данные для конструктора [id, link, name, наработка на отказ, номинальная интенсивность отказа]
# данные по первой конфигурации элементов

def get_data():
    sql = f'SELECT * FROM elements'
    conn = sqlite3.connect('database.db')
    data = conn.execute(sql).fetchall()
    conn.close()
    return data

def get_elements():
    elements = {}
    row_data = get_data()
    for data in row_data:
        elements[data[0]] = {'name': data[1], 'fault': data[2], 'intensity': data[3]}
    names = [element['name'] for element in elements.values()]
    return (elements, names)

elements, names = get_elements()

def get_element(name):
    sql = f"SELECT * FROM elements WHERE name='{name}'"
    conn = sqlite3.connect('database.db')
    data = conn.execute(sql).fetchone()
    conn.close()
    entry_1['text'] = data[1]
    entry_2['text'] = str(data[2])
    entry_3['text'] = str(data[3])

def ok_1():
    for label in frm_com.grid_slaves():
        if int(label.grid_info()["row"]) > 0 and int(label.grid_info()["row"]) < 5:
            label.destroy()
    variable_1 = tk.StringVar(window)
    variable_1.set(names[0])
    w_1 = tk.OptionMenu(frm_com, variable_1, *names)
    lbl_1 = tk.Label(master=frm_com, text='1')
    bnt_inf_1 = tk.Button(master=frm_com, text='Информация', command=(lambda: get_element(variable_1.get())))
    ent_date_1 = tk.Entry(master=frm_com, width=20)
    lbl_1.grid(row=1, column=0, sticky='e')
    w_1.grid(row=1, column=1, padx=5, pady=5, sticky='n')
    bnt_inf_1.grid(row=1, column=2, padx=5, pady=5, sticky='n')
    ent_date_1.grid(row=1, column=3, padx=5, pady=5, sticky='n')

def ok_2():
    for label in frm_com.grid_slaves():
        if int(label.grid_info()["row"]) > 0 and int(label.grid_info()["row"]) < 5:
            label.destroy()
    variable_1 = tk.StringVar(window)
    variable_1.set(names[0])
    variable_2 = tk.StringVar(window)
    variable_2.set(names[0])
    w_1 = tk.OptionMenu(frm_com, variable_1, *names)
    w_2 = tk.OptionMenu(frm_com, variable_2, *names)
    lbl_1 = tk.Label(master=frm_com, text='1')
    lbl_2 = tk.Label(master=frm_com, text='2')
    bnt_inf_1 = tk.Button(master=frm_com, text='Информация', command=(lambda: get_element(variable_1.get())))
    bnt_inf_2 = tk.Button(master=frm_com, text='Информация', command=(lambda: get_element(variable_2.get())))
    ent_date_1 = tk.Entry(master=frm_com, width=20)
    ent_date_2 = tk.Entry(master=frm_com, width=20)
    lbl_1.grid(row=1, column=0, sticky='e')
    lbl_2.grid(row=2, column=0, sticky='e')
    w_1.grid(row=1, column=1, padx=5, pady=5, sticky='n')
    w_2.grid(row=2, column=1, padx=5, pady=5, sticky='n')
    bnt_inf_1.grid(row=1, column=2, padx=5, pady=5, sticky='n')
    bnt_inf_2.grid(row=2, column=2, padx=5, pady=5, sticky='n')
    ent_date_1.grid(row=1, column=3, padx=5, pady=5, sticky='n')
    ent_date_2.grid(row=2, column=3, padx=5, pady=5, sticky='n')

def ok_3():
    for label in frm_com.grid_slaves():
        if int(label.grid_info()["row"]) > 0 and int(label.grid_info()["row"]) < 5:
            label.destroy()
    variable_1 = tk.StringVar(window)
    variable_1.set(names[0])
    variable_2 = tk.StringVar(window)
    variable_2.set(names[0])
    variable_3 = tk.StringVar(window)
    variable_3.set(names[0])
    w_1 = tk.OptionMenu(frm_com, variable_1, *names)
    w_2 = tk.OptionMenu(frm_com, variable_2, *names)
    w_3 = tk.OptionMenu(frm_com, variable_3, *names)
    lbl_1 = tk.Label(master=frm_com, text='1')
    lbl_2 = tk.Label(master=frm_com, text='2')
    lbl_3 = tk.Label(master=frm_com, text='3')
    bnt_inf_1 = tk.Button(master=frm_com, text='Информация', command=(lambda: get_element(variable_1.get())))
    bnt_inf_2 = tk.Button(master=frm_com, text='Информация', command=(lambda: get_element(variable_2.get())))
    bnt_inf_3 = tk.Button(master=frm_com, text='Информация', command=(lambda: get_element(variable_3.get())))
    ent_date_1 = tk.Entry(master=frm_com, width=20)
    ent_date_2 = tk.Entry(master=frm_com, width=20)
    ent_date_3 = tk.Entry(master=frm_com, width=20)
    lbl_1.grid(row=1, column=0, sticky='e')
    lbl_2.grid(row=2, column=0, sticky='e')
    lbl_3.grid(row=3, column=0, sticky='e')
    w_1.grid(row=1, column=1, padx=5, pady=5, sticky='n')
    w_2.grid(row=2, column=1, padx=5, pady=5, sticky='n')
    w_3.grid(row=3, column=1, padx=5, pady=5, sticky='n')
    bnt_inf_1.grid(row=1, column=2, padx=5, pady=5, sticky='n')
    bnt_inf_2.grid(row=2, column=2, padx=5, pady=5, sticky='n')
    bnt_inf_3.grid(row=3, column=2, padx=5, pady=5, sticky='n')
    ent_date_1.grid(row=1, column=3, padx=5, pady=5, sticky='n')
    ent_date_2.grid(row=2, column=3, padx=5, pady=5, sticky='n')
    ent_date_3.grid(row=3, column=3, padx=5, pady=5, sticky='n')

def ok_4():
    for label in frm_com.grid_slaves():
        if int(label.grid_info()["row"]) > 0 and int(label.grid_info()["row"]) < 5:
            label.destroy()
    variable_1 = tk.StringVar(window)
    variable_1.set(names[0])
    variable_2 = tk.StringVar(window)
    variable_2.set(names[0])
    variable_3 = tk.StringVar(window)
    variable_3.set(names[0])
    variable_4 = tk.StringVar(window)
    variable_4.set(names[0])
    w_1 = tk.OptionMenu(frm_com, variable_1, *names)
    w_2 = tk.OptionMenu(frm_com, variable_2, *names)
    w_3 = tk.OptionMenu(frm_com, variable_3, *names)
    w_4 = tk.OptionMenu(frm_com, variable_4, *names)
    lbl_1 = tk.Label(master=frm_com, text='1')
    lbl_2 = tk.Label(master=frm_com, text='2')
    lbl_3 = tk.Label(master=frm_com, text='3')
    lbl_4 = tk.Label(master=frm_com, text='4')
    bnt_inf_1 = tk.Button(master=frm_com, text='Информация', command=(lambda: get_element(variable_1.get())))
    bnt_inf_2 = tk.Button(master=frm_com, text='Информация', command=(lambda: get_element(variable_2.get())))
    bnt_inf_3 = tk.Button(master=frm_com, text='Информация', command=(lambda: get_element(variable_3.get())))
    bnt_inf_4 = tk.Button(master=frm_com, text='Информация', command=(lambda: get_element(variable_4.get())))
    ent_date_1 = tk.Entry(master=frm_com, width=20)
    ent_date_2 = tk.Entry(master=frm_com, width=20)
    ent_date_3 = tk.Entry(master=frm_com, width=20)
    ent_date_4 = tk.Entry(master=frm_com, width=20)
    lbl_1.grid(row=1, column=0, sticky='e')
    lbl_2.grid(row=2, column=0, sticky='e')
    lbl_3.grid(row=3, column=0, sticky='e')
    lbl_4.grid(row=4, column=0, sticky='e')
    w_1.grid(row=1, column=1, padx=5, pady=5, sticky='n')
    w_2.grid(row=2, column=1, padx=5, pady=5, sticky='n')
    w_3.grid(row=3, column=1, padx=5, pady=5, sticky='n')
    w_4.grid(row=4, column=1, padx=5, pady=5, sticky='n')
    bnt_inf_1.grid(row=1, column=2, padx=5, pady=5, sticky='n')
    bnt_inf_2.grid(row=2, column=2, padx=5, pady=5, sticky='n')
    bnt_inf_3.grid(row=3, column=2, padx=5, pady=5, sticky='n')
    bnt_inf_4.grid(row=4, column=2, padx=5, pady=5, sticky='n')
    ent_date_1.grid(row=1, column=3, padx=5, pady=5, sticky='n')
    ent_date_2.grid(row=2, column=3, padx=5, pady=5, sticky='n')
    ent_date_3.grid(row=3, column=3, padx=5, pady=5, sticky='n')
    ent_date_4.grid(row=4, column=3, padx=5, pady=5, sticky='n')

#Виджеты Конструктор
constructer = tk.Label(master=frm_con, text='Конструктор')
constructer.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

number_of_link = tk.Entry(master=frm_con)
number_of_link.grid(row=1, column=0, padx=5, pady=5, sticky="n")

btn_1 = tk.Button(master=frm_con, text='1', width=10, command=ok_1)
btn_1.grid(row=2, column=0, padx=5, pady=5, sticky='n')

btn_2 = tk.Button(master=frm_con, text='2', width=10, command=ok_2)
btn_2.grid(row=3, column=0, padx=5, pady=5, sticky='n')

btn_3 = tk.Button(master=frm_con, text='3', width=10, command=ok_3)
btn_3.grid(row=4, column=0, padx=5, pady=5, sticky='n')

btn_4 = tk.Button(master=frm_con, text='4', width=10, command=ok_4)
btn_4.grid(row=5, column=0, padx=5, pady=5, sticky='n')

# Фрейм для компонент
frm_com = tk.Frame(master=frm_1, relief=tk.SUNKEN, borderwidth=3)
frm_com.grid(row=0, column=1, padx=5, columnspan=2, pady=5, sticky='nsew')

frm_com.rowconfigure(0, weight=0, minsize=10)
frm_com.rowconfigure([1, 2, 3, 4, 5], weight=0, minsize=25)
frm_com.columnconfigure([1, 2], weight=1, minsize=25)

# Виджеты для компонент
lbl_components = tk.Label(master=frm_com, text='Компоненты')
lbl_date = tk.Label(master=frm_com, text='Дата установки')
lbl_components.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="n")
lbl_date.grid(row=0, column=3, padx=5, pady=5, sticky="n")

def h(name):
    sql = f"SELECT * FROM elements WHERE name='{name}'"
    conn = sqlite3.connect('database.db')
    data = conn.execute(sql).fetchone()
    conn.close()
    return data

def add_link():
    link = number_of_link.get()
    number_of_element_1 = None
    name_of_element_1 = None
    date_of_element_1 = None
    number_of_element_2 = None
    name_of_element_2 = None
    date_of_element_2 = None
    number_of_element_3 = None
    name_of_element_3 = None
    date_of_element_3 = None
    number_of_element_4 = None
    name_of_element_4 = None
    date_of_element_4 = None
    for label in frm_com.grid_slaves():
        if int(label.grid_info()["row"]) > 0 and int(label.grid_info()["row"]) < 5:
            if int(label.grid_info()["row"]) == 1 and int(label.grid_info()["column"]) == 0:
                number_of_element_1 = int(label['text'])
            if int(label.grid_info()["row"]) == 1 and int(label.grid_info()["column"]) == 1:
                name_of_element_1 = label['text']
                fault_1 = h(name_of_element_1)[2]
                intensity_1 = h(name_of_element_1)[3]
            if int(label.grid_info()["row"]) == 1 and int(label.grid_info()["column"]) == 3:
                date_of_element_1 = datetime.datetime.strptime(label.get(), '%d.%m.%y')
            if int(label.grid_info()["row"]) == 2 and int(label.grid_info()["column"]) == 0:
                number_of_element_2 = int(label['text'])
            if int(label.grid_info()["row"]) == 2 and int(label.grid_info()["column"]) == 1:
                name_of_element_2 = label['text']
                fault_2 = h(name_of_element_2)[2]
                intensity_2 = h(name_of_element_2)[3]
            if int(label.grid_info()["row"]) == 2 and int(label.grid_info()["column"]) == 3:
                date_of_element_2 = datetime.datetime.strptime(label.get(), '%d.%m.%y')
            if int(label.grid_info()["row"]) == 3 and int(label.grid_info()["column"]) == 0:
                number_of_element_3 = int(label['text'])
            if int(label.grid_info()["row"]) == 3 and int(label.grid_info()["column"]) == 1:
                name_of_element_3 = label['text']
                fault_3 = h(name_of_element_3)[2]
                intensity_3 = h(name_of_element_3)[3]
            if int(label.grid_info()["row"]) == 3 and int(label.grid_info()["column"]) == 3:
                date_of_element_3 = datetime.datetime.strptime(label.get(), '%d.%m.%y')
            if int(label.grid_info()["row"]) == 4 and int(label.grid_info()["column"]) == 0:
                number_of_element_4 = int(label['text'])
            if int(label.grid_info()["row"]) == 4 and int(label.grid_info()["column"]) == 1:
                name_of_element_4 = label['text']
                fault_4 = h(name_of_element_4)[2]
                intensity_4 = h(name_of_element_4)[3]
            if int(label.grid_info()["row"]) == 4 and int(label.grid_info()["column"]) == 3:
                date_of_element_4 = datetime.datetime.strptime(label.get(), '%d.%m.%y')
    if number_of_element_4:
        shema_data[int(link)] = {
            number_of_element_1: {'name': name_of_element_1, 'fault': fault_1, 'intensity': intensity_1, 'date': date_of_element_1},
            number_of_element_2: {'name': name_of_element_2, 'fault': fault_2, 'intensity': intensity_2, 'date': date_of_element_2},
            number_of_element_3: {'name': name_of_element_3, 'fault': fault_3, 'intensity': intensity_3, 'date': date_of_element_3},
            number_of_element_4: {'name': name_of_element_4, 'fault': fault_4, 'intensity': intensity_4, 'date': date_of_element_4}
        }
        start = int(link)
        for label in frm_2.grid_slaves():
            if int(label.grid_info()["row"]) == start:
                label.destroy()
        lbl_number = tk.Label(master=frm_2, text=f'Номер звена: {start}')
        lbl_number.grid(row=start, column=0, sticky='e')
        lbl_name_1 = tk.Label(master=frm_2, text=f"{name_of_element_1}: дата установки: {date_of_element_1.strftime('%d.%m.%y')}")
        lbl_name_1.grid(row=start, column=1, sticky='n')
        lbl_name_2 = tk.Label(master=frm_2, text=f"{name_of_element_2}: дата установки: {date_of_element_2.strftime('%d.%m.%y')}")
        lbl_name_2.grid(row=start, column=2, sticky='n')
        lbl_name_3 = tk.Label(master=frm_2, text=f"{name_of_element_3}: дата установки: {date_of_element_3.strftime('%d.%m.%y')}")
        lbl_name_3.grid(row=start, column=3, sticky='n')
        lbl_name_4 = tk.Label(master=frm_2, text=f"{name_of_element_4}: дата установки: {date_of_element_4.strftime('%d.%m.%y')}")
        lbl_name_4.grid(row=start, column=4, sticky='n')
    elif number_of_element_3:
        shema_data[int(link)] = {
            number_of_element_1: {'name': name_of_element_1, 'fault': fault_1, 'intensity': intensity_1, 'date': date_of_element_1},
            number_of_element_2: {'name': name_of_element_2, 'fault': fault_2, 'intensity': intensity_2, 'date': date_of_element_2},
            number_of_element_3: {'name': name_of_element_3, 'fault': fault_3, 'intensity': intensity_3, 'date': date_of_element_3}
        }
        start = int(link)
        for label in frm_2.grid_slaves():
            if int(label.grid_info()["row"]) == start:
                label.destroy()
        lbl_number = tk.Label(master=frm_2, text=f'Номер звена: {start}')
        lbl_number.grid(row=start, column=0, sticky='e')
        lbl_name_1 = tk.Label(master=frm_2, text=f"{name_of_element_1}: дата установки: {date_of_element_1.strftime('%d.%m.%y')}")
        lbl_name_1.grid(row=start, column=1, sticky='n')
        lbl_name_2 = tk.Label(master=frm_2, text=f"{name_of_element_2}: дата установки: {date_of_element_2.strftime('%d.%m.%y')}")
        lbl_name_2.grid(row=start, column=2, sticky='n')
        lbl_name_3 = tk.Label(master=frm_2, text=f"{name_of_element_3}: дата установки: {date_of_element_3.strftime('%d.%m.%y')}")
        lbl_name_3.grid(row=start, column=3, sticky='n')
    elif number_of_element_2:
        shema_data[int(link)] = {
            number_of_element_1: {'name': name_of_element_1, 'fault': fault_1, 'intensity': intensity_1, 'date': date_of_element_1},
            number_of_element_2: {'name': name_of_element_2, 'fault': fault_2, 'intensity': intensity_2, 'date': date_of_element_2}
        }
        start = int(link)
        for label in frm_2.grid_slaves():
            if int(label.grid_info()["row"]) == start:
                label.destroy()
        lbl_number = tk.Label(master=frm_2, text=f'Номер звена: {start}')
        lbl_number.grid(row=start, column=0, sticky='e')
        lbl_name_1 = tk.Label(master=frm_2, text=f"{name_of_element_1}: дата установки: {date_of_element_1.strftime('%d.%m.%y')}")
        lbl_name_1.grid(row=start, column=1, sticky='n')
        lbl_name_2 = tk.Label(master=frm_2, text=f"{name_of_element_2}: дата установки: {date_of_element_2.strftime('%d.%m.%y')}")
        lbl_name_2.grid(row=start, column=2, sticky='n')
    elif number_of_element_1:
        shema_data[int(link)] = {
            number_of_element_1: {'name': name_of_element_1, 'fault': fault_1, 'intensity': intensity_1, 'date': date_of_element_1}
        }
        start = int(link)
        for label in frm_2.grid_slaves():
            if int(label.grid_info()["row"]) == start:
                label.destroy()
        lbl_number = tk.Label(master=frm_2, text=f'Номер звена: {start}')
        lbl_number.grid(row=start, column=0, sticky='e')
        lbl_name_1 = tk.Label(master=frm_2, text=f"{name_of_element_1}: дата установки: {date_of_element_1.strftime('%d.%m.%y')}")
        lbl_name_1.grid(row=start, column=1, sticky='n')

btn_add = tk.Button(master=frm_com, text='Добавить звено в цепь', command=add_link)
btn_add.grid(row=5, column=2, sticky='ew')

# требуемый уровень надежности
reliability = tk.Label(master=frm_1, text='Требуемый уровень надежности:')
reliability.grid(row=1, column=0, padx=10, pady=10, sticky='n')

ent_reliability = tk.Entry(master=frm_1, width=50, relief=tk.SUNKEN, borderwidth=3)
ent_reliability.grid(row=1, column=1, padx=10, pady=10,)

btn_reliability = tk.Button(master=frm_1, text="Вывод плана замены оборудования", command=solver)
btn_reliability.grid(row=1, column=2, padx=10, pady=10, sticky='e')

# btn_graph = tk.Button(master=frm_1, text='Вывести график', command=draw)
# btn_graph.grid(row=2, column=2, padx=10, pady=10, sticky='e')

# Схема
frm_2 = tk.Frame(master=window, relief=tk.SUNKEN, borderwidth=3)
frm_2.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky='nsew')
frm_2.rowconfigure([0, 1, 2], weight=0, minsize=20)
frm_2.columnconfigure([0, 1, 2, 3, 4], weight=1, minsize=50)

shema = tk.Label(master=frm_2, text='Схема')
shema.grid(row=0, column=0, padx=5, pady=5, sticky="n")

# Информация о выбранном компоненте
frm_3 = tk.Frame(master=window, relief=tk.SUNKEN, borderwidth=3)
frm_3.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky='nsew')
inf = tk.Label(master=frm_3, text='Информация о выбранном компоненте:')
inf.grid(row=0, column=0, padx=5, pady=5, sticky="n")

# Наименование
label_1 = tk.Label(master=frm_3, text="Наименование:")
entry_1 = tk.Label(master=frm_3, width=50, relief=tk.SUNKEN, borderwidth=3)
label_1.grid(row=1, column=0, sticky="e")
entry_1.grid(row=1, column=1)

# Наработка на отказ
label_2 = tk.Label(master=frm_3, text="Наработка на отказ:")
entry_2 = tk.Label(master=frm_3, width=50, relief=tk.SUNKEN, borderwidth=3)
label_2.grid(row=2, column=0, sticky="e")
entry_2.grid(row=2, column=1)

#Номинальная интенсивность отказов
label_3 = tk.Label(master=frm_3, text="Номинальная интенсивность отказов:")
entry_3 = tk.Label(master=frm_3, width=50, relief=tk.SUNKEN, borderwidth=3)
label_3.grid(row=3, column=0, sticky="e")
entry_3.grid(row=3, column=1)

# Кнопка добавить
label_4 = tk.Button(master=frm_3, text="Добавить компонент", command=run)
label_4.grid(row=4, column=1, sticky="e")

# Вывод плана замены оборудования
frm_4 = tk.Frame(master=window, relief=tk.SUNKEN, borderwidth=3)
frm_4.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky='nsew')

window.mainloop()
