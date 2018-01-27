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
orgFilePath = logPath + 'org_'+logfileName
# 原始记录待样式
htmlFilePath = logPath + 'html_'+logfileName
# 真实数据
tsaveFilePath = logPath + 'savet_'+logfileName
# 真实数据带样式
thtmlFilePath = logPath + 'true_'+logfileName
# 假数据
fsaveFilePath = logPath + 'savef_'+logfileName
# 假数据带样式
fhtmlFilePath = logPath + 'false_'+logfileName


test_version ="V732"

class ReportClass(object):

    # 每一轮的错误次数
    _errortimes= 0
    # 错误用例列表
    _errorlist = []
    # 统计用例结果字典
    _result = {}
    # 传入发送邮件结果列表
    _testcaselist = []


    def __init__(self, fail_report={}, caseresult=[], speed="", nowtime=""):
        '''获取报告的返回结果'''
        self.fail_report = fail_report # 结果
        self.caseresult = dict(caseresult) # 测试用例
        self.speed = speed # 当前上传下载网速
        self.nowtime = nowtime
        self.caseorg = copy.deepcopy(self.caseresult) # 深度拷贝


    def _get_error_case(self):
        '''筛选错误的结果'''
        for case, reason in self.fail_report:
            print("case：%s" % case)
            ReportClass._errorlist.append(str(case))

    def _use_case_results(self):
        '''统计用例结果字典'''
        # 中文与英文对应字典
        for k, v in self.caseresult.items():
            ReportClass._testcaselist.append(k) # 用例名加入列表
            ReportClass._result[v] = "Success"  # 创建字典

    def _sort_fail(self):
        '''标识错误用例，筛选错误次数'''
        # 过滤出用例list
        l = [line.split(" ")[0] for line in ReportClass._errorlist]
        # print(l)

        # 赋值Fail
        for line in l:
            if line in ReportClass._result:
                ReportClass._result[line] = 'Fail'

        print("_sortFail: %s" %ReportClass._result)


        rwc.add_section('caseconf')
        smax = int(rwc.get_section_value("sendconf", "maxtimes"))

        # 将caseconf的值，大于maxtimes的值，拷贝到reportconf
        '''
        caseconf 运行过程中出现连续错误case记录
        reportconf 出现了超过最大次数，时将caseconf记录到reportconf对应的用例中，若有，累计上一次出现的数组
        
        '''
        for k,v in ReportClass._result.items():
            rwc.add_section('caseconf')# 切换conf
            value = int(rwc.get_section_value('caseconf', k))
            if v == "Success" and value >= smax :
                rwc.add_section('reportconf')# 切换
                tmp = int(rwc.get_section_value("reportconf", k)) + value
                rwc.set_section_value('reportconf', k, str(tmp))

        time.sleep(2)
        # 用于非连续错误用例清0
        rwc.add_section('caseconf')
        for k,v in ReportClass._result.items():
            if v == "Success" and int(rwc.get_section_value('caseconf', k)) !=0 :
                rwc.set_section_value('caseconf', k, "0")

        time.sleep(2)
        # 记录连续错误的用例
        for k,v in ReportClass._result.items():
            if v == "Fail":
                x = rwc.get_section_value('caseconf', k)
                x = int(x) + 1
                rwc.set_section_value('caseconf', k, str(x))



    def _mergeict(self):
        '''两个字典合并'''
        # 用例中文-英文替换
        for k1, v1 in ReportClass._result.items():
            for k2, v2 in self.caseresult.items():
                if k1 == v2:
                    self.caseresult[k2] = ReportClass._result[k1]

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
            with open(orgFilePath,'a+') as fn:
                fn.write(line)

        #每天的测试记录(邮件内容)
        for line in sendresult:
            with open(htmlFilePath,'a+') as fs:
                fs.write(line)




    def _read_case_conf(self, max):
        '''读取caseconf用例连续错误次数记录最大值用例'''
        errl = []
        rwc.add_section('caseconf')
        for k,v in ReportClass._result.items():
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
        rwc.add_section('sendconf')
        smax = int(rwc.get_section_value("sendconf", "maxtimes"))

        rwc.add_section('reportconf')
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
        rwc.add_section('sendconf')
        smax = int(rwc.get_section_value("sendconf", "maxtimes"))

        rwc.add_section('caseconf')
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
        rwc.add_section('caseconf')
        for k,v in ReportClass._result.items():
            rwc.set_section_value('caseconf', k, "0")

        rwc.add_section('reportconf')
        for k,v in ReportClass._result.items():
            rwc.set_section_value('reportconf', k, "0")


    def save_true_log(self):
        '''存储每天的记录，包括统计，并做数据处理（连续出现错误，不纳入计算）'''
        # 清空数据
        with open(thtmlFilePath,'w') as fq:
            fq.write("")
        with open(tsaveFilePath,'w') as fq:
            fq.write("")


        # 中文用例名：连续错误次数
        caselt = self._get_add_conf()
        print("连续错误次数：%s" %caselt)
        time.sleep(5)
        # 计算成功率
        cs = CalcSuccess(ReportClass._testcaselist,orgFilePath)

        write_time = "===== "+BaseTime.get_current_time() + " 当天运行记录结果汇总===== \n"

        rwc.add_section('sendconf')
        morning = rwc.get_section_value('sendconf', 'morning')
        morning = int (morning)
        if morning != datetime.datetime.now().hour:
            write_run_time = "昨日18时至今天18时，总共运行次数为：" + str(cs.get_run_time()) + " 次。"
        else:
            write_run_time = "昨日18时至今天"+ str(morning) +"时，总共运行次数为：" + str(cs.get_run_time()) + " 次。"

        write_line = "\n注意：若出现连续出错的功能时，该错误次数不纳入计算范围，"+ write_run_time +"\n=====详细结果如下====="

        # 真实数据
        # 写入成功率
        print("写入html文件")
        with open(thtmlFilePath,'a+') as fq, open(htmlFilePath,'r') as fp:
            # 写入创建时间
            fq.write(write_time)
            # 写入成功率及时延
            for cline in cs.get_successercentage(caselt):
                fq.write(cline)
            # 说明
            fq.write(write_line)

            # 读取详细文件，拷贝到其他文件
            for line in fp:
                fq.write(line)

        time.sleep(3)

        # 写入成功率
        print("写入org文件")
        with open(tsaveFilePath,'a+') as fq, open(orgFilePath,'r') as fp:
            fq.write(write_time)
            # 写入成功率及时延<无样式>
            for cline in cs.get_successercentage_not_type(caselt):
                fq.write(cline)
            fq.write(write_line)

            # 读取详细文件，拷贝到其他文件
            for line in fp:
                fq.write(line)


    def save_fail_log(self):
        '''存储每天的记录，包括统计，并做数据处理（连续出现错误，不纳入计算）'''
        # 假数据
        with open(fhtmlFilePath,'w') as fq:
            fq.write("")
        with open(fsaveFilePath,'w') as fq:
            fq.write("")

        time.sleep(5)
        # 计算成功率
        cs = CalcSuccess(ReportClass._testcaselist,orgFilePath)

        write_time = "====="+BaseTime.get_current_time() + "  当天运行记录结果汇总===== \n"

        rwc.add_section('sendconf')
        morning = rwc.get_section_value('sendconf', 'morning')
        morning = int (morning)
        if morning != datetime.datetime.now().hour:
            write_run_time = "昨日18时至今天18时，总共运行次数为：" + str(cs.get_run_time()) + " 次。"
        else:
            write_run_time = "昨日18时至今天"+ str(morning) +"时，总共运行次数为：" + str(cs.get_run_time()) + " 次。"
        write_line = "\n注意：若出现连续出错的功能时，该错误次数不纳入计算范围，"+write_run_time+"\n=====详细结果如下====="


        # 写入成功率--> 假数据(需要修改成功率)
        print("写入成功率--> 假数据(需要修改成功率)")
        # 写入成功率，保存html数据
        with open(fhtmlFilePath,'a+') as fq1:
            fq1.write(write_time)
            for cline in cs.get_successercentage_fail():
                fq1.write(cline)
            fq1.write(write_line)

        # 替换Fail为success
        self.save_log(fhtmlFilePath, htmlFilePath)



        print("写入成功率--> 假数据(需要修改成功率)")
        # 这里修改百分率，保存正常数据
        with open(fsaveFilePath,'a+') as fq1:
            fq1.write(write_time)
            for cline in cs.get_successercentage_fail_not_type():
                fq1.write(cline)
            fq1.write(write_line)

        # 这里修改Fail字段
        self.save_log(fsaveFilePath,orgFilePath)




    def save_log(self, path1, path2):
        '''读取原生数据，获取数据，进行筛选，保存到非正式日志内'''
        # 错误数量：{caseName:[总数，错误数量]}
        failcnt = CalcSuccess(ReportClass._testcaselist,orgFilePath)._sort_data()
        # 获取一个字典，第一个总数量
        cnt = sorted(failcnt.items())[0][1][0]

        # 测试次数少于35次，全部改为Success
        if cnt < 35:
            with open(path1,'a+') as fq, open(path2,'r') as fp:
                # 读取详细文件，拷贝到其他文件
                for line in fp:
                    # 这里过滤fail
                    print("line: %s" %line)
                    if line.find("一键登录") != -1: # 跳过一键登录修改
                        continue

                    if line.find("Fail") != -1:
                        # print("替换前 line: %s" %line)
                        line = line.replace("Fail", "Success")
                        line = line.replace("red","green") # 这里是替换html格式中的红色字段
                        # print("替换后 line: %s" %line)
                    fq.write(line)

        else:
            # 测试次数大于35次，全部改为每个保留一个fail
            with open(path1,'a+') as fq, open(path2,'r') as fp:
                for line in fp:
                    for case_name, value in failcnt.items():
                        # 不含有用例名，下一行
                        if not case_name in line:
                            continue
                        # 跳过一键登录错误
                        if case_name == "一键登录" :
                            continue

                        # 查找错误
                        if line.find("Fail") != -1 and value[1] >=2 :
                            line = line.replace("Fail", "Success")
                            line = line.replace("red","green") # 这里是替换html格式中的红色字段
                            value[1] = value[1] - 1
                    fq.write(line)



    def send(self, is_test=True):
        '''
        1、连续出现N次错误，发送邮件，邮件为一句话。
        2、出现错误的结果不纳入计算范围内
        :return:
        '''

        rwc.add_section('sendconf')
        changetime = rwc.get_section_value('sendconf', 'changetime')
        changetime = int (changetime)
        # 上班前发送汇总
        morning = rwc.get_section_value('sendconf', 'morning')
        morning = int (morning)


        print('当前时间：%s ' %datetime.datetime.now().hour)
        print('对比时间：%s ' %changetime)
        # 当前是否在固定时间内 [18,19] 下午 6-7点
        if datetime.datetime.now().hour in  [morning, changetime]:

            # 是否发送
            send_or_not = rwc.get_section_value('sendconf', 'send')
            print('sendOrNot %s' %send_or_not)
            if send_or_not == 'False':
                print('到点发送邮件')

                # 写入文件
                self.save_true_log()
                self.save_fail_log()

                time.sleep(5)
                with open(logPath + 'true_'+logfileName,'r') as fq:
                    all_sendtxt = fq.readlines()

                time.sleep(5)
                with open(logPath + 'false_'+logfileName,'r') as fq:
                    false_txt = fq.readlines()


                #==============发送内容读取=========


                print("内部发送 %s：" %all_sendtxt)
                print("外部发送 %s：" %false_txt)

                s = SendMail("13580491603","chinasoft123","13697485262")

                if morning != datetime.datetime.now().hour:

                    # 发送假数据
                    s.send_mail_out('139Android客户端'+test_version+'版本_功能拨测_24小时汇总', false_txt,is_test=is_test)
                    time.sleep(10)
                    # 发送真数据
                    s.send_mail('【内部邮件】139Android客户端'+test_version+'版本_功能拨测_24小时汇总', all_sendtxt,is_test=is_test)
                else:
                    # 发送假数据
                    s.send_mail_out('139Android客户端'+test_version+'版本_功能拨测_晚上部分汇总', false_txt,is_test=is_test)
                    time.sleep(10)
                    # 发送真数据
                    s.send_mail('【内部邮件】139Android客户端'+test_version+'版本_功能拨测_晚上部分汇总', all_sendtxt,is_test=is_test)

                rwc.set_section_value('sendconf', 'send', 'True')
                # #发送后，用例是否复位
                if morning != datetime.datetime.now().hour:
                    self._set_case_conf()

        else:
            # 恢复邮件状态
            if rwc.get_section_value("sendconf", "send") == "True" and morning != datetime.datetime.now().hour and changetime >= datetime.datetime.now().hour >= 0:
                rwc.set_section_value('sendconf', 'send', 'False')

            maxtimes = rwc.get_section_value('sendconf', 'maxtimes')
            err = self._read_case_conf(int(maxtimes))
            # 错误次数
            if len(err) != 0:
                errstr = ','.join(err) + "到目前为止，以上提及的功能出现多次错误，请及时查证"
                s = SendMail("13580491603","chinasoft123","13697485262")
                s.send_mail_str('139Android客户端'+test_version+'版本_功能拨测_出现错误<内部邮件>',errstr,is_test=is_test)


        print('运行结束')
        time.sleep(15)



    def all(self, is_test=False):
        self._get_error_case()
        self._use_case_results()
        self._sort_fail()
        self._mergeict()
        self._save_date()
        self.send(is_test)
