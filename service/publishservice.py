# -*- coding: utf-8 -*-
import lib.requests as requests

class Publish(object):
    
    def __init__(self):
        self.url = 'http://192.168.150.233:4267/api/versionAdd/upload?f='
       
    def __upLoad(self,fileName,directory):
            self.url = self.url + directory
            files = {'file': open(fileName, 'rb')}
            result = requests.post(self.url, files=files)
            print result.text
        
          
    def callService(self,fileName,directory):
        return self.__upLoad(fileName,directory)
    
