# -*- coding: utf-8 -*-
from PySide import QtCore, QtGui

class Ui_Widget(object):
    def setupUi(self, Widget):
        Widget.setObjectName("Widget")
        Widget.resize(840, 827)
        Widget.setMaximumSize(840, 827)
        Widget.setMinimumSize(840, 827)
        self.workBox = QtGui.QGroupBox(Widget)
        self.workBox.setGeometry(QtCore.QRect(20, 20, 331, 521))
        self.workBox.setObjectName("workBox")
        self.workFile = QtGui.QGroupBox(Widget)
        self.workFile.setGeometry(QtCore.QRect(380, 20, 441, 721))
        self.workFile.setObjectName("workFile")
        self.backBtn = QtGui.QPushButton(Widget)
        self.backBtn.setGeometry(QtCore.QRect(550, 780, 75, 23))
        self.backBtn.setObjectName("backBtn")
        self.newBtn = QtGui.QPushButton(Widget)
        self.newBtn.setGeometry(QtCore.QRect(650, 780, 75, 23))
        self.newBtn.setObjectName("newBtn")
        self.openBtn = QtGui.QPushButton(Widget)
        self.openBtn.setGeometry(QtCore.QRect(750, 780, 75, 23))
        self.openBtn.setObjectName("openBtn")

        self.retranslateUi(Widget)
        QtCore.QMetaObject.connectSlotsByName(Widget)

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QtGui.QApplication.translate("Widget", "选择工作文件", None, QtGui.QApplication.UnicodeUTF8))
        self.workBox.setTitle(QtGui.QApplication.translate("Widget", "Selected Work Area", None, QtGui.QApplication.UnicodeUTF8))
        self.workFile.setTitle(QtGui.QApplication.translate("Widget", "Work Files", None, QtGui.QApplication.UnicodeUTF8))
        self.backBtn.setText(QtGui.QApplication.translate("Widget", "返回", None, QtGui.QApplication.UnicodeUTF8))
        self.newBtn.setText(QtGui.QApplication.translate("Widget", "新建文件", None, QtGui.QApplication.UnicodeUTF8))
        self.openBtn.setText(QtGui.QApplication.translate("Widget", "打开文件", None, QtGui.QApplication.UnicodeUTF8))