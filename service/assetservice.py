# -*- coding: utf-8 -*-
import requests 

class Asset(object):
    
    def __init__(self):
        self.url = 'http://192.168.150.233:4267/api/assetList/load?project_id&step_id'
       
    def __getAssetName(self,projectID):
        params  = {'project_id':projectID}
        result = requests.post(self.url,params)
        return result.json()['ASSETS']
         
          
    def callService(self,projectID):
        return self.__getAssetName(projectID)