import unittest,os,sys
# 添加环境路径，脚本
p = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print("path: %s" %p)
sys.path.append(p+"/")


import time, datetime
from src.base.baseTime import BaseTime
from src.readwriteconf.initData import InitData
from src.readwriteconf.saveData import save
from src.reportlib.reportclass import ReportClass

from src.testcase.HTMLTestRunner import HTMLTestRunner
import random
localPath = InitData().get_sys_path()["savepath"]
# 信息存储路径
reportPath = localPath + "/reports/"
logPath = localPath + "/logs/"
iniPath = localPath + '/ini/'


logfileName= BaseTime.get_date_hour() + '.log'




class MyTest(unittest.TestCase):


    @classmethod
    def setUpClass(self):
        print("setUp.....")
        self.testRun = False

    @classmethod
    def tearDownClass(self):
        print("tearDown......")


    def testCase01(self):
        try:
            start = time.time()
            if int(random.random() * 10) > 5:
                self.assertTrue(True, "测试错误")
            else:
                self.assertTrue(False, "测试错误")

            print("testCase01")
            time.sleep(1)
            print('=>记录当前时间，时间差')
            valueTime = str(round((time.time() - start), 2))
            print('[登录时延]: %r'  %valueTime)
            save.save("用例1:%s" %valueTime)
        except BaseException:
            self.fail("用例1 错误")

        else:
            print("testCase01")


    def testCase02(self):
        try:
            if int(random.random() * 10) > 5:
                self.assertTrue(True, "测试错误")
            else:
                self.assertTrue(False, "测试错误")
            print("testCase02")
        except BaseException:
            self.fail("testCase02 错误")

        else:
            print("testCase02")


class MyTest2(unittest.TestCase):


    def setUp(self):
        time.sleep(1)
        print("MyTest2 setUp.....")
        self.testRun = False


    def tearDown(self):
        print("MyTest2 tearDown......")



    def testCase03(self):
        print("testCase01")
        start = time.time()
        time.sleep(1)
        print('=>记录当前时间，时间差')
        valueTime = str(round((time.time() - start), 2))
        print('[登录时延]: %r'  %valueTime)
        save.save("用例3:%s" %valueTime)


    def testCase04(self):
        try:
            if int(random.random() * 10) > 5:
                self.assertTrue(True, "测试错误")
            else:
                self.assertTrue(False, "测试错误")
            print("testCase03")

        except BaseException:
            self.fail("MyTest2 testCase04 错误")
        else:
            print("testCase04 return")
            return 0





if __name__ == '__main__':
    speed = ''

    # 添加测试的用例
    testtxt=[]
    testtxt.append(("用例1","testCase01"))
    testtxt.append(("用例2","testCase02"))
    testtxt.append(("用例3","testCase03"))
    testtxt.append(("用例4","testCase04"))

    suite = unittest.TestSuite()
    suite.addTest(MyTest('testCase01'))
    suite.addTest(MyTest('testCase02'))
    suite.addTest(MyTest2('testCase03'))
    suite.addTest(MyTest2('testCase04'))

    # 生成html
    now = time.strftime("%Y-%m-%d %H_%M_%S")
    filename_now = time.strftime("%Y_%m_%d_%H_%M_%S")
    filename = reportPath + now + '_result.html'
    fp = open(filename, 'wb')
    runner = HTMLTestRunner(stream=fp,title='Test Report', description='DialsMeasured with: ')
    testResultReport = runner.run(suite)
    fp.close()

    time.sleep(2)


    ReportClass(testResultReport.failures,testtxt,speed,now).all()

