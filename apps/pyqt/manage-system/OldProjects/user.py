from PyQt5.QtWidgets import QWidget, QMainWindow
# from PyQt5.QtCore import pyqtSlot, Qt

from user_ui import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setStyleSheet('background: purple')
        self.setupUi(self)

    def handle_visible(self):
        if not self.isVisible():
            self.show()

    def handle_close(self):
        self.close()
