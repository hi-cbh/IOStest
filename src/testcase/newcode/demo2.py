#coding:utf-8

import atx

import wda,time
import unittest
from src.base.basecmd import BaseCMD
from src.base.baseImage import BaseImage

class atxDemo(unittest.TestCase):



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

    def testcase(self):
        try:

            time.sleep(2)
            print("点击第一封邮件")
            self.s.tap(100,100)

            print("点击全部下载")
            time.sleep(2)
            self.s(name="全部下载").click_exists()

            start_time = time.time()

            print("等待完成")
            self.s(label="Done").wait(30)
            print('=>记录当前时间，')
            value_time = str(round((time.time() - start_time), 2))
            print('[下载时延]: %r'  %value_time)

            self.s(label="Done").click_exists()
            time.sleep(5)
        except BaseException:
            print("登录出错")
            return 0



if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(atxDemo('testcase'))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)













