# -*- coding: utf-8 -*-
import core.requests as requests

class Asset(object):
    
    def __init__(self):
        self.url = 'http://192.168.150.233:4267/api/assetList/load?step_id&project_id='
       
    def __getAssetName(self,projectID):
        result = requests.post(self.url + projectID)
        
        if result.text != u"null":
            return result.json()['ASSETS']
        else:
            return ""
          
    def callService(self,projectID):
        return self.__getAssetName(projectID)