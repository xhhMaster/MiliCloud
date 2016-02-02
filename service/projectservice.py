# -*- coding: utf-8 -*-
import lib.requests as requests
import conf.apiconfig as conf

class Project(object):
    def __getProject(self):
        result=requests.post(conf.projectApi)
        if result.text != u"null":
            return result.json()['PROJECTS']
        else:
            return ""
         
    def callService(self):
        return self.__getProject()
    
class SingalProject(object):
    def __getSingalProject(self,pid):
        result=requests.post(conf.singalProjectApi + pid)
        if result.text != u"null":
            return result.json()['PROJECT']
        else:
            return ""
        
    def callService(self,pid):
        return self.__getSingalProject(pid)