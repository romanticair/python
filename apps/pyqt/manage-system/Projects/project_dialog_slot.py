from PyQt5.QtWidgets import QDialog
from project_dialog import Ui_Dialog


class ProjectDialog(QDialog, Ui_Dialog):
    def __init__(self):
        super(ProjectDialog, self).__init__()
        self.setupUi(self)
