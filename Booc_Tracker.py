import tkinter as tk
from tkinter import ttk, messagebox
import json
import os


class BookTracker:
    """Класс для управления трекером прочитанных книг"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("📚 Book Tracker")
        self.root.geometry("950x750")
        self.root.minsize(850, 700)
        self.root.configure(bg="#f0f0f0")
        
        self.books = []
        self.filename = "books.json"
        
        # Жанры по умолчанию
        self.genres = ["Фантастика", "Детектив", "Роман", "Фэнтези", 
                       "Научная литература", "Биография", "Ужасы", "Другое"]
        
        self.create_widgets()
        self.load_books()
    
    def create_widgets(self):
        """Создание элементов интерфейса"""
        
        # Заголовок
        title_label = tk.Label(
            self.root,
            text="📚 Book Tracker",
            font=("Arial", 20, "bold"),
            bg="#f0f0f0",
            fg="#1a1a2e"
        )
        title_label.pack(pady=15)
        
        # Фрейм для добавления книги
        add_frame = tk.LabelFrame(
            self.root,
            text="Добавить новую книгу",
            font=("Arial", 12, "bold"),
            bg="#ffffff",
            padx=15,
            pady=15
        )
        add_frame.pack(fill="x", padx=20, pady=10)
        
        # Название книги
        tk.Label(add_frame, text="Название книги:", bg="#ffffff", 
                font=("Arial", 10)).grid(row=0, column=0, sticky="e", pady=5)
        self.entry_title = tk.Entry(add_frame, width=30, font=("Arial", 10))
        self.entry_title.grid(row=0, column=1, padx=10, pady=5)
        self.create_tooltip(self.entry_title, "Введите название книги")
        
        # Автор
        tk.Label(add_frame, text="Автор:", bg="#ffffff", 
                font=("Arial", 10)).grid(row=0, column=2, sticky="e", pady=5)
        self.entry_author = tk.Entry(add_frame, width=20, font=("Arial", 10))
        self.entry_author.grid(row=0, column=3, padx=10, pady=5)
        self.create_tooltip(self.entry_author, "Введите имя автора")
        
        # Жанр
        tk.Label(add_frame, text="Жанр:", bg="#ffffff", 
                font=("Arial", 10)).grid(row=1, column=0, sticky="e", pady=5)
        self.combo_genre = ttk.Combobox(add_frame, width=25, font=("Arial", 10), 
                                        values=self.genres, state="readonly")
        self.combo_genre.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.combo_genre.set("Выберите жанр")
        self.create_tooltip(self.combo_genre, "Выберите жанр книги")
        
        # Количество страниц
        tk.Label(add_frame, text="Количество страниц:", bg="#ffffff", 
                font=("Arial", 10)).grid(row=1, column=2, sticky="e", pady=5)
        self.entry_pages = tk.Entry(add_frame, width=15, font=("Arial", 10))
        self.entry_pages.grid(row=1, column=3, padx=10, pady=5, sticky="w")
        self.create_tooltip(self.entry_pages, "Введите количество страниц")
        
        # Кнопка добавления
        btn_add = tk.Button(
            add_frame,
            text="➕ Добавить книгу",
            command=self.add_book,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 11, "bold"),
            width=20,
            height=2
        )
        btn_add.grid(row=2, column=0, columnspan=4, pady=10)
        self.create_tooltip(btn_add, "Добавить книгу в список")
        
        # Фрейм для фильтрации и статистики
        filter_frame = tk.LabelFrame(
            self.root,
            text="Фильтрация и статистика",
            font=("Arial", 12, "bold"),
            bg="#ffffff",
            padx=15,
            pady=15
        )
        filter_frame.pack(fill="x", padx=20, pady=10)
        
        # Фильтр по жанру
        tk.Label(filter_frame, text="Жанр:", bg="#ffffff", 
                font=("Arial", 10)).grid(row=0, column=0, padx=5)
        self.filter_genre = ttk.Combobox(filter_frame, width=20, font=("Arial", 10),
                                         values=["Все"] + self.genres, state="readonly")
        self.filter_genre.grid(row=0, column=1, padx=5)
        self.filter_genre.set("Все")
        self.create_tooltip(self.filter_genre, "Фильтр по жанру")
        
        # Фильтр по страницам
        tk.Label(filter_frame, text="Страниц больше:", bg="#ffffff", 
                font=("Arial", 10)).grid(row=0, column=2, padx=5)
        self.filter_pages = tk.Entry(filter_frame, width=10, font=("Arial", 10))
        self.filter_pages.grid(row=0, column=3, padx=5)
        self.filter_pages.insert(0, "0")
        self.create_tooltip(self.filter_pages, "Фильтр по количеству страниц")
        
        # Кнопки фильтрации
        btn_filter = tk.Button(
            filter_frame,
            text="🔍 Применить",
            command=self.apply_filter,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10, "bold"),
            width=12
        )
        btn_filter.grid(row=0, column=4, padx=10)
        self.create_tooltip(btn_filter, "Применить фильтры")
        
        btn_reset = tk.Button(
            filter_frame,
            text="🔄 Сбросить",
            command=self.reset_filter,
            bg="#FF9800",
            fg="white",
            font=("Arial", 10, "bold"),
            width=12
        )
        btn_reset.grid(row=0, column=5, padx=10)
        self.create_tooltip(btn_reset, "Сбросить все фильтры")
        
        # Статистика
        self.label_total = tk.Label(
            filter_frame,
            text="📖 Всего страниц: 0",
            font=("Arial", 14, "bold"),
            bg="#e8f5e9",
            fg="#2E7D32",
            padx=20,
            pady=10
        )
        self.label_total.grid(row=1, column=0, columnspan=6, pady=15, sticky="ew")
        
        # Таблица книг (Treeview)
        table_frame = tk.Frame(self.root, bg="#ffffff")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        columns = ("title", "author", "genre", "pages")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
        
        # Настройка заголовков
        self.tree.heading("title", text="Название")
        self.tree.heading("author", text="Автор")
        self.tree.heading("genre", text="Жанр")
        self.tree.heading("pages", text="Страниц")
        
        # Настройка ширины колонок
        self.tree.column("title", width=300, minwidth=200)
        self.tree.column("author", width=150, minwidth=100)
        self.tree.column("genre", width=120, minwidth=100)
        self.tree.column("pages", width=80, minwidth=60)
        
        # Полоса прокрутки
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Кнопки управления
        btn_frame = tk.Frame(self.root, bg="#f0f0f0")
        btn_frame.pack(pady=10)
        
        btn_delete = tk.Button(
            btn_frame,
            text="🗑️ Удалить выбранную",
            command=self.delete_book,
            bg="#f44336",
            fg="white",
            font=("Arial", 10, "bold"),
            width=18,
            height=2
        )
        btn_delete.pack(side="left", padx=5)
        self.create_tooltip(btn_delete, "Удалить выбранную книгу")
        
        btn_save = tk.Button(
            btn_frame,
            text="💾 Сохранить",
            command=self.save_books,
            bg="#9C27B0",
            fg="white",
            font=("Arial", 10, "bold"),
            width=18,
            height=2
        )
        btn_save.pack(side="left", padx=5)
        self.create_tooltip(btn_save, "Сохранить данные в JSON")
        
        btn_export = tk.Button(
            btn_frame,
            text="📊 Экспорт отчёта",
            command=self.export_report,
            bg="#00BCD4",
            fg="white",
            font=("Arial", 10, "bold"),
            width=18,
            height=2
        )
        btn_export.pack(side="left", padx=5)
        self.create_tooltip(btn_export, "Экспортировать отчёт в текстовый файл")
        
        # Статус бар
        self.status_label = tk.Label(
            self.root,
            text=f"Всего книг: 0",
            font=("Arial", 10),
            bg="#1a1a2e",
            fg="white",
            pady=5
        )
        self.status_label.pack(fill="x", side="bottom")
    
    def create_tooltip(self, widget, text):
        """Создание подсказки для виджета"""
        tooltip = tk.Toplevel(widget)
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry("+0+0")
        tooltip.withdraw()
        
        label = tk.Label(
            tooltip,
            text=text,
            background="#ffffe0",
            relief="solid",
            borderwidth=1,
            font=("Arial", 9)
        )
        label.pack()
        
        def show_tooltip(event):
            tooltip.deiconify()
            x = widget.winfo_rootx() + 20
            y = widget.winfo_rooty() + widget.winfo_height() + 5
            tooltip.wm_geometry(f"+{x}+{y}")
        
        def hide_tooltip(event):
            tooltip.withdraw()
        
        widget.bind("<Enter>", show_tooltip)
        widget.bind("<Leave>", hide_tooltip)
    
    def validate_title(self, title):
        """Проверка названия книги"""
        if not title.strip():
            messagebox.showerror("Ошибка", "Введите название книги!")
            return False
        return True
    
    def validate_author(self, author):
        """Проверка автора"""
        if not author.strip():
            messagebox.showerror("Ошибка", "Введите имя автора!")
            return False
        return True
    
    def validate_genre(self, genre):
        """Проверка жанра"""
        if not genre or genre == "Выберите жанр":
            messagebox.showerror("Ошибка", "Выберите жанр!")
            return False
        return True
    
    def validate_pages(self, pages):
        """Проверка количества страниц (должно быть числом)"""
        try:
            value = int(pages)
            if value <= 0:
                messagebox.showerror("Ошибка", "Количество страниц должно быть положительным числом!")
                return False
            return True
        except ValueError:
            messagebox.showerror("Ошибка", "Количество страниц должно быть числом!")
            return False
    
    def add_book(self):
        """Добавление новой книги"""
        
        title = self.entry_title.get().strip()
        author = self.entry_author.get().strip()
        genre = self.combo_genre.get()
        pages = self.entry_pages.get().strip()
        
        # Валидация названия
        if not self.validate_title(title):
            return
        
        # Валидация автора
        if not self.validate_author(author):
            return
        
        # Валидация жанра
        if not self.validate_genre(genre):
            return
        
        # Валидация страниц
        if not self.validate_pages(pages):
            return
        
        # Создание записи
        book = {
            "title": title,
            "author": author,
            "genre": genre,
            "pages": int(pages)
        }
        
        self.books.append(book)
        self.update_table()
        self.save_books()
        self.calculate_total()
        
        # Очистка полей
        self.entry_title.delete(0, tk.END)
        self.entry_author.delete(0, tk.END)
        self.combo_genre.set("Выберите жанр")
        self.entry_pages.delete(0, tk.END)
        
        messagebox.showinfo("Успех", f"Книга '{title}' добавлена!")
    
    def delete_book(self):
        """Удаление выбранной книги"""
        
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите книгу для удаления!")
            return
        
        index = self.tree.index(selected[0])
        book = self.books[index]
        confirm = messagebox.askyesno("Подтверждение", 
                                      f"Удалить книгу '{book['title']}'?")
        
        if confirm:
            self.books.pop(index)
            self.update_table()
            self.save_books()
            self.calculate_total()
            messagebox.showinfo("Успех", "Книга удалена!")
    
    def apply_filter(self):
        """Применение фильтрации"""
        
        genre_filter = self.filter_genre.get()
        pages_filter = self.filter_pages.get().strip()
        
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        filtered = []
        min_pages = 0
        
        # Парсинг фильтра по страницам
        if pages_filter and pages_filter != "0":
            try:
                min_pages = int(pages_filter)
            except ValueError:
                messagebox.showerror("Ошибка", "Фильтр страниц должен быть числом!")
                return
        
        # Фильтрация
        for book in self.books:
            # Фильтр по жанру
            if genre_filter and genre_filter != "Все":
                if book["genre"] != genre_filter:
                    continue
            
            # Фильтр по страницам
            if min_pages > 0:
                if book["pages"] < min_pages:
                    continue
            
            filtered.append(book)
        
        # Вывод отфильтрованных
        for book in filtered:
            self.tree.insert("", "end", values=(
                book["title"],
                book["author"],
                book["genre"],
                book["pages"]
            ))
        
        # Подсчёт страниц
        total = sum(b["pages"] for b in filtered)
        self.label_total.config(text=f"📖 Всего страниц: {total}")
        self.status_label.config(text=f"Показано: {len(filtered)} из {len(self.books)}")
    
    def reset_filter(self):
        """Сброс фильтров"""
        
        self.filter_genre.set("Все")
        self.filter_pages.delete(0, tk.END)
        self.filter_pages.insert(0, "0")
        
        self.update_table()
    
    def calculate_total(self):
        """Подсчёт общего количества страниц"""
        
        total = sum(b["pages"] for b in self.books)
        self.label_total.config(text=f"📖 Всего страниц: {total}")
    
    def update_table(self):
        """Обновление таблицы книг"""
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for book in self.books:
            self.tree.insert("", "end", values=(
                book["title"],
                book["author"],
                book["genre"],
                book["pages"]
            ))
        
        self.calculate_total()
        self.status_label.config(text=f"Всего книг: {len(self.books)}")
    
    def save_books(self):
        """Сохранение книг в JSON"""
        
        try:
            with open(self.filename, "w", encoding="utf-8") as file:
                json.dump(self.books, file, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить: {e}")
    
    def load_books(self):
        """Загрузка книг из JSON"""
        
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as file:
                    self.books = json.load(file)
                self.update_table()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить: {e}")
                self.books = []
    
    def export_report(self):
        """Экспорт отчёта в текстовый файл"""
        
        if not self.books:
            messagebox.showwarning("Внимание", "Нет книг для экспорта!")
            return
        
        try:
            with open("book_report.txt", "w", encoding="utf-8") as file:
                file.write("=" * 70 + "\n")
                file.write("📚 BOOK TRACKER — ОТЧЁТ ПО ПРОЧИТАННЫМ КНИГАМ\n")
                file.write("=" * 70 + "\n\n")
                
                total = sum(b["pages"] for b in self.books)
                avg_pages = total // len(self.books) if self.books else 0
                
                file.write(f"Всего книг: {len(self.books)}\n")
                file.write(f"Общее количество страниц: {total}\n")
                file.write(f"Среднее количество страниц: {avg_pages}\n\n")
                file.write("-" * 70 + "\n\n")
                
                # Группировка по жанрам
                genres = {}
                for book in self.books:
                    genre = book["genre"]
                    if genre not in genres:
                        genres[genre] = {"count": 0, "pages": 0}
                    genres[genre]["count"] += 1
                    genres[genre]["pages"] += book["pages"]
                
                file.write("📊 ПО ЖАНРАМ:\n\n")
                for genre, data in sorted(genres.items(), key=lambda x: x[1]["count"], reverse=True):
                    file.write(f"  {genre}: {data['count']} книг, {data['pages']} страниц\n")
                
                file.write("\n" + "-" * 70 + "\n\n")
                file.write("📋 ВСЕ КНИГИ:\n\n")
                
                for book in self.books:
                    file.write(f"  📖 {book['title']}\n")
                    file.write(f"     Автор: {book['author']} | Жанр: {book['genre']} | "
                              f"Страниц: {book['pages']}\n\n")
                
                file.write("=" * 70 + "\n")
            
            messagebox.showinfo("Успех", "Отчёт экспортирован в book_report.txt!")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось экспортировать: {e}")


# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = BookTracker(root)
    root.mainloop()