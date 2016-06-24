# -*- coding: utf-8 -*-
import lib.requests as requests
import conf.config as conf


class Login(object):
    def __getUserInfo(self,userName,password):
        base = conf.read_config(conf.path, 'API', 'baseUrl')
        api = conf.read_config(conf.path, 'API', 'loginApi')
        url = base + api 
        data = {'name': userName,'password':password}
        s = requests.session()
        result = s.post(url,data = data)
        s.keep_alive = False  
        if  result.json() != "error":
            return result.json()['Table']
        else:
            return "error"
     
    def callService(self,userName,password):
        return self.__getUserInfo(userName,password)

class Competence(object):
    def __getCompetence(self,uid):
        base = conf.read_config(conf.path, 'API', 'baseUrl')
        api = conf.read_config(conf.path, 'API', 'getUserRule')
        url = base + api
        s = requests.session()
        idData = { 'ID': uid, 'VALUE': '5' };
        result = s.post(url,data = idData)
        s.keep_alive = False 
        if result.text != u"null":
            return result.json()['AUTH']
        else:
            return ""
        
    
    
    def callService(self,uid):
        return self.__getCompetence(uid)