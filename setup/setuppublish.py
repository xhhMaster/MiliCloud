# -*- coding: utf-8 -*-
from PySide import QtGui,QtCore
from ui.publish_ui import Ui_Widget
import os
import maya.cmds as cmds
import time
from common.datacommon import Data 
from common.uicommon import UI
from common.uicommon import Msg
import conf.msgconfig as suggestion
import conf.pathConfig as pConf

class Widget(QtGui.QWidget, Ui_Widget):
    def __init__(self,uid,parent=None):
        super(Widget,self).__init__(parent)
        self.uid = str(uid)
        self.setupUi(self)  
        self.__ImageBox()
        self.savePath = None
        self.comboBoxForProject()
        self.comboBoxForType()
        self.comboBoxForTask()
        self.FileTxt.setMinimumWidth(500)
        self.warning = UI().initMessageBox()
        self.projectComboBox.currentIndexChanged.connect(self.comboBoxForType)
        self.projectComboBox.currentIndexChanged.connect(self.comboBoxForTask)
        self.typeComboBox.currentIndexChanged.connect(self.comboBoxForTask)
        self.publishBtn.clicked.connect(self.publish)
        self.cancelBtn.clicked.connect(self.cancelBtnClicked)
  
    def cancelBtnClicked(self):
        self.close()
      
    def save(self):
        if self.__preSave():
            resultFile = os.path.exists(self.fullpath)
            remark = self.contentTxt.toPlainText()
            self.warning.setIcon(QtGui.QMessageBox.Critical)     
            if self.savePath == None:
                Msg().showDialog(self.warning,suggestion.warning,suggestion.publishFailed,suggestion.imgContent)
                return False
            if resultFile:
                Msg().showDialog(self.warning,suggestion.warning,suggestion.publishFailed,suggestion.fileRename)
                return False
            if remark == '':
                Msg().showDialog(self.warning,suggestion.warning,suggestion.publishFailed,suggestion.remarkContent)
                return False
            else:   
                cmds.file(rename = self.fullpath)
                cmds.file(save =1,type='mayaBinary')
                self.warning.setIcon(QtGui.QMessageBox.NoIcon)
                Msg().showDialog(self.warning,suggestion.prompt,suggestion.publishSucessed,'')
                return True
        else:
            return False    
        
    def publish(self):
        if self.save():
            self.addImg()
            self.addVersion()
            import service.publishservice as publishservice
            path = pConf.publishFilePath + self.VersionID
            imgPath = pConf.publishImgPath + self.ImageID
            publishservice.Publish().callService(self.fullpath,path)
            publishservice.Publish().callService(self.savePath,imgPath)
            self.close()
            
    def addVersion(self):
        data = {}
        data['entity_type'] = self.typeComboBox.currentText()
        data['entity_id'] = self.__getSelectedId(self.taskComboBox,self.List)
        data['content'] = self.taskComboBox.currentText()
        data['code'] = self.FileTxt.text() + '.mb'
        data['image_id']= self.ImageID
        data['description'] = self.contentTxt.toPlainText()
        data['project_id'] = self.__getSelectedId(self.projectComboBox,self.projectList)
        data['file_type'] = 'mb'
        data['file_size'] = '100'
        data['user_id'] = self.uid
        data['created_by_id'] = self.uid
        data['updated_by_id'] = ''
        self.VersionID = Data().addVersion(data)
        
        
    def addImg(self):
        data = {}
        data['the_file'] = self.FileTxt.text()+'.png'
        data['mime_type'] = 'image/png'
        data['file_type'] = 'png'
        self.ImageID = Data().addImg(data)
       
    #绑定项目名
    
    def comboBoxForProject(self):
        self.projectComboBox.setMinimumWidth(500)
        data = Data().getProject()
        self.projectList = UI().initTableWidget(['ID','Name'],2)
        self.__addItem(data,self.projectList,self.projectComboBox,suggestion.projectContent,'Project')
    
    
        
    #绑定类型名
    def comboBoxForType(self):
        self.typeComboBox.setMinimumWidth(500)
        self.typeComboBox.clear()
        projectName = self.projectComboBox.currentText()
        if projectName != suggestion.projectContent:
            self.typeComboBox.insertItem(0,'Task')
        else:  
            self.typeComboBox.insertItem(0,suggestion.selectProject)
    
    #绑定镜头号或者资产名
    def comboBoxForTask(self):
        self.taskComboBox.setMinimumWidth(500)
        self.taskComboBox.clear()
        self.List = UI().initTableWidget(['ID','Name'],2)
        pid = self.__getSelectedId(self.projectComboBox,self.projectList)
        data = Data().getMyTask(self.uid,pid, '')
        if data != -1: 
            self.__addItem(data,self.List,self.taskComboBox,suggestion.taskContent,'Task')
        else:
            self.taskComboBox.insertItem(0,suggestion.typeContent)
            return False
      
    #获得选中值ID
    def __getSelectedId(self,comboBox,inputList):
        txt = comboBox.currentText()
        if txt != suggestion.projectContent:
            selectedRow = comboBox.currentIndex()
            selectedId = inputList.item(selectedRow,0).text()
        else:
            selectedId = -1
        return selectedId
    
    def __addItem(self,sourceData,ouputList,comboBox,txt,flag):
        if len(sourceData) > 0:
            self.__bindingData(sourceData,ouputList,comboBox,flag)     
        else:
            comboBox.insertItem(0,txt)
    
    def __bindingData(self,sourceData,outputList,comboBox,flag):
        for index,content in enumerate(sourceData):
            outputList.insertRow(index)  
            if flag == 'Task':
                itemId = QtGui.QTableWidgetItem(str(content['task_id']))
            else:
                itemId = QtGui.QTableWidgetItem(content['id'])
            itemName = QtGui.QTableWidgetItem(content['name'])
            outputList.setItem(index,0,itemId)
            outputList.setItem(index,1,itemName)
            outputList.setColumnHidden(0,True)
            comboBox.setModel(outputList.model())
        comboBox.setModelColumn(1)
        comboBox.setView(outputList)  
    
    def getSourceData(self):
        ptype = self.typeComboBox.currentText()
        pid = self.__getSelectedId(self.projectComboBox,self.projectList)
        data = ''
        if ptype == 'Shot':
            data = Data().getShot(pid)
        if ptype == 'Asset':
            data = Data().getAsset(pid)
        if ptype != 'Shot' and ptype != 'Asset':
            data = -1
        return data
    
    def __ImageBox(self):
        self.imageBtn = QtGui.QPushButton()
        self.imageBtn.setMaximumSize(580,160)
        self.imageBtn.setMinimumSize(580,160)
        self.imageBtn.setIcon(QtGui.QIcon(pConf.iconForScreenBtn))
        self.imageBtn.setIconSize(QtCore.QSize(580, 100))
        self.imageBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.imageBtn.clicked.connect(self.grapWindowScreen)
        Layout = QtGui.QVBoxLayout()
        Layout.addWidget(self.imageBtn)
        self.imageBox.setLayout(Layout)
        
    def grapWindowScreen(self):
        self.fullScreenLabel = QtGui.QLabel()
        fullScreenPixmap = QtGui.QPixmap.grabWindow(QtGui.QApplication.desktop().winId())
        self.fullScreenLabel.setPixmap(fullScreenPixmap)
        myCursor = QtGui.QCursor(QtGui.QPixmap(pConf.iconForCursor),-1,-1);
        self.fullScreenLabel.setCursor(myCursor)
        self.fullScreenLabel.showFullScreen()
        self.fullScreenLabel.mousePressEvent = lambda event: self.screenShotPressEvent(event)
        self.fullScreenLabel.mouseMoveEvent = lambda event: self.screenShotMoveEvent(event)
        self.fullScreenLabel.mouseReleaseEvent = lambda event: self.screenShotReleaseEvent(event)
        
    def screenShotPressEvent(self,event):
        #True 鼠标左键按下且按键还未弹起
        if event.button() == QtCore.Qt.LeftButton and event.type() == QtCore.QEvent.MouseButtonPress:
            #鼠标左键标志位按下
            self.leftMousePress = True
            #获取鼠标点
            self.origin = event.pos()
            self.rubberBand = QtGui.QRubberBand(QtGui.QRubberBand.Rectangle,self.fullScreenLabel)
            self.rubberBand.setGeometry(QtCore.QRect(self.origin,QtCore.QSize()))
            self.rubberBand.show()
            return True
        
    def screenShotMoveEvent(self,event):
        #True 鼠标左键按下并拖动
        if event.type() == QtCore.QEvent.MouseMove and self.leftMousePress:
            self.rubberBand.setGeometry(QtCore.QRect(self.origin,event.pos()).normalized())
            return True
        
    def screenShotReleaseEvent(self,event):
        #鼠标左键松开
        if event.button() == QtCore.Qt.LeftButton and event.type() == QtCore.QEvent.MouseButtonRelease:
            #鼠标标志位弹起
            self.leftMousePress = False  
             
            #获取橡皮筋框的终止坐标
            termination = event.pos()
            rect = QtCore.QRect(self.origin,termination)
            
            #根据橡皮筋框截取全屏上的信息，并将其放入shotScreenLabel
            self.shotScreenLabel = QtGui.QLabel()
            pixmap = QtGui.QPixmap.grabWidget(self.fullScreenLabel,rect.x(),rect.y(),rect.width(),rect.height())
            #self.shotScreenLabel.setPixmap(pixmap)
            path = self.__getImageSavePath()
            pixmap.save(path)
            self.imageBtn.setIcon(pixmap)
            self.imageBtn.setIconSize(QtCore.QSize(rect.width()/3, rect.height()/3))
            #将shotScreenLabel的用户区大小固定为所截图片大小
            #self.shotScreenLabel.setFixedSize(rect.width(), rect.height())
           
            self.rubberBand.hide()
            self.fullScreenLabel.hide()
          
            return True       
    
    def __customSaveFileInfo(self):
        fileInfo = {}
        fileInfo['createDate'] = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        #项目名称
        fileInfo['projectName'] = self.projectComboBox.currentText() 
        #所属类型
        fileInfo['ptype'] = self.typeComboBox.currentText()
        #镜头号或者资产名
        fileInfo['content'] = self.taskComboBox.currentText()
        
        fileInfo['name'] = self.FileTxt.text()
        
        return fileInfo
        
    def __getImageSavePath(self):
        FileInfo = self.__customSaveFileInfo()
        self.savePath = ('D:/MayaLocalFile/Image/' + FileInfo['createDate'] + '/'
                     + FileInfo['projectName'] + '/' + FileInfo['ptype'] 
                     + '/' + FileInfo['content']
                     )
        
        self.saveSubPath = ('Image/' + FileInfo['createDate'] + '/'
                     + FileInfo['projectName'] + '/' + FileInfo['ptype'] 
                     + '/' + FileInfo['content']
                     )
        
        resultDir = os.path.exists(self.savePath)
        if not resultDir:
            os.makedirs(self.savePath)
        if FileInfo['name'] != '' :
            self.savePath = self.savePath + '/' + FileInfo['name'] + '.png'
        else:
            self.savePath =  self.savePath + '/default.png'  
        return self.savePath
      
    def __preSave(self):
        self.path = 'D:/MayaLocalFile/Sence/'
        fileInfo = self.__customSaveFileInfo()
        if (fileInfo['projectName'] != suggestion.projectContent and 
            fileInfo['name'] != '' and 
            fileInfo['content'] != suggestion.taskContent):
            
            self.path = (self.path + fileInfo['createDate'] + '/' 
                         + fileInfo['projectName'] + '/' 
                         + fileInfo['ptype'] + '/'
                         + fileInfo['content'])
            
            self.subPath = ('Sence/'+fileInfo['createDate'] + '/' 
                            + fileInfo['projectName'] + '/' 
                            + fileInfo['ptype'] + '/' 
                            + fileInfo['content'])
            
            self.fullpath = self.path +'/' + fileInfo['name']
            
            resultDir = os.path.exists(self.path)
            if not resultDir:
                os.makedirs(self.path)
                
            return True
        else:                               
            if fileInfo['projectName'] == suggestion.projectContent:
                txtSubContent = suggestion.selectProject
            elif fileInfo['content'] == suggestion.taskContent:
                txtSubContent = suggestion.selectTask
            else:
                txtSubContent = suggestion.fileNameIsNull
            self.warning.setIcon(QtGui.QMessageBox.Critical)     
            Msg().showDialog(self.warning,suggestion.warning,suggestion.publishFailed, txtSubContent)
            return False    
        
