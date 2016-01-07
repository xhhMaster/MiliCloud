# -*- coding: utf-8 -*-
import maya.cmds as cmds
import os,sys
from mili.menu import MenuGenerator
    
class MiliCloudToolsInstall(object):
    def __init__(self):
        self.windowName = u"米粒云安装界面"
        cmds.scriptJob(event = ["NewSceneOpened",self.miliCloud])
      
    #安装错误
    def install_Error(self):
        errorMsg = u"错误：找不到米粒云安装目录.\n\n请通过\'浏览\'按钮查找."   
        title = u"米粒云"
        cancelBtn = u"取消"
        browseBtn = u"浏览"
        
        if cmds.window(self.windowName,exists=True):
            cmds.deleteUI(self.windowName)
            
        window = cmds.window(self.windowName, title= title, w = 300, h = 110, titleBarMenu = False,sizeable = False)
        
        #设置窗口大小
        #mainLayout = cmds.columnLayout(w=300,h=110)
        formLayout = cmds.formLayout(w=300,h=110)
        
        #错误提示
        text = cmds.text(label = errorMsg,w =300)
        
        #创建按钮
        cancelButton = cmds.button(label = cancelBtn,w = 140,h = 35,c = self.install_Cancel)
        browseButton = cmds.button(label = browseBtn,w = 140,h = 35,c = self.install_Browse)
        
        #设置窗体布局
        cmds.formLayout(formLayout,edit = True,af = [(text,'left',10),(text,'top',10)])
        cmds.formLayout(formLayout,edit = True,af = [(cancelButton,'left',5),(cancelButton,'bottom',5)])
        cmds.formLayout(formLayout,edit = True,af = [(browseButton,'right',5),(browseButton,'bottom',5)])
        
        #显示窗口
        cmds.showWindow(window)
        cmds.window(window,edit = True,w = 300,h = 110)
        
    
    
    #浏览     
    
    def install_Browse(self,*args):
        
        #self.windowName = u"米粒云安装界面"
        warningMsg = u"选中的目录不是米粒云的目录.请重新选择！"
        
        miliCloudDir =  cmds.fileDialog2(dialogStyle = 2,fileMode = 3)[0]
        
        #确认米粒云的目录路径
        if  miliCloudDir.rpartition("/")[2] != "MiliCloud":
            cmds.warning(warningMsg)
        else:
            cmds.deleteUI(self.windowName)
            
        #创建包含米粒云目录路径的文本文件
        path = cmds.internalVar(upd = True) + "miliCloud.txt"
        
        f = open(path,'w')
        f.write(miliCloudDir)
        f.close()
        
        #执行
        MenuGenerator()   
        
    
    #取消    
    
    def install_Cancel(self,*args):  
        cmds.deleteUI(self.windowName) 
  
    #执行
    
    def miliCloud(self):
        path = cmds.internalVar(upd = True) + "miliCloud.txt"       
      
        if os.path.exists(path):
            f = open(path,'r')
            miliCloudDir = f.readline()
           
            path = miliCloudDir+"/Tools/Scripts/"
    
            if os.path.exists(path):
                if not path in sys.path:
                    sys.path.append(path)
            else:
                MenuGenerator()
        else:            
            self.install_Error()          

        