import pandas as pd
from tkinter import *
from tkinter import filedialog, messagebox, simpledialog  
from tkinter import ttk

class DataAnalysisApp:
    def __init__(self, master):
        self.master = master
        master.title("Data Analysis App")
        master.geometry("800x600")
        master.configure(bg="#f0f0f0")

        style = ttk.Style()
        style.theme_use('clam')  # Установка стиля

        # Настройка кнопок
        style.configure("TButton", padding=6, relief="flat", background="#007bff", foreground="white",
                        font=('Arial', 10, 'bold'))
        style.map("TButton", background=[('active', '#0056b3')])

        # Настройка таблицы
        style.configure("Treeview", background="#ffffff", foreground="#000000",
                        rowheight=25, font=('Arial', 10))

        style.configure("Treeview.Heading", background="#007bff", foreground="white", font=('Arial', 12, 'bold'))
        style.map("Treeview.Heading", background=[('active', '#0056b3')])

        # Инициализация переменных
        self.data = None

        # Кнопка загрузки файла
        self.load_button = Button(master, text="Загрузить файл", command=self.load_file)
        self.load_button.pack()

        # Таблица для отображения данных
        self.treeview = ttk.Treeview(master)
        self.treeview.pack(expand=True, fill='both')

        # Поле для ввода значения для фильтрации
        self.filter_value = Entry(master)
        self.filter_value.pack()

        # Кнопки для анализа данных
        self.avg_button = Button(master, text="Среднее", command=self.calculate_avg)
        self.avg_button.pack()

        self.min_button = Button(master, text="Минимум", command=self.calculate_min)
        self.min_button.pack()

        self.max_button = Button(master, text="Максимум", command=self.calculate_max)
        self.max_button.pack()

        self.filter_button = Button(master, text="Фильтрация", command=self.filter_data)
        self.filter_button.pack()

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                self.data = pd.read_csv(file_path)
                self.show_data()
            except Exception as e:
                messagebox.showerror("Error", f"Ошибка при загрузке файла: {e}")

    def show_data(self):
        """Отображает данные в таблице Treeview."""
        self.treeview.delete(*self.treeview.get_children())
        columns = list(self.data.columns)
        self.treeview["columns"] = columns
        self.treeview["show"] = "headings"

        for col in columns:
            self.treeview.heading(col, text=col)
            self.treeview.column(col, anchor="center")

        for index, row in self.data.iterrows():
            self.treeview.insert("", "end", values=list(row))

    def calculate_avg(self):
        column_name = self.get_column_name()
        if column_name:
            avg_value = self.data[column_name].mean()
            messagebox.showinfo("Среднее значение", f"Среднее значение в '{column_name}': {avg_value}")
        else:
            messagebox.showinfo("Невозможно найти не числовое значение")

    def calculate_min(self):
        column_name = self.get_column_name()
        if column_name:
            min_value = self.data[column_name].min()
            messagebox.showinfo("Минимальное значение", f"Минимальное значение в '{column_name}': {min_value}")

    def calculate_max(self):
        column_name = self.get_column_name()
        if column_name:
            max_value = self.data[column_name].max()
            messagebox.showinfo("Максимальное значение", f"Максимальное значение в '{column_name}': {max_value}")
        

    def filter_data(self):
        filter_value = self.filter_value.get()
        filtered_data = self.data[self.data.apply(lambda row: row.astype(str).str.contains(filter_value).any(), axis=1)]
        if not filtered_data.empty:
            self.data = filtered_data
            self.show_data()
        else:
            messagebox.showinfo("Фильтрация", "Нет результатов для фильтрации.")

    def get_column_name(self):
        """Запрашивает у пользователя имя столбца для анализа."""
        column_name = simpledialog.askstring("Введите имя столбца", "Какой столбец вы хотите проанализировать?")
        if column_name in self.data.columns:
            return column_name
        else:
            messagebox.showerror("Ошибка", f"Столбец '{column_name}' не найден в данных.")
            return None

if __name__ == "__main__":
    root = Tk()
    app = DataAnalysisApp(root)
    root.mainloop()
