from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlTableModel, QSqlQuery, QSqlDatabase
from PyQt5.QtWidgets import QDialog, QTableView, QAbstractItemView
from clerk_dialog import Ui_Dialog
from PyQt5.QtCore import pyqtSlot

from db import (ORDER, ID, NAME, GENDER, DEPARTMENT, createmoth)


class ClerkDialog(QDialog, Ui_Dialog):
    def __init__(self, table, mainModel, parent=None):
        super(ClerkDialog, self).__init__(parent)
        self.setupUi(self)
        self.table = table
        self.mainModel = mainModel

        # 关联待写
        self.model = QSqlTableModel(self)
        self.model.setTable(table)
        self.model.setSort(ID, Qt.AscendingOrder)
        self.model.setHeaderData(ID, Qt.Horizontal, "Order")
        self.model.setHeaderData(NAME, Qt.Horizontal, "Name")
        self.model.setHeaderData(GENDER, Qt.Horizontal, "Gender")
        self.model.setHeaderData(DEPARTMENT, Qt.Horizontal, "Department")
        self.model.select()

        self.tableView.setModel(self.model)
        self.tableView.setSelectionMode(QTableView.SingleSelection)
        self.tableView.setSelectionBehavior(QTableView.SelectRows)
        self.tableView.setColumnHidden(ID, True)
        self.tableView.setColumnHidden(GENDER, True)
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 不允许编辑
        # self.tableView.verticalHeader(False)
        self.tableView.resizeColumnsToContents()
        items = []                                                        # 获取所有部门名称
        query = QSqlQuery()
        query.exec("SELECT dpt_name FROM departments{0}".format(createmoth))
        while query.next():                                              # 找到第一条记录，每次后移一条记录
            items.append(query.value("dpt_name"))
        self.clerk_dpt_comboBox.addItems(items)

    @pyqtSlot()
    def on_clk_del_pb_clicked(self):
        """删除职员"""
        index = self.tableView.currentIndex()
        if not index.isValid():
            return
        self.model.removeRow(index.row())
        self.model.submitAll()
        self.model.select()
        self.mainModel.select()                      # 同步更新

    @pyqtSlot()
    def on_clk_add_pb_clicked(self):
        """增加职员"""
        id = self.clk_seq_le.text()                  # 获取id
        name = self.clk_name_le.text()               # 获取姓名
        dpt = self.clerk_dpt_comboBox.currentText()  # 获取部门
        query = QSqlQuery()                          # 将名称转换成部门id
        query.exec("SELECT dpt_id FROM departments{0} WHERE dpt_name='{1}'".format(createmoth, dpt))
        query.next()
        dpt_id = query.value(0)

        row = self.model.rowCount()                   # 在最后一行加上去
        # row = self.tableView.currentIndex().row()   # 在所选取的行插入，在这里不可行，因为已经有排序策略
        self.model.database().transaction()
        self.model.insertRow(row)
        self.model.setData(self.model.index(row, ID), id)
        self.model.setData(self.model.index(row, NAME), name)
        self.model.setData(self.model.index(row, DEPARTMENT), dpt_id)
        self.model.submitAll()
        self.model.select()
        self.model.database().commit()
        self.mainModel.select()

    @pyqtSlot()
    def on_clk_modify_pb_clicked(self):
        """修改职员"""
        index = self.tableView.currentIndex()
        if not index.isValid():
            return
        self.clk_id = self.model.record(index.row()).value(ID)
        clk_name = self.model.record(index.row()).value(NAME)
        clk_dpt = self.model.record(index.row()).value(DEPARTMENT)

        from change_slot import ChangeDialog
        dialog = ChangeDialog(self.clk_id, clk_name, clk_dpt, self)
        dialog.okClickedSignal.connect(self.ok_slot)
        if dialog.exec():
            print("Done")

    def ok_slot(self, cid, name, dpt):
        QSqlDatabase.database().transaction()
        query = QSqlQuery()
        query.exec("UPDATE clerks{0} SET clk_id='{1}',clk_name='{2}',dpt_id='{3}'"
                   "WHERE clk_id='{4}'".format(createmoth, cid, name, dpt, self.clk_id))
        if 'Yes':
            QSqlDatabase.database().commit()
            self.model.select()
            self.mainModel.select()
        else:
            QSqlDatabase.database().rollback()

    @pyqtSlot()
    def on_clk_up_pb_clicked(self):
        """职员上移"""
        # 先避开
        pass

    @pyqtSlot()
    def on_clk_down_pb_clicked(self):
        """职员下移"""
        # 先避开
        pass

    @pyqtSlot()
    def on_clk_save_pb_clicked(self):
        """保存"""
        # 先避开
        pass

    @pyqtSlot()
    def on_clk_quit_pb_clicked(self):
        QDialog.done(self, 1)


