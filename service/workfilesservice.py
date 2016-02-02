# -*- coding: utf-8 -*-
import lib.requests as requests
import conf.apiconfig as conf

class WorkFile(object):
    def __getFile(self,entity_id,entity_type):
        url = conf.workfileApi + entity_id + '&entity_type=' + entity_type 
        result = requests.post(url)
        if result.text != u"null":
            return result.json()['VERSION']
        else:
            return ""
          
    def callService(self,entity_id,entity_type):
        return self.__getFile(entity_id,entity_type)