# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'project_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(348, 338)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 20, 61, 16))
        self.label.setObjectName("label")
        self.prj_class_comboBox = QtWidgets.QComboBox(Dialog)
        self.prj_class_comboBox.setGeometry(QtCore.QRect(80, 20, 101, 22))
        self.prj_class_comboBox.setObjectName("prj_class_comboBox")
        self.prj_left_pb = QtWidgets.QPushButton(Dialog)
        self.prj_left_pb.setGeometry(QtCore.QRect(10, 280, 75, 23))
        self.prj_left_pb.setObjectName("prj_left_pb")
        self.prj_right_pb = QtWidgets.QPushButton(Dialog)
        self.prj_right_pb.setGeometry(QtCore.QRect(100, 280, 75, 23))
        self.prj_right_pb.setObjectName("prj_right_pb")
        self.prj_add_pb = QtWidgets.QPushButton(Dialog)
        self.prj_add_pb.setGeometry(QtCore.QRect(220, 80, 75, 23))
        self.prj_add_pb.setObjectName("prj_add_pb")
        self.prj_del_pb = QtWidgets.QPushButton(Dialog)
        self.prj_del_pb.setGeometry(QtCore.QRect(220, 130, 75, 23))
        self.prj_del_pb.setObjectName("prj_del_pb")
        self.prj_modify_pb = QtWidgets.QPushButton(Dialog)
        self.prj_modify_pb.setGeometry(QtCore.QRect(220, 180, 75, 23))
        self.prj_modify_pb.setObjectName("prj_modify_pb")
        self.prj_quit_pb = QtWidgets.QPushButton(Dialog)
        self.prj_quit_pb.setGeometry(QtCore.QRect(260, 300, 75, 23))
        self.prj_quit_pb.setObjectName("prj_quit_pb")
        self.columnView = QtWidgets.QColumnView(Dialog)
        self.columnView.setGeometry(QtCore.QRect(10, 50, 171, 192))
        self.columnView.setObjectName("columnView")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "项目管理"))
        self.label.setText(_translate("Dialog", "项目类别："))
        self.prj_left_pb.setText(_translate("Dialog", "左移"))
        self.prj_right_pb.setText(_translate("Dialog", "右移"))
        self.prj_add_pb.setText(_translate("Dialog", "增加"))
        self.prj_del_pb.setText(_translate("Dialog", "删除"))
        self.prj_modify_pb.setText(_translate("Dialog", "修改"))
        self.prj_quit_pb.setText(_translate("Dialog", "退出"))

