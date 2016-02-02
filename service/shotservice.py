# -*- coding: utf-8 -*-
import lib.requests as requests
import conf.apiconfig as conf

class Shot(object):
    def __getShot(self,projectID):
        result = requests.post(conf.shotApi+projectID)
        if result.text != u"null":
            return result.json()['SHOTS']
        else:
            return ""
          
    def callService(self,projectID):
        return self.__getShot(projectID)
    
class SingalShot(object):
    def __getSingalShot(self,pid,entityId,entityType):
        url = conf.singalShotApi + pid + '&entity_id=' + entityId + '&entity_type=' + entityType 
        result = requests.post(url)
        if result.text != u"null":
            return result.json()['SA']
        else:
            return ""
        
    
    def callService(self,pid,entityId,entityType):
        return self.__getSingalShot(pid,entityId,entityType)