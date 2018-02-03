#coding:utf-8

import atx

import wda,time
import unittest
from src.readwriteconf.saveData import save
from src.base.basecmd import BaseCMD
from src.base.baseImage import BaseImage

from src.readwriteconf.initData import InitData
from src.mail.mailOperation import EmailOperation

# d = InitData().get_users()
#
# username = d['user2']
# pwd = d['pwd2']


class TestSelect(unittest.TestCase):



    def setUp(self):
        # BaseCMD.clear_app()
        # BaseCMD.install_app()
        # time.sleep(10)

        bundle_id = "com.cloudlinkin.139pushmail"
        self.c = wda.Client('http://localhost:8100') # DEVICE_URL
        self.s = self.c.session(bundle_id) # 启动应用


    def tearDown(self):
        self.c.home()
        time.sleep(2)
        self.s.close()

    def testCaseSelected(self):
        try:

            time.sleep(2)
            print("点击139精选")
            self.s(name="139精选").click_exists()
            start_time = time.time()

            print("等待阅读全文")
            time.sleep(2)
            self.s(name="阅读全文").wait(30)

            print('=>记录当前时间，')
            value_time = str(round((time.time() - start_time), 2))
            print('[139精选]: %r'  %value_time)
            save.save("收件箱列表中精选:%s" %value_time)

            time.sleep(5)
        except BaseException:
            BaseImage.screenshot(self.s, "testCaseSelected")
            time.sleep(5)
            self.fail("【139精选】出错！")


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(TestSelect('testcase'))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)













