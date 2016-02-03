# -*- coding: utf-8 -*-
import unittest
from service.loginservice import Login
class MiliCloudTest(unittest.TestCase):
    
    def setUp(self):        
        self.mili = Login()
        
  
    def tearDown(self):  
        self.mili = None  
   
    def testGetProjectName(self): 
        t = '%d' %1
        print self.mili.callService('admin',t)
  
if __name__ == "__main__":  
    unittest.main()  

