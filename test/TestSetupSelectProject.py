# -*- coding: utf-8 -*-
import unittest
from setup.setupselectproject import Widget
import sys
from PySide import QtGui

class SelectProjectTest(unittest.TestCase):
    
    def setUp(self):       
        app = QtGui.QApplication(sys.argv) 
        self.project = Widget()     
        self.project.show()
        app.exec_()         
    
    #def testGetProjectName(self):
        #self.assertEqual(self.project.bindingProject(),None)  
    
    def testSelectedClicked(self):
        self.assertEqual(self.project.selectedClicked(),None)  
    
if __name__ == "__main__":  
    unittest.main()  
    