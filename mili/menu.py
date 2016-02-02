# -*- coding: utf-8 -*-
import maya.cmds as cmds
import pymel.core as pm

class MenuGenerator(object):
     
    def __init__(self):
        self.mainMenuName = u"米粒云"
        self.fileManage = u"文件管理"
        self.publish = u"文件发布"
        self.loader = u"加载预览"
        self.breakdown = u"场景拆分"
        self.mainMenu = ''
        cmds.scriptJob(event = ["NewSceneOpened",self.menuGenerator])
        
    #创建Maya主页面菜单按钮
    def createMenu(self):
        self.mainMenu = cmds.menu('MayaMiliCloud',parent = pm.melGlobals["gMainWindow"],label = self.mainMenuName,tearOff = 1)
        cmds.menuItem(parent = self.mainMenu,label = u'登录米粒云',c = self.loginDlg)
    
    #打开文件管理窗口
    def showFileManageDlg(self,*args):
        import ui.selectarea_ui as selectarea_ui
        selectarea_ui.SelectedWorkFiles_UI(self.userID)
    
    #打开发布窗口
    def publishDlg(self,*args):
        import setup.setuppublish as setuppublish
        self.Widget = setuppublish.Widget(self.userID)
        self.Widget.show()
    
    
    def loginDlg(self,*args):
        import setup.setuplogin as setuplogin
        self.Widget = setuplogin.Widget()
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
        
    def updateMenu(self,userName,userID):
        self.userID = userID
        cmds.deleteUI('MayaMiliCloud',menu = True)
        self.mainMenu = cmds.menu('MayaMiliCloud',parent = pm.melGlobals["gMainWindow"],label = self.mainMenuName,tearOff = 1)
        cmds.menuItem(parent = self.mainMenu,label = u'欢迎，'+ userName)
        cmds.menuItem(parent = self.mainMenu,label = self.fileManage,c = self.showFileManageDlg)
        cmds.menuItem(parent = self.mainMenu,label = self.publish,c = self.publishDlg)  
        cmds.menuItem(parent = self.mainMenu,label = self.loader)
        cmds.menuItem(parent = self.mainMenu,label = self.breakdown)