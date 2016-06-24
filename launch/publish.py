# -*- coding: utf-8 -*-
from PySide import QtGui,QtCore
from ui.publish_ui import Ui_Widget
import os,time
import maya.cmds as cmds
from common.datacommon import Data 
from common.uicommon import UI
from common.uicommon import Msg
import conf.msgsetting as suggestion
import conf.path as confPath
import common.xmlcommon as xml

class Widget(QtGui.QWidget, Ui_Widget):
    def __init__(self,uid,parent=None):
        super(Widget,self).__init__(parent)
        self.uid = str(uid)
        #初始化ui
        self.setupUi(self) 
        
        #初始化缩略图窗口
        self.__ImageBox()
    
        
        if os.path.exists(confPath.xmlForFile):
            self.x = xml.readXmlForFile(confPath.xmlForFile)
        else:
            self.x = ''
        
        #绑定项目下拉列表
        self.comboBoxForProject()
        
        #获取项目名
        projectName = self.projectComboBox.currentText()

    
        #绑定类型下拉列表
        self.comboBoxForType(projectName)
    
        
        
        #获取项目id和所属类型（shot or asset）
        self.pid = self.__getSelectedId(self.projectComboBox,self.projectList)
        ptype = self.typeComboBox.currentText()
        
        
        #绑定资产或者镜头下拉列表
        self.comboBoxForSA(self.pid,ptype)
        
        #获取资产号或者镜头号
        sid = self.__getSelectedId(self.SAComboBox,self.SAList)
        
        #绑定任务下拉列表
        self.comboBoxForTask(self.pid,ptype,sid)
        #设置文件名输入框最小宽度
        self.FileTxt.setMinimumWidth(450)
        #初始化提示框
        self.warning = UI().initMessageBox()
        
        
        #根据项目名联动类型、资产或镜头、任务三个下拉列表
        self.projectComboBox.currentIndexChanged.connect(self.ActivatedType)
        self.projectComboBox.currentIndexChanged.connect(self.ActivatedSA)
        self.projectComboBox.currentIndexChanged.connect(self.ActivatedTask)
        
        #根据类型名联动资产或镜头、任务两个下拉列表
        self.typeComboBox.currentIndexChanged.connect(self.ActivatedSA)
        self.typeComboBox.currentIndexChanged.connect(self.ActivatedTask)
        
        #根据镜头或者资产联动任务下拉列表
        self.SAComboBox.currentIndexChanged.connect(self.ActivatedTask)
        
        #绑定文件后缀类型下拉列表
        self.comboBoxForFileType()
        
        
        #绑定发布按钮事件
        self.publishBtn.clicked.connect(self.publish)
        #绑定取消按钮事件
        self.cancelBtn.clicked.connect(self.cancelBtnClicked)
  
    #取消事件
    def cancelBtnClicked(self):
        import launch.loader as loader
        self.Widget = loader.Widget(2,88)
        self.Widget.show()
        self.close()
    
    #保存 
    def save(self):
        if self.__preSave():
            i = 1
            self.warning.setIcon(QtGui.QMessageBox.Critical)    
            filetype = self.typeComboBox2.currentText()
            if self.imgPath == None:
                Msg().showDialog(self.warning,suggestion.warning,suggestion.publishFailed,suggestion.imgContent)
                return False
            else:
            
                while(os.path.exists(self.saveFilePath)):
                    if i == 1:
                        self.saveFilePath = self.saveFilePath.replace('001','002')
                        i = i+1
                    else:
                        self.saveFilePath = self.saveFilePath.replace('00'+ str(i),'00'+ str(i+1))
                        i = i+1
            
                
                cmds.file(rename = self.saveFilePath)
                if filetype == '.mb':
                    cmds.file(save =1,type='mayaBinary')
                else:
                    cmds.file(save =1,type='mayaAscii')
                
                self.warning.setIcon(QtGui.QMessageBox.NoIcon)
                Msg().showDialog(self.warning,suggestion.prompt,suggestion.publishSucessed,'')
                return True
              
        else:
            return False    
     
    #发布   
    def publish(self):
        if self.save():
            referenceList = cmds.file(query = 1,reference = 1)
            versionId = []
            if len(referenceList) > 0 :
                for reference in referenceList:
                    contents = Data().getVersionByName(os.path.basename(reference),self.pid)
                    if len(contents) >0 :
                        for content in contents:
                            versionId.append(content['versionId'])                                                
            self.addImg()
          
            self.addVersion(versionId)
            versionId = []
            import service.publishservice as publishservice
            fileDir = self.vid
            imgDir = self.imgId
            publishservice.PublishFile().callService(self.saveFilePath,fileDir)
            publishservice.Thumbnail().callService(self.imgPath,imgDir)
            self.close()      
              
    def addVersion(self,vid):
        versionData = {}
        versionData['entity_type'] = 'Task'
        versionData['entity_id'] = self.__getSelectedId(self.taskComboBox,self.List)
        versionData['content'] = self.taskComboBox.currentText()
        code = self.saveFilePath.split('/')
        versionData['code'] =  code[len(code)-1]
        versionData['image_id']= self.imgId
        versionData['description'] = self.contentTxt.toPlainText()
        versionData['project_id'] = self.__getSelectedId(self.projectComboBox,self.projectList)
        versionData['file_type'] = (self.typeComboBox2.currentText().split('.'))[1]
        versionData['file_size'] = os.stat(self.saveFilePath).st_size
        versionData['user_id'] = self.uid
        versionData['created_by_id'] = self.uid
        versionData['updated_by_id'] = ''
        versionData['reference_version_id'] = vid
        self.vid = Data().addVersion(versionData)
        
    def addImg(self):
        imgData = {}
        imgData['the_file'] = self.imgName
        imgData['mime_type'] = 'image/png'
        imgData['file_type'] = 'png'
        self.imgId = Data().addImg(imgData)
    
    def comboBoxForProject(self):
        self.projectComboBox.setMinimumWidth(500)
        if os.path.exists(confPath.xmlForProject):
            x = xml.readXmlForProject(confPath.xmlForProject)
      
        pid = x['id']
       
        data = Data().getSingleProject(pid)
        self.projectList = UI().initListWidget()
        self.__addItem(data,self.projectList,self.projectComboBox,suggestion.projectContent,'Project') 
        self.projectComboBox.setCurrentIndex(0)
               
    #绑定类型名
    def comboBoxForType(self,projectName):
        self.typeComboBox.setMinimumWidth(500)
        if projectName != suggestion.projectContent:
            self.typeComboBox.insertItem(0,'Asset')
            self.typeComboBox.insertItem(1,'Shot')
            if len(self.x) > 0:
                if self.x['entity_type'] == 'Shot':
                    self.typeComboBox.setCurrentIndex(1)
                else:
                    self.typeComboBox.setCurrentIndex(0)
        else:
            self.typeComboBox.insertItem(0,suggestion.selectProject)
            
            
    def comboBoxForFileType(self):
        self.typeComboBox2.setMinimumWidth(500)
        self.typeComboBox2.insertItem(0,'.ma')
        self.typeComboBox2.insertItem(1,'.mb')
          
            
    def comboBoxForSA(self,pid,ptype):
        self.SAComboBox.setMinimumWidth(500)
        self.SAList = UI().initListWidget()
        typeContent = self.typeComboBox.currentText()
        data = self.getSourceData(pid,ptype)
        if len(data) > 0: 
            self.__addItem(data,self.SAList,self.SAComboBox,suggestion.SAContent,ptype)
            if len(self.x) > 0:
                index = self.getIndex(self.x['entity_id'],self.SAList)
                self.SAComboBox.setCurrentIndex(index)
        else:
            if typeContent == suggestion.typeContent:
                self.SAComboBox.insertItem(0,suggestion.selectType)
            else:
                self.SAComboBox.insertItem(0,suggestion.SAContent)
           
    
    #绑定镜头号或者资产名
    def comboBoxForTask(self,pid,ptype,sid):
        self.taskComboBox.setMinimumWidth(500)
        saContent = self.SAComboBox.currentText()
        self.List = UI().initListWidget()
        data = Data().getTask(sid,ptype,self.uid,pid)
        if len(data) > 0: 
            self.__addItem(data,self.List,self.taskComboBox,suggestion.taskContent,'Task')
            if len(self.x) > 0:
                index = self.getIndex(self.x['task_id'],self.List)
                self.taskComboBox.setCurrentIndex(index)
        else:
            if saContent == suggestion.SAContent:
                self.taskComboBox.insertItem(0,suggestion.selectSA)
            else:
                self.taskComboBox.insertItem(0,suggestion.taskContent)
            return False
    
    def ActivatedType(self):
        projectName = self.projectComboBox.currentText()
        if projectName == suggestion.projectContent:
            self.typeComboBox.clear()
            self.comboBoxForType()
    
    def ActivatedSA(self):
        pid = self.__getSelectedId(self.projectComboBox,self.projectList)
        ptype = self.typeComboBox.currentText()
        self.SAComboBox.clear()
        self.comboBoxForSA(pid,ptype)
       
    def ActivatedTask(self):
        pid = self.__getSelectedId(self.projectComboBox,self.projectList)
        ptype = self.typeComboBox.currentText()
        sid = self.__getSelectedId(self.SAComboBox,self.SAList)
        self.taskComboBox.clear()
        self.comboBoxForTask(pid,ptype,sid) 
        
    def __getSelectedId(self,comboBox,inputList):
        txt = comboBox.currentText()
        rowId = comboBox.currentIndex()
        selectedId = '-1'
        if rowId != -1:
            if txt != suggestion.projectContent:
                if txt != suggestion.SAContent:
                    selectedId = inputList.item(rowId).data(QtCore.Qt.UserRole)
        return str(selectedId)
    
    def __addItem(self,sourceData,ouputList,comboBox,txt,flag):
        if len(sourceData) > 0:
            self.bindingComboBox(sourceData,ouputList,comboBox,flag)     
        else:
            comboBox.insertItem(0,txt)
    
    def bindingComboBox(self,sourceData,outputList,comboBox,flag):
        outputList.clear()
        if len(sourceData) > 0 :
            for index,content in enumerate(sourceData):
                newItem = QtGui.QListWidgetItem()
                newItem.setData(QtCore.Qt.UserRole,content['id'])
                newItem.setData(QtCore.Qt.UserRole+1,flag)
                newItem.setText(content['name'])
                outputList.insertItem(index, newItem)
            
            comboBox.setModel(outputList.model())
            #comboBox.setModelColumn(1)
            comboBox.setView(outputList)   
        else:
            newItem = QtGui.QListWidgetItem()
            newItem.setText(suggestion.noData)
            outputList.insertItem(0,newItem)
            outputList.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
            comboBox.setView(outputList)   
            
    def getSourceData(self,pid,ptype):
        data = []
        if ptype == 'Shot':
            data = Data().getShot(self.uid,pid,'','')
        elif ptype == 'Asset':
            data = Data().getAsset(self.uid,pid,'','')
        return data
    
    def __ImageBox(self):
        self.imageBtn = QtGui.QPushButton()
        self.imageBtn.setMaximumSize(580,160)
        self.imageBtn.setMinimumSize(580,160)
        self.imageBtn.setIcon(QtGui.QIcon(confPath.iconForScreenBtn))
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
        myCursor = QtGui.QCursor(QtGui.QPixmap(confPath.iconForCursor),-1,-1);
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
        #项目名称
        fileInfo['projectName'] = self.projectComboBox.currentText() 
        #所属类型
        fileInfo['ptype'] = self.typeComboBox.currentText()
        
        #镜头号或者资产名
        fileInfo['sa'] = self.SAComboBox.currentText()
        
        fileInfo['content'] = self.taskComboBox.currentText()
        
        fileInfo['name'] = self.FileTxt.text()
        
        return fileInfo
        
    def __getImageSavePath(self):
        self.imgPath = confPath.localPublishImage
        today = time.strftime('%Y%m%d')
        now = time.strftime('%H%M%S') 
        self.imgPath = self.imgPath + '/' + today + '/'
        if not os.path.exists(self.imgPath):
            os.makedirs(self.imgPath)
        self.imgName = now + '.png'
        self.imgPath = self.imgPath + self.imgName
        return self.imgPath
      
    def __preSave(self):
        today = time.strftime('%Y%m%d')
        filePath = confPath.localPublishFile + '/' + today + '/'
        fileInfo = self.__customSaveFileInfo()
        if (fileInfo['projectName'] != suggestion.projectContent and 
            fileInfo['ptype'] != suggestion.typeContent and
            fileInfo['sa'] != suggestion.SAContent and
            fileInfo['name'] != '' and 
            fileInfo['content'] != suggestion.taskContent):  
            
            if not os.path.exists(filePath):
                os.makedirs(filePath)   
            self.saveFilePath = filePath + fileInfo['name'] + '.001' + self.typeComboBox2.currentText()
            return True
        else:                               
            if fileInfo['projectName'] == suggestion.projectContent:
                txtSubContent = suggestion.selectProject
            elif fileInfo['ptype'] == suggestion.typeContent:
                txtSubContent = suggestion.selectType
            elif fileInfo['sa'] == suggestion.SAContent:
                txtSubContent = suggestion.selectSA
            elif fileInfo['content'] == suggestion.taskContent:
                txtSubContent = suggestion.selectTask
            else:
                txtSubContent = suggestion.fileNameIsNull
            self.warning.setIcon(QtGui.QMessageBox.Critical)     
            Msg().showDialog(self.warning,suggestion.warning,suggestion.publishFailed, txtSubContent)
            return False    
             
    def getIndex(self,defaultData,sourceData):
        rows = sourceData.count()
        for index in range(rows):
            sourceData.setCurrentIndex(QtCore.QModelIndex(sourceData.model().index(index)))
            if int(defaultData) == sourceData.currentIndex().data(QtCore.Qt.UserRole):
                return index