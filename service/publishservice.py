# -*- coding: utf-8 -*-
import lib.requests as requests
import conf.apiconfig as conf

class Publish(object):
    def __upLoad(self,fileName,directory):
        url = conf.publishApi + directory
        files = {'file': open(fileName, 'rb')}
        requests.post(url, files=files)
        
          
    def callService(self,fileName,directory):
        return self.__upLoad(fileName,directory)
    
