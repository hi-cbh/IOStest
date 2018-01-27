from src.mail.sendEmailSmtp import  SendMail
import time, datetime
import copy
from src.base.baseTime import BaseTime
from src.readwriteconf.rwconf import ReadWriteConfFile as rwc
from src.readwriteconf.initData import InitData
from src.readwriteconf.saveData import save
from src.readwriteconf.calcSucPer import CalcSuccess
from collections import Counter

logPath = InitData().get_sys_path()["savepath"] + "/logs/"
logfileName= BaseTime.get_date_hour() + '.log'

# 原始记录
org_file_path = logPath + 'org_' + logfileName
# 原始记录待样式
html_file_path = logPath + 'html_' + logfileName
# 真实数据
tsave_file_path = logPath + 'savet_' + logfileName
# 真实数据带样式
thtml_file_path = logPath + 'true_' + logfileName
# 假数据
fsave_file_path = logPath + 'savef_' + logfileName
# 假数据带样式
fhtml_file_path = logPath + 'false_' + logfileName


class ReportClass(object):

    # 每一轮的错误次数
    error_times= 0
    # 错误用例列表
    error_list = []
    # 统计用例结果字典
    result = {}
    # 传入发送邮件结果列表
    testcase_list = []


    def __init__(self, fail_report={}, caseresult=[], speed="", nowtime=""):
        '''获取报告的返回结果'''
        self.fail_report = fail_report # 结果
        self.caseresult = dict(caseresult) # 测试用例
        self.speed = speed # 当前上传下载网速
        self.nowtime = nowtime
        self.caseorg = copy.deepcopy(self.caseresult) # 深度拷贝


    def _get_error_case(self):
        '''筛选错误的结果'''
        for case, value in self.fail_report:
            print("case：%s" % case)
            ReportClass.error_list.append(str(case))

    def _use_case_results(self):
        '''统计用例结果字典'''
        # 中文与英文对应字典
        for k, v in self.caseresult.items():
            ReportClass.testcase_list.append(k) # 用例名加入列表
            ReportClass.result[v] = "Success"  # 创建字典

    def _sort_fail(self):
        '''标识错误用例，筛选错误次数'''

        # 过滤出用例list
        l = [line.split(" ")[0] for line in ReportClass.error_list]
        # print(l)

        # 赋值Fail
        for line in l:
            if line in ReportClass.result:
                ReportClass.result[line] = 'Fail'


        print("_sortFail: %s" % ReportClass.result)


        rwc.addsection('caseconf')
        smax = int(rwc.get_section_value("sendconf", "maxtimes"))

        # 将caseconf的值，大于maxtimes的值，拷贝到reportconf
        '''
        caseconf 运行过程中出现连续错误case记录
        reportconf 出现了超过最大次数，时将caseconf记录到reportconf对应的用例中，若有，累计上一次出现的数组
        
        '''
        for k,v in ReportClass.result.items():
            rwc.addsection('caseconf')# 切换conf
            value = int(rwc.get_section_value('caseconf', k))
            if v == "Success" and value >= smax :
                rwc.addsection('reportconf')# 切换
                tmp = int(rwc.get_section_value("reportconf", k)) + value
                rwc.set_section_value('reportconf', k, str(tmp))

        time.sleep(2)
        # 用于非连续错误用例清0
        rwc.addsection('caseconf')
        for k,v in ReportClass.result.items():
            if v == "Success" and int(rwc.get_section_value('caseconf', k)) !=0 :
                rwc.set_section_value('caseconf', k, "0")

        time.sleep(2)
        # 记录连续错误的用例
        for k,v in ReportClass.result.items():
            if v == "Fail":
                x = rwc.get_section_value('caseconf', k)
                x = int(x) + 1
                rwc.set_section_value('caseconf', k, str(x))



    def _mergeict(self):
        '''两个字典合并'''
        # 用例中文-英文替换
        for k1, v1 in ReportClass.result.items():
            for k2, v2 in self.caseresult.items():
                if k1 == v2:
                    self.caseresult[k2] = ReportClass.result[k1]

    def _save_date(self):
        '''保存每一轮的数据，分为带样式和无样式'''
        # 获取用例对应的时延
        demotime=save.get_value()
        print("时延：%s" %demotime)

        resulttxt = [] # 写入日志
        resulttxt.append('\n'+"====="+self.nowtime +"====="+'\n')
        resulttxt.append(self.speed +'\n')

        sendresult = [] # 邮件发送正文
        sendresult.append('\n'+"====="+self.nowtime +"====="+'\n')
        sendresult.append(self.speed+'\n')

        # 写入文件，并添加发送邮件格式
        for case, reason in self.caseresult.items():
            # 含有时延的用例
            if case in demotime:
                resulttxt.append('case：%s , 时延：%s, result：%s \n' %(case,demotime[case], reason ))
                if reason == 'Fail':
                    # 用例错误
                    sendresult.append('case：<font size="3" color="blue"> %s </font> ,result：<font size="4" color="red"> %s </font>\n' %(case, reason) )
                else:
                    # 用例Success
                    sendresult.append('case：<font size="3" color="blue"> %s </font> , 时延：%s,  result：<font size="3" color="green"> %s </font>\n' %(case,demotime[case], reason) )
            # 不含时延的用例
            else:
                resulttxt.append('case：%s , result：%s \n' %(case, reason))
                if reason == 'Fail':
                    # 用例错误
                    sendresult.append('case：<font size="3" color="blue"> %s </font> , result：<font size="4" color="red"> %s </font>\n' %(case, reason) )
                else:
                    # 用例success
                    sendresult.append('case：<font size="3" color="blue"> %s </font> , result：<font size="3" color="green"> %s </font>\n' %(case, reason) )


        #每天的测试记录
        for line in resulttxt:
            with open(org_file_path, 'a+') as fn:
                fn.write(line)

        #每天的测试记录(邮件内容)
        for line in sendresult:
            with open(html_file_path, 'a+') as fs:
                fs.write(line)

    def _read_case_conf(self, max):
        '''读取caseconf用例连续错误次数记录最大值用例'''
        errl = []
        rwc.addsection('caseconf')
        for k,v in ReportClass.result.items():
            tmp = int(rwc.get_section_value('caseconf', k))
            if tmp >= max and tmp % max == 0: # 最大值的倍数才加入列表
                errl.append(k)

        tmpl = []
        # 筛选出用例名称
        for line in errl:
            # print("line: %s" %line)
            for k, v in self.caseorg.items():
                if line == v:
                    tmpl.append(k)


        # print("_readCaseConf2: %s" %tmpl)

        return tmpl

    def _get_report_conf(self):
        '''返回：{用例：连续错误次数}，读取reportconf'''
        # print("self.caseorg: %s" %self.caseorg)
        errl = {}
        rwc.addsection('sendconf')
        smax = int(rwc.get_section_value("sendconf", "maxtimes"))

        rwc.addsection('reportconf')
        for k,v in self.caseorg.items():
            tmpvalue = int(rwc.get_section_value('reportconf', v))
            if tmpvalue>=smax:
                errl[k] = tmpvalue

        # print("_getReportConf: %s" %errl)

        return errl


    def _get_case_conf(self):
        '''返回：{用例：连续错误次数}，读取caseconf'''
        # print("self.caseorg: %s" %self.caseorg)
        errl = {}
        rwc.addsection('sendconf')
        smax = int(rwc.get_section_value("sendconf", "maxtimes"))

        rwc.addsection('caseconf')
        for k,v in self.caseorg.items():
            tmpvalue = int(rwc.get_section_value('caseconf', v))
            if tmpvalue>=smax:
                errl[k] = tmpvalue

        # print("_getCaseConf: %s" %errl)

        return errl

    def _get_add_conf(self):
        '''读取caseconf与reportconf两个的和，两个字典相加'''
        return dict(Counter(self._get_case_conf()) + Counter(self._get_report_conf()))


    def _set_case_conf(self):
        '''各个用例复位'''
        rwc.addsection('caseconf')
        for k,v in ReportClass.result.items():
            rwc.set_section_value('caseconf', k, "0")

        rwc.addsection('reportconf')
        for k,v in ReportClass.result.items():
            rwc.set_section_value('reportconf', k, "0")


    def save_true_fail_log(self):
        '''存储每天的记录，包括统计，并做数据处理（连续出现错误，不纳入计算）'''
        # 清空数据
        with open(thtml_file_path, 'w') as fq:
            fq.write("")
        with open(tsave_file_path, 'w') as fq:
            fq.write("")
        # 假数据
        with open(fhtml_file_path, 'w') as fq:
            fq.write("")
        with open(fsave_file_path, 'w') as fq:
            fq.write("")

        # 中文用例名：连续错误次数
        caselt = self._get_add_conf()
        print("连续错误次数：%s" %caselt)
        time.sleep(5)
        # 计算成功率
        cs = CalcSuccess(ReportClass.testcase_list, org_file_path)

        write_time = "====="+BaseTime.get_current_time() + "  当天运行记录结果汇总===== \n"
        write_line = "\n注意：若出现连续出错的功能时，该错误次数不纳入计算范围 \n=====详细结果如下====="

        # 真实数据
        # 写入成功率
        print("写入html文件")
        with open(thtml_file_path, 'a+') as fq, open(html_file_path, 'r') as fp:
            # 写入创建时间
            fq.write(write_time)
            # 写入成功率及时延
            for cline in cs.get_success_rate(caselt):
                fq.write(cline)
            # 说明
            fq.write(write_line)

            # 读取详细文件，拷贝到其他文件
            for line in fp:
                fq.write(line)

        time.sleep(3)

        # 写入成功率
        print("写入org文件")
        with open(tsave_file_path, 'a+') as fq, open(org_file_path, 'r') as fp:
            fq.write(write_time)
            # 写入成功率及时延<无样式>
            for cline in cs.get_success_rate_not_type(caselt):
                fq.write(cline)
            fq.write(write_line)

            # 读取详细文件，拷贝到其他文件
            for line in fp:
                fq.write(line)


        # 写入成功率--> 假数据(需要修改成功率)
        print("写入成功率--> 假数据(需要修改成功率)")
        with open(fhtml_file_path, 'a+') as fq, open(html_file_path, 'r') as fp:
            fq.write(write_time)
            for cline in cs.get_fail_date_html(caselt):
                fq.write(cline)
            fq.write(write_line)

            # 错误数量：{caseName:[总数，错误数量]}
            failcnt = cs._sort_data()
            # 获取一个字典，第一个总数量
            cnt = sorted(failcnt.items())[0][1][0]

            '''
            测试用例总数35为分界点，
            低于35，全部用例错误的标为success
            高于35，各个用例数量，最多只显示一个错误
            '''
            if cnt < 35:

                # 读取详细文件，拷贝到其他文件
                for line in fp:
                    # 这里过滤fail
                    if line.find("Fail") != -1:
                        line = line.replace("Fail", "Success")
                        line = line.replace("red","green")
                    fq.write(line)
            else:
                # 读取详细文件，拷贝到其他文件
                for line in fp:
                    for case, value in failcnt.items():
                        if case in line and line.find("Fail") != -1 and value[1] >=2 :
                            line = line.replace("Fail", "Success")
                            line = line.replace("red","green")
                            value[1] = value[1] - 1
                    fq.write(line)

        print("写入成功率--> 假数据(需要修改成功率)")
        with open(fsave_file_path, 'a+') as fq, open(org_file_path, 'r') as fp:
            fq.write(write_time)
            for cline in cs.get_fail_data(caselt):
                fq.write(cline)
            fq.write(write_line)

            # 错误数量：{caseName:[总数，错误数量]}
            failcnt = cs._sort_data()
            # 获取一个字典，第一个总数量
            cnt = sorted(failcnt.items())[0][1][0]
            print("总数量：%s" %cnt)
            if cnt < 35:

                # 读取详细文件，拷贝到其他文件
                for line in fp:
                    # 这里过滤fail
                    print("line: %s" %line)
                    if line.find("Fail") != -1:
                        # print("替换前 line: %s" %line)
                        line = line.replace("Fail", "Success")
                        # print("替换后 line: %s" %line)
                    fq.write(line)
            else:
                # 读取详细文件，拷贝到其他文件
                for line in fp:
                    for case, value in failcnt.items():
                        if case in line and line.find("Fail") != -1 and value[1] >=2 :
                            line = line.replace("Fail", "Success")
                            value[1] = value[1] - 1
                    fq.write(line)




    def send(self):
        '''
        1、连续出现N次错误，发送邮件，邮件为一句话。
        2、出现错误的结果不纳入计算范围内
        :return:
        '''

        rwc.addsection('sendconf')
        changetime = rwc.get_section_value('sendconf', 'changetime')
        changetime = int (changetime)


        print('当前时间：%s ' %datetime.datetime.now().hour)
        print('对比时间：%s ' %changetime)
        # 当前是否在固定时间内 [18,19] 下午 6-7点
        if datetime.datetime.now().hour in  [changetime]:
        # if datetime.datetime.now().hour in  [14,15]:

            # 是否发送
            send_or_not = rwc.get_section_value('sendconf', 'send')
            print('sendOrNot %s' %send_or_not)
            if send_or_not == 'False':
                print('到点发送邮件')

                # 读取
                self.save_true_fail_log()

                time.sleep(5)
                with open(logPath + 'true_'+logfileName,'r') as fq:
                    all_send_txt = fq.readlines()

                time.sleep(5)
                with open(logPath + 'false_'+logfileName,'r') as fq:
                    false_txt = fq.readlines()


                #==============发送内容读取=========


                print("预备发送 %s：" %all_send_txt)
                print("外部发送 %s：" %false_txt)

                s = SendMail("13580491603","chinasoft123","13697485262")
                # 发送假数据
                s.send_mail_man('139Ios客户端V318版本_功能拨测_汇总<发给移动>',false_txt,is_test=False)
                time.sleep(10)
                # 发送真数据
                s.send_mail_man('139Ios客户端V318版本_功能拨测_汇总<内部邮件>',all_send_txt,is_test=False)
                rwc.set_section_value('sendconf', 'send', 'True')
                # #发送后，用例是否复位
                self._set_case_conf()

        else:
            if rwc.get_section_value("sendconf", "send") == "True":
                rwc.set_section_value('sendconf', 'send', 'False')

            maxtimes = rwc.get_section_value('sendconf', 'maxtimes')
            err = self._read_case_conf(int(maxtimes))
            # 错误次数
            if len(err) != 0:
                errstr = ','.join(err) + "到目前为止，以上提及的功能出现多次错误，请及时查证"
                print("错误邮件：" + errstr)
                s = SendMail("13580491603","chinasoft123","13697485262")
                s.send_mail_man_str('139Ios客户端V318版本_功能拨测_出现错误<内部邮件>',errstr,is_test=False)


        print('运行结束')
        time.sleep(15)



    def all(self):
        self._get_error_case()
        self._use_case_results()
        self._sort_fail()
        self._mergeict()
        self._save_date()
        self.send()



if __name__ == "__main__":
    d = {'testCase01': 'Success', 'testCase02': 'Success', 'testCase03': 'Success', 'testCase04': 'Success'}
    l = ['testCase01 (__main__.MyTest)', 'testCase04 (__main__.MyTest2)']

    # 过滤出用例list
    l = [line.split(" ")[0] for line in l]
    print(l)

    # 赋值Fail
    for line in l:
        if line in d:
            d[line] = 'Fail'



    print("_sortFail: %s" % d)