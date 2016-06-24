# -*- coding: utf-8 -*-
import ConfigParser
import sys,os

#path = os.path.expanduser('~').replace('\\','/') + '/maya/scripts'+'/conf/config.ini'
path = '../conf/config.ini'
def read_config(config_file_path, field, key):   
    cf = ConfigParser.ConfigParser()
    cf.read(config_file_path)  
    try:  
        result = cf.get(field, key)  
    except:  
        sys.exit(1)  
    return result   