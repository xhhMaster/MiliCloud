# -*- coding: utf-8 -*-
import lib.requests as requests
import conf.config as conf

base = conf.read_config(conf.path, 'API', 'baseUrl')


class Shot(object):
    def __getShot(self,uid,project_id,start,length):
        api = conf.read_config(conf.path, 'API', 'getShotApi')
        url = base + api + '?uid=' + uid +  '&project_id=' + project_id + '&start=' + start + '&length=' + length
        s = requests.session()
        result = s.post(url)
        s.keep_alive = False
        if result.text != u"null":
            return result.json()['SHOT']
        else:
            return ""
          
    def callService(self,uid,project_id,start,length):
        return self.__getShot(uid,project_id,start,length)
    
class SingleShot(object):
    def __getSingleShot(self,pid,entityId,entityType):
        api = conf.read_config(conf.path, 'API', 'getSingleShotApi')
        url = base + api + '?project_id=' + pid + '&entity_id=' + entityId + '&entity_type=' + entityType 
        s = requests.session()
        result = s.post(url)
        s.keep_alive = False     
        if result.text != u"null":
            return result.json()['SA']
        else:
            return ""
        
    def callService(self,pid,entityId,entityType):
        return self.__getSingleShot(pid,entityId,entityType)

    
class Sequences(object):
    def __getSequences(self,pid):
        api = conf.read_config(conf.path, 'API', 'sequencesApi')
        url = base + api + pid
        s = requests.session()
        result = s.post(url)
        s.keep_alive = False   
        
        if result.text != u"null":
            return result.json()['SEQUENCENAME']
        else:
            return ""
          
    def callService(self,pid):
        return self.__getSequences(pid)
    
class ShotBySequences(object):
    def __getShotBySequences(self,pid):
        api = conf.read_config(conf.path, 'API', 'shotBySequenceApi')
        url = base + api + '?project_id=' + pid
        s = requests.session()
        result = s.post(url)
        s.keep_alive = False   
        return result.json()
          
    def callService(self,pid):
        return self.__getShotBySequences(pid)
