import requests
import re
import bs4
from bs4 import BeautifulSoup
import bs4
import pymysql

headers = {
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
    src = "http://www.hnzzmuseum.com/attached/upload/20190606131110823.jpg"
    print("------参观信息------")
    visit = soup.find('table',class_ ='abstract_tbl')
    info = visit.find_all('tr')
    #for tag in info:
        #title = tag.find('th',class_ = 'base-info-card-title')
        #print(title.text+":",end="")
        #texts = tag.find('div',class_ = 'base-info-card-value').find(text=True).strip()
        #print(texts)
    brief["name"] = "郑州博物馆"
    brief["img"] = src
    brief["location"] = "郑州市嵩山南路168号"
    brief["number"] = "预约电话：0371-67438090转分机8088"
    brief["opentime"] = "夏季：9:00—17:00  冬季：9:00—16:30" 
    return brief

def show(url,temp):
    exhibition = {}
    home = "http://www.hnzzmuseum.com"
    soup = get_soup(url)
    div = soup.find('div',attrs={'class':'n_collection_box'})
    title = div.find('span')
    #print(title.text)
    exhibition["name"] = temp
    p = div.find_all('p')
    main = ""
    for tag in p:
        main = main+tag.text
    #print(main)
    exhibition["description"] = main
    img = div.find_all('img')
    i = 0
    for tag in img:
        i = i+1
        src =home+tag["src"]
        exhibition["img"] = src
        #print("展览图示:"+src)
        #if i == 3:
        break
    exhibition["mname"] = "郑州博物馆"
    return exhibition

def object(url):
    collection = {}
    home = "http://www.hnzzmuseum.com"
    soup = get_soup(url)
    div = soup.find('div',attrs={'class':'n_collection_box'})
    title = div.find('span')
    #print(title.text)
    collection["name"] = (title.text).strip()
    p = div.find_all('p')
    main = ""
    for tag in p:
        main = main+tag.text
    #print(main)
    collection["description"] = main
    img = div.find_all('img')
    i = 0
    for tag in img:
        i = i+1
        src =home+tag["src"]
        collection["img"] = src
        #print("典藏图片:"+src)
        #if i == 3:
        break
    collection["mname"] = "郑州博物馆"
    return collection

def education(url,temp):
    edu = {}
    home = "http://www.hnzzmuseum.com"
    soup = get_soup(url)
    div = soup.find('div',attrs={'class':'n_news_box'})
    title = div.find('span')
    edu["name"] = title.text
    #print(title.text)
    p = div.find_all('p')
    main = ""
    for tag in p:
        main = main+tag.text
    #print(main)
    edu["description"] = main
    img = div.find_all('img')
    i = 0
    for tag in img:
        i = i+1
        src =home+tag["src"]
        edu["img"] = src
        #print("活动写照:"+src)
        #if i == 3:
        break
    edu["mname"] = "郑州博物馆"
    edu["time"] = temp
    return edu

url = "https://baike.sogou.com/v8033039.htm?fromTitle=%E9%83%91%E5%B7%9E%E5%8D%9A%E7%89%A9%E9%A6%86"
x = get_brief(url)
a = []
a.append(x)

exhibitions = []
print("------展览陈列------")
url = "http://www.hnzzmuseum.com/display/2.html"
temp = "长渠缀珍——南水北调中线工程河南段文物保护成果展"
x = show(url,temp)
exhibitions.append(x)
print("\n")
url = "http://www.hnzzmuseum.com/display/1.html"
temp = "古代石刻艺术展"
x = show(url,temp)
exhibitions.append(x)
print("\n")
url = "http://www.hnzzmuseum.com/display/8.html"
temp = "追迹文明——新中国河南考古七十年"
x = show(url,temp)
exhibitions.append(x)
print("\n")

collections = []
print("------典藏珍品------")
url = "http://www.hnzzmuseum.com/collection/23.html"
y = object(url)
collections.append(y)
print("\n")
url = "http://www.hnzzmuseum.com/collection/21.html"
y = object(url)
collections.append(y)
print("\n")
url = "http://www.hnzzmuseum.com/collection/38.html"
y = object(url)
collections.append(y)
print("\n")
url = "http://www.hnzzmuseum.com/collection/48.html"
y = object(url)
collections.append(y)
print("\n")
url = "http://www.hnzzmuseum.com/collection/28.html"
y = object(url)
collections.append(y)
print("\n")

educational = []
print("------教育活动------")
url = "http://www.hnzzmuseum.com/article/550.html"
time = "2019年2月5日、2月6日、2月8日"
z = education(url,time)
educational.append(z)
print("\n")
url = "http://www.hnzzmuseum.com/article/515.html"
time = "2018年9月24日"
z = education(url,time)
educational.append(z)
print("\n")
url = "http://www.hnzzmuseum.com/article/17.html"
time = "2018年4月15日"
z = education(url,time)
educational.append(z)
print("\n")

museum_info["1"] = []#a
museum_info["2"] = exhibitions
museum_info["3"] = []#collections
museum_info["4"] = []#educational

save_data(museum_info)

