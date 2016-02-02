# -*- coding: utf-8 -*-
import lib.requests as requests

class Shot(object):
    
    def __init__(self):
        self.url = 'http://192.168.150.233:4267/api/shotList/load?step_id&related_asset_id&project_id='
       
    def __getShotName(self,projectID):
        result = requests.post(self.url+projectID)
        if result.text != u"null":
            return result.json()['SHOTS']
        else:
            return ""
    
    def __getShotInfo(self,pid,entityId,entityType):
        self.url = 'http://192.168.150.233:4267/api/maya/selectShotAsset?project_id='
        self.url = self.url + pid + '&entity_id=' + entityId + '&entity_type=' + entityType 
        result = requests.post(self.url)
        if result.text != u"null":
            return result.json()['SA']
        else:
            return ""
          
    def callService(self,projectID):
        return self.__getShotName(projectID)
    
    def callInfoService(self,pid,entityId,entityType):
        return self.__getShotInfo(pid,entityId,entityType)