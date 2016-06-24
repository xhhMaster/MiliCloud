# -*- coding: utf-8 -*-
import lib.requests as requests
import conf.config as conf

base = conf.read_config(conf.path, 'API', 'baseUrl')

class Asset(object):
    def __getAsset(self,uid,project_id,start,length):
        api = conf.read_config(conf.path, 'API', 'getAssetApi')
        url = base + api + '?uid=' + uid +  '&project_id=' + project_id + '&start=' + start + '&length=' + length
        s = requests.session()
        result = s.post(url)
        s.keep_alive = False   
        if result.text != u"null":
            return result.json()['ASSET']
        else:
            return ""
    
    def callService(self,uid,project_id,start,length):
        return self.__getAsset(uid,project_id,start,length)
    
class SingleAsset(object):
    def __getSingleAsset(self,pid,entityId,entityType):
        api = conf.read_config(conf.path, 'API', 'getSingleAssetApi')
        url = base + api +  '?project_id=' + pid + '&entity_id=' + entityId + '&entity_type=' + entityType 
        s = requests.session()
        result = s.post(url)
        s.keep_alive = False   
        if result.text != u"null":
            return result.json()['SA']
        else:
            return ""
        
    def callService(self,pid,entityId,entityType):
        return self.__getSingleAsset(pid,entityId,entityType)


class AssetType(object):
    def __getAssetType(self):
        api = conf.read_config(conf.path, 'API', 'getAssetTypeAPi')
        url = base + api
        s = requests.session()
        result = s.post(url)
        s.keep_alive = False  
        if result.text != u"null":
            return result.json()['ASSETTYPE']
        else:
            return ""
        
    def callService(self):
        return self.__getAssetType()
    
    
class AssetByType(object):
    def __getAssetByType(self,pid):
        api = conf.read_config(conf.path, 'API', 'getAssetByTypeApi')
        url = base + api + '?project_id=' + pid
        s = requests.session()
        result = s.post(url)
        s.keep_alive = False 
        return result.json()
        
        
    def callService(self,pid):
        return self.__getAssetByType(pid)