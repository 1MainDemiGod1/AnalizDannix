import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import pandas as pd

class DataAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Анализатор данных")
        self.df = None

        # Кнопка загрузки файла
        self.load_button = tk.Button(root, text="Загрузить файл", command=self.load_file)
        self.load_button.pack(pady=10)

        # Таблица для отображения данных
        self.tree = ttk.Treeview(root)
        self.tree.pack(pady=10)

        # Поле для фильтрации
        self.filter_label = tk.Label(root, text="Фильтр по значению:")
        self.filter_label.pack(pady=5)

        self.filter_entry = tk.Entry(root)
        self.filter_entry.pack(pady=5)

        # Кнопка фильтрации
        self.filter_button = tk.Button(root, text="Применить фильтр", command=self.filter_data)
        self.filter_button.pack(pady=5)

        # Кнопки анализа данных
        self.mean_button = tk.Button(root, text="Среднее значение", command=self.calculate_mean)
        self.mean_button.pack(pady=5)

        self.min_button = tk.Button(root, text="Минимум", command=self.calculate_min)
        self.min_button.pack(pady=5)

        self.max_button = tk.Button(root, text="Максимум", command=self.calculate_max)
        self.max_button.pack(pady=5)

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.df = pd.read_csv(file_path)
            self.display_data()

    def display_data(self):
        # Очистить таблицу
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = list(self.df.columns)
        for column in self.tree["columns"]:
            self.tree.heading(column, text=column)

        for index, row in self.df.iterrows():
            self.tree.insert("", "end", values=list(row))

    def filter_data(self):
        filter_value = self.filter_entry.get()
        if self.df is not None:
            filtered_df = self.df[self.df.apply(lambda row: row.astype(str).str.contains(filter_value).any(), axis=1)]
            self.display_filtered_data(filtered_df)
        else:
            messagebox.showerror("Ошибка", "Сначала загрузите файл CSV")

    def display_filtered_data(self, filtered_df):
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = list(filtered_df.columns)
        for column in self.tree["columns"]:
            self.tree.heading(column, text=column)

        for index, row in filtered_df.iterrows():
            self.tree.insert("", "end", values=list(row))

    def calculate_mean(self):
        self.perform_operation(pd.Series.mean, "Среднее значение")

    def calculate_min(self):
        self.perform_operation(pd.Series.min, "Минимум")

    def calculate_max(self):
        self.perform_operation(pd.Series.max, "Максимум")

    def perform_operation(self, operation, title):
        if self.df is not None:
            column = self.tree["columns"][0]  # Используем первый столбец для примера
            mean_value = operation(self.df[column])
            messagebox.showinfo(title, f"{title} для '{column}': {mean_value}")
        else:
            messagebox.showerror("Ошибка", "Сначала загрузите файл CSV")

if __name__ == "__main__":
    root = tk.Tk()
    app = DataAnalyzerApp(root)
    root.mainloop()