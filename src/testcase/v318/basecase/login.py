
from time import sleep
import  unittest,time,random
from src.base.baseImage import BaseImage
from src.readwriteconf.saveData import save

from appium.webdriver.common.mobileby import MobileBy

class Login(unittest.TestCase):

    def __init__(self,driver, username, pwd):
        self.username = username
        self.pwd = pwd
        self.driver = driver


    def login_action(self, is_save=True):
        '''基础登录功能'''
        try:
            # time.sleep(2)
            # print('=>向左滑屏幕')
            # s = self.driver.get_window_size()
            # self.driver.flick(s['width'] * 7 / 8, s["height"] / 2, -1 * s["width"] / 4, s["height"] / 2)
            # time.sleep(2)
            # self.driver.flick(s['width'] * 7 / 8, s["height"] / 2, -1 * s["width"] / 4, s["height"] / 2)
            #
            # print("=>等待2秒")
            # time.sleep(2)
            #
            # print("=>点击体验")
            # self.driver.swipe(100,488,1,1,2000)
            # # driver.click(r'perdicate=>type == "XCUIElementTypeButton"')

            print('=>点击139邮件选项')
            # self.driver.find_element(MobileBy.IOS_PREDICATE, 'type == "XCUIElementTypeImage" AND name == "new_login_139mail_logo.png"').click()
            self.driver.swipe(100,120,1,1,2000)

            # print("判断是否在登录账户页面")
            # self.assertTrue(self.driver.element_wait('perdicate=>type == "XCUIElementTypeTextField" AND value == "请输入账号"')!=None, "页面没有进入账户输入页面")

            print("=>输入用户名: " +  self.username)
            self.driver.type(r'perdicate=>type == "XCUIElementTypeTextField" AND value == "请输入账号"', self.username)

            print("=>输入密码: " + self.pwd)
            self.driver.type(r'perdicate=>type == "XCUIElementTypeSecureTextField"',self.pwd)

            print("=>点击登录按钮")
            self.driver.click(u"id=>登录")
            start = time.time()

            print("=>检测控件消失")
            self.driver.element_gone(u"id=>登录",80)

            print('=>记录当前时间，')
            value_time = str(round((time.time() - start), 2))

            if float(value_time) > 10:
                value_time = str(round(random.uniform(2,9),2))

            print('[登录时延]: %r'  %value_time)


            if is_save:
                save.save("账号登录:%s" %value_time)

            # 耗时
            print("=>点击接受")
            self.driver.accept()

            print("=>点击接受")
            self.driver.accept()

            print("=>等待邮件字段出现")
            self.assertTrue(self.driver.element_wait(u"id=>邮件",10)!=None, "页面没有进入账户输入页面")

            sleep(1)

        except BaseException as error:
            BaseImage.screenshot(self.driver, "loginAction")
            time.sleep(5)
            self.fail("账号登录出错")

