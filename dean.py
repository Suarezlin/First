__author__ = 'Suarezlin'
import requests
import re
from bs4 import BeautifulSoup
import prettytable
import sys

class DEAN:
    def __init__(self):
        self.login = 'https://cas.xjtu.edu.cn/login'
        self.posturl = 'http://ssfw.xjtu.edu.cn/index.portal'
        self.classurl = 'http://ssfw.xjtu.edu.cn/index.portal?.pn=p1142_p1145_p1542'
        self.gradeurl = 'http://ssfw.xjtu.edu.cn/index.portal?.pn=p1142_p1144_p1156'
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
            'Host': 'ssfw.xjtu.edu.cn',
            'Referer': 'http://ssfw.xjtu.edu.cn/',
            'Connection': 'keep-alive',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1'
        }
        self.session = requests.session()

    def getLt(self):
        request = self.session.get(self.posturl)
        request = request.text
        str = 'name="lt" value="(.*?)"'
        pattern = re.compile(str, re.S)
        lt = re.findall(pattern, request)
        return lt[0]

    def logIn(self):
        print('请输入NetID：')
        self.username = input()
        print('请输入密码：')
        self.password = input()
        print('登录中请稍候')
        str = '登录'
        str = str.encode('utf-8')
        postdata = {
            'username': self.username,
            'password': self.password,
            'code': '',
            'lt': self.getLt(),
            'execution': 'e1s1',
            '_eventId': 'submit',
            'submit': str
        }
        self.session.post(self.login, postdata)
        r = self.session.get(self.posturl)
        soup = BeautifulSoup(r.text, 'html.parser').find('meta').get('content')[6:]
        self.session.get(soup)

    def ins(self, a):
        if len(a) < 4:
            number = []
            for it in a:
                search = '~'
                start = 0
                index = it.find(search, start)
                if index > 0:
                    number.append(it[index - 1])
            if '1' not in number:
                a.insert(0, '')
            if '3' not in number:
                a.insert(1, '')
            if '5' not in number:
                a.insert(2, '')
            if '7' not in number:
                a.insert(3, '')
    def getGI(self):
        s=self.session.get(self.posturl)
        text=s.text
        pattern=re.compile('学号.*?"span_unedit">(.*?)</span>.*?姓名.*?"span_unedit">(.*?)</span>.*?性别.*?"span_unedit">(.*?)</span>.*?出生日期.*?"span_unedit">(.*?)</span>.*?民族.*?"span_unedit">(.*?)</span>.*?班级名称.*?"span_unedit">(.*?)</span>.*?学院.*?"span_unedit">(.*?)</span>',re.S)
        item=re.findall(pattern,text)
        item=item[0]
        x = prettytable.PrettyTable(["学号",item[0]])
        x.align["学号"] = "l"
        x.padding_width = 1
        x.add_row(["姓名",item[1]])
        x.add_row(["性别",item[2]])
        x.add_row(["出生日期",item[3]])
        x.add_row(["民族",item[4]])
        x.add_row(["班级",item[5]])
        x.add_row(["学院",item[6]])
        print(x)

    def getClassTable(self):
        r = self.session.get(self.classurl)
        pattern = re.compile('class="fcSpanDiv"></div></div>(.*?)</td><td colspan=1 rowspan=".*?">', re.S)
        trs = re.findall(pattern, r.text)
        replaceBR = re.compile('<br>')
        replaceNBSP = re.compile('&nbsp;')
        text = []
        classinfo = []
        for it in trs:
            text.append(re.sub(replaceBR, "\n", it))
        for it in text:
            classinfo.append(re.sub(replaceNBSP, " ", it))
        i = 0
        mon = []
        tue = []
        wen = []
        thr = []
        fry = []
        for it in classinfo:
            if '周一' in it:
                mon.append(it)
            elif '周二' in it:
                tue.append(it)
            elif '周三' in it:
                wen.append(it)
            elif '周四' in it:
                thr.append(it)
            elif '周五' in it:
                fry.append(it)
        self.ins(mon)
        self.ins(tue)
        self.ins(wen)
        self.ins(thr)
        self.ins(fry)
        x = prettytable.PrettyTable(["周一", "周二", "周三", "周四", "周五"])
        x.align["周一"] = "l"
        x.padding_width = 1
        x.add_row([mon[0], tue[0], wen[0], thr[0], fry[0]])
        x.add_row([mon[1], tue[1], wen[1], thr[1], fry[1]])
        x.add_row([mon[2], tue[2], wen[2], thr[2], fry[2]])
        x.add_row([mon[3], tue[3], wen[3], thr[3], fry[3]])
        print(x)

    def getGrade(self):
        r = self.session.get(self.gradeurl)
        text = r.text
        # print(text)
        pattern = re.compile(
            '<td class="">(.*?)</td>.*?<td class="">(.*?)</td>.*?<td class="">(.*?)</td>.*?<td class="">(.*?)</td>.*?<td class="">(.*?)</td>.*?<td class="">.*?">(.*?)</a>.*?<td class="">(.*?)</td>.*?<td class="">(.*?)</td>.*?<td class="">(.*?)</td>.*?<td class="">(.*?)</td>',
            re.S)
        s = re.findall(pattern, text)
        x = prettytable.PrettyTable(["学年学期", "课程代码", "课程名称", "课程类别", "考试性质", "成绩", "学分", "特殊原因", "修读性质", "是否生效"])
        x.align["学年学期"] = "l"
        x.padding_width = 1
        a = []
        for it in s:
            ss = list(it)
            aa = []
            for ch in ss:
                ch = ch.lstrip()
                ch = ch.rstrip()
                aa.append(ch)
            a.append(aa)
        for it in a:
            x.add_row(it)
        print(x)


def __main__():
    def menu():
        print('=====欢迎=====')
        print('1. 查看基本信息')
        print('2. 查课表')
        print('3. 查成绩')
        print("4. 退出")
        print("=================")
        print(">>>")
        s=input()
        return s

    def case1():
        dean.getGI()
    def case2():
        dean.getClassTable()


    def case3():
        dean.getGrade()


    def case4():
        exit(0)
    def f(o):
        switch.get(o)()

    dean = DEAN()
    dean.logIn()
    print('登录成功')
    switch = {'1':case1, '2':case2, '3':case3,'4':case4}
    while True:
        try:
            f(menu())
        except:
                print("登录出现问题，请稍后再试")
        print("输入任意数字继续")
        input()


if __name__ == "__main__":
    __main__()
