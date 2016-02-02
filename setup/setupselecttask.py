# -*- coding: utf-8 -*-
from PySide import QtGui
from ui.selecttask_ui import Ui_Widget
from common.datacommon import Data 
from common.uicommon import UI
from common.uicommon import Msg
from common.funcommon import Fun

class Widget(QtGui.QWidget, Ui_Widget):
    
    def __init__(self,pid,uid,parent=None):
        super(Widget,self).__init__(parent)
        self.pid = pid
        self.uid = str(uid)
        self.shotList = UI().initTableWidget(['ID','Image','Name','Type','ImgPath'],5)
        self.assetList = UI().initTableWidget(['ID','Image','Name','Type','ImgPath'],5)
        self.taskList = UI().initTableWidget(['ID','Image','Name','Type','ImgPath'],5) 
        self.setupUi(self)
        self.searchSA.setStyleSheet("background-image: url(C:/Users/HH.Pic-p-127/Documents/maya/scripts/Image/search.png);\n"
                                    "background-repeat: no-repeat;\n"
                                    "background-position: center left;\n"
                                    "border-style: inset; \n"
                                    "border-radius: 9px; \n"
                                    "padding-left: 15px")
        self.searchTask.setStyleSheet("background-image: url(C:/Users/HH.Pic-p-127/Documents/maya/scripts/Image/search.png);\n"
                                    "background-repeat: no-repeat;\n"
                                    "background-position: center left;\n"
                                    "border-style: inset; \n"
                                    "border-radius: 9px; \n"
                                    "padding-left: 15px")
        
        self.shotLabel = QtGui.QLabel('Shot')
        self.assetLabel = QtGui.QLabel('Asset')
        self.mainLayout = QtGui.QVBoxLayout()
        self.taskLayout = QtGui.QVBoxLayout()
        self.showData(self.shotList)
        self.showData(self.assetList) 
        self.showTask()
        self.warning = UI().initMessageBox()
        self.warning.setIcon(QtGui.QMessageBox.Critical)     
        self.ShotAndAsset()
        self.searchSA.textChanged.connect(self.inputSATxtChanged)
        self.searchTask.textChanged.connect(self.inputTaskTxtChanged)
        self.shotList.clicked.connect(lambda:self.task(self.shotList,self.taskList))
        self.assetList.clicked.connect(lambda:self.task(self.assetList,self.taskList))
        self.selBtn.clicked.connect(self.openSelectedTask)
        self.cancelBtn.clicked.connect(self.cancelClicked)
       
       
        
    #点击取消按钮触发的事件    
    
    def cancelClicked(self):
        self.close()

    def ShotAndAsset(self):
        queryField = ['id','name','description']
        shotData = Data().getShotInfo(self.pid)
        assetData = Data().getAssetInfo(self.pid)
        self.bindingData(shotData,self.shotList,queryField,'Shot')
        self.bindingData(assetData,self.assetList,queryField,'Asset')
    
    def task(self,sourceList,outputList):
        userInput = self.searchTask.text()  
        outputList.setRowCount(0)
        if userInput == '':
            self.getTask(sourceList,self.taskList)
        else:
            self.inputTaskTxtChanged()
          
    def getTask(self,sourceList,outputList):
        selectedRow = sourceList.currentIndex().row()
        self.selectedId = sourceList.item(selectedRow,0).text()
        self.selectedType = sourceList.item(selectedRow,3).text()
        taskData = Data().getTaskInfo(self.selectedId,self.selectedType,self.uid,self.pid)
        queryField = ['task_id','name','user_id']
        self.bindingData(taskData,outputList,queryField,'Task')
    
    def inputSATxtChanged(self):
        userInput = self.searchSA.text() 
        self.searchTask.clear()
        self.taskList.setRowCount(0)
        Fun().sourceDataISNULL(self.taskList,'Task')
        self.searchData(userInput)
       
    def searchData(self,userInput):
        self.ShotAndAsset()
        if userInput != '':
            self.getData(userInput,self.shotList,'Shot')
            self.getData(userInput,self.assetList,'Asset')
            
    def inputTaskTxtChanged(self):
        userInput = self.searchTask.text()
        ImgPath = 'C:/Users/HH.Pic-p-127/Documents/maya/scripts/Image/12.jpg'
        self.searchTaskData(userInput,ImgPath)
  
    def searchTaskData(self,userInput,ImgPath):
        self.resetControl()
        if userInput != '':
            if (self.shotList.currentIndex().row() != -1 or
                self.assetList.currentIndex().row() != -1 ):
                self.getData(userInput,self.taskList,'Task')
            else:
                self.taskList.show()
        else:     
            self.taskList.show()
           
    def resetControl(self):
        self.taskList.setRowCount(0)
        if self.shotList.currentIndex().row() != -1:
            self.getTask(self.shotList,self.taskList)
        elif self.assetList.currentIndex().row() != -1:
            self.getTask(self.assetList,self.taskList)
        else:
            Fun().sourceDataISNULL(self.taskList,'Task')
    
    def openSelectedTask(self):
        selectedRow = self.taskList.currentIndex().row()
        selectedTaskID = self.taskList.item(selectedRow,0).text()
        if selectedRow != -1:
            import setup.setupselectworkefiles as setupselectworkefiles
            self.Widget = setupselectworkefiles.Widget(self.uid,self.pid,self.selectedId,self.selectedType,selectedTaskID)
            self.Widget.show()   
            self.close()  
        else:
            txtTitle = u'警告信息'
            txtMainContent = u'打开失败！                                             '
            txtSubContent =  u'请选择一个任务文件！'
            Msg().showDialog(self.warning, txtTitle, txtMainContent, txtSubContent)
    
    def showData(self,outputList):
        self.mainLayout.removeWidget(outputList)
        self.mainLayout.addWidget(outputList)
        self.scrollAreaForSA.setLayout(self.mainLayout)
    
    def showTask(self):
        self.taskLayout.addWidget(self.taskList)
        self.scrollAreaForTask.setLayout(self.taskLayout)
    
    def bindingData(self,sourceData,outputList,queryField,Flag):
        outputList.setRowCount(0)
        if len(sourceData) > 0 :
            for index,content in enumerate(sourceData):
                imageId = content[u'image_id']
                if str(imageId) != '':
                    imgPath = Fun().getImgPath(str(imageId), 'thumbnails/')
                else:
                    imgPath = 'D:/mayaDownload/Image/000.png'
                Fun().bindingDataSingal(index,content,outputList,queryField,imgPath,Flag)
        else:
            Fun().sourceDataISNULL(outputList,Flag)
        
    def getData(self,userInput,outputList,Flag):
        if Flag == 'Shot': 
            resultData = Fun().fiterData(userInput,self.shotList)
        elif Flag == 'Asset':
            resultData = Fun().fiterData(userInput,self.assetList)
        else:
            resultData = Fun().fiterData(userInput,self.taskList)
               
        outputList.setRowCount(0)
        if len(resultData) > 0 :
            for index,content in enumerate(resultData):
                imgPath = content[3]
                Fun().bindingDataSingal(index,content,outputList,[0,1],imgPath,Flag)
        else:
            Fun().sourceDataISNULL(outputList,Flag)
