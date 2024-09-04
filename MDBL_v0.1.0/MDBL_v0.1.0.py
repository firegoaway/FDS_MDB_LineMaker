import re
import tkinter as tk
from tkinter import messagebox
import configparser
import os

class Tooltip(object):
    """    Другой метод создания тултипсов    """
    def __init__(self, widget, text='widget info'):
        self.waittime = 200     # время ожидания после наведения
        self.wraplength = 280   # размер области отображения тултипса
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # Создаем окошко верхнего уровня
        self.tw = tk.Toplevel(self.widget)
        # Оставляем единственную метку и убираем окно
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                       background="#ffffff", relief='solid', borderwidth=1,
                       wraplength = self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()

def read_file_path(ini_file):
    config = configparser.ConfigParser()
    config.read(ini_file, encoding='utf-16')
    return config['filePath']['filePath']

def calculate_cell_sizes(meshes):
    max_cs_values = []
    mode = 'LES'

    for I, J, K, X1, X2, Y1, Y2, Z1, Z2 in meshes:
        Csx = (X2 - X1) / I
        Csy = (Y2 - Y1) / J
        Csz = (Z2 - Z1) / K
        Cs = (Csx + Csy + Csz) / 3
        max_cs_values.append(Cs)

        if Cs > 0.2125:
            mode = None

    return max(max_cs_values), mode


def submit_changes(file_path, level, add_rhf, add_bwt, add_wt):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    meshes, min_x1, max_x2, min_y1, max_y2 = parse_fds_file(file_path)
    max_cs, simulation_mode = calculate_cell_sizes(meshes)

    # Update &MISC line
    for i, line in enumerate(lines):
        if line.startswith("&MISC"):
            if max_cs > 0.2125:
                line = line.strip().rstrip("/") + " MAXIMUM_VISIBILITY=100.0, VISIBILITY_FACTOR=2.38 /"
            else:
                line = line.strip().rstrip("/") + " MAXIMUM_VISIBILITY=100.0, VISIBILITY_FACTOR=2.38 SIMULATION_MODE='LES' /"
            lines[i] = line + "\n"
            break

    Zh = level + 1.7
    devc_lines = [
        f"&DEVC ID='Radiative Heat Flux_SURFACE INTEGRAL', QUANTITY='RADIATIVE HEAT FLUX', SPATIAL_STATISTIC='SURFACE INTEGRAL', XB={min_x1},{max_x2},{min_y1},{max_y2},{Zh},{Zh}/\n"
    ]

    if add_rhf:
        devc_lines.append("&BNDF QUANTITY='RADIATIVE HEAT FLUX'/\n")
    if add_bwt:
        devc_lines.append("&BNDF QUANTITY='BACK WALL TEMPERATURE'/\n")
    if add_wt:
        devc_lines.append("&BNDF QUANTITY='WALL TEMPERATURE'/\n")

    for i, line in enumerate(lines):
        if line.startswith("&TAIL"):
            lines = lines[:i] + devc_lines + lines[i:]
            break

    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)


def on_submit():
    try:
        level = float(level_entry.get())
        submit_changes(file_path, level, rhf_var.get(), bwt_var.get(), wt_var.get())
        messagebox.showinfo("Принято", "Данные успешно добавлены")
    except ValueError:
        messagebox.showerror("Ошибка ввода", "Пожалуйста, введите рациональное число")


def load_file_path():
    current_directory = os.path.dirname(__file__)
    parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
    inis_path = os.path.join(parent_directory, 'inis')
        
    ini_path = os.path.join(inis_path, 'filePath.ini')
    
    try:
        return read_file_path(ini_path)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось считать путь к файлу: {str(e)}")


if __name__ == "__main__":
    file_path = load_file_path()
    
    current_directory = os.path.dirname(__file__)
    parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
    icon_path = os.path.join(parent_directory, '.gitpics', 'rhf.ico')

    root = tk.Tk()
    root.title("FDS MISC/DEVC/BNDF Line Maker v0.1.0")
    root.geometry("400x200")
    root.iconbitmap(icon_path)
    
    main_frame = tk.Frame(root, padx=10, pady=10)
    main_frame.pack(padx=10, pady=10)

    tk.Label(main_frame, text="Уровень:", font=("Arial", 12)).grid(row=0, column=0, sticky='w', pady=5)
    level_entry = tk.Entry(main_frame, font=("Arial", 12))
    level_entry.grid(row=0, column=1, pady=5)
    entry1_ttp = Tooltip(level_entry, "Уровень этажа, на котором вы хотите измерить тепловой поток")

    rhf_var = tk.BooleanVar()
    Chk1 = tk.Checkbutton(main_frame, text="Добавить измеритель теплового потока", variable=rhf_var, font=("Arial", 10))
    Chk1.grid(row=1, columnspan=2, sticky='w')
    Chk1_ttp = Tooltip(Chk1, "Измеряется тепловой поток на всех твёрдых поверхностях")

    bwt_var = tk.BooleanVar()
    Chk2 = tk.Checkbutton(main_frame, text="Добавить измеритель температуры задней стороны", variable=bwt_var, font=("Arial", 10))
    Chk2.grid(row=2, columnspan=2, sticky='w')
    Chk2_ttp = Tooltip(Chk2, "Измеряется температура обратной стороны стен, площадок, перекрытий и пр.")

    wt_var = tk.BooleanVar()
    Chk3 = tk.Checkbutton(main_frame, text="Добавить измеритель температуры лицевой стороны", variable=wt_var, font=("Arial", 10))
    Chk3.grid(row=3, columnspan=2, sticky='w')
    Chk3_ttp = Tooltip(Chk3, "Измеряется температура лицевой стороны стен, площадок, перекрытий и пр.")

    Btn1 = tk.Button(main_frame, text="Добавить", command=on_submit, font=("Arial", 12))
    Btn1.grid(row=4, columnspan=2, pady=10)
    Btn1_ttp = Tooltip(Btn1, \
    "Введите значение отметки нужного этажа и нажмите эту кнопку, чтобы добавить плоскость измерения на этаж."
    "\nВведите значение отметки следующего этажа и нажмите кнопку... и так далее, чтобы добавить плоскости измерения на всех нужных вам этажах.")

    root.mainloop()
    