
from src.readwriteconf.initData import InitData


class SaveData(object):

    _path = InitData().get_sys_path()["savepath"] + "/logs/tmp.log"


    def save(self, msg=None):
        '''写入的数据格式与 runTest的格式一致（中文名）'''
        if msg == None:
            print('不保存数据')
            return

        with open(SaveData._path,'a+') as fn:
            fn.write(msg+'\n')

    def get_value(self):
        '''主要不错数据格式：中文名(case固定):时延'''
        # 读取文件
        with open(SaveData._path, 'r') as fn:
            txt = fn.readlines()

        # 清空数据
        with open(SaveData._path, 'w') as fn:
            fn.write("")

        txt2 = []
        for line in txt:
            key = line.split(":")[0]
            value = line.split(":")[1][:-1]
            # print(key, value)
            txt2.append((key, value))
        # 返回字典格式

        return dict(txt2)


save = SaveData()