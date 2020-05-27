import requests
import bs4
import re
from bs4 import BeautifulSoup
import bs4
import pymysql

headers ={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0'
    }

#全局变量
global mid,eid,oid
mid = int(0)
eid = int(0)
oid = int(0)

museum_info = {}

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
    def insert(self,dict1):
        global mid,eid,oid
        # 将数据添加到数据库中的movie表中
        sql_1 = "insert into museums(name,imgurl,mobile,address,introduction,opentime) values(%s,%s,%s,%s,%s,%s)"
        for i in dict1["1"]:    
            data_1 = [i["name"],i["img"],i['number'],i['location'],i['description'],i['opentime']]
            try:
                 self.cursor.execute(sql_1,data_1)
                 self.db.commit() # 提交操作
            except:
                 self.db.rollback()
        sql_2 = "insert into exhibitions(name,imgurl,introduction,mname) values(%s,%s,%s,%s)"
        for i in dict1["2"]:
            data_2 = [i["name"],i["img"],i['description'],i["mname"]]
            try:
                self.cursor.execute(sql_2,data_2)
                self.db.commit() # 提交操作
            except:
                self.db.rollback()

        sql_3 = "insert into collections(name,imgurl,introduction,mname) values(%s,%s,%s,%s)"
        for i in dict1["3"]:
            data_3 = [i["name"],i["img"],i['description'],i["mname"]]
            try:
                self.cursor.execute(sql_3,data_3)
                self.db.commit() # 提交操作
            except:
                self.db.rollback()

        sql_4 = "insert into educations(name,imgurl,introduction,time,mname) values(%s,%s,%s,%s,%s)"
        for i in dict1["4"]:
            data_4 = [i["name"],i["img"],i['description'],i['time'],i["mname"]]
            try:
                self.cursor.execute(sql_4,data_4)
                self.db.commit() # 提交操作
            except:
                self.db.rollback()

        self.db.close()
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
    print("数据保存")

def get_text(url):
    try:
        res = requests.get(url)
        res.raise_for_status()
        res.encoding = res.apparent_encoding
        return res.text
    except:
        return ""

def get_soup(url):
    text = get_text(url)
    soup = BeautifulSoup(text,"html.parser")
    return soup

def get_soup1(url):
    res = requests.get(url,headers = headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text,"html.parser")
    return soup

def get_brief(url):
    brief  ={}
    soup = get_soup1(url)
    print("------博物馆简介------")
    brief = soup.find('div',id = 'j-shareAbstract',style = 'display: none')
    description = brief.text
    brief["description"] = description 
    #print(description)
    div = soup.find('div',attrs={'class':'abstract_main'})
    img = div.find('img',attrs={'width':'250'})
    src = img["src"]
    print("------参观信息------")
    visit = soup.find('table',class_ ='abstract_tbl')
    info = visit.find_all('tr')
    #for tag in info:
        #title = tag.find('th',class_ = 'base-info-card-title')
        #print(title.text+":",end="")
        #texts = tag.find('div',class_ = 'base-info-card-value').find(text=True).strip()
        #print(texts)
    brief["name"] = "青州博物馆"
    brief["img"] = src
    brief["location"] = "山东省青州市范公亭西路1号"
    brief["number"] = "咨询电话：0536-3266200"
    brief["opentime"] = "每天9：00-16：30（16：00停止入馆），每周一全天闭馆（国家法定节假日除外）" 
    return brief

def show(url):
    exhibition = {}
    home = "http://bowuguan.qingzhou.gov.cn/zl/"
    soup = get_soup(url)
    title = soup.find('td',attrs={'height':'80'})
    exhibition["name"] = title.text
    #print(title.text)
    td = soup.find('div',attrs={'class':'TRS_Editor'})
    main = ""
    p = td.find_all('p')
    for tag in p:
        main = main+tag.text
    #print(main)
    exhibition["description"] = main
    a = td.find('a')
    src = home +a["href"]
    #print("展览图示:"+src)
    exhibition["img"] = src
    exhibition["mname"] = "青州博物馆"
    return exhibition

def object(url):
    collection = {}
    home = "http://bowuguan.qingzhou.gov.cn/zl/"
    soup = get_soup(url)
    title = soup.find('td',attrs={'height':'80'})
    collection["name"] = title.text
    #print(title.text)
    td = soup.find('div',attrs={'class':'TRS_Editor'})
    main = ""
    p = td.find_all('p')
    for tag in p:
        main = main+tag.text
    #print(main)
    collection["description"] = main
    a = td.find('a')
    src = home +a["href"]
    #print("典藏图片:"+src)
    collection["img"] = src
    collection["mname"] = "青州博物馆"
    return collection

def education(url,temp):
    edu = {}
    home = "http://bowuguan.qingzhou.gov.cn/zl/"
    soup = get_soup(url)
    title = soup.find('td',attrs={'height':'80'})
    #print(title.text)
    edu["name"] = title.text
    td = soup.find('div',attrs={'class':'TRS_Editor'})
    main = ""
    p = td.find_all('p')
    for tag in p:
        main = main+tag.text
    #print(main)
    edu["description"] = main
    a = td.find('a')
    src = home +a["href"]
    #print("活动写照:"+src)
    edu["img"] = src
    edu["mname"] = "青州博物馆"
    edu["time"] = temp
    return edu

url = "https://baike.sogou.com/v163579.htm?fromTitle=%E9%9D%92%E5%B7%9E%E5%8D%9A%E7%89%A9%E9%A6%86"
x = get_brief(url)
a = []
a.append(x)

url = "http://bowuguan.qingzhou.gov.cn/"
soup = get_soup(url)
visit = ""
print("------参观信息------")
font = soup.find_all('font',attrs={'class':'title4'})
for tag in font:
    visit = visit+tag.text
print(visit)
print("\n")

exhibitions = []
#展览陈列
print("------展览陈列------")
url = "http://bowuguan.qingzhou.gov.cn/zl/jbcl/201910/t20191021_486708.html"
x = show(url)
exhibitions.append(x)
print("\n")
url = "http://bowuguan.qingzhou.gov.cn/zl/jbcl/201910/t20191021_486708.html"
x = show(url)
exhibitions.append(x)
print("\n")
url = "http://bowuguan.qingzhou.gov.cn/zl/jbcl/201910/t20191018_486432.html"
x = show(url)
exhibitions.append(x)
print("\n")

collections = []
#典藏珍品
print("------典藏珍品------")
url = "http://bowuguan.qingzhou.gov.cn/cp/tq/201910/t20191016_486076.html"
y = object(url)
collections.append(y)
print("\n")
url = "http://bowuguan.qingzhou.gov.cn/cp/tq/201910/t20191016_486071.html"
y = object(url)
collections.append(y)
print("\n")
url = "http://bowuguan.qingzhou.gov.cn/cp/sh/201910/t20191016_486125.html"
y = object(url)
collections.append(y)
print("\n")
url = "http://bowuguan.qingzhou.gov.cn/cp/qtq/201910/t20191017_486245.html"
y = object(url)
collections.append(y)
print("\n")
url = "http://bowuguan.qingzhou.gov.cn/cp/sk/201910/t20191017_486223.html"
y = object(url)
collections.append(y)
print("\n")

educational = []
#教育活动
print("------教育活动------")
url = "http://bowuguan.qingzhou.gov.cn/jy/sjhd/dslxs/201910/t20191031_487522.html"
temp = "2019年9月15日"
z = education(url,temp)
educational.append(z)
print("\n")
url = "http://bowuguan.qingzhou.gov.cn/jy/sjhd/xyx/201910/t20191018_486369.html"
temp = "2019年6月24日"
z = education(url,temp)
educational.append(z)
print("\n")
url = "http://bowuguan.qingzhou.gov.cn/jy/wbjz/201910/t20191018_486382.html"
temp = "2019年5月13日"
z = education(url,temp)
educational.append(z)
print("\n")

museum_info["1"] = a
museum_info["2"] = exhibitions
museum_info["3"] = collections
museum_info["4"] = educational

save_data(museum_info)