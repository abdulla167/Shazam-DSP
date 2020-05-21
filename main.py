from ICA
import sys
from PyQt5 import QtWidgets
import os
import numpy as np
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem


class MyTable(QTableWidget):
    def __init__(self, r, c):
        super().__init__(r, c)

class ApplicationWindow(QtWidgets.QMainWindow):


    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_3.clicked.connect(lambda : self.load_song(1))
        self.ui.pushButton_4.clicked.connect(lambda :self.load_song(2))
        self.ui.pushButton_2.clicked.connect(self.mix)
        self.ui.pushButton.clicked.connect(self.match_hash_peaks)





def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()

    app.exec_()


if __name__ == "__main__":
    main()
