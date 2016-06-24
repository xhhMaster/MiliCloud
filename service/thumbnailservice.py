# -*- coding: utf-8 -*-
import lib.requests as requests
import conf.config as conf

base = conf.read_config(conf.path, 'API', 'baseUrl')

class AddImg(object):
    def __addImg(self,data):
        api = conf.read_config(conf.path, 'API', 'addImgApi')
        url = base + api
        s = requests.session()
        result = s.post(url,data)
        s.keep_alive = False       
        return result.text
          
    def callService(self,data):
        return self.__addImg(data)
    
class GetImg(object):
    def __getImg(self,imgId):
        api = conf.read_config(conf.path, 'API', 'getImgApi')
        url = base + api + '?image_id=' + imgId
        s = requests.session()
        result = s.post(url)
        s.keep_alive = False
        if result.text != u"null":
            return result.json()['THUMBNAIL']
        else:
            return ""
        
    def callService(self,imgId):
        return self.__getImg(imgId)