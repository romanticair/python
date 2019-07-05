from PyQt5.QtCore import pyqtSlot, Qt, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QLineEdit, QFormLayout

from init_ui import Ui_MainWindow
from register import Register


class Init(QMainWindow, Ui_MainWindow):
    close_signal = pyqtSignal()

    def __init__(self, parent=None):
        super(Init, self).__init__(parent)
        self.setupUi(self)

        self.lineEdit_2.setContextMenuPolicy(Qt.NoContextMenu)
        self.lineEdit_2.setEchoMode(QLineEdit.Password)
        self.formLayout = QFormLayout()  # The register's widget

    @pyqtSlot()
    def on_loginButton_clicked(self):
        acount = self.lineEdit_1.text()
        passwd = self.lineEdit_2.text()
        print(acount, passwd)
        QMessageBox.about(self, 'Login', "Waiting to achieve this function")

    @pyqtSlot()
    def on_changePasswordButton_clicked(self):
        register = Register()
        self.formLayout.addWidget(register)
        register.show()

    def closeEvent(self, event):
        self.close_signal.emit()
        self.close()



