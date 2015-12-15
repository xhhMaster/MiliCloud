# -*- coding: utf-8 -*-
import unittest
from service.assetservice import Asset

class MiliCloudTest(unittest.TestCase):
    
  
    def setUp(self):        
        self.mili = Asset()
        
    
    def tearDown(self):  
        self.mili = None  
    

    def testGetAssetName(self):
        t = '%d' %2
        print self.mili.callService(t) 
    
  
if __name__ == "__main__":  
    unittest.main() 