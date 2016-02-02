# -*- coding: utf-8 -*-
import unittest
from service.taskservice import MyTask

class MiliCloudTest(unittest.TestCase):
    
  
    def setUp(self):        
        self.mili = MyTask()
        
    
    def tearDown(self):  
        self.mili = None  
    

    def testGetTaskName(self):
        t= '%d' %20
        t1= '%d' %1
        t2= '%d' %1
        t3= '%d' %540
        self.mili.callService(t1,t2,'')
    
  
if __name__ == "__main__":  
    unittest.main()  
    