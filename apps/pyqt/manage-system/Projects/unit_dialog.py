# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'unit_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(234, 110)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 91, 16))
        self.label.setObjectName("label")
        self.unit_name_le = QtWidgets.QLineEdit(Dialog)
        self.unit_name_le.setGeometry(QtCore.QRect(10, 50, 211, 20))
        self.unit_name_le.setObjectName("unit_name_le")
        self.unit_ok_pb = QtWidgets.QPushButton(Dialog)
        self.unit_ok_pb.setGeometry(QtCore.QRect(20, 80, 75, 23))
        self.unit_ok_pb.setObjectName("unit_ok_pb")
        self.unit_quit_pb = QtWidgets.QPushButton(Dialog)
        self.unit_quit_pb.setGeometry(QtCore.QRect(140, 80, 75, 23))
        self.unit_quit_pb.setObjectName("unit_quit_pb")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "单位名称"))
        self.label.setText(_translate("Dialog", "请输入单位名称："))
        self.unit_ok_pb.setText(_translate("Dialog", "确定"))
        self.unit_quit_pb.setText(_translate("Dialog", "退出"))

