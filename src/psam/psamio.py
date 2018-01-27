import time
from appium import webdriver
from selenium.webdriver.common.by import By
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from src.base.baseImage import BaseImage

class Psam(object):
    
    def __init__(self, version="11.1", device_name='ip5s', udid='6517E5E2-97B2-490A-9BCF-893A09A44D5F', bundle_id='com.cloudlinkin.139pushmail',is_install=True):
        print("\n启动driver")
        start = time.time()

        desired_caps = {}
        desired_caps['platformName'] = 'iOS'
        desired_caps['platformVersion'] = version
        desired_caps['deviceName'] = device_name
        desired_caps['udid'] = udid
        desired_caps['bundleId'] = bundle_id
        desired_caps['automationName'] = "XCUITest"
        desired_caps['autoAcceptAlerts'] = 'true'
        desired_caps['simpleIsVisibleCheck'] = True #，则有副作用，当滚动到不在屏幕上的不可见组件时，滚动不起作用，
        desired_caps['preventWDAAttachments'] = True
        desired_caps['useNewWDA'] = False
        desired_caps['noReset'] = False
        desired_caps['newCommandTimeout'] = 180
        # desired_caps['app'] = '/Users/admin/Desktop/Build/Products/Debug-iphoneos/139PushMail.app'
        print("重新安装app")
        if is_install:
            # desired_caps['app'] = '/Users/admin/Desktop/Build/Products/Debug-iphoneos/139PushMail.app'
            desired_caps['app'] = '/Users/admin/Desktop/Build/Products/Debug-iphonesimulator/139PushMail.app'

        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)


        print('=>记录当前时间，')
        value_time = str(round((time.time() - start), 2))
        print('[安装时间]: %r'  %value_time)

    def element_wait(self, css, secs = 10):
        '''
        Waiting for an element to display.

        Usage:
        driver.element_wait("css=>#el",10)
        '''
        if "=>" not in css:
            raise NameError("Positioning syntax errors, lack of '=>'.")

        by = css.split("=>")[0]
        value = css.split("=>")[1]
#         print('[%s] finding it！' %value)
#         print("等待秒数：%d" %secs )
        
        el = None
        try:
            if by == "id":
                el = WebDriverWait(self.driver,secs,1).until(EC.presence_of_element_located((By.ID, value)))
            elif by == "name":
                el = WebDriverWait(self.driver,secs,1).until(EC.presence_of_element_located((By.NAME, value)))
            elif by == "class":
                el = WebDriverWait(self.driver,secs,1).until(EC.presence_of_element_located((By.CLASS_NAME, value)))
            elif by == "link_text":
                el = WebDriverWait(self.driver,secs,1).until(EC.presence_of_element_located((By.LINK_TEXT, value)))
            elif by == "xpath":
                el = WebDriverWait(self.driver,secs,1).until(EC.presence_of_element_located((By.XPATH, value)))
            elif by == "css":
                el = WebDriverWait(self.driver,secs,1).until(EC.presence_of_element_located((By.CSS_SELECTOR, value)))
            elif by == "uiautomator":
                el = WebDriverWait(self.driver,secs,1).until(EC.presence_of_element_located((By.ANDROID_UIAUTOMATOR, u'new UiSelector().text("%s")' %value)))
            elif by == "uiautomation":
                el= WebDriverWait(self.driver,secs,1).until(EC.presence_of_element_located((By.IOS_UIAUTOMATION,value)))
            elif by == "perdicate":
                el= WebDriverWait(self.driver,secs,1).until(EC.presence_of_element_located((MobileBy.IOS_PREDICATE,value)))
            else:
                raise NameError("Please enter the correct targeting elements,'id','name','class','link_text','xpath','css', 'uiautomator'.")
            return el
        except BaseException as e:
            print('[%s] can not find it！' %value)
            return None


    def element_gone(self, css, secs = 10):
        '''
        等待元素消失

        Usage:
        driver.element_wait("css=>#el",10)
        '''
        if "=>" not in css:
            raise NameError("Positioning syntax errors, lack of '=>'.")

        by = css.split("=>")[0]
        value = css.split("=>")[1]
        #         print('[%s] finding it！' %value)
        #         print("等待秒数：%d" %secs )

        el = None
        try:
            if by == "id":
                el = WebDriverWait(self.driver,secs,1).until_not(EC.presence_of_element_located((By.ID, value)))
            elif by == "name":
                el = WebDriverWait(self.driver,secs,1).until_not(EC.presence_of_element_located((By.NAME, value)))
            elif by == "class":
                el = WebDriverWait(self.driver,secs,1).until_not(EC.presence_of_element_located((By.CLASS_NAME, value)))
            elif by == "link_text":
                el = WebDriverWait(self.driver,secs,1).until_not(EC.presence_of_element_located((By.LINK_TEXT, value)))
            elif by == "xpath":
                el = WebDriverWait(self.driver,secs,1).until_not(EC.presence_of_element_located((By.XPATH, value)))
            elif by == "css":
                el = WebDriverWait(self.driver,secs,1).until_not(EC.presence_of_element_located((By.CSS_SELECTOR, value)))
            elif by == "uiautomator":
                el = WebDriverWait(self.driver,secs,1).until_not(EC.presence_of_element_located((By.ANDROID_UIAUTOMATOR, u'new UiSelector().text("%s")' %value)))
            elif by == "uiautomation":
                el= WebDriverWait(self.driver,secs,1).until_not(EC.presence_of_element_located((By.IOS_UIAUTOMATION,value)))
            elif by == "perdicate":
                el= WebDriverWait(self.driver,secs,1).until_not(EC.presence_of_element_located((MobileBy.IOS_PREDICATE,value)))
            else:
                raise NameError("Please enter the correct targeting elements,'id','name','class','link_text','xpath','css', 'uiautomator'.")
            return el
        except BaseException as e:
            print('[%s] can not find it！' %value)
            return None








    def get_element(self,css, secs=30):
        
        self.element_wait(css, secs)
        '''
        Judge element positioning way, and returns the element.
        '''
        if "=>" not in css:
            raise NameError("Positioning syntax errors, lack of '=>'.")

        by = css.split("=>")[0]
        value = css.split("=>")[1]
        # print("value")
        try:
            if by == "id":
                element = self.driver.find_element_by_accessibility_id(value)
            elif by == "name":
                element = self.driver.find_element_by_name(value)
            elif by == "class":
                element = self.driver.find_element_by_class_name(value)
            elif by == "link_text":
                element = self.driver.find_element_by_link_text(value)
            elif by == "xpath":
                element = self.driver.find_element_by_xpath(value)
            elif by == "css":
                element = self.driver.find_element_by_css_selector(value)
            elif by == "uiautomator":
                element = self.driver.find_element_by_android_uiautomator(u'new UiSelector().text("%s")' %value)
            elif by == "uiautomation":
                element = self.driver.find_element_by_ios_uiautomation(value)
            elif by == "perdicate":
                element = self.driver.find_element_by_ios_predicate(value)
            else:
                raise NameError("Please enter the correct targeting elements,'id','name','class','link_text','xpath','css'.")
            return element
        except BaseException as error:
            return None 


    def get_elements(self,css,secs=30 ):
             
        self.element_wait(css, secs)
        '''
        Judge element positioning way, and returns the element.
        '''
        if "=>" not in css:
            raise NameError("Positioning syntax errors, lack of '=>'.")

        by = css.split("=>")[0]
        value = css.split("=>")[1]
        try:
            if by == "id":
                elements = self.driver.find_elements_by_id(value)
            elif by == "name":
                elements = self.driver.find_elements_by_name(value)
            elif by == "class":
                elements = self.driver.find_elements_by_class_name(value)
            elif by == "link_text":
                elements = self.driver.find_elements_by_link_text(value)
            elif by == "xpath":
                elements = self.driver.find_elements_by_xpath(value)
            elif by == "css":
                elements = self.driver.find_elements_by_css_selector(value)
            elif by == "uiautomator":
                elements = self.driver.find_elements_by_android_uiautomator(u'new UiSelector().text("%s")' %value)
            else:
                raise NameError("Please enter the correct targeting elements,'id','name','class','link_text','xpath','css'.")
            return elements
        
        except BaseException as error:
            return None      
    
    def get_sub_element(self, css1, css2, secs=20):
        '''实现查找子控件'''
        # self.element_wait(css2, secs)
        
        element = self.get_element(css1, secs)

        if "=>" not in css2:
            raise NameError("Positioning syntax errors, lack of '=>'.")

        by = css2.split("=>")[0]
        value = css2.split("=>")[1]
        
        try:
            if by == "id":
                elements = element.find_elements_by_id(value)
            elif by == "name":
                elements = element.find_elements_by_name(value)
            elif by == "class":
                elements = element.find_elements_by_class_name(value)
            elif by == "link_text":
                elements = element.find_elements_by_link_text(value)
            elif by == "xpath":
                elements = element.find_elements_by_xpath(value)
            elif by == "css":
                elements = element.find_elements_by_css_selector(value)
            elif by == "uiautomator":
                elements = self.driver.find_element_by_android_uiautomator(u'new UiSelector().text("%s")' %value)
            else:
                raise NameError("Please enter the correct targeting elements,'id','name','class','link_text','xpath','css'.")
            return elements
        except BaseException as error:
            return None   

    def type(self, css, text):
        '''
        Operation input box.

        Usage:
        driver.type("css=>#el","selenium")
        '''
        # self.element_wait(css)
        el = self.get_element(css)
        el.send_keys(text)

    def hide_keyboard(self):
        self.driver.hide_keyboard()

    def set_value(self, css, text):
        '''
        Operation input box. appium 1.6

        Usage:
        driver.type("css=>#el","selenium")
        '''
        # self.element_wait(css)
        el = self.get_element(css)
        el.set_value(text)



    def clear(self, css):
        '''
        Clear the contents of the input box.

        Usage:
        driver.clear("css=>#el")
        '''
        # self.element_wait(css)
        el = self.get_element(css)
        el.clear()

    def click(self, css,secs=10 ):
        '''
        It can click any text / image can be clicked
        Connection, check box, radio buttons, and even drop-down box etc..

        Usage:
        driver.click("css=>#el")
        '''
        # self.element_wait(css,secs)
        el = self.get_element(css,secs)
        if el == None:
            print("%s 元素为None" %css)
            return
        el.click()    

    def get_attribute(self, css, attribute,secs=30):
        '''
        Gets the value of an element attribute.

        Usage:
        driver.get_attribute("css=>#el","type")
        '''
        el = self.get_element(css,secs)
        return el.get_attribute(attribute)

    def get_text(self, css):
        '''
        Get element text information.

        Usage:
        driver.get_text("css=>#el")
        '''
        # self.element_wait(css)
        el = self.get_element(css)
        return el.text

    def get_display(self, css):
        '''
        Gets the element to display,The return result is true or false.

        Usage:
        driver.get_display("css=>#el")
        '''
        # self.element_wait(css)
        el = self.get_element(css)
        return el.is_displayed()

    def reset(self):
        '''
                    重置 app
        '''
        self.driver.reset()
 

    def swipe_up(self):
        '''向上滑动'''
        d = self.driver.get_window_size()
        l = (d['width'],d['height'])

        x1 = int(l[0] * 0.5)    #获取x坐标，根据实际调整相乘参数
        y1 = int(l[1] * 0.8)    #获取起始y坐标，根据实际调整相乘参数
        y2 = int(l[1] * 0.2)    #获取终点y坐标，根据实际调整相乘参数

        self.driver.flick(x1, y1, x1, y2)
        time.sleep(2)


 
    def swipe_down(self):
        '''向下滑动'''
        d = self.driver.get_window_size()
        l = (d['width'],d['height'])

        x1 = int(l[0] * 0.5)    #获取x坐标，根据实际调整相乘参数
        y2 = int(l[1] * 0.8)    #获取起始y坐标，根据实际调整相乘参数
        y1 = int(l[1] * 0.2)    #获取终点y坐标，根据实际调整相乘参数

        self.driver.flick(x1, y1, x1, y2)
        time.sleep(2)

    def swipe_left(self):
        '''向左滑动'''
        s = self.driver.get_window_size()
        self.driver.flick(s['width'] * 7 / 8, s["height"] / 2, -1 * s["width"] / 4, s["height"] / 2)
        time.sleep(1)


    def swipe_right(self):
        '''向右滑动'''
        s = self.driver.get_window_size()
        self.driver.flick(s['width'] /4, s["height"] / 2, s["width"] * 7 / 8, s["height"] / 2)
        time.sleep(1)

    def get_window_size(self):
        width = self.driver.get_window_size()['width']
        height = self.driver.get_window_size()['height']
        return {'width':width, 'height':height}

    def quit(self):
        '''
        Quit the driver and close all the windows.

        Usage:
        driver.quit()
        '''
        self.driver.quit()

    def close(self):
        self.driver.close()


    def close_app(self):
        self.driver.close_app()


    def launch_app(self):
        self.driver.launch_app()

    def swipe(self,start_x, start_y, end_x, end_y, duration):
        '''滑动'''
        self.driver.swipe(start_x, start_y, end_x, end_y, duration)

    def flick(self,start_x, start_y, end_x, end_y):
        self.driver.flick(start_x, start_y, end_x, end_y)


    def screenshot(self,filename):
        '''截屏'''
        self.driver.save_screenshot(filename)

    def implicitly_wait(self, secs = 10):
        '''隐式等待'''
        self.driver.implicitly_wait(secs)

    def uiautomator(self,uia_string):
        return self.driver.find_element_by_android_uiautomator(uia_string)
        # self.driver.find_element_by_android_uiautomator('new UiSelector().description("%s")' %uia_string)

    def find_element(self,by,value):
        return self.driver.find_element(by,value)

    def find_elements(self,by,value):
        return self.driver.find_elements(by,value)


    def accept(self):
        start = time.time()
        time.sleep(2)
        # self.driver.switch_to.alert.accept()
        self.execute_script('mobile:alert',{'action' : 'accept'})
        value_time = str(round((time.time() - start), 2))
        print('[点击允许需要时间]: %r'  %value_time)


    def execute_script(self,script,*args):
        self.driver.execute_script(script, *args)

    def page_source(self):
        '''获取页面元素'''
        return self.driver.page_source


    def background_app(self,secs=30):
        '''相当于按Home键'''
        self.driver.background_app(secs)


#     def scrollTo(self):
#         self.driver.scroll(origin_el, destination_el)

def login(driver):
    time.sleep(2)
    print('向左滑')
    s = driver.get_window_size()
    driver.flick(s['width'] * 7 / 8, s["height"] / 2, -1 * s["width"] / 4, s["height"] / 2)

    print("等待2秒")
    time.sleep(2)

    print("点击体验")
    driver.swipe(100,418,1,1,2000)
    # driver.click(r'perdicate=>type == "XCUIElementTypeButton"')



    print('点击139邮件选项')
    driver.find_element(MobileBy.IOS_PREDICATE, 'type == "XCUIElementTypeImage" AND name == "new_login_139mail_logo.png"').click()

    # assertTrue(driver.element_wait('perdicate=>type == "XCUIElementTypeTextField" AND value == "请输入账号"')!=None, "页面没有进入账户输入页面")

    print("输入用户名")
    driver.type(r'perdicate=>type == "XCUIElementTypeTextField" AND value == "请输入账号"', "18899734340")

    print("输入密码")
    driver.type(r'perdicate=>type == "XCUIElementTypeSecureTextField"',"hy12345678")

    print("点击登录按钮")
    driver.click(u"id=>登录")
    start = time.time()

    print("检测控件消失")
    driver.element_gone(u"id=>登录",60)

    print('=>记录当前时间，')
    value_time = str(round((time.time() - start), 2))
    print('[登录时延]: %r'  %value_time)

    print("点击接受")
    driver.accept()

    print("点击接受")
    driver.accept()

    print("等待邮件字段出现")
    driver.element_wait(u"id=>邮件",10)


def send(driver):
    print("等待5秒")
    time.sleep(5)

    # 写信
    elels = driver.get_sub_element("class=>XCUIElementTypeNavigationBar","class=>XCUIElementTypeButton",30)
    # print("写信：%s" %elels[3].is_displayed())
    elels[3].click()

    print("收件人")
    driver.find_elements(MobileBy.CLASS_NAME,'XCUIElementTypeTextField')[0].send_keys("18899734340@139.com")


    print("主题")
    driver.find_elements(MobileBy.CLASS_NAME,'XCUIElementTypeTextField')[1].send_keys("test")

    print("发送")
    print(driver.get_element(u"id=>发送").is_displayed())


    print("附件")
    driver.find_element(MobileBy.ACCESSIBILITY_ID,"write fujian").click()

    # 点击弹窗允许
    print("点击允许")
    driver.accept()

    time.sleep(3)
    print("拍照")
    driver.find_elements(MobileBy.CLASS_NAME,"UIAButton")[0].click()# 拍照

    print("点击允许")
    driver.accept()

    print("开始拍照")
    driver.click(r"id=>PhotoCapture")# 拍照
    time.sleep(5)
    driver.click(u"id=>使用照片")# 使用

    print("发送")
    driver.click(u"id=>发送")
    start = time.time()

    print("页面的百分百")
    # 等待两分钟
    timeout = int(round(time.time() * 1000)) + 120 * 1000
    try:
        while (int(round(time.time() * 1000) < timeout)):
            # print('wait.....')
            s = driver.get_attribute(u"id=>进度","value",1)
            print(s)
            if(s == "100%"):
                # print('find it')
                break
            time.sleep(0.1)
    except BaseException as msg:
        print(msg)


    print('=>记录当前时间，')
    value_time = str(round((time.time() - start), 2))
    print('[登录时延]: %r'  %value_time)


def fwdsend(driver):
    '''转发'''
    print("等待30秒")
    time.sleep(30)


    print("打开第一封邮件")
    driver.swipe(100,100,1,1,5)# 通过坐标点击第一封邮件
    # self.driver.click("xpath=>//UIAApplication[1]/UIAWindow[1]/UIATableView[2]/UIATableCell[1]")

    print("点击转发")
    ls = driver.find_elements(MobileBy.IOS_PREDICATE,'type == "XCUIElementTypeButton" and visible == true')
    ls[5].click()

    print("收件人")
    driver.find_elements(MobileBy.CLASS_NAME,'XCUIElementTypeTextField')[0].send_keys("18899734340@139.com")

    print("发送")
    driver.click(u"id=>发送")
    start = time.time()


    print("页面的百分百")
    # 等待两分钟
    timeout = int(round(time.time() * 1000)) + 120 * 1000
    try:
        while (int(round(time.time() * 1000) < timeout)):
            # print('wait.....')
            s = driver.get_attribute(u"id=>进度","value",1)
            print(s)
            if(s == "100%"):
                # print('find it')
                break
            time.sleep(0.1)
    except BaseException as msg:
        print(msg)


    print('=>记录当前时间，')
    value_time = str(round((time.time() - start), 2))
    print('[登录时延]: %r'  %value_time)


def select(driver):
    '''收件箱列表的精选'''
    print("点击139精选")
    driver.click(u"id=>139精选")

    start = time.time()

    print("页面加载60秒")
    # 等待两分钟
    timeout = int(round(time.time() * 1000)) + 60 * 1000
    try:
        while (int(round(time.time() * 1000) < timeout)):
            print("wait")
            if driver.element_wait(u"id=>阅读全文",2) != None:
                print('find it')
                break
            time.sleep(1)
    except BaseException as msg:
        print(msg)

    print("判断页面是否存在：阅读全文")
    print(driver.element_wait(u"id=>阅读全文",3) != None )

    print('=>记录当前时间，')
    value_time = str(round((time.time() - start), 2))
    print('[登录时延]: %r'  %value_time)


def down(driver):

    print("等待邮件出现....")
    time.sleep(30)

    print("打开第一封邮件")
    driver.swipe(100,100,1,1,5)# 通过坐标点击第一封邮件
    # self.driver.click("xpath=>//UIAApplication[1]/UIAWindow[1]/UIATableView[2]/UIATableCell[1]")

    print("点击全部下载")
    driver.click(u"id=>全部下载")
    #//UIAApplication[1]/UIAWindow[1]/UIAScrollView[1]/UIAButton[9]
    start = time.time()


    print("等待完成")
    # driver.element_wait(u"id=>完成",120)
    driver.element_gone(u"id=>全部下载",120)

    print('=>记录当前时间，')
    value_time = str(round((time.time() - start), 2))
    print('[登录时延]: %r'  %value_time)

    driver.click(u"id=>完成")
    time.sleep(10)

def test_contant(driver):
    '''联系人同步'''

    print("点击联系人")
    driver.click(u"id=>联系人")
    print("截图")
    BaseImage.screenshot(driver,"testConant")

    print("开始计时")
    start = time.time()

    print("页面加载60秒")
    # 等待两分钟
    timeout = int(round(time.time() * 1000)) + 60 * 1000
    try:
        while (int(round(time.time() * 1000) < timeout)):
            print("=>下拉")
            driver.swipe_down()
            # 这里需要实际情况，是否添加时延
            print("=>截图判断")
            d = BaseImage.screenshot(driver,"testConant")
            if d["result"] and BaseImage.get_pic_txt(d['path']).__contains__("手机联系人同步完成"):
                break
            time.sleep(1)
    except BaseException as msg:
        print(msg)

    print('=>记录当前时间，')
    value_time = str(round((time.time() - start), 2))
    print('[联系人同步时间]: %r'  %value_time)




if __name__ == '__main__':
    print("运行脚本")
    driver = Psam()
    login(driver)
    time.sleep(3)
    # test_contant(driver)
    # time.sleep(4)
    # print("end")
    #
    #




            