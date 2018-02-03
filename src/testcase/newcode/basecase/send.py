import time,unittest
from src.readwriteconf.saveData import save
from src.mail.sendEmailSmtp import SendMail


class Send(unittest.TestCase):

    def __init__(self,session, username):
        ''''''
        self.username = username
        self.s = session


    def send_action(self, subjetc="iosappiumpython", is_save=True, is_accept = True):
        '''发送待附件的邮件：拍照后发送邮件'''

        try:
            print("sleep")
            time.sleep(2)

            print("点击写信")
            self.s.tap(290, 35)
            time.sleep(2)

            print("输入接收者")
            self.s(className="TextField",index=0).set_text(self.username+"@139.com")

            time.sleep(2)
            print("输入主题")
            self.s(className="TextField")[2].set_text(subjetc)
            time.sleep(2)

            self.s(name="write fujian").click_exists()
            time.sleep(2)

            if is_accept:
                print("点击 OK")
                self.s(name="OK").click_exists()
                time.sleep(2)

            print("相册")
            self.s(name="write alter photo").click_exists()
            time.sleep(2)

            print("选择第一个")
            self.s.tap(110,90)

            time.sleep(2)

            print("选择图片")
            self.s.tap(50, 80)

            self.s(name=u"完成").click_exists()

            time.sleep(2)

            self.s(name=u"发送").click_exists()
            start_time = time.time()

            self.s(name="发送成功").wait(30)
            self.s(name="已完成").wait(30)

            print('=>记录当前时间，')
            value_time = str(round((time.time() - start_time), 2))
            print('[发送邮件]: %r'  %value_time)

            if is_save:
                save.save("发送邮件带附件:%s" %value_time)

            time.sleep(2)
            print("点击返回")
            self.s.tap(20,30)
            time.sleep(2)
        except BaseException:
            #BaseImage.screenshot(self.driver, "sendAction")
            time.sleep(5)
            self.fail("【发送邮件】出错")


    def send_fwd_action(self, reveicer, sender, is_accept=True):
        '''转发邮件'''

        try:

            print("=>第三方发送邮件")
            s = SendMail(sender['name'], sender['pwd'], reveicer['name'])
            self.assertTrue(s.send_mail_test('sendTestIOS','testIOS...'),"邮件发送失败")
            time.sleep(2)

            print("=>加载本地邮件封邮件")
            timeout = int(round(time.time() * 1000)) + 1*60 * 1000
            # 找到邮件结束
            while int(round(time.time() * 1000)) < timeout :
                print("=>等待邮件：sendTestIOS")
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

            time.sleep(2)

            print("点击转发")
            self.s.tap(165,520)

            print("输入接收者")
            self.s(className="TextField",index=0).set_text("13533348571@139.com")


            self.s(name="write fujian").click_exists()
            time.sleep(2)

            if is_accept:
                print("点击 OK")
                self.s(name="OK").click_exists()
                time.sleep(2)

            print("相册")
            self.s(name="write alter photo").click_exists()
            time.sleep(2)

            print("选择第一个")
            self.s.tap(110,90)

            time.sleep(2)

            print("选择图片")
            self.s.tap(50, 80)

            self.s(name=u"完成").click_exists()

            time.sleep(2)

            self.s(name=u"发送").click_exists()
            start_time = time.time()

            self.s(name="发送成功").wait(30)
            self.s(name="已完成").wait(30)

            print('=>记录当前时间，')
            value_time = str(round((time.time() - start_time), 2))
            print('[发送邮件]: %r'  %value_time)

            time.sleep(2)
            print("点击返回")
            self.s.tap(20,30)
            time.sleep(2)

        except BaseException :
            #BaseImage.screenshot(self.driver, "sendFWDAction")
            time.sleep(5)
            self.fail("【转发邮件】出错")


    def element_wait(self):
        try:
            self.s(name="sendTestIOS").wait(2,True)
            return True
        except BaseException:
            return False


