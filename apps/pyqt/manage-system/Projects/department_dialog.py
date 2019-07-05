# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'department_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(332, 300)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 20, 31, 16))
        self.label.setObjectName("label")
        self.dpt_up_pb = QtWidgets.QPushButton(Dialog)
        self.dpt_up_pb.setGeometry(QtCore.QRect(181, 60, 75, 23))
        self.dpt_up_pb.setObjectName("dpt_up_pb")
        self.dpt_down_pb = QtWidgets.QPushButton(Dialog)
        self.dpt_down_pb.setGeometry(QtCore.QRect(181, 90, 75, 23))
        self.dpt_down_pb.setObjectName("dpt_down_pb")
        self.dpt_add_pb = QtWidgets.QPushButton(Dialog)
        self.dpt_add_pb.setGeometry(QtCore.QRect(181, 150, 75, 23))
        self.dpt_add_pb.setObjectName("dpt_add_pb")
        self.dpt_del_pb = QtWidgets.QPushButton(Dialog)
        self.dpt_del_pb.setGeometry(QtCore.QRect(181, 210, 75, 23))
        self.dpt_del_pb.setObjectName("dpt_del_pb")
        self.dpt_modify_pb = QtWidgets.QPushButton(Dialog)
        self.dpt_modify_pb.setGeometry(QtCore.QRect(181, 180, 75, 23))
        self.dpt_modify_pb.setObjectName("dpt_modify_pb")
        self.dpt_quit_pb = QtWidgets.QPushButton(Dialog)
        self.dpt_quit_pb.setGeometry(QtCore.QRect(240, 260, 81, 31))
        self.dpt_quit_pb.setObjectName("dpt_quit_pb")
        self.listView = QtWidgets.QListView(Dialog)
        self.listView.setGeometry(QtCore.QRect(10, 50, 131, 192))
        self.listView.setObjectName("listView")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "部门管理"))
        self.label.setText(_translate("Dialog", "部门："))
        self.dpt_up_pb.setText(_translate("Dialog", "上移"))
        self.dpt_down_pb.setText(_translate("Dialog", "下移"))
        self.dpt_add_pb.setText(_translate("Dialog", "增加"))
        self.dpt_del_pb.setText(_translate("Dialog", "删除"))
        self.dpt_modify_pb.setText(_translate("Dialog", "修改"))
        self.dpt_quit_pb.setText(_translate("Dialog", "退出"))

