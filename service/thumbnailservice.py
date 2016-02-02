# -*- coding: utf-8 -*-
import lib.requests as requests
import conf.apiconfig as conf

class InsertImg(object):
    def __UploadData(self,data):
        result = requests.post(conf.addThumbnailApi,data)
        return result.text
          
    def callService(self,data):
        return self.__UploadData(data)
    
class SelectImg(object):
    def __findData(self,imgId):
        url = conf.getThumbnailApi+imgId
        result = requests.post(url)
        if result.text != u"null":
            return result.json()['THUMBNAIL']
        else:
            return ""
        
          
    def callService(self,imgId):
        return self.__findData(imgId)