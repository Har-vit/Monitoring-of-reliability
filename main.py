import tkinter as tk
from tkinter import ttk
import pandas as pd
import sqlite3
import math

class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self):
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file='add.gif')
        btn_open_dialog = tk.Button(toolbar, text='Добавить оценку', command=self.open_dialog, bg='#d7d8e0', bd=0,
                                    compound=tk.TOP, image=self.add_img)
        btn_open_dialog.pack(side=tk.LEFT)

        self.update_img = tk.PhotoImage(file='update.gif')
        btn_edit_dialog = tk.Button(toolbar, text='Редактировать', bg='#d7d8e0', bd=0, image=self.update_img,
                                    compound=tk.TOP, command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        self.delete_img = tk.PhotoImage(file='delete.gif')
        btn_delete = tk.Button(toolbar, text='Удалить оценку', bg='#d7d8e0', bd=0, image=self.delete_img,
                               compound=tk.TOP, command=self.delete_records)
        btn_delete.pack(side=tk.LEFT)

        self.search_img = tk.PhotoImage(file='search.gif')
        btn_search = tk.Button(toolbar, text='Поиск', bg='#d7d8e0', bd=0, image=self.search_img,
                               compound=tk.TOP, command=self.open_search_dialog)
        btn_search.pack(side=tk.LEFT)

        self.refresh_img = tk.PhotoImage(file='refresh.gif')
        btn_refresh = tk.Button(toolbar, text='Обновить', bg='#d7d8e0', bd=0, image=self.refresh_img,
                                compound=tk.TOP, command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(self, columns=('ID', 'description', 'probability'), height=15, show='headings')

        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('description', width=1200, anchor='w')
        self.tree.column('probability', width=150, anchor='w')

        self.tree.heading('ID', text='ID')
        self.tree.heading('description', text='Вид деятельности')
        self.tree.heading('probability', text='Частота ошибок')

        self.tree.pack()

    def records(self, description, probability):
        self.db.insert_data(description, probability)
        self.view_records()

    def update_record(self, description, probability):
        self.db.c.execute('''UPDATE probabilities SET description=?, probability=? WHERE ID=?''',
                          (description, probability, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()

    def view_records(self):
        self.db.c.execute('''SELECT * FROM probabilities''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.c.execute('''DELETE FROM probabilities WHERE id=?''', (self.tree.set(selection_item, '#1'),))
        self.db.conn.commit()
        self.view_records()

    def search_records(self, description):
        description = ('%' + description + '%',)
        self.db.c.execute('''SELECT * FROM probabilities WHERE description LIKE ?''', description)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def open_dialog(self):
        Child()

    def open_update_dialog(self):
        Update()

    def open_search_dialog(self):
        Search()


class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app
        self.probability_culc()

    def probability_culc(self):
        try:
            pisp = float(self.entry_probability_1.get()) * float(self.entry_probability_2.get()) * float(self.entry_probability_3.get())
            pop = math.exp(-(float(self.entry_2.get()) / float(self.entry_1.get()) * float(self.entry_3.get())) * float(self.entry_3.get()) * float(self.entry_4.get()))
            return pop + (1 - pop) * pisp
        except ValueError:
            tk.Label(text="Ошибка. Ввод некорректен.")

    def init_child(self):
        self.title('Добавить оценку')
        self.geometry('900x400+400+300')
        # self.resizable(False, False)

        label_description = tk.Label(self, text='Вид деятельности:')
        label_description.place(x=50, y=50)

        label_probability_1 = tk.Label(self, text='Вероятность выдачи сигнала системой контроля:')
        label_probability_1.place(x=50, y=80)

        label_probability_2 = tk.Label(self, text='Вероятность обнаружения диспетчером сигнала контроля:')
        label_probability_2.place(x=50, y=110)

        label_probability_3 = tk.Label(self, text='Вероятность исправления ошибочных действий при повторном выполнении операции:')
        label_probability_3.place(x=50, y=140)

        label_1 = tk.Label(self, text='Общее число выполненных операций:')
        label_1.place(x=50, y=170)

        label_2 = tk.Label(self, text='Число допущенных ошибок:')
        label_2.place(x=50, y=200)

        label_3 = tk.Label(self, text='Среднее время выполнения операций:')
        label_3.place(x=50, y=230)

        label_4 = tk.Label(self, text='Число выполненных операций:')
        label_4.place(x=50, y=260)

        self.entry_description = ttk.Entry(self)
        self.entry_description.place(x=200, y=50)

        self.entry_probability_1 = ttk.Entry(self)
        self.entry_probability_1.place(x=415, y=80)

        self.entry_probability_2 = ttk.Entry(self)
        self.entry_probability_2.place(x=485, y=110)

        self.entry_probability_3 = ttk.Entry(self)
        self.entry_probability_3.place(x=685, y=140)

        self.entry_1 = ttk.Entry(self)
        self.entry_1.place(x=335, y=170)

        self.entry_2 = ttk.Entry(self)
        self.entry_2.place(x=265, y=200)

        self.entry_3 = ttk.Entry(self)
        self.entry_3.place(x=340, y=230)

        self.entry_4 = ttk.Entry(self)
        self.entry_4.place(x=285, y=260)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=300)

        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y=300)
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_description.get(), self.probability_culc()))
        self.grab_set()
        self.focus_set()

class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        # self.default_data()

    def init_edit(self):
        self.title('Редактировать оценку')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=185, y=300)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_record(self.entry_description.get(),
                                                                          self.probability_culc()))

        self.btn_ok.destroy()

    # def default_data(self):
    #     self.db.c.execute('''SELECT * FROM probabilities WHERE id=?''',
    #                       (self.view.tree.set(self.view.tree.selection()[0], '#1'),))
    #     row = self.db.c.fetchone()
    #     self.entry_description.insert(0, row[1])
    #     self.entry_probability.insert(0, row[2])


class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Поиск')
        self.geometry('300x100+400+300')
        # self.resizable(False, False)

        label_search = tk.Label(self, text='Поиск')
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Поиск')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event: self.view.search_records(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('probabilities.db')
        self.c = self.conn.cursor()
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS probabilities (id integer primary key, description text, probability text)''')
        self.conn.commit()

    def insert_data(self, description, probability):
        self.c.execute('''INSERT INTO probabilities(description, probability) VALUES (?, ?)''',
                       (description, probability))
        self.conn.commit()

def import_data():
    conn = sqlite3.connect("probabilities.db")
    df = pd.read_excel('probabilities.xlsx')
    df.to_sql("probabilities", conn, if_exists="replace", index=False)

def export_data():
    conn = sqlite3.connect("probabilities.db")
    df = pd.read_sql_query("select * from probabilities;", conn)
    df.to_excel("probabilities.xlsx", index=False)

if __name__ == "__main__":

    root = tk.Tk()
    main_menu = tk.Menu(root)
    root.configure(menu=main_menu)
    first_item = tk.Menu(main_menu)
    main_menu.add_cascade(label="Файл", menu=first_item)
    first_item.add_command(label="Импорт", command=import_data)
    first_item.add_command(label="Экспорт", command=export_data)
    db = DB()
    app = Main(root)
    app.pack()
    root.title("Оценка надежности безошибочного выполнения задач оператором")
    root.geometry("1400x450+300+200")
    # root.resizable(False, False)
    root.mainloop()

