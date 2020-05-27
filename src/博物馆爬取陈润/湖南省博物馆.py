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
    for tag in info:
        title = tag.find('th',class_ = 'base-info-card-title')
        #print(title.text+":",end="")
        texts = tag.find('div',class_ = 'base-info-card-value').find(text=True).strip()
        #print(texts)
    brief["name"] = "湖南省博物馆"
    brief["img"] = src
    brief["location"] = "地址：湖南省长沙市开福区东风路50号"
    brief["number"] = "参观咨询电话：0731-84415833、84475933"
    brief["opentime"] = "每周二至周日9:00—17:00（16:00停止入馆），每周一为闭馆日（逢法定节假日顺延）" 
    return brief

def show(url): #藏品由一张图诠释简介和样式
    exhibition = {}
    home = "http://www.jhgmuseum.com"
    soup = get_soup1(url)
    div = soup.find('div',attrs={'class':'zt_topcontent container'})
    title = div.find('h3',attrs={'class':'title'})
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
        src = tag["src"]
        exhibition["img"] = src
        #print("展览图示:"+src)
        #if i == 4:
        break
    exhibition["mname"] = "湖南省博物馆"
    return exhibition

def object(url):
    collection = {}
    home = "http://www.hnmuseum.com"
    soup = get_soup1(url)
    div = soup.find('div',attrs={'class':'container'})
    title = div.find('span',attrs={'property':'dc:title'})['content']
    collection["name"] = title
    #print(title)
    img = div.find('img',attrs={'alt':''})
    src = home+img["src"]
    collection["img"] = src
    collection["description"] = ""
    collection["mname"] = "湖南省博物馆"
    return collection
    #print("藏品图示:"+src) 

def education(url):
    edu = {}
    home = "http://www.hnmuseum.com"
    soup = get_soup1(url)
    div = soup.find('div',attrs={'class':'eleven columns'})
    title = div.find('span',attrs={'property':'dc:title'})['content']
    edu["name"] = title
    #print(title)
    p = div.find_all('p')
    main = ""
    for tag in p:
        main = main+tag.text
    #print(main)
    edu["description"] = main
    img = div.find_all('img',attrs={'alt':''})
    i = 0
    for tag in img:
        i = i+1
        src = home+tag["src"]
        edu["img"] = src
        #print("藏品图示:"+src)
        #if i == 3:
        break
    edu["mname"] = "湖南省博物馆"
    return edu

url = "https://baike.sogou.com/v114563.htm?fromTitle=%E6%B9%96%E5%8D%97%E7%9C%81%E5%8D%9A%E7%89%A9%E9%A6%86"
x = get_brief(url)
a = []
a.append(x)

exhibitions = []
print("------展览陈列------")
url = "http://www.hnmuseum.com/zh-hans/content/%E9%95%BF%E6%B2%99%E9%A9%AC%E7%8E%8B%E5%A0%86%E6%B1%89%E5%A2%93%E9%99%88%E5%88%97"
x = show(url)
exhibitions.append(x)
print("\n")
url = "http://www.hnmuseum.com/zh-hans/content/%E9%BD%90%E5%AE%B6%E2%80%94%E2%80%94%E6%98%8E%E6%B8%85%E4%BB%A5%E6%9D%A5%E4%BA%BA%E7%89%A9%E7%94%BB%E4%B8%AD%E7%9A%84%E5%AE%B6%E6%97%8F%E7%94%9F%E6%B4%BB%E4%B8%8E%E4%BF%A1%E4%BB%B0"
x = show(url)
exhibitions.append(x)
print("\n")
url = "http://www.hnmuseum.com/zh-hans/content/%E6%BF%80%E9%80%B8%E5%93%8D%E4%BA%8E%E6%B9%98%E6%B1%9F%E5%85%AE%E2%80%94%E2%80%94%E6%BD%87%E6%B9%98%E5%8F%A4%E7%90%B4%E6%96%87%E5%8C%96%E5%B1%95"
x = show(url)
exhibitions.append(x)
print("\n")

collections = []
print("------典藏珍品------")
url = "http://www.hnmuseum.com/zh-hans/content/%E9%BB%84-%E7%BA%B1-%E5%9C%B0-%E5%8D%B0-%E8%8A%B1-%E6%95%B7-%E5%BD%A9-%E4%B8%9D-%E7%BB%B5-%E8%A2%8D"
y = object(url)
collections.append(y)
print("\n")
url = "http://www.hnmuseum.com/zh-hans/content/%E5%A4%A7-%E7%A6%BE-%E4%BA%BA-%E9%9D%A2-%E7%BA%B9-%E6%96%B9-%E9%BC%8E"
y = object(url)
collections.append(y)
print("\n")
url = "http://www.hnmuseum.com/zh-hans/content/%E5%95%86-%E4%BB%A3-%E8%B1%A1-%E7%BA%B9-%E9%93%9C-%E9%93%99"
y = object(url)
collections.append(y)
print("\n")
url = "http://www.hnmuseum.com/zh-hans/content/t-%E5%BD%A2-%E5%B8%9B-%E7%94%BB"
y = object(url)
collections.append(y)
print("\n")
url = "http://www.hnmuseum.com/zh-hans/content/%E6%9C%B1-%E5%9C%B0-%E5%BD%A9-%E7%BB%98-%E6%A3%BA"
y = object(url)
collections.append(y)
print("\n")

educational = []
print("------教育活动------")
url = "http://www.hnmuseum.com/zh-hans/huodong_zhuanti/%E5%AF%92%E6%84%8F%E6%B8%90%E6%B5%93%EF%BC%8C%E6%9A%96%E5%BF%83%E5%86%AC%E8%87%B3"
z = education(url)
z["time"] = "活动时间: 2018-12-30 09:30 to 16:00"
educational.append(z)
print("\n")
url = "http://www.hnmuseum.com/zh-hans/huodong_zhuanti/%E7%AC%AC%E4%BA%8C%E5%B1%8A%E5%8D%9A%E7%89%A9%E9%A6%86%E5%84%BF%E7%AB%A5%E8%89%BA%E6%9C%AF%E5%AD%A3%E6%AC%A2%E4%B9%90%E6%9D%A5%E8%A2%AD"
z = education(url)
z["time"] = "活动时间: 2019-08-21 14:03"
educational.append(z)
print("\n")
url = "http://www.hnmuseum.com/zh-hans/huodong_zhuanti/%E5%AF%92%E5%81%87%E5%9C%A8%E6%B9%98%E5%8D%9A%E9%81%87%E8%A7%81%E5%A5%87%E5%A6%99%E2%80%A2%E5%A5%87%E8%B6%A3%E2%80%A2%E5%A5%87%E5%B9%BB"
z = education(url)
z["time"] = "活动时间: 2019-01-22 09:30 to 2019-02-10 16:00"
educational.append(z)
print("\n")

museum_info["1"] = a
museum_info["2"] = []#exhibitions
museum_info["3"] = []#collections
museum_info["4"] = []#educational

save_data(museum_info)