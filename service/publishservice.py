# -*- coding: utf-8 -*-
import requests 

class Publish(object):
    
    def __init__(self):
        self.url = 'http://192.168.150.233:4267/api/versionAdd/upload?f='
       
    def __upLoad(self,fileName):
        requests.post(self.url + fileName)
          
    def callService(self,fileName):
        return self.__upLoad(fileName)