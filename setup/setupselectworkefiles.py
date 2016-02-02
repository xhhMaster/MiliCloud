# -*- coding: utf-8 -*-
from PySide import QtGui,QtCore
from ui.selectworkfiles import Ui_Widget
from common.datacommon import Data 
from common.uicommon import UI
from common.uicommon import Msg
from common.funcommon import Fun
import os
import maya.cmds as cmds

class Widget(QtGui.QWidget, Ui_Widget):
    def __init__(self, uid,pid,entityId,entityType,taskID,parent=None):
        super(Widget,self).__init__(parent)
        self.pid = pid
        self.uid = uid
        self.selectedId = entityId
        self.selectedType = entityType
        self.taskID = taskID
        self.setupUi(self)    
        self.warning = UI().initMessageBox()
        self.warning.setIcon(QtGui.QMessageBox.Critical)     
        self.projectList = UI().initTableWidget(['ID','Image','Name','Type'],4)
        self.SAList = UI().initTableWidget(['ID','Image','Name','Type'],4)
        self.taskList = UI().initTableWidget(['ID','Image','Name','Type'],4)
        self.fileList = UI().initTableWidget(['ID','Image','Name','Type'],4)
        
        self.showData()
        self.getProject()
        self.getSA()
        self.getTask()
        self.getWorkFile()
        self.backBtn.clicked.connect(self.backClicked)
        self.openBtn.clicked.connect(self.openClicked)
        self.bindingComboBox()
        
    def backClicked(self):
        import setup.setupselecttask as setupselecttask
        self.Widget = setupselecttask.Widget(self.pid,self.uid)
        self.fileList.setRowCount(0)
        self.Widget.show() 
        self.close()                
        
    def openClicked(self):
        self.openSelectedFile()
        
    def getProject(self): 
        self.projectInfo = Data().getProject(self.pid)
        for index,content in enumerate(self.projectInfo):
            imageId = content[u'image_id']
            imgPath = Fun().getImgPath(str(imageId), 'thumbnails/')
            Fun().bindingDataSingal(index,content,self.projectList,['id','name','description'],imgPath,'Project')
        self.projectList.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.projectList.setFocusPolicy(QtCore.Qt.NoFocus)
    
    def getSA(self):
        if self.selectedType == 'Shot':
            self.resultInfo = Data().getShot(self.pid,self.selectedId,self.selectedType)
        else:
            self.resultInfo = Data().getAsset(self.pid,self.selectedId,self.selectedType)
        for index,content in enumerate(self.resultInfo):
            imageId = content[u'image_id']
            imgPath = Fun().getImgPath(str(imageId), 'thumbnails/')
            Fun().bindingDataSingal(index,content,self.SAList,['id','name','description'],imgPath,self.selectedType)
        self.SAList.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.SAList.setFocusPolicy(QtCore.Qt.NoFocus)
        
    def getTask(self):
        self.taskInfo = Data().getTask(self.uid,self.selectedId,self.selectedType,self.taskID,self.pid)
        for index,content in enumerate(self.taskInfo):
            imageId = content[u'image_id']
            imgPath = Fun().getImgPath(str(imageId), 'thumbnails/')
            Fun().bindingDataSingal(index,content,self.taskList, ['task_id','name','user_id'],imgPath,'Task')
        self.taskList.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.taskList.setFocusPolicy(QtCore.Qt.NoFocus)
    
    def getWorkFile(self):
        fileInfo = Data().getWorkFile(self.taskID,'Task')
        if len(fileInfo) > 0 :
            for index,content in enumerate(fileInfo):
                imageId = content[u'image_id']
                imgPath = Fun().getImgPath(str(imageId), 'version/MayaPushImage/')
                Fun().bindingDataSingal(index,content,self.fileList,['id','code','user_id'],imgPath,'Work')
        else:
            Fun().sourceDataISNULL(self.fileList,'Work')
      
       
    def bindingComboBox(self):
        self.comboBox.insertItem(0,u'已发布的文件')
    
    def openSelectedFile(self):
        selectedRow = self.fileList.currentIndex().row()
        if selectedRow != -1: 
            selectedTxt = self.fileList.item(selectedRow,2).text()
            selectedID = self.fileList.item(selectedRow,0).text()
            print selectedID
            fileInfo = selectedTxt.split(u'制作人')
            filePath = 'd:/mayaDownload/SenceFile/'
            pathDir = os.path.exists(filePath)
            if not pathDir:
                os.makedirs(filePath)
            fileInfo[0] = fileInfo[0].strip('\n')
            fullPathFileName = filePath + fileInfo[0]
          
            Data().downLoad('version/MayaPushFile/'+ selectedID+'/'+fileInfo[0], fullPathFileName)
            cmds.file(fullPathFileName,f = 1,type='mayaBinary',o = 1) 
        else:
            txtTitle = u'警告信息'
            txtMainContent = u'打开失败！                                             '
            txtSubContent =  u'请选择工作文件！'
            Msg().showDialog(self.warning, txtTitle, txtMainContent, txtSubContent)
    
    def showData(self):
        self.mainLayout = QtGui.QVBoxLayout()
        
        self.projectLayout = QtGui.QVBoxLayout()
        self.projectBox = QtGui.QGroupBox()
        self.projectBox.setTitle('Project')
        self.projectLayout.addWidget(self.projectList)
        self.projectBox.setLayout(self.projectLayout)
        
        self.SALayout = QtGui.QVBoxLayout()
        self.SABox = QtGui.QGroupBox()
        self.SABox.setTitle('Shot&Asset')
        self.SALayout.addWidget(self.SAList)
        self.SABox.setLayout(self.SALayout)
       
        self.taskLayout = QtGui.QVBoxLayout()
        self.taskBox = QtGui.QGroupBox()
        self.taskBox.setTitle('Task')
        self.taskLayout.addWidget(self.taskList)
        self.taskBox.setLayout(self.taskLayout)
       
        self.mainLayout.addWidget(self.projectBox)
        self.mainLayout.addWidget(self.SABox)
        self.mainLayout.addWidget(self.taskBox)
        self.workBox.setLayout(self.mainLayout)
        
        self.workLayout = QtGui.QVBoxLayout() 
        self.workLayout.addWidget(self.fileList)
        self.workFile.setLayout(self.workLayout) 
