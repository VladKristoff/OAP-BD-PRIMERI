from PyQt5 import QtCore, QtWidgets


class Ui_pushButtonWrite(object):
    def setupUi(self, pushButtonWrite):
        pushButtonWrite.setObjectName("pushButtonWrite")
        pushButtonWrite.resize(818, 566)
        pushButtonWrite.setStyleSheet("background-color: rgb(29, 29, 29);")

        self.centralwidget = QtWidgets.QWidget(pushButtonWrite)
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.tableWidget = QtWidgets.QTableWidget(self.gridLayoutWidget)
        self.gridLayout.addWidget(self.tableWidget, 0, 0, 1, 1)

        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.pushButton_2 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.verticalLayout.addWidget(self.pushButton_2)
        self.verticalLayout.addWidget(self.pushButton)

        pushButtonWrite.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(pushButtonWrite)
        self.statusbar = QtWidgets.QStatusBar(pushButtonWrite)
        pushButtonWrite.setMenuBar(self.menubar)
        pushButtonWrite.setStatusBar(self.statusbar)
