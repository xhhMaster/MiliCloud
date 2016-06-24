# -*- coding: utf-8 -*-
import lib.requests as requests
import conf.config as conf

base = conf.read_config(conf.path, 'API', 'baseUrl')


class Task(object):
    def __getTask(self,entity_id,entity_type,uid,pid):
        api = conf.read_config(conf.path, 'API', 'getTaskApi')
        url = (base + api + '?entity_id=' + entity_id + 
            '&entity_type='+ entity_type + 
            '&uid='+ uid + 
            '&project_id=' + pid )
        s = requests.Session()
        result = requests.post(url)
        s.keep_alive = False     
        if result.text != u"null":
            return result.json()['TASKS']
        else:
            return ""
        
    def callService(self,entity_id,entity_type,uid,pid):
        return self.__getTask(entity_id,entity_type,uid,pid)
    
class SingleTask(object):
    def __getSingleTask(self,uid,taskId,stepId):
        api = conf.read_config(conf.path, 'API', 'getSingleTaskApi')
        url = (base + api + '?uid=' + uid + '&task_id=' + taskId + '&step_id=' + stepId)
        s = requests.session()
        result = s.post(url)
        s.keep_alive = False   
        if result.text != u"null":
            return result.json()['TASK']
        else:
            return ""   
    
    def callService(self,uid,taskId,stepId):
        return self.__getSingleTask(uid,taskId,stepId)    
          
class TaskStep(object):
    def __getTaskStep(self,uid,pid,tableName):
        api = conf.read_config(conf.path, 'API', 'getTaskStepApi')
        url = base + api + '?user_id=' +  uid  + '&project_id='+ pid
        s = requests.session()
        result = s.post(url)
        s.keep_alive = False   
        return result.json()[tableName]
          
    def callService(self,uid,pid,tableName):
        return self.__getTaskStep(uid,pid,tableName)
    