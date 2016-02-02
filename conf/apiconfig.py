projectApi = 'http://192.168.150.233:4267/api/projectList/load'
singalProjectApi ='http://192.168.150.233:4267/api/maya/selectProject?project_id='

assetApi = 'http://192.168.150.233:4267/api/assetList/load?step_id&related_shot_id&project_id='
singalAssetApi ='http://192.168.150.233:4267/api/maya/selectShotAsset?project_id='

shotApi = 'http://192.168.150.233:4267/api/shotList/load?step_id&related_asset_id&project_id='
singalShotApi = 'http://192.168.150.233:4267/api/maya/selectShotAsset?project_id='

taskApi = 'http://192.168.150.233:4267/api/maya/loadTask?entity_id='
singalTaskApi = 'http://192.168.150.233:4267/api/maya/selectTask?uid='
myTaskApi = 'http://192.168.150.233:4267/api/maya/getMyTask?uid='

loginApi = 'http://192.168.150.233:4267/api/shotList/load?step_id&related_asset_id&project_id='
downloadApi = 'http://192.168.150.233:4267/App_SaveData/tmp/'
publishApi  = 'http://192.168.150.233:4267/api/versionAdd/upload?f='

addThumbnailApi  = 'http://192.168.150.233:4267/api/maya/insertThumbnail'
getThumbnailApi = 'http://192.168.150.233:4267/api/maya/selectThumbnail?image_id='

addVersionApi = 'http://192.168.150.233:4267/api/versionAdd/mayaInsert'
workfileApi = 'http://192.168.150.233:4267/api/maya/publishFile?entity_id='
