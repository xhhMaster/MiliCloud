# -*- coding: utf-8 -*-
import unittest
from service.assetservice import AssetByType

class MiliCloudTest(unittest.TestCase):
    
    def setUp(self):        
        self.mili = AssetByType()
        
    
    def tearDown(self):  
        self.mili = None  
    

    def testGetAssetName(self):
        t1 = '%d' %5
        t2 = '%d' %2
        self.mili.callService(t2) 
    
if __name__ == "__main__":  
    unittest.main() 