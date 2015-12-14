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
       
        if selectedIndex == -1:
            cmds.confirmDialog(b=u"确定",m=u"请选择一个项目！",t=u"提示信息")
        else:
            selectedContent = self.projectList.currentIndex().data()
            print self.contents.find(selectedContent)
            import setup.setupselectworkfiles as setupselectworkfiles
            self.Widget = setupselectworkfiles.Widget(content = selectedContent)
            self.Widget.show()        
                 
    #点击取消按钮触发的事件    
    def cancelClicked(self):
        self.close()
        
    #绑定数据到项目列表中
    def bindingProject(self):
        #导入apiService
        import service.projectservice as projectservice
        
        #获取项目数据
        contents = projectservice.Project().callService()
             
        #创建一个容器列表存放数据
        itemList = QtGui.QStandardItemModel()
        for content in contents:        
            item  = QtGui.QStandardItem(content['NAME'])
            itemList.appendRow(item)
           
        self.projectList.setModel(itemList)
        
        #让list默认不选中
        index =  QtCore.QModelIndex()
        self.projectList.setCurrentIndex(index)
    

       

