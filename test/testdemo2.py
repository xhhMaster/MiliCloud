# -*- coding: utf-8 -*-
import unittest
from service import thumbnailservice

class MiliCloudTest(unittest.TestCase):
    def setUp(self):        
        self.mili = thumbnailservice.SelectImg()
        
    
    def tearDown(self):  
        self.mili = None  
    

    def testGetTaskName(self):
        t3= '%d' %3
        self.mili.callService(t3) 
    
  
if __name__ == "__main__":  
    unittest.main()  