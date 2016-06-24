# -*- coding: utf-8 -*-
import unittest
from service.taskservice import Task

class MiliCloudTest(unittest.TestCase):
    
  
    def setUp(self):        
        self.mili = Task()
        
    
    def tearDown(self):  
        self.mili = None  
    

    def testGetTaskName(self):
        t1= '%d' %15
        t2= '%d' %5
        t3= '%d' 

        print self.mili.callService(t1,'shot',t2,t3)
    
  
if __name__ == "__main__":  
    unittest.main()  
    