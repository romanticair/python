from PyQt5.QtWidgets import QDialog
from department_dialog import Ui_Dialog


class DepartmentDialog(QDialog, Ui_Dialog):
    def __init__(self):
        super(DepartmentDialog, self).__init__()
        self.setupUi(self)
