# -*- coding: utf-8 -*-
from PySide import QtGui,QtCore
from ui.selectproject_ui import Ui_Widget
from common.uicommon import UI
from common.uicommon import Msg
from common.datacommon import Data 
from common.funcommon import Fun
import conf.msgconfig as suggestion

class Widget(QtGui.QWidget, Ui_Widget):

    def __init__(self,uid,parent=None):
        super(Widget,self).__init__(parent)
        self.uid = uid
        self.setupUi(self)
        self.mainLayout = QtGui.QVBoxLayout()
        self.warning = UI().initMessageBox()
        self.warning.setIcon(QtGui.QMessageBox.Critical)     
        self.bindingProject()
        self.selectBtn.clicked.connect(self.selectedClicked)
        self.cancelBtn.clicked.connect(self.cancelClicked)
      
    #点击选择按钮触发的事件
    def selectedClicked(self):
        #获取当前选中行
        selectedIndex = self.projectList.currentIndex().row()

        if selectedIndex != -1:
            #获取选中行号
            selectedRow = self.projectList.currentItem().row()
            #获取选中的ID
            selectedId = self.projectList.item(selectedRow,0).text()
       
            import setup.setupselecttask as setupselecttask
            self.Widget = setupselecttask.Widget(selectedId,self.uid)
            self.Widget.show() 
            self.close()                
        else:
            Msg().showDialog(self.warning,suggestion.warning,suggestion.clickedFailed,suggestion.selectProject)
    
    #点击取消按钮触发的事件    
    def cancelClicked(self):
        self.close()
        
    #绑定数据到项目列表中
    def bindingProject(self):
        #获取项目数据
        contents = Data().getProject()
        self.projectList = UI().initTableWidget(['projectID','projectName','description'],3)
        self.projectList.setColumnHidden(0,True)
        self.projectList.setColumnHidden(2,True) 
        self.mainLayout.addWidget(self.projectList)
        self.projectGroupBox.setLayout(self.mainLayout)
        if len(contents) > 0:
            for index,content in enumerate(contents):
                #动态插入行
                self.projectList.insertRow(index)
                #抓去数据源id字段
                itemId = QtGui.QTableWidgetItem(content['id'])
                #抓去数据源name字段
                itemName = QtGui.QTableWidgetItem(content['name'])
                #抓去数据源description字段
                itemDesc = QtGui.QTableWidgetItem(content['description'])
                #将上述抓取到的值分别绑定到projectList控件上
                self.projectList.setItem(index,0,itemId)
                self.projectList.setItem(index,1,itemName)
                self.projectList.setItem(index,2,itemDesc)
            
        else:
            Fun.sourceDataISNULL(self.projectList, 'Project')
    
        #设置projectList默认不选中
        index = QtCore.QModelIndex()
        self.projectList.setCurrentIndex(index)
      
    