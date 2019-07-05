from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtSql import QSqlQuery, QSqlDatabase
from change import Ui_Dialog


class ChangeDialog(QDialog, Ui_Dialog):
    okClickedSignal = pyqtSignal(str, str, str)

    def __init__(self, cid, name, dpt, parent=None):
        super(ChangeDialog, self).__init__(parent)
        self.setupUi(self)

        self.id_le.setText(cid)
        self.name_le.setText(name)
        self.dpt_combo.addItem(dpt)

    @pyqtSlot()
    def on_ok_pb_clicked(self):
        cid = self.id_le.text()
        name = self.name_le.text()
        dpt_id = self.dpt_combo.currentText()
        if cid and name and dpt_id:
            self.okClickedSignal.emit(cid, name, dpt_id)
            QDialog.done(self, 1)

    @pyqtSlot()
    def on_cancel_pb_clicked(self):
        QDialog.done(self, 1)  # return 1
