import os

class BaseCMD(object):

    def del_app(self, name):
        os.popen("xcrun simctl uninstall booted " + name)
        print("del success: %s " %name)


    def clear_app(self):
        self.del_app("com.cloudlinkin.139pushmail")


    def install_app(self):
        os.popen("xcrun simctl install booted /Users/apple/Desktop/Build/Products/Debug-iphonesimulator/139PushMail.app")
        print("install success")

BaseCMD = BaseCMD()