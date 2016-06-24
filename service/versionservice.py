# -*- coding: utf-8 -*-
import lib.requests as requests
import conf.config as conf

base = conf.read_config(conf.path, 'API', 'baseUrl')

class AddVersion(object):
    def __addVersion(self,data):
        api = conf.read_config(conf.path, 'API', 'addVersionApi')
        url = base + api
        s = requests.session()
        result = s.post(url,data)
        s.keep_alive = False     
        return result.text
          
    def callService(self,data):
        return self.__addVersion(data)
    

class GetVersionById(object):
    def __getVersion(self,vid):
        api = conf.read_config(conf.path, 'API', 'getVersionByIdApi')
        url = base + api 
        s = requests.session()
        data = {'id':vid}
        result = s.post(url,data = data)
        s.keep_alive = False   
        if result.text != u"null":
            return result.json()['VERSION']
        else:
            return ""
    
    def callService(self,vid):
        return self.__getVersion(vid)


class GetVersionByName(object):
    def __getVersion(self,vname,pid):
        api = conf.read_config(conf.path, 'API', 'getVersionByNameApi')
        url = base + api + '?versionName=' + vname + '&project_id=' + pid
        s = requests.session()
        result = s.post(url)
        s.keep_alive = False  
        if result.text != u"null":
            return result.json()['VERSION']
        else:
            return ""
    
    def callService(self,vname,pid):
        return self.__getVersion(vname,pid)   

class GetLastVersion(object):
    def __getLastVersion(self,entity_id,entity_type):
        api = conf.read_config(conf.path, 'API', 'getLastVersionApi')
        url = base + api + '?entity_id=' + entity_id + '&entity_type=' + entity_type
        s = requests.session()
        result = s.post(url)
        s.keep_alive = False     
        return result.content
        
    
    def callService(self,entity_id,entity_type):
        return self.__getLastVersion(entity_id,entity_type)
    
class GetReferenceVersion(object):
    def __getReferenceVersion(self,version_id):
        api = conf.read_config(conf.path, 'API', 'getReferenceVersionApi')
        url = base + api + '?version_id=' + version_id 
        s = requests.session()
        result = s.post(url)
        s.keep_alive = False    
        if result.text != u"null":
            return result.json()['ATTACHMENTID']
        else:
            return ""
        
    
    def callService(self,version_id):
        return self.__getReferenceVersion(version_id)
    
class CheckVersion(object):
    def __checkVersion(self,vid):
        api = conf.read_config(conf.path, 'API', 'checkVersionApi1')
        url = base + api
        s = requests.session()
        data = {'id':vid}
        result = s.post(url,data = data)
        s.keep_alive = False 
        if result.text != u"null":
            return result.json()['LASTVERSION']
        else:
            return ""
    
    def callService(self,vid):
        return self.__checkVersion(vid)
    
class LastVersionView(object):
    def __lastVersion(self,vid):
        api = conf.read_config(conf.path, 'API', 'checkVersionApi2')
        url = base + api
        s = requests.session()
        data = {'id':vid}
        result = s.post(url,data = data)
        s.keep_alive = False 
        if result.text != u"null":
            return result.json()['LASTVERSION']
        else:
            return ""
    
    def callService(self,vid):
        return self.__lastVersion(vid)
    
    