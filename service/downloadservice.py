# -*- coding: utf-8 -*-
import lib.requests as requests

class DownLoad(object):
    
    def __init__(self):
        self.url = 'http://192.168.150.233:4267/App_SaveData/tmp/'
    
   
    def __download(self,directory,fullfileName):
        self.url = self.url+directory
        r = requests.get(self.url)
        with open(fullfileName, "wb") as code:
            code.write(r.content)      

        
    def callService(self,directory,fullfileName):
        return self.__download(directory,fullfileName)