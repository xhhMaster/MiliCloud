# -*- coding: utf-8 -*-
import lib.requests as requests

class Asset(object):
    
    def __init__(self):
        self.url = 'http://192.168.150.233:4267/api/assetList/load?step_id&related_shot_id&project_id='
       
    def __getAssetName(self,projectID):
        result = requests.post(self.url + projectID)
        
        if result.text != u"null":
            return result.json()['ASSETS']
        else:
            return ""
    
    
    def __getAssetInfo(self,pid,entityId,entityType):
        self.url = 'http://192.168.150.233:4267/api/maya/selectShotAsset?project_id='
        self.url = self.url + pid + '&entity_id=' + entityId + '&entity_type=' + entityType 
        result = requests.post(self.url)
        if result.text != u"null":
            return result.json()['SA']
        else:
            return ""
    
         
    def callService(self,projectID):
        return self.__getAssetName(projectID)
    
    
    def callInfoService(self,pid,entityId,entityType):
        return self.__getShotInfo(pid,entityId,entityType)