# -*- coding: utf-8 -*-
from PySide import QtGui,QtCore

class UI(object):
    #初始化自定义TableWidget
    def initTableWidget(self,header,columnNum):
        table = QtGui.QTableWidget() 
        table.setColumnCount(columnNum)
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setVisible(False)
        table.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        table.setShowGrid(False)
        table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        table.horizontalHeader().setStretchLastSection(True)#设置充满表宽度
        table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        table.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        table.resizeColumnsToContents()
        table.resizeRowsToContents()
        #table.setFrameShape(QtGui.QFrame.NoFrame) #去除边框
        table.setHorizontalHeaderLabels(header)
        return table
    
    #初始化提示信息窗口
    def initMessageBox(self):
        warning = QtGui.QMessageBox()
        okBtn = warning.addButton(u'确定',QtGui.QMessageBox.AcceptRole)
        okBtn.clicked.connect(warning.close)
        return warning   
    
    def initListWidget(self):
        List = QtGui.QListWidget() 
        List.setFocusPolicy(QtCore.Qt.NoFocus)
        return List
        
class Msg(object):
    #自定义显示子窗口
    def showDialog(self,outputWindow,txtTitle,txtMainContent,txtSubContent):
        outputWindow.setWindowTitle(txtTitle)
        outputWindow.setText(txtMainContent)
        outputWindow.setInformativeText(txtSubContent)
        outputWindow.show()
        
