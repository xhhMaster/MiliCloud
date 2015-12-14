# -*- coding: utf-8 -*-
from PySide import QtGui
from ui.newtask_ui import Ui_Widget

class Widget(QtGui.QWidget, Ui_Widget):
    def __init__(self, parent=None):
        super(Widget,self).__init__(parent)
        self.setupUi(self)
        



Window=Widget()
Window.show()  