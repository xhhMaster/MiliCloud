# -*- coding: utf-8 -*-
import unittest
from service.shotservice import Shot

class MiliCloudTest(unittest.TestCase):
    
    #初始化工作  
    def setUp(self):        
        self.mili = Shot()
        
    #退出清理工作  
    def tearDown(self):  
        self.mili = None  
    
    #具体的测试用例，一定要以test开头   
    def testGetProjectName(self):
        t = 2
        print self.mili.callService(t) 
    
  
if __name__ == "__main__":  
    unittest.main()  
    