# urs/bin/python
# encoding:utf-8

import os
import configparser as cparser


file_path = str(os.path.dirname(os.path.dirname(__file__))) + "/user_db.ini"

cf = cparser.ConfigParser()
cf.read(file_path)

class InitData():

    def get_users(self):

        return dict(cf.items("users"))

    def get_sql(self):
        return dict(cf.items("mysqlconf"))


    def get_file(self):
        # print(cf.items("userconf"))
        return dict(cf.items("userconf"))


    def get_sys_path(self):
        return dict(cf.items("sysconf"))

if __name__ == "__main__":
    print(InitData().get_file())
    print(InitData().get_sys_path())
