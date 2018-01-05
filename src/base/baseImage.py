# urs/bin/python
# encoding:utf-8


try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract


import os, time
from src.base.baseTime import BaseTime

base_dir = str(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
local = "/var/appiumRunLogIos"+ "/pics/"

class BaseImage(object):
    def screenshot(self, driver, pic_name):
        '''截屏，保存在根目录下的pics文件夹下，已时间戳命名'''
        try:
            print("运行截图")
            filename = pic_name + "-" + BaseTime.current_time() + ".png"
            file_path = local + filename
            driver.screenshot(file_path)
            result = True
        except BaseException as e:
            # print(e)
            print("截屏失败！！！")
            result = False
        finally:
            # 返回文件名及结果
            return {"path": file_path, "result":result}


    def get_pic_txt(self, pic_path):
        # 保存临时文件
        tmppic = '/var/appiumRunLogIos/pics/tmp.png'
        # 语言包位置
        tessdata_dir_config = '--tessdata-dir "/usr/local/Cellar/tesseract/3.05.01/share/tessdata/"'
        # 截图
        loc = {"x":0, "y":0} # 位置
        size = {"width":620, 'height':40} # 截图大小
        # 打开图片
        img = Image.open(pic_path)
        # 截图区域
        box = (loc['x'], loc['y'], float(loc['x']) + float(size['width']), float(loc['y']) + float(size['height']))
        # 裁剪出验证码图片
        img = img.crop(box)
        # 保存验证码图片
        img.save(tmppic)

        # lang 指定中文简体
        text = pytesseract.image_to_string(Image.open(tmppic), lang='chi_sim',config=tessdata_dir_config)
        print("图片文字打印开始。")
        print("图片中的文字为：%s"%text)
        print("图片文字打印结束。")
        return text






BaseImage = BaseImage()


if __name__ == "__main__":

    BaseImage.screenshot()