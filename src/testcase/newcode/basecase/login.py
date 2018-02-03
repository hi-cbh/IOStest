import  time,unittest
from src.readwriteconf.saveData import save
from src.base.baseImage import BaseImage

class Login(unittest.TestCase):


    def __init__(self,session, username, pwd):
        self.username = username
        self.pwd = pwd
        self.s = session


    def login_action(self, is_save=True):
        '''基础登录功能'''
        try:

            print("sleep")
            time.sleep(1)

            print("左滑")
            self.s.swipe(300, 200, 100, 200, 0.5)
            time.sleep(2)
            self.s.swipe(300, 200, 100, 200, 0.5)

            print("sleep")
            time.sleep(2)
            print("点击体验")
            self.s.tap(100,488)

            print("sleep")
            time.sleep(2)

            print("点击139邮箱")
            self.s(name='new_login_139mail_logo.png').click_exists(2)

            time.sleep(2)

            print("输入账号")
            self.s(className='TextField').set_text(self.username)

            print("输入密码")
            self.s(className='SecureTextField').set_text(self.pwd)

            print("点击登录")
            self.s(name='登录').click_exists()
            start = time.time()

            print("等待元素消失")
            self.s(name='登录').wait_gone(30)


            print('=>记录当前时间，')
            value_time = str(round((time.time() - start), 2))
            print('[登录时延]: %r'  %value_time)

            if is_save:
                save.save("账号登录:%s" %value_time)

            time.sleep(3)
            print("点击 Allow")
            self.s(name="Allow").click_exists()

            time.sleep(2)

            print("点击 OK")
            self.s(name="OK").click_exists()
            time.sleep(2)

            print("验证页面是否存在")
            assert self.s(name="邮件").exists

            return value_time
        except BaseException:
            #BaseImage.screenshot(self.c, "loginAction")
            time.sleep(5)
            self.fail("账号登录出错")
