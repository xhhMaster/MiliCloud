# -*- coding: utf-8 -*-
import lib.requests as requests
import conf.config as conf

base = conf.read_config(conf.path, 'API', 'baseUrl')


class PublishFile(object):
    def __upLoadFile(self,filePath,directory):
        api = conf.read_config(conf.path, 'API', 'publishFileApi')
        url = base + api + '?f=' + directory
        files = {'file': open(filePath, 'rb')}
        s = requests.session()
        s.post(url, files=files)
        s.keep_alive = False   
    
    def callService(self,filePath,directory):
        return self.__upLoadFile(filePath,directory)
    
class Thumbnail(object):
    def __upLoadImg(self,filePath,directory):
        api = conf.read_config(conf.path, 'API', 'uploadImgApi')
        url = base + api + '?f='+ directory
        files = {'file': open(filePath, 'rb')}
        s = requests.session()
        s.post(url, files=files)
        s.keep_alive = False   
          
    def callService(self,filePath,directory):
        return self.__upLoadImg(filePath,directory)