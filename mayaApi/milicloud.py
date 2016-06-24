# -*- coding: utf-8 -*-
from mayaService import mayaservice

reload(mayaservice)

class miliCloud(object):
    def __init__(self,usename,password): 
        self.login(usename,password)
        
    def login(self,usename,password):
        result =  mayaservice.Login().callService(usename,password)  
        if result != "error":
            self.userName = result[0][u'name']
            self.uid = result[0][u'id']
        else:
            self.uid = ''
    
    def find(self,tableName,filters,fields):
        return mayaservice.Find().callService(tableName, filters, fields)  
    
    def customFind(self,tableName,filters,fields):
        return mayaservice.customFind().callService(tableName, filters, fields)  
    
    def update(self,tableName,filters,fields):
        if self.uid != '':
            return mayaservice.Update().callService(tableName,filters,fields)
        else:
            print u'请重新登录'
        
    def insert(self,tableName,fields):
        if self.uid != '':
            return mayaservice.Insert().callService(tableName, fields)
        else:
            print u'请重新登录'
    
    def delete(self,tableName,filters,fields):
        if self.uid != '':
            return mayaservice.Delete().callService(tableName, filters, fields)
        else:
            print u'请重新登录'

    def timeLog(self,pid):
        if self.uid != '':
            return mayaservice.TimeLog().callService(pid)
        else:
            print u'请重新登录'
    
    def ticket(self,pid):
        if self.uid != '':
            return mayaservice.Ticket().callService(pid)
        else:
            print u'请重新登录'   
    
    
    data = {}
    data['login'] 
    data['salted_password'] 
    data['firstname'] 
    data['lastname']
    data['email'] 
    data['description'] 
    data['group_id'] 
    data['project_id'] 
    data['user_id'] 
    data['created_by_id'] 
    data['updated_by_id'] 
    data['reference_version_id'] 
    def addUser(self,data):
        if self.uid != '':
            return mayaservice.AddUser().callService(data)
        else:
            print u'请重新登录' 