# -*- coding: utf-8 -*-
import service.projectservice as projectservice
import service.shotservice as shotservice
import service.assetservice as assetservice
import service.taskservice as taskservice

class Data(object):
    #获取项目列表
    def getProject(self,uid):
        contents = projectservice.Project().callService(uid)
        return contents
    
    #获取指定项目
    def getSingleProject(self,pid):
        contents = projectservice.SingleProject().callService(pid)
        return contents
    
    #获取镜头列表
    def getShot(self,uid,pid,start,length):
        contents = shotservice.Shot().callService(uid,pid,start,length)
        return contents
    
    #获取指定镜头
    def getSingleShot(self,pid,entityId,entityType):
        contents = shotservice.SingleShot().callService(pid,entityId,entityType)
        return contents
    
    #获取资产列表
    def getAsset(self,uid,pid,start,length):
        contents = assetservice.Asset().callService(uid,pid,start,length)
        return contents
    
    #获取指定资产
    def getSingleAsset(self,pid,entityId,entityType):
        contents = assetservice.SingleAsset().callService(pid,entityId,entityType)
        return contents
    
    #获取资产的角色类型
    def getAssetType(self):
        contents = assetservice.AssetType().callService()
        return contents
    
    def getAssetByType(self,pid):
        contents = assetservice.AssetByType().callService(pid)
        return contents
    
    #获取Sequence列表
    def getSequences(self,pid):
        contents = shotservice.Sequences().callService(pid)
        return contents
    
    def getShotBySequences(self,pid):
        contents = shotservice.ShotBySequences().callService(pid)
        return contents
    
    #获取Pipline
    def getTaskStep(self,uid,pid,tableName):
        contents = taskservice.TaskStep().callService(uid,pid,tableName)
        return contents
    
    #获取任务
    def getTask(self,entity_id,entity_type,user_id,pid):
        contents = taskservice.Task().callService(entity_id,entity_type,user_id,pid)  
        return contents
    
    #获取指定任务
    def getSingleTask(self,uid,taskId,stepId):
        contents = taskservice.SingleTask().callService(uid,taskId,stepId)  
        return contents
    
    #获取工作文件
    def getWorkFile(self,entity_id,entity_type,pid):
        import service.workfilesservice as workfilesservice
        contents = workfilesservice.GetWorkFile().callService(entity_id,entity_type,pid)  
        return contents
    
    #查找工作文件
    def selectWorkFile(self,entity_id,entity_type,pid):
        import service.workfilesservice as workfilesservice
        contents = workfilesservice.SelectWorkFile().callService(entity_id,entity_type,pid)  
        return contents
    
    #添加版本（插入版本库）
    def addVersion(self,data):
        import service.versionservice as versionservice
        ID = versionservice.AddVersion().callService(data)
        return ID 
    
    #查找ID指定版本
    def getVersionById(self,vid):
        import service.versionservice as versionservice
        contents = versionservice.GetVersionById().callService(vid)
        return contents
    
    #查找name指定版本
    def getVersionByName(self,vname,pid):
        import service.versionservice as versionservice
        contents = versionservice.GetVersionByName().callService(vname,pid)
        return contents
    
    
    #查找最新版本
    def getLastVersion(self,entity_id,entity_type):
        import service.versionservice as versionservice
        ID = versionservice.GetLastVersion().callService(entity_id,entity_type)
        return ID
    
    #查找引用版本
    def getReferenceVersion(self,vid):
        import service.versionservice as versionservice
        contents = versionservice.GetReferenceVersion().callService(vid)
        return contents
    
    def checkVersion(self,vid):
        import service.versionservice as versionservice
        contents = versionservice.CheckVersion().callService(vid)
        return contents
    
    def lastVersionView(self,vid):
        import service.versionservice as versionservice
        contents = versionservice.LastVersionView().callService(vid)
        return contents
    
    #添加缩略图
    def addImg(self,data):
        import service.thumbnailservice as thumbnailservice
        ID = thumbnailservice.AddImg().callService(data)
        return ID 
    
    #获取缩略图     
    def getImg(self,imgId):
        import service.thumbnailservice as thumbnailservice 
        contents = thumbnailservice.GetImg().callService(imgId)
        return contents
    
    #下载
    def downLoad(self,directory,fullfileName):
        import service.downloadservice as downloadservice
        code = downloadservice.DownLoad().callService(directory,fullfileName)
        return code
   
    
    def getCompetence(self,uid):
        import service.loginservice as loginservice
        contents = loginservice.Competence().callService(uid)
        return contents