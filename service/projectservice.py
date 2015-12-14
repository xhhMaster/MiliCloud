# -*- coding: utf-8 -*-
import requests 

class Project(object):
    
    def __init__(self):
        self.url = 'http://192.168.150.233:1002/api/projectList/load' 
       
    def __getProjectName(self):
        result=requests.post(self.url)
        #print result.text
        print result.json()['PROJECTS']
          
    def callService(self):
        return self.__getProjectName()