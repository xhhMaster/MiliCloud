# -*- coding: utf-8 -*-
import lib.requests as requests

class Login(object):
    
    def __init__(self):
        self.url = 'http://192.168.150.233:4267/api/login' 
       
    def __getUserInfo(self,userName,password):
        self.url = self.url + '?name=' + userName + '&password=' + password
        result=requests.post(self.url)
        if  result.json() != "error":
            return result.json()['Table']
        else:
            return "error"
     
    def callService(self,userName,password):
        return self.__getUserInfo(userName,password)
    