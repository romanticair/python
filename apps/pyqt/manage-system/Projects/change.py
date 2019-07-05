# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'change.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.id_le = QtWidgets.QLineEdit(Dialog)
        self.id_le.setGeometry(QtCore.QRect(150, 66, 113, 20))
        self.id_le.setObjectName("id_le")
        self.name_le = QtWidgets.QLineEdit(Dialog)
        self.name_le.setGeometry(QtCore.QRect(150, 107, 113, 20))
        self.name_le.setObjectName("name_le")
        self.dpt_combo = QtWidgets.QComboBox(Dialog)
        self.dpt_combo.setGeometry(QtCore.QRect(150, 146, 69, 22))
        self.dpt_combo.setObjectName("dpt_combo")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(70, 70, 61, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(94, 110, 54, 12))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(93, 150, 54, 12))
        self.label_3.setObjectName("label_3")
        self.ok_pb = QtWidgets.QPushButton(Dialog)
        self.ok_pb.setGeometry(QtCore.QRect(100, 230, 75, 23))
        self.ok_pb.setObjectName("ok_pb")
        self.cancel_pb = QtWidgets.QPushButton(Dialog)
        self.cancel_pb.setGeometry(QtCore.QRect(210, 230, 75, 23))
        self.cancel_pb.setObjectName("cancel_pb")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "员工编号："))
        self.label_2.setText(_translate("Dialog", "姓名："))
        self.label_3.setText(_translate("Dialog", "部门："))
        self.ok_pb.setText(_translate("Dialog", "确定"))
        self.cancel_pb.setText(_translate("Dialog", "取消"))

