#coding=utf-8
import os
from os.path import join, getsize, isdir, exists

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

#得到文件夹的大小
def getdirsize(dir) :
  totalsize = 0L
  dirsize = 0L
  filesize = 0L
  filepath = ""
  threshold = 500*1024*1024 #500M的才显示
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
      #文件超过一定大小，打印文件路径及其大小
      if filesize > threshold :
        print filepath + " : " + sizetostring(filesize)
    
    totalsize += dirsize
    #文件夹超过一定大小，打印文件夹路径及其大小
    if dirsize > threshold :
      print root + " : " + sizetostring(dirsize)
      
  return totalsize  

def checksize(filepath, filesize) :
  #文件超过一定大小，打印文件路径及其大小
  threshold = 500*1024*1024 #500M的才显示
  if filesize > threshold :
    print filepath + " : " + sizetostring(filesize)

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

def listchildsize(dir) :
  for name in os.listdir(dir) :
    filepath = join(dir, name)
    filesize = 0L
    try :
      if isdir(filepath) :
        filesize = getdirsize(filepath)
      elif exists(filepath) :
        filesize = getsize(filepath)
    except :
      filesize = 0L
    print filepath + " : " + sizetostring(filesize)
    
    
"""
folder = r'C:\Users\bingoli\AppData\Roaming\Tencent\QQBrowser'
for name in os.listdir(folder) :
  print name
"""

folder = r'C:\Users\bingoli\AppData\Roaming'
listchildsize(folder);

"""
folder = r'C:\Users\bingoli'
totalsize = getdirsizerecursive(folder)
print folder + " : " + sizetostring(totalsize)
"""
