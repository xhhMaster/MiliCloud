# -*- coding: utf-8 -*-
import maya.cmds as cmds
import pymel.core as pm

class MenuGenerator(object):
     
    def __init__(self):
        self.mainMenuName = u"米粒云"
        self.miliCloudFileManage = u"米粒云文件管理"
        self.fileManage = u"文件管理"
        self.saveAs = u"保存"
        self.versionManage = u"版本管理"
        self.publish = u"发布"
        self.loader = u"加载"
        self.breakdown = u"场景拆分"
        self.snapshotManage = u"快照备份管理"
        self.snapshot = u"快照备份"
        self.history = u"历史浏览"
        self.settingLauguage = u"切换英文菜单"
        self.flag = True
        if cmds.window(self.mainMenuName,exists=True):
            cmds.deleteUI(self.windowName)
        else:
            self.createMenu()
        
    def createMenu(self):
        #gMainWindow = mel.eval('$temp1 = $gMainWindow')   
        self.mainMenu = cmds.menu(parent = pm.melGlobals["gMainWindow"],label = self.mainMenuName)
               
        miliCloudFileManage = cmds.menuItem(parent = self.mainMenu,label = self.miliCloudFileManage,subMenu = True)
        fileManage = cmds.menuItem(parent = miliCloudFileManage,label = self.fileManage,c = self.showFileManageDlg)
        saveAs = cmds.menuItem(parent = miliCloudFileManage,label = self.saveAs)
        versionManage = cmds.menuItem(parent = miliCloudFileManage,label = self.versionManage)  
        
        publish = cmds.menuItem(parent = self.mainMenu,label = self.publish,c = self.publishDlg)
        loader = cmds.menuItem(parent = self.mainMenu,label = self.loader)
        breakdown = cmds.menuItem(parent = self.mainMenu,label = self.breakdown)
        snapshotManage = cmds.menuItem(parent = self.mainMenu,label = self.snapshotManage,subMenu = True)
        snapshot = cmds.menuItem(parent = snapshotManage,label = self.snapshot)
        history = cmds.menuItem(parent = snapshotManage,label = self.history)
        settingLauguage = cmds.menuItem(parent = self.mainMenu,label = self.settingLauguage,c = self.settingMenuLanguage)
    
    def showFileManageDlg(self,*args):
        import ui.selectarea_ui as selectarea_ui
        selectarea_ui.SelectedWorkFiles_UI()
        
    def publishDlg(self,*args):
        import setup.setuppublish as setuppublish
        reload(setuppublish)
        self.Widget = setuppublish.Widget()
        self.Widget.show()
        
    def settingMenuLanguage(self,*args):
        if(self.flag):
            cmds.deleteUI(self.mainMenu,menu = True)
            self.mainMenuName = "MiliCloud"
            self.miliCloudFileManage = "MiliCloud File Manage"
            self.fileManage = "File Manage"
            self.saveAs = "Save As"
            self.versionManage = "Version Control"
            self.publish = "Publish"
            self.loader = "Loader"
            self.breakdown = "Breakdown"
            self.snapshotManage = "Snapshot Manage"
            self.snapshot = "Snapshot"
            self.history = "History"
            self.settingLauguage = "Switch Chinese menu"
            self.flag = False
            self.createMenu()            
        else:
            cmds.deleteUI(self.mainMenu,menu = True)
            self.mainMenuName = u"米粒云"
            self.miliCloudFileManage = u"米粒云文件管理"
            self.fileManage = u"文件管理"
            self.saveAs = u"保存"
            self.versionManage = u"版本管理"
            self.publish = u"发布"
            self.loader = u"加载"
            self.breakdown = u"场景拆分"
            self.snapshotManage = u"快照备份管理"
            self.snapshot = u"快照备份"
            self.history = u"历史浏览"
            self.settingLauguage = u"切换英文菜单"
            self.flag = True
            self.createMenu()     
        