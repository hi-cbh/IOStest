#!/usr/bin/python  
# -*- coding: utf-8 -*- 

import pyzmail
import time
from imapclient import IMAPClient


class EmailOperation(object):
    
    def __init__(self, user_name, pwd):
        print("使用imapclient，操作邮件...")
        self.server = IMAPClient('imap.139.com', use_uid=True, ssl=False)
        self.username = user_name
        self.password = pwd
        
    
    def logout(self):
        self.server.logout()
        
    # 删除邮件
    def _del(self, messages):
#         print('del message')
        self.server.delete_messages(messages)
        self.server.expunge()
    
    def _mv(self, message, folder):
        self.server.copy(message, folder)
        time.sleep(1)
        self._del(message)
    
    def _into(self, box):
        # 'INBOX','草稿箱','已发送','已删除','100'
        self.server.select_folder(box)
        
    def _get_uids(self):
        # 获取序列
        uids = self.server.search(['NOT', 'DELETED'])
        return uids
    
    def email_body(self, mss):
        # 获取某序列id的原始信息
        raw_messages = self.server.fetch([mss],['BODY[]','FLAGS'])
#         pprint.pprint(rawMessages)
        # 使用pyzmail，返回主体信息
        message = pyzmail.PyzMessage.factory(raw_messages[mss][b'BODY[]'])
        
        # 如果信息为空，返回None
        if not message:
            return None
        # 获取正文内容
        if message.text_part != None:
            lines = message.text_part.get_payload().decode(message.text_part.charset)
        
        str=''
        # 去除内容中的回车
        for line in lines:
            if line not in ['\n', '\r'] :    
                str+=line

        print(str)
        # body自动
        body = {'subject':message.get_subject(),
                'from': message.get_address('from'),
                'to': message.get_address('to'),
                'mainbody': str
                }
        return body
        
        
    def del_all_message(self, folder):
        '''清空某个文件夹下的所有邮件'''
        self._into(folder)
        
        uids = self._get_uids()
        if len(uids) ==  0 :
            return
        else:
            self._del(uids)
    
    def del_new_message(self, fforlder):
        '''把最近一封新邮件已到目的目录'''
        self._into(fforlder)
        
        uids = self._get_uids()
        
        if len(uids) ==  0 :
            return
        else:
            self._del(uids[-1])
    
    def move_all_message_to_folder(self, fforlder, tforlder):
        '''把maessage/messages 从 ffolder 移动到 tforlder'''
        
        self._into(fforlder)
        
        uids = self._get_uids()
        # 邮件数量为空
        if len(uids) ==  0 :
            print("%s 数量为：0，该操作无效" %fforlder)
            return True
        self._mv(uids, tforlder)
            

    def check_new_message(self):
        '''判断最新一封邮件，是否包含某个字段，显示邮件数量'''
        self._into("INBOX")
        
        uids = self._get_uids()

        print('current INBOX email: %s' %str(len(uids)))

        if len(uids) in [0 ,1]:
            print("不执行，目前邮件数量为：%r" %len(uids))
            return
        
        if self.email_body(uids[-1])['subject'] == 'testReceive':
            self._del(uids[-1])

    
    def delete_newest_mail(self):
        '''删除最新的一封邮件'''
        try:
            is_true = False
            self.server.login(self.username, self.password)    
            self.del_new_message('INBOX')
            is_true = True
        except BaseException as error:
            print(error)
            print("删除邮件可能出现错误")
        finally:
            self.logout()
            return is_true

    def clear_forlder(self, l=[]):
        '''清空邮箱某个文件夹'''
        '''
        sample:
        clearForlder(['100', 'INBOX'])
        '''
        is_true = False
        if len(l) == 0:
            return is_true
        try:
            self.server.login(self.username, self.password)    
            for f in l:
                print("clear Forlder: %s" %f)
                self.del_all_message(f)
                time.sleep(1)
                
            is_true = True
        except BaseException as error:
            print(error)
            print("删除邮件可能出现错误")
        finally:
            self.logout() 
            return is_true
                
    def move_forlder(self, l=[]):
        '''移动邮件
        sample:
            moveForlder(['100', 'INBOX'])
        '''
        is_true = False
        if len(l) == 0:
            return is_true
        try:
            self.server.login(self.username, self.password)    
            self.move_all_message_to_folder(l[0], l[1])
            print("移动邮件成功：%s => %s" %(l[0], l[1]))
            is_true = True
        except BaseException as error:
            print(error)
            print("清空邮箱某个文件夹可能出现错误")
        finally:
            self.logout()
            return is_true
    
    def check_inbox_cnt(self):
        '''获取邮件数量'''
        try:
            is_true = 0
            self.server.login(self.username, self.password) 
            
            self._into("INBOX")
            uids = self._get_uids()
            # 数量为 0
            if len(uids) == 0:
                return 0
            # 判断
            if len(uids) == 100:
                print("100封邮件")
                return 0
            elif len(uids) < 100:
                print('邮件数量少于100封')
                return 0
            else:
                cnt = len(uids) - 100
                print('需要删除邮件数量为：%d' %cnt)
                is_true =  cnt
        except BaseException as error:
            print(error)
            print("删除邮件可能出现错误")
        finally:
            self.logout() 
            return  is_true
    
    def check_inbox(self):
        '''确保收件箱有100封邮件'''
        try:
            is_true = True
            self.server.login(self.username, self.password) 
            
            self._into("INBOX")
            uids = self._get_uids()
            all = len(uids)
            # 数量为 0
            if all == 0:
                return False
            # 判断
            if all == 100:
                print("100封邮件")
                return is_true
            elif all < 100:
                print('邮件数量少于100封')
                return False
            else:
                print('需要删除邮件数量为：%d' %(all - 100))
#                 print(Uids[100:])
                self._del(uids[100:])
                return is_true
        except BaseException as error:
            print(error)
            print("删除邮件可能出现错误")
            is_true = False
        finally:
            self.logout()  
            return is_true


    def seen(self):
        '''将收件箱邮件，标记已读'''
        self.server.login(self.username, self.password)
        self._into("INBOX")
        # 搜索 未读邮件
        typ = self.server.search([u'UNSEEN'])
        # 把邮件改为已读
        for num in typ:
            print(num)
            self.server.set_flags(num,  [u'Seen'])


if __name__ == '__main__':
    eo = EmailOperation("13697485262@139.com","chinasoft123")
#     eo.moveForlder(['INBOX','100' ]) 
#     eo.moveForlder(['100', 'INBOX']) 
#     eo.clearForlder(['已发送','已删除'])
#     eo.checkInbox()
    eo.seen()