# urs/bin/python
# encoding:utf-8

import unittest,os,sys
import time, datetime


# 添加环境路径，脚本
p = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
print("path: %s" %p)
sys.path.append(p+"/")


localPath = "/var/appiumRunLogIos"
from src.base.baseImage import BaseImage
print("hellowrld")