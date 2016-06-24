import unittest
from launch.publish import Widget
import sys
from PySide import QtGui


class PublishTest(unittest.TestCase):
    
    def setUp(self):       
        app = QtGui.QApplication(sys.argv) 
        self.project = Widget(6)     
        self.project.show()
        app.exec_()
    
    def testBtn(self):
        self.project.cancelBtnClicked()
    
if __name__ == "__main__":  
    unittest.main()  
    