# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'register_ui.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(530, 437)
        self.changeButton = QtWidgets.QPushButton(Form)
        self.changeButton.setGeometry(QtCore.QRect(210, 285, 75, 23))
        self.changeButton.setObjectName("changeButton")
        self.lineEdit_1 = QtWidgets.QLineEdit(Form)
        self.lineEdit_1.setGeometry(QtCore.QRect(199, 137, 121, 20))
        self.lineEdit_1.setObjectName("lineEdit_1")
        self.lineEdit_2 = QtWidgets.QLineEdit(Form)
        self.lineEdit_2.setGeometry(QtCore.QRect(199, 186, 121, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_1 = QtWidgets.QLabel(Form)
        self.label_1.setGeometry(QtCore.QRect(150, 140, 54, 12))
        self.label_1.setObjectName("label_1")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(140, 190, 54, 12))
        self.label_2.setObjectName("label_2")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(140, 234, 54, 12))
        self.label.setObjectName("label")
        self.lineEdit_3 = QtWidgets.QLineEdit(Form)
        self.lineEdit_3.setGeometry(QtCore.QRect(199, 230, 121, 20))
        self.lineEdit_3.setObjectName("lineEdit_3")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "注册页面"))
        self.changeButton.setText(_translate("Form", "确定修改"))
        self.lineEdit_2.setPlaceholderText(_translate("Form", "请输入密码"))
        self.label_1.setText(_translate("Form", "账号："))
        self.label_2.setText(_translate("Form", "原密码："))
        self.label.setText(_translate("Form", "新密码："))
        self.lineEdit_3.setPlaceholderText(_translate("Form", "请再次输入您的密码"))

