#coding:utf-8

import atx

import wda,time
import unittest
from src.base.basecmd import BaseCMD
from src.base.baseImage import BaseImage

class TestContant(unittest.TestCase):



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

    def testCaseConant(self):
        try:

            time.sleep(2)
            print("点击联系人")
            self.s(name="联系人").click_exists()
            start_time = time.time()

            print("截图")
            time.sleep(2)
            BaseImage.screenshot(self.c,"testConant")

            print("开始计时")
            start = time.time()

            print("页面加载60秒")
            # 等待两分钟
            timeout = int(round(time.time() * 1000)) + 60 * 1000
            try:
                while (int(round(time.time() * 1000) < timeout)):
                    print("=>截图判断")
                    d = BaseImage.screenshot(self.c,"testConant")
                    if d["result"] and BaseImage.get_pic_txt(d['path']).__contains__("手机联系人同步完成"):
                        break

                    time.sleep(1)

                    print("=>下拉")
                    self.s.swipe_down()
                    # 这里需要实际情况，是否添加时延


                    # print("超时")
            except BaseException as msg:
                print(msg)

            print('=>记录当前时间，')
            value_time = str(round((time.time() - start_time), 2))
            print('[139精选]: %r'  %value_time)
            time.sleep(5)
        except BaseException:
            # BaseImage.screenshot(self.driver, "Conant")
            time.sleep(5)
            self.fail("【联系人同步】出错")


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(TestContant('testcase'))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)













