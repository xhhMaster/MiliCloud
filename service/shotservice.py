# -*- coding: utf-8 -*-
import core.requests as requests

class Shot(object):
    
    def __init__(self):
        self.url = 'http://192.168.150.233:4267/api/shotList/load?step_id&project_id='
       
    def __getShotName(self,projectID):
        result = requests.post(self.url+projectID)
        if result.text != u"null":
            return result.json()['SHOTS']
        else:
            return ""
          
    def callService(self,projectID):
        return self.__getShotName(projectID)