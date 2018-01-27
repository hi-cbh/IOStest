# urs/bin/python
# encoding:utf-8

import os
import configparser as cparser
from src.readwriteconf.initData import InitData

class ReadWriteConfFile:
    file_path = InitData().get_sys_path()['rwconf']
    print(file_path)

    @staticmethod
    def get_config_parser():
        cf=cparser.ConfigParser()
        cf.read(ReadWriteConfFile.file_path)
        return cf

    @staticmethod
    def write_config_parser(cf):
        f=open(ReadWriteConfFile.file_path,"w")
        cf.write(f)
        f.close()

    @staticmethod
    def get_section_value(section, key):
        cf=ReadWriteConfFile.get_config_parser()
        return cf.get(section, key)

    @staticmethod
    def add_section(section):
        cf=ReadWriteConfFile.get_config_parser()
        all_sections=cf.sections()
        if section in all_sections:
            return
        else:
            cf.add_section(section)
            ReadWriteConfFile.write_config_parser(cf)

    @staticmethod
    def set_section_value(section, key, value):
        cf=ReadWriteConfFile.get_config_parser()
        cf.set(section, key, value)
        ReadWriteConfFile.write_config_parser(cf)


if __name__ == '__main__':
    ReadWriteConfFile.add_section('sendconf')
    ReadWriteConfFile.set_section_value('sendconf', 'error', '0')
    x=ReadWriteConfFile.get_section_value('sendconf', 'error')
    print(x)