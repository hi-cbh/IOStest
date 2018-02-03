#coding:utf-8

import atx

import wda,time
import unittest
from src.testcase.newcode.basecase.send import Send
from src.base.basecmd import BaseCMD
from src.base.baseImage import BaseImage
from src.readwriteconf.saveData import save
from src.mail.mailOperation import EmailOperation
from src.readwriteconf.initData import InitData
d = InitData().get_users()

username = d['user1']
pwd = d['pwd1']
username2 = d['user2']
pwd2 = d['pwd2']


class TestDown(unittest.TestCase):



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

    def testCaseDown(self):
        try:
            Send(self.s,username).send_action("appiumpythonios", is_save=False, is_accept=False)

            print("=>加载本地邮件封邮件")
            timeout = int(round(time.time() * 1000)) + 1*60 * 1000
            # 找到邮件结束
            while int(round(time.time() * 1000)) < timeout :
                print("=>等待邮件：appiumpythonios")
                el = self.element_wait()
                if el == False:
                    print("=>下拉")
                    self.s.swipe_down()
                    time.sleep(1)
                    print("=>下拉")
                    self.s.swipe_down()
                    time.sleep(1)
                else:
                    print("列表有邮件，退出循环")
                    break

                time.sleep(1)


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
            save.save("附件下载:%s" %value_time)

            self.s(label="Done").click_exists()
            time.sleep(5)
        except BaseException:
            # print("下载出错: %s" %error)
            # BaseImage.screenshot(self.driver, "DownFile")
            time.sleep(5)
            self.fail("【下载附件】出错")


    def element_wait(self):
        try:
            self.s(name="appiumpythonios").wait(2,True)
            return True
        except BaseException:
            return False



if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(TestDown('testCaseDown'))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)













