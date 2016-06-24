# -*- coding: utf-8 -*-
import maya.cmds as cmds
import pymel.core as pm
import os
import conf.path as path
from PySide import QtGui
from common.uicommon import Msg


class MenuGenerator(object):
    def __init__(self):
        self.mainMenuName = u"米粒云"
        self.loginName = u'登录米粒云'
        self.fileManage = u"文件管理"
        self.selectProject = u"请选择项目"
        self.publish = u"文件发布"
        self.loader = u"引用文件"
        self.breakdown = u"引用更新"
        self.mainMenu = ''
        self.path = path.xmlForFile
        cmds.scriptJob(event = ["NewSceneOpened",self.menuGenerator])
        
    #创建Maya主页面菜单按钮
    def createMenu(self):
        self.mainMenu = cmds.menu('MayaMiliCloud',parent = pm.melGlobals["gMainWindow"],label = self.mainMenuName,tearOff = 1)
        cmds.menuItem(parent = self.mainMenu,label = self.loginName,c = self.loginDlg)
    
    #打开文件管理窗口
    def showFileManageDlg(self,*args):
        if os.path.exists(self.path):
            import launch.selectworkfile as selectworkfile
            reload(selectworkfile)
            import common.xmlcommon as xml
            reload(xml)
            x = xml.readXmlForFile(self.path)
            self.Widget = selectworkfile.Widget(str(self.userID),str(x['project_id']),str(x['entity_id']),
                                                str(x['entity_type']),str(x['task_id']),self.useName)
            self.Widget.show() 
        else:
            import launch.selecttask as selecttask
            reload(selecttask)
            self.Widget = selecttask.Widget(self.pid,self.userID,self.useName)
            self.Widget.show()  
    
    #打开发布窗口
    def publishDlg(self,*args):
        import launch.publish as publish
        reload(publish)
        self.Widget = publish.Widget(self.userID)
        self.Widget.show()
    
    
    def projectDlg(self,*args):
        import launch.selectproject as selectproject
        reload(selectproject)
        self.Widget = selectproject.Widget(self.userID,self.useName)
        self.Widget.show() 
            
    
    def loginDlg(self,*args):
        import launch.login as login
        reload(login)
        self.Widget = login.Widget()
        self.Widget.show()
    
    def loginOutDlg(self,*args):
        cmds.deleteUI('MayaMiliCloud',menu = True)
        self.mainMenu = cmds.menu('MayaMiliCloud',parent = pm.melGlobals["gMainWindow"],label = self.mainMenuName,tearOff = 1)
        cmds.menuItem(parent = self.mainMenu,label = u'登录米粒云',c = self.loginDlg)
    
    def loaderDlg(self,*args):
        import launch.loader as loader
        reload(loader)
        self.Widget = loader.Widget(self.userID,self.pid) 
        self.Widget.show()
        
    def aboutDlg(self,*args):
        txt = u'当前登录人是:' + self.useName +'              '
        self.about = QtGui.QMessageBox()
        loginOut = self.about.addButton(u'注销',QtGui.QMessageBox.AcceptRole)
        loginOut.clicked.connect(self.loginOutDlg)
        self.about.setIcon(QtGui.QMessageBox.NoIcon)
        Msg().showDialog(self.about,u'关于',txt,'')
    
    def msgDlg(self,*args):
        txt = u'你没有查看项目的权限，请联系相应负责人'
        self.about = QtGui.QMessageBox()
        self.about.setIcon(QtGui.QMessageBox.NoIcon)
        Msg().showDialog(self.about,u'提示',txt,'')
    
    
    def breakdownDlg(self,*args):
        import launch.breakdown as breakdown
        reload(breakdown)
        self.Widget = breakdown.Widget(self.userID,self.pid)
        self.Widget.show()
       
         
    #菜单生成器  
    def menuGenerator(self):
        if self.mainMenu != '':  
            menuList = cmds.window(pm.melGlobals["gMainWindow"],q = 1,ma = 1)
            menuName = self.mainMenu.split('|')[1]
            if not menuName in menuList:
                self.createMenu()
        else:
            self.createMenu()
        
    def updateMenu(self,userName,userID,pid,editRole):
        self.pid = pid
        self.useName = userName
        self.userID = userID
        if os.path.exists(self.path):
            os.remove(self.path)
        cmds.deleteUI('MayaMiliCloud',menu = True)
        self.mainMenu = cmds.menu('MayaMiliCloud',parent = pm.melGlobals["gMainWindow"],label = self.mainMenuName,tearOff = 1)
        cmds.menuItem(parent = self.mainMenu,label = u'欢迎，'+ self.useName,c = self.aboutDlg)
        cmds.menuItem(parent = self.mainMenu,label = self.fileManage,c = self.showFileManageDlg)
        if editRole == 1:
            cmds.menuItem(parent = self.mainMenu,label = self.publish,c = self.publishDlg)  
        cmds.menuItem(parent = self.mainMenu,label = self.loader,c = self.loaderDlg)
        cmds.menuItem(parent = self.mainMenu,label = self.breakdown,c = self.breakdownDlg)
        self.showFileManageDlg()
    
    def unselectProjectMenu(self,userName,userID):
        self.useName = userName
        self.userID = userID
        if os.path.exists(self.path):
            os.remove(self.path)
        cmds.deleteUI('MayaMiliCloud',menu = True)
        self.mainMenu = cmds.menu('MayaMiliCloud',parent = pm.melGlobals["gMainWindow"],label = self.mainMenuName,tearOff = 1)
        cmds.menuItem(parent = self.mainMenu,label = u'欢迎，'+ self.useName,c = self.aboutDlg)
        cmds.menuItem(parent = self.mainMenu,label = self.selectProject,c = self.projectDlg) 
    
    def unRoleMenu(self,userName,userID):
        self.userID = userID
        if os.path.exists(self.path):
            os.remove(self.path)
        cmds.deleteUI('MayaMiliCloud',menu = True)
        self.mainMenu = cmds.menu('MayaMiliCloud',parent = pm.melGlobals["gMainWindow"],label = self.mainMenuName,tearOff = 1)
        cmds.menuItem(parent = self.mainMenu,label = u'欢迎，'+ userName,c = self.aboutDlg)
        cmds.menuItem(parent = self.mainMenu,label = u'权限不足',c = self.msgDlg)               