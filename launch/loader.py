# -*- coding: utf-8 -*-
from PySide import QtGui,QtCore
from ui.loader_ui import Ui_Widget
import conf.path as path
from common.datacommon import Data 
import os,re
from common.funcommon import Fun
import maya.cmds as cmds
from common.uicommon import Msg
import conf.msgsetting as suggestion
from common.uicommon import UI
import collections
import common.xmlcommon as xml

class Widget(QtGui.QWidget, Ui_Widget):
    def __init__(self,uid,pid,parent=None):
        super(Widget,self).__init__(parent)
        self.setupUi(self)
        self.label = QtGui.QLabel(self)
        self.label.setGeometry(QtCore.QRect(370, 60, 191, 20))
        self.uid = str(uid)
        self.pid = str(pid)
        self.searchSA.setStyleSheet("background-image: url("+ path.iconForSearch + ");\n"
                                    "background-repeat: no-repeat;\n"
                                    "background-position: center left;\n"
                                    "border-style: inset; \n"
                                    "border-radius: 9px; \n"
                                    "padding-left: 15px")
        self.searchPublish.setStyleSheet("background-image: url("+ path.iconForSearch +");\n"
                                    "background-repeat: no-repeat;\n"
                                    "background-position: center left;\n"
                                    "border-style: inset; \n"
                                    "border-radius: 9px; \n"
                                    "padding-left: 15px")
        
        
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(path.iconForDetail))
        self.detailBtn.setIcon(icon1)
        self.warning = UI().initMessageBox()
        self.warning.setIcon(QtGui.QMessageBox.Critical)     
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(path.iconForList))
        self.listBtn.setIcon(icon2)
        
        self.bindingTab()
        self.List = QtGui.QListWidget()
        self.List.setMovement(QtGui.QListView.Static)
        self.mainLayout = QtGui.QVBoxLayout()
        self.tabWidget.currentChanged.connect(self.selectTab)
        self.assetTree.itemClicked.connect(self.assetTreeClicked)
        self.shotTree.itemClicked.connect(self.shotTreeClicked)
        self.taskTree.itemClicked.connect(self.taskTreeClicked)
        self.detailBtn.clicked.connect(self.detailClicked)
        self.listBtn.clicked.connect(self.listClicked)
        self.List.itemDoubleClicked.connect(self.doubleClicked)
        self.cancelBtn.clicked.connect(self.cancelClicked)
        self.searchSA.textChanged.connect(self.searchTab)
        self.searchPublish.textChanged.connect(self.searchFile)
        self.selBtn.clicked.connect(self.selectClicked)
      
        if os.path.exists(path.xmlForRef):
            self.setStatus(path.xmlForRef)
        
        self.file = []
       
    def cancelClicked(self):
        self.close()
    
    def selectClicked(self):
        selectRow = self.List.currentIndex().row()
        selectData = self.List.currentIndex().data()
        if selectRow == -1 or selectData == u'没有发布的文件':
            Msg().showDialog(self.warning,suggestion.warning,suggestion.clickedFailed,suggestion.selectWorkFile)
        else:
            self.doubleClicked()
            
    def bindingTab(self):
        self.bindingAsset()
        self.bindingShot()
        self.bindingMyTask()
      
    def assetPublish(self,selectType,selectData):
        self.List.clear()
        if selectType != 'Task' :
            data = collections.OrderedDict(sorted((self.assetData).items(),key = lambda t:t[1])) 
            for (key,value) in data.items():
                if key == selectData:
                    for index,content in enumerate(value):
                        newItem = QtGui.QListWidgetItem()
                        newItem.setIcon(QtGui.QPixmap(path.iconForFile))
                        self.List.setIconSize(QtCore.QSize(150,150))
                        newItem.setData(QtCore.Qt.UserRole,str(content['id']))
                        newItem.setData(QtCore.Qt.UserRole+1,'Asset')
                        newItem.setText(content['name'])
                        self.List.insertItem(index, newItem)
        else:
            selectID = self.assetTree.currentItem().data(0,QtCore.Qt.UserRole)
            taskData = Data().getTask(str(selectID),'Asset',self.uid,self.pid)
            self.bindingPubilshFile(taskData)
        
        if self.List.count() == 0:
            newItem = QtGui.QListWidgetItem()
            newItem.setText(u'没有发布的文件')
            self.List.insertItem(0, newItem)
            self.List.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.mainLayout.addWidget(self.List)
        self.List.setViewMode(QtGui.QListView.IconMode)
        self.scrollArea.setLayout(self.mainLayout)

    def shotPublish(self,selectType,selectData):
        self.List.clear()
        if selectType != 'Task' :
            data = collections.OrderedDict(sorted((self.shotData).items(),key = lambda t:t[1])) 
            for (key,value) in data.items():
                if value[0]['sequence_name'] == selectData:
                    for index,content in enumerate(value):
                        newItem = QtGui.QListWidgetItem()
                        newItem.setIcon(QtGui.QPixmap(path.iconForFile))
                        self.List.setIconSize(QtCore.QSize(150,150))
                        newItem.setData(QtCore.Qt.UserRole,str(content['id']))
                        newItem.setData(QtCore.Qt.UserRole+1,'Shot')
                        newItem.setData(0,QtCore.Qt.UserRole+3,key)
                        newItem.setText(content['name'])
                        self.List.insertItem(index, newItem)
        else:
            selectID = self.shotTree.currentItem().data(0,QtCore.Qt.UserRole)
            taskData = Data().getTask(str(selectID),'Shot',self.uid,self.pid)
            self.bindingPubilshFile(taskData)
        
        if self.List.count() == 0:
            newItem = QtGui.QListWidgetItem()
            newItem.setText(u'没有发布的文件')
            self.List.insertItem(0, newItem)
            self.List.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.mainLayout.addWidget(self.List)
        self.List.setViewMode(QtGui.QListView.IconMode)
        self.scrollArea.setLayout(self.mainLayout) 
       
    def taskPublish(self,selectType,selectData):
        self.List.clear()
        if selectType != 'Task' :
            for evalue in self.entityData:
                parentName = evalue['entity_type'] + ' ' + evalue['entity_name']
                if parentName == selectData:
                    for index,content in enumerate(self.entityByStepData):
                        if (content['entity_type'] == evalue['entity_type'] and content['entity_id'] == evalue['entity_id']):
                            newItem = QtGui.QListWidgetItem()
                            newItem.setIcon(QtGui.QPixmap(path.iconForFile))
                            self.List.setIconSize(QtCore.QSize(150,150))
                            newItem.setData(QtCore.Qt.UserRole,content['step_id'])
                            newItem.setData(QtCore.Qt.UserRole+1,evalue['entity_type'])
                            newItem.setText(content['step_name'])
                            self.List.insertItem(index, newItem)
                else: 
                    selectID = self.taskTree.currentItem().data(0,QtCore.Qt.UserRole)
                    selectType = self.taskTree.currentItem().data(0,QtCore.Qt.UserRole+2)
                    selectEntityID = self.taskTree.currentItem().data(0,QtCore.Qt.UserRole+3)
                    if selectType == evalue['entity_type'] and selectEntityID == evalue['entity_id']:
                        taskData = Data().getTask(str(evalue['entity_id']),str(evalue['entity_type']),self.uid,self.pid)
                        for index,tvalue in enumerate(taskData):
                            if (tvalue['entity_type'] == evalue['entity_type'] and tvalue['step_id'] == selectID
                                and tvalue['entity_id'] == evalue['entity_id']):
                                    newItem = QtGui.QListWidgetItem()
                                    newItem.setIcon(QtGui.QPixmap(path.iconForFile))
                                    self.List.setIconSize(QtCore.QSize(150,150))
                                    newItem.setData(QtCore.Qt.UserRole,tvalue['id'])
                                    newItem.setData(QtCore.Qt.UserRole+1,'Task')
                                    newItem.setText(tvalue['name'])
                                    self.List.insertItem(index, newItem)    
        else:
            selectTaskId = self.taskTree.currentItem().data(0,QtCore.Qt.UserRole+2)
            selectStepId = self.taskTree.currentItem().data(0,QtCore.Qt.UserRole)
            taskData = Data().getSingleTask(self.uid, str(selectTaskId),str(selectStepId))
            self.bindingPubilshFile(taskData)
        
        if self.List.count() == 0:
            newItem = QtGui.QListWidgetItem()
            newItem.setText(u'没有发布的文件')
            self.List.insertItem(0, newItem)
            self.List.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.mainLayout.addWidget(self.List)
        self.List.setViewMode(QtGui.QListView.IconMode)
        self.scrollArea.setLayout(self.mainLayout) 
         
    def assetTreeClicked(self):
        selectType= self.assetTree.currentItem().data(0,QtCore.Qt.UserRole+2)
        selectContent = self.assetTree.currentIndex().data()
        self.label.setText('Asset\\' + selectContent)
        self.label.setStyleSheet('font-size:13px')
        self.assetPublish(selectType,selectContent)
    
    def shotTreeClicked(self):
        selectType= self.shotTree.currentItem().data(0,QtCore.Qt.UserRole+2)
        selectContent = self.shotTree.currentIndex().data()
        self.label.setText('Shot\\' + selectContent)
        self.label.setStyleSheet('font-size:13px')
        self.shotPublish(selectType,selectContent)
    
    def taskTreeClicked(self):
        selectType = self.taskTree.currentItem().data(0,QtCore.Qt.UserRole+1)
        selectContent = self.taskTree.currentIndex().data()
        self.taskPublish(selectType,selectContent)
        
    def treeForAsset(self,tree,sourceData):
        tree.header().hide()
        data = collections.OrderedDict(sorted((sourceData).items(),key = lambda t:t[1])) 
        for (key, value) in data.items():
            rootItem = QtGui.QTreeWidgetItem(tree)
            rootItem.setData(0,QtCore.Qt.UserRole,'0')
            rootItem.setData(0,QtCore.Qt.UserRole+1,'Asset')
            rootItem.setData(0,QtCore.Qt.UserRole+2,'NUll')
            rootItem.setText(0,key)
            for content in value:
                child = QtGui.QTreeWidgetItem(rootItem)
                child.setData(0,QtCore.Qt.UserRole,content['id'])
                child.setData(0,QtCore.Qt.UserRole+1,'Asset')
                child.setData(0,QtCore.Qt.UserRole+2,'Task')
                child.setText(0,content['name'])  
                
    def treeForShot(self,tree,sourceData):
        tree.header().hide()
        data = collections.OrderedDict(sorted((sourceData).items(),key = lambda t:t[1])) 
        for (key, value) in data.items():
            rootItem = QtGui.QTreeWidgetItem(tree)
            rootItem.setData(0,QtCore.Qt.UserRole,'0')
            rootItem.setData(0,QtCore.Qt.UserRole+1,'Shot')
            rootItem.setData(0,QtCore.Qt.UserRole+2,'NUll')
            rootItem.setData(0,QtCore.Qt.UserRole+3,key)
            rootItem.setText(0,value[0]['sequence_name'])
            for content in value:
                child = QtGui.QTreeWidgetItem(rootItem)
                child.setData(0,QtCore.Qt.UserRole,content['id'])
                child.setData(0,QtCore.Qt.UserRole+1,'Shot')
                child.setData(0,QtCore.Qt.UserRole+2,'Task')
                child.setText(0,content['name'])                      
      
    def treeForTask(self,tree,entityData,entityByStepData,taskData):
        tree.header().hide()
        for evalue in entityData:
            rootItem = QtGui.QTreeWidgetItem(tree)
            rootItem.setData(0,QtCore.Qt.UserRole,evalue['entity_id'])
            rootItem.setData(0,QtCore.Qt.UserRole+1,evalue['entity_type'])
            rootItem.setData(0,QtCore.Qt.UserRole+2,'NULL')
            rootItem.setText(0,evalue['entity_type'] + ' ' + evalue['entity_name'])
            tempStepID = ''
            for esvalue in entityByStepData:
                if (esvalue['entity_type'] == evalue['entity_type'] and esvalue['entity_id'] == evalue['entity_id']):
                    if tempStepID != esvalue['step_id']:
                        child = QtGui.QTreeWidgetItem(rootItem)
                        child.setData(0,QtCore.Qt.UserRole,esvalue['step_id'])
                        child.setData(0,QtCore.Qt.UserRole+1,'Step')
                        child.setData(0,QtCore.Qt.UserRole+2,esvalue['entity_type'])
                        child.setData(0,QtCore.Qt.UserRole+3,esvalue['entity_id'])
                        child.setText(0,esvalue['step_name'])
                        for tvalue in taskData:
                            if (tvalue['step_id'] == esvalue['step_id'] and tvalue['entity_type'] == esvalue['entity_type']
                                and tvalue['entity_id'] == esvalue['entity_id']):
                                    child2 = QtGui.QTreeWidgetItem(child)
                                    child2.setData(0,QtCore.Qt.UserRole,tvalue['step_id'])
                                    child2.setData(0,QtCore.Qt.UserRole+1,'Task')
                                    child2.setData(0,QtCore.Qt.UserRole+2,tvalue['task_id'])
                                    child2.setText(0,tvalue['name'])
                        
                        tempStepID = esvalue['step_id']
        
    def bindingAsset(self):
        self.assetData = Data().getAssetByType(self.pid)
        self.assetTree = QtGui.QTreeWidget()
        self.assetTree.setStyleSheet("font-size:13px")
        self.treeForAsset(self.assetTree,self.assetData)
        assetLayout = QtGui.QVBoxLayout()
        assetLayout.addWidget(self.assetTree)
        self.tab.setLayout(assetLayout)
        
    def bindingShot(self):
        self.shotData =Data().getShotBySequences(self.pid)
        self.shotTree = QtGui.QTreeWidget()
        self.shotTree.setStyleSheet("font-size:13px")
        self.treeForShot(self.shotTree,self.shotData)
        shotLayout = QtGui.QVBoxLayout()
        shotLayout.addWidget(self.shotTree)
        self.tab_2.setLayout(shotLayout)  
        
    def bindingMyTask(self):
        self.entityData = Data().getTaskStep(self.uid,self.pid,'entity')
        self.taskData = Data().getTaskStep(self.uid,self.pid,'Table')
        self.entityByStepData = Data().getTaskStep(self.uid,self.pid,'step')
        self.taskTree = QtGui.QTreeWidget()
        self.taskTree.setStyleSheet("font-size:13px")
        self.treeForTask(self.taskTree,self.entityData,self.entityByStepData,self.taskData)
        taskLayout = QtGui.QVBoxLayout()
        taskLayout.addWidget(self.taskTree)
        self.tab_3.setLayout(taskLayout)  
        
    def detailClicked(self):
        self.List.setViewMode(QtGui.QListView.IconMode)
      
    def listClicked(self):
        self.List.setViewMode(QtGui.QListView.ListMode)
        
    def double(self,tree,flag):
        selectRow = self.List.currentIndex().row()
        selectData = self.List.currentIndex().data()
        if selectData != u'没有发布的文件':
            if '.' not in selectData:
                selectChild = tree.currentItem().child(selectRow)
                tree.expandItem(selectChild)
                tree.setCurrentItem(selectChild)
                if flag == 'Shot':
                    self.shotTreeClicked()
                elif flag == 'Asset':
                    self.assetTreeClicked()
                else:
                    self.taskTreeClicked()
            else:
                self.select()
    
    def searchTab(self):
        userInput = self.searchSA.text()
        selectTab = self.tabWidget.currentIndex()
        self.List.clear()
        if userInput != '':
            if selectTab == 0:
                queryData = self.filterAsset(userInput)
                self.assetTree.clear()
                self.treeForAsset(self.assetTree,queryData)
                self.assetTree.expandAll()
            if selectTab == 1:
                queryData = self.filterShot(userInput)
                self.shotTree.clear()
                self.treeForShot(self.shotTree,queryData)
                self.shotTree.expandAll()
            if selectTab == 2:
                queryEntityData = self.filterEntity(userInput)
                queryTaskData = self.filterTask(userInput)
                self.taskTree.clear()
                if len(queryEntityData) > 0: 
                    self.treeForTask(self.taskTree,queryEntityData,self.entityByStepData,self.taskData)
                elif len(queryTaskData)> 0:
                    self.treeForTask(self.taskTree,self.entityData,self.entityByStepData,queryTaskData)
                    
                self.taskTree.expandAll()        
        else:
            if selectTab == 0:
                self.assetTree.clear()
                self.treeForAsset(self.assetTree,self.assetData)
            elif selectTab == 1:
                self.shotTree.clear()
                self.treeForShot(self.shotTree,self.shotData)
            else:
                self.taskTree.clear()
                self.treeForTask(self.taskTree,self.entityData,self.entityByStepData,self.taskData)
    
    def searchFile(self):
        selectTab = self.tabWidget.currentIndex()
        userInput = self.searchPublish.text()
        if self.List.count() > 0:
            searchData = self.filterPublishfile(userInput,self.List)
            self.List.clear()
            if userInput != '':
                for index,content in enumerate(searchData):
                    newItem = QtGui.QListWidgetItem()
                    imageId = content[1]
                    if imageId == None:
                        imageId = ''
                    elif content[2] == None:
                        imgPath = path.iconForFile
                    else:
                        imgPath = Fun().getImgPath(imageId,content[u'id'],'Work',path.publishImgPath)
                    newItem.setIcon(QtGui.QPixmap(imgPath))
                    self.List.setIconSize(QtCore.QSize(150,150))
                    newItem.setTextAlignment(QtCore.Qt.AlignHCenter)
                    newItem.setData(QtCore.Qt.UserRole,imageId)
                    newItem.setData(QtCore.Qt.UserRole+1,content[2])
                    newItem.setData(QtCore.Qt.UserRole+2,content[3])
                    newItem.setText(content[0])
                    self.List.insertItem(index,newItem)
            else:
                self.List.clear()
                if selectTab == 0:
                    self.assetTreeClicked()
                elif selectTab == 1:
                    self.shotTreeClicked()
                else:
                    self.taskTreeClicked()
        else:
            if userInput == '':
                self.List.clear()
                if selectTab == 0:
                    self.assetTreeClicked()
                elif selectTab == 1:
                    self.shotTreeClicked()
                else:
                    self.taskTreeClicked()
        
    def selectTab(self):
        self.searchSA.clear()
        self.label.clear()
        self.List.clear()
        self.searchPublish.clear()
    
    def select(self):
        selectTab = self.tabWidget.currentIndex()
        if selectTab == 0:
            currentNode = self.assetTree.currentIndex().row()
            selectParent = self.assetTree.currentIndex().parent().row()
        elif selectTab == 1:
            currentNode = self.shotTree.currentIndex().row()
            selectParent = self.shotTree.currentIndex().parent().row()
        else:
            currentNode = self.taskTree.currentIndex().row()
            selectParent = self.taskTree.currentIndex().parent().parent().row()
            
        listIndex = self.List.currentIndex().row()
        userInput = self.searchSA.text()
        info = {'tab':str(selectTab),'parent':str(selectParent),'currentNode':str(currentNode),
                'listIndex':str(listIndex),'text':userInput}
        xml.writeSelectedRef(info)
        self.downloadPublish()
        self.close()
        
    def filterAsset(self,userinput):
        queryData = {}
        pattern = '.*?'.join(userinput)   
        regex = re.compile(pattern)
        data =  collections.OrderedDict(sorted((self.assetData).items(),key = lambda t:t[1])) 
        for (key,value) in data.items():
            suggestions= []
            for content in value:
                itemId = content['id']
                itemName = content['name']
                itemType = content['asset_type']
                match1 = regex.search(key)
                match2 = regex.search(itemName)
                if match2:
                    suggestions.append({u'id':itemId,u'name':itemName,u'asset_type':itemType})
                    queryData[key] = suggestions
                else:
                    if match1:
                        queryData[key] = value
        return queryData
       
    def filterShot(self,userinput):
        queryData = {}
        pattern = '.*?'.join(userinput)   
        regex = re.compile(pattern)
        data =  collections.OrderedDict(sorted((self.shotData).items(),key = lambda t:t[1])) 
      
        for (key,value) in data.items():
            suggestions= []
            for content in value:
                itemId = content['id']
                itemName = content['name']
                itemSeqId = content['sequence_id']
                itemSeqName = content['sequence_name']
                match1 = regex.search(value[0]['sequence_name'])
                match2 = regex.search(itemName)
                if match2:
                    suggestions.append({u'id':itemId,u'name':itemName,u'sequence_id':itemSeqId,u'sequence_name':itemSeqName})
                    queryData[value[0]['sequence_name']] = suggestions
                else:
                    if match1:
                        queryData[value[0]['sequence_name']] = value
        return queryData
    
    def filterTask(self,userinput):
        suggestions = []
        pattern = '.*?'.join(userinput)   
        regex = re.compile(pattern)
        for content in self.taskData:
            itemId = content['task_id']
            itemEntityType = content['entity_type']
            itemEntityId = content['entity_id']
            itemStepId = content['step_id']
            itemName = content['name']
            match = regex.search(itemName)
            if match:
                suggestions.append({u'task_id':itemId,u'entity_id':itemEntityId,u'entity_type':itemEntityType,u'name':itemName,u'step_id':itemStepId})
                    
        return suggestions
    
    def filterStep(self,userinput):
        suggestions = []
        pattern = '.*?'.join(userinput)   
        regex = re.compile(pattern)
        for content in self.entityByStepData:
            itemId = content['step_id']
            itemEntityType = content['entity_type']
            itemEntityId = content['entity_id']
            itemName = content['step_name']
            match = regex.search(itemName)
            if match:
                suggestions.append({u'step_id':itemId,u'entity_id':itemEntityId,u'entity_type':itemEntityType,u'step_name':itemName})
        return suggestions
    
    def filterEntity(self,userinput):
        suggestions = []
        pattern = '.*?'.join(userinput)   
        regex = re.compile(pattern)
        for content in self.entityData:
            itemId = content['entity_id']
            itemType = content['entity_type']
            itemName = content['entity_name']
            name = itemType + ' ' + itemName
            match = regex.search(name)
            if match:
                suggestions.append({u'entity_id':itemId,u'entity_type':itemType,u'entity_name':itemName})
        return suggestions
    
    def filterPublishfile(self,userinput,sourceList):
        suggestions = []
        pattern = '.*?'.join(userinput)   
        regex = re.compile(pattern)
        rows = sourceList.count()
        for rows_index in range(rows):
            itemName = sourceList.item(rows_index).text()
            txt = sourceList.item(rows_index).data(QtCore.Qt.UserRole+1)
            if txt not in ('Shot','Asset'):
                imagePath = txt
                imageID = sourceList.item(rows_index).data(QtCore.Qt.UserRole)
                itemID = sourceList.item(rows_index).data(QtCore.Qt.UserRole+2)
            else:
                imagePath = None
                imageID = ''
                itemID = sourceList.item(rows_index).data(QtCore.Qt.UserRole)
            match = regex.search(itemName) 
            if match:
                suggestions.append((len(match.group()),match.start(),(itemName,imageID,imagePath,itemID)))
        return [x for _, _, x in sorted(suggestions)]
    
    def downloadPublish(self):
        pushFileName = self.List.currentIndex().data()
        selectRow = self.List.currentIndex().row()
        selectedID = self.List.item(selectRow).data(QtCore.Qt.UserRole+2)
        filePath =  path.downloadRefFile
        filePath = filePath  + '/'
        if not os.path.exists(filePath):
            os.makedirs(filePath)
            
        referenceData = Data().getReferenceVersion(str(selectedID))
        if len(referenceData)>0:
            for content in referenceData:
                Data().downLoad('version/'+ str(content['attachment_id']) +'/'+ content['filename'], (filePath+content['filename']))
        fullPath = filePath + pushFileName
        Data().downLoad('version/'+ str(selectedID) +'/'+ pushFileName, fullPath)
        cmds.file(fullPath,reference = True) 
        
    def doubleClicked(self):
        selectTab = self.tabWidget.currentIndex()
        if selectTab == 0:
            self.double(self.assetTree,'Asset')
        elif selectTab == 1:
            self.double(self.shotTree,'Shot')
        else:
            self.double(self.taskTree,'Task')            
    
    def setTreeSelected(self,tree,selectParent,selectRow,selectTab):
        index = QtCore.QModelIndex(tree.model().index(selectParent,0,QtCore.QModelIndex()))
        indexChild = QtCore.QModelIndex(tree.model().index(selectRow,0,index))
        tree.setCurrentIndex(indexChild)
        if selectTab == 2:
            tree.expandItem(tree.currentItem())
            tree.setCurrentItem(tree.currentItem().child(selectRow))
            
    def bindingPubilshFile(self,taskData):
        for taskContent in taskData:
            workFile = Data().selectWorkFile(str(taskContent['id']), 'Task', '')
            for index,workContent in enumerate(workFile):
                newItem = QtGui.QListWidgetItem()
                imageId = workContent[u'image_id']
                if imageId == None:
                    imageId = ''
                imgPath = Fun().getImgPath(imageId,workContent[u'id'],'Work',path.publishImgPath)
                newItem.setIcon(QtGui.QPixmap(imgPath))
                self.List.setIconSize(QtCore.QSize(150,150))
                newItem.setData(QtCore.Qt.UserRole,imageId)
                newItem.setData(QtCore.Qt.UserRole+1,imgPath)
                newItem.setData(QtCore.Qt.UserRole+2,workContent['id'])
                newItem.setData(QtCore.Qt.UserRole+3,workContent['created_at'])
                newItem.setText(workContent['code'])
                self.List.insertItem(index, newItem)
    
    def setStatus(self,filePath):
        x = xml.readXmlForRef(filePath)
        tab = int(x['tab'])
        parent = int(x['parent'])
        selectedNode = int(x['selectedNode'])
        listIndex = int(x['listIndex'])
        inputText = x['inputText']
        self.tabWidget.setCurrentIndex(tab)
        if inputText != None:
            self.searchSA.setText(inputText)
        if tab == 0:
            self.setTreeSelected(self.assetTree,parent,selectedNode,tab)
            self.assetTreeClicked()
        elif tab == 1:
            self.setTreeSelected(self.shotTree,parent,selectedNode,tab)
            self.shotTreeClicked()
        else:
            self.setTreeSelected(self.taskTree,parent,selectedNode,tab)
            self.taskTreeClicked()
        
        index = QtCore.QModelIndex(self.List.model().index(listIndex))
        self.List.setCurrentIndex(index)   
        