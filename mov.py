import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# Основное окно
root = tk.Tk()
root.title("Моя кинотека")

# Поля для ввода данных
frame = ttk.Frame(root, padding="10")
frame.pack()

ttk.Label(frame, text="Название:").grid(row=0, column=0, sticky='w')
name_entry = ttk.Entry(frame)
name_entry.grid(row=0, column=1)

ttk.Label(frame, text="Жанр:").grid(row=1, column=0, sticky='w')
genre_entry = ttk.Entry(frame)
genre_entry.grid(row=1, column=1)

ttk.Label(frame, text="Год выпуска:").grid(row=2, column=0, sticky='w')
year_entry = ttk.Entry(frame)
year_entry.grid(row=2, column=1)

ttk.Label(frame, text="Рейтинг:").grid(row=3, column=0, sticky='w')
rating_entry = ttk.Entry(frame)
rating_entry.grid(row=3, column=1)

# Таблица для отображения фильмов
columns = ("Название", "Жанр", "Год", "Рейтинг")
tree = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col)
tree.pack()

# Функции для работы с данными
movies = []

def load_data():
    global movies
    if os.path.exists("movies.json"):
        with open("movies.json", "r", encoding="utf-8") as f:
            movies = json.load(f)
        reload_table()

def save_data():
    with open("movies.json", "w", encoding="utf-8") as f:
        json.dump(movies, f, ensure_ascii=False, indent=4)

def reload_table():
    for row in tree.get_children():
        tree.delete(row)
    for movie in movies:
        tree.insert('', 'end', values=(movie['name'], movie['genre'], movie['year'], movie['rating']))

def add_movie():
    name = name_entry.get().strip()
    genre = genre_entry.get().strip()
    year = year_entry.get().strip()
    rating = rating_entry.get().strip()

    # Проверка корректности
    if not name or not genre or not year or not rating:
        messagebox.showerror("Ошибка", "Все поля должны быть заполнены.")
        return
    if not year.isdigit():
        messagebox.showerror("Ошибка", "Год должен быть числом.")
        return
    try:
        rating_value = float(rating)
        if not (0 <= rating_value <= 10):
            raise ValueError
    except ValueError:
        messagebox.showerror("Ошибка", "Рейтинг должен быть числом от 0 до 10.")
        return

    movie = {
        "name": name,
        "genre": genre,
        "year": int(year),
        "rating": rating_value
    }
    movies.append(movie)
    save_data()
    reload_table()

    # Очистка полей
    name_entry.delete(0, tk.END)
    genre_entry.delete(0, tk.END)
    year_entry.delete(0, tk.END)
    rating_entry.delete(0, tk.END)

# Кнопка добавления
add_button = ttk.Button(frame, text="Добавить фильм", command=add_movie)
add_button.grid(row=4, column=0, columnspan=2, pady=10)

# Загрузка данных при старте
load_data()

# --- Фильтрация ---
filter_frame = ttk.Frame(root, padding="10")
filter_frame.pack()

ttk.Label(filter_frame, text="Фильтр по жанру:").grid(row=0, column=0)
genre_filter_var = tk.StringVar()
genre_filter_entry = ttk.Entry(filter_frame, textvariable=genre_filter_var)
genre_filter_entry.grid(row=0, column=1)

ttk.Label(filter_frame, text="по году:").grid(row=0, column=2)
year_filter_var = tk.StringVar()
year_filter_entry = ttk.Entry(filter_frame, textvariable=year_filter_var)
year_filter_entry.grid(row=0, column=3)

def apply_filters():
    genre_filter = genre_filter_var.get().strip().lower()
    year_filter = year_filter_var.get().strip()
    filtered = []

    for movie in movies:
        if genre_filter and genre_filter not in movie['genre'].lower():
            continue
        if year_filter:
            if not year_filter.isdigit() or int(year_filter) != movie['year']:
                continue
        filtered.append(movie)

    # Обновляем таблицу
    for row in tree.get_children():
        tree.delete(row)
    for movie in filtered:
        tree.insert('', 'end', values=(movie['name'], movie['genre'], movie['year'], movie['rating']))

filter_button = ttk.Button(filter_frame, text="Применить фильтр", command=apply_filters)
filter_button.grid(row=0, column=4, padx=5)

root.mainloop()
