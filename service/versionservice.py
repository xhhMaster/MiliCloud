# -*- coding: utf-8 -*-
import lib.requests as requests
import conf.apiconfig as conf

class AddVersion(object):
    def __UploadData(self,data):
        result = requests.post(conf.addVersionApi,data)
        return result.text
          
    def callService(self,data):
        return self.__UploadData(data)