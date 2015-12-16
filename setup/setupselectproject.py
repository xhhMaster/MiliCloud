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
            #获取选中行号
            selectedRow = self.projectList.currentItem().row()
            #获取选中的ID
            selectedId = self.projectList.item(selectedRow,0).text()
            #获取选中的内容
            selectedContent = self.projectList.item(selectedRow,1).text()
            #获取选中内容的描述
            selectedDesc = self.projectList.item(selectedRow,2).text()
            #如果选中的内容描述为空则设置默认值
            if selectedDesc == "":
                selectedDesc = u"暂无内容"
                       
            import setup.setupselectworkfiles as setupselectworkfiles
            self.Widget = setupselectworkfiles.Widget(pid = selectedId,content = selectedContent,desc = selectedDesc )
            self.Widget.show() 
            self.close()                
        else:
            #提示信息
            cmds.confirmDialog(b=u"确定",m=u"请选择一个项目！",t=u"提示信息")
    
    #点击取消按钮触发的事件    
    def cancelClicked(self):
        self.close()
        
    #绑定数据到项目列表中
    def bindingProject(self):
        #导入projectservice
        import service.projectservice as projectservice
        
        #获取项目数据
        contents = projectservice.Project().callService()
        
        #设置列数
        self.projectList.setColumnCount(3)
        #设置列title
        header = ['projectID','projectName','description']
        #绑定列title到projectList控件
        self.projectList.setHorizontalHeaderLabels(header)
   
        if len(contents) > 0:
            for index,content in enumerate(contents):
                #动态插入行
                self.List.insertRow(index)
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
                #设置列隐藏显示        
                self.projectList.setColumnHidden(0,True)
                self.projectList.setColumnHidden(2,True)   
        else:
            self.projectList.setRowCount(10)
            self.projectList.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
            self.projectList.setSpan(3, 1, 5, 3);
            msg = QtGui.QTableWidgetItem(u"没有找到相关内容")
            self.projectList.setItem(3,1,msg) 
            #去除光标
            self.projectList.setFocusPolicy(QtCore.Qt.NoFocus);
            self.selectBtn.setHidden(True)
    
        #设置projectList默认不选中
        index = QtCore.QModelIndex()
        self.projectList.setCurrentIndex(index)
      
    