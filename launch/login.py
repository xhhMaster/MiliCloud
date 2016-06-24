# -*- coding: utf-8 -*-
from PySide import QtGui
from ui.login_ui import Ui_Widget
from common.uicommon import UI
from common.uicommon import Msg
import conf.msgsetting as suggestion
import conf.path as path
import os
from common.datacommon import Data 

class Widget(QtGui.QWidget, Ui_Widget):
    def __init__(self, parent=None):
        super(Widget,self).__init__(parent)
        #初始化ui
        self.setupUi(self)
        #初始化提示框
        self.warning = UI().initMessageBox()
        #设置提示框Icon
        self.warning.setIcon(QtGui.QMessageBox.Critical)   
        #设置按钮通过enter键触发事件
        self.loginBtn.setFocus()
        self.loginBtn.setShortcut(QtGui.QKeySequence.InsertParagraphSeparator)  
        
        if os.path.exists(path.xmlForRef):
            os.remove(path.xmlForRef)
        
        if os.path.exists(path.xmlForFile):
            os.remove(path.xmlForFile)
            
        if os.path.exists(path.xmlForProject):
            os.remove(path.xmlForProject)
            
        if os.path.exists(path.xmlForLogin):
            os.remove(path.xmlForLogin)
            
        #按钮绑定登录事件
        self.loginBtn.clicked.connect(self.loginClicked)
    
    
    #登录事件    
    def loginClicked(self):
        #调用登录service
        import service.loginservice as loginservice
        reload(loginservice)
        result =loginservice.Login().callService(self.userName.text(),self.passWord.text())
        if result != "error":
            userName = result[0][u'name']
            userID = result[0][u'id']
            content = Data().getCompetence(str(userID))
            editRole = content[0]['insert']
            readRole = content[0]['select']
            import common.xmlcommon as xml
            xml.writeLoginInfo({'userID':str(userID),'userName':userName,'editRole':str(editRole)})
            if readRole == 0:
                if not os.path.exists(path.xmlForProject):
                    from menu.menugenerator import MenuGenerator
                    MenuGenerator().unRoleMenu(userName,str(userID))   
            else:
                import launch.selectproject as selectproject
                reload(selectproject)
                self.Widget = selectproject.Widget(str(userID),userName)
                self.Widget.show()
            self.close()
        else:
            Msg().showDialog(self.warning,suggestion.warning,suggestion.loginFailed,suggestion.failedCause)
    