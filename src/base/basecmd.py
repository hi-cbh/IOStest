# urs/bin/python
# encoding:utf-8

import os

class BaseCMD(object):
    '''使用命令行控制'''
    def __init__(self):
        pass


    def del_app(self, name):
        print("del_app %s" %name)
        os.popen("xcrun simctl uninstall booted " + name)
        print("delete success.")

    def clear_app(self):
        self.del_app("com.apple.test.WebDriverAgentRunner-Runner")
        self.del_app("com.cloudlinkin.139pushmail")



BaseCMD = BaseCMD()

if __name__ == "__main__":
    bc = BaseCMD
    bc.clear_app()
