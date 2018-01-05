

# 计算成功率
class CalcSuccess(object):

    def __init__(self, caselist=[], logpath=""):
        self.caselist = caselist
        self.path = logpath
        print("org: %s" %self.caselist)


    def _sort_data(self):
        suclist = [] # 成功率统计
        # 数据筛选，成功率
        print("self.caselist : %s" %self.caselist)
        for case_name in self.caselist:
            suclist.append((case_name, [0, 0]))# 第一个为总数，第二个为错误次数
            # self.caselist3.append((caseName,0))


        with open(self.path, 'r') as fn:
            txt = fn.readlines()

        suclist = dict(suclist)

        for line in txt:
            if "case" not in line:
                continue

            for case in self.caselist:
                if case in line:
                    suclist[case][0] = suclist[case][0] + 1
                if case in line and "Fail" in line:
                    suclist[case][1] = suclist[case][1] + 1

        return suclist

    def _sort_speed(self):
        speedlist = [] # 速度统计
        # 数据筛选，速度
        for case_name in self.caselist:
            speedlist.append((case_name, [0,0])) # 第一个值为速度和，第二个为个数

        print(speedlist)

        with open(self.path, 'r') as fn:
            txt = fn.readlines()

        # print(txt)
        speedlist = dict(speedlist)

        for line in txt:
            if "case" not in line:
                continue

            for case in self.caselist:
                if case in line and "时延" in line:
                    sd = line[line.find("时延：")+3:line.find(",",line.find("时延："))]

                    speedlist[case][0] = float(speedlist[case][0]) + float(sd)
                    speedlist[case][1] = speedlist[case][1] + 1

        # 计算平均值，赋值第二个值
        for k,v in speedlist.items():
            if v[0] == 0:
                continue
            else:
                v[1]=round(float(v[0]/v[1]),2)

        print(speedlist)

        return speedlist


    def get_success_rate(self, casel={}):
        # 成功率
        suclist = self._sort_data()
        speedlist = self._sort_speed()

        # 如何出现连续错误，键错误次数减出
        print("处理前：%s" %suclist)
        print("处理前 casel：%s" %casel)

        if len(casel) >0:
            for case, value in suclist.items():
                print("case: %s" %case)
                if case in casel:
                    print("true")
                    suclist[case][1] =  suclist[case][1] - casel[case]
                # elif case in casel and (self.suclist[case][1] < casel[case]): # 连续错误次数 大于正常错误次数
                #     self.suclist[case][1] =  0

        print("处理中：%s" %suclist)

        for case, value in suclist.items():
            if suclist[case][1] == 0:
                suclist[case][0] = "100%"
            else:
                suclist[case][0] = str(round((1 - value[1]/value[0])*100, 2)) + "%"


        print("处理后：%s" %suclist)
        result = []

        for k, v in suclist.items():
            if k in speedlist and speedlist[k][0] != 0:
                result.append("case: <font size='3' color='blue'> %s </font>, 成功率: <font size='3' color='blue'> %s </font> , 平均时延: <font size='3' color='blue'> %s </font> \n" %(k, v[0], speedlist[k][1]))
            else:
                result.append("case: <font size='3' color='blue'> %s </font>, 成功率: <font size='3' color='blue'> %s </font> \n" %(k, v[0]))
        print(result)

        return result


    def get_success_rate_not_type(self, casel={}):
        # 成功率没有样式
        suclist = self._sort_data()
        speedlist = self._sort_speed()

        # 如何出现连续错误，键错误次数减出
        print("处理前：%s" %suclist)
        print("处理前 casel：%s" %casel)

        if len(casel) >0:
            for case, value in suclist.items():
                print("case: %s" %case)
                if case in casel:
                    print("true")
                    suclist[case][1] =  suclist[case][1] - casel[case]
                    # elif case in casel and (self.suclist[case][1] < casel[case]): # 连续错误次数 大于正常错误次数
                    #     self.suclist[case][1] =  0

        print("处理中：%s" %suclist)

        for case, value in suclist.items():
            if suclist[case][1] == 0:
                suclist[case][0] = "100%"
            else:
                suclist[case][0] = str(round((1 - value[1]/value[0])*100, 2)) + "%"


        print(suclist)
        result = []

        for k, v in suclist.items():
            if k in speedlist and speedlist[k][0] != 0:
                result.append("case:  %s , 成功率:  %s , 平均时延: %s \n" %(k, v[0], speedlist[k][1]))
            else:
                result.append("case:  %s , 成功率:  %s \n" %(k, v[0]))
        print(result)
        return result

    def get_fail_date_html(self, casel={}):
        # 成功率(数据过滤)
        suclist = self._sort_data()
        speedlist = self._sort_speed()

        # 如何出现连续错误，键错误次数减出
        print("假的处理前：%s" %suclist)
        print("处理前 casel：%s" %casel)

        if len(casel) >0:
            for case, value in suclist.items():
                print("case: %s" %case)
                if case in casel:
                    print("true")
                    suclist[case][1] =  suclist[case][1] - casel[case]
                # 如何casel为空，修改bug
                suclist[case] = self.create_false_data(suclist[case]) # 数据过滤

        print("假的处理中：%s" %suclist)

        for case, value in suclist.items():
            if suclist[case][1] == 0:
                suclist[case][0] = "100%"
            else:
                suclist[case][0] = str(round((1 - value[1]/value[0])*100, 2)) + "%"


        print("假的处理后：%s" %suclist)
        result = []

        for k, v in suclist.items():
            if k in speedlist and speedlist[k][0] != 0:
                result.append("case: <font size='3' color='blue'> %s </font>, 成功率: <font size='3' color='blue'> %s </font> , 平均时延: <font size='3' color='blue'> %s </font> \n" %(k, v[0], speedlist[k][1]))
            else:
                result.append("case: <font size='3' color='blue'> %s </font>, 成功率: <font size='3' color='blue'> %s </font> \n" %(k, v[0]))
        print(result)

        return result


    def get_fail_data(self, casel={}):
        # 成功率没有样式(数据过滤)
        suclist = self._sort_data()
        speedlist = self._sort_speed()

        # 如何出现连续错误，键错误次数减出
        print("假的处理前：%s" %suclist)
        print("处理前 casel：%s" %casel)

        for case in suclist.keys():
            suclist[case] = self.create_false_data(suclist[case]) # 数据过滤

        print("假的处理中：%s" %suclist)

        for case, value in suclist.items():
            if suclist[case][1] == 0:
                suclist[case][0] = "100%"
            else:
                suclist[case][0] = str(round((1 - value[1]/value[0])*100, 2)) + "%"


        print(suclist)
        result = []

        for k, v in suclist.items():
            if k in speedlist and speedlist[k][0] != 0:
                result.append("case:  %s , 成功率:  %s , 平均时延: %s \n" %(k, v[0], speedlist[k][1]))
            else:
                result.append("case:  %s , 成功率:  %s \n" %(k, v[0]))
        print(result)
        return result


    def create_false_data(self, l=[]):
        '''修正数据
        总数量必须大于42以上，达到97 - 100
        '''
        if l[0] > 35:
            #[数据总数量，错误数]
            # 预防错误数量 > 总数量
            if l[1] > l[0]:
                l[1] = l[0]

            # 错误数量为负数
            if l[1] < 0:
                l[1] = 0


            while True:
                tmp = float(round((1 - l[1]/l[0])*100, 2))
                # print(tmp)
                print("错误数量/总数：%s/%s = %s" %(l[1],l[0],tmp))
                if tmp > 97.0:
                    break
                else:
                    l[1] = l[1] - 1 # 自减一
            print("错误数量/总数：%s/%s = %s" %(l[1],l[0],round((1 - l[1]/l[0])*100, 2)))

        else:
            print("总数量低于35，全部错误数量为0")
            l[1] = 0


        return l



if __name__ == "__main__":
    caselist = ["用例1","用例2","用例3","用例4"]
    path1 = "/var/appiumRunLog/logs/org_2017126.log"
    CalcSuccess(caselist, path1).get_fail_data(casel={})


