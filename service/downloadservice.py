# -*- coding: utf-8 -*-
import lib.requests as requests
import conf.config as conf


class DownLoad(object):
    def __download(self,directory,fullfileName):
        api = conf.read_config(conf.path, 'API', 'downloadApi')
        url = api +directory
        r = requests.get(url)
        if r.status_code != 404:
            with open(fullfileName, "wb") as code:
                code.write(r.content)
        return r.status_code
       

        
    def callService(self,directory,fullfileName):
        return self.__download(directory,fullfileName)