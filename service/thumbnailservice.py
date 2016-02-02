# -*- coding: utf-8 -*-
import lib.requests as requests


class InsertImg(object):
    def __init__(self):
        self.url = 'http://192.168.150.233:4267/api/maya/insertThumbnail'
       
    def __UploadData(self,data):
        result = requests.post(self.url,data)
        return result.text
          
    def callService(self,data):
        return self.__UploadData(data)
    

class SelectImg(object):
    def __init__(self):
        self.url = 'http://192.168.150.233:4267/api/maya/selectThumbnail?image_id='
       
    def __findData(self,imgId):
        self.url = self.url+imgId
        result = requests.post(self.url)
        if result.text != u"null":
            return result.json()['THUMBNAIL']
        else:
            return ""
        
          
    def callService(self,imgId):
        return self.__findData(imgId)