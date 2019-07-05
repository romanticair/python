import os
import time
import random
from PyQt5.QtWidgets import QMainWindow, QDialog, QWidget, QMessageBox
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtSql import (QSqlQuery, QSqlDatabase, QSqlTableModel, QSqlRelationalTableModel,
                         QSqlRelation, QSqlRelationalDelegate)
from system_ui import Ui_MainWindow

import clerk_dialog_slot
import department_dialog_slot
import project_dialog_slot
import unit_dialog_slot

from db import *


class WhichDelegate(QSqlRelationalDelegate):
    def __init__(self, parent=None):
        super(WhichDelegate, self).__init__(parent)


class MyWin(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyWin, self).__init__()
        self.setupUi(self)
        self.init_db()
        self.tableView.setModel(self.model)
        self.tableView.resizeColumnsToContents()
        # 试试使用委托，要不要重写实现这个委托类？
        self.tableView.setItemDelegate(QSqlRelationalDelegate(self))

    def init_db(self):
        filename = os.path.join(os.path.dirname(__file__), "management{0}.db".format(createyear))
        create = not os.path.exists(filename)
        self.db = open_database()
        self.db.open()
        if create:
            init_tables()
        self.model = model(self)

    @pyqtSlot()
    def on_clk_tb_clicked(self):
        """
        职员管理入口
        """
        self.clerk = clerk_dialog_slot.ClerkDialog('clerks{0}'.format(createmoth), self.model, self)
        self.clerk.exec_()

    @pyqtSlot()
    def on_dpt_tb_clicked(self):
        """
        部门管理入口
        """
        self.department = department_dialog_slot.DepartmentDialog()
        self.department.exec_()

    @pyqtSlot()
    def on_prj_tb_clicked(self):
        """
        项目管理入口
        """
        self.project = project_dialog_slot.ProjectDialog()
        self.project.exec_()

    @pyqtSlot()
    def on_unit_tb_clicked(self):
        """
        单位名称入口
        """
        self.unit = unit_dialog_slot.UnitDialog()
        self.unit.exec_()

    def closeEvent(self, event):
        # 重写退出事件
        reply = QMessageBox.question(self, '提示', 'Are you sure to quit ?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.db.close()
            event.accept()
        else:
            event.ignore()
