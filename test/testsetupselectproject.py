# -*- coding: utf-8 -*-
import unittest
from launch.selecttask import Widget
import sys
from PySide import QtGui

class SelectProjectTest(unittest.TestCase):
    
    def setUp(self):       
        app = QtGui.QApplication(sys.argv) 
        t = '%d' %2
        t1 = '%d' %3
        self.project = Widget(t1,t,u'')     
        self.project.show()
        app.exec_()         
    
    def testTask(self):
        t = '%d' %2
        t1 = '%d' %3
        self.project = Widget(t1,t,u'')     
        self.project.show()
    
    
if __name__ == "__main__":  
    unittest.main()  
    