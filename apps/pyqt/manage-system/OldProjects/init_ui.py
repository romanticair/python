# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'init_ui.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_1 = QtWidgets.QLabel(self.centralwidget)
        self.label_1.setGeometry(QtCore.QRect(151, 191, 54, 12))
        self.label_1.setTextFormat(QtCore.Qt.AutoText)
        self.label_1.setObjectName("label_1")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(151, 234, 54, 12))
        self.label_2.setObjectName("label_2")
        self.lineEdit_1 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_1.setGeometry(QtCore.QRect(200, 188, 113, 20))
        self.lineEdit_1.setInputMask("")
        self.lineEdit_1.setObjectName("lineEdit_1")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(200, 230, 113, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.loginButton = QtWidgets.QPushButton(self.centralwidget)
        self.loginButton.setGeometry(QtCore.QRect(160, 280, 75, 23))
        self.loginButton.setObjectName("loginButton")
        self.changePasswordButton = QtWidgets.QPushButton(self.centralwidget)
        self.changePasswordButton.setGeometry(QtCore.QRect(270, 280, 75, 23))
        self.changePasswordButton.setObjectName("changePasswordButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "工资系统登录"))
        self.label_1.setText(_translate("MainWindow", "账号："))
        self.label_2.setText(_translate("MainWindow", "密码："))
        self.lineEdit_1.setPlaceholderText(_translate("MainWindow", "请输入你的账号"))
        self.lineEdit_2.setPlaceholderText(_translate("MainWindow", "请输入你的密码"))
        self.loginButton.setText(_translate("MainWindow", "登录"))
        self.loginButton.setShortcut(_translate("MainWindow", "Return"))
        self.changePasswordButton.setText(_translate("MainWindow", "重置密码"))

