# -*- coding: utf-8 -*-
from PySide import QtGui,QtCore
from ui.selectworkfiles_ui import Ui_Widget
import re
import maya.cmds as cmds
import os

class Widget(QtGui.QWidget, Ui_Widget):
    
    def __init__(self,pid,desc,content,parent=None):
        super(Widget,self).__init__(parent)
        self.pid = pid
        self.desc = desc
        self.content = content
        self.shotFiter = QtGui.QLabel('Shot')
        self.assetFiter = QtGui.QLabel('Asset')
        self.searchAssetList = self.__initTableWidget()
        self.searchShotList = self.__initTableWidget()
        self.mainLayout = QtGui.QVBoxLayout()
        self.setupUi(self)   
        self.warning = self.__initMessageBox()
        self.projectNameEdit.setText(self.content)
        self.projectDescEdit.setText(self.desc)
        self.searchShots.textChanged.connect(self.__inputTxtChanged)
        self.searchTasks.textChanged.connect(self.__inputTaskTxtChanged)
        self.ShotAndAsset()
        self.taskList = QtGui.QListWidget()
        self.shotList.clicked.connect(self.__bindingTaskForShot)
        self.assetList.clicked.connect(self.__bindingTaskForAsset)
        self.searchShotList.clicked.connect(self.__bindingTaskForSearchShot)
        self.searchAssetList.clicked.connect(self.__bindingTaskForSearchAsset)
        self.selBtn.clicked.connect(self.openSelectedFile)
        self.createBtn.clicked.connect(self.createClicked)
        self.cancelBtn.clicked.connect(self.cancelClicked)
        
    #点击新建按钮触发的事件    
    def createClicked(self):
        import setup.setupnewtask as setupnewtask    
        setupnewtask.Widget()
        self.close()
       
        
    #点击取消按钮触发的事件    
    def cancelClicked(self):
        self.close()

    def ShotAndAsset(self):   
        self.shotLabel = QtGui.QLabel('Shot')
        self.mainLayout.addWidget(self.shotLabel)
        self.__bindingShotData()
        self.mainLayout.addWidget(self.shotList)
        
        self.assetLabel = QtGui.QLabel('Asset')
        self.mainLayout.addWidget(self.assetLabel)
        self.__bindingAssetData()
        self.mainLayout.addWidget(self.assetList)
       
        self.shotScrollArea.setLayout(self.mainLayout)
      
    def __bindingTaskForShot(self):
        selectedRow = self.shotList.currentItem().row()
        selectedId = self.shotList.item(selectedRow,0).text()
        selectedType = self.shotList.item(selectedRow,2).text()
        self.__getTaskData(selectedId,selectedType)
        
    def __bindingTaskForAsset(self):
        selectedRow = self.assetList.currentItem().row()
        selectedId = self.assetList.item(selectedRow,0).text()
        selectedType = self.assetList.item(selectedRow,2).text()
        self.__getTaskData(selectedId,selectedType)
    
    def __initTableWidget(self):
        header = ['ID','Name','Type']
        List = QtGui.QTableWidget()
        List.setHorizontalHeaderLabels(header)   
        List.setColumnCount(3)
        List.verticalHeader().setVisible(False)
        List.horizontalHeader().setVisible(False)
        List.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        List.setShowGrid(False)
        List.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        List.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        List.horizontalHeader().setStretchLastSection(True)
        return List
    
    def __getShotData(self):
        import service.shotservice as shotservice
        shotContents = shotservice.Shot().callService(self.pid)
        return shotContents
    
    def __getAssetData(self):
        import service.assetservice as assetservice
        assetContents = assetservice.Asset().callService(self.pid)
        return assetContents  
     
    def __getTaskData(self,entity_id,entity_type):
        #导入TaskService
        import service.workfilesservice as workfilesservice
        contents = workfilesservice.Task().callService(entity_id,entity_type)  
        self.taskList = QtGui.QListWidget()    
        self.taskList.clear()
        if len(contents) > 0:
            for content in contents:        
                QtGui.QListWidgetItem(content['code'],self.taskList)
            self.tasksScrollArea.setWidget(self.taskList)
        else:
            QtGui.QListWidgetItem(u'没有相关Task',self.taskList)
            self.tasksScrollArea.setWidget(self.taskList)
            
    def __bindingShotData(self):
        self.shotList = self.__initTableWidget()
        shotData = self.__getShotData()
        self.__bindingData(shotData,self.shotList,'Shot')
        
    def __bindingAssetData(self):
        self.assetList = self.__initTableWidget()
        assetData = self.__getAssetData()
        self.__bindingData(assetData,self.assetList,'Asset')                
    
    def __fiter(self,user_input,List):
        suggestions = []
        pattern = '.*?'.join(user_input)   
        regex = re.compile(pattern)
        rows = List.rowCount()
        for rows_index in range(rows):
            itemId = List.item(rows_index,0).text()
            itemName = List.item(rows_index,1).text()
            itemType = List.item(rows_index,2).text()
            match = regex.search(itemName) 
            if match:
                suggestions.append((len(match.group()), match.start(), (itemId,itemName,itemType)))
        return [x for _, _, x in sorted(suggestions)]
    
    def __fiterForTask(self,user_input,List):
        suggestions = []
        pattern = '.*?'.join(user_input)   
        regex = re.compile(pattern)
        rows = List.count()
        for rows_index in range(rows):
            item = List.item(rows_index).text()
            match = regex.search(item) 
            if match:
                suggestions.append((len(match.group()), match.start(), item))
        return [x for _, _, x in sorted(suggestions)]
    
    def __inputTxtChanged(self):
        userInput = self.searchShots.text()  
        self.searchTaskList = QtGui.QListWidget()     
        if userInput != '':
            self.__searchData(userInput)
            if self.searchShotList.currentIndex().row() == -1:
                self.searchTasks.clear()
                QtGui.QListWidgetItem(u'没有相关Task',self.searchTaskList)
                self.tasksScrollArea.setWidget(self.searchTaskList)
            elif self.searchAssetList.currentIndex().row() == -1:
                self.searchTasks.clear()
                QtGui.QListWidgetItem(u'没有相关Task',self.searchTaskList)
                self.tasksScrollArea.setWidget(self.searchTaskList)
        else:
            self.searchAssetList.hide()
            self.searchShotList.hide()
            self.__showWidget()
             
    def __inputTaskTxtChanged(self):
        userInput = self.searchTasks.text()   
        self.searchTaskList = QtGui.QListWidget()
        self.searchTaskList.clear()   
        if self.shotFiter.isHidden():
            self.__resetControl()
            if userInput != '':
                self.__fiterTask(userInput,self.taskList,self.searchTaskList)
            elif self.shotList.currentIndex().row() != -1:
                self.__bindingTaskForShot()
            elif self.assetList.currentIndex().row() != -1:
                self.__bindingTaskForAsset()               
            else:
                QtGui.QListWidgetItem(u'没有相关Task',self.searchTaskList)
                self.tasksScrollArea.setWidget(self.searchTaskList)
        else:
            self.__resetSearchListControl()
            if userInput != '':
                self.__fiterTask(userInput,self.taskList,self.searchTaskList)
            elif self.searchShotList.currentIndex().row() != -1:
                self.__bindingTaskForSearchShot()
            elif self.searchAssetList.currentIndex().row() != -1:
                self.__bindingTaskForSearchAsset()
            else:
                QtGui.QListWidgetItem(u'没有相关Task',self.searchTaskList)
                self.tasksScrollArea.setWidget(self.searchTaskList)
            
    def __bindingSearchShotData(self,userInput):
        self.searchShotList.clearContents()
        self.searchShotList.setRowCount(0)
        self.__fiterData(userInput,self.shotList,self.searchShotList,'Shot')
            
    def __bindingSearchAssetData(self,userInput):
        self.searchAssetList.clearContents()
        self.searchAssetList.setRowCount(0)
        self.__fiterData(userInput,self.assetList,self.searchAssetList,'Asset')
    
    def __bindingTaskForSearchShot(self):
        selectedRow = self.searchShotList.currentItem().row()
        selectedId = self.searchShotList.item(selectedRow,0).text()
        selectedType = self.searchShotList.item(selectedRow,2).text()
        self.__getTaskData(selectedId,selectedType)

    def __bindingTaskForSearchAsset(self):
        selectedRow = self.searchAssetList.currentItem().row()
        selectedId = self.searchAssetList.item(selectedRow,0).text()
        selectedType = self.searchAssetList.item(selectedRow,2).text()
        self.__getTaskData(selectedId,selectedType)
        
    def __searchData(self,userInput):
        self.__hideWidget()
        
        self.mainLayout.addWidget(self.shotFiter)
        self.__bindingSearchShotData(userInput)
        self.mainLayout.addWidget(self.searchShotList) 
        self.searchShotList.show()
        
        self.mainLayout.addWidget(self.assetFiter)  
        self.__bindingSearchAssetData(userInput)
        self.mainLayout.addWidget(self.searchAssetList)  
        self.searchAssetList.show()
           
        self.shotScrollArea.setLayout(self.mainLayout)  
    
    def __hideWidget(self):
        self.shotFiter.show()
        self.assetFiter.show()
        self.shotLabel.hide()
        self.assetLabel.hide()
        self.shotList.hide()
        self.assetList.hide()

    def __showWidget(self):
        self.shotLabel.show()
        self.assetLabel.show()
        self.shotFiter.hide()
        self.assetFiter.hide()
        self.shotList.show()
        self.assetList.show()
    
    def __fiterData(self,userInput,sourceList,outputList,Flag):
        fiterData = self.__fiter(userInput,sourceList)
        if len(fiterData) > 0:
            for index,content in enumerate(fiterData):
                outputList.insertRow(index)
                itemId = QtGui.QTableWidgetItem(content[0])
                itemName = QtGui.QTableWidgetItem(content[1])  
                itemType = QtGui.QTableWidgetItem(content[2])
                outputList.setItem(index,0,itemId)
                outputList.setItem(index,1,itemName)
                outputList.setItem(index,2,itemType)
            outputList.setColumnHidden(0,True)
            outputList.setColumnHidden(2,True)
            
        else:
            outputList.setRowCount(3)
            outputList.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
            outputList.setColumnHidden(0,False)
            outputList.setColumnHidden(2,False)
            outputList.setSpan(2, 1, 3, 3)
            if Flag == 'Shot':
                Flag =u"没有Shot相关内容"
            else:
                Flag = u"没有Asset相关内容"
            msg = QtGui.QTableWidgetItem(Flag)
            outputList.setItem(2,1,msg) 
            outputList.setFocusPolicy(QtCore.Qt.NoFocus) 
         
    def __bindingData(self,sourceData,outputList,Flag):
        if len(sourceData) > 0:
            for index,content in enumerate(sourceData):
                outputList.insertRow(index)    
                itemId = QtGui.QTableWidgetItem(content['id'])
                itemName = QtGui.QTableWidgetItem(content['name'])
                itemType = QtGui.QTableWidgetItem(Flag)
                outputList.setItem(index,0,itemId)
                outputList.setItem(index,1,itemName)
                outputList.setItem(index,2,itemType)
            outputList.setColumnHidden(0,True)
            outputList.setColumnHidden(2,True)
            index = QtCore.QModelIndex()
            outputList.setCurrentIndex(index)
        else:
            outputList.setRowCount(3)
            outputList.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
            outputList.setSpan(2, 1, 3, 3)
            if Flag == 'Shot':
                Flag =u"没有Shot相关内容"
            else:
                Flag = u"没有Asset相关内容"
            msg = QtGui.QTableWidgetItem(Flag)
            outputList.setItem(2,1,msg) 
            outputList.setFocusPolicy(QtCore.Qt.NoFocus)  
 
    def __fiterTask(self,userInput,sourceList,outputList):
        fiterData = self.__fiterForTask(userInput,sourceList)
        if len(fiterData) > 0:
            for content in fiterData:        
                QtGui.QListWidgetItem(content,outputList)
            self.tasksScrollArea.setWidget(outputList)
        else:
            QtGui.QListWidgetItem(u'没有相关Task',outputList)
            self.tasksScrollArea.setWidget(outputList) 
    
    #重置QListWidget
    def __resetControl(self):
        if self.shotList.currentIndex().row() != -1:
            self.__bindingTaskForShot()
        elif self.assetList.currentIndex().row() != -1:
            self.__bindingTaskForAsset()                
        else:
            self.taskList = QtGui.QListWidget()
    
    def __resetSearchListControl(self):
        if self.searchShotList.currentIndex().row() != -1:
            self.__bindingTaskForSearchShot()
        elif self.searchAssetList.currentIndex().row() != -1:
            self.__bindingTaskForSearchAsset()
        else:
            self.taskList = QtGui.QListWidget()
    
    def openSelectedFile(self):
        fileName = self.taskList.currentIndex().data()
        if fileName  != None: 
            filePath = 'd:/mayaDownload/'
            pathDir = os.path.exists(filePath)
            if not pathDir:
                os.makedirs(filePath)
                
            import service.downloadservice as downloadservice
            downloadservice.DownLoad().callService(filePath+fileName,fileName)
            cmds.file(filePath+fileName,f = 1,type='mayaBinary',o = 1) 
        else:
            txt = u'请选择工作文件！'
            self.showWarningDialog(txt)
    
    def __initMessageBox(self):
        warning = QtGui.QMessageBox()
        okBtn = warning.addButton(u'确定',QtGui.QMessageBox.AcceptRole)
        okBtn.clicked.connect(warning.close)
        return warning 
    
    def showWarningDialog(self,txt):
        self.warning.setWindowTitle(u'警告信息')
        self.warning.setIcon(QtGui.QMessageBox.Critical)
        self.warning.setText(u"  打开失败！                                                                    ")
        self.warning.setInformativeText("  " + txt)
        self.warning.show() 