# -*- coding: utf-8 -*-
import lib.requests as requests
import conf.apiconfig as conf

class Asset(object):
    def __getAsset(self,projectID):
        result = requests.post(conf.assetApi + projectID)
        if result.text != u"null":
            return result.json()['ASSETS']
        else:
            return ""
    
   
    def callService(self,projectID):
        return self.__getAsset(projectID)
    
class SingalAsset(object):
    def __getSingalAsset(self,pid,entityId,entityType):
        url = conf.singalAssetApi + pid + '&entity_id=' + entityId + '&entity_type=' + entityType 
        result = requests.post(url)
        if result.text != u"null":
            return result.json()['SA']
        else:
            return ""
        
    def callService(self,pid,entityId,entityType):
        return self.__getSingalAsset(pid,entityId,entityType)