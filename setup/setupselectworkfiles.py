# -*- coding: utf-8 -*-
from PySide import QtGui,QtCore
from ui.selectworkfiles_ui import Ui_Widget

class Widget(QtGui.QWidget, Ui_Widget):
    def __init__(self,pid,desc,content,parent=None):
        super(Widget,self).__init__(parent)
        self.pid = pid
        self.desc = desc
        self.content = content
        self.setupUi(self)
        self.getShotAndAssetInfo(self.pid)
        self.projectNameEdit.setText(self.content)
        self.projectDescEdit.setText(self.desc)
        
        self.List.clicked.connect(self.getTaskInfo)
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

        
        
    def getShotAndAssetInfo(self,pid):  
        #导入ShotService
        import service.shotservice as shotservice
        shotContents = shotservice.Shot().callService(pid)
        
        #导入AssetService
        import service.assetservice as assetservice
        assetContents = assetservice.Asset().callService(pid)
                     
        #创建一个容器列表存放数据
        self.List = self.__initTableWidget()

        header = ['A&SID','A&SName','A&SType']
        self.List.setHorizontalHeaderLabels(header)
                               
        if len(shotContents) > 0:
            for index,content in enumerate(shotContents):
                self.List.insertRow(index)    
                itemId = QtGui.QTableWidgetItem(content['id'])
                itemName = QtGui.QTableWidgetItem(content['name'])
                itemType = QtGui.QTableWidgetItem("Shot")
                self.List.setItem(index,0,itemId)
                self.List.setItem(index,1,itemName)
                self.List.setItem(index,2,itemType)  
        
        if len(assetContents) > 0:
            for index,content in enumerate(assetContents):
                self.List.insertRow(index)
                itemId = QtGui.QTableWidgetItem(content['id'])
                itemName = QtGui.QTableWidgetItem(content['name'])
                itemType = QtGui.QTableWidgetItem("Asset")
                self.List.setItem(index,0,itemId)
                self.List.setItem(index,1,itemName)
                self.List.setItem(index,2,itemType)    
                  
        self.List.setColumnHidden(0,True)
        self.List.setColumnHidden(2,True)
        index = QtCore.QModelIndex()
        self.List.setCurrentIndex(index)
            
        self.shotScrollArea.setWidget(self.List)
        
       
      
    def getTaskInfo(self):
        
        selectedRow = self.List.currentItem().row()
        selectedId = self.List.item(selectedRow,0).text()
        selectedType = self.List.item(selectedRow,2).text()
        
        #导入apiService
        import service.taskservice as taskservice
        contents = taskservice.Task().callService(selectedId,selectedType)
        
        #创建一个容器列表存放数据
        List=QtGui.QListWidget()
        
        if len(contents) > 0:
            for content in contents:        
                QtGui.QListWidgetItem(content['content'],List)
          
        self.tasksScrollArea.setWidget(List)


    def __initTableWidget(self):
        List = QtGui.QTableWidget()
        List.setColumnCount(3)
        List.verticalHeader().setVisible(False)
        List.horizontalHeader().setVisible(False)
        List.setFrameShape(QtGui.QFrame.NoFrame)
        List.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        List.setShowGrid(False)
        List.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        List.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        return List
    
    