import requests
import re
import bs4
from bs4 import BeautifulSoup
import bs4
import pymysql

headers ={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0'
    }
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

def get_soup1(url):
    text = get_text(url)
    soup = BeautifulSoup(text,"html.parser")
    return soup

def get_soup(url):
    res = requests.get(url,headers = headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text,"html.parser")
    return soup

def get_brief(url):
    brief  ={}
    soup = get_soup(url)
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
    for tag in info:
        title = tag.find('th',class_ = 'base-info-card-title')
        #print(title.text+":",end="")
        texts = tag.find('div',class_ = 'base-info-card-value').find(text=True).strip()
        #print(texts)
    brief["name"] = "南阳汉画馆"
    brief["img"] = src
    brief["location"] = "南阳市卧龙区汉画街398号（卧龙区车站南路以西，卧龙路以南）"
    brief["number"] = ""
    brief["opentime"] = "冬季：8:30-17:00，春、夏、秋季：8:30-17:30（周一闭馆，节假日除外）" 
    return brief

def visit(url):
    soup = get_soup(url)
    visit = soup.find('div',attrs={'class':'fcon_m'})
    print(visit.text)

def show(url):
    exhibition = {}
    home = "http://nyhhg.com"
    soup = get_soup(url)
    div = soup.find(attrs={'class':'main_right'})
    title = div.find('div',attrs={'class':'news_xaingxi'})
    #print(title.text)
    exhibition["name"] = title.text
    span = div.find_all('span')
    main = ""
    for tag in span:
        main = main+tag.text
    #print(main)
    exhibition["description"] = main
    img = div.find_all('img')
    i = 0
    for tag in img:
        i = i+1
        src = home+tag["src"]
        #print("展览图示:"+src)
        exhibition["img"] = src
        break
    exhibition["mname"] = "南阳汉画馆"
    return exhibition

def object(url):
    collection = {}
    home = "http://nyhhg.com"
    soup = get_soup(url)
    div = soup.find(attrs={'class':'main_right'})
    title = div.find('div',attrs={'class':'news_xaingxi'})
    #print(title.text)
    collection["name"] = title.text
    span = div.find_all('span')
    main = ""
    for tag in span:
        main = main+tag.text
    #print(main)
    collection["description"] = main
    img = div.find_all('img')
    i = 0
    for tag in img:
        i = i+1
        src = home+tag["src"]
        #print("藏品图片:"+src)
        collection["img"] = src
        break
    collection["mname"] = "南阳汉画馆"
    return collection

def education(url,temp):
    edu = {}
    home = "http://nyhhg.com"
    soup = get_soup(url)
    div = soup.find(attrs={'class':'main_right'})
    title = div.find('div',attrs={'class':'news_xaingxi'})
    #print(title.text)
    edu["name"] = title.text
    span = div.find_all('span')
    main = ""
    for tag in span:
        main = main+tag.text
    #print(main)
    edu["description"] = main
    img = div.find_all('img')
    i = 0
    for tag in img:
        i = i+1
        src = home+tag["src"]
        #print("活动写照:"+src)
        break
    edu["img"] = ""
    edu["time"] = temp
    edu["mname"] = "南阳汉画馆"
    return edu

url = "https://baike.sogou.com/v195918.htm?fromTitle=%E5%8D%97%E9%98%B3%E6%B1%89%E7%94%BB%E9%A6%86"
x = get_brief(url)
a = []
a.append(x)

url = "http://nyhhg.com/"
visit(url)
print("\n")

exhibitions = []
print("------展览陈列------")
url = "http://nyhhg.com/a/jx/214.html"
x = show(url)
exhibitions.append(x)
print("\n")
url = "http://nyhhg.com/a/jx/169.html"
x = show(url)
exhibitions.append(x)
print("\n")
url = "http://nyhhg.com/a/jx/210.html"
x = show(url)
exhibitions.append(x)
print("\n")

collections = []
print("-----典藏珍品------")
url = "http://nyhhg.com/a/xy/164.html"
y = object(url)
collections.append(y)
print("\n")
url = "http://nyhhg.com/a/xy/162.html"
y = object(url)
collections.append(y)
print("\n")
url = "http://nyhhg.com/a/xy/162.html"
y = object(url)
collections.append(y)
print("\n")
url = "http://nyhhg.com/a/xy/141.html"
y = object(url)
collections.append(y)
print("\n")
url = "http://nyhhg.com/a/xy/144.html"
y = object(url)
collections.append(y)
print("\n")

educational = []
print("------教育活动------")
url = "http://nyhhg.com/a/zx/jiaoyuhuodonggongshi/2018/0118/184.html"
temp = "2015-3-15"
z = education(url,temp)
educational.append(z)
print("\n")
url = "http://nyhhg.com/a/gy/205.html"
temp = " 2017年7月29日"
z = education(url,temp)
educational.append(z)
print("\n")
url = "http://nyhhg.com/a/sz/237.html"
temp = "2020-01-15"
z = education(url,temp)
educational.append(z)
print("\n")

museum_info["1"] = []#a
museum_info["2"] = []#exhibitions
museum_info["3"] = []#collections
museum_info["4"] = educational

save_data(museum_info)