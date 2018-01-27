import  unittest
import  time
from time import sleep
from src.base.baseImage import BaseImage
from src.mail.sendEmailSmtp import SendMail
from appium.webdriver.common.mobileby import MobileBy
from src.readwriteconf.saveData import save

class Send(unittest.TestCase):

    def __init__(self,driver, username):
        ''''''
        self.username = username
        self.driver = driver

    def send_action(self, subjetc="iosappiumpython", is_save=True, is_accept = True):
        '''发送待附件的邮件：拍照后发送邮件'''
        try:
            # 写信
            print("=>点击写信按钮")
            elels = self.driver.get_sub_element("class=>XCUIElementTypeNavigationBar","class=>XCUIElementTypeButton",30)
            elels[3].click()

            print("=>输入收件人: " + self.username+"@139.com")
            self.driver.find_elements(MobileBy.CLASS_NAME,'XCUIElementTypeTextField')[0].send_keys(self.username+"@139.com")


            print("=>输入主题: " + subjetc)
            self.driver.find_elements(MobileBy.CLASS_NAME,'XCUIElementTypeTextField')[1].send_keys(subjetc)

            print("=>附件")
            self.driver.find_element(MobileBy.ACCESSIBILITY_ID,"write fujian").click()

            print("=>相册")
            self.photo(is_accept)

            time.sleep(4)

            print("=>发送")
            self.driver.click(u"id=>发送")
            start = time.time()

            print("=>等待发送完成")
            # 等待两分钟
            timeout = int(round(time.time() * 1000)) + 120 * 1000
            try:
                while (int(round(time.time() * 1000) < timeout)):
                    # print('wait.....')
                    s = self.driver.get_attribute(u"id=>进度","value",1)
                    print(s)
                    if(s == "100%"):
                        # print('find it')
                        break
                    time.sleep(0.1)
                    # print("超时")
            except BaseException as msg:
                print(msg)


            if is_save:
                print('=>记录当前时间，')
                value_time = str(round((time.time() - start), 2))
                print('[发送邮件]: %r'  %value_time)
                save.save("发送邮件带附件:%s" %value_time)

            time.sleep(3)
            # 返回
            # //XCUIElementTypeNavigationBar[@name="发送成功"]/XCUIElementTypeButton
            #visible	true
            print("返回")
            self.driver.get_sub_element("class=>XCUIElementTypeNavigationBar","class=>XCUIElementTypeButton",10)[0].click()

            print("等待1秒")
            time.sleep(1)

        except BaseException as error:
            print("下载出错: %s" %error)
            BaseImage.screenshot(self.driver, "sendAction")
            time.sleep(5)
            self.fail("【发送邮件】出错")


    def send_fwd_action(self, reveicer, sender):
        '''转发邮件'''
        try:
            print("\n 判断是否在邮件列表")
            self.assertTrue(self.driver.get_element(u"id=>邮件",5) != None,"页面不在邮件列表")

            print("=>第三方发送邮件")
            s = SendMail(sender['name'], sender['pwd'], reveicer['name'])
            self.assertTrue(s.send_mail_test('sendTestIOS','testIOS...'),"邮件发送失败")
            time.sleep(2)

            print("=>加载本地邮件封邮件")
            timeout = int(round(time.time() * 1000)) + 2*60 * 1000
            # 找到邮件结束
            while int(round(time.time() * 1000)) < timeout :

                el = self.driver.element_wait(r"id=>sendTestIOS",secs = 2)
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


            print("=>打开第一封邮件")
            self.driver.swipe(100,100,1,1,5)# 通过坐标点击第一封邮件

            print("=>点击转发")
            ls = self.driver.find_elements(MobileBy.IOS_PREDICATE,'type == "XCUIElementTypeButton" and visible == true')
            ls[5].click()

            print("=>输入收件人: "+self.username)
            self.driver.find_elements(MobileBy.CLASS_NAME,'XCUIElementTypeTextField')[0].send_keys(self.username + "@139.com")

            print("=>相册")
            self.photo(is_accept= False)

            print("=>发送")
            self.driver.click(u"id=>发送")
            start = time.time()

            print("页面的百分百")
            # 等待两分钟
            timeout = int(round(time.time() * 1000)) + 120 * 1000
            try:
                while (int(round(time.time() * 1000) < timeout)):
                    # print('wait.....')
                    s = self.driver.get_attribute(u"id=>进度","value",1)
                    print(s)
                    if(s == "100%"):
                        # print('find it')
                        break
                    time.sleep(0.1)
                    # print("超时")
            except BaseException as msg:
                print(msg)

            print('=>记录当前时间，')
            value_time = str(round((time.time() - start), 2))
            print('[转发附件]: %r'  %value_time)
            save.save("转发邮件带附件:%s" %value_time)

            time.sleep(1)
        except BaseException as error:
            print("下载出错: %s" %error)
            BaseImage.screenshot(self.driver, "sendFWDAction")
            time.sleep(5)
            self.fail("【转发邮件】出错")




    def photo_capture(self, is_accept=True):
        '''拍照'''

        if is_accept:
            # 点击弹窗允许
            print("=>点击允许")
            self.driver.accept()

        time.sleep(3)
        print("=>拍照")
        self.driver.find_elements(MobileBy.CLASS_NAME,"UIAButton")[0].click()# 拍照
        if is_accept:
            print("=>点击允许")
            self.driver.accept()

        print("=>开始拍照")
        self.driver.click(r"id=>PhotoCapture")# 拍照

        print("等待时间")
        time.sleep(3)

        print("=>使用照片")
        self.driver.click(u"id=>使用照片")# 使用

    def photo(self, is_accept=True):
        '''相册'''

        if is_accept:
            # 点击弹窗允许
            print("=>点击允许")
            self.driver.accept()

        time.sleep(3)
        print("=>相册")
        self.driver.find_elements(MobileBy.CLASS_NAME,"UIAButton")[1].click()


        time.sleep(2)
        print("=>选择第一个")
        self.driver.swipe(110,90,1,1,2000)

        print("等待时间")
        time.sleep(2)
        print("=>使用选择图片")
        self.driver.swipe(50,80,1,1,2000)

        # print("等待时间")
        # time.sleep(2)
        # print("=>使用选择图片")
        # self.driver.swipe(40,50,1,1,2000)

        print("=>选择完成")
        self.driver.click(u"id=>完成")
