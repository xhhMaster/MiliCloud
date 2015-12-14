# -*- coding: utf-8 -*-
from PySide import QtGui
from ui.selectworkfiles_ui import Ui_Widget

class Widget(QtGui.QWidget, Ui_Widget):
    def __init__(self,content,parent=None):
        super(Widget,self).__init__(parent)
        self.setupUi(self)
        self.getShotAndAssetInfo()
        self.getTaskInfo()
        self.projectNameEdit.setText(content)

        self.createBtn.clicked.connect(self.createClicked)
        self.cancelBtn.clicked.connect(self.cancelClicked)
        
    #点击新建按钮触发的事件
    def createClicked(self):
        import setup.setupnewtask as setupnewtask    
        self.close()
        reload(setupnewtask)
       
        
    #点击取消按钮触发的事件    
    def cancelClicked(self):
        self.close()

        
        
    def getShotAndAssetInfo(self):  
        #导入ShotService
        import service.shotservice as shotservice
        shotContents = shotservice.Shot().callService(2)
        
        #导入AssetService
        import service.assetservice as assetservice
        assertContents = assetservice.Asset().callService(2)
                     
        #创建一个容器列表存放数据
        List=QtGui.QListWidget()
        for content in shotContents:        
            QtGui.QListWidgetItem(content['name'],List)
        
        for content in assertContents:        
            QtGui.QListWidgetItem(content['name'],List)
            
        self.shotScrollArea.setWidget(List)
        
    
    def getTaskInfo(self):
        
        #导入apiService
        import service.taskservice as taskservice
        contents = taskservice.Task().callService(2)
        
        #创建一个容器列表存放数据
        List=QtGui.QListWidget()
        for content in contents:        
            QtGui.QListWidgetItem(content['content'],List)
          
        self.tasksScrollArea.setWidget(List)
