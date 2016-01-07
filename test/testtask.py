# -*- coding: utf-8 -*-
import unittest
from service.workfilesservice import Task

class MiliCloudTest(unittest.TestCase):
    
  
    def setUp(self):        
        self.mili = Task()
        
    
    def tearDown(self):  
        self.mili = None  
    

    def testGetTaskName(self):
        print self.mili.callService('82','Shot') 
    
  
if __name__ == "__main__":  
    unittest.main()  
    