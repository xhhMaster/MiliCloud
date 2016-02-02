# -*- coding: utf-8 -*-
import service.projectservice as projectservice
import service.shotservice as shotservice
import service.assetservice as assetservice
import service.taskservice as taskservice

class Data(object):
    def getProject(self):
        contents = projectservice.Project().callService()
        return contents
    
    def getSingalProject(self,pid):
        contents = projectservice.SingalProject().callService(pid)
        return contents
        
    def getShot(self,pid):
        contents = shotservice.Shot().callService(pid)
        return contents
    
    def getSingalShot(self,pid,entityId,entityType):
        contents = shotservice.SingalShot().callService(pid,entityId,entityType)
        return contents
    
    def getAsset(self,pid):
        contents = assetservice.Asset().callService(pid)
        return contents
    
    def getSingalAsset(self,pid,entityId,entityType):
        contents = assetservice.SingalAsset().callService(pid,entityId,entityType)
        return contents
    
    def getTask(self,entity_id,entity_type,user_id,pid):
        contents = taskservice.Task().callService(entity_id,entity_type,user_id,pid)  
        return contents
    
    def getSingalTask(self,uid,entity_id,entity_type,taskId,pid):
        contents = taskservice.SingalTask().callService(uid,entity_id,entity_type,taskId,pid)  
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