# -*- coding: utf-8 -*-
import unittest
from service.taskservice import Task

class MiliCloudTest(unittest.TestCase):
    
  
    def setUp(self):        
        self.mili = Task()
        
    
    def tearDown(self):  
        self.mili = None  
    

    def testGetTaskName(self):
        print self.mili.callService('20','Asset') 
    
  
if __name__ == "__main__":  
    unittest.main()  
    