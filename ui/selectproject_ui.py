# -*- coding: utf-8 -*-
from PySide import QtCore, QtGui

class Ui_Widget(object):
    def setupUi(self, Widget):
        Widget.setObjectName("Widget")
        Widget.resize(426, 549)
        Widget.setMaximumSize(426, 549)
        Widget.setMinimumSize(426, 549)
        self.projectGroupBox = QtGui.QGroupBox(Widget)
        self.projectGroupBox.setGeometry(QtCore.QRect(30, 30, 361, 441))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(9)
        font.setWeight(75)
        font.setBold(True)
        self.projectGroupBox.setFont(font)
        self.projectGroupBox.setFlat(False)
        self.projectGroupBox.setObjectName("projectGroupBox")
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(11)
        font.setWeight(75)
        font.setBold(True)
        self.selectBtn = QtGui.QPushButton(Widget)
        self.selectBtn.setGeometry(QtCore.QRect(230, 490, 75, 23))
        self.selectBtn.setObjectName("selectBtn")       
        self.cancelBtn = QtGui.QPushButton(Widget)
        self.cancelBtn.setGeometry(QtCore.QRect(320, 490, 75, 23))
        self.cancelBtn.setObjectName("cancelBtn")
        self.retranslateUi(Widget)
        QtCore.QMetaObject.connectSlotsByName(Widget)

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QtGui.QApplication.translate("Widget", "选择项目", None, QtGui.QApplication.UnicodeUTF8))
        self.projectGroupBox.setTitle(QtGui.QApplication.translate("Widget", "项目名称列表", None, QtGui.QApplication.UnicodeUTF8))
        self.selectBtn.setText(QtGui.QApplication.translate("Widget", "确定", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelBtn.setText(QtGui.QApplication.translate("Widget", "取消", None, QtGui.QApplication.UnicodeUTF8))

