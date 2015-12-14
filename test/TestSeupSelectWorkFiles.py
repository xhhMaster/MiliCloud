# -*- coding: utf-8 -*-
import unittest
from setup.setupselectworkfiles import Widget
import sys
from PySide import QtGui

class SelectProjectTest(unittest.TestCase):
    
    def setUp(self):       
        app = QtGui.QApplication(sys.argv) 
        self.workfile = Widget()     
        self.workfile.show()
        app.exec_()         
    
    def testGetShotInfo(self):
        print self.workfile.getTaskInfo()
        
        
if __name__ == "__main__":  
    unittest.main()  
    