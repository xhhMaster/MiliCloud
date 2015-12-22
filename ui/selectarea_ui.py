# -*- coding: utf-8 -*-
from PySide import QtGui,QtCore
import maya.OpenMayaUI as mui
import shiboken



class SelectedWorkFiles_UI(object):
    
    def __init__(self):
        self.UI()
        
     
    def UI(self):
        #创建主窗口
        parent = self.getMayaWindow()
        self.mainWindow = QtGui.QMainWindow(parent)
        self.mainWindow.setMaximumSize(650,350)
        self.mainWindow.setMinimumSize(650,350)
        self.mainWindow.setWindowTitle(u"选择文件")
        Widget = QtGui.QWidget()
        self.mainWindow.setCentralWidget(Widget)
        groupBox = QtGui.QGroupBox(u"提示信息")
        groupBox.setStyleSheet("font-size:15px;")
        #外层布局
        outLayout = QtGui.QVBoxLayout()
        outLayout.addWidget(groupBox)
        Widget.setLayout(outLayout)
        #创建一个按钮
        button= QtGui.QPushButton(u"单击此区域选择工作文件")
        button.setMaximumSize(600,300)
        button.setMinimumSize(600,300)
        button.setStyleSheet("font-size:30px;border:solid black 1px")
        button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        button.clicked.connect(lambda *args: [self.btnClicked()])
        #内层布局
        innerLayout = QtGui.QVBoxLayout()
        innerLayout.addWidget(button)
        groupBox.setLayout(innerLayout)
        #显示窗口
        self.mainWindow.show()
        
    def btnClicked(self,*args):     
        import setup.setupselectproject as setupselectproject
        self.mainWindow.close()
        self.Widget = setupselectproject.Widget()
        self.Widget.show()      
        
            
    def getMayaWindow(self,*args):
        pointer = mui.MQtUtil.mainWindow()
        return shiboken.wrapInstance(long(pointer),QtGui.QWidget)
    