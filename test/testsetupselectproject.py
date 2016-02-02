# -*- coding: utf-8 -*-
import unittest
from setup.setupselectproject import Widget
import sys
from PySide import QtGui

class SelectProjectTest(unittest.TestCase):
    
    def setUp(self):       
        app = QtGui.QApplication(sys.argv) 
        t = '%d' %5 
        self.project = Widget(t)     
        self.project.show()
        app.exec_()         
    
    def testGetProjectName(self):
        self.project.bindingProject()
    
    
if __name__ == "__main__":  
    unittest.main()  
    