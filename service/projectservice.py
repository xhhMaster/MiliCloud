# -*- coding: utf-8 -*-
import lib.requests as requests
import conf.config as conf

base = conf.read_config(conf.path, 'API', 'baseUrl')

class Project(object):
    def __getProject(self,uid):
        api = conf.read_config(conf.path, 'API', 'getProjectApi')
        url = base + api + '?user_id=' + uid
        s = requests.session()
        result = s.post(url)
        s.keep_alive = False
        if result.text != u"null":
            return result.json()['PROJECT']
        else:
            return ""
         
    def callService(self,uid):
        return self.__getProject(uid)
    
class SingleProject(object):
    def __getSingleProject(self,pid):
        api = conf.read_config(conf.path, 'API', 'getSingleProjectApi')
        url = base + api + '?project_id=' + pid
        s = requests.session()
        result = s.post(url)
        s.keep_alive = False   
        if result.text != u"null":
            return result.json()['PROJECT']
        else:
            return ""
        
    def callService(self,pid):
        return self.__getSingleProject(pid)
    