# -*- coding: utf-8 -*-
import unittest
from mayaApi import milicloud


class MiliCloudTest(unittest.TestCase):
    def setUp(self):    
        name = 'huanghao'
        p = '1'    
        self.mili = milicloud.miliCloud(name,p)
    
    def tearDown(self):  
        self.mili = None  
    

    def testGetTaskName(self):
        """
        filters = []
        fields = ['id','name','description']
        print 111
        print self.mili.find('PROJECTS',filters,fields)
        print 111
        """
        
        """
        filters = [{'field': 'project_id', 'customOperator': 'is', 'value':['2']}]
        fields = ['id'] 
        print self.mili.customFind('TASKS',filters,fields)
        """
        
    
        filters = [{'field': 'addressable_id', 'customOperator': 'is', 'value':['26975']}]
        fields = [{'field': 'entity_id', 'value':u'45'}] 
        print self.mili.update('addressings', filters,fields)
        
        
        """
        filters = [{'field': 'id', 'customOperator': 'is', 'value':['134']}]
        fields = [] 
        self.mili.delete('PROJECTS', filters,fields)
        """
       
if __name__ == "__main__":  
    unittest.main()  
    