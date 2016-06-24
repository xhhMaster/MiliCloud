# -*- coding: utf-8 -*-
from PySide import QtCore, QtGui

class Ui_Widget(object):
    def setupUi(self, Widget):
        Widget.setObjectName("Widget")
        Widget.resize(605, 922)
        Widget.setMaximumSize(605, 922)
        Widget.setMinimumSize(605, 922)
        self.groupBox = QtGui.QGroupBox(Widget)
        self.groupBox.setGeometry(QtCore.QRect(10, 20, 581, 841))
        self.groupBox.setObjectName("groupBox")
        self.search = QtGui.QLineEdit(self.groupBox)
        self.search.setGeometry(QtCore.QRect(10, 30, 561, 20))
        self.search.setObjectName("search")
        self.scrollArea = QtGui.QScrollArea(self.groupBox)
        self.scrollArea.setGeometry(QtCore.QRect(10, 60, 561, 770))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 561, 760))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.updateBtn = QtGui.QPushButton(Widget)
        self.updateBtn.setGeometry(QtCore.QRect(400, 880, 75, 23))
        self.updateBtn.setObjectName("updateBtn")
        self.cancelBtn = QtGui.QPushButton(Widget)
        self.cancelBtn.setGeometry(QtCore.QRect(500, 880, 75, 23))
        self.cancelBtn.setObjectName("cancelBtn")

        self.retranslateUi(Widget)
        QtCore.QMetaObject.connectSlotsByName(Widget)

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QtGui.QApplication.translate("Widget", "更新引用", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Widget", "已经选择的引用文件", None, QtGui.QApplication.UnicodeUTF8))
        self.updateBtn.setText(QtGui.QApplication.translate("Widget", "更新", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelBtn.setText(QtGui.QApplication.translate("Widget", "取消", None, QtGui.QApplication.UnicodeUTF8))