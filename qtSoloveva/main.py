import os
import sys
from PyQt5.QtWidgets import QApplication
from main_window import MainWindow

os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = "C:\\Users\\студент\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages\\PyQt5\\Qt5\\plugins"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())