import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QMessageBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from ui_main_window import Ui_MainWindow

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


        self.conn = sqlite3.connect("bookshop.db")
        self.cursor = self.conn.cursor()


        self.ui.btn_show_books.clicked.connect(self.show_books)
        self.ui.btn_show_genres.clicked.connect(self.show_genres)
        self.ui.btn_add_book.clicked.connect(self.add_book)
        self.ui.btn_add_genre.clicked.connect(self.add_genre)
        self.ui.btn_delete_book.clicked.connect(self.delete_book)

    def show_books(self):
        self.cursor.execute("""
            SELECT book.id, book.name, genre.genre, book.price, book.count
            FROM book
            JOIN genre ON book.id_genre = genre.id_genre
        """)
        data = self.cursor.fetchall()
        headers = ["ID", "Название", "Жанр", "Цена", "Количество"]
        self.display_table(data, headers)

    def show_genres(self):
        self.cursor.execute("SELECT * FROM genre")
        data = self.cursor.fetchall()
        headers = ["ID жанра", "Жанр"]
        self.display_table(data, headers)

    def add_book(self):
        try:
            name = self.ui.input_book_name.text()
            id_genre = int(self.ui.input_book_genre_id.text())
            price = int(self.ui.input_book_price.text())
            count = int(self.ui.input_book_count.text())
            self.cursor.execute("INSERT INTO book (name, id_genre, price, count) VALUES (?, ?, ?, ?)",
                                (name, id_genre, price, count))
            self.conn.commit()
            self.show_books()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", str(e))

    def add_genre(self):
        try:
            id_genre = int(self.ui.input_genre_id.text())
            genre = self.ui.input_genre_name.text()
            self.cursor.execute("INSERT INTO genre (id_genre, genre) VALUES (?, ?)", (id_genre, genre))
            self.conn.commit()
            self.show_genres()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", str(e))

    def delete_book(self):
        try:

            index = self.ui.tableView.currentIndex()
            if not index.isValid():
                QMessageBox.warning(self, "Ошибка", "Выберите строку для удаления.")
                return
            row = index.row()
            model = self.ui.tableView.model()
            book_id = model.item(row, 0).text()
            self.cursor.execute("DELETE FROM book WHERE id = ?", (book_id,))
            self.conn.commit()
            self.show_books()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", str(e))

    def display_table(self, data, headers):
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(headers)
        for row in data:
            items = [QStandardItem(str(field)) for field in row]
            model.appendRow(items)
        self.ui.tableView.setModel(model)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
