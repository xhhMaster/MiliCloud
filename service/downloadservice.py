# -*- coding: utf-8 -*-
import lib.requests as requests
import conf.apiconfig as conf

class DownLoad(object):
    def __download(self,directory,fullfileName):
        url = conf.downloadApi+directory
        r = requests.get(url)
        with open(fullfileName, "wb") as code:
            code.write(r.content)      

        
    def callService(self,directory,fullfileName):
        return self.__download(directory,fullfileName)