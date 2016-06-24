# -*- coding: utf-8 -*-
import unittest
from service import loginservice

class MiliCloudTest(unittest.TestCase):
    def setUp(self):        
        self.mili = loginservice.Login()
        
    
    def tearDown(self):  
        self.mili = None  
    

    def testGetTaskName(self):
        t3= '%d' %3
        print self.mili.callService('yingjun','1') 
    
  
if __name__ == "__main__":  
    unittest.main()  
        
  
   


