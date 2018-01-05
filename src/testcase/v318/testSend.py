# urs/bin/python
# encoding:utf-8

import unittest,time
from src.psam.psamio import Psam
from src.testcase.v318.basecase.send import Send
from src.testcase.v318.basecase.login import Login
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
        try:
            self.driver = Psam()
        except BaseException as error:
            self.fail("setUp启动出错！")

        else:
            EmailOperation(username+"@139.com", pwd).clear_forlder(['INBOX'])
            time.sleep(10)

            Login(self.driver,username,pwd).login_action(is_save=False)


    def tearDown(self):
        self.driver.quit()
        time.sleep(10)
        print("run end")

    def testCaseSend(self):
        '''发送邮件'''
        Send(self.driver,username).send_action("appiumpythonios")

    def testCaseFwdSend(self):
        '''转发邮件'''
        Send(self.driver,username).send_fwd_action(receiver, receiver)





if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(TestSend('testCaseSend'))
    suite.addTest(TestSend('testCaseFwdSend'))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)