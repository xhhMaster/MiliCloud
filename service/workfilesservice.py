# -*- coding: utf-8 -*-
import lib.requests as requests
import conf.config as conf

base = conf.read_config(conf.path, 'API', 'baseUrl')

class GetWorkFile(object):
    def __getFile(self,entity_id,entity_type,project_id):
        api = conf.read_config(conf.path, 'API', 'workfileApi')
        url = (base + api + '?entity_id=' + entity_id + 
               '&entity_type=' + entity_type +
               '&project_id=' + project_id)
        s = requests.session()
        result = s.post(url)
        s.keep_alive = False   
        if result.text != u"null":
            return result.json()['VERSION']
        else:
            return ""
          
    def callService(self,entity_id,entity_type,project_id):
        return self.__getFile(entity_id,entity_type,project_id)
    
    
class SelectWorkFile(object):
    def __selectFile(self,entity_id,entity_type,project_id):
        api = conf.read_config(conf.path, 'API', 'selectWorkfileApi')
        url = (base + api + '?entity_id=' + entity_id + 
               '&entity_type=' + entity_type +
               '&project_id=' + project_id)
        s = requests.session()
        result = s.post(url)
        s.keep_alive = False   
        if result.text != u"null":
            return result.json()['VERSION']
        else:
            return ""
          
    def callService(self,entity_id,entity_type,project_id):
        return self.__selectFile(entity_id,entity_type,project_id)