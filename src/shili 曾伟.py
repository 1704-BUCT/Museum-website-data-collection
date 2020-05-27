import requests
import bs4
import re
from bs4 import BeautifulSoup
import pymysql
import time
import datetime

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
}


def get_all(url):
    re = requests.get(url, headers=header)
    re.encoding = 'utf-8'
    soup = BeautifulSoup(re.text, 'html.parser')
    return soup

#全局变量
global mid,eid,oid
mid=int(0)
eid=int(0)
oid=int(0)

class ConnMysql(object):
    def __init__(self):
        # 连接数据库
        self.db = pymysql.connect(host='39.97.241.101',
                                  port=3306,
                                  database='testsitedb',
                                  user='root',
                                  password='root',
                                  charset='utf8')
        self.cursor = self.db.cursor()

    def insert(self, dict1):
        sql_1 = "insert into museums(name,imgurl,mobile,address,introduction,opentime) values(%s,%s,%s,%s,%s,%s)"
        for i in dict1["1"]:
            data_1 = [i["name"], i["url"], i["number"], i["location"],i["brief"], i["opentime"]]
            try:
                self.cursor.execute(sql_1, data_1)
                self.db.commit()  # 提交操作
            except:
                self.db.rollback()
        #sql_2 = "insert into exhibitions(name,imgurl,introduction,mname) values(%s,%s,%s,%s)"
        #for i in dict1["2"]:
        #    data_2 = [i["ename"], i["img_src"], i["ds"], i["emname"]]
        #    try:
        #        self.cursor.execute(sql_2, data_2)
        #        self.db.commit()  # 提交操作
        #    except:
        #        self.db.rollback()
        #sql_3 = "insert into educations(name,imgurl,introduction,time,mname) values(%s,%s,%s,%s,%s)"
        #for i in dict1["3"]:
        #    data_3 = [i["edname"], i["img_src"], i['ds'], i['time'], i["edmname"]]
        #    try:
        #        self.cursor.execute(sql_3, data_3)
        #        self.db.commit()  # 提交操作
        #    except:
        #        self.db.rollback()
        #sql_4 = "insert into collections(name,imgurl,introduction,mname) values(%s,%s,%s,%s)"
        #for i in dict1["4"]:
         #   data_4 = [i["cpname"],i["img_src"],i['ds'], i["cpmname"]]
          #  try:
          #      self.cursor.execute(sql_4, data_4)
          #      self.db.commit()  # 提交操作
          #  except:
          #      self.db.rollback()


       # self.db.close()

    def dataselect(self, issue, db_table):
        try:
            sql = "SELECT '%s' FROM %s " % (issue, db_table)
            self.cursor.execute(sql)
            self.db.commit()  # 提交操作
        except:
            self.db.rollback()
        finally:
            return issue

def save_data(dict_data):
    # 存数据库
    database = ConnMysql()
    database.insert(dict_data)
    print("保存")
    #数据更新
    # now = datetime.datetime.now()
    # sched_time = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, now.second) +\
    #         datetime.timedelta(days=14)
    # while True:
    #     now = datetime.datetime.now()
    #     if sched_time < now:
    #         print(now)
    #         database.update(dict_data)
    #         sched_time+=datetime.timedelta(days=14)


# 四川
# 自贡恐龙博物馆
def SC_ZGKLmuseum():
    info_main={}
    url = "https://baike.sogou.com/v156681.htm?fromTitle=%E8%87%AA%E8%B4%A1%E6%81%90%E9%BE%99%E5%8D%9A%E7%89%A9%E9%A6%86"
    url_1 = "http://www.zdm.cn/"
    url_2 = "http://www.zdm.cn/introduceinfo.html"
    url_3 = "http://www.zdm.cn/portal/article/index/id/15/cid/51.html"
    res = requests.get(url, headers=header)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    name = '自贡恐龙博物馆'

    #简介
    brief = soup.find(attrs={"name": "description"})['content']
    #print(brief)

    visit = soup.find('table', class_='abstract_tbl')
    info0 = visit.find_all('tr')
    for tag0 in info0:
        title0 = tag0.find('th', class_='base-info-card-title')
        #print(title0.text + ":", end="")
        texts = tag0.find('div', class_='base-info-card-value').find(text=True).strip()
       #print(texts)

    #开放时间
    opentime = ""
    hostinfo = get_all(url_1)
    for i in hostinfo.find_all(name='ul', attrs={'class': "list1BottomBox"}):
        opentime = i.text
       #print(opentime)

    #电话
    number = ""
    for i in str(hostinfo.find_all(name='p', attrs={'class': "footerTel"})).split("<br/>"):
        if (re.search(re.compile(r'联系电话：'), i)):
            number = i
    number = number.split('\u3000')
    number = number[0]
    #print(number)

    #地址
    location = "四川省自贡市"

    info_main["name"] = name
    info_main["brief"] = brief
    info_main["url"] = url
    info_main["location"] = location
    info_main["number"] = number
    info_main["opentime"] = opentime
    aa=[]
    aa.append(info_main)


    #展览简介及图片
    hall=[]
    s={}
    s["ename"]="四川省科普教育基地"
    x = get_all(url_2).find(name="div", attrs={'class': 'textBox'})
    p = x.find_all('p', attrs={'style': 'text-indent: 2em;'})
    a = ""
    for tag in p:
        a = a + tag.text
    s["ds"]=a
    #print(a)
    y = x.find_all_next(name="img")
    num = 0
    for i in y:
        url = url_1 + i["src"]
        #print(url)
        num = num + 1
        s["img_src"]=url
    s["emname"] = '自贡恐龙博物馆'
    hall.append(s)
    #print(hall)

    #教育活动
    s={}
    ed=[]
    s["edname"] = "--第49个世界地球日活动周“珍惜自然资源 呵护美丽国土——讲好我们的地球故事”--"
    url_5 = "http://www.zdm.cn/scenery/175.html"
    x = get_all(url_5).find(name="div", attrs={'class': 'textBox'})
    p = x.find_all('p', attrs={'style': 'text-indent: 2em;'})
    object2 = ""
    for tag in p:
        object2 = object2 + tag.text
    s["ds"]=object2
    #print(object2)
    s["img_src"]=url_5
    s["time"]="4月22日"
    s["edmname"]="自贡恐龙博物馆"
    ed.append(s)


    #博物馆藏品
    cp=[]
    s={}
    s["cpname"]="恐龙头骨化石"
    x = get_all(url_3).find(name="div", attrs={'class': 'textBox'})
    p = x.find_all('p', attrs={'style': 'text-indent: 2em;'})
    object = ""
    for tag in p:
        object = object + tag.text
    s["ds"]=object
    s["img_src"]=url_3
    s["cpmname"] = "自贡恐龙博物馆"
    cp.append(s)
    #print(object)

    info_all = {}
    info_all["1"] = aa
    info_all["2"] = hall
    info_all["3"] = ed
    info_all["4"] = cp

    return(info_all)

# 三星堆博物馆
def SC_SXDmuseum():
    info_main={}
    url = "https://baike.sogou.com/v154245.htm?fromTitle=%E4%B8%89%E6%98%9F%E5%A0%86%E5%8D%9A%E7%89%A9%E9%A6%86"
    url_1 = "http://www.sxd.cn/"
    url_2 = "https://www.sohu.com/a/108829969_111938"
    res = requests.get(url, headers=header)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    name = '三星堆博物馆'

    #简介
    brief = soup.find(attrs={"name": "description"})['content']
    #print(brief)

    #博物馆信息
    visit = soup.find('table', class_='abstract_tbl')
    info0 = visit.find_all('tr')
    for tag0 in info0:
        title0 = tag0.find('th', class_='base-info-card-title')
        #print(title0.text + ":", end="")
        texts = tag0.find('div', class_='base-info-card-value').find(text=True).strip()
        #print(texts)

    #开放参观时间
    opentime = "8:30 - 18:00"
    #print(opentime)

    #联系方式
    number = ""
    hostinfo = get_all(url_1)
    for i in hostinfo.find_all(name='table', attrs={'width': "922", 'height': "68", 'border': "0", 'align': "center",
                                                    'cellpadding': "0", 'cellspacing': "0"}):
        for x in i.find_all(name='td', attrs={'align': "center"}):
            number = x
    #print(number.text)

    # 地址
    location = "四川省广汉市三星堆遗址东北角"

    info_main["name"] = name
    info_main["brief"] = brief
    info_main["location"] = location
    info_main["number"] = number
    info_main["opentime"] = opentime
    info_main["url"] = url
    aa=[]
    aa.append(info_main)

    #展览简介及图片
    hall=[]
    s={}
    s["ename"]="三星堆，长江文明之源"
    x = get_all(url_2).find(name="div", attrs={'class': 'text'})
    p = x.find_all('article', attrs={'class': 'article', 'id': 'mp-editor'})
    object = ""
    for tag in p:
        object = object + tag.text
        s["ds"]=object
    #print(object)
    y = x.find_all_next(name="img")
    num = 0
    for i in y:
        url = url_1 + i["src"]
        s["img_src"]=url
        #print(url)
        s["emname"] = '三星堆博物馆'
        hall.append(s)
        num = num + 1

    #教育活动无
    ed=[]
    s={}
    s["edname"]=""
    s["ds"] = ""
    s["img_src"] = ""
    s["time"] = ""
    s["edmname"] = '三星堆博物馆'
    ed.append(s)

    #博物馆藏品
    cp=[]
    s={}
    s["cpname"]="三星堆文化圆冠神人首玉佩"
    url_3 = "https://baike.sogou.com/v175583995.htm?fromTitle=%E4%B8%89%E6%98%9F%E5%A0%86%E6%96%87%E5%8C%96%E5%9C%86%E5%86%A0%E7%A5%9E%E4%BA%BA%E9%A6%96%E7%8E%89%E4%BD%A9"
    brief1 = get_all(url_3).find(attrs={"name": "description"})['content']
    s["ds"]=brief1
    s["img_src"]=url_3
    s["cpmname"] = '三星堆博物馆'
    cp.append(s)
    #print(brief1)

    info_all = {}
    info_all["1"] = aa
    info_all["2"] = hall
    info_all["3"] = ed
    info_all["4"] = cp

    return (info_all)

# 成都武侯祠博物馆
def SC_CDWHCmuseum():
    info_main={}
    url = "https://baike.sogou.com/v79057.htm?fromTitle=%E6%88%90%E9%83%BD%E6%AD%A6%E4%BE%AF%E7%A5%A0%E5%8D%9A%E7%89%A9%E9%A6%86"
    url_1 = "http://www.wuhouci.net.cn/visit-top1.html"
    url_6 = "http://www.wuhouci.net.cn/index.html"
    res = requests.get(url, headers=header)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    name = '成都武侯祠博物馆'

    #print('简介')
    brief = soup.find(attrs={"name": "description"})['content']
    #print(brief)

    #print('博物馆信息')
    visit = soup.find('table', class_='abstract_tbl')
    info0 = visit.find_all('tr')
    for tag0 in info0:
        title0 = tag0.find('th', class_='base-info-card-title')
        #print(title0.text + ":", end="")
        texts = tag0.find('div', class_='base-info-card-value').find(text=True).strip()
        #print(texts)

    #print('开放时间')
    opentime = "8:00-18:00"
    #print(opentime)

    #print("电话")
    number = "电话:+86-028-85552397(业务)、85535951(票务)、85593818(网站)"
    #print(number)

    # 地址
    location = "中国 四川省 成都市"

    info_main["name"] = name
    info_main["brief"] = brief
    info_main["location"] = location
    info_main["number"] = number
    info_main["opentime"] = opentime
    info_main["url"] = url
    aa=[]
    aa.append(info_main)

    #print('展览简介及图片')
    hall=[]
    s={}
    s["ename"]="武侯祠成都大庙会"
    i = get_all(url_1).find(name="div", attrs={'class': 't'})
    a=i.text
    #print(i.text)
    x = get_all(url_1).find(name="div", attrs={'class': 'd'})
    s["ds"]=x.text
    #print(x.text)
    z = get_all(url_1).find(name="div", attrs={'class': 'focus'})
    y = z.find_all_next(name="img")
    num = 0
    for i in y:
        url = url_1 + i["src"]
        s["img_src"]=url
        #print(url)
        s["emname"] = '成都武侯祠博物馆'
        hall.append(s)
        num = num + 1

    #print('教育活动无')
    ed=[]
    s={}
    s["edname"] = ""
    s["ds"] = ""
    s["img_src"] = ""
    s["time"] = ""
    s["edmname"] = '成都武侯祠博物馆'
    ed.append(s)


    #print('博物馆藏品')
    cp=[]
    s={}
    s["cpname"]="诸葛碗"
    url_3 = "https://baike.sogou.com/v68762251.htm?fromTitle=%E6%98%8E%E8%B1%86%E9%9D%92%E9%87%89%E8%AF%B8%E8%91%9B%E7%A2%97"
    a='诸葛碗'
    brief1 = get_all(url_3).find(attrs={"name": "description"})['content']
    s["ds"]=brief1
    s["img_src"]=url_3
    s["cpmname"] = '成都武侯祠博物馆'
    #print(brief1)
    cp.append(s)


    info_all = {}
    info_all["1"] = aa
    info_all["2"] = hall
    info_all["3"] = ed
    info_all["4"] = cp

    return (info_all)


# 邓小平故居陈列馆
def SC_DXPGJmuseum():
    info_main={}
    url = "https://baike.sogou.com/v10997201.htm?fromTitle=%E9%82%93%E5%B0%8F%E5%B9%B3%E6%95%85%E5%B1%85%E9%99%88%E5%88%97%E9%A6%86"
    url_1 = "http://www.china.com.cn/book/zhuanti/1bowuguan/2008-11/11/content_16746678.htm"
    res = requests.get(url, headers=header)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    name = '邓小平故居陈列馆'

    #print('简介')
    brief = soup.find(attrs={"name": "description"})['content']
    #print(brief)

    #print('博物馆信息')
    visit = soup.find('table', class_='abstract_tbl')
    info0 = visit.find_all('tr')
    for tag0 in info0:
        title0 = tag0.find('th', class_='base-info-card-title')
        #print(title0.text + ":", end="")
        texts = tag0.find('div', class_='base-info-card-value').find(text=True).strip()
        #print(texts)

    #print('开放时间')
    opentime = "淡季8:30～17:30　旺季8:30～18:00"
    #print(opentime)

    #print('电话')
    number = "电话：0826-2413858"
    #print(number)

    # 地址
    location = "四川省广安市广安区"
    info_main["url"] = url
    info_main["name"] = name
    info_main["brief"] = brief
    info_main["location"] = location
    info_main["number"] = number
    info_main["opentime"] = opentime
    aa=[]
    aa.append(info_main)

    #print('展馆介绍及图片')
    hall=[]
    s={}
    s["ename"]="《我是中国人民的儿子》为主题"
    s["ds"]=  '邓小平故居陈列馆由一个序厅、三个陈列展厅、一个珍藏厅、一个电影放映厅及相关附属设施组成。' \
        '陈列布展引入了国际博物馆先进展示理念，以《我是中国人民的儿子》为主题，展出珍贵文物170件、图片408幅、' \
        '文献资料200余件、复制场景4个、制作多媒体620万字，结合声、光、电等高科技手段，再现邓小平光辉的一生。' \
        '2005年5月17日该展览荣获第六届全国博物馆系统十大精品陈列展览特别奖。第一单元“走出广安”反映了邓小平的家世、' \
        '童年和少年读书生活，旅法勤工俭学走上革命道路，在莫斯科中山大学学习，投身国内革命洪流等早期革命生涯。第二单元“戎马生涯”' \
        '反映了邓小平从领导广西革命斗争、参加长征到战斗在抗战前线，再到挥师解放战场，为建立新中国，实现中华民族的独立和解放立下的赫赫战功。' \
        '第三单元“艰辛探索”反映了建国后，邓小平主政大西南，特别是作为以毛泽东为核心的党的第一代中央领导集体的重要成员，在总书记执任上，为建立和巩固社会主义制度进行的艰辛探索。' \
        '第四单元“非常岁月”反映了“文化大革命”中邓小平在江西的日子和他复出主持中央日常工作，大刀阔斧地全面整顿，表现了他“两落两起”的传奇经历。第五单元“开创伟业”反映了在新的历史时期，' \
        '邓小平领导党和人民实现伟大的历史转折，开辟中国特色社会主义道路，改革开放，进行现代化建设的伟大功绩。第五单元“开创伟业”反映了在新的历史时期，邓小平领导党和人民实现伟大的历史转折，' \
        '开辟中国特色社会主义道路，改革开放，进行现代化建设的伟大功绩。'
    url_2 = "http://cpc.people.com.cn/n/2013/0806/c69687-22460654.html"
    x = get_all(url_2).find(name="div", attrs={'class': 'text', 'id': 'p_content'})
    y = x.find_all_next(name="img")
    num = 0
    for i in y:
        url = url_1 + i["src"]
        #print(url)
        s["img_src"]=url
        s["emname"] = '邓小平故居陈列馆'
        hall.append(s)
        num = num + 1

    #print('教育活动无')
    ed=[]
    s={}
    s["edname"] = ""
    s["ds"] = ""
    s["img_src"] = ""
    s["time"] = ""
    s["edmname"] = '邓小平故居陈列馆'
    ed.append(s)

    #print('博物馆藏品')
    cp=[]
    s={}
    s["cpname"]="红旗检阅车"
    url_4 = "https://baike.sogou.com/v70017724.htm?fromTitle=%E7%BA%A2%E6%97%97%E6%A3%80%E9%98%85%E8%BD%A6"
    a='红旗检阅车'
    brief1 = get_all(url_4).find(attrs={"name": "description"})['content']
    s["ds"]=brief1
    s["img_src"]=url_4
    s["cpmname"] = '邓小平故居陈列馆'
    cp.append(s)
    #print(brief1)

    info_all = {}
    info_all["1"] = aa
    info_all["2"] = hall
    info_all["3"] = ed
    info_all["4"] = cp

    return (info_all)

# 成都杜甫草堂博物馆
def SC_CDDFCTmuseum():
    info_main={}
    url = "https://baike.sogou.com/v175310.htm?fromTitle=%E6%88%90%E9%83%BD%E6%9D%9C%E7%94%AB%E8%8D%89%E5%A0%82%E5%8D%9A%E7%89%A9%E9%A6%86"
    res = requests.get(url, headers=header)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    name = '成都杜甫草堂博物馆'

    #print('简介')
    brief = soup.find(attrs={"name": "description"})['content']
    #print(brief)

    #print('博物馆信息')
    visit = soup.find('table', class_='abstract_tbl')
    info0 = visit.find_all('tr')
    for tag0 in info0:
        title0 = tag0.find('th', class_='base-info-card-title')
        #print(title0.text + ":", end="")
        texts = tag0.find('div', class_='base-info-card-value').find(text=True).strip()
        #print(texts)

    #print('开放时间')
    opentime = "（5月~10月）：8:00~20:00（11月~次年4月）：8:00~18:30"
    #print(opentime)

    #print('电话')
    number = "028-66005161;028-87327392'"
    #print(number)

    # 地址
    location = "中国 四川省 成都市"
    info_main["url"] = url
    info_main["name"] = name
    info_main["brief"] = brief
    info_main["location"] = location
    info_main["number"] = number
    info_main["opentime"] = opentime
    aa=[]
    aa.append(info_main)

    #print('展览简介及图片')
    hall=[]
    s={}
    s["ename"] = "草堂听琴"
    url_1 = "https://baike.sogou.com/v66232978.htm?fromTitle=%E8%8D%89%E5%A0%82%E5%90%AC%E7%90%B4"
    a='草堂听琴'
    brief1 = get_all(url_1).find(attrs={"name": "description"})['content']
    s["ds"]=brief1
    s["img_src"]=url_1
    s["emname"] = '成都杜甫草堂博物馆'
    hall.append(s)
    #print(brief)

    #print('教育活动无')
    ed=[]
    s={}
    s["edname"] = ""
    s["ds"] = ""
    s["img_src"] = ""
    s["time"] = ""
    s["edmname"] = '成都杜甫草堂博物馆'
    ed.append(s)

    cp=[]
    s={}
    s["cpname"]="中外杜诗版本、书画、研究手稿、音像制品、图片资料和有关实物等各类文物藏品和资料5万件（册）"
    s["ds"]='博物馆藏品'\
         '成都杜甫草堂博物馆馆藏中外杜诗版本、书画、研究手稿、音像制品、图片资料和有关实物等各类文物藏品和资料5万件（册），是当代最大的杜甫研究资料和杜诗书画的收藏展示中心。' \
         '其中系统收藏了宋、元、明、清历代杜集版本万余册，明、清至近现代杜诗书画作品3000余件。'
    s["img_src"] = ""
    s["cpmname"] = '成都杜甫草堂博物馆'
    cp.append(s)

    info_all = {}
    info_all["1"] = aa
    info_all["2"] = hall
    info_all["3"] = ed
    info_all["4"] = cp

    return (info_all)

# 四川博物院
def SC_SCmuseum():
    info_main={}
    url = "https://baike.sogou.com/v163005.htm?fromTitle=%E5%9B%9B%E5%B7%9D%E5%8D%9A%E7%89%A9%E9%99%A2"
    res = requests.get(url, headers=header)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    name = '四川博物院'

    #print('简介')
    brief = soup.find(attrs={"name": "description"})['content']
    #print(brief)

    #print('博物馆信息')
    visit = soup.find('table', class_='abstract_tbl')
    info0 = visit.find_all('tr')
    for tag0 in info0:
        title0 = tag0.find('th', class_='base-info-card-title')
        #print(title0.text + ":", end="")
        texts = tag0.find('div', class_='base-info-card-value').find(text=True).strip()
        #print(texts)

    #print('开放时间')
    opentime = "周二-周日9:00-17:00"
    #print(opentime)

    #print('电话')
    number = ('028-65521888')
    #print(number)

    # 地址
    location = "中国 四川省 成都市"
    info_main["url"] = url
    info_main["name"] = name
    info_main["brief"] = brief
    info_main["location"] = location
    info_main["number"] = number
    info_main["opentime"] = opentime
    aa=[]
    aa.append(info_main)

    #print('展览简介及图片')
    hall=[]
    s={}
    s["ename"]="蜀地海关 守关护宝——成都海关查获文物特展"
    url_1 = "http://www.scmuseum.cn/thread-117-114.html"
    x = get_all(url_1).find(name="div", attrs={'id': 'MyContent'})
    s["ds"]='蜀地海关 守关护宝——成都海关查获文物特展,文物是中华文明源远流长和生生不息的实物见证' \
         '，依法履行对文物资源的守护之责，是对中华文化的认同与尊重，是后辈对前人文化遗产一脉相传的坚守与传承。2018年底，' \
         '中华人民共和国成都海关将数年查获走私的334件文物及艺术品移交给四川省文物局。这些文物时间跨度长，种类丰富，具有较高的历史、科学和艺术价值。' \
         '我们从中挑选了200余件文物，策划了此次展览，一方面让公众了解海关日常工作，展示成都海关近年来打击走私工作成果；另一方面希望通过该展览提升社会公众的文物保护意识。'
    y = x.find_all_next(name="img")
    num = 0
    for i in y:
        url = url_1 + i["src"]
        s["img_src"]=url
        #print(url)
        s["emname"] = '四川博物院'
        hall.append(s)
        num = num + 1

    #print('教育活动')
    ed=[]
    s={}
    s["edname"]="四川博物院与四川省电化教育馆开展合作"
    url_3 = "http://www.scmuseum.cn/thread-2-120.html"
    x = get_all(url_3).find(name="div", attrs={'class': 'sbp-content'})
    p = get_all(url_3).find(name="p", attrs={'style': 'TEXT-INDENT: 2em;'})
    s["ds"]='2015年9月，经四川省文化厅、教育厅党组批准，四川博物院与四川省教育科学研究所合作成立了四川省博物馆教育研究所（以下简称博教所）.' \
      '博教所立足于博物馆教育资源的研究与开发，是目前国内第一家博物馆与教科所联合成立的旨在促进博物馆教育与学校教育融合对接的研究机构。' \
      '同时，四川博物院与四川省电化教育馆开展合作，双方充分利用四川丰富的文博资源，通过四川省“三通两平台”建设和四川卫视科教频道的资源优势，让博物馆资源插上信息化的翅膀，惠及四川1000多万中小学师生。'
    y = x.find_all_next(name="img")
    num = 0
    for i in y:
        url = url_1 + i["src"]
        s["img_src"]=url
        s["time"]="2015年9月"
        s["edmname"] = '四川博物院'
        #print(url)
        num = num + 1
    ed.append(s)

    cp=[]
    #'博物馆藏品'
    s={}
    s["cpname"]="张大千书画  藏传佛教"
    s["ds"]='张大千书画  藏传佛教'
    s["img_src"] = ""
    s["cpmname"] = '四川博物院'
    cp.append(s)


    info_all = {}
    info_all["1"] = aa
    info_all["2"] = hall
    info_all["3"] = ed
    info_all["4"] = cp

    return (info_all)


# 成都金沙遗址博物馆
def SC_CDJSJmuseum():
    info_main={}
    url = "https://baike.sogou.com/v7864706.htm?fromTitle=%E6%88%90%E9%83%BD%E9%87%91%E6%B2%99%E9%81%97%E5%9D%80%E5%8D%9A%E7%89%A9%E9%A6%86"
    res = requests.get(url, headers=header)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    name = '成都金沙遗址博物馆'

    #print('简介')
    brief = soup.find(attrs={"name": "description"})['content']
    #print(brief)

    #print('博物馆信息')
    visit = soup.find('table', class_='abstract_tbl')
    info0 = visit.find_all('tr')
    for tag0 in info0:
        title0 = tag0.find('th', class_='base-info-card-title')
        #print(title0.text + ":", end="")
        texts = tag0.find('div', class_='base-info-card-value').find(text=True).strip()
        #print(texts)

    #print('电话')
    number = ('028-66113699')
    #print(number)

    #print('开放参观时间')
    url_1 = "http://www.jinshasitemuseum.com/Visit/VisitOpenTime"
    hostinfo = get_all(url_1)
    for i in hostinfo.find_all(name='div', attrs={'class': "openTime-details"}):
        opentime = i.text
        #print(opentime)

    # 地址
    location = "中国 四川省 成都市"
    info_main["url"] = url
    info_main["name"] = name
    info_main["brief"] = brief
    info_main["location"] = location
    info_main["number"] = number
    info_main["opentime"] = opentime
    aa=[]
    aa.append(info_main)


    #print('展览简介及图片')
    hall=[]
    s={}
    s["ename"] = "第一展厅 远古家园"
    url_2 = "http://www.jinshasitemuseum.com/Exhibition/ExhibitionFourth?id=780"
    hostinfo = get_all(url_2)
    for i in hostinfo.find_all(name='div', attrs={'class': "museum-text"}):
        a=i.text
        s["ds"]=a
        #print(i.text)
    x = get_all(url_2).find(name="div", attrs={'class': 'museum-carousel'})
    y = x.find_all_next(name="img")
    num = 0
    for i in y:
        url = url_1 + i["src"]
        s["img_src"]=url
        s["emname"] = '成都金沙遗址博物馆'
        hall.append(s)
        #print(url)
        num = num + 1


    #print('教育活动')
    ed=[]
    s={}
    s["edname"]=""
    url_7 = "http://www.jinshasitemuseum.com/CulturalActivity/CulturalDetails?id=4888&&line=%E7%B3%BB%E5%88%97%E6%96%87%E5%8C%96%E6%B4%BB%E5%8A%A8"
    hostinfo = get_all(url_7)
    for i in hostinfo.find_all(name='div', attrs={'id': "MyContent"}):
        a=i.text
        s["ds"]=a
        #print(i.text)
    x = get_all(url_7).find(name="div", attrs={'id': 'MyContent'})
    y = x.find_all_next(name="img")
    num = 0
    for i in y:
        url = url_1 + i["src"]
        s["img_src"]=url
        #print(url)
        num = num + 1
    s["time"]=""
    s["edmname"] = '成都金沙遗址博物馆'
    ed.append(s)

    #print('博物馆藏品')
    cp=[]
    s={}
    s["cpname"]="商周鸟首鱼纹金带"
    url_8 = "https://baike.sogou.com/v71434129.htm?fromTitle=%E5%95%86%E5%91%A8%E9%B8%9F%E9%A6%96%E9%B1%BC%E7%BA%B9%E9%87%91%E5%B8%A6"
    a='商周鸟首鱼纹金带'
    brief1 = get_all(url_8).find(attrs={"name": "description"})['content']
    s["ds"]=brief1
    s["img_src"] = url_8
    s["cpmname"] = '成都金沙遗址博物馆'
    #print(brief1)
    cp.append(s)

    info_all = {}
    info_all["1"] = aa
    info_all["2"] = hall
    info_all["3"] = ed
    info_all["4"] = cp

    return (info_all)


# 自贡市盐业历史博物馆
def SC_ZGYYmuseum():
    info_main={}
    url = "https://baike.sogou.com/v155008.htm?fromTitle=%E8%87%AA%E8%B4%A1%E5%B8%82%E7%9B%90%E4%B8%9A%E5%8E%86%E5%8F%B2%E5%8D%9A%E7%89%A9%E9%A6%86"
    res = requests.get(url, headers=header)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    name = '自贡市盐业历史博物馆'

   # print('简介')
    brief = soup.find(attrs={"name": "description"})['content']
   # print(brief)

    #print('博物馆信息')
    visit = soup.find('table', class_='abstract_tbl')
    info0 = visit.find_all('tr')
    for tag0 in info0:
        title0 = tag0.find('th', class_='base-info-card-title')
        #print(title0.text + ":", end="")
        texts = tag0.find('div', class_='base-info-card-value').find(text=True).strip()
        #print(texts)

    #print('电话')
    url_8 = "http://www.zgshm.cn/bwggk.html"
    hostinfo = get_all(url_8)
    for i in hostinfo.find_all(name='div', attrs={'class': "btm_txt"}):
        number = i.text
        #print(number)

    #print('开放参观时间')
    opentime = "8:00-17:00"
    #print(opentime)

    # 地址
    location = "中国 四川省 自贡市"
    info_main["url"] = url
    info_main["name"] = name
    info_main["brief"] = brief
    info_main["location"] = location
    info_main["number"] = number
    info_main["opentime"] = opentime
    aa=[]
    aa.append(info_main)

    #print('展览简介及图片')
    hall=[]
    s={}
    s["ename"] = "赵熙书画精品展"
    url_2 = "http://www.zgshm.cn/content.jsp?id=297e0fc26362ffbb016380999c120188"
    hostinfo = get_all(url_2)
    for i in hostinfo.find_all(name='div', attrs={'id': "news_conent_two_text", 'class': 'news_conent_two_text'}):
        a=i.text
        s["ds"]=a
        #print(i.text)
    x = get_all(url_2).find(name="div", attrs={'id': "news_conent_two_text", 'class': 'news_conent_two_text'})
    y = x.find_all_next(name="img")
    num = 0
    for i in y:
        url = url_2 + i["src"]
        s["img_src"]=url
        s["emname"] = '自贡市盐业历史博物馆'
        hall.append(s)
        #print(url)
        num = num + 1

    #print('教育活动')
    ed=[]
    s={}
    s["edname"] = "--“天车杯”自贡青少年足球邀请赛颁奖典礼 暨盐博馆研学游参观学习活动圆满成功--"
    url_6 = "http://www.zgshm.cn/content.jsp?id=297e0fc26e679f79016fc0be2bdc0060"
    hostinfo = get_all(url_6)
    for i in hostinfo.find_all(name='div', attrs={'id': "news_conent_two_text", 'class': 'news_conent_two_text'}):
        a = i.text
        s["ds"]=a
        #print(i.text)
    x = get_all(url_6).find(name="div", attrs={'id': "news_conent_two_text", 'class': 'news_conent_two_text'})
    y = x.find_all_next(name="img")
    num = 0
    for i in y:
        url = url_6 + i["src"]
        s["img_src"]=url
        #print(url)
        num = num + 1
    s["time"]="1月18日"
    s["img_src"]=""
    s["edmname"] = '自贡市盐业历史博物馆'
    ed.append(s)


    #print('博物馆藏品')
    cp=[]
    s={}
    s["cpname"]="一套最完整的中国古代凿井、修治井工具群"
    url_5 = "http://www.zgshm.cn/content.jsp?id=297e0fc26386368801638c40788f011f&classid=2e4d84b1fd574326ae0f1915eb1c28da"
    hostinfo = get_all(url_5)
    for i in hostinfo.find_all(name='div', attrs={'id': "news_conent_two_text", 'class': 'news_conent_two_text'}):
        a = i.text
        s["ds"]=a
        s["img_src"] = url_5
        #print(i.text)
        s["cpmname"] = '自贡市盐业历史博物馆'
        cp.append(s)

        info_all = {}
        info_all["1"] = aa
        info_all["2"] = hall
        info_all["3"] = ed
        info_all["4"] = cp

        return (info_all)


# 贵州
# 遵义会议纪念馆
def GZ_ZYHYmuseum():
    info_main={}
    url = "https://baike.sogou.com/v7940672.htm?fromTitle=%E9%81%B5%E4%B9%89%E4%BC%9A%E8%AE%AE%E7%BA%AA%E5%BF%B5%E9%A6%86"
    res = requests.get(url, headers=header)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    name = '遵义会议纪念馆'

    #print('简介')
    brief = soup.find(attrs={"name": "description"})['content']
    #print(brief)

    #print('博物馆信息')
    visit = soup.find('table', class_='abstract_tbl')
    info0 = visit.find_all('tr')
    for tag0 in info0:
        title0 = tag0.find('th', class_='base-info-card-title')
        #print(title0.text + ":", end="")
        texts = tag0.find('div', class_='base-info-card-value').find(text=True).strip()
        #print(texts)

    #print('电话')
    url_1 = "http://www.zunyihy.cn/about.html"
    hostinfo = get_all(url_1)
    for i in hostinfo.find_all(name='div', attrs={'class': "add"}):
        number = i.text
        #print(number)

    #print('开放参观时间')
    opentime = "8:30-17:00"
    #print(opentime)

    # 地址
    location = "中国 贵州省 遵义市"
    info_main["url"] = url
    info_main["name"] = name
    info_main["brief"] = brief
    info_main["location"] = location
    info_main["number"] = number
    info_main["opentime"] = opentime
    aa=[]
    aa.append(info_main)

    #print('展览简介及图片')
    hall=[]
    s={}
    s["ename"]="遵义会议会址"
    url_2 = "http://www.zunyihy.cn/display.html"
    hostinfo = get_all(url_2)
    for i in hostinfo.find_all(name='div', attrs={'class': "list"}):
        a = i.text
        s["ds"]=a
        #print(i.text)
    x = get_all(url_2).find(name='div', attrs={'class': "list"})
    y = x.find_all_next(name="img")
    num = 0
    for i in y:
        url = url_2 + i["src"]
        s["img_src"]=url
        s["emname"] = '遵义会议纪念馆'
        hall.append(s)
        #print(url)
        num = num + 1

    #print('教育活动')
    ed=[]
    s={}
    s["edname"] = "--遵义市消防部门在遵义会议会址开展宣传活动--"
    url_3 = "http://www.zunyihy.cn/detail/506.html"
    hostinfo = get_all(url_3)
    for i in hostinfo.find_all(name='div', attrs={'style': 'text-indent:2em;'}):
        a = i.text
        s["ds"]=a
        s["img_src"]=url_3
        s["time"]="12月9日"
        #print(i.text)
    s["edmname"] = '遵义会议纪念馆'
    ed.append(s)

    #print('博物馆藏品')
    cp=[]
    s={}
    s["cpname"]="遵义会议开会的长方桌"
    url_5 = "http://www.zunyihy.cn/detail/947.html"
    hostinfo = get_all(url_5)
    for i in hostinfo.find_all(name='div', attrs={'class': 'situation_1'}):
        a = i.text
        s["ds"]=a
        s["img_src"] = url_5
        #print(i.text)
        s["cpmname"] = '遵义会议纪念馆'
        cp.append(s)

        info_all = {}
        info_all["1"] = aa
        info_all["2"] = hall
        info_all["3"] = ed
        info_all["4"] = cp

        return (info_all)

# 云南
# 云南省博物馆
def YN_YNmuseum():
    info_main={}
    url = "https://baike.sogou.com/v163118.htm?fromTitle=%E4%BA%91%E5%8D%97%E7%9C%81%E5%8D%9A%E7%89%A9%E9%A6%86"
    res = requests.get(url, headers=header)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    name = '云南省博物馆'

    #print('简介')
    brief = soup.find(attrs={"name": "description"})['content']
    #print(brief)

    #print('博物馆信息')
    visit = soup.find('table', class_='abstract_tbl')
    info0 = visit.find_all('tr')
    for tag0 in info0:
        title0 = tag0.find('th', class_='base-info-card-title')
        #print(title0.text + ":", end="")
        texts = tag0.find('div', class_='base-info-card-value').find(text=True).strip()
        #print(texts)

    #print('开放参观时间')
    url_1 = "http://www.ynmuseum.org/index.html"
    hostinfo = get_all(url_1)
    for i in hostinfo.find_all(name='div', attrs={'class': "time"}):
        opentime = i.text
        #print(opentime)

    #print('电话')
    url_8 = "http://www.ynmuseum.org/survey.html#section=5"
    hostinfo = get_all(url_8)
    for i in hostinfo.find_all(name='div', attrs={'class': "s2"}):
        number = i.text
        #print(number)

    # 地址
    location = "云南省昆明市广福路6393号"
    info_main["url"] = url
    info_main["name"] = name
    info_main["brief"] = brief
    info_main["location"] = location
    info_main["number"] = number
    info_main["opentime"] = opentime
    aa=[]
    aa.append(info_main)

    #print('展览简介及图片')
    hall=[]
    s={}
    s["ename"] = "木韵春华——海南黄花黎展"
    url_2 = "http://www.ynmuseum.org/detail/665.html"
    hostinfo = get_all(url_2)
    for i in hostinfo.find_all(name='div', attrs={'class': "content"}):
        a=i.text
        s["ds"]=a
        #print(i.text)
    x = get_all(url_2).find(name="div", attrs={'class': 'content'})
    y = x.find_all_next(name="img")
    num = 0
    for i in y:
        url = url_2 + i["src"]
        s["img_src"]=url
        s["emname"] = '云南省博物馆'
        hall.append(s)
        #print(url)
        num = num + 1

    #print('教育活动')
    ed=[]
    s={}
    s["edname"] = "---守护国宝 传承文明——记金康园小学二年级学生博物馆研学活动---"
    url_5 = "http://www.ynmuseum.org/detail/1177.html"
    hostinfo = get_all(url_5)
    for i in hostinfo.find_all(name='div', attrs={'style': "text-align:justify;"}):
        a = i.text
        s["ds"]=a
        #print(i.text)
    x = get_all(url_5).find(name="div", attrs={'class': 'content'})
    y = x.find_all_next(name="img")
    num = 0
    for i in y:
        url = url_5 + i["src"]
        s["img_src"]=url
        #print(url)
        num = num + 1
    s["time"]="2019年10月16日"
    s["edmname"] = '云南省博物馆'
    ed.append(s)

    #print('博物馆藏品')
    cp=[]
    s={}
    s["cpname"]="书画、青铜器、宗教、邮票、钱币、金银器、玉器、漆器、织绣、契约文书、元明清景德镇青花瓷器"
    url_7 = "http://www.ynmuseum.org/detail/141.html"
    hostinfo = get_all(url_7)
    for i in hostinfo.find_all(name='div', attrs={'class': "content"}):
        a = i.text
        s["ds"]=a
        s["img_src"] = url_7
        #print(i.text)
        s["cpmname"] = '云南省博物馆'
        cp.append(s)


        info_all = {}
        info_all["1"] = aa
        info_all["2"] = hall
        info_all["3"] = ed
        info_all["4"] = cp

        return (info_all)

# 云南民族博物馆
def YN_YNMZmuseum():
    info_main={}
    url = "https://baike.sogou.com/v513028.htm?fromTitle=%E4%BA%91%E5%8D%97%E6%B0%91%E6%97%8F%E5%8D%9A%E7%89%A9%E9%A6%86"
    res = requests.get(url, headers=header)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    name = '云南民族博物馆'

    #print('简介')
    brief = soup.find(attrs={"name": "description"})['content']
    #print(brief)

    #print('博物馆信息')
    visit = soup.find('table', class_='abstract_tbl')
    info0 = visit.find_all('tr')
    for tag0 in info0:
        title0 = tag0.find('th', class_='base-info-card-title')
        #print(title0.text + ":", end="")
        texts = tag0.find('div', class_='base-info-card-value').find(text=True).strip()
        #print(texts)

    #print('开放参观时间')
    opentime = '周二至周日上午9:00——下午4:30（周一闭馆）'
    #print(opentime)

    #print('电话')
    url_1 = "http://www.ynnmuseum.com/lianxi.html"
    hostinfo = get_all(url_1)
    for i in hostinfo.find_all(name='div', attrs={'class': "FrontComContent_detail01-1345105899276_htmlbreak"}):
        number = i.text
        #print(number)

    # 地址
    location = "中国 云南省 昆明市"

    info_main["url"] = url
    info_main["name"] = name
    info_main["brief"] = brief
    info_main["location"] = location
    info_main["number"] = number
    info_main["opentime"] = opentime
    aa=[]
    aa.append(info_main)

    #print('展览简介及图片')
    hall=[]
    s={}
    s["ename"] = "铸牢中华民族共同体意识 建设全国民族团结进步示范区—中国特色解决民族问题正确道路的云南实践"
    url_2 = "http://www.ynnmuseum.com/products_detail/productId=131.html"
    hostinfo = get_all(url_2)
    for i in hostinfo.find_all(name='div', attrs={'class': "FrontProducts_detail02-1345165696285_htmlbreak"}):
        a = i.text
        s["ds"]=a
        #print(i.text)
    x = get_all(url_2).find(name="div", attrs={'class': 'content'})
    y = x.find_all_next(name="img")
    num = 0
    for i in y:
        url = url_2 + i["src"]
        s["img_src"]=url
        s["emname"] = '云南民族博物馆'
        hall.append(s)
        #print(url)
        num = num + 1

    #print('教育活动')
    ed=[]
    s={}
    s["edname"]="“东风霁雨烟柳情”清明活动推文 "
    url_5 = "http://www.ynnmuseum.com/kj.html#"
    hostinfo = get_all(url_5)
    for i in hostinfo.find_all(name='div', attrs={'class': "FrontComContent_detail01-1345105408838_htmlbreak"}):
        a = i.text
        s["ds"]=a
        #print(i.text)
    x = get_all(url_5).find(name="div", attrs={'class': 'content'})
    y = x.find_all_next(name="img")
    num = 0
    for i in y:
        url = url_5 + i["src"]
        s["img_src"]=url
        s["time"]="2019.06.26"
        #print(url)
        num = num + 1
        s["edmname"] = '云南民族博物馆'
    hall.append(s)

    #print('博物馆藏品')
    cp=[]
    s={}
    s["cpname"]="张德和40件白族布扎"
    a='张德和40件白族布扎'
    cp.append(a)
    url_6 = "http://www.ynnmuseum.com/products_detail1/productId=129.html"
    hostinfo = get_all(url_6)
    for i in hostinfo.find_all(name='div', attrs={'class': "FrontProducts_detail02-13451656965_htmlbreak"}):
        a=i.text
        s["ds"]=a
        s["img_src"] = url_6
        #print(i.text)
        s["cpmname"] = '云南民族博物馆'
        cp.append(s)

        info_all = {}
        info_all["1"] = aa
        info_all["2"] = hall
        info_all["3"] = ed
        info_all["4"] = cp
        return (info_all)


# 重庆
# 重庆中国三峡博物馆
def CQ_CQSXmuseum():
    info_main={}
    url = "https://baike.sogou.com/v154272.htm?fromTitle=%E9%87%8D%E5%BA%86%E4%B8%AD%E5%9B%BD%E4%B8%89%E5%B3%A1%E5%8D%9A%E7%89%A9%E9%A6%86"
    res = requests.get(url, headers=header)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    name = '重庆中国三峡博物馆'

    #print('简介')
    brief = soup.find(attrs={"name": "description"})['content']
    #print(brief)

    #print('博物馆信息')
    visit = soup.find('table', class_='abstract_tbl')
    info0 = visit.find_all('tr')
    for tag0 in info0:
        title0 = tag0.find('th', class_='base-info-card-title')
        #print(title0.text + ":", end="")
        texts = tag0.find('div', class_='base-info-card-value').find(text=True).strip()
        #print(texts)

    #print('电话')
    url_1 = "http://www.3gmuseum.cn/"
    hostinfo = get_all(url_1)
    number = "023-7454886"
    #print(number)

    #print('开放时间')
    opentime = "9：00—17：00"
    #print(opentime)

    # 地址
    location = "中国 重庆市"

    info_main["url"] = url
    info_main["name"] = name
    info_main["brief"] = brief
    info_main["location"] = location
    info_main["number"] = number
    info_main["opentime"] = opentime
    aa=[]
    aa.append(info_main)

    #print('展览简介及图片')
    hall=[]
    s={}
    s["ename"] = "衣袭华美——百年海派旗袍的前世今生---"
    url_2 = "http://www.3gmuseum.cn/web/article/toArticleNo.do?itemno=23&pageindex=1&itemsonno=25434353&articleno=5cb088aee0a3482997f9265a335f7183"
    hostinfo = get_all(url_2)
    for i in hostinfo.find_all(name='div', attrs={'class': "art-footer1"}):
        a = i.text
        s["ds"]=a
        #print(i.text)
    x = get_all(url_2).find(name="div", attrs={'class': 'art-footer1'})
    y = x.find_all_next(name="img")
    num = 0
    for i in y:
        url = url_2 + i["src"]
        s["img_src"]=url
        #print(url)
        num = num + 1
    s["emname"] = '重庆中国三峡博物馆'
    hall.append(s)

    #print('教育活动')
    ed=[]
    s={}
    s["edname"] = "---东风霁雨烟柳情”清明活动---"
    url_4 = "http://www.3gmuseum.cn/web/activity/toActivityInfo.do?itemsonno=34324333&articleno=2c8482d76998ee140169dcfc4d8700a5&pageindex=2&activityType=1"
    hostinfo = get_all(url_4)
    for i in hostinfo.find_all(name='div', attrs={'class': "art-footer1"}):
        a = i.text
        s["ds"]=a
        #print(i.text)
    s["img_src"]=url_4
    s["time"]="2019.03.08"
    s["edmname"] = '重庆中国三峡博物馆'
    ed.append(s)

    #print('博物馆藏品')
    cp=[]
    s={}
    s["cpname"]="三羊尊 鸟形尊"
    a='三羊尊'
    url_6 = "http://www.3gmuseum.cn/web/article/toArticleNo.do?itemno=4086522052551f21g55h1d25a1s2s1g5&itemsonno=402880b25a3bb962015a3bc512601205&articleno=402880e55a49ba4f015a49da08370003&pageindex=2"
    hostinfo = get_all(url_6)
    for i in hostinfo.find_all(name='div', attrs={'class': "art-footer1"}):
        a = i.text
        s["ds"]=a
        s["img_src"] = url_6
        s["cpmname"] = '重庆中国三峡博物馆'
        cp.append(s)
        #print(i.text)


        info_all = {}
        info_all["1"] = aa
        info_all["2"] = hall
        info_all["3"] = ed
        info_all["4"] = cp
        return (info_all)


# 重庆自然博物馆
def CQ_CQZRmuseum():
    info_main={}
    url = "https://baike.sogou.com/v5682917.htm?fromTitle=%E9%87%8D%E5%BA%86%E8%87%AA%E7%84%B6%E5%8D%9A%E7%89%A9%E9%A6%86"
    res = requests.get(url, headers=header)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    name = '重庆自然博物馆'

    #print('简介')
    brief = soup.find(attrs={"name": "description"})['content']
    #print(brief)

    #print('博物馆信息')
    visit = soup.find('table', class_='abstract_tbl')
    info0 = visit.find_all('tr')
    for tag0 in info0:
        title0 = tag0.find('th', class_='base-info-card-title')
        #print(title0.text + ":", end="")
        texts = tag0.find('div', class_='base-info-card-value').find(text=True).strip()
        #print(texts)

    #print('电话')
    url_1 = "https://www.cmnh.org.cn/about/?31.html"
    hostinfo = get_all(url_1)
    for i in hostinfo.find_all(name='div', attrs={'class': "pp1"}):
        number = i.text
        #print(number)

    #print('开放时间')
    opentime = "9：00—17：00"
    #print(opentime)

    # 地址
    location = "中国 重庆市"
    info_main["url"] = url
    info_main["name"] = name
    info_main["brief"] = brief
    info_main["location"] = location
    info_main["number"] = number
    info_main["opentime"] = opentime
    aa=[]
    aa.append(info_main)

    #print('展览简介及图片')
    hall=[]
    s={}
    s["ename"] = "邮票上的恐龙---"
    url_2 = "https://www.cmnh.org.cn/content/?137.html"
    hostinfo = get_all(url_2)
    for i in hostinfo.find_all(name='div', attrs={'class': "newsxx_nr"}):
        a = i.text
        s["ds"]=a
        #print(i.text)
    x = get_all(url_2).find(name="div", attrs={'class': 'newsxx_nr'})
    y = x.find_all_next(name="img")
    num = 0
    for i in y:
        url = url_2 + i["src"]
        s["img_src"]=url
        s["emname"] = '重庆自然博物馆'
        hall.append(s)
        #print(url)
        num = num + 1

    #print('教育活动')
    ed=[]
    s={}
    s["edname"] = "--重庆自然博物馆暑期活动征集令--"
    url_4 = "https://www.cmnh.org.cn/content/?61.html"
    hostinfo = get_all(url_4)
    for i in hostinfo.find_all(name='div', attrs={'class': "newsxx_nr"}):
        a = i.text
        s["ds"]=a
        #print(i.text)
    s["img_src"]=url_4
    s["time"]="2019.07.03"
    s["edmname"] = '重庆自然博物馆'
    ed.append(s)

    #print('博物馆藏品')
    cp=[]
    s={}
    s["cpname"]=""
    s["ds"]=""
    s["img_src"] = ""
    s["cpmname"] = '重庆自然博物馆'
    cp.append(s)


    info_all = {}
    info_all["1"] = aa
    info_all["2"] = hall
    info_all["3"] = ed
    info_all["4"] = cp
    return (info_all)

# 陕西
# 秦始皇兵马俑博物馆
def SX_QSHBMYmuseum():
    info_main={}
    url = "https://baike.sogou.com/v4956701.htm?fromTitle=%E7%A7%A6%E5%A7%8B%E7%9A%87%E5%85%B5%E9%A9%AC%E4%BF%91%E5%8D%9A%E7%89%A9%E9%A6%86"
    res = requests.get(url, headers=header)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    name = '秦始皇兵马俑博物馆'

    #print('简介')
    brief = soup.find(attrs={"name": "description"})['content']
    #print(brief)

    #print('博物馆信息')
    visit = soup.find('table', class_='abstract_tbl')
    info0 = visit.find_all('tr')
    for tag0 in info0:
        title0 = tag0.find('th', class_='base-info-card-title')
        #print(title0.text + ":", end="")
        texts = tag0.find('div', class_='base-info-card-value').find(text=True).strip()
        #print(texts)

    #print('电话')
    url_1 = "http://www.bmy.com.cn/html/public/dl/0f082ba612ca4ebc8ffe58958470c487.html"
    hostinfo = get_all(url_1)
    for i in hostinfo.find_all(name='div', attrs={'class': "timeBody"}):
        number = i.text
        #print(number)

    #print('开放时间')
    opentime = "3月16日-11月15日8:30-18:35；11月16日-次年3月15日：8:30-18:05"
    #print(opentime)

    # 地址
    location = "中国 陕西省 西安市"
    info_main["url"] = url
    info_main["name"] = name
    info_main["brief"] = brief
    info_main["location"] = location
    info_main["number"] = number
    info_main["opentime"] = opentime
    aa=[]
    aa.append(info_main)

    #print('展览简介及图片')
    hall=[]
    s={}
    s["ename"] = "兵马俑一号坑---"
    url_2 = "http://www.bmy.com.cn/bmy-websitems-1.0-SNAPSHOT/static/site/public/pages/bmyOne.html"
    hostinfo = get_all(url_2)
    for i in hostinfo.find_all(name='div', attrs={'class': "arcitel"}):
        a = i.text
        s["ds"]=a
        #print(i.text)
    x = get_all(url_2).find(name="div", attrs={'class': 'arcitel'})
    y = x.find_all_next(name="img")
    num = 0
    for i in y:
        url = url_2 + i["src"]
        s["img_src"]=url
        #print(url)
        num = num + 1
        s["emname"] = '秦始皇兵马俑博物馆'
    hall.append(s)

    #print('教育活动')
    ed=[]
    s={}
    s["edname"] = "---1.秦陵博物院走进西电培训志愿者---"
    url_5 = "http://www.bmy.com.cn/html/public/jy/zyzyd/03563dd140d24fa09fd9c62d241fa831.html"
    hostinfo = get_all(url_5)
    for i in hostinfo.find_all(name='div', attrs={'class': "arcitel"}):
        a = i.text
        s["ds"]=a
        #print(i.text)
    s["img_src"]=url_5
    s["time"]="2018.06.07"
    s["edmname"] = '秦始皇兵马俑博物馆'
    ed.append(s)

    #print('博物馆藏品')
    cp=[]
    s={}
    s["cpname"]="秦青铜矛 "
    url_8 = "https://baike.sogou.com/v66752074.htm?fromTitle=%E7%A7%A6%E9%9D%92%E9%93%9C%E9%BC%8E"
    a='秦青铜矛'
    brief1= get_all(url_8).find(attrs={"name": "description"})['content']
    s["ds"]=brief1
    s["img_src"] = url_8
    s["cpmname"] = '秦始皇兵马俑博物馆'
    cp.append(s)
    #print(brief)

    info_all = {}
    info_all["1"] = aa
    info_all["2"] = hall
    info_all["3"] = ed
    info_all["4"] = cp
    return (info_all)

# 延安革命纪念馆
def SX_YAGMmuseum():
    info_main={}
    url = "https://baike.sogou.com/v204544.htm?fromTitle=%E5%BB%B6%E5%AE%89%E9%9D%A9%E5%91%BD%E7%BA%AA%E5%BF%B5%E9%A6%86"
    res = requests.get(url, headers=header)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    name = '延安革命纪念馆'

    #print('简介')
    brief = soup.find(attrs={"name": "description"})['content']
    #print(brief)

    #print('博物馆信息')
    visit = soup.find('table', class_='abstract_tbl')
    info0 = visit.find_all('tr')
    for tag0 in info0:
        title0 = tag0.find('th', class_='base-info-card-title')
        #print(title0.text + ":", end="")
        texts = tag0.find('div', class_='base-info-card-value').find(text=True).strip()
        #print(texts)

    #print('电话')
    url_1 = "http://www.yagmjng.com/rsf/site/jinianguan/825/info/2019/81371.html"
    hostinfo = get_all(url_1)
    for i in hostinfo.find_all('p', attrs={'style': "text-align: left;"}):
        number = i.text
        #print(number)

    #print('开放时间')
    opentime = "8:00~18:00"
    #print(opentime)

    # 地址
    location = "陕西省延安市宝塔区"
    info_main["url"] = url
    info_main["name"] = name
    info_main["brief"] = brief
    info_main["location"] = location
    info_main["number"] = number
    info_main["opentime"] = opentime
    aa=[]
    aa.append(info_main)

    #print('展览简介及图片')
    hall=[]
    s={}
    s["ename"] = "南泥湾革命旧址---"
    url_2 = "http://www.yagmjng.com/rsf/site/jinianguan/zhongdianjieshao/info/2016/81109.html"
    hostinfo = get_all(url_2)
    for i in hostinfo.find_all('span', attrs={'style': "font-size: 16px"}):
        a = i.text
        s["ds"]=a
        #print(i.text)
    x = get_all(url_2).find(name="div", attrs={'id': "zcnr"})
    y = x.find_all_next(name="img")
    num = 0
    for i in y:
        url = url_2 + i["src"]
        s["img_src"]=url
        s["emname"] = '延安革命纪念馆'
        hall.append(s)
        #print(url)
        num = num + 1

    #print('教育活动')
    ed=[]
    s={}
    s["edname"] = "---胡锦涛论延安精神---"
    url_4 = "http://www.yagmjng.com/rsf/site/jinianguan/xuexiyuandi/info/2016/81125.html"
    hostinfo = get_all(url_4)
    for i in hostinfo.find_all('p'):
        a = i.text
        s["ds"]=a
        #print(i.text)
    s["img_src"]=url_4
    s["time"]="2019.06.07"
    s["edmname"] = '延安革命纪念馆'
    ed.append(s)

    #print('博物馆藏品')
    cp=[]
    s={}
    s["cpname"]="毛泽东骑过的马 周恩来穿过的皮大衣 谢子长用过的细瓷碗 任弼时用过的拐杖"
    url_8 = "http://www.yagmjng.com/rsf/site/jinianguan/wenwujianshang/info/2020/81101.html"
    hostinfo = get_all(url_8)
    for i in hostinfo.find_all('p', attrs={'style': "TEXT-ALIGN: center"}):
        a = i.text
        s["ds"]=a
        s["img_src"] = url_8
        #print(i.text)
        s["cpmname"] = '延安革命纪念馆'
        cp.append(s)


        info_all = {}
        info_all["1"] = aa
        info_all["2"] = hall
        info_all["3"] = ed
        info_all["4"] = cp
        return (info_all)


# 汉阳陵博物馆
def SX_HYLmuseum():
    info_main={}
    url = "https://baike.sogou.com/v163140.htm?fromTitle=%E6%B1%89%E9%98%B3%E9%99%B5%E5%8D%9A%E7%89%A9%E9%A6%86"
    res = requests.get(url, headers=header)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    name = '汉阳陵博物馆'

    #print('简介')
    brief = soup.find(attrs={"name": "description"})['content']
    #print(brief)

    #print('博物馆信息')
    visit = soup.find('table', class_='abstract_tbl')
    info0 = visit.find_all('tr')
    for tag0 in info0:
        title0 = tag0.find('th', class_='base-info-card-title')
        #print(title0.text + ":", end="")
        texts = tag0.find('div', class_='base-info-card-value').find(text=True).strip()
        #print(texts)

    #print('联系电话')
    url_1 = "http://www.hylae.com/index.php"
    hostinfo = get_all(url_1)
    for i in hostinfo.find_all(name="div", attrs={'class': "foot_span"}):
        number = i.text
        #print(number)

    #print('开放参观时间')
    hostinfo = get_all(url_1)
    for i in hostinfo.find_all(name="div", attrs={'class': "nr"}):
        opentime = i.text
        #print(opentime)

    # 地址
    location = "中国 陕西省 西安市"
    info_main["url"] = url
    info_main["name"] = name
    info_main["brief"] = brief
    info_main["location"] = location
    info_main["number"] = number
    info_main["opentime"] = opentime
    aa=[]
    aa.append(info_main)

    #print('展览简介及图片')
    hall=[]
    s={}
    s["ename"] = "帝陵外藏坑遗址保护展示厅---"
    url_2 = "http://www.hylae.com/index.php?ac=article&at=read&did=49"
    hostinfo = get_all(url_2)
    for i in hostinfo.find_all(name="div", attrs={'class': "list-right-box"}):
        s["ds"]=i.text
        #print(i.text)
    x = get_all(url_2).find(name="div", attrs={'class': "list-right-box"})
    y = x.find_all_next(name="img")
    num = 0
    for i in y:
        url = url_2 + i["src"]
        s["img_src"]=url
        s["emname"] = '汉阳陵博物馆'
        hall.append(s)
        #print(url)
        num = num + 1

    #print('教育活动')
    ed=[]
    s={}
    s["edname"] = "---互联网+文物教育---"
    url_5 = "http://www.hylae.com/index.php?ac=article&at=read&did=110"
    hostinfo = get_all(url_5)
    for i in hostinfo.find_all(name="div", attrs={'class': "list-right-box"}):
        a = i.text
        s["ds"]=a
        #print(i.text)
    s["img_src"]=url_5
    s["time"]="2019.05.08"
    s["edmname"] = '汉阳陵博物馆'
    ed.append(s)


    #print('博物馆藏品')
    cp=[]
    s={}
    s["cpname"]="兵俑"
    a='着衣式女骑兵俑'
    url_8 = "http://www.hylae.com/index.php?ac=article&at=read&did=62"
    hostinfo = get_all(url_8)
    for i in hostinfo.find_all(name="div", attrs={'class': "list-right-box"}):
        a = i.text
        s["ds"]=a
        s["img_src"] = url_8
        s["cpmname"] = '汉阳陵博物馆'
        cp.append(s)

        info_all = {}
        info_all["1"] = aa
        info_all["2"] = hall
        info_all["3"] = ed
        info_all["4"] = cp
        return (info_all)

# 西安碑林博物馆
def SX_XABLmuseum():
    info_main={}
    url = 'https://baike.sogou.com/v75043022.htm?fromTitle=%E8%A5%BF%E5%AE%89%E7%A2%91%E6%9E%97%E5%8D%9A%E7%89%A9%E9%A6%86'
    res = requests.get(url, headers=header)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    name = '西安碑林博物馆'

    #print('简介')
    brief = soup.find(attrs={"name": "description"})['content']
    #print(brief)

    #print('博物馆信息')
    visit = soup.find('table', class_='abstract_tbl')
    info0 = visit.find_all('tr')
    for tag0 in info0:
        title0 = tag0.find('th', class_='base-info-card-title')
        #print(title0.text + ":", end="")
        texts = tag0.find('div', class_='base-info-card-value').find(text=True).strip()
        #print(texts)

    #print('电话')
    number = ("87210764")
    #print(number)

    #print("开放时间")
    opentime = "8:00-17:30"
    #print(opentime)

    # 地址
    location = "中国 陕西省 西安市"
    info_main["url"] = url
    info_main["name"] = name
    info_main["brief"] = brief
    info_main["location"] = location
    info_main["number"] = number
    info_main["opentime"] = opentime
    aa=[]
    aa.append(info_main)

    #print('展览简介及图片')
    hall=[]
    s={}
    s["ename"] = "西安碑林举办“韩国当代书家书法展”---"
    url_2 = "http://www.beilin-museum.com/contents/17/3677.html"
    hostinfo = get_all(url_2)
    s["ds"]='近日，由西安碑林博物馆和韩国全罗南道文化艺术财团共同举办的“韩国当代书家书法展”在西安'\
          '碑林博物馆东临展室开展，展出韩国全罗南道地区书法家创作的书法作品35件。 展览开幕式上，'\
          '西安碑林博物馆党委书记强跃先生致辞，韩国全罗南道文化艺术财团事务处长郑光德先生发表答谢词'\
          '，韩国全罗南道文化艺术财团代表团5人参加了开幕式。开幕式前还组织了一场中韩书法家书法笔会活动，'\
          '两国书法家现场挥毫，互磋技艺。这次展览是西安碑林博物馆近年来首次与韩国书法界合作，为两国书法家'\
          '提供了了解彼此书法发展特点的交流机会，同时也更为广泛地让韩国民众体会到西安碑林所藏碑石的书法精'\
          '髓与魅力。（西安碑林博物馆  贾梅）'
    x = get_all(url_2).find(name="div", attrs={'class': "content"})
    y = x.find_all_next(name="img")
    num = 0
    for i in y:
        url = url_2 + i["src"]
        s["img_src"]=url
        s["emname"] = '西安碑林博物馆'
        hall.append(s)
        #print(url)
        num = num + 1

    #print('教育活动')
    ed=[]
    s={}
    s["edname"]="西安工业大学等院校的数十名大学生在西安碑林博物馆开展了志愿者暑期服务活动"
    s["ds"]=" 2009年的暑期，对于许多大学生来说具有着特殊的意义。来自西安交通大学、"\
          "西安工业大学等院校的数十名大学生在西安碑林博物馆开展了志愿者暑期服务活动。"\
          "大学生们在碑林博物馆经过有组织的辅导培训，通过自身的努力学习，对古老的碑林不仅有"\
          "了一定的了解与认知，还担当起了义务讲解员的工作。在西安碑林博物馆他们不仅增强了信心"\
          "，锻炼了综合能力，提高了文化素养，同时向社会、向大众传播着中国悠久的历史文化，将自己的所学、"\
          "所想传递给大众，回报予社会。 大学生的暑期志愿服务活动引起了社会的重视与关注，陕西日报、"\
          "陕西电视台、西安电视台等许多媒体对他们进行了采访报道，给他们支持和鼓励，希望他们为将来走出校园"\
          "、步入社会打下坚实的基础。西安碑林博物馆也将继续加强与院校的合作，努力为大学生"\
          "提供锻炼的平台和实践的机会，让更多的大学生接触社会、服务社会、融入社会，以不断扎"\
          "实有效的发挥博物馆社会教育功能。"
    s["img_src"]=""
    s["time"]="2009年的暑期"
    s["edmname"] = '西安碑林博物馆'
    ed.append(s)

    #print('博物馆藏品')
    cp=[]
    s={}
    s["cpname"]="争座位稿 孔子见老子图"
    url_3 = "https://baike.sogou.com/v71598358.htm?fromTitle=%E4%BA%89%E5%BA%A7%E4%BD%8D%E7%A8%BF"
    a='争座位稿'
    brief1 = get_all(url_3).find(attrs={"name": "description"})['content']
    s["ds"]=brief1
    s["img_src"] = url_3
    s["cpmname"] = '西安碑林博物馆'
    cp.append(s)
    #print(brief1)

    info_all = {}
    info_all["1"] = aa
    info_all["2"] = hall
    info_all["3"] = ed
    info_all["4"] = cp
    return (info_all)

# 西安半坡博物馆
def SX_XABPmuseum():
    info_main={}
    url = 'https://baike.sogou.com/v163102.htm?fromTitle=%E8%A5%BF%E5%AE%89%E5%8D%8A%E5%9D%A1%E5%8D%9A%E7%89%A9%E9%A6%86'
    res = requests.get(url, headers=header)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    name = '西安半坡博物馆'

    #print('简介')
    brief = soup.find(attrs={"name": "description"})['content']
    #print(brief)

    #print('博物馆信息')
    visit = soup.find('table', class_='abstract_tbl')
    info0 = visit.find_all('tr')
    for tag0 in info0:
        title0 = tag0.find('th', class_='base-info-card-title')
        #print(title0.text + ":", end="")
        texts = tag0.find('div', class_='base-info-card-value').find(text=True).strip()
        #print(texts)

    #print('联系电话')
    url_1 = "https://bpmuseum.com/index.php?m=content&c=index&a=lists&catid=8"
    hostinfo = get_all(url_1)
    for i in hostinfo.find_all(name="div", attrs={'class': "foot-d-l"}):
        number = i.text
        #print(number)

    #print('开放参观时间')
    hostinfo = get_all(url_1)
    for i in hostinfo.find_all(name="div", attrs={'class': "daodu01-l"}):
        opentime = i.text
        #print(opentime)

    # 地址
    location = "中国 陕西省 西安市"
    info_main["url"] = url
    info_main["name"] = name
    info_main["brief"] = brief
    info_main["location"] = location
    info_main["number"] = number
    info_main["opentime"] = opentime
    aa=[]
    aa.append(info_main)

    #print('展览简介及图片')
    hall=[]
    s={}
    s["ename"] = "西安半坡博物馆举办“屋漏痕——柳明草书展”---"
    url_2 = "https://bpmuseum.com/index.php?m=content&c=index&a=show&catid=38&id=725"
    hostinfo = get_all(url_2)
    for i in hostinfo.find_all(name="div", attrs={'class': "ti"}):
        a = i.text
        s["ds"]=a
        #print(i.text)
    x = get_all(url_2).find(name="div", attrs={'class': "ti"})
    y = x.find_all_next(name="img")
    num = 0
    for i in y:
        url = url_2 + i["src"]
        s["img_src"]=a
        s["emname"] = '西安半坡博物馆'
        hall.append(s)
        #print(url)
        num = num + 1

    #print('教育活动')
    ed=[]
    s={}
    s["edname"] = "---半坡博物馆品牌教育活动走进阎良西飞一小---"
    url_5 = "https://bpmuseum.com/index.php?m=content&c=index&a=show&catid=41&id=640"
    hostinfo = get_all(url_5)
    for i in hostinfo.find_all(name="div", attrs={'class': "ti"}):
        a = i.text
        s["ds"]=a
        s["img_src"]=url_5
        s["time"]="2019.06.08"
        #print(i.text)
        s["edmname"] = '西安半坡博物馆'
    ed.append(s)


    #print('博物馆藏品')
    cp=[]
    s={}
    s["cpname"]="半坡文化三角纹钵 半坡类型彩陶瓶游鱼纹"
    url_7 = "https://baike.sogou.com/v50957908.htm?fromTitle=%E5%8D%8A%E5%9D%A1%E6%96%87%E5%8C%96%E4%B8%89%E8%A7%92%E7%BA%B9%E9%92%B5"
    a='半坡文化三角纹钵'
    brief1 = get_all(url_7).find(attrs={"name": "description"})['content']
    s["ds"]=brief1
    s["img_src"] = url_7
    s["cpmname"] = '西安半坡博物馆'
    cp.append(s)
    #print(brief1)


    info_all = {}
    info_all["1"] = aa
    info_all["2"] = hall
    info_all["3"] = ed
    info_all["4"] = cp
    return (info_all)

# 西安博物院
def SX_XAmuseum():
    info_main={}
    url = 'https://baike.sogou.com/v7115587.htm?fromTitle=%E8%A5%BF%E5%AE%89%E5%8D%9A%E7%89%A9%E9%99%A2'
    res = requests.get(url, headers=header)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    name = '西安博物院'

    #print('简介')
    brief = soup.find(attrs={"name": "description"})['content']
    #print(brief)

    #print('博物馆信息')
    visit = soup.find('table', class_='abstract_tbl')
    info0 = visit.find_all('tr')
    for tag0 in info0:
        title0 = tag0.find('th', class_='base-info-card-title')
        #print(title0.text + ":", end="")
        texts = tag0.find('div', class_='base-info-card-value').find(text=True).strip()
        #print(texts)

    #print('电话')
    number = "029-87803591"
    #print(number)

    opentime = "8:00-17:00"
    #print(opentime)

    # 地址
    location = "中国 陕西省 西安市"
    info_main["url"] = url
    info_main["name"] = name
    info_main["brief"] = brief
    info_main["location"] = location
    info_main["number"] = number
    info_main["opentime"] = opentime
    aa=[]
    aa.append(info_main)

    #print('展览简介及图片')
    hall=[]
    s={}
    s["ename"] = "展览一区---"
    url_2 = "http://www.xabwy.com/Statics/2018.02/1882.html"
    hostinfo = get_all(url_2)
    for i in hostinfo.find_all(name="div", attrs={'id': "shownews_div"}):
        a = i.text
        s["ds"]=a
        #print(i.text)
    x = get_all(url_2).find(name='div', attrs={'id': "shownews_div"})
    y = x.find_all_next(name="img")
    num = 0
    for i in y:
        url = url_2 + i["src"]
        s["img_src"]=url
        s["emname"] = '西安博物院'
        hall.append(s)
        #print(url)
        num = num + 1

    #print('教育活动')
    ed=[]
    s={}
    s["edname"] = "---西安博物院参加“博物馆校园大讲堂公益巡讲”系列活动---"
    url_3 = "http://www.xabwy.com/Statics/2018.02/2590.html"
    hostinfo = get_all(url_3)
    for i in hostinfo.find_all(name="div", attrs={'id': "shownews_div"}):
        a = i.text
        s["ds"]=a
        s["img_src"]=url_3
        s["time"]="2017年9月27日"
        s["edmname"] = '西安博物院'
        ed.append(s)
        #print(i.text)


    #print('博物馆藏品')
    cp=[]
    s={}
    s["cpname"]="鎏金翼兽纹五足铜炉台 三彩腾空马"
    url_7 = "https://baike.sogou.com/v172064472.htm?fromTitle=%E9%8E%8F%E9%87%91%E7%BF%BC%E5%85%BD%E7%BA%B9%E4%BA%94%E8%B6%B3%E9%93%9C%E7%82%89%E5%8F%B0"
    a='鎏金翼兽纹五足铜炉台'
    brief1 = get_all(url_7).find(attrs={"name": "description"})['content']
    s["ds"]=brief1
    s["img_src"] = url_7
    s["cpmname"] = '西安博物院'
    cp.append(s)
    #print(brief1)

    info_all = {}
    info_all["1"] = aa
    info_all["2"] = hall
    info_all["3"] = ed
    info_all["4"] = cp
    return (info_all)


# 宝鸡青铜器博物院
def SX_BJQTmuseum():
    info_main={}
    url = 'https://baike.sogou.com/v35175447.htm?fromTitle=%E5%AE%9D%E9%B8%A1%E9%9D%92%E9%93%9C%E5%99%A8%E5%8D%9A%E7%89%A9%E9%99%A2'
    res = requests.get(url, headers=header)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    name = '宝鸡青铜器博物院'

    #print('简介')
    brief = soup.find(attrs={"name": "description"})['content']
    #print(brief)

    #print('博物馆信息')
    visit = soup.find('table', class_='abstract_tbl')
    info0 = visit.find_all('tr')
    for tag0 in info0:
        title0 = tag0.find('th', class_='base-info-card-title')
        #print(title0.text + ":", end="")
        texts = tag0.find('div', class_='base-info-card-value').find(text=True).strip()
        #print(texts)

    #print('电话')
    url_1 = "http://www.bjqtm.com/"
    hostinfo = get_all(url_1)
    for i in hostinfo.find_all(name="div", attrs={'class': "f_adress fl"}):
        number = i.text
        #print(number)

    #print('开放参观时间')
    hostinfo = get_all(url_1)
    for i in hostinfo.find_all(name="div", attrs={'class': "top_sum_left fl"}):
        opentime = i.text
        #print(opentime)

    # 地址
    location = "中国 陕西省 宝鸡市"
    info_main["url"] = url
    info_main["name"] = name
    info_main["brief"] = brief
    info_main["location"] = location
    info_main["number"] = number
    info_main["opentime"] = opentime
    aa=[]
    aa.append(info_main)

    #print('展览简介及图片')
    hall=[]
    s={}
    s["ename"] = "陶语诉春秋——古代陶瓷与文化生活展---"
    url_2 = "http://www.bjqtm.com/index.php?ac=article&at=read&did=227"
    x = get_all(url_2).find(name='div', attrs={'class': "p"})
    y = x.find_all_next(name="img")
    num = 0
    for i in y:
        url = url_2 + i["src"]
        s["img_src"]=url
        #print(url)
        num = num + 1
    hostinfo = get_all(url_2)
    for i in hostinfo.find_all(name="div", attrs={'class': "p"}):
        a = i.text
        s["ds"]=a
        s["emname"] = '宝鸡青铜器博物院'
        hall.append(s)
        #print(i.text)

    #print('教育活动')
    ed=[]
    s={}
    s["edname"]="宝鸡青铜器博物院与宝鸡市残联在中华石鼓园隆重举行第五届“养成健身习惯，享受健康生活”残疾人健身周活动"
    url_4 = "http://www.bjqtm.com/index.php?ac=article&at=read&did=247"
    hostinfo = get_all(url_4)
    for i in hostinfo.find_all(name="div", attrs={'class': "p"}):
        a = i.text
        s["ds"]=a
        s["img_src"]=url_4
        s["time"]="8月11日上午"
        s["edmname"] = '宝鸡青铜器博物院'
        ed.append(s)
        #print(i.text)


    #print('博物馆藏品')
    cp=[]
    s={}
    s["cpname"]="夨伯鬲 虢仲鬲 凤鸟纹方座簋"
    a='夨伯鬲'
    url_6 = "http://www.bjqtm.com/index.php?ac=article&at=read&did=282"
    hostinfo = get_all(url_6)
    for i in hostinfo.find_all(name="div", attrs={'class': "p"}):
        a = i.text
        s["ds"]=a
        s["img_src"] = url_6
        s["cpmname"] = '宝鸡青铜器博物院'
        cp.append(s)
        #print(i.text)


    info_all = {}
    info_all["1"] = aa
    info_all["2"] = hall
    info_all["3"] = ed
    info_all["4"] = cp
    return (info_all)

# 西安大唐西市博物馆
def SX_XADTXSmuseum():
    info_main={}
    url = 'https://baike.sogou.com/v83755867.htm?fromTitle=%E8%A5%BF%E5%AE%89%E5%A4%A7%E5%94%90%E8%A5%BF%E5%B8%82%E5%8D%9A%E7%89%A9%E9%A6%86'
    res = requests.get(url, headers=header)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    name = '西安大唐西市博物馆'

    #print('简介')
    brief = soup.find(attrs={"name": "description"})['content']
    #print(brief)

    #print('博物馆信息')
    visit = soup.find('table', class_='abstract_tbl')
    info0 = visit.find_all('tr')
    for tag0 in info0:
        title0 = tag0.find('th', class_='base-info-card-title')
        #print(title0.text + ":", end="")
        texts = tag0.find('div', class_='base-info-card-value').find(text=True).strip()
        #print(texts)

    #print('电话')
    url_1 = "http://www.dtxsmuseum.com/index.aspx"
    hostinfo = get_all(url_1)
    for i in hostinfo.find_all(name="div", attrs={'style': "width:660px; float:left;"}):
        number = i.text
        #print(number)

    #print('开放参观时间')
    opentime = " 全年开放（每周一及除夕闭馆，法定节假日正常开放）"
    #print(opentime)

    # 地址
    location = "中国 陕西省 西安市"
    info_main["url"] = url
    info_main["name"] = name
    info_main["brief"] = brief
    info_main["location"] = location
    info_main["number"] = number
    info_main["opentime"] = opentime
    aa=[]
    aa.append(info_main)

    #print('展览简介及图片')
    hall=[]
    s={}
    s["ename"] = "国庆献礼：“盛世遗珍——大唐西市博物馆藏精品面面观”---"
    url_2 = "http://www.dtxsmuseum.com/news_show.aspx?id=1114"
    x = get_all(url_2).find(name='div', attrs={'class': "news-content"})
    y = x.find_all_next(name="img")
    num = 0
    for i in y:
        url = url_2 + i["src"]
        s["img_src"]=url
        #print(url)
        num = num + 1
    hostinfo = get_all(url_2)
    for i in hostinfo.find_all(name="div", attrs={'class': "news-content"}):
        a=i.text
        s["ds"]=a
        s["emname"] = '西安大唐西市博物馆'
        hall.append(s)
        #print(i.text)

    #print('教育活动')
    ed=[]
    s={}
    s["edname"] = "---大唐西市博物馆首期“丝路小小讲解员”培训班成功举办---"
    url_5 = "http://www.dtxsmuseum.com/news_show.aspx?id=1074"
    hostinfo = get_all(url_5)
    for i in hostinfo.find_all(name="div", attrs={'class': "news-content"}):
        a = i.text
        s["ds"]=a
        s["img_src"]=url_5
        s["time"]="2018年1月28日"
        s["edmname"] = '西安大唐西市博物馆'
        ed.append(s)
        #print(i.text)

    #print('博物馆藏品')
    cp=[]
    s={}
    s["cpname"]="道路与车辙遗迹 古井遗址"
    a='道路与车辙遗迹'
    url_7 = "http://www.dtxsmuseum.com/news_show.aspx?id=624"
    hostinfo = get_all(url_7)
    for i in hostinfo.find_all(name="div", attrs={'class': "news-content"}):
        a = i.text
        s["ds"]=a
        s["img_src"] = url_7
        s["cpmname"] = '西安大唐西市博物馆'
        cp.append(s)
        #print(i.text)


    info_all = {}
    info_all["1"] = aa
    info_all["2"] = hall
    info_all["3"] = ed
    info_all["4"] = cp

    return (info_all)

# 甘肃
#甘肃省博物馆
def GS_GSSmuseum():
    info_main={}
    url = 'https://baike.sogou.com/v154956.htm?fromTitle=%E7%94%98%E8%82%83%E7%9C%81%E5%8D%9A%E7%89%A9%E9%A6%86'
    res = requests.get(url, headers=header)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    name = '甘肃省博物馆'

    #print('简介')
    brief = soup.find(attrs={"name": "description"})['content']
    #print(brief)

    #print('博物馆信息')
    visit = soup.find('table', class_='abstract_tbl')
    info0 = visit.find_all('tr')
    for tag0 in info0:
        title0 = tag0.find('th', class_='base-info-card-title')
        #print(title0.text + ":", end="")
        texts = tag0.find('div', class_='base-info-card-value').find(text=True).strip()
        #print(texts)

    #print('电话')
    number = "（0931）2339131 、2339133"
    #print(number)

    #print('开放参观时间')
    opentime = "每星期二至星期日 9：00—17：00（16：00停止入馆）；星期一闭馆（除国家法定节假日外）"
    #print(opentime)

    # 地址
    location = "甘肃省兰州市七里河区西津西路3号"
    info_main["url"] = url
    info_main["name"] = name
    info_main["brief"] = brief
    info_main["location"] = location
    info_main["number"] = number
    info_main["opentime"] = opentime
    aa=[]
    aa.append(info_main)

    #print('展览简介及图片')
    hall=[]
    s={}
    s["ename"] = "黄河之滨也很美——兰州的前世今生---"
    url_2 = "http://www.gansumuseum.com/zl/show-52.html"
    hostinfo = get_all(url_2)
    for i in hostinfo.find_all(name="div", attrs={'class': "inner"}):
        a=i.text
        s["ds"]=a
        #print(i.text)
    x = get_all(url_2).find(name="div", attrs={'class': "inner"})
    y = x.find_all_next(name="img")
    num = 0
    for i in y:
        url = url_2 + i["src"]
        s["img_src"]=url
        s["emname"] = '甘肃省博物馆'
        hall.append(s)
        #print(url)
        num = num + 1

    #print('教育活动')
    ed=[]
    s={}
    s["edname"]="甘肃省博物馆馆长贾建威向敦煌路小学颁发了“中华传统文化传承实践基地” 牌匾"
    url_4 = "http://www.gansumuseum.com/news/show-2477.html"
    hostinfo = get_all(url_4)
    for i in hostinfo.find_all(name="div", attrs={'class': "inner"}):
        a = i.text
        s["ds"]=a
        s["img_src"]=url_4
        s["time"]="2018.02.06"
        s["edmname"] = '甘肃省博物馆'
        ed.append(s)
        #print(i.text)

    #print('博物馆藏品')
    cp=[]
    s={}
    s["cpname"]="嘉靖款汤镇造金碗 镶宝石桃形镂孔金头银柄簪"
    url_5 = "http://www.gansumuseum.com/dc/show-316.html"
    hostinfo = get_all(url_5)
    for i in hostinfo.find_all(name="div", attrs={'class': "inner"}):
        a = i.text
        s["ds"]=a
        s["img_src"] = url_5
        s["cpmname"] = '甘肃省博物馆'
        cp.append(s)
        #print(i.text)


    info_all = {}
    info_all["1"] = aa
    info_all["2"] = hall
    info_all["3"] = ed
    info_all["4"] = cp


# 天水市博物馆
def GS_TSSmuseum():
    info_main={}
    url = 'https://baike.sogou.com/v63174578.htm?fromTitle=%E5%A4%A9%E6%B0%B4%E5%B8%82%E5%8D%9A%E7%89%A9%E9%A6%86'
    res = requests.get(url, headers=header)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    name = '天水市博物馆'

    #print('简介')
    brief = soup.find(attrs={"name": "description"})['content']
    #print(brief)

    #print('博物馆信息')
    visit = soup.find('table', class_='abstract_tbl')
    info0 = visit.find_all('tr')
    for tag0 in info0:
        title0 = tag0.find('th', class_='base-info-card-title')
        #print(title0.text + ":", end="")
        texts = tag0.find('div', class_='base-info-card-value').find(text=True).strip()
        #print(texts)

    #print('电话')
    url_1 = "http://www.tssbwg.com.cn/"
    hostinfo = get_all(url_1)
    for i in hostinfo.find_all(name="div", attrs={'align': "center", 'class': 'STYLE2 STYLE1'}):
        number = i.text
        #print(number)

    opentime = "每天上午8:00 - 12:00；下午 14:00 - 18:00 开放"
    #print(opentime)

    # 地址
    location = "中国 甘肃省 天水市"
    info_main["url"] = url
    info_main["name"] = name
    info_main["brief"] = brief
    info_main["location"] = location
    info_main["number"] = number
    info_main["opentime"] = opentime
    aa=[]
    aa.append(info_main)

    #print('展览简介及图片')
    hall=[]
    s={}
    s["ename"] = "国庆献礼：“盛世遗珍——大唐西市博物馆藏精品面面观”---"
    url_2 = "http://www.tssbwg.com.cn/html/2020/czxc_0109/4138.html"
    x = get_all(url_2).find('span', attrs={'class': "STYLE56"})
    y = x.find_all_next(name="img")
    num = 0
    for i in y:
        url = url_2 + i["src"]
        s["img_src"]=url
        #print(url)
        num = num + 1
    s["ds"]='这次展览由天水市文学艺术界联合会和天水市博物馆主办，天水市艺术研究院、'\
          '天水民俗博物馆、天水市书法家协会、天水市美术家协会承办，展期1个月，'\
          '展览地点在天水民俗博物馆北宅子。展览展出的60幅作品出自蔡晓斌、焦全、'\
          '王一潮、张升、赵世峰、颉自强6位天水书画艺术家之手。他们的作品均于今年'\
          '入选第十二届中国书法篆刻作品展和第十三届全国美术作品展。这些作品通过不'\
          '同的艺术风格，展现了新时代天水书画艺术的新风貌，弘扬了社会主义核心价值观'\
          '，进一步展现了文化自信。'
    s["emname"] = '天水市博物馆'
    hall.append(s)

    # 教育活动无
    ed = []
    s = {}
    s["edname"] = ""
    s["ds"] = ""
    s["img_src"] = ""
    s["time"] = ""
    s["edmname"] = '天水市博物馆'
    ed.append(s)

    #print('博物馆藏品')
    cp=[]
    s={}
    s["cpname"]="天王俑 唐海兽葡萄纹铜镜 "
    url_7 = "https://baike.sogou.com/v73281744.htm?fromTitle=%E5%A4%A9%E7%8E%8B%E4%BF%91"
    a='天王俑'
    brief1 = get_all(url_7).find(attrs={"name": "description"})['content']
    s["ds"]=brief1
    s["img_src"] = url_7
    s["cpmname"] = '天水市博物馆'
    cp.append(s)
    #print(brief1)


    info_all = {}
    info_all["1"] = aa
    info_all["2"] = hall
    info_all["3"] = ed
    info_all["4"] = cp
    return (info_all)


# 敦煌研究院
def GS_DHmuseum():
    info_main={}
    url = 'https://baike.sogou.com/v6564635.htm?fromTitle=%E6%95%A6%E7%85%8C%E7%A0%94%E7%A9%B6%E9%99%A2'
    res = requests.get(url, headers=header)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    name = '敦煌研究院'

    #print('简介')
    brief = soup.find(attrs={"name": "description"})['content']
    #print(brief)

    #print('博物馆信息')
    visit = soup.find('table', class_='abstract_tbl')
    info0 = visit.find_all('tr')
    for tag0 in info0:
        title0 = tag0.find('th', class_='base-info-card-title')
        #print(title0.text + ":", end="")
        texts = tag0.find('div', class_='base-info-card-value').find(text=True).strip()
        #print(texts)

    #print('电话：')
    number = ('0937-8869852')
    #print(number)

    #print('开放参观时间')
    opentime = ('旺　季：5月1日至10月31日：8:00— 18:00 '
                ' 淡　季：11月1日至4月30日：9:00 —17:30')
    #print(opentime)

    # 地址
    location = "敦煌莫高窟"
    info_main["url"] = url
    info_main["name"] = name
    info_main["brief"] = brief
    info_main["location"] = location
    info_main["number"] = number
    info_main["opentime"] = opentime
    aa=[]
    aa.append(info_main)

    #print('展览简介及图片')
    hall=[]
    s={}
    s["ename"] = "敦煌莫高窟洞窟---"
    url_4 = "http://public.dha.ac.cn/content.aspx?id=353908940100"
    hostinfo = get_all(url_4)
    for i in hostinfo.find_all('p', attrs={'style': "text-align: center; line-height: 3em;"}):
        a = i.text
        s["ds"]=a
        #print(i.text)
    x = get_all(url_4).find('p', attrs={'style': "text-align: center; line-height: 3em;"})
    y = x.find_all_next(name="img")
    num = 0
    for i in y:
        url = url_4 + i["src"]
        s["img_src"]=a
        s["emname"] = '敦煌研究院'
        hall.append(s)
        #print(url)
        num = num + 1

    #print('教育活动')
    ed=[]
    s={}
    s["edname"] = "---博物馆之旅 体验的快乐——《敦煌石窟壁画临摹体验》---"
    url_5 = "http://public.dha.ac.cn/content.aspx?id=676881787237"
    hostinfo = get_all(url_5)
    for i in hostinfo.find_all('p', attrs={'style': "LINE-HEIGHT: 3em"}):
        a = i.text
        s["ds"]=a
        s["img_src"]="url_5"
        s["time"]="2018.05.06"
        s["edmname"] = '敦煌研究院'
        ed.append(s)
        #print(i.text)

    #print('博物馆藏品')
    cp=[]
    s={}
    s["cpname"]="刺绣佛像供养人 彩绘影塑供养菩萨像"
    url_8 = "https://baike.sogou.com/v169050385.htm?fromTitle=%E5%88%BA%E7%BB%A3%E4%BD%9B%E5%83%8F%E4%BE%9B%E5%85%BB%E4%BA%BA"
    a='刺绣佛像供养人'
    brief1 = get_all(url_8).find(attrs={"name": "description"})['content']
    s["ds"]=a
    s["img_src"] = url_8
    s["cpmname"] = '敦煌研究院'
    cp.append(s)
    #print(brief1)


    info_all = {}
    info_all["1"] = aa
    info_all["2"] = hall
    info_all["3"] = ed
    info_all["4"] = cp
    return (info_all)



# 宁夏
# 固原博物馆
def NX_GYmuseum():
    info_main={}
    url = 'https://baike.sogou.com/v157256.htm?fromTitle=%E5%9B%BA%E5%8E%9F%E5%8D%9A%E7%89%A9%E9%A6%86'
    res = requests.get(url, headers=header)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    name = '固原博物馆'

    #print('简介')
    brief = soup.find(attrs={"name": "description"})['content']
    #print(brief)

    #print('博物馆信息')
    visit = soup.find('table', class_='abstract_tbl')
    info0 = visit.find_all('tr')
    for tag0 in info0:
        title0 = tag0.find('th', class_='base-info-card-title')
        #print(title0.text + ":", end="")
        texts = tag0.find('div', class_='base-info-card-value').find(text=True).strip()
        #print(texts)

    #print('电话')
    url_1 = "http://www.nxgybwg.com/"
    hostinfo = get_all(url_1)
    for i in hostinfo.find_all(name='div', attrs={'class': "footer_addl"}):
        number = i.text
        #print(number)

    #print('开放参观时间')
    for i in hostinfo.find_all(name='div', attrs={'class': "section_tit"}):
        opentime = i.text
        #print(opentime)

    # 地址
    location = "中国 宁夏省 固原市"
    info_main["url"] = url
    info_main["name"] = name
    info_main["brief"] = brief
    info_main["location"] = location
    info_main["number"] = number
    info_main["opentime"] = opentime
    aa=[]
    aa.append(info_main)

    #print('展览简介及图片')
    hall=[]
    s={}
    s["ename"] = "宁夏固原博物馆基本陈列的主题及展品说明---"
    url_2 = "http://www.nxgybwg.com/e/action/ShowInfo.php?classid=13&id=160"
    hostinfo = get_all(url_2)
    for i in hostinfo.find_all(name='div', attrs={'class': "contents"}):
        a=i.text
        s["ds"]=a
        #print(i.text)
    x = get_all(url_2).find(name="div", attrs={'class': 'contents'})
    y = x.find_all_next(name="img")
    num = 0
    for i in y:
        url = url_2 + i["src"]
        s["img_src"]=url
        s["emname"] = '固原博物馆'
        hall.append(s)
        #print(url)
        num = num + 1

    #print('教育活动')
    ed=[]
    s={}
    s["edname"] = "---固原博物馆开展2019年宪法宣传日系列活动----"
    url_5 = "http://www.nxgybwg.com/e/action/ShowInfo.php?classid=34&id=473"
    hostinfo = get_all(url_5)
    for i in hostinfo.find_all(name='div', attrs={'class': "contents"}):
        a = i.text
        s["ds"]=a
        s["img_src"]=url_5
        s["time"]="2019.04.08"
        s["edmname"] = '固原博物馆'
        ed.append(s)
        #print(i.text)

    #print('博物馆藏品')
    cp=[]
    s={}
    s["cpname"]="棺侧板漆画 琉璃碗 鎏金银壶"
    a='棺侧板漆画 '
    url_7 = "http://www.nxgybwg.com/e/action/ShowInfo.php?classid=47&id=346"
    hostinfo = get_all(url_7)
    for i in hostinfo.find_all(name='div', attrs={'class': "contents"}):
        a=i.text
        s["ds"]=a
        s["img_src"] = url_7
        s["cpmname"] = '固原博物馆'
        cp.append(s)
        #print(i.text)


        info_all = {}
        info_all["1"] = aa
        info_all["2"] = hall
        info_all["3"] = ed
        info_all["4"] = cp
        return (info_all)


# 宁夏博物馆
def NX_NXmuseum():
    info_main={}
    url = 'https://baike.sogou.com/v157244.htm?fromTitle=%E5%AE%81%E5%A4%8F%E5%8D%9A%E7%89%A9%E9%A6%86'
    res = requests.get(url, headers=header)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    name = '宁夏博物馆'

    #print('简介')
    brief = soup.find(attrs={"name": "description"})['content']
    #print(brief)

    #print('博物馆信息')
    visit = soup.find('table', class_='abstract_tbl')
    info0 = visit.find_all('tr')
    for tag0 in info0:
        title0 = tag0.find('th', class_='base-info-card-title')
        #print(title0.text + ":", end="")
        texts = tag0.find('div', class_='base-info-card-value').find(text=True).strip()
        #print(texts)

    #print('电话')
    number = "023-8769543"
    #print(number)

    #print('开放参观时间')
    opentime = "8:00-17:00"
    #print(opentime)

    # 地址
    location = "中国 宁夏省 银川市"
    info_main["url"] = url
    info_main["name"] = name
    info_main["brief"] = brief
    info_main["location"] = location
    info_main["number"] = number
    info_main["opentime"] = opentime
    aa = []
    aa.append(info_main)

    #print('展览简介及图片')
    hall=[]
    s={}
    s["ename"] = "悠然心会——王成国画作品展---"
    url_2 = "https://www.nxbwg.com/a/90.html"
    hostinfo = get_all(url_2)
    for i in hostinfo.find_all(name='div', attrs={'class': "article-text"}):
        a = i.text
        s["ds"]=a
        #print(i.text)
    x = get_all(url_2).find(name="div", attrs={'class': 'article-text'})
    y = x.find_all_next(name="img")
    num = 0
    for i in y:
        url = url_2 + i["src"]
        s["img_src"]=url
        s["emname"] = '宁夏博物馆'
        hall.append(s)
        #print(url)
        num = num + 1

    #print('教育活动')
    ed=[]
    s={}
    s["edname"] = "---宁夏博物馆2019年寒假小小志愿者讲解员引人注目---"
    url_5 = "https://www.nxbwg.com/a/92.html"
    hostinfo = get_all(url_5)
    for i in hostinfo.find_all(name='div', attrs={'class': "article-text"}):
        a = i.text
        s["ds"]=a
        s["img_src"]=url_5
        s["time"]="2020.1.2"
        s["edmname"] = '宁夏博物馆'
        ed.append(s)
        #print(i.text)

    #print('博物馆藏品')
    cp=[]
    s={}
    s["cpname"]="豆荚纹双耳彩陶壶 偏颈鸭形彩陶壶 绿玉凿"
    a='豆荚纹双耳彩陶壶'
    url_7 = "https://www.nxbwg.com/a/143.html"
    hostinfo = get_all(url_7)
    for i in hostinfo.find_all(name='div', attrs={'class': "article-text"}):
        a = i.text
        s["ds"]=a
        s["img_src"] = url_7
        s["cpmname"] = '宁夏博物馆'
        cp.append(s)
        #print(i.text)

        info_all = {}
        info_all["1"] = aa
        info_all["2"] = hall
        info_all["3"] = ed
        info_all["4"] = cp
        return (info_all)


# 新疆
# 新疆维吾尔自治区博物馆
def XJ_XJWWEZZQmuseum():
    info_main={}
    url = 'https://baike.sogou.com/v163130.htm?fromTitle=%E6%96%B0%E7%96%86%E7%BB%B4%E5%90%BE%E5%B0%94%E8%87%AA%E6%B2%BB%E5%8C%BA%E5%8D%9A%E7%89%A9%E9%A6%86'
    res = requests.get(url, headers=header)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    name = '新疆维吾尔自治区博物馆'

    #print('简介')
    brief = soup.find(attrs={"name": "description"})['content']
    #print(brief)

    #print('博物馆信息')
    visit = soup.find('table', class_='abstract_tbl')
    info0 = visit.find_all('tr')
    for tag0 in info0:
        title0 = tag0.find('th', class_='base-info-card-title')
        #print(title0.text + ":", end="")
        texts = tag0.find('div', class_='base-info-card-value').find(text=True).strip()
        #print(texts)

    #print('电话：')
    number = ('0991-4533561')
    #print(number)

    #print('开放参观时间:')
    opentime = ('每周二至周日的10：30—18：00')
    #print(opentime)

    # 地址
    location = "中国 新疆"
    info_main["url"] = url
    info_main["name"] = name
    info_main["brief"] = brief
    info_main["location"] = location
    info_main["number"] = number
    info_main["opentime"] = opentime
    aa = []
    aa.append(info_main)


    hall=[]
    s={}
    s["ename"]="“新疆古代历史文物陈列，”反映了新疆历史发展的概貌和丰富的内涵，"
    s["ds"] ='展览简介：（1）“新疆古代历史文物陈列，”反映了新疆历史发展的概貌和丰富的内涵，'\
          '同时对新疆民族特点、地方特色和“丝绸之路”作了应有的展示。展出的文物有完好的陶器，'\
          '精美的玉器，栩栩如生的泥俑，色泽艳丽的织物，举世罕见的简牍，种类繁多的石器，铜器，'\
          '铁器，以及1000多件辅助展品，充分反映了新疆各个历史时期、发展时期的进程。'\
          '（2）“新疆民族民俗陈列”，通过居住在新疆的12个少数民族的建筑艺术,生产工具，'\
          '服饰，生活及文化用品等，形象地表现了新疆各民族的民俗民风。（3）“新疆古尸陈列”，'\
          ' 陈列的古尸达21具，展出有保存最好，最完整的距今4000年的“楼兰美女”、'\
          '具有欧罗巴人特征的距今3200年的哈密的女尸，身材高大、体形健美的且末男尸，'\
          '身着艳丽服饰的且末女尸，举世罕见的且末婴尸；2500年前的苏贝希干尸的及唐高昌左卫将军张雄干尸等。'\
          '同时还对新疆具有代表性的古墓葬进行了复原展出。（4）“新疆革命文物史料展览”展示了为新疆和平解放'\
          '而英勇献身的革命志士可歌可泣的英勇事迹。（5）“拯救中华古机械国宝展览”；展出了1000多年前'\
          '的鲁班木车马及诸葛亮木牛流马等大型古代出行机械奇器模型，充分反映了中华民族聪明的才智和高超的'\
          '智慧。'
    s["img_src"]=url
    s["emname"] = '新疆维吾尔自治区博物馆'
    hall.append(s)

    # print('教育活动无')
    ed = []
    s = {}
    s["edname"] = ""
    s["ds"] = ""
    s["img_src"] = ""
    s["time"] = ""
    s["edmname"] = '新疆维吾尔自治区博物馆'
    ed.append(s)

    #print('博物馆藏品')
    cp=[]
    s={}
    s["cpname"]="楼兰女尸"
    url_8 = "https://baike.sogou.com/v862433.htm?fromTitle=%E6%A5%BC%E5%85%B0%E5%A5%B3%E5%B0%B8"
    a='楼兰女尸'
    brief1 = get_all(url_8).find(attrs={"name": "description"})['content']
    s["ds"]=brief1
    s["img_src"] = url_8
    s["cpmname"] = '新疆维吾尔自治区博物馆'
    cp.append(s)
    #print(brief)

    info_all = {}
    info_all["1"] = aa
    info_all["2"] = hall
    info_all["3"] = ed
    info_all["4"] = cp
    return (info_all)

if __name__ == '__main__':
    #x1=SC_ZGKLmuseum()
    #save_data(x1)
    #x2=SC_SXDmuseum()
    #save_data(x2)
    #x3=SC_CDWHCmuseum()
    #save_data(x3)
    #x4=SC_DXPGJmuseum()
    #save_data(x4)
    #x5=SC_CDDFCTmuseum()
    #save_data(x5)
    #x6=SC_SCmuseum()
    #save_data(x6)
    #x7=SC_CDJSJmuseum()
    #save_data(x7)
    #x8=SC_ZGYYmuseum()
    #save_data(x8)
    #x9=GZ_ZYHYmuseum()
    #save_data(x9)
    #x10=YN_YNmuseum()
    #save_data(x10)
    ##x11=YN_YNMZmuseum()  有问题。。。
    ##save_data(x11)
    #x12=CQ_CQSXmuseum()
    #save_data(x12)
    #x13=CQ_CQZRmuseum()
    #save_data(x13)
    #x14=SX_QSHBMYmuseum()
    #save_data(x14)
    #x15=SX_BJQTmuseum()
    #save_data(x15)
    ##x16=SX_XAmuseum()  无响应。。。。
    ##save_data(x16)
    #x17=SX_YAGMmuseum()
    #save_data(x17)
    #x18=SX_HYLmuseum()
    #save_data(x18)
    #x19=SX_XABLmuseum()
    #save_data(x19)
    #x20=SX_XABPmuseum()
    #save_data(x20)
    #x21=SX_XADTXSmuseum()
    #save_data(x21)
    ##x22=GS_GSSmuseum()   有问题。。。。
    ##save_data(x22)
    #x23=GS_TSSmuseum()
    #save_data(x23)
    #x24=GS_DHmuseum()
    #save_data(x24)
    #x25=NX_GYmuseum()
    #save_data(x25)
    #x26=NX_NXmuseum()
    #save_data(x26)
    #x27=XJ_XJWWEZZQmuseum()
    #save_data(x27)