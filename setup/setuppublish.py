# -*- coding: utf-8 -*-
from PySide import QtGui
from ui.publish_ui import Ui_Widget
import os
import maya.cmds as cmds
import time
import core.PIL as PIL

class Widget(QtGui.QWidget, Ui_Widget):
    def __init__(self, parent=None):
        super(Widget,self).__init__(parent)
        self.setupUi(self)
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
        #self.close()
        self.getThumbnails()

    def save(self):
        self.path = 'D:\\Sence\\'
        #获取当前日期
        createDate = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        #项目名称
        projectName = self.projectComboBox.currentText() 
        #所属类型
        ptype = self.typeComboBox.currentText()
    
        #镜头号或者资产名
        content = self.shotComboBox.currentText()
        
        fileName = self.FileTxt.text()
        if projectName !=  u'暂无项目请先创建' and fileName != '' and content != u'没有可选的镜头或者资产,请先去创建':
            self.path = self.path + createDate + '\\' + projectName + '\\' + ptype + '\\' + content
            self.subPath =  createDate + '\\' + projectName + '\\' + ptype + '\\' + content
            self.fullpath ='D:\\123' +'\\' + fileName + '.mb'
            #判断目录是否存在
            resultDir = os.path.exists('D:\\123')
            if not resultDir:
                os.makedirs('D:\\123')
                
            #判断文件是否存在
            resultFile = os.path.exists(self.fullpath)
            if resultFile:
                self.warning.setWindowTitle(u'警告信息')
                self.warning.setIcon(QtGui.QMessageBox.Critical)
                self.warning.setText(u"  发布失败！                                                                    ")
                self.warning.setInformativeText(u"  当前文件名已经存在，请更改！")
                self.warning.show()
                return False
            else:   
                cmds.file(rename = self.fullpath)
                cmds.file(save =1,type='mayaBinary')
                self.warning.setIcon(QtGui.QMessageBox.NoIcon)
                self.warning.setWindowTitle(u'提示信息')
                self.warning.setText(u"  发布成功！                                                                                     ")
                self.warning.setInformativeText('')
                self.warning.show()
                return True
        else:
            self.warning.setWindowTitle(u'警告信息')
            self.warning.setIcon(QtGui.QMessageBox.Critical)
            self.warning.setText(u"  发布失败！                                                                                ")
            if projectName ==  u'暂无项目请先创建':
                self.warning.setInformativeText(u"  请选择项目名！")
            elif  content == u'没有可选的镜头或者资产,请先去创建':
                self.warning.setInformativeText(u"  请选择所属类型！")
            else:
                self.warning.setInformativeText(u"  文件名为空，请输入文件名！")
            self.warning.show()
            return False
        
    def publishClicked(self):
        if self.save():
            import service.publishservice as publishservice
            publishservice.Publish().callService(self.fullpath,self.subPath)
        
    #绑定项目名
    def bindingProjectComboBox(self):
        self.projectComboBox.setMinimumWidth(500)
        import service.projectservice as projectservice
        contents = projectservice.Project().callService()
        self.projectList = self.__initTableWidget()
        if len(contents) > 0:
            for index,content in enumerate(contents):
                self.projectList.insertRow(index)    
                itemId = QtGui.QTableWidgetItem(content['id'])
                itemName = QtGui.QTableWidgetItem(content['name'])
                self.projectList.setItem(index,0,itemId)
                self.projectList.setItem(index,1,itemName)
            self.projectList.setColumnHidden(0,True)
            self.projectComboBox.setModel(self.projectList.model())
            self.projectComboBox.setModelColumn(1)
            self.projectComboBox.setView(self.projectList)
            
        else:
            self.projectComboBox.addItem(u"暂无项目请先创建")
           
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
        ptype = self.typeComboBox.currentText()
        pid = self.__getSelectedProjectId()
        if ptype == 'Shot':
            import service.shotservice as shotservice
            shotContents = shotservice.Shot().callService(pid)
            self.__addItemInShotComboBox(shotContents)
        elif ptype == 'Asset':
            import service.assetservice as assetservice
            assetContents = assetservice.Asset().callService(pid)
            self.__addItemInShotComboBox(assetContents)
        else:
            self.shotComboBox.insertItem(0,u"请先选择类型")
      
    def getThumbnails(self):
        print dir(PIL.Image)

          
    
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
    
    def __getSelectedProjectId(self):
        #设置默认选中第一行
        txt = self.projectComboBox.currentText()
        if txt != u'暂无项目请先创建':
            self.projectList.selectRow(self.projectComboBox.currentIndex())
            selectedRow = self.projectList.currentIndex().row()
            selectedId = self.projectList.item(selectedRow,0).text()
        else:
            selectedId = ''
        return selectedId
    
    def __addItemInShotComboBox(self,sourceData):
        if len(sourceData) > 0:
            for index,content in enumerate(sourceData):
                self.shotComboBox.insertItem(index,content['name'])
        else:
            self.shotComboBox.insertItem(0,u"没有可选的镜头或者资产,请先去创建")
    
    #初始化提示框
    def __initMessageBox(self):
        warning = QtGui.QMessageBox()
        okBtn = warning.addButton(u'确定',QtGui.QMessageBox.AcceptRole)
        okBtn.clicked.connect(warning.close)
        return warning