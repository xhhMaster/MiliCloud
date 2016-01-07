# -*- coding: utf-8 -*-
import lib.requests as requests

class Task(object):
    
    def __init__(self):
        self.url = 'http://192.168.150.233:4267/api/maya/publishFile?entity_id='
       
    def __getTaskName(self,entity_id,entity_type):
        self.url = self.url + entity_id + '&entity_type=' + entity_type 
        result = requests.post(self.url)
        if result.text != u"null":
            return result.json()['VERSION']
        else:
            return ""
          
         
          
    def callService(self,entity_id,entity_type):
        return self.__getTaskName(entity_id,entity_type)