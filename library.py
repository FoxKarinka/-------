import json
from datetime import datetime

class Book:
    def __init__(self, title, author, genre, published_year, book_id=None, available=True):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.genre = genre
        self.published_year = published_year
        self.available = available

    def get_summary(self):
        status = "Доступна" if self.available else "Недоступна"
        return f"«{self.title}» — {self.author}, {self.published_year} [{self.genre}] — {status}"


class User:
    def __init__(self, username, email, user_id=None):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.borrowed_books = []

    def borrow_book(self, book):
        self.borrowed_books.append(book)
        book.available = False
        return f"{self.username} позичив книгу «{book.title}»."

    def return_book(self, book):
        if book in self.borrowed_books:
            self.borrowed_books.remove(book)
            book.available = True
            return f"{self.username} повернув книгу «{book.title}»."
        else:
            return f"{self.username} не позичав книгу «{book.title}»."

    def list_borrowed_books(self):
        if not self.borrowed_books:
            return "немає позичених книг"
        return ", ".join([book.title for book in self.borrowed_books])


class Library:
    def __init__(self):
        self.books = []
        self.users = []
        self.history = []

    def borrow_book_to_user(self, username, book_title):
        user = next((u for u in self.users if u.username == username), None)
        book = next((b for b in self.books if b.title == book_title), None)

        if not user:
            return f"Користувача «{username}» не знайдено."
        if not book:
            return f"Книгу «{book_title}» не знайдено."
        if not book.available:
            return f"Книга «{book_title}» вже позичена."

        user.borrow_book(book)
        self.history.append({
            "action": "borrow",
            "username": user.username,
            "book_title": book.title,
            "timestamp": datetime.now().isoformat()
        })
        return f"Книга «{book.title}» видана користувачу «{user.username}»."

    def return_book_from_user(self, username, book_title):
        user = next((u for u in self.users if u.username == username), None)
        book = next((b for b in self.books if b.title == book_title), None)

        if not user:
            return f"Користувача «{username}» не знайдено."
        if not book:
            return f"Книгу «{book_title}» не знайдено."

        result = user.return_book(book)
        if "повернув" in result:
            self.history.append({
                "action": "return",
                "username": user.username,
                "book_title": book.title,
                "timestamp": datetime.now().isoformat()
            })
        return result

    def save_history_to_json(self, filename):
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(self.history, file, indent=4, ensure_ascii=False)

    def load_history_from_json(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                self.history = json.load(file)
        except FileNotFoundError:
            self.history = []

    def add_book(self, book):
        self.books.append(book)
        return f"Книга «{book.title}» додана до бібліотеки."

    def edit_book(self, old_title, new_book):
        for i, book in enumerate(self.books):
            if book.title == old_title:
                self.books[i] = new_book
                return f"Книгу «{old_title}» оновлено."
        return f"Книгу «{old_title}» не знайдено."

    def remove_book(self, title):
        for book in self.books:
            if book.title == title:
                self.books.remove(book)
                return f"Книгу «{title}» вилучено."
        return f"Книгу «{title}» не знайдено."

    def register_user(self, user):
        self.users.append(user)
        return f"Користувача «{user.username}» зареєстровано."

    def find_book_by_title(self, title):
        title = str(title).lower()
        for book in self.books:
            if book.title.lower() == title:
                return book
        return None

    def find_book_by_id(self, book_id):
        for book in self.books:
            if getattr(book, "book_id", None) == book_id:
                return book
        return None

    def list_all_books(self):
        if not self.books:
            return "У бібліотеці немає книг."
        return "\n".join([book.get_summary() for book in self.books])

    def save_books_to_json(self, filename):
        with open(filename, 'w', encoding='utf-8') as file:
            books_data = []
            for book in self.books:
                books_data.append({
                    "book_id": book.book_id,
                    "title": book.title,
                    "author": book.author,
                    "genre": book.genre,
                    "published_year": book.published_year,
                    "available": book.available
                })
            json.dump(books_data, file, indent=4, ensure_ascii=False)

    def load_books_from_json(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                books_data = json.load(file)
                for book_dict in books_data:
                    book = Book(
                        title=book_dict["title"],
                        author=book_dict["author"],
                        genre=book_dict["genre"],
                        published_year=book_dict["published_year"],
                        book_id=book_dict.get("book_id"),
                        available=book_dict.get("available", True)
                    )
                    self.add_book(book)
        except FileNotFoundError:
            pass

    def load_users_from_json(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                users_data = json.load(file)
                for user_dict in users_data:
                    user = User(
                        username=user_dict["name"],
                        email=user_dict["email"],
                        user_id=user_dict.get("user_id")
                    )
                    for book_id in user_dict.get("borrowed_books", []):
                        book = self.find_book_by_id(book_id)
                        if book:
                            user.borrow_book(book)
                    self.register_user(user)
        except FileNotFoundError:
            pass

    def save_users_to_json(self, filename):
        with open(filename, 'w', encoding='utf-8') as file:
            users_data = []
            for user in self.users:
                users_data.append({
                    "user_id": user.user_id,
                    "name": user.username,
                    "email": user.email,
                    "borrowed_books": [book.book_id for book in user.borrowed_books if book.book_id is not None]
                })
            json.dump(users_data, file, indent=4, ensure_ascii=False)