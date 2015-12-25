# -*- coding: utf-8 -*-
import core.requests as requests

class Task(object):
    
    def __init__(self):
        self.url = 'http://192.168.150.233:4267/api/maya/loadTask?id='
       
    def __getTaskName(self,entity_id,entity_type):
        self.url = self.url + entity_id + '&type=' + entity_type 
        result = requests.post(self.url)
       
        if result.text != u"null":
            return result.json()['TASKS']
        else:
            return ""
          
         
          
    def callService(self,entity_id,entity_type):
        return self.__getTaskName(entity_id,entity_type)