import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from trip import Ui_MainWindow  # Убедись, что файл trip.ui был скомпилирован в trip.py

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()  # Правильное имя класса интерфейса
        self.ui.setupUi(self)      # Настройка интерфейса

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())  # Или exec_() для совместимости со старыми версиями
