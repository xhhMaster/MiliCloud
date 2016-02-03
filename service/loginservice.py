# -*- coding: utf-8 -*-
import lib.requests as requests
import conf.apiconfig as conf

class Login(object):
    def __getUserInfo(self,userName,password):
        url = conf.loginApi + '?name=' + userName + '&password=' + password
        result=requests.post(url)
        print result.url,result.text
        if  result.json() != "error":
            return result.json()['Table']
        else:
            return "error"
     
    def callService(self,userName,password):
        return self.__getUserInfo(userName,password)
    