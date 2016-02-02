# -*- coding: utf-8 -*-
import lib.requests as requests

class Project(object):
    
    def __init__(self):
        self.url = 'http://192.168.150.233:4267/api/projectList/load' 
       
    def __getProjectName(self):
        result=requests.post(self.url)
        if result.text != u"null":
            return result.json()['PROJECTS']
        else:
            return ""
         
    def __getProjectInfo(self,pid):
        self.url = 'http://192.168.150.233:4267/api/maya/selectProject?project_id='
        result=requests.post(self.url + pid)
        if result.text != u"null":
            return result.json()['PROJECT']
        else:
            return ""
     
    def callService(self):
        return self.__getProjectName()
    
    def callInfoService(self,pid):
        return self.__getProjectInfo(pid)