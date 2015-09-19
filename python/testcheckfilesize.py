#coding=utf-8

import sys
import os
from datetime import datetime
from checkfilesize import *

#把日志打印到屏幕中
setlogfile("a.log")

#文件超过该大小后，将输出日志
setlogsizethresdhold(500*1024*1024)

dir = os.getenv("APPDATA")
if (len(sys.argv) > 1) :
  dir = sys.argv[1]

log("")
log(datetime.now().strftime("%A, %d. %B %Y %I:%M %p"))

#通过递归方式获取指定目录的大小
log("")
print "Start to traverse dir - %s" %dir
totalsize = getdirsizerecursive(dir)
print "The total size of dir - %s : %s" %(dir, sizetostring(totalsize))

#列出当前目录下所有子目录的大小
log("")
print "Start to list all child dir of %s" %dir
listchildsize(dir)
print "finish list all child dir of %s" %dir
print "end"
