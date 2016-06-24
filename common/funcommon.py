# -*- coding: utf-8 -*-
from PySide import QtGui,QtCore
import os
from common.datacommon import Data
import conf.path as confPath

class Fun(object):
    def getImgPath(self,imageId,entity_id,Flag,baseDir):
        if imageId != '':
            imgInfo = Data().getImg(str(imageId))
            if len(imgInfo) > 0:
                imgName = imgInfo[0][u'the_file']
            else:
                imgName = ''
           
            if imgName != '':
                filePath = confPath.downLoadImg + Flag + '/' + str(entity_id) + '/'
                if not os.path.exists(filePath):
                    os.makedirs(filePath)
                fullPath = filePath + imgName
            else:
                fullPath = confPath.defaultImgPath
            
            directory = baseDir + str(imageId) +'/'+ imgName
            if fullPath != confPath.defaultImgPath:
                if os.path.exists(fullPath):
                    os.remove(fullPath)
                code = Data().downLoad(directory,fullPath)
                if code == 404:
                    fullPath = confPath.defaultImgPath
        else:
            fullPath = confPath.defaultImgPath
        return fullPath
    
    def bindingList(self,index,content,outputList,imgPath,Flag):
        newItem = QtGui.QListWidgetItem()
        pixmap = QtGui.QPixmap(imgPath)
        newItem.setIcon(pixmap.scaled(QtCore.QSize(122,95)))
        newItem.setSizeHint(QtCore.QSize(122,95))
        if Flag == 'Work':
            newItem.setData(QtCore.Qt.UserRole,content['versionId'])
            newItem.setData(QtCore.Qt.UserRole+2,content['id'])
        else:
            newItem.setData(QtCore.Qt.UserRole,content['id'])
        newItem.setData(QtCore.Qt.UserRole+1,Flag)
        if Flag in ('Task','Work') :
            if Flag == 'Work':
                txt = (content['code']+ u'\n上传人：' + content['user_name'] + u'\n上传时间：' + content['created_at'])
            else:
                txt = (content['name']+ u'\n上传人：' + content['user_name'])
        else:
            txt = content['name'] + u'\n描述：' + content['description']
        newItem.setText(txt)
        outputList.insertItem(index, newItem)
    
