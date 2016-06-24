# -*- coding: utf-8 -*-
import unittest
from service import shotservice


class MiliCloudTest(unittest.TestCase):
    
    #初始化工作  
    def setUp(self):        
        self.mili = shotservice.Shot()
        
    #退出清理工作  
    def tearDown(self):  
        self.mili = None  
    
    #具体的测试用例，一定要以test开头   
    def testGetProjectName(self):
        t1 = '%d' %29
        t2 = '%d' %239
        print self.mili.callService(t1, t2, '0', '5')
        
  
if __name__ == "__main__":  
    unittest.main()  
    