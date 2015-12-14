# -*- coding: utf-8 -*-
import unittest
from service.taskservice import Task

class MiliCloudTest(unittest.TestCase):
    
  
    def setUp(self):        
        self.mili = Task()
        
    
    def tearDown(self):  
        self.mili = None  
    

    def testGetTaskName(self):
        t = 3
        print self.mili.callService(t) 
    
  
if __name__ == "__main__":  
    unittest.main()  
    