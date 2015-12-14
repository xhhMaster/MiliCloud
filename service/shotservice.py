# -*- coding: utf-8 -*-
import requests 

class Shot(object):
    
    def __init__(self):
        self.url = 'http://192.168.150.233:4267/api/shotList/load?project_id&step_id'
       
    def __getShotName(self,projectID):
        params  = {'project_id':projectID}
        result = requests.post(self.url,params)
        return result.json()['SHOTS']
          
    def callService(self,projectID):
        return self.__getShotName(projectID)