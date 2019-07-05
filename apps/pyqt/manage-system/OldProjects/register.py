from PyQt5.QtWidgets import QWidget, QLineEdit
from PyQt5.QtCore import pyqtSlot, Qt

from register_ui import Ui_Form


class Register(QWidget, Ui_Form):
    def __init__(self):
        super(Register, self).__init__()
        self.setupUi(self)

        self.lineEdit_2.setContextMenuPolicy(Qt.NoContextMenu)
        self.lineEdit_3.setContextMenuPolicy(Qt.NoContextMenu)
        self.lineEdit_2.setEchoMode(QLineEdit.Password)
        self.lineEdit_3.setEchoMode(QLineEdit.Password)

        self.lineEdit_1.setToolTip("账号不许超过16位")
        self.lineEdit_2.setToolTip("密码不许超过26位")

    @pyqtSlot()
    def on_changeButton_clicked(self):
        acount = self.lineEdit_1.text()
        passwd = self.lineEdit_2.text()
        print("Your: ", acount, passwd, ", ready for change!")