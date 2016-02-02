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
        table.horizontalHeader().setStretchLastSection(True)
        table.setHorizontalHeaderLabels(header)
        return table
    
    #初始化提示信息窗口
    def initMessageBox(self):
        warning = QtGui.QMessageBox()
        okBtn = warning.addButton(u'确定',QtGui.QMessageBox.AcceptRole)
        okBtn.clicked.connect(warning.close)
        return warning   
    
class Msg(object):
    #自定义显示子窗口
    def showDialog(self,outputWindow,txtTitle,txtMainContent,txtSubContent):
        outputWindow.setWindowTitle(txtTitle)
        outputWindow.setText(txtMainContent)
        outputWindow.setInformativeText(txtSubContent)
        outputWindow.show()
        
class ThumbnailLabel(QtGui.QLabel):
    """
    Special case label that resizes pixmap that gets set to a specific size.  This
    is duplicated from the tk-framework-widget browser_widget control
    """
    def __init__(self, parent=None):
        QtGui.QLabel.__init__(self, parent)

    def setPixmap(self, pixmap):
        # scale the pixmap down to fit
        if pixmap.height() > 55 or pixmap.width() > 80:
            # scale it down to 120x80
            pixmap = pixmap.scaled(QtCore.QSize(80,55), 
                                   QtCore.Qt.KeepAspectRatio, 
                                   QtCore.Qt.SmoothTransformation)
        
        QtGui.QLabel.setPixmap(self, pixmap)