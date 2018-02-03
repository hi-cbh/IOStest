#coding:utf-8

import atx

import wda,time
import unittest
from src.base.basecmd import BaseCMD
from src.testcase.newcode.basecase.send import Send
from src.readwriteconf.initData import InitData
from src.mail.mailOperation import EmailOperation


d = InitData().get_users()

username = d['user1']
pwd = d['pwd1']
username2 = d['user2']
pwd2 = d['pwd2']

receiver = {'name':username, 'pwd':pwd}
sender = {'name':username2, 'pwd':pwd2}

class TestSend(unittest.TestCase):



    def setUp(self):
        # BaseCMD.clear_app()
        # BaseCMD.install_app()
        # time.sleep(10)

        bundle_id = "com.cloudlinkin.139pushmail"
        self.c = wda.Client('http://localhost:8100') # DEVICE_URL
        self.s = self.c.session(bundle_id) # 启动应用

        EmailOperation(username+"@139.com", pwd).clear_forlder(['INBOX'])
        time.sleep(5)

        print("=>下拉")
        self.s.swipe_down()
        time.sleep(1)
        print("=>下拉")
        self.s.swipe_down()
        time.sleep(1)


    def tearDown(self):
        self.c.home()
        time.sleep(2)
        self.s.close()

    def testCaseSend(self):

        Send(self.s,username).send_action(subjetc="appiumpythonios")


    def testCaseFwdSend(self):

        Send(self.s,username).send_fwd_action(receiver, receiver, is_accept=False)

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(TestSend('testcase'))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)