# -*- coding: utf-8 -*-
import lib.requests as requests
import conf.apiconfig as conf

class Task(object):
    def __getTask(self,entity_id,entity_type,uid,pid):
        url = conf.taskApi + entity_id + '&entity_type='+ entity_type + '&uid='+ uid + '&project_id=' + pid
        result = requests.post(url)
        if result.text != u"null":
            return result.json()['TASKS']
        else:
            return ""
        
   
    def callService(self,entity_id,entity_type,uid,pid):
        return self.__getTask(entity_id,entity_type,uid,pid)
    
class SingalTask(object):
    def __getSingalTask(self,uid,entity_id,entity_type,taskId,pid):
        url = conf.singalTaskApi + uid + '&project_id='+ pid+'&entity_id=' + entity_id + '&entity_type=' + entity_type + '&task_id='+taskId
        result = requests.post(url)
        if result.text != u"null":
            return result.json()['TASK']
        else:
            return ""   
    
      
    def callService(self,uid,entity_id,entity_type,taskId,pid):
        return self.__getSingalTask(uid,entity_id,entity_type,taskId,pid)    
          
class MyTask(object):
    def __getMyTask(self,uid,pid,entity_type):
        url = conf.myTaskApi + uid + '&project_id=' + pid + '&entity_type=' + entity_type
        result = requests.post(url)
        if result.text != u"null":
            return result.json()['MYTASK']
        else:
            return ""
    
    def callService(self,uid,pid,entity_type):
        return self.__getMyTask(uid,pid,entity_type)
    
    