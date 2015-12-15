# -*- coding: utf-8 -*-
from PySide import QtGui,QtCore
from ui.selectproject_ui import Ui_Widget
import maya.cmds as cmds


class Widget(QtGui.QWidget, Ui_Widget):

    def __init__(self, parent=None):
        super(Widget,self).__init__(parent)
        self.setupUi(self)
        self.bindingProject()
        self.selectBtn.clicked.connect(self.selectedClicked)
        self.cancelBtn.clicked.connect(self.cancelClicked)
      
    #点击选择按钮触发的事件
    def selectedClicked(self):
        
        #获取当前选中行
        selectedIndex = self.projectList.currentIndex().row()

        if selectedIndex != -1:
            selectedRow = self.projectList.currentItem().row()
            selectedId = self.projectList.item(selectedRow,0).text()
            selectedContent = self.projectList.item(selectedRow,1).text()
            selectedDesc = self.projectList.item(selectedRow,2).text()
            if selectedDesc == "":
                selectedDesc = u"暂无内容"           
            import setup.setupselectworkfiles as setupselectworkfiles
            self.Widget = setupselectworkfiles.Widget(pid = selectedId,content = selectedContent,desc = selectedDesc )
            self.Widget.show()        
           
        else:
            cmds.confirmDialog(b=u"确定",m=u"请选择一个项目！",t=u"提示信息")
                 
    #点击取消按钮触发的事件    
    def cancelClicked(self):
        self.close()
        
    #绑定数据到项目列表中
    def bindingProject(self):
        #导入apiService
        import service.projectservice as projectservice
        
        #获取项目数据
        contents = projectservice.Project().callService()
       
        self.projectList.setColumnCount(3)
        self.projectList.setRowCount(int(len(contents)))
        header = ['projectID','projectName','description']
        self.projectList.setHorizontalHeaderLabels(header)
       
        for index,content in enumerate(contents):
            itemId = QtGui.QTableWidgetItem(content['id'])
            itemName = QtGui.QTableWidgetItem(content['name'])
            itemDesc = QtGui.QTableWidgetItem(content['description'])
            self.projectList.setItem(index,0,itemId)
            self.projectList.setItem(index,1,itemName)
            self.projectList.setItem(index,2,itemDesc)      
             
        self.projectList.setColumnHidden(0,True)
        self.projectList.setColumnHidden(2,True)
        
        index = QtCore.QModelIndex()
        self.projectList.setCurrentIndex(index)
       
                 
        
      
    