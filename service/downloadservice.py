# -*- coding: utf-8 -*-
import lib.requests as requests

class DownLoad(object):
    
    def __init__(self):
        self.url = 'http://192.168.150.233:4267/App_SaveData/tmp/version/'
   
    def __download(self,fileName,directory):
        self.url = self.url + directory
        r = requests.get(self.url) 
        with open(fileName, "wb") as code:
            code.write(r.content)      
        
        
    def callService(self,fileName,directory):
        return self.__download(fileName,directory)