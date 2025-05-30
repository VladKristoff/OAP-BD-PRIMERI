import sys
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, \
    QSpinBox, QDoubleSpinBox, QDialogButtonBox, QMessageBox
from PyQt5 import QtCore, QtWidgets
import sqlite3
from main_window import Ui_pushButtonWrite

db_path = r'C:\Users\Студент.44-4\Desktop\OAP-DZ-BD-QT-DESIGNER-main\ShumovVlad.db'


class MyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_pushButtonWrite()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.load_products_data)
        self.ui.pushButton_2.clicked.connect(self.show_add_product_dialog)
        self.load_products_data()

    def load_products_data(self):
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT id, Product, Product_group, Price_purchase, Price_sale FROM products')
            rows = cursor.fetchall()
            conn.close()

            self.ui.tableWidget.setRowCount(0)
            self.ui.tableWidget.setRowCount(len(rows))

            for row_idx, row_data in enumerate(rows):
                for col_idx, value in enumerate(row_data):
                    item = QtWidgets.QTableWidgetItem(str(value))
                    self.ui.tableWidget.setItem(row_idx, col_idx, item)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить данные: {str(e)}")

    def show_add_product_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Добавить новый продукт")
        dialog.setFixedSize(400, 300)

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        product_edit = QLineEdit()
        group_edit = QSpinBox()
        price_purchase_edit = QDoubleSpinBox()
        price_purchase_edit.setMaximum(999999.99)
        price_sale_edit = QDoubleSpinBox()
        price_sale_edit.setMaximum(999999.99)

        form_layout.addRow("Название продукта:", product_edit)
        form_layout.addRow("Группа (ID):", group_edit)
        form_layout.addRow("Цена закупки:", price_purchase_edit)
        form_layout.addRow("Цена продажи:", price_sale_edit)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(lambda: self.add_product(
            dialog, product_edit.text(), group_edit.value(),
            price_purchase_edit.value(), price_sale_edit.value()
        ))
        button_box.rejected.connect(dialog.reject)

        layout.addLayout(form_layout)
        layout.addWidget(button_box)
        dialog.setLayout(layout)
        dialog.exec_()

    def add_product(self, dialog, product, product_group, price_purchase, price_sale):
        if not product:
            QMessageBox.warning(dialog, "Ошибка", "Введите название продукта")
            return

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO products VALUES (NULL, ?, ?, ?, ?)",
                (product, product_group, price_purchase, price_sale)
            )
            conn.commit()
            conn.close()

            QMessageBox.information(dialog, "Успех", "Продукт успешно добавлен")
            dialog.accept()
            self.load_products_data()

        except Exception as e:
            QMessageBox.critical(dialog, "Ошибка", f"Не удалось добавить продукт: {str(e)}")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())