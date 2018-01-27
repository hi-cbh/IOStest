# urs/bin/python
# encoding:utf-8

import time
import datetime
from src.readwriteconf.rwconf import ReadWriteConfFile
class BaseTime(object):
    
    def current_time(self):
        '''用于写入文件，或文件格式'''
        return time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()) 
     
    def get_current_time(self):
        '''用于写入数据库'''    
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 


    def get_time_pro(self):
        '''写入产品ID'''
        return time.strftime("%m%d", time.localtime())

    def get_date_hour(self):
        '''获取固定的文件名'''
        '''
        # 可能这里出错，导致Jenkins运行失败
        #
        # i = datetime.datetime.now()
        # print ("当前的日期和时间是 %s" % i)
        # print ("ISO格式的日期和时间是 %s" % i.isoformat() )
        # print ("当前的年份是 %s" %i.year)
        # print ("当前的月份是 %s" %i.month)
        # print ("当前的日期是  %s" %i.day)
        # print ("dd/mm/yyyy 格式是  %s/%s/%s" % (i.day, i.month, i.year) )
        # print ("当前小时是 %s" %i.hour)
        # print ("当前分钟是 %s" %i.minute)
        # print ("当前秒是  %s" %i.second)
        '''
        ReadWriteConfFile.add_section('sendconf')
        changetime = ReadWriteConfFile.get_section_value('sendconf', 'changetime' )
        changetime = int (changetime)

        i = datetime.datetime.now()

        # 添加是否为发送状态
        ReadWriteConfFile.add_section('sendconf')
        send_status = ReadWriteConfFile.get_section_value('sendconf', 'send' )

        d = i.day
        if changetime >= i.hour >= 0 and send_status == "False":
            d = d
        else:
            d = d + 1


        name = str(i.year) +str(i.month) + str(d)
        print(name)
        return name

BaseTime = BaseTime()

if __name__ == "__main__":
    print(BaseTime.get_date_hour())
