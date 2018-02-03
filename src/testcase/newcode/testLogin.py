#coding:utf-8
import os,sys

# 添加环境路径，脚本
p = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
print("path: %s" %p)
sys.path.append(p+"/")
import wda,time
import unittest
from src.base.basecmd import BaseCMD
from src.testcase.newcode.basecase.login import Login
from src.readwriteconf.initData import InitData

d = InitData().get_users()
username = d['user1']
pwd = d['pwd1']



class TestLogin(unittest.TestCase):

    def setUp(self):
        BaseCMD.clear_app()
        time.sleep(5)
        BaseCMD.install_app()
        time.sleep(10)

        bundle_id = "com.cloudlinkin.139pushmail"
        self.c = wda.Client('http://localhost:8100') # DEVICE_URL
        self.s = self.c.session(bundle_id) # 启动应用


    def tearDown(self):
        self.c.home()
        time.sleep(2)
        self.s.close()

    def testCaseLogin(self):
        Login(self.s, username,pwd).login_action()



if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(TestLogin('testcase'))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)