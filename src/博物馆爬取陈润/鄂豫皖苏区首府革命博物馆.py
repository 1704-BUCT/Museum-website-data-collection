import requests
import re
import bs4
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

museum_info = {}

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
    for tag in info:
        title = tag.find('th',class_ = 'base-info-card-title')
        #print(title.text+":",end="")
        texts = tag.find('div',class_ = 'base-info-card-value').find(text=True).strip()
        #print(texts)
    brief["name"] = "鄂豫皖苏区首府革命博物馆"
    brief["img"] = src
    brief["location"] = "河南省信阳市新县首府路文博新村4号"
    brief["number"] = "监督、投诉电话：0376-2987315"
    brief["opentime"] = "开放时间：春季、夏季8:00-17:30；秋季、冬季8:00-17:00）" 
    return brief

def show(url):
    exhibition = {}
    home = "http://www.eywsqsfbwg.com"
    soup = get_soup1(url)
    div = soup.find('div',attrs={'class':'inner'})
    title = div.find('h2',attrs={'class':'newstit'})
    exhibition["name"] = (title.text).strip()
    #print(title.text)
    main = ""
    p = div.find_all('p')
    for tag in p:
        main = main+tag.text
    exhibition["description"] = main
    #print(main)
    img = div.find_all('img')
    i = 0
    for tag in img:
        i = i+1
        src =home+tag["src"]
        exhibition["img"] = src
        #print("展览图示:"+src)
        #if i == 3:
        break
    exhibition["mname"] = "鄂豫皖苏区首府革命博物馆"
    return exhibition

def object(url):
    collection = {}
    home = "http://www.eywsqsfbwg.com"
    soup = get_soup1(url)
    div = soup.find('div',attrs={'class':'inner'})
    title = div.find('h2',attrs={'class':'newstit'})
    collection["name"] = (title.text).strip()
    #print(title.text)
    main = ""
    p = div.find_all('p')
    for tag in p:
        main = main+tag.text
    collection["description"] = main
    #print(main)
    img = div.find_all('img')
    i = 0
    for tag in img:
        i = i+1
        src =home+tag["src"]
        collection["img"] = src
        #print("藏品图片:"+src)
        #if i == 3:
        break
    collection["mname"] = "鄂豫皖苏区首府革命博物馆"
    return collection

def education(url):
    edu = {}
    home = "http://www.eywsqsfbwg.com"
    soup = get_soup1(url)
    div = soup.find('div',attrs={'class':'inner'})
    title = div.find('h2',attrs={'class':'newstit'})
    edu["name"] = (title.text).strip()
    #print(title.text)
    main = ""
    p = div.find_all('p')
    for tag in p:
        main = main+tag.text
    edu["description"] = main
    #print(main)
    img = div.find_all('img')
    i = 0
    for tag in img:
        i = i+1
        src =home+tag["src"]
        edu["img"] = src
        #print("活动写照:"+src)
        #if i == 3:
        break
    edu["mname"] = "鄂豫皖苏区首府革命博物馆"
    return edu
    
url = "https://baike.sogou.com/v10990393.htm?fromTitle=%E9%84%82%E8%B1%AB%E7%9A%96%E8%8B%8F%E5%8C%BA%E9%A6%96%E5%BA%9C%E9%9D%A9%E5%91%BD%E5%8D%9A%E7%89%A9%E9%A6%86"
x = get_brief(url)
a = []
a.append(x)

exhibitions = []
print("-----展览陈列------")
url = "http://www.eywsqsfbwg.com/index.php?m=content&c=index&a=show&catid=11&id=45"
x = show(url)
exhibitions.append(x)
print("\n")
url = "http://www.eywsqsfbwg.com/index.php?m=content&c=index&a=show&catid=12&id=65"
x = show(url)
exhibitions.append(x)
print("\n")
url = "http://www.eywsqsfbwg.com/index.php?m=content&c=index&a=show&catid=13&id=66"
x = show(url)
exhibitions.append(x)
print("\n")

collections = []
print("------典藏珍品------")
url = "http://www.eywsqsfbwg.com/index.php?m=content&c=index&a=show&catid=15&id=30"
y = object(url)
collections.append(y)
print("\n")
url = "http://www.eywsqsfbwg.com/index.php?m=content&c=index&a=show&catid=15&id=29"
y = object(url)
collections.append(y)
print("\n")
url = "http://www.eywsqsfbwg.com/index.php?m=content&c=index&a=show&catid=15&id=27"
y = object(url)
collections.append(y)
print("\n")
url = "http://www.eywsqsfbwg.com/index.php?m=content&c=index&a=show&catid=15&id=25"
y = object(url)
collections.append(y)
print("\n")
url = "http://www.eywsqsfbwg.com/index.php?m=content&c=index&a=show&catid=15&id=24"
y = object(url)
collections.append(y)
print("\n")

educational = []
print("------教育活动------")
url = "http://www.eywsqsfbwg.com/index.php?m=content&c=index&a=show&catid=9&id=176"
z = education(url)
z["time"] = "发布时间：2020-04-18 17:04:00"
educational.append(z)
print("\n")
url = "http://www.eywsqsfbwg.com/index.php?m=content&c=index&a=show&catid=9&id=124"
z = education(url)
z["time"] = "发布时间：2019-12-24 17:21:00"
educational.append(z)
print("\n")
url = "http://www.eywsqsfbwg.com/index.php?m=content&c=index&a=show&catid=9&id=126"
z = education(url)
z["time"] = "发布时间：2019-12-05 14:02:00"
educational.append(z)
print("\n")

museum_info["1"] = a
museum_info["2"] = []#exhibitions
museum_info["3"] = []#collections
museum_info["4"] = []#educational

save_data(museum_info)