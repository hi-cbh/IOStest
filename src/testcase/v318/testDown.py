# urs/bin/python
# encoding:utf-8
import unittest,time
from src.psam.psamio import Psam
from src.testcase.v318.basecase.login import Login
from src.testcase.v318.basecase.send import Send
from src.readwriteconf.initData import InitData
from src.base.baseImage import BaseImage
from src.mail.mailOperation import EmailOperation
d = InitData().get_users()

username = d['user1']
pwd = d['pwd1']
username2 = d['user2']
pwd2 = d['pwd2']


class TestDown(unittest.TestCase):


    def setUp(self):
        try:
            self.driver = Psam()
            print("success")
        except BaseException as error:
            self.fail("setUp启动出错！")

        else:
            EmailOperation(username+"@139.com", pwd).clear_forlder(['INBOX'])
            time.sleep(10)

            Login(self.driver,username,pwd).login_action(is_save=False)


    def tearDown(self):
        self.driver.quit()

    def testCaseDown(self):
        '''下载附件'''
        try:
            Send(self.driver,username).send_action("appiumpythonios", is_save=False)

            print("=>加载本地邮件封邮件")
            timeout = int(round(time.time() * 1000)) + 2*60 * 1000
            # 找到邮件结束
            while int(round(time.time() * 1000)) < timeout :
                print("=>等待邮件：appiumpythonios")
                el = self.driver.element_wait(r"id=>appiumpythonios",secs = 2)
                if el == None:
                    print("=>下拉")
                    self.driver.flick(150,100,150,400)
                    time.sleep(1)
                    print("=>下拉")
                    self.driver.flick(150,100,150,400)
                    time.sleep(1)
                else:
                    print("列表有邮件，退出循环")
                    break

                time.sleep(1)


            print("打开第一封邮件")
            self.driver.swipe(100,100,1,1,5)# 通过坐标点击第一封邮件

            print("点击全部下载")
            self.driver.click(u"id=>全部下载")

            print("开始记录")
            start = time.time()

            print("等待完成")
            self.driver.element_wait(u"id=>完成",120)
            # self.driver.element_gone(u"id=>全部下载",120)

            print('=>记录当前时间，')
            value_time = str(round((time.time() - start), 2))
            print('[下载附件]: %r'  %value_time)

            self.driver.click(u"id=>完成")
            time.sleep(3)

        except BaseException as error:
            BaseImage.screenshot(self.driver, "DownFile")
            time.sleep(5)
            self.fail("【下载附件】出错")



if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(TestDown('testCaseDown'))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)