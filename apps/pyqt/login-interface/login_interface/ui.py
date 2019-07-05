# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui.ui'
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
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        self.menu_File = QtWidgets.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        self.menu_Help = QtWidgets.QMenu(self.menubar)
        self.menu_Help.setObjectName("menu_Help")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionopen = QtWidgets.QAction(MainWindow)
        self.actionopen.setObjectName("actionopen")
        self.actionclose = QtWidgets.QAction(MainWindow)
        self.actionclose.setObjectName("actionclose")
        self.menu_File.addAction(self.actionopen)
        self.menu_File.addAction(self.actionclose)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "病毒来袭"))
        self.menu_File.setTitle(_translate("MainWindow", "文件"))
        self.menu_Help.setTitle(_translate("MainWindow", "帮助", "H"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionopen.setText(_translate("MainWindow", "打开"))
        self.actionopen.setToolTip(_translate("MainWindow", "打开文件"))
        self.actionopen.setStatusTip(_translate("MainWindow", "打开一个文件"))
        self.actionopen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionclose.setText(_translate("MainWindow", "关闭"))
        self.actionclose.setToolTip(_translate("MainWindow", "关闭文件"))
        self.actionclose.setStatusTip(_translate("MainWindow", "关闭该文件"))
        self.actionclose.setShortcut(_translate("MainWindow", "Ctrl+C"))

import apprcc_rc
