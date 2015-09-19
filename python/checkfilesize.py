#coding=utf-8

import os
from os.path import join, getsize, isdir, exists

#日志文件，如果未设置日志文件，则打印到屏幕
LOGFILE = "checkfilesize.log"

#超过这个大小的文件或目录将会输出日志
LOGSIZETHRESHOLD = 500*1024*1024

def setlogfile(logfile) :
  global LOGFILE
  LOGFILE = logfile
  return
  
def setlogsizethresdhold(size) :
  global LOGSIZETHRESHOLD
  LOGSIZETHRESHOLD = size
  return

#日志处理，打印到文件或屏幕
def log(str) :
  global LOGFILE 
  if len(LOGFILE) > 0 :
    f = open(LOGFILE,"a+")
    try :
      f.write(str + "\n")
    finally :
      f.close()
  else :
    print str
  return

#文件大小转换为字符串
def sizetostring(size) :
  if size > 1024*1024*1024:
    return "%.2f GB" %(float(size)/1024/1024/1024)
  elif size > 1024*1024 :
    return "%.2f MB" %(float(size)/1024/1024)
  elif size > 1024 :
    return "%.2f KB" %(float(size)/1024)
  else :
    return "%.2f B" %(float(size))

#文件超过一定大小，打印文件路径及其大小
def checksize(filepath, filesize) :
  global LOGSIZETHRESHOLD
  if filesize > LOGSIZETHRESHOLD :
    log(filepath + " : " + sizetostring(filesize))
  return
    
#通过os.walk遍历文件得到目录的总大小
def getdirsizebywalk(dir) :
  totalsize = 0L
  dirsize = 0L
  filesize = 0L
  filepath = ""
  #os.walk会遍历所有嵌套子目录
  for root, dirs, files in os.walk(dir):
    dirsize = 0L
    for name in files :
      filesize = 0L
      filepath = join(root, name)
      try :
        filesize = getsize(filepath)
      except :
        filesize = 0
      dirsize += filesize
    
    totalsize += dirsize      
  return totalsize  

#通过函数递归的方式，获取目录的总大小
#如果文件或目录的大小超过阈值，会打印文件路径和大小
def getdirsizerecursive(dir) :
  totalsize = 0L
  filesize = 0L
  filepath = ""
  for name in os.listdir(dir) :
    filesize = 0L
    filepath = join(dir, name)
    try : 
      if isdir(filepath):
        filesize += getdirsizerecursive(filepath)
      elif exists(filepath) :
        filesize = getsize(filepath)
      else :
        filesize = 0L
    except :
      filesize = 0L
    totalsize += filesize;
    checksize(filepath, filesize)
  
  return totalsize  

#列出指定目录下的所有文件和目录的总大小
def listchildsize(dir) :
  listfile = []
  filePath = ""
  filesize = 0L
  for name in os.listdir(dir) :
    filepath = join(dir, name)
    filesize = 0L
    try :
      if isdir(filepath) :
        filesize = getdirsizebywalk(filepath)
      elif exists(filepath) :
        filesize = getsize(filepath)
    except :
      filesize = 0L
    listfile.append((filepath, filesize))
  
  #对文件进行从大到小排序
  listfile.sort(lambda x,y:cmp(x[1],y[1]), reverse = True)
  for item in listfile :
    log(item[0] + " : " + sizetostring(item[1]))
  return  
    
