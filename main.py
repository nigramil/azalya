import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

# Имя файла для сохранения данных
DATA_FILE = 'weather_data.json'

class WeatherDiary:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Diary")
        
        self.records = []  # список для хранения записей

        # --- Создаем интерфейс ---
        # Поле для даты
        tk.Label(root, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.date_entry = tk.Entry(root)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        # Поле для температуры
        tk.Label(root, text="Температура (°C):").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.temp_entry = tk.Entry(root)
        self.temp_entry.grid(row=1, column=1, padx=5, pady=5)

        # Поле для описания погоды
        tk.Label(root, text="Описание погоды:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.desc_entry = tk.Entry(root, width=50)
        self.desc_entry.grid(row=2, column=1, padx=5, pady=5)

        # Осадки (да/нет)
        tk.Label(root, text="Осадки:").grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.rain_var = tk.StringVar(value='Нет')
        tk.Radiobutton(root, text='Да', variable=self.rain_var, value='Да').grid(row=3, column=1, sticky='w')
        tk.Radiobutton(root, text='Нет', variable=self.rain_var, value='Нет').grid(row=3, column=1, sticky='e')

        # Кнопка "Добавить запись"
        self.add_button = tk.Button(root, text="Добавить запись", command=self.add_record)
        self.add_button.grid(row=4, column=0, columnspan=2, pady=10)

        # --- Фильтр ---
        # По дате
        tk.Label(root, text="Фильтр по дате (ГГГГ-ММ-ДД):").grid(row=5, column=0, padx=5, pady=5, sticky='w')
        self.filter_date_entry = tk.Entry(root)
        self.filter_date_entry.grid(row=5, column=1, padx=5, pady=5)
        self.filter_date_button = tk.Button(root, text="Показать за дату", command=self.filter_by_date)
        self.filter_date_button.grid(row=5, column=2, padx=5, pady=5)

        # По температуре
        tk.Label(root, text="Минимальная температура:").grid(row=6, column=0, padx=5, pady=5, sticky='w')
        self.filter_temp_entry = tk.Entry(root)
        self.filter_temp_entry.grid(row=6, column=1, padx=5, pady=5)
        self.filter_temp_button = tk.Button(root, text="Показать выше", command=self.filter_by_temp)
        self.filter_temp_button.grid(row=6, column=2, padx=5, pady=5)

        # Кнопка "Показать все"
        self.show_all_button = tk.Button(root, text="Показать все записи", command=self.load_records)
        self.show_all_button.grid(row=7, column=0, columnspan=3, pady=5)

        # Таблица для отображения записей
        self.tree = ttk.Treeview(root, columns=('Дата', 'Температура', 'Описание', 'Осадки'), show='headings')
        self.tree.heading('Дата', text='Дата')
        self.tree.heading('Температура', text='Температура')
        self.tree.heading('Описание', text='Описание')
        self.tree.heading('Осадки', text='Осадки')
        self.tree.grid(row=8, column=0, columnspan=3, padx=5, pady=5)

        # Загружаем существующие данные
        self.load_records()

    def add_record(self):
        date_str = self.date_entry.get()
        temp_str = self.temp_entry.get()
        desc = self.desc_entry.get().strip()
        rain = self.rain_var.get()

        # Проверка корректности ввода
        if not self.validate_date(date_str):
            messagebox.showerror("Ошибка", "Некорректный формат даты.")
            return
        try:
            temperature = float(temp_str)
        except ValueError:
            messagebox.showerror("Ошибка", "Температура должна быть числом.")
            return
        if not desc:
            messagebox.showerror("Ошибка", "Описание погоды не должно быть пустым.")
            return

        # Создаем запись
        record = {
            'date': date_str,
            'temperature': temperature,
            'description': desc,
            'rain': rain
        }
        self.records.append(record)
        self.save_records()
        self.display_records(self.records)

        # Очистка полей
        self.date_entry.delete(0, tk.END)
        self.temp_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.rain_var.set('Нет')

    def validate_date(self, date_text):
        # Проверка правильности формата даты
        try:
            datetime.strptime(date_text, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def load_records(self):
        # Загрузка данных из файла
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                self.records = json.load(f)
        self.display_records(self.records)

    def save_records(self):
        # Сохранение данных в файл
        with open(DATA_FILE, 'w') as f:
            json.dump(self.records, f, ensure_ascii=False, indent=2)

    def display_records(self, records):
        # Отображение записей в таблице
        self.tree.delete(*self.tree.get_children())
        for rec in records:
            self.tree.insert('', tk.END, values=(
                rec['date'],
                rec['temperature'],
                rec['description'],
                rec['rain']
            ))

    def filter_by_date(self):
        date_filter = self.filter_date_entry.get()
        if not self.validate_date(date_filter):
            messagebox.showerror("Ошибка", "Некорректный формат даты.")
            return
        filtered = [rec for rec in self.records if rec['date'] == date_filter]
        self.display_records(filtered)

    def filter_by_temp(self):
        temp_str = self.filter_temp_entry.get()
        try:
            min_temp = float(temp_str)
        except ValueError:
            messagebox.showerror("Ошибка", "Минимальная температура должна быть числом.")
            return
        filtered = [rec for rec in self.records if rec['temperature'] >= min_temp]
        self.display_records(filtered)

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherDiary(root)
    root.mainloop()
