# -*- coding: utf-8 -*-
from PySide import QtCore, QtGui

class Ui_Widget(object):
    def setupUi(self, Widget):
        Widget.setObjectName("Widget")
        Widget.resize(398, 182)
        Widget.setMaximumSize(398, 182)
        Widget.setMinimumSize(398, 182)
        self.formLayoutWidget = QtGui.QWidget(Widget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(40, 30, 321, 81))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(-1, 20, -1, -1)
        self.formLayout.setHorizontalSpacing(15)
        self.formLayout.setVerticalSpacing(20)
        self.formLayout.setObjectName("formLayout")
        self.userLabel = QtGui.QLabel(self.formLayoutWidget)
        self.userLabel.setObjectName("userLabel")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.userLabel)
        self.userName = QtGui.QLineEdit(self.formLayoutWidget)
        self.userName.setObjectName("userName")
        self.userName.setMinimumHeight(20)
        
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.userName)
        self.pwLabel = QtGui.QLabel(self.formLayoutWidget)
        self.pwLabel.setObjectName("pwLabel")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.pwLabel)
        self.passWord = QtGui.QLineEdit(self.formLayoutWidget)
        self.passWord.setObjectName("passWord")
        self.passWord.setMinimumHeight(20)
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.passWord)
        self.loginBtn = QtGui.QPushButton(Widget)
        self.loginBtn.setGeometry(QtCore.QRect(170, 135, 71, 23))
        self.loginBtn.setObjectName("loginBtn")

        self.retranslateUi(Widget)
        QtCore.QMetaObject.connectSlotsByName(Widget)

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QtGui.QApplication.translate("Widget", "登录窗口", None, QtGui.QApplication.UnicodeUTF8))
        self.userLabel.setText(QtGui.QApplication.translate("Widget", "用户名：", None, QtGui.QApplication.UnicodeUTF8))
        self.pwLabel.setText(QtGui.QApplication.translate("Widget", "密码：", None, QtGui.QApplication.UnicodeUTF8))
        self.loginBtn.setText(QtGui.QApplication.translate("Widget", "登录", None, QtGui.QApplication.UnicodeUTF8))