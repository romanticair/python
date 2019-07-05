from PyQt5.QtWidgets import QDialog
from unit_dialog import Ui_Dialog


class UnitDialog(QDialog, Ui_Dialog):
    def __init__(self):
        super(UnitDialog, self).__init__()
        self.setupUi(self)
