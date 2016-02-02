# -*- coding: utf-8 -*-
import unittest
from service import workfilesservice

class MiliCloudTest(unittest.TestCase):
    def setUp(self):        
        self.mili = workfilesservice.WorkFile()
        
    
    def tearDown(self):  
        self.mili = None  
    

    def testGetTaskName(self):
        t3= '%d' %516 
        print self.mili.callService(t3,'Task') 
    
  
if __name__ == "__main__":  
    unittest.main()  
    