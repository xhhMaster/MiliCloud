# -*- coding: utf-8 -*-
from PySide import QtGui

class Demo(QtGui.QWidget):
    
    def __init__(self):
        self.shootScreen()
    
    def shootScreen(self):
        
        self.originalPixmap = None
        self.originalPixmap = QtGui.QPixmap.grabWindow(QtGui.QApplication.desktop().winId())
        self.updateScreenshotLabel()
        