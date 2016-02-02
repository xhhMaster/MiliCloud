# -*- coding: utf-8 -*-
import lib.requests as requests

class Task(object):
    
    def __init__(self):
        self.url = 'http://192.168.150.233:4267/api/maya/loadTask?entity_id='
       
    def __getTaskName(self,entity_id,entity_type,uid,pid):
        self.url = self.url + entity_id + '&entity_type='+ entity_type + '&uid='+ uid + '&project_id=' + pid
        result = requests.post(self.url)
        if result.text != u"null":
            return result.json()['TASKS']
        else:
            return ""
        
    def __getTaskInfo(self,uid,entity_id,entity_type,taskId,pid):
        self.url = 'http://192.168.150.233:4267/api/maya/selectTask?uid='
        self.url = self.url + uid + '&project_id='+ pid+'&entity_id=' + entity_id + '&entity_type=' + entity_type + '&task_id='+taskId
        result = requests.post(self.url)
        if result.text != u"null":
            return result.json()['TASK']
        else:
            return ""     
        
    def callService(self,entity_id,entity_type,uid,pid):
        return self.__getTaskName(entity_id,entity_type,uid,pid)
    
    
    def callInfoService(self,uid,entity_id,entity_type,taskId,pid):
        return self.__getTaskInfo(uid,entity_id,entity_type,taskId,pid)

class MyTask(object):
    def __init__(self):
        self.url = 'http://192.168.150.233:4267/api/maya/getMyTask?uid='
       
    def __getMyTask(self,uid,pid,entity_type):
        self.url = self.url + uid + '&project_id=' + pid + '&entity_type=' + entity_type
        result = requests.post(self.url)
        if result.text != u"null":
            return result.json()['MYTASK']
        else:
            return ""
    
    def callService(self,uid,pid,entity_type):
        return self.__getMyTask(uid,pid,entity_type)
    
    