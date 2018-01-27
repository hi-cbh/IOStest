import unittest
import time
from src.psam.psamio import Psam
from src.testcase.v318.basecase.login import Login
from src.readwriteconf.initData import InitData
from src.mail.mailOperation import EmailOperation

d = InitData().get_users()

username = d['user1']
pwd = d['pwd1']



'''账号登录'''
class TestLogin(unittest.TestCase):

    def setUp(self):
        try:

            self.driver = Psam()
            print("success")#iphone5s

        except BaseException as error:
            self.fail("setUp启动错误")

        # else:
        #     EmailOperation(username+"@139.com", pwd).clear_forlder(['INBOX'])
        #     time.sleep(10)


    def tearDown(self):
        self.driver.quit()

    def testCaseLogin(self):
        '''账号登录'''
        Login(self.driver,username,pwd).login_action()




if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(TestLogin('testCaseLogin'))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
