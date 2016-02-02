# -*- coding: utf-8 -*-
import re
from PySide import QtGui,QtCore
import os
from common.datacommon import Data 

class Fun(object):
    def fiterData(self,userinput,sourceList):
        suggestions = []
        pattern = '.*?'.join(userinput)   
        regex = re.compile(pattern)
        rows = sourceList.rowCount()
        for rows_index in range(rows):
            itemId = sourceList.item(rows_index,0).text()
            itemName = sourceList.item(rows_index,2).text()
            itemType = sourceList.item(rows_index,3).text()
            itemPath = sourceList.item(rows_index,4).text()
            match = regex.search(itemName) 
            if match:
                suggestions.append((len(match.group()), match.start(), (itemId,itemName,itemType,itemPath)))
        return [x for _, _, x in sorted(suggestions)]
    
    def sourceDataISNULL(self,outputList,Flag):
        outputList.setRowCount(3)
        if Flag == 'Shot':
            txt =u"没有Shot相关内容"
        elif Flag == 'Asset':
            txt = u"没有Asset相关内容"
        elif Flag == 'Project':
            txt = u"没有Project相关内容"
        elif Flag == 'Work':
            txt = u"没有Work File相关内容"
        else:
            txt = u"没有Task相关内容"
        contentItem = QtGui.QTableWidgetItem(txt)
        outputList.setItem(2,1,contentItem) 
        outputList.setFocusPolicy(QtCore.Qt.NoFocus)
        outputList.setColumnHidden(0,False)
        outputList.setColumnHidden(2,False)
        outputList.setSpan(2, 1, 3, 3)
        outputList.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
    
    def bindingDataSingal(self,index,content,outputList,queryField,imgPath,Flag):
        outputList.insertRow(index)   
        itemId = QtGui.QTableWidgetItem(str(content[queryField[0]]))
        if Flag not in ('Task','Work') :
            if len(queryField) < 3:
                txt = content[queryField[1]]
            else:
                txt = (content[queryField[1]]+ u'\n描述：' + 
                           content[queryField[2]])
        else:
            if  len(queryField) < 3:
                txt = content[queryField[1]]
            else:
                txt = (content[queryField[1]]+ u'\n制作人：' + 
                str(content[queryField[2]]))
        itemName = QtGui.QTableWidgetItem(txt)
        itemType = QtGui.QTableWidgetItem(Flag)
        itemPath = QtGui.QTableWidgetItem(imgPath)
        outputList.setItem(index,0,itemId)
        outputList.setCellWidget(index,1,self.setImg(imgPath))
        outputList.setItem(index,2,itemName)
        outputList.setItem(index,3,itemType)
        outputList.setItem(index,4,itemPath)
        outputList.setRowHeight(index,90)
        outputList.setColumnWidth(1,120)
        outputList.setColumnHidden(0,True)
        outputList.setColumnHidden(3,True)
        outputList.setColumnHidden(4,True)
        outputList.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
  
    def setImg(self,imgPath):
        imgLabel = QtGui.QLabel()
        pixmap = QtGui.QPixmap(imgPath)
        pixmap = pixmap.scaled(QtCore.QSize(120,80), 
                               QtCore.Qt.KeepAspectRatio, 
                               QtCore.Qt.SmoothTransformation)
        imgLabel.setPixmap(pixmap)
        return imgLabel    
    
    def getImgPath(self,imageId,baseDir):
        imgInfo = Data().getImgName(imageId)
        if len(imgInfo)>0:
            imgName = imgInfo[0][u'the_file']
        else:
            imgName = '000.png' 
        filePath = 'D:/mayaDownload/Image/'
        pathDir = os.path.exists(filePath)
        if not pathDir:
            os.makedirs(filePath)
        
        """
        fullPathFileName = unicode(filePath + self.projectInfo[0]['name']+'/'
            +self.resultInfo[0]['name']+'/'
            +self.taskInfo[0]['name']+'/'+ imgName)
        """
        
        fullPathFileName = filePath + imgName
        directory = baseDir +imageId+'/'+ imgName
        if not os.path.exists(fullPathFileName):
            Data().downLoad(directory, fullPathFileName)
        return fullPathFileName