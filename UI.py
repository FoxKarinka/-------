import tkinter as tk
from tkinter import messagebox
from library import Book, User, Library

library = Library()
library.load_books_from_json("books.json")
library.load_users_from_json("users.json")
library.load_history_from_json("history.json")

def save_all():
    library.save_books_to_json("books.json")
    library.save_users_to_json("users.json")
    library.save_history_to_json("history.json")
    messagebox.showinfo("Збережено", "Усі дані успішно збережено.")

def add_book_window():
    def submit():
        title = title_entry.get()
        author = author_entry.get()
        genre = genre_entry.get()
        year = year_entry.get()
        if title and author and genre and year.isdigit():
            book_id = max([b.book_id for b in library.books if b.book_id is not None] + [0]) + 1
            book = Book(title, author, genre, int(year), book_id=book_id)
            messagebox.showinfo("Успіх", library.add_book(book))
            save_all()
            window.destroy()
        else:
            messagebox.showerror("Помилка", "Будь ласка, введіть коректні дані.")

    window = tk.Toplevel(root)
    window.title("Додати книгу")

    tk.Label(window, text="Назва книги").pack()
    title_entry = tk.Entry(window)
    title_entry.pack()

    tk.Label(window, text="Автор").pack()
    author_entry = tk.Entry(window)
    author_entry.pack()

    tk.Label(window, text="Жанр").pack()
    genre_entry = tk.Entry(window)
    genre_entry.pack()

    tk.Label(window, text="Рік видання").pack()
    year_entry = tk.Entry(window)
    year_entry.pack()

    tk.Button(window, text="Додати", command=submit).pack()

def list_books():
    summaries = [book.get_summary() for book in library.books]
    messagebox.showinfo("Список книг", "\n\n".join(summaries))

def search_by_author_or_genre():
    def search():
        author = author_entry.get()
        genre = genre_entry.get()
        results = []
        for book in library.books:
            if (author and author.lower() in book.author.lower()) or (genre and genre.lower() in book.genre.lower()):
                results.append(book.get_summary())
        if results:
            messagebox.showinfo("Результати пошуку", "\n\n".join(results))
        else:
            messagebox.showerror("Нічого не знайдено", "Книги не знайдено.")
        window.destroy()

    window = tk.Toplevel(root)
    window.title("Пошук за автором або жанром")

    tk.Label(window, text="Автор").pack()
    author_entry = tk.Entry(window)
    author_entry.pack()

    tk.Label(window, text="Жанр").pack()
    genre_entry = tk.Entry(window)
    genre_entry.pack()

    tk.Button(window, text="Шукати", command=search).pack()

def register_user_window():
    def submit():
        username = username_entry.get()
        email = email_entry.get()
        if username and email:
            user = User(username, email)
            messagebox.showinfo("Успіх", library.register_user(user))
            save_all()
            window.destroy()
        else:
            messagebox.showerror("Помилка", "Введіть коректні дані.")

    window = tk.Toplevel(root)
    window.title("Реєстрація користувача")

    tk.Label(window, text="Ім’я користувача").pack()
    username_entry = tk.Entry(window)
    username_entry.pack()

    tk.Label(window, text="Email").pack()
    email_entry = tk.Entry(window)
    email_entry.pack()

    tk.Button(window, text="Зареєструвати", command=submit).pack()

def list_all_users():
    if not library.users:
        messagebox.showinfo("Користувачі", "Немає зареєстрованих користувачів.")
        return
    info = []
    for user in library.users:
        info.append(f"{user.username} ({user.email}) — {user.list_borrowed_books()}")
    messagebox.showinfo("Всі користувачі", "\n\n".join(info))

def users_who_borrowed_book():
    def search():
        title = title_entry.get()
        borrowers = []
        for user in library.users:
            for book in user.borrowed_books:
                if book.title.lower() == title.lower():
                    borrowers.append(user.username)
        if borrowers:
            messagebox.showinfo("Позичили книгу", "\n".join(borrowers))
        else:
            messagebox.showinfo("Ніхто не позичив", "Немає користувачів, які позичили цю книгу.")
        window.destroy()

    window = tk.Toplevel(root)
    window.title("Хто позичив книгу")

    tk.Label(window, text="Назва книги").pack()
    title_entry = tk.Entry(window)
    title_entry.pack()
    tk.Button(window, text="Показати", command=search).pack()

def issue_book_window():
    def issue():
        username = user_entry.get()
        title = title_entry.get()
        result = library.borrow_book_to_user(username, title)
        messagebox.showinfo("Результат", result)
        save_all()
        window.destroy()

    window = tk.Toplevel(root)
    window.title("Видати книгу")

    tk.Label(window, text="Ім’я користувача").pack()
    user_entry = tk.Entry(window)
    user_entry.pack()

    tk.Label(window, text="Назва книги").pack()
    title_entry = tk.Entry(window)
    title_entry.pack()

    tk.Button(window, text="Видати", command=issue).pack()

root = tk.Tk()
root.title("Система управління бібліотекою")

tk.Button(root, text="📚 Переглянути всі книги", width=30, command=list_books).pack(pady=5)
tk.Button(root, text="👥 Всі користувачі", width=30, command=list_all_users).pack(pady=5)
tk.Button(root, text="📘 Додати книгу", width=30, command=add_book_window).pack(pady=5)
tk.Button(root, text="🔍 Пошук за автором/жанром", width=30, command=search_by_author_or_genre).pack(pady=5)
tk.Button(root, text="👤 Реєстрація користувача", width=30, command=register_user_window).pack(pady=5)
tk.Button(root, text="📕 Виписати книгу", width=30, command=issue_book_window).pack(pady=5)
tk.Button(root, text="📖 Дізнатися чи книга в бібліотеці", width=30, command=users_who_borrowed_book).pack(pady=5)
tk.Button(root, text="💾 Зберегти зміни", width=30, command=save_all).pack(pady=5)

root.mainloop()