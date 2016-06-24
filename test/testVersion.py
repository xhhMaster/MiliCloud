# -*- coding: utf-8 -*-
import unittest
from service.versionservice import GetVersionByName

class MiliCloudTest(unittest.TestCase):
    def setUp(self):        
        self.mili = GetVersionByName()
        
    
    def tearDown(self):  
        self.mili = None  
    

    def testGetTaskName(self):
        print self.mili.callService('a1234.001.ma','88')
    
  
if __name__ == "__main__":  
    unittest.main()  
        