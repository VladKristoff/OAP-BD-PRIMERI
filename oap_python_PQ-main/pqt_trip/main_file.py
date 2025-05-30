import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QMessageBox, QTableWidgetItem
)
from trip_333 import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Добавление значений в выпадающий список
        self.ui.comboBox.addItems(["Автобус", "Самолёт", "Поезд"])

        # Путь к базе по умолчанию
        self.db_path = r"C:\Users\sofia\PycharmProjects\pqt_trip\Trip.db3"
        self.connection = None

        self.setup_connections()
        self.load_data()

    def setup_connections(self):
        self.ui.pushButton_4.clicked.connect(self.choose_file)      # "Открыть файл"
        self.ui.pushButton_2.clicked.connect(self.add_row)          # "Добавить"
        self.ui.pushButton.clicked.connect(self.save_changes)       # "Сохранить"
        self.ui.pushButton_3.clicked.connect(self.delete_row)       # "Удалить"

    def connect_db(self):
        if self.connection:
            self.connection.close()
        self.connection = sqlite3.connect(self.db_path)

    def load_data(self):
        self.connect_db()
        cursor = self.connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS trip (departure TEXT, destination TEXT, price REAL, transport TEXT)")
        cursor.execute("SELECT * FROM trip")
        rows = cursor.fetchall()

        self.ui.tableWidget.setRowCount(0)
        self.ui.tableWidget.setColumnCount(4)
        self.ui.tableWidget.setHorizontalHeaderLabels(["Пункт отправки", "Пункт назначения", "Цена", "Транспорт"])
        for row_data in rows:
            row = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(row)
            for col, value in enumerate(row_data):
                self.ui.tableWidget.setItem(row, col, QTableWidgetItem(str(value)))

    def add_row(self):
        departure = self.ui.textEdit.toPlainText().strip()
        destination = self.ui.textEdit_2.toPlainText().strip()
        price = self.ui.textEdit_3.toPlainText().strip()
        transport = self.ui.comboBox.currentText().strip()

        if not departure or not destination or not price or not transport:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля.")
            return

        try:
            float(price)  # Проверка, что цена — число
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Цена должна быть числом.")
            return

        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO trip (departure, destination, price, transport) VALUES (?, ?, ?, ?)",
                       (departure, destination, price, transport))
        self.connection.commit()
        self.load_data()

        # Очистка полей после добавления
        self.ui.textEdit.clear()
        self.ui.textEdit_2.clear()
        self.ui.textEdit_3.clear()
        self.ui.comboBox.setCurrentIndex(0)

    def delete_row(self):
        selected = self.ui.tableWidget.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите строку для удаления.")
            return

        try:
            item_departure = self.ui.tableWidget.item(selected, 0).text()
            item_destination = self.ui.tableWidget.item(selected, 1).text()
            item_price = self.ui.tableWidget.item(selected, 2).text()
            item_transport = self.ui.tableWidget.item(selected, 3).text()
        except AttributeError:
            QMessageBox.warning(self, "Ошибка", "Невозможно получить данные строки.")
            return

        cursor = self.connection.cursor()
        cursor.execute(
            "DELETE FROM trip WHERE rowid IN (SELECT rowid FROM trip WHERE departure=? AND destination=? AND price=? AND transport=? LIMIT 1)",
            (item_departure, item_destination, item_price, item_transport)
        )
        self.connection.commit()
        self.load_data()

    def save_changes(self):
        if self.connection:
            self.connection.commit()
        QMessageBox.information(self, "Сохранено", "Изменения сохранены.")

    def choose_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Выбрать файл базы данных", "", "SQLite DB (*.db3);;Все файлы (*)"
        )
        if file_name:
            self.db_path = file_name
            self.load_data()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
