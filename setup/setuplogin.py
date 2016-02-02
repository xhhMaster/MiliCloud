# -*- coding: utf-8 -*-
from PySide import QtGui
from ui.login_ui import Ui_Widget
from common.uicommon import UI
from common.uicommon import Msg

class Widget(QtGui.QWidget, Ui_Widget):
    def __init__(self, parent=None):
        super(Widget,self).__init__(parent)
        self.setupUi(self)
        self.warning = UI().initMessageBox()
        self.warning.setIcon(QtGui.QMessageBox.Critical)     
        self.loginBtn.clicked.connect(self.loginClicked)
        
    def loginClicked(self):
        self.name = self.userName.text()
        self.pword = self.passWord.text()
        
        import service.loginservice as loginservice
        result =loginservice.Login().callService(self.name,self.pword)
      
        if result != "error":
            userName = result[0][u'name']
            userID = result[0][u'id']
            from mili.menu import MenuGenerator
            MenuGenerator().updateMenu(userName,userID)
            self.close()
        else:
            txtTitle = u'警告信息'
            txtMainContent = u'登录失败！                                             '
            txtSubContent =  u'用户名或密码错误！'
            Msg().showDialog(self.warning, txtTitle, txtMainContent, txtSubContent)
            
    