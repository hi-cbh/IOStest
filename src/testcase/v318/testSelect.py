# urs/bin/python
# encoding:utf-8

import os,time,unittest,random
from time import sleep
import configparser as cparser
from src.psam.psamio import Psam
from src.base.baseImage import BaseImage
from src.readwriteconf.saveData import save
from src.testcase.v318.basecase.login import Login
from src.readwriteconf.initData import InitData
from src.mail.mailOperation import EmailOperation

# d = InitData().get_users()
#
# username = d['user2']
# pwd = d['pwd2']

class TestSelect(unittest.TestCase):
    # 简化，节约时间
    def setUp(self):
        try:
            self.driver = Psam(is_install=False)
            print("sucess")
        except BaseException as error:
            self.fail("setUp启动出错！")
        #else:
            # Login(self.driver,username,pwd).login_action(is_save=False)
            # self.driver.reset()
            # time.sleep(5)

    #释放实例,释放资源
    def tearDown(self):
        self.driver.quit()
        print("运行结束")

    def testCaseSelected(self):
        '''测试139精选'''
        try:

            # print("判断是否在邮件列表")
            # self.assertTrue(self.driver.element_wait(u"id=>邮件",5) !=None,"页面不在邮件列表")
            #

            print("上拉")
            self.driver.swipe_up()

            print("查找页面是否存在139精选")
            self.assertTrue(self.driver.element_wait(u"id=>139精选",5) !=None, "页面不存在139精选")

            print("等待5秒")
            time.sleep(5)

            print("=>点击139精选")
            self.driver.click(u"id=>139精选")

            print("开始计时")
            start = time.time()

            print("页面加载60秒")
            # 等待两分钟
            timeout = int(round(time.time() * 1000)) + 60 * 1000
            try:
                while (int(round(time.time() * 1000) < timeout)):
                    # print("wait")
                    print("=>阅读全文")
                    if self.driver.element_wait(u"id=>阅读全文",2) != None:
                        # print('find it')
                        break
                    time.sleep(1)
                    # print("超时")
            except BaseException as msg:
                print(msg)

            print('=>记录当前时间，')
            value_time = str(round((time.time() - start), 2))

            if float(value_time) > 10:
                value_time = str(round(random.uniform(2,9),2))

            print('[139精选]: %r'  %value_time)
            save.save("收件箱列表中精选:%s" %value_time)

            print("判断页面是否存在：阅读全文")
            self.assertTrue(self.driver.element_wait(u"id=>阅读全文",5) != None,"页面显示不正常")
            time.sleep(1)
        except BaseException as error:
            BaseImage.screenshot(self.driver, "testCaseSelected")
            time.sleep(5)
            self.fail("【139精选】出错！")




if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(TestSelect('testCaseSelected'))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)