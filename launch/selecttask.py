# -*- coding: utf-8 -*-
from PySide import QtGui,QtCore
from ui.selecttask_ui import Ui_Widget
from common.datacommon import Data 
from common.uicommon import UI
from common.uicommon import Msg
from common.funcommon import Fun
import conf.msgsetting as suggestion
import conf.path as path
import re


class Widget(QtGui.QWidget, Ui_Widget):
    def __init__(self,pid,uid,userName,parent=None):
        super(Widget,self).__init__(parent)
        #初始化 项目id,用户id,用户名三个字段
        self.pid = pid
        self.uid = str(uid)
        self.useName = userName
        #初始化shotList、assetList、cacheShotList、cacheAssetList、taskList五个列表
        #其中cacheShotList、cacheAssetList用来保存临时数据用于搜索框查找
        self.shotList = UI().initListWidget()
        self.assetList = UI().initListWidget()
        self.taskList = UI().initListWidget()
        #初始化ui
        self.setupUi(self)
        
        #设置（shot or asset）搜索框样式  和 task搜索框样式
        self.searchSA.setStyleSheet("background-image: url("+ path.iconForSearch + ");\n"
                                    "background-repeat: no-repeat;\n"
                                    "background-position: center left;\n"
                                    "border-style: inset; \n"
                                    "border-radius: 9px; \n"
                                    "padding-left: 15px")
        self.searchTask.setStyleSheet("background-image: url("+ path.iconForSearch +");\n"
                                    "background-repeat: no-repeat;\n"
                                    "background-position: center left;\n"
                                    "border-style: inset; \n"
                                    "border-radius: 9px; \n"
                                    "padding-left: 15px")
        
        
       
        self.initSA()
        
        #初始化mainLayout，taskLayout两个容器
        self.mainLayout = QtGui.QVBoxLayout()
        self.taskLayout = QtGui.QVBoxLayout()
        
        self.mainLayout.addLayout(self.shotFrame)
        self.showData(self.shotList)
        self.mainLayout.addLayout(self.assetFrame)
        self.showData(self.assetList) 
        self.showTask()
        self.warning = UI().initMessageBox()
        self.warning.setIcon(QtGui.QMessageBox.Critical) 
        self.shotData = Data().getShot(self.uid,self.pid,'','')    
        self.assetData = Data().getAsset(self.uid,self.pid,'','')  
        
        self.nextStartForAsset = 0
        self.nextStartForShot = 0
        self.preStartForAsset = len(self.assetData)
        self.preStartForShot = len(self.shotData)
        self.pageValue = 3
        self.getShotPageSize()
        self.getAssetPageSize()
        self.showPage()
          
        self.ShotAndAsset()
     
        self.searchSA.textChanged.connect(self.SATxtChanged)
        self.searchTask.textChanged.connect(self.taskTxtChanged)
        self.shotList.clicked.connect(lambda:self.task(self.shotList))
        self.assetList.clicked.connect(lambda:self.task(self.assetList))
        self.backBtn.clicked.connect(self.backClicked)
        self.selBtn.clicked.connect(self.openSelectedTask)
        self.cancelBtn.clicked.connect(self.cancelClicked)
        self.previousShot.clicked.connect(lambda:self.prePage('Shot'))
        self.nextShot.clicked.connect(lambda:self.nextPage('Shot'))
        self.previousAsset.clicked.connect(lambda:self.prePage('Asset'))
        self.nextAsset.clicked.connect(lambda:self.nextPage('Asset'))
        self.moreAsset.clicked.connect(lambda:self.moreData('Asset'))
        self.moreShot.clicked.connect(lambda:self.moreData('Shot'))

        
    #点击取消按钮触发的事件    
    def cancelClicked(self):
        self.close()

    def backClicked(self):
        import launch.selectproject as selectproject
        reload(selectproject)
        self.Widget = selectproject.Widget(self.uid,self.useName)
        self.Widget.show()   
        self.close()   
    
    #绑定shot和Asset    
    def ShotAndAsset(self):
        shotData = Data().getShot(self.uid,self.pid,'0','3')
        assetData = Data().getAsset(self.uid,self.pid,'0','3')
        self.bindingData(shotData,self.shotList,'Shot')
        self.bindingData(assetData,self.assetList,'Asset')
    
    #绑定任务   
    def task(self,sourceList):
        userInput = self.searchTask.text()  
        self.taskList.clear()
        self.searchTask.clear()
        if userInput == '':
            self.getTask(sourceList)
        else:
            self.taskTxtChanged()
    
    #获取任务      
    def getTask(self,sourceList):
        selectedRow = sourceList.currentIndex().row()
        self.selectedId = sourceList.item(selectedRow).data(QtCore.Qt.UserRole)
        self.selectedType = sourceList.item(selectedRow).data(QtCore.Qt.UserRole+1)
        if self.selectedType == 'Shot':
            self.assetList.clearSelection()
        if  self.selectedType == 'Asset':
            self.shotList.clearSelection()
        self.taskData = Data().getTask(str(self.selectedId),self.selectedType,self.uid,self.pid)
        self.bindingData(self.taskData,self.taskList,'Task')
    
    #资产或镜头搜索框触发事件
    def SATxtChanged(self):
        userInput = self.searchSA.text() 
        self.searchTask.clear()
        self.taskList.clear()
        
        if userInput != '':
            self.previousShot.setEnabled(False)
            self.nextShot.setEnabled(False)
            self.moreShot.setEnabled(False)
            self.previousAsset.setEnabled(False)
            self.nextAsset.setEnabled(False)
            self.moreAsset.setEnabled(False)
            
            self.bindindSearchData(userInput,self.shotList,'Shot')
            self.bindindSearchData(userInput,self.assetList,'Asset')
        else:
            self.currentPageForShot = 1
            self.currentPageForAsset = 1
            if self.nextAsset.isEnabled() or self.nextShot.isEnabled():
                self.ShotAndAsset()
            else:
                self.moreData('Shot')
                self.moreData('Asset')
                
    #任务搜索框触发事件     
    def taskTxtChanged(self):
        userInput = self.searchTask.text()
        if userInput != '':
            if (self.shotList.currentIndex().row() != -1 or
                self.assetList.currentIndex().row() != -1 ):
                self.bindindSearchData(userInput,self.taskList,'Task')
            else:
                self.bindingData('',self.taskList,'Task')
        else: 
            self.resetUI()
    
    #重置TaskUI
    def resetUI(self):
        self.taskList.clear()
        if self.shotList.currentIndex().row() != -1:
            self.getTask(self.shotList)
        elif self.assetList.currentIndex().row() != -1:
            self.getTask(self.assetList)
        else:
            self.bindingData('',self.taskList,'Task')
    
    #选择任务事件   
    def openSelectedTask(self):
        selectedRow = self.taskList.currentIndex().row()
        if selectedRow != -1:
            selectedTaskID = self.taskList.item(selectedRow).data(QtCore.Qt.UserRole)
            import launch.selectworkfile as selectworkfile
            self.Widget = selectworkfile.Widget(self.uid,self.pid,str(self.selectedId),self.selectedType,str(selectedTaskID),self.useName)
            self.Widget.show()   
            self.close()  
        else:
            Msg().showDialog(self.warning,suggestion.warning,suggestion.clickedFailed,suggestion.selectTask)
    
    #显示shot or asset列表
    def showData(self,outputList):
        self.mainLayout.removeWidget(outputList)
        self.mainLayout.addWidget(outputList)
        self.scrollAreaForSA.setLayout(self.mainLayout)
    
    #显示task列表
    def showTask(self):
        self.taskLayout.addWidget(self.taskList)
        self.scrollAreaForTask.setLayout(self.taskLayout)
    
    
    #绑定查找后的数据源
    def bindindSearchData(self,userInput,outputList,Flag):
        if Flag == 'Shot': 
            resultData = self.filterData(userInput,self.shotData,Flag)
        elif Flag == 'Asset':
            resultData = self.filterData(userInput,self.assetData,Flag)
        else:
            resultData = self.filterData(userInput,self.taskData,Flag)
        self.bindingData(resultData,outputList,Flag)

    def initSA(self):
        self.shotLabel = QtGui.QLabel('Shot')
        self.nextShot = QtGui.QPushButton(u'下一页')
        self.previousShot = QtGui.QPushButton(u'上一页')
        self.moreShot = QtGui.QPushButton(u'全部')
        self.shotFrame = QtGui.QHBoxLayout()
        self.shotFrame.addWidget(self.shotLabel)
        self.shotFrame.addWidget(self.previousShot)
        self.shotFrame.addWidget(self.nextShot)
        self.shotFrame.addWidget(self.moreShot)
        
        self.assetLabel = QtGui.QLabel('Asset')
        self.nextAsset = QtGui.QPushButton(u'下一页')
        self.previousAsset = QtGui.QPushButton(u'上一页')
        self.moreAsset = QtGui.QPushButton(u'全部')
        self.assetFrame = QtGui.QHBoxLayout()
        self.assetFrame.addWidget(self.assetLabel)
        self.assetFrame.addWidget(self.previousAsset)
        self.assetFrame.addWidget(self.nextAsset)
        self.assetFrame.addWidget(self.moreAsset)
    
    def nextPage(self,entity_type):
        if entity_type == 'Shot':
            self.previousShot.setEnabled(True)
            self.currentPageForShot = self.currentPageForShot + 1
            if  self.currentPageForShot >= self.shotPageSize:
                self.currentPageForShot = self.shotPageSize
                self.nextShot.setEnabled(False)
            index = (self.currentPageForShot - 1)+ ((self.currentPageForShot - 1)*2)
            shotData = Data().getShot(self.uid,self.pid,str(index),str(self.pageValue))
            self.bindingData(shotData,self.shotList,entity_type)
        else:
            self.previousAsset.setEnabled(True)
            self.currentPageForAsset = self.currentPageForAsset + 1
            if  self.currentPageForAsset >= self.assetPageSize:
                self.currentPageForAsset = self.assetPageSize
                self.nextAsset.setEnabled(False)
            index = (self.currentPageForAsset - 1)+ ((self.currentPageForAsset - 1)*2)
            assetData = Data().getAsset(self.uid,self.pid,str(index),str(self.pageValue))
            self.bindingData(assetData,self.assetList,entity_type)
             
    def prePage(self,entity_type):
        if entity_type == 'Shot':
            self.nextShot.setEnabled(True)
            self.currentPageForShot = self.currentPageForShot - 1
            if self.currentPageForShot <= 1:
                self.currentPageForShot = 1
                self.previousShot.setEnabled(False)
            index = (self.currentPageForShot - 1)+ ((self.currentPageForShot - 1)*2)
            shotData = Data().getShot(self.uid,self.pid,str(index),str(self.pageValue))
            self.bindingData(shotData,self.shotList,entity_type)
        else:
            self.nextAsset.setEnabled(True)
            self.currentPageForAsset = self.currentPageForAsset - 1
            if self.currentPageForAsset <= 1:
                self.currentPageForAsset = 1
                self.previousAsset.setEnabled(False)
            index = (self.currentPageForAsset - 1)+ ((self.currentPageForAsset - 1)*2)
            assetData = Data().getAsset(self.uid,self.pid,str(index),str(self.pageValue))
            self.bindingData(assetData,self.assetList,entity_type)
           
    def moreData(self,entity_type):
        if entity_type == 'Shot':
            self.previousShot.setEnabled(False)
            self.nextShot.setEnabled(False)
            self.moreShot.setEnabled(False)
            self.shotList.clearMask()
            self.bindingData(self.shotData,self.shotList,entity_type)
        else:
            self.previousAsset.setEnabled(False)
            self.nextAsset.setEnabled(False)
            self.moreAsset.setEnabled(False)
            self.bindingData(self.assetData,self.assetList,entity_type)
    
    def bindingData(self,sourceData,outputList,Flag):
        outputList.clear()
        outputList.setSpacing(5)
        outputList.setIconSize(QtCore.QSize(122,95))
        if len(sourceData) > 0 :
            for index,content in enumerate(sourceData):
                imageId = content[u'image_id']
                if imageId == None:
                    imageId = ''
                imgPath = Fun().getImgPath(imageId,content['id'],Flag,path.publishImgPath)
                Fun().bindingList(index,content,outputList,imgPath,Flag)
            outputList.setSelectionMode(QtGui.QAbstractItemView.SingleSelection) 
        else:
            newItem = QtGui.QListWidgetItem()
            newItem.setText(suggestion.noData)
            outputList.insertItem(0,newItem)
            outputList.setSelectionMode(QtGui.QAbstractItemView.NoSelection)       
    
    def showPage(self):
        self.previousAsset.setEnabled(False)
        self.previousShot.setEnabled(False)
        if len(self.shotData) == 0 or len(self.shotData) < self.pageValue:
            self.nextShot.setEnabled(False)
        if len(self.assetData) == 0 or len(self.assetData) < self.pageValue:
            self.nextAsset.setEnabled(False)
            
    def getShotPageSize(self):
        self.currentPageForShot = 1
        self.shotPageSize = len(self.shotData) / self.pageValue
        if (len(self.shotData) % self.pageValue) > 0 :
            self.shotPageSize = self.shotPageSize + 1
    
    def getAssetPageSize(self):
        self.currentPageForAsset = 1
        self.assetPageSize = len(self.assetData) / self.pageValue
        if (len(self.assetData) % self.pageValue) > 0 :
            self.assetPageSize = self.assetPageSize + 1   
    
    def filterData(self,userinput,sourceData,Flag):
        suggestions = []
        pattern = '.*?'.join(userinput)   
        regex = re.compile(pattern)
        for content in sourceData:
            itemId = content['id']
            itemImg = content['image_id']
            itemName = content['name']
            match = regex.search(itemName)
            if match:
                if Flag == 'Task':
                    itemUser = content['user_name']
                    suggestions.append({u'id':itemId,u'name':itemName,u'image_id':itemImg,u'user_name':itemUser})
                else:
                    itemDesc = content['description']
                    suggestions.append({u'id':itemId,u'name':itemName,u'image_id':itemImg,u'description':itemDesc})           
        return suggestions
        