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
    brief["name"] = "广东省博物馆"
    brief["img"] = src
    brief["location"] = "地址: 广东省广州市天河区珠江新城珠江东路2号"
    brief["number"] = "咨询电话：020-38046886"
    brief["opentime"] = "开放时间：春季、夏季8:00-17:30；秋季、冬季8:00-17:00）" 
    return brief

def show(url):
    exhibition = {}
    home = "http://www.gdmuseum.com"
    soup = get_soup1(url)
    div = soup.find('div',attrs={'id':'jianjie_content'})
    title = div.find('div',attrs={'class':'Head'})
    exhibition["name"] = (title.text).strip()
    #print(title.text)
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
        src = home+tag["src"]
        exhibition["img"] = src
        #print("展览图示:"+src)
        #if i == 3:
        break
    exhibition["mname"] = "广东省博物馆"
    return exhibition

def object(url):
    collection = {}
    home = "http://www.gdmuseum.com"
    soup = get_soup1(url)
    div = soup.find('div',attrs={'class':'cp_list'})
    dd = div.find_all('dd')
    main = ""
    for tag in dd:
        x = tag.find(text=True).strip()
        print(x,end="")
        y = tag.find('span')
        print(y.text)
        main = main+x+y.text
    collection["description"] = main
    collection["mname"] = "广东省博物馆"
    return collection

def object1(url):
    collection = {}
    soup = get_soup1(url)
    div = soup.find('div',attrs={'class':'cont'})
    p = div.find_all('p')
    main = ""
    for tag in p:
        main = main+tag.text
    #print(main)
    collection["description"] = main
    collection["mname"] = "广东省博物馆"
    return collection

def education(url):
    edu = {}
    home = "http://www.gdmuseum.com"
    soup = get_soup1(url)
    div = soup.find('div',attrs={'class':'detail'})
    p = div.find_all('p')
    for tag in p:
        title = tag.text
        edu["name"] = title
        break
    main = ""
    for tag in p:
        main = main+tag.text
    edu["description"] = main
    #print(main)
    img = div.find_all('img')
    i = 0
    for tag in img:
        i = i+1
        src = home+tag["src"]
        edu["img"] = src
        #print("活动写照:"+src)
        #if i == 4:
        break
    edu["mname"] = "广东省博物馆"
    return edu

url = "https://baike.sogou.com/v584354.htm?fromTitle=%E5%B9%BF%E4%B8%9C%E7%9C%81%E5%8D%9A%E7%89%A9%E9%A6%86"
x = get_brief(url)
a = []
a.append(x)

exhibitions = []
print("-----展览图示------")
url = "http://www.gdmuseum.com/gdmuseum/_300730/_300734/532437/index.html"
x = show(url)
exhibitions.append(x)
print("\n")
url = "http://www.gdmuseum.com/gdmuseum/_300730/_300734/448105/index.html"
x = show(url)
exhibitions.append(x)
print("\n")
url = "http://www.gdmuseum.com/gdmuseum/_300730/_300734/532560/index.html"
x = show(url)
exhibitions.append(x)
print("\n")

collections = []
print("------典藏珍品------")
url = "http://www.gdmuseum.com/gdmuseum/_300746/_300758/tc45/515013/index.html"
y = object(url)
y["img"] = "http://www.gdmuseum.com/gdmuseum/_300746/_300758/tc45/515013/2018120709163868233.jpg"
y["name"] = "明崇祯款青花罗汉纹炉"
collections.append(y)
print("\n")
url = "http://www.gdmuseum.com/gdmuseum/_300746/_300758/sh87/429266/index.html"
y = object1(url)
y["name"] = "沈周 青山暮云图轴"
y["img"] = "http://www.gdmuseum.com/attachment/201209/19/2_1348037436N2IU.jpg"
collections.append(y)
print("\n")
url = "http://www.gdmuseum.com/gdmuseum/_300746/_300758/qtq/429271/index.html"
y = object1(url)
y["name"] = "春秋楚王孙铜钟"
y["img"] = "http://www.gdmuseum.com/attachment/201209/24/2_1348450555RzSZ.jpg"
collections.append(y)
print("\n")
url = "http://www.gdmuseum.com/gdmuseum/_300746/_300758/yq43/531376/index.html"
y = object(url)
y["name"] = "明青玉桃式洗"
y["img"] = "http://www.gdmuseum.com/gdmuseum/_300746/_300758/yq43/531376/E1224-%E6%98%8E%E6%99%9A%E6%9C%9F%E9%9D%92%E7%8E%89%E6%A1%83%E5%BC%8F%E6%B4%97%201.jpg"
collections.append(y)
print("\n")
url = "http://www.gdmuseum.com/gdmuseum/_300746/_300758/tc45/515033/index.html"
y = object(url)
y["name"] = "明石湾窑翠毛釉梅瓶"
y["img"] = "http://www.gdmuseum.com/gdmuseum/_300746/_300758/tc45/515033/2018120709150168958.jpg"
collections.append(y)
print("\n")

educational = []
print("------教育活动------")
url = "http://www.gdmuseum.com/gdmuseum/_300670/_300702/543277/index.html"
z = education(url)
z["time"] = "2020年03月25日"
educational.append(z)
print("\n")
url = "http://www.gdmuseum.com/gdmuseum/_300670/_300702/537464/index.html"
z = education(url)
z["time"] = "2020年02月18日"
print("\n")
url = "http://www.gdmuseum.com/gdmuseum/_300670/_300702/537226/index.html"
z = education(url)
z["time"] = "2020年02月18日"
educational.append(z)
print("\n")

museum_info["1"] = a
museum_info["2"] = []#exhibitions
museum_info["3"] = []#collections
museum_info["4"] = []#educational

save_data(museum_info)