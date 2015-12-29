# -*- coding: utf-8 -*-
import ctypes 
import os 
    
def capture_choose_windows():  
    ''''' 
    Function:抓取选择的区域，没有自己写这个，借用QQ抓图功能 
    Input：NONE 
    Output: NONE 
    author: socrates 
    blog:http://blog.csdn.net/dyx1024 
    date:2012-03-10 
    '''       
    try:  
        #加载QQ抓图使用的dll  
        
        dll_handle = ctypes.cdll.LoadLibrary('CameraDll.dll')   
    except Exception:  
            try:  
                #如果dll加载失败，则换种方法使用，直接运行，如果还失败，退出  
                os.system("Rundll32.exe CameraDll.dll, CameraSubArea")  
            except Exception:  
                return      
    else:  
        try:  
            #加载dll成功，则调用抓图函数，注:没有分析清楚这个函数带的参数个数  
            #及类型，所以此语句执行后会报参数缺少4个字节，但不影响抓图功能，所  
            #以直接忽略了些异常  
            dll_handle.CameraSubArea(0)  
        except Exception:  
            return    
        
capture_choose_windows()         