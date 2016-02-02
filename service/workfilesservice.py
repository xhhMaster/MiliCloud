# -*- coding: utf-8 -*-
import lib.requests as requests

class WorkFile(object):
    
    def __init__(self):
        self.url = 'http://192.168.150.233:4267/api/maya/publishFile?entity_id='
       
    def __getFileName(self,entity_id,entity_type):
        self.url = self.url + entity_id + '&entity_type=' + entity_type 
        result = requests.post(self.url)
        if result.text != u"null":
            return result.json()['VERSION']
        else:
            return ""
          
    def callService(self,entity_id,entity_type):
        return self.__getFileName(entity_id,entity_type)