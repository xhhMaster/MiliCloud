# -*- coding: utf-8 -*-
import requests

class Task(object):
    
    def __init__(self):
        self.url = 'http://192.168.150.233:4267/api/taskList/load?projectId='
       
    def __getTaskName(self,projectID):
        projectID = '%d'%projectID
        result = requests.post(self.url + projectID)
        return result.json()['Table']
         
          
    def callService(self,projectID):
        return self.__getTaskName(projectID)