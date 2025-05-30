from PyQt5.QtWidgets import (QMainWindow, QMessageBox, QInputDialog,
                             QTableWidgetItem)
from PyQt5.QtCore import Qt
from Builds_designer import Ui_MainWindow
from cls_builds import Builds
from cls_Itog import Itog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.builds_db = Builds()
        self.itog_db = Itog()

        self.setup_table()
        self.connect_buttons()
        self.current_table = None
    def setup_table(self):
        self.ui.tableWidget.setColumnCount(5)
        self.ui.tableWidget.setHorizontalHeaderLabels(["ID", "Тип строения", "Комнаты", "Метраж", "Цена"])
        self.ui.tableWidget.horizontalHeader().setStretchLastSection(True)

    def connect_buttons(self):
        self.ui.pushButton.clicked.connect(self.view_itog_table)
        self.ui.pushButton_2.clicked.connect(self.view_builds_table)
        self.ui.pushButton_3.clicked.connect(self.delete_record)
        self.ui.pushButton_4.clicked.connect(self.add_build_type)
        self.ui.pushButton_5.clicked.connect(self.add_itog_record)
        self.ui.pushButton_6.clicked.connect(self.clear_table)

    def view_builds_table(self):
        try:
            data = self.builds_db.view()
            self.current_table = "Builds"

            self.ui.tableWidget.setColumnCount(2)
            self.ui.tableWidget.setHorizontalHeaderLabels(["ID", "Тип строения"])
            self.ui.tableWidget.setRowCount(len(data))

            for row_idx, row in enumerate(data):
                for col_idx, value in enumerate(row):
                    item = QTableWidgetItem(str(value))
                    item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                    self.ui.tableWidget.setItem(row_idx, col_idx, item)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при загрузке данных: {str(e)}")

    def view_itog_table(self):
        try:
            data = self.itog_db.view_with_type()
            self.current_table = "Itog"

            self.ui.tableWidget.setColumnCount(5)
            self.ui.tableWidget.setHorizontalHeaderLabels(["ID", "Тип строения", "Комнаты", "Метраж", "Цена"])
            self.ui.tableWidget.setRowCount(len(data))

            for row_idx, row in enumerate(data):
                for col_idx, value in enumerate(row):
                    item = QTableWidgetItem(str(value))
                    item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                    self.ui.tableWidget.setItem(row_idx, col_idx, item)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при загрузке данных: {str(e)}")

    def add_build_type(self):
        text, ok = QInputDialog.getText(self, 'Добавить тип', 'Введите тип строения:')
        if ok and text:
            try:
                self.builds_db.insert(text)
                QMessageBox.information(self, "Успех", "Тип строения успешно добавлен")
                if self.current_table == "Builds":
                    self.view_builds_table()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка при добавлении: {str(e)}")

    def add_itog_record(self):
        builds = self.builds_db.view()
        if not builds:
            QMessageBox.warning(self, "Ошибка", "Сначала добавьте типы строений")
            return

        build_types = [build[1] for build in builds]
        build_type, ok = QInputDialog.getItem(
            self, 'Выберите тип', 'Тип строения:', build_types, 0, False)

        if not ok or not build_type:
            return

        build_id = next(build[0] for build in builds if build[1] == build_type)

        count_rooms, ok = QInputDialog.getInt(
            self, 'Количество комнат', 'Введите количество комнат:', 1, 1, 100, 1)
        if not ok:
            return

        footage, ok = QInputDialog.getDouble(
            self, 'Метраж', 'Введите метраж:', 1.0, 1.0, 10000.0, 2)
        if not ok:
            return

        price, ok = QInputDialog.getDouble(
            self, 'Цена', 'Введите цену:', 1.0, 1.0, 1000000000.0, 2)
        if not ok:
            return

        try:
            self.itog_db.insert(build_id, count_rooms, footage, price)
            QMessageBox.information(self, "Успех", "Запись успешно добавлена")
            if self.current_table == "Itog":
                self.view_itog_table()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при добавлении: {str(e)}")

    def delete_record(self):
        if not self.current_table:
            QMessageBox.warning(self, "Ошибка", "Сначала выберите таблицу")
            return

        selected_row = self.ui.tableWidget.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите запись для удаления")
            return

        id_item = self.ui.tableWidget.item(selected_row, 0)
        if not id_item:
            return

        record_id = int(id_item.text())

        reply = QMessageBox.question(
            self, 'Подтверждение',
            'Вы уверены, что хотите удалить запись?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            try:
                if self.current_table == "Builds":
                    self.itog_db.cur.execute("SELECT COUNT(*) FROM Itog WHERE Build=?", (record_id,))
                    count = self.itog_db.cur.fetchone()[0]
                    if count > 0:
                        QMessageBox.warning(
                            self, "Ошибка",
                            "Нельзя удалить тип строения, так как есть связанные записи")
                        return

                    self.builds_db.cur.execute("DELETE FROM Builds WHERE id_build=?", (record_id,))
                    self.builds_db.con.commit()

                elif self.current_table == "Itog":
                    self.itog_db.cur.execute("DELETE FROM Itog WHERE id=?", (record_id,))
                    self.itog_db.con.commit()

                QMessageBox.information(self, "Успех", "Запись успешно удалена")

                if self.current_table == "Builds":
                    self.view_builds_table()
                else:
                    self.view_itog_table()

            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка при удалении: {str(e)}")

    def clear_table(self):
        self.ui.tableWidget.clearContents()
        self.ui.tableWidget.setRowCount(0)
        self.current_table = None

    def closeEvent(self, event):
        self.builds_db.con.close()
        self.itog_db.con.close()
        event.accept()