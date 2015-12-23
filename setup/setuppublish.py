# -*- coding: utf-8 -*-
from PySide import QtGui
from ui.publish_ui import Ui_Widget
import os
import maya.cmds as cmds
import time

class Widget(QtGui.QWidget, Ui_Widget):
    def __init__(self, parent=None):
        super(Widget,self).__init__(parent)
        self.setupUi(self)
        self.bindingProjectComboBox()
        self.bindingTypeComboBox()
        self.bindingShotComboBox()
        self.projectComboBox.currentIndexChanged.connect(self.bindingTypeComboBox)
        self.projectComboBox.currentIndexChanged.connect(self.bindingShotComboBox)
        self.typeComboBox.currentIndexChanged.connect(self.bindingShotComboBox)
        self.publishBtn.clicked.connect(self.publishClicked)
        self.cancelBtn.clicked.connect(self.cancelBtnClicked)
  
    def cancelBtnClicked(self):
        #self.close()
        self.save()
        
        
    def save(self):
        self.path = 'D:\\Sence\\'
        x = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        #项目名称
        projectName = self.projectComboBox.currentText() 
        #所属类型
        ptype = self.typeComboBox.currentText()
        #镜头号或者资产名
        content = self.shotComboBox.currentText()
        
        fileName = self.FileTxt.text()
        if projectName !=  u'暂无项目请先创建' or fileName != '':
            self.path = self.path + x + '\\' + projectName + '\\' + ptype + '\\' + content
            self.fullpath =self.path +'\\' + fileName + '.mb'
            #判断目录是否存在
            result = os.path.exists(self.path)
            if not result:
                os.makedirs(self.path)
            cmds.file(rename = self.fullpath)
            cmds.file(save =1,type='mayaBinary')
            #return cmds.confirmDialog(b=u"确定",m=u"发布成功！",t=u"提示信息")
            return u'发布成功'
        else:
            return u'发布失败'
            #return cmds.confirmDialog(b=u"确定",m=u"发布失败！！！请选择项目名称！",t=u"提示信息")
           
    
        
    def publishClicked(self):
        #self.save()


        import service.publishservice as publishservice
        publishservice.Publish().callService('D:\Sence\米粒云\Shot\收件箱\\a.mb')
        
        
          
    
    #绑定项目名
    def bindingProjectComboBox(self):
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
        self.typeComboBox.clear()
        projectName = self.projectComboBox.currentText()
        if projectName != u'暂无项目请先创建':
            self.typeComboBox.insertItem(0,'Shot')
            self.typeComboBox.insertItem(1,'Asset')
        else:  
            self.typeComboBox.insertItem(0,u"请先选择项目")

            
    #绑定镜头号或者资产名
    def bindingShotComboBox(self):
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
            self.shotComboBox.insertItem(0,u"没有可选的镜头或者资产,请先去创建!")
       