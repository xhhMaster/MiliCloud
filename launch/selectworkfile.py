# -*- coding: utf-8 -*-
from PySide import QtGui,QtCore
from ui.selectworkfiles_ui import Ui_Widget
from common.datacommon import Data 
from common.uicommon import UI
from common.uicommon import Msg
from common.funcommon import Fun
import os,time
import maya.cmds as cmds
import conf.msgsetting as suggestion
import conf.path as confPath
import common.xmlcommon as xml

class Widget(QtGui.QWidget, Ui_Widget):
    def __init__(self,uid,pid,entityId,entityType,taskID,useName,parent=None):
        super(Widget,self).__init__(parent)
        self.pid = pid
        self.uid = uid
        self.selectedId = entityId
        self.selectedType = entityType
        self.taskID = taskID
        self.useName = useName
        self.setupUi(self)    
        self.warning = UI().initMessageBox()
        self.warning.setIcon(QtGui.QMessageBox.Critical)
            
        self.projectList = UI().initListWidget()
        self.SAList = UI().initListWidget()
        self.taskList = UI().initListWidget()
        self.fileList = UI().initListWidget()
        
        self.showData()
        self.getProject()
        self.getSA()
        self.getTask()
        self.getWorkFile()
        self.backBtn.clicked.connect(self.backClicked)
        self.openBtn.clicked.connect(self.openClicked)
        self.newBtn.clicked.connect(self.newClicked)
        
    def backClicked(self):
        import launch.selecttask as selecttask
        reload(selecttask)
        self.Widget = selecttask.Widget(self.pid,self.uid,self.useName)
        self.Widget.show() 
        self.close()                
        
    def openClicked(self):
        if self.fileList.currentIndex().row() != -1:
            info = {'project_id':str(self.projectInfo[0]['id']),'entity_type':self.selectedType,
                'entity_id':str(self.entityInfo[0]['id']),'task_id':str(self.taskInfo[0]['id'])}
            xml.writeSelectedFile(info)
            self.openSelectedFile()
            self.close()           
        else:
            Msg().showDialog(self.warning,suggestion.warning,suggestion.clickedFailed,suggestion.selectWorkFile)
            
    def newClicked(self):
        info = {'project_id':str(self.projectInfo[0]['id']),'entity_type':self.selectedType,
                'entity_id':str(self.entityInfo[0]['id']),'task_id':str(self.taskInfo[0]['id'])}
        xml.writeSelectedFile(info)
        cmds.file(new = True,force = True)
        self.close()           
        
    def getProject(self): 
        self.projectInfo = Data().getSingleProject(self.pid)
        self.bindingData(self.projectInfo,self.projectList,'Project')
        self.projectList.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
    
    def getSA(self):
        if self.selectedType == 'Shot':
            self.entityInfo = Data().getSingleShot(self.pid,self.selectedId,self.selectedType)
        else:
            self.entityInfo = Data().getSingleAsset(self.pid,self.selectedId,self.selectedType)
        self.bindingData(self.entityInfo,self.SAList,self.selectedType)
        self.SAList.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        
    def getTask(self):
        self.taskInfo = Data().getSingleTask(self.uid,self.taskID,'')
        self.bindingData(self.taskInfo,self.taskList,'Task')
        self.taskList.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
         
    def getWorkFile(self):
        fileInfo = Data().getWorkFile(self.taskID,'Task',str(self.pid))
        self.bindingData(fileInfo,self.fileList,'Work')
    
    def openSelectedFile(self):
        selectedRow = self.fileList.currentIndex().row()
        if selectedRow != -1: 
            selectedTxt = self.fileList.currentIndex().data()
            selectedID = self.fileList.item(selectedRow).data(QtCore.Qt.UserRole+2)
            fileInfo = selectedTxt.split(u'上传人')
            filePath = confPath.downloadFile
            today = time.strftime('%Y%m%d')
            filePath = filePath + '/' + today + '/'
          
            if not os.path.exists(filePath):
                os.makedirs(filePath)
            fileInfo[0] = fileInfo[0].strip('\n')
            fType = (fileInfo[0].split('.'))[2]
            fullPath = filePath + fileInfo[0]
            
            selectVid = self.fileList.item(selectedRow).data(QtCore.Qt.UserRole)
            referenceData = Data().getReferenceVersion(str(selectVid))
            if len(referenceData)>0:
                if not os.path.exists(confPath.localpath +'/Reference/'):
                    os.makedirs(confPath.localpath +'/Reference/')
                for content in referenceData:
                    Data().downLoad('version/'+ str(content['attachment_id']) +'/'+ content['filename'], 
                                    (confPath.localpath +'/Reference/' + content['filename']))
            
            if os.path.exists(fullPath):
                os.remove(fullPath)
            
            
            code = Data().downLoad('version/'+ str(selectedID) +'/'+fileInfo[0], fullPath)
            if code == 404 :
                Msg().showDialog(self.warning,suggestion.warning,suggestion.clickedFailed,suggestion.noFoundFile)
            else:
                if fType == 'mb':
                    cmds.file(fullPath,f = 1,type='mayaBinary',o = 1) 
                else:
                    cmds.file(fullPath,f = 1,type='mayaAscii',o = 1)   
        else:
            Msg().showDialog(self.warning,suggestion.warning,suggestion.clickedFailed,suggestion.selectWorkFile)
    
    def showData(self):
        self.mainLayout = QtGui.QVBoxLayout()
        
        self.projectLayout = QtGui.QVBoxLayout()
        self.projectBox = QtGui.QGroupBox()
        self.projectBox.setMaximumSize(310,135)
        self.projectBox.setTitle('Project')
        self.projectLayout.addWidget(self.projectList)
        self.projectBox.setLayout(self.projectLayout)
        
        self.SALayout = QtGui.QVBoxLayout()
        self.SABox = QtGui.QGroupBox()
        self.SABox.setMaximumSize(310,135)
        self.SABox.setTitle(self.selectedType)
        self.SALayout.addWidget(self.SAList)
        self.SABox.setLayout(self.SALayout)
       
        self.taskLayout = QtGui.QVBoxLayout()
        self.taskBox = QtGui.QGroupBox()
        self.taskBox.setMaximumSize(310,135)
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

    def bindingData(self,sourceData,outputList,Flag):
        outputList.clear()
        outputList.setSpacing(5)
        outputList.setIconSize(QtCore.QSize(122,95))
        if len(sourceData) > 0 :
            for index,content in enumerate(sourceData):
                print content
                imageId = content[u'image_id']
                if imageId == None:
                    imageId = ''
                imgPath = Fun().getImgPath(imageId,content['id'],Flag,confPath.publishImgPath)
                Fun().bindingList(index,content,outputList,imgPath,Flag)
        else:
            newItem = QtGui.QListWidgetItem()
            newItem.setText(suggestion.noData)
            outputList.insertItem(0,newItem)
            outputList.setSelectionMode(QtGui.QAbstractItemView.NoSelection)   
    