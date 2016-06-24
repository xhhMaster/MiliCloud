# -*- coding: utf-8 -*-
from PySide import QtGui,QtCore
from ui.selectproject_ui import Ui_Widget
from common.uicommon import UI
from common.uicommon import Msg
from common.datacommon import Data 
from common.funcommon import Fun
import conf.msgsetting as suggestion
import conf.path as path
import os
import common.xmlcommon as xml

class Widget(QtGui.QWidget, Ui_Widget):

    def __init__(self,uid,userName,parent=None):
        super(Widget,self).__init__(parent)
        self.uid = uid
        self.useName = userName
        #初始化ui
        self.setupUi(self)
        #初始化一个Layout容器
        self.mainLayout = QtGui.QVBoxLayout()
        #初始化一个提示框
        self.warning = UI().initMessageBox()
        #设置提示框icon
        self.warning.setIcon(QtGui.QMessageBox.Critical)
        #绑定项目列表    
        self.bindingProject()
        #绑定选择按钮和取消按钮事件
        self.selectBtn.clicked.connect(self.selectedClicked)
        self.cancelBtn.clicked.connect(self.cancelClicked)
         
    #点击选择按钮触发的事件
    def selectedClicked(self):
        if os.path.exists(path.xmlForProject):
            os.remove(path.xmlForProject)
        
        #获取当前选中行
        selectedIndex = self.projectList.currentIndex().row()
        if selectedIndex != -1:
            #获取选中行号
            selectedRow = self.projectList.currentIndex().row()
            #获取选中的ID
            selectedId = self.projectList.item(selectedRow).data(QtCore.Qt.UserRole)
            
            selectedValue = self.projectList.currentIndex().data()
            
            xml.writeSelectedProject({'id':str(selectedId),'name':selectedValue})
            
            #调用菜单构造器
            x = xml.readXmlForLogin(path.xmlForLogin)
            from menu.menugenerator import MenuGenerator
            MenuGenerator().updateMenu(self.useName,self.uid,str(selectedId),int(x['editRole']))
            
            self.close() 
            
        else:
            Msg().showDialog(self.warning,suggestion.warning,suggestion.clickedFailed,suggestion.selectProject)
    
    #点击取消按钮触发的事件    
    def cancelClicked(self):
        if os.path.exists(path.xmlForLogin):
            if not os.path.exists(path.xmlForProject):
                from menu.menugenerator import MenuGenerator
                MenuGenerator().unselectProjectMenu(self.useName,self.uid)   
            else:
                x = xml.readXmlForProject(path.xmlForProject)
                import launch.selecttask as selecttask
                reload(selecttask)
                self.Widget = selecttask.Widget(str(x['id']),self.uid,self.useName)
                self.Widget.show()    
            self.close()
    
        
    #绑定数据到项目列表中
    def bindingProject(self):
        #获取项目数据
        contents = Data().getProject(self.uid)
        #初始化项目列表（有id,name,desc三列）
        self.projectList = UI().initListWidget()
        
        #将项目列表嵌入layout下
        self.mainLayout.addWidget(self.projectList)
        #讲layout嵌入groupBox
        self.projectGroupBox.setLayout(self.mainLayout)
        #check 数据源
        self.projectList.clear()
        self.projectList.setSpacing(5)
        self.projectList.setIconSize(QtCore.QSize(122,85))
        if len(contents) > 0 :
            for index,content in enumerate(contents):
                imageId = content[u'image_id']
                if imageId == None:
                    imageId = ''
                imgPath = Fun().getImgPath(imageId,content['id'],'Project',path.publishImgPath)
                Fun().bindingList(index,content,self.projectList,imgPath,'Project')
        else:
            newItem = QtGui.QListWidgetItem()
            newItem.setText(suggestion.noData)
            self.projectList.insertItem(0,newItem)
            self.projectList.setSelectionMode(QtGui.QAbstractItemView.NoSelection)