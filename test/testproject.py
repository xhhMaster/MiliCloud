# -*- coding: utf-8 -*-
import unittest
from service.projectservice import Project

class MiliCloudTest(unittest.TestCase):
    
    def setUp(self):        
        self.mili = Project()
        
  
    def tearDown(self):  
        self.mili = None  
   
    def testGetProjectName(self): 
        t = '%d' %2  
        print self.mili.callInfoService(t)
  
if __name__ == "__main__":  
    unittest.main()  

