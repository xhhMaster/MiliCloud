from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
from xml.etree.ElementTree import dump
import conf.path as confPath
import os

def writeLoginInfo(info):
    book = ElementTree()
    parent = Element('LoginInfo')
    book._setroot(parent)
    item = Element('user')
    parent.append(item)   
    SubElement(item,'id').text = info['userID']
    SubElement(item,'name').text = info['userName']
    SubElement(item,'editRole').text = info['editRole']
    dump(indent(parent))
    if not os.path.exists(confPath.localXml):
        os.makedirs(confPath.localXml)
    book.write(confPath.localXml + 'loginInfo.xml',"utf-8")
    
def writeSelectedFile(info):
    book = ElementTree()
    parent = Element('FileInfo')
    book._setroot(parent)
    item = Element('file')
    parent.append(item)   
    SubElement(item,'project_id').text = info['project_id']
    SubElement(item,'entity_type').text = info['entity_type']
    SubElement(item,'entity_id').text = info['entity_id']
    SubElement(item,'task_id').text = info['task_id']
    dump(indent(parent))
    if not os.path.exists(confPath.localXml):
        os.makedirs(confPath.localXml)
    book.write(confPath.localXml + 'selectedFile.xml',"utf-8")
    
def writeSelectedProject(info):
    book = ElementTree()
    parent = Element('ProjectInfo')
    book._setroot(parent)
    item = Element('project')
    parent.append(item)   
    SubElement(item,'id').text = info['id']
    SubElement(item,'name').text = info['name']
    dump(indent(parent))
    if not os.path.exists(confPath.localXml):
        os.makedirs(confPath.localXml)
    book.write(confPath.localXml + 'selectedProject.xml',"utf-8")

def writeSelectedRef(info):
    book = ElementTree()
    parent = Element('RefInfo')
    book._setroot(parent)
    item = Element('ref')
    parent.append(item)   
    SubElement(item,'tab').text = info['tab']
    SubElement(item,'parent').text = info['parent']
    SubElement(item,'selectedNode').text = info['currentNode']
    SubElement(item,'listIndex').text = info['listIndex']
    SubElement(item,'inputText').text = info['text']
    dump(indent(parent))
    if not os.path.exists(confPath.localXml):
        os.makedirs(confPath.localXml)
    book.write(confPath.localXml + 'SelectedRef.xml',"utf-8")
    
    
def readXmlForLogin(path):
    uid = ElementTree(file = path).getroot().find('user/id').text
    name = ElementTree(file = path).getroot().find('user/name').text
    editRole = ElementTree(file = path).getroot().find('user/editRole').text
    content = {'id':uid,'name':name,'editRole':editRole}
    return content

def readXmlForRef(path):
    tab = ElementTree(file = path).getroot().find('ref/tab').text
    parent = ElementTree(file = path).getroot().find('ref/parent').text
    currentNode = ElementTree(file = path).getroot().find('ref/selectedNode').text
    listIndex = ElementTree(file = path).getroot().find('ref/listIndex').text
    inputText = ElementTree(file = path).getroot().find('ref/inputText').text
    content = {'tab':tab,'parent':parent,'selectedNode':currentNode,
               'listIndex':listIndex,'inputText':inputText}
    return content

def readXmlForProject(path):
    pid = ElementTree(file = path).getroot().find('project/id').text
    name = ElementTree(file = path).getroot().find('project/name').text
    content = {'id':pid,'name':name}
    return content

def readXmlForFile(path):
    pid = ElementTree(file = path).getroot().find('file/project_id').text
    entity_type = ElementTree(file = path).getroot().find('file/entity_type').text
    entity_id = ElementTree(file = path).getroot().find('file/entity_id').text
    task_id = ElementTree(file = path).getroot().find('file/task_id').text
    content = {'project_id':pid,'entity_type':entity_type,'entity_id':entity_id,'task_id':task_id}
    return content

def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        for e in elem:
            indent(e, level+1)
        if not e.tail or not e.tail.strip():
            e.tail = i
    if level and (not elem.tail or not elem.tail.strip()):
        elem.tail = i
    return elem