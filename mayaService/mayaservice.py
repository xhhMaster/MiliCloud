# -*- coding: utf-8 -*-
import lib.requests as requests
import json 

baseUrl = 'http://192.168.150.235:4267/api/'

class Login(object):
    def __getUserInfo(self,userName,password):
        url = baseUrl + 'login'
        data = {'name': userName,'password':password}
        result=requests.post(url,data = data)
        if  result.json() != "error":
            return result.json()['Table']
        else:
            return "error"
     
    def callService(self,userName,password):
        return self.__getUserInfo(userName,password)

class Find(object):
    def __getData(self,tableName,filters,fields):
        url = baseUrl + 'mayaExpansion/find'
        paramData = {'table':tableName,'filters':json.dumps(filters),'selFields':fields}
        result = requests.post(url,data = paramData)
        if result.text != '[]':
            return result.json()
        else:
            return ""
          
    def callService(self,tableName,filters,fields):
        return self.__getData(tableName,filters,fields)

class customFind(object):
    def __getData(self,tableName,filters,fields):
        url = baseUrl + 'mayaExpansion/customFind'
        paramData = {'table':tableName,'filters':json.dumps(filters),'selFields':fields}
        result = requests.post(url,data = paramData)
        print result.text
        if result.text != '[]':
            return result.json()
        else:
            return ""
          
    def callService(self,tableName,filters,fields):
        return self.__getData(tableName,filters,fields)
    
class Update(object):
    def __updateData(self,tableName,filters,fields):
        url = baseUrl + 'mayaExpansion/update'
        paramData = {'table':tableName,'filters':json.dumps(filters),'updFields':json.dumps(fields)}
        result = requests.post(url,data = paramData)
        return result.text
          
    def callService(self,tableName,filters,fields):
        return self.__updateData(tableName,filters,fields)

class Insert(object):
    def __addData(self,tableName,fields):
        url = baseUrl + 'mayaExpansion/insert'
        paramData = {'table':tableName,'updFields':json.dumps(fields)}
        result = requests.post(url,data = paramData)
        return result.text
          
    def callService(self,tableName,fields):
        return self.__addData(tableName,fields)
  
class Delete(object):
    def __deleteData(self,tableName,filters,fields):
        url = baseUrl + 'mayaExpansion/delete'
        paramData = {'table':tableName,'filters':json.dumps(filters),'updFields':json.dumps(fields)}
        result = requests.post(url,data = paramData)
        return result.text
          
    def callService(self,tableName,filters,fields):
        return self.__deleteData(tableName,filters,fields)
    
class TimeLog(object):
    def __timeLog(self,pid):
        url = baseUrl + 'timeLog/loadData'
        paramData = {'currentEntityInfo':{'ID':pid,'type':'project_id'}}
        result = requests.post(url,data = paramData)
        return result.json()['TMP']
          
    def callService(self,pid):
        return self.__timeLog(pid)
    
class Ticket(object):
    def __ticket(self,pid):
        url = baseUrl + 'ticket/loadData'
        paramData = {'currentEntityInfo':{'ID':pid,'type':'project_id'}}
        result = requests.post(url,data = paramData)
        return result.json()['TMP']
          
    def callService(self,pid):
        return self.__ticket(pid)

class AddUser(object):
    def __add(self,data):
        url = baseUrl + 'userAdd/save'
        s = requests.session()
        result = s.post(url,data)
        s.keep_alive = False     
        return result.text
    
    def callService(self,data):
        return self.__add(data)