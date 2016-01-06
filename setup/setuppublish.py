# -*- coding: utf-8 -*-
from PySide import QtGui,QtCore
from ui.publish_ui import Ui_Widget
import os
import maya.cmds as cmds
import time

class Widget(QtGui.QWidget, Ui_Widget):
    def __init__(self, parent=None):
        super(Widget,self).__init__(parent)
        self.setupUi(self)  
        self.__ImageBox()
        self.savePath = None
        self.bindingProjectComboBox()
        self.bindingTypeComboBox()
        self.bindingShotComboBox()
        self.FileTxt.setMinimumWidth(500)
        self.warning = self.__initMessageBox()
        self.projectComboBox.currentIndexChanged.connect(self.bindingTypeComboBox)
        self.projectComboBox.currentIndexChanged.connect(self.bindingShotComboBox)
        self.typeComboBox.currentIndexChanged.connect(self.bindingShotComboBox)
        self.publishBtn.clicked.connect(self.publishClicked)
        self.cancelBtn.clicked.connect(self.cancelBtnClicked)
  
    def cancelBtnClicked(self):
        self.close()
           
    def save(self):
        if self.__preSaveCheck():
            #判断文件是否存在
            resultFile = os.path.exists(self.fullpath)
            remark = self.contentTxt.toPlainText()
            
            if self.savePath == None:
                msg = u'请添加缩略图'
                self.showWarningDialog(msg)
                return False
            if resultFile:
                msg = u'当前文件名已经存在，请更改!'
                self.showWarningDialog(msg)
                return False
            if remark == '':
                msg = u'请添加备注信息!'
                self.showWarningDialog(msg)
                return False
            else:   
                cmds.file(rename = self.fullpath)
                cmds.file(save =1,type='mayaBinary')
                self.showSucessDialog()
                return True
        else:
            return False    
        
    def publishClicked(self):
        if self.save():
            import service.publishservice as publishservice
            publishservice.Publish().callService(self.fullpath,self.subPath)
            publishservice.Publish().callService(self.savePath,self.subPath)
            self.insertDataBase()
    
    def insertDataBase(self):
        data = {}
        data['entity_type'] = self.typeComboBox.currentText()
        data['entity_id'] = self.__getSelectedId(self.shotComboBox,self.List)
        data['content'] = self.shotComboBox.currentText()
        data['code'] = self.FileTxt.text() + '.mb'
        data['image_id']= ''
        data['description'] = self.contentTxt.toPlainText()
        data['project_id'] = self.__getSelectedId(self.projectComboBox,self.projectList)
        data['file_type'] = 'mb'
        data['file_size'] = '100'
        data['user_id'] = '100'
        data['created_by_id'] = '100'
        data['updated_by_id'] = ''
        import service.insertdbservice as insertdbservice
        insertdbservice.InsertVersionDB().callService(data)
        
    #绑定项目名
    def bindingProjectComboBox(self):
        self.projectComboBox.setMinimumWidth(500)
        data = self.getProjectInfo()
        self.projectList = self.__initTableWidget()
        txt = u"暂无项目请先创建"
        self.__addItemInComboBox(data,self.projectList,self.projectComboBox,txt)
    
    #绑定类型名    
    def bindingTypeComboBox(self):
        self.typeComboBox.setMinimumWidth(500)
        self.typeComboBox.clear()
        projectName = self.projectComboBox.currentText()
        if projectName != u'暂无项目请先创建':
            self.typeComboBox.insertItem(0,'Shot')
            self.typeComboBox.insertItem(1,'Asset')
        else:  
            self.typeComboBox.insertItem(0,u"请先选择项目")

    #绑定镜头号或者资产名
    def bindingShotComboBox(self):
        self.shotComboBox.setMinimumWidth(500)
        self.shotComboBox.clear()
        self.List = self.__initTableWidget()
        data = self.getSourceData()  
        if data != -1: 
            txt = u"没有可选的镜头或者资产,请先去创建"
            self.__addItemInComboBox(data,self.List,self.shotComboBox,txt)
        else:
            self.shotComboBox.insertItem(0,u"请先选择类型")
            return False
      
    def __initTableWidget(self):
        header = ['ID','Name']
        List = QtGui.QTableWidget()
        List.setHorizontalHeaderLabels(header)   
        List.setColumnCount(2)
        List.verticalHeader().setVisible(False)
        List.horizontalHeader().setVisible(False)
        List.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        List.setShowGrid(False)
        List.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        List.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        List.horizontalHeader().setStretchLastSection(True)
        return List
    
    #初始化提示框
    
    def __initMessageBox(self):
        warning = QtGui.QMessageBox()
        okBtn = warning.addButton(u'确定',QtGui.QMessageBox.AcceptRole)
        okBtn.clicked.connect(warning.close)
        return warning    
    
    def __getSelectedId(self,comboBox,inputList):
        #设置默认选中第一行
        txt = comboBox.currentText()
        if txt != u'暂无项目请先创建':
            selectedRow = comboBox.currentIndex()
            selectedId = inputList.item(selectedRow,0).text()
        else:
            selectedId = -1
        return selectedId
    
    def __addItemInComboBox(self,sourceData,ouputList,comboBox,txt):
        if len(sourceData) > 0:
            self.__bindingComboxBox(sourceData,ouputList,comboBox)     
        else:
            comboBox.insertItem(0,txt)
    
    def __bindingComboxBox(self,sourceData,outputList,comboBox):
        for index,content in enumerate(sourceData):
            outputList.insertRow(index)    
            itemId = QtGui.QTableWidgetItem(content['id'])
            itemName = QtGui.QTableWidgetItem(content['name'])
            outputList.setItem(index,0,itemId)
            outputList.setItem(index,1,itemName)
            outputList.setColumnHidden(0,True)
            comboBox.setModel(outputList.model())
        comboBox.setModelColumn(1)
        comboBox.setView(outputList)  
             
    def getProjectInfo(self):
        import service.projectservice as projectservice
        data = projectservice.Project().callService()
        return data
        
    def getShotInfo(self,pid):
        import service.shotservice as shotservice
        shotContents = shotservice.Shot().callService(pid)
        return shotContents
    
    def getAssetInfo(self,pid):
        import service.assetservice as assetservice
        assetContents = assetservice.Asset().callService(pid)
        return assetContents
    
    def getSourceData(self):
        ptype = self.typeComboBox.currentText()
        pid = self.__getSelectedId(self.projectComboBox,self.projectList)
        data = ''
        if ptype == 'Shot':
            data = self.getShotInfo(pid)
        if ptype == 'Asset':
            data = self.getAssetInfo(pid)
        if ptype != 'Shot' and ptype != 'Asset':
            data = -1
        return data
    
    def __ImageBox(self):
        self.imageBtn = QtGui.QPushButton()
        self.imageBtn.setMaximumSize(580,160)
        self.imageBtn.setMinimumSize(580,160)
        self.imageBtn.setIcon(QtGui.QIcon('../Image/camera.png'))
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
        myCursor = QtGui.QCursor(QtGui.QPixmap('../Image/pointer.png'),-1,-1);
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
            pixmap.save(path + '.png')
            self.imageBtn.setIcon(pixmap)
            self.imageBtn.setIconSize(QtCore.QSize(rect.width()/3, rect.height()/3))
            #将shotScreenLabel的用户区大小固定为所截图片大小
            #self.shotScreenLabel.setFixedSize(rect.width(), rect.height())
           
            self.rubberBand.hide()
            self.fullScreenLabel.hide()
          
            return True       
    
    def __customSaveFileName(self):
        fileName = {}
        fileName['createDate'] = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        #项目名称
        fileName['projectName'] = self.projectComboBox.currentText() 
        #所属类型
        fileName['ptype'] = self.typeComboBox.currentText()
        #镜头号或者资产名
        fileName['content'] = self.shotComboBox.currentText()
        
        fileName['name'] = self.FileTxt.text()
        
        return fileName
        
    def __getImageSavePath(self):
        FileInfo = self.__customSaveFileName()
        self.savePath = ('D:\\Image\\' + FileInfo['createDate'] + '\\'
                     + FileInfo['projectName'] + '\\' + FileInfo['ptype'] 
                     + '\\' + FileInfo['content']
                     )
        resultDir = os.path.exists(self.savePath)
        if not resultDir:
            os.makedirs(self.savePath)
        if FileInfo['name'] != '' :
            self.savePath = self.savePath + '\\' + FileInfo['name']
        else:
            self.savePath =  self.savePath + '\\default'  
        return self.savePath
      
    def __preSaveCheck(self):
        self.path = 'D:\\Sence\\'
        File = self.__customSaveFileName()
        if File['projectName'] !=  u'暂无项目请先创建' and File['name'] != '' and File['content'] != u'没有可选的镜头或者资产,请先去创建':
            self.path = (self.path + File['createDate'] + '\\' 
                         + File['projectName'] + '\\' 
                         + File['ptype'] + '\\' + File['content']
                        )
            
            self.subPath = (File['createDate'] + '\\' + File['projectName'] 
                            + '\\' + File['ptype'] + '\\' 
                            + File['content']
                        )
            
            self.fullpath = 'D:\\123' +'\\' + File['name'] + '.mb'
            
            resultDir = os.path.exists(self.path)
            
            if not resultDir:
                os.makedirs(self.path)
            return True
        else:
            self.warning.setWindowTitle(u'警告信息')
            self.warning.setIcon(QtGui.QMessageBox.Critical)
            self.warning.setText(u"  发布失败！                                                                                ")
            if File['projectName'] ==  u'暂无项目请先创建':
                self.warning.setInformativeText(u"  请选择项目名！")
            elif File['content'] == u'没有可选的镜头或者资产,请先去创建':
                self.warning.setInformativeText(u"  请选择镜头或者资产名！")
            else:
                self.warning.setInformativeText(u"  文件名为空，请输入文件名！")
            self.warning.show()
            return False    
        
    def showWarningDialog(self,txt):
        self.warning.setWindowTitle(u'警告信息')
        self.warning.setIcon(QtGui.QMessageBox.Critical)
        self.warning.setText(u"  发布失败！                                                                    ")
        self.warning.setInformativeText("  " + txt)
        self.warning.show()
        
    def showSucessDialog(self):
        self.warning.setIcon(QtGui.QMessageBox.NoIcon)
        self.warning.setWindowTitle(u'提示信息')
        self.warning.setText(u"  发布成功！                                                                                     ")
        self.warning.setInformativeText('')
        self.warning.show()