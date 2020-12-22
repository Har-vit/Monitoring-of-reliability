import tkinter
import math
import sqlite3

# Данные
shema_data = {}

# Определение функций
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

def solver():
    plan = shema_data
    data = {}
    number = 1
    p = float(ent_reliability.get())
    p_i = p ** (1 / number)

    p_i_j = p_i
    result = - float(math.log(p_i_j) * float(shema_data[link][1]['fault']))
    plan[link][1]['date'] += datetime.timedelta(days=int(result))

# def h(name):
#     sql = f"SELECT * FROM elements WHERE name='{name}'"
#     conn = sqlite3.connect('database.db')
#     data = conn.execute(sql).fetchone()
#     conn.close()
#     return data
#
# number_of_element_1 = None
# name_of_element_1 = None
# date_of_element_1 = None

# name_of_element_1 = label['text']
# fault_1 = h(name_of_element_1)[2]
# intensity_1 = h(name_of_element_1)[3]

# shema_data[1] = {
#     number_of_element_1: {'name': name_of_element_1, 'fault': fault_1, 'intensity': intensity_1,
#                           'date': date_of_element_1}
# }

def plot_x_axe(x0,y0,x1):
    x_axe=[]
    xx=(x0,y0)
    x_axe.append(xx)
    xx=(x1,y0)
    x_axe.append(xx)
    canvas.create_line(x_axe, fill="black", width=2)

def plot_y_axe(x0,y0,y1):
    y_axe=[]
    yy=(x0,y1)
    y_axe.append(yy)
    yy=(x0,y0)
    y_axe.append(yy)
    canvas.create_line(y_axe,fill="black",width=2)

def plot_func0(x0,x1,dx,y0,y1):
    x0i=int(x0)
    x1i=int(x1)
    y0i=int(y0)
    y1i=int(y1)
    a=y1
    b=(y0-y1)/(x1-x0)
    points=[]
    for x in range(x0i,x1i,dx):
        y=int(a+b*x)
        pp=(x,y)
        points.append(pp)

    canvas.create_line(points,fill="blue",smooth=1)
    plot_y_axe(x0i,y0i,y1i)
    plot_x_axe(x0i,y0i,x1i)

def plot_func1(x0,x1,dx,y0,y1):
    x0i=int(x0)
    x1i=int(x1)
    y0i=int(y0)
    y1i=int(y1)
    a=y0
    b=y0-y1
    points=[]
    for x in range(x0i,x1i,dx):
        y=int(a-y1i*b/x)
        pp=(x,y)
        points.append(pp)

    canvas.create_line(points,fill="blue",smooth=1)
    plot_y_axe(x0i,y0i,y1i)
    plot_x_axe(x0i,y0i,x1i)

def plot_func2(x0,x1,dx,y0,y1):
    x0i = int(x0)
    x1i = int(x1)
    y0i = int(y0)
    y1i = int(y1)
    a = (y0-y1) / (15 * x1)
    b = 1 + ((y0-y1) / (x1-x0))
    points = []
    for x in range(x0i, x1i, dx):
        y = y0i-int(a * (x-x0i) ** b)
        pp = (x, y)
        points.append(pp)

    canvas.create_line(points, fill="blue", smooth=1)
    plot_y_axe(x0i, y0i, y1i)
    plot_x_axe(x0i, y0i, x1i)

def plot_func3(x0, x1, dx, y0, y1):
    x0i = int(x0)
    x1i = int(x1)
    y0i = int(y0)
    y1i = int(y1)
    ay = 150
    y0i = 150
    points = []
    for x in range(x0i, x1i, dx):
        y = y0i-ay * math.cos(x * dx)
        pp = (x, y)
        points.append(pp)

    canvas.create_line(points, fill="blue", smooth=1)
    plot_y_axe(x0i, 0, y0i + ay)
    plot_x_axe(x0i, y0i, x1i)

def DrawGraph():
    fn = func.get()
    f = fn[0]
    x0 = 50.0
    y0 = 250.0
    x1 = 450.0
    y1 = 50.0
    dx = 10
    #
    if f == "0":
        canvas.delete("all")
        plot_func0(x0, x1, dx, y0, y1)
    elif f == "1":
        canvas.delete("all")
        plot_func1(x0, x1, dx, y0, y1)
    elif f == "2":
        canvas.delete("all")
        plot_func2(x0, x1, dx, y0, y1)
    else:
        canvas.delete("all")
        plot_func3(x0, x1, dx, y0, y1)

# Основная часть
tk = tkinter.Tk()
tk.title("Визуализация изменения надежности элемента во времени")
# Верхняя часть окна со списком и кнопками
menuframe = tkinter.Frame(tk)
menuframe.pack({"side": "top", "fill": "x"})
# требуемый уровень надежности
reliability = tkinter.Label(menuframe, text='Требуемый уровень надежности:')
reliability.pack({"side": "left"})
ent_reliability = tkinter.Entry(menuframe)
ent_reliability.pack({"side": "left"})
# текущая дата
reliability = tkinter.Label(menuframe, text='текущая дата дата:')
reliability.pack({"side": "left"})
ent_reliability = tkinter.Entry(menuframe)
ent_reliability.pack({"side": "left"})
# конечная дата
reliability = tkinter.Label(menuframe, text='Конечная дата:')
reliability.pack({"side": "left"})
ent_reliability = tkinter.Entry(menuframe)
ent_reliability.pack({"side": "left"})
# Надпись для списка
lbl = tkinter.Label(menuframe)
lbl["text"] = "Выбор:"
lbl.pack({"side": "left"})
# Инициализация и формирования списка
func = tkinter.StringVar(tk)
# func.set('0 y=Ax+B')
#
# fspis = tkinter.OptionMenu(menuframe, func,
#                            '0 y=Ax+B',
#                            '1 y=A+B/x',
#                            '2 y=Ax^B',
#                            '3 y=A*cos(Bx)')

func.set(names[0])
fspis = tkinter.OptionMenu(menuframe, func, *names)

fspis.pack({"side": "left"})
# Кнопка управления рисованием
btnOk = tkinter.Button(menuframe)
btnOk["text"] = "Нарисовать"
btnOk["command"] = DrawGraph
btnOk.pack({"side": "left"})
# Кнопка закрытия приложения
button = tkinter.Button(menuframe)
button["text"] = "Закрыть"
button["command"] = tk.quit
button.pack({"side": "right"})
# Область рисования (холст)
canvas = tkinter.Canvas(tk)
canvas["height"] = 360
canvas["width"] = 480
canvas["background"] = "#eeeeff"
canvas["borderwidth"] = 2
canvas.pack({"side": "bottom"})

tk.mainloop()

