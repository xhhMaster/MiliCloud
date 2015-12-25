# -*- coding: utf-8 -*-
import core.requests as requests

class Project(object):
    
    def __init__(self):
        self.url = 'http://192.168.150.233:4267/api/projectList/load' 
       
    def __getProjectName(self):
        result=requests.post(self.url)
        if result.text != u"null":
            return result.json()['PROJECTS']
        else:
            return ""
          
    def callService(self):
        return self.__getProjectName()