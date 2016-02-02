# -*- coding: utf-8 -*-
import unittest
from service.loginservice import Login
import setup.setuplogin as setuplogin
class MiliCloudTest(unittest.TestCase):
    
    def setUp(self):        
        self.mili = setuplogin()
        
  
    def tearDown(self):  
        self.mili = None  
   
    def testGetProjectName(self): 
        t = '%d' %234
        print self.mili.callService('admin',t)
  
if __name__ == "__main__":  
    unittest.main()  

