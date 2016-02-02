# -*- coding: utf-8 -*-
import service.projectservice as projectservice
import service.shotservice as shotservice
import service.assetservice as assetservice
import service.taskservice as taskservice

class Data(object):
    def getProjectInfo(self):
        contents = projectservice.Project().callService()
        return contents
    
    def getProject(self,pid):
        contents = projectservice.Project().callInfoService(pid)
        return contents
        
    def getShotInfo(self,pid):
        contents = shotservice.Shot().callService(pid)
        return contents
    
    def getShot(self,pid,entityId,entityType):
        contents = shotservice.Shot().callInfoService(pid,entityId,entityType)
        return contents
    
    def getAssetInfo(self,pid):
        contents = assetservice.Asset().callService(pid)
        return contents
    
    def getAsset(self,pid,entityId,entityType):
        contents = assetservice.Asset().callInfoService(pid,entityId,entityType)
        return contents
    
    def getTaskInfo(self,entity_id,entity_type,user_id,pid):
        contents = taskservice.Task().callService(entity_id,entity_type,user_id,pid)  
        return contents
    
    def getTask(self,uid,entity_id,entity_type,taskId,pid):
        contents = taskservice.Task().callInfoService(uid,entity_id,entity_type,taskId,pid)  
        return contents
    
    def getMyTask(self,uid,pid,entity_type):
        contents = taskservice.MyTask().callService(uid,pid,entity_type)  
        return contents
    
    def getWorkFile(self,entity_id,entity_type):
        import service.workfilesservice as workfilesservice
        contents = workfilesservice.WorkFile().callService(entity_id,entity_type)  
        return contents
    
    def addVersion(self,data):
        import service.versionservice as versionservice
        ID = versionservice.AddVersion().callService(data)
        return ID 
    
    def addImg(self,data):
        import service.thumbnailservice as thumbnailservice
        ID = thumbnailservice.InsertImg().callService(data)
        return ID 
    
    def downLoad(self,directory,fullfileName):
        import service.downloadservice as downloadservice
        downloadservice.DownLoad().callService(directory,fullfileName)
        
    def getImgName(self,imgId):
        import service.thumbnailservice as thumbnailservice 
        contents = thumbnailservice.SelectImg().callService(imgId)
        return contents