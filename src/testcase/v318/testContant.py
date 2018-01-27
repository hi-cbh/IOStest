# urs/bin/python
# encoding:utf-8
import unittest,time
from src.psam.psamio import Psam
from src.testcase.v318.basecase.login import Login
from src.readwriteconf.initData import InitData
from src.base.baseImage import BaseImage
from src.mail.mailOperation import EmailOperation
d = InitData().get_users()

username = d['user1']
pwd = d['pwd1']
username2 = d['user2']
pwd2 = d['pwd2']


class TestContant(unittest.TestCase):


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

    def testCaseConant(self):
        '''联系人同步'''
        try:

            print("点击联系人")
            self.driver.click(u"id=>联系人")
            print("截图")
            BaseImage.screenshot(self.driver,"testConant")

            print("开始计时")
            start = time.time()

            print("页面加载60秒")
            # 等待两分钟
            timeout = int(round(time.time() * 1000)) + 60 * 1000
            try:
                while (int(round(time.time() * 1000) < timeout)):
                    print("=>下拉")
                    self.driver.swipeDown()
                    # 这里需要实际情况，是否添加时延
                    print("=>截图判断")
                    d = BaseImage.screenshot(self.driver,"testConant")
                    if d["result"] and BaseImage.get_pic_txt(d['path']).__contains__("手机联系人同步完成"):
                        break
                    time.sleep(1)
                    # print("超时")
            except BaseException as msg:
                print(msg)

            print('=>记录当前时间，')
            value_time = str(round((time.time() - start), 2))
            print('[联系人同步时间]: %r'  %value_time)

            time.sleep(3)

        except BaseException:
            BaseImage.screenshot(self.driver, "Conant")
            time.sleep(5)
            self.fail("【联系人同步】出错")


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(TestContant('testCaseConant'))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)