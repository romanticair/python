# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'verify_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 299)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/pic/images/save.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setStyleSheet("background-image:url(:/pic/images/armyFlag.jpg)")
        Dialog.setSizeGripEnabled(False)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(60, 70, 41, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(60, 110, 41, 16))
        self.label_2.setObjectName("label_2")
        self.acount_le = QtWidgets.QLineEdit(Dialog)
        self.acount_le.setGeometry(QtCore.QRect(110, 70, 113, 20))
        self.acount_le.setObjectName("acount_le")
        self.password_le = QtWidgets.QLineEdit(Dialog)
        self.password_le.setGeometry(QtCore.QRect(110, 110, 113, 20))
        self.password_le.setInputMethodHints(QtCore.Qt.ImhNone)
        self.password_le.setObjectName("password_le")
        self.login_pb = QtWidgets.QPushButton(Dialog)
        self.login_pb.setGeometry(QtCore.QRect(170, 240, 75, 23))
        self.login_pb.setObjectName("login_pb")
        self.quit_pb = QtWidgets.QPushButton(Dialog)
        self.quit_pb.setGeometry(QtCore.QRect(270, 240, 75, 23))
        self.quit_pb.setObjectName("quit_pb")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "口水快要下滴了"))
        self.label.setText(_translate("Dialog", "账号："))
        self.label_2.setText(_translate("Dialog", "密码："))
        self.login_pb.setText(_translate("Dialog", "登录"))
        self.quit_pb.setText(_translate("Dialog", "退出"))

import apprcc_rc
