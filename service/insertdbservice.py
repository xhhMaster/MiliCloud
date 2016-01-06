# -*- coding: utf-8 -*-
import lib.requests as requests


class InsertVersionDB(object):
    
    def __init__(self):
        self.url = 'http://192.168.150.233:4267/api/versionAdd/mayaInsert'
       
    def __UploadData(self,data):
        requests.post(self.url,data)
          
    def callService(self,data):
        return self.__UploadData(data)