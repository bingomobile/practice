#coding=utf-8

import os
from os.path import join, getsize, isdir, exists

#��־�ļ������δ������־�ļ������ӡ����Ļ
LOGFILE = "checkfilesize.log"

#���������С���ļ���Ŀ¼���������־
LOGSIZETHRESHOLD = 500*1024*1024

def setlogfile(logfile) :
  global LOGFILE
  LOGFILE = logfile
  return
  
def setlogsizethresdhold(size) :
  global LOGSIZETHRESHOLD
  LOGSIZETHRESHOLD = size
  return

#��־������ӡ���ļ�����Ļ
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

#�ļ���Сת��Ϊ�ַ���
def sizetostring(size) :
  if size > 1024*1024*1024:
    return "%.2f GB" %(float(size)/1024/1024/1024)
  elif size > 1024*1024 :
    return "%.2f MB" %(float(size)/1024/1024)
  elif size > 1024 :
    return "%.2f KB" %(float(size)/1024)
  else :
    return "%.2f B" %(float(size))

#�ļ�����һ����С����ӡ�ļ�·�������С
def checksize(filepath, filesize) :
  global LOGSIZETHRESHOLD
  if filesize > LOGSIZETHRESHOLD :
    log(filepath + " : " + sizetostring(filesize))
  return
    
#ͨ��os.walk�����ļ��õ�Ŀ¼���ܴ�С
def getdirsizebywalk(dir) :
  totalsize = 0L
  dirsize = 0L
  filesize = 0L
  filepath = ""
  #os.walk���������Ƕ����Ŀ¼
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

#ͨ�������ݹ�ķ�ʽ����ȡĿ¼���ܴ�С
#����ļ���Ŀ¼�Ĵ�С������ֵ�����ӡ�ļ�·���ʹ�С
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

#�г�ָ��Ŀ¼�µ������ļ���Ŀ¼���ܴ�С
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
  
  #���ļ����дӴ�С����
  listfile.sort(lambda x,y:cmp(x[1],y[1]), reverse = True)
  for item in listfile :
    log(item[0] + " : " + sizetostring(item[1]))
  return  
    
