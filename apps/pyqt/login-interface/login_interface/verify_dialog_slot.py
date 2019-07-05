import sys
import hashlib
import json
from PyQt5.QtWidgets import QDialog, QMessageBox, QLineEdit
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QTimer

from verify_dialog import Ui_Dialog


class VerifyDialog(QDialog, Ui_Dialog):
    """
    Login dialog.

    Separate user login window's interface and logic.
    """

    ok_signal = pyqtSignal(bool)

    def __init__(self):
        super(VerifyDialog, self).__init__()
        self.setupUi(self)
        self.try_times = 0
        self.password_le.setEchoMode(QLineEdit.Password)

    @pyqtSlot()
    def on_login_pb_clicked(self):
        self.check_data()
        if self.try_times >= 3:
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.close_all)
            self.timer.start(2000)
            reply = QMessageBox.critical(self, 'Fail', '账号或密码错误！', QMessageBox.Abort)
            if reply:
                sys.exit()

    @pyqtSlot()
    def on_quit_pb_clicked(self):
        sys.exit()

    def check_data(self):
        """
        Verify id and password.

        Get user's input, encrypting them, and contrast them with
        the model of users.json, tell the true or not.
        """
        id = self.acount_le.text()
        password = self.password_le.text()

        md5_id = hashlib.md5()
        md5_password = hashlib.md5()
        md5_id.update(id.encode(encoding="utf-8"))
        md5_password.update(password.encode(encoding="utf-8"))

        with open("users.json", "r") as file:
            model = json.load(file)

        id_ok = md5_id.hexdigest() in model.keys()
        password_ok = md5_password.hexdigest() in model.values()
        if id_ok and password_ok:
            self.ok_signal.emit(True)

        self.acount_le.clear()
        self.password_le.clear()
        self.acount_le.setFocus()
        self.try_times += 1

    def close_all(self):
        """Close the program."""
        sys.exit()
		
    def closeEvent(self, event):
	    self.close()
