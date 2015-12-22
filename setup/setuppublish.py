# -*- coding: utf-8 -*-
from PySide import QtGui
from ui.publish_ui import Ui_Widget
import os
import maya.cmds as cmds

class Widget(QtGui.QWidget, Ui_Widget):
    def __init__(self, parent=None):
        super(Widget,self).__init__(parent)
        self.setupUi(self)
        self.save()
        self.cancelBtn.clicked.connect(self.cancelClicked)

    def cancelClicked(self):
        self.close()
        
        
    def save(self):
        s = os.getcwd()
        self.path = r'D:\\123'
        b = os.path.exists(self.path)
        if b == False:
            os.makedirs(self.path)    
        else:
            cmds.file(rn='D:\\123\test',save =1,type='mayaBinary')
        print s 
    

        
    
        
        
        