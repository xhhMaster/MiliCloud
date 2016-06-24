# -*- coding: utf-8 -*-
from PySide import QtGui,QtCore
from ui.breakdown_ui import Ui_Widget
import conf.path as confPath
import maya.cmds as cmds
from common.datacommon import Data 
from common.funcommon import Fun
from common.uicommon import UI
from common.uicommon import Msg
import conf.msgsetting as suggestion
import re
import os

class Widget(QtGui.QWidget, Ui_Widget):
    def __init__(self,uid,pid,parent=None):
        super(Widget,self).__init__(parent)
        self.setupUi(self)
        self.uid = str(uid)
        self.pid = str(pid)
        self.search.setStyleSheet("background-image: url("+ confPath.iconForSearch + ");\n"
                                    "background-repeat: no-repeat;\n"
                                    "background-position: center left;\n"
                                    "border-style: inset; \n"
                                    "border-radius: 9px; \n"
                                    "padding-left: 15px")
        
      
        self.updateList = UI().initListWidget()
        self.noUpdateList = UI().initListWidget()
        self.mainLayout = QtGui.QVBoxLayout()
        self.showData()
        self.getData()
        self.getReference()
        self.warning = UI().initMessageBox()
        self.warning.setIcon(QtGui.QMessageBox.Critical)  
        self.search.textChanged.connect(self.searchData)
        self.updateBtn.clicked.connect(self.updateClicked)
        self.cancelBtn.clicked.connect(self.cancelClicked)
       
    def cancelClicked(self):
        self.close()
        
    def updateClicked(self):
        selectedIndex = self.updateList.currentIndex().row()
        if selectedIndex != -1:
            selectTxt = self.updateList.currentIndex().data()
            fileInfo = selectTxt.split(u'上传人')
            fileInfo[0] = fileInfo[0].strip('\n')
            filePath = confPath.downloadRefFile
            fullPath = filePath + fileInfo[0]
            selectedID = self.updateList.item(selectedIndex).data(QtCore.Qt.UserRole)
            newData = Data().getVersionById(selectedID)
            s = cmds.ls(type = ['reference'])
            for content in s:
                try:
                    chilidPath = cmds.referenceQuery(content,filename =1).split('{')[0]
                except Exception,e:
                    print Exception,e
                    chilidPath = ''
                oldData = Data().getVersionByName(os.path.basename(chilidPath),self.pid)
                if len(oldData > 0):
                    if (oldData[0]['entity_id'] == newData[0]['entity_id'] and 
                        oldData[0]['entity_type'] == newData[0]['entity_type']):
                        if chilidPath == fullPath:
                            break 
                        else:
                            self.downloadPublish(content)
            self.close()
            self.warning.setIcon(QtGui.QMessageBox.NoIcon)
            Msg().showDialog(self.warning,suggestion.prompt,suggestion.updateSucessed,'')
        else:
            Msg().showDialog(self.warning,suggestion.warning,suggestion.updateFailed,suggestion.selectRedf)
        
    def getReference(self):
        self.bindingUpdateList(self.updateData)
        self.bindingUnUpdateList(self.noUpdateData)
       
        
    def showData(self):
        self.updateLabel = QtGui.QLabel()
        self.updateLabel.setText(u'服务器上有新版本的文件')
        
        self.noUpdateLabel = QtGui.QLabel()
        self.noUpdateLabel.setText(u'没有新的版本的文件')
        
        self.mainLayout.addWidget(self.updateLabel)
        self.mainLayout.addWidget(self.updateList)
        self.mainLayout.addWidget(self.noUpdateLabel)
        self.mainLayout.addWidget(self.noUpdateList)
        self.scrollArea.setLayout(self.mainLayout) 
        
    def searchData(self):
        userInput = self.search.text()
        if userInput != '':
            searchUpDateData = self.filterData(userInput,self.updateData)
            searchUnUpadateData = self.filterData(userInput,self.noUpdateData)
            self.bindingUpdateList(searchUpDateData)
            self.bindingUnUpdateList(searchUnUpadateData)
        else:
            self.getReference()
    
          
    def filterData(self,userinput,sourceData):
        suggestions = []
        pattern = '.*?'.join(userinput)   
        regex = re.compile(pattern)
        for content in sourceData:
            itemId = content['id']
            itemImg = content['image_id']
            itemName = content['code']
            itemVid = content['versionId']
            itemUser = content['user_name']
            itemCreate = content['created_at']
            match = regex.search(itemName)
            if match:
                itemDesc = content['description']
                suggestions.append({u'id':itemId,u'code':itemName,u'image_id':itemImg,
                                    u'description':itemDesc,u'versionId':itemVid,
                                    u'user_name':itemUser,u'created_at':itemCreate})           
        return suggestions
    
        
    def downloadPublish(self,content):
        selectedIndex = self.updateList.currentIndex().row()
        selectedID = self.updateList.item(selectedIndex).data(QtCore.Qt.UserRole+2)
        selectTxt = self.updateList.currentIndex().data()
        fileInfo = selectTxt.split(u'上传人')
        fileInfo[0] = fileInfo[0].strip('\n')
   
        filePath = confPath.downloadRefFile
        filePath = filePath  + '/'
        pathDir = os.path.exists(filePath)
        if not pathDir:
            os.makedirs(filePath)
        fullPath = filePath + fileInfo[0]
        if not os.path.exists(fullPath):
            Data().downLoad('version/'+ str(selectedID) +'/'+ fileInfo[0], fullPath)
        cmds.file(fullPath,loadReference = content) 

    def getVersionID(self,referenceList): 
        versionIDList = []
        for reference in referenceList:
            contents = Data().getVersionByName(os.path.basename(reference),self.pid)
            if len(contents) > 0:
                for content in contents:
                    versionIDList.append(str(content['versionId']))
        return versionIDList
    
    def getLastVersion(self,referenceList):
        lastVersionID = []
        for reference in referenceList:
            if os.path.exists(reference):
                content = Data().getVersionByName(os.path.basename(reference),self.pid)
                entityID = content[0]['entity_id']
                versionID = Data().getLastVersion(str(entityID), 'Task')
                versionID = versionID.replace('"','')
                lastVersionID.append(versionID)
        
        vIdList = sorted(set(lastVersionID),key=lastVersionID.index)
        return vIdList
        
    def bindingUpdateList(self,sourceData): 
        self.updateList.clear()
        self.updateList.setSpacing(7)
        self.updateList.setIconSize(QtCore.QSize(122,95))
        self.noUpdateList.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        for index,content in enumerate(sourceData):
            imageId = content[u'image_id']
            if imageId == None:
                imageId = ''
            imgPath = Fun().getImgPath(imageId,content['id'],'Work',confPath.publishImgPath)
            Fun().bindingList(index,content,self.updateList,imgPath,'Work')
    
    def bindingUnUpdateList(self,sourceData):
        self.noUpdateList.clear()
        self.noUpdateList.setSpacing(7)
        self.noUpdateList.setIconSize(QtCore.QSize(122,95))
        self.noUpdateList.setSelectionMode(QtGui.QAbstractItemView.NoSelection)   
        for index,content in enumerate(sourceData):
            imageId = content[u'image_id']
            if imageId == None:
                imageId = ''
            imgPath = Fun().getImgPath(imageId,content['id'],'Work',confPath.publishImgPath)
            Fun().bindingList(index,content,self.noUpdateList,imgPath,'Work')         
    
    def getData(self):
        referenceList = cmds.file(query = 1,reference = 1)
        #referenceList = [u'd:/mayaDownload/SenceFile/a1234.001.ma', u'd:/mayaDownload/SenceFile/a164121.001.ma', u'd:/mayaDownload/SenceFile/a2016163321.001.ma']
        reList = self.getVersionID(referenceList)
    
        if len(reList) == 0:
            reList.append('-1')
        self.noUpdateData = Data().lastVersionView(reList)
        self.updateData = Data().checkVersion(reList)

        