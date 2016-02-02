# -*- coding: utf-8 -*-
import lib.requests as requests


class AddVersion(object):
    
    def __init__(self):
        self.url = 'http://192.168.150.233:4267/api/versionAdd/mayaInsert'
       
    def __UploadData(self,data):
        result = requests.post(self.url,data)
        return result.text
          
    def callService(self,data):
        return self.__UploadData(data)