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
            data_1 = [i["name"],i["imgurl"],i['number'],i['location'],i['brief'],i['opentime']]
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
    brief_info = {}
    brief_info["name"] = "广西民族博物馆"
    soup = get_soup1(url)
    print("------博物馆简介------")
    div = soup.find('div',attrs={'class':'abstract_main'})
    img = div.find('img',attrs={'title':'广西民族博物馆'})
    src = img["src"]
    brief = soup.find('div',id = 'j-shareAbstract',style = 'display: none')
    description = brief.text
    #print(description)
    brief_info["brief"] = description
    print("------参观信息------")
    visit = soup.find('table',class_ ='abstract_tbl')
    info = visit.find_all('tr')
    for tag in info:
        title = tag.find('th',class_ = 'base-info-card-title')
        #print(title.text+":",end="")
        texts = tag.find('div',class_ = 'base-info-card-value').find(text=True).strip()
        #print(texts)
    visited = "电话/传真:0771-2024322\nEmail:gxmzbwgbgs@amgx.org"
    #print(visited)
    brief_info["number"] = "0771-2024322"
    brief_info["imgurl"] = src
    brief_info["opentime"] = "周二至周日（9：30-16:30）"
    brief_info["location"] = "南宁市青秀山风景区青环路11号"
    print(brief_info)
    return brief_info

def show(url):
    exhibition_hall = []
    exhibitions = {}
    soup = get_soup1(url)
    div = soup.find_all('div',attrs={'class':'lzhg'})
    for tag in div:
        a = tag.find_all('a',attrs={'target':'_blank'})
        for x in a:
            title = x.text
            print(title)
            break
        exhibitions["mname"] = "广西民族博物馆"
        exhibitions["name"] = title.strip()
        exhibitions["description"] = tag.text
        i = 0
        #print(tag.text)
        org = tag.find('a',attrs={'target':'_blank'})['href']
        exhibitions["img"] = org
        exhibition_hall.append(exhibitions)
        #print("3D导视图:"+org)
        if i == 4:
            break
    return exhibition_hall

def object(url):
    collections = []
    collection = {}
    soup = get_soup1(url)
    div = soup.find('div',attrs={'class':'videoli'})
    dl = div.find_all('dl')
    main = ""
    for tag in dl:
        collection["name"] = (tag.text).strip()
        #print(tag.text)
        org = tag.find('a',attrs={'target':'_blank'})['href']
        collection["img"] = org
        collection["mname"] = "广西民族博物馆"
        collection["description"] = ""
        #print("3D视频连接:"+org)
        collections.append(collection)
    print(collections)
    return collections

def education(url):
    edu = {}
    soup = get_soup1(url)
    div = soup.find('div',attrs={'class':'mbinnerr dright'})
    title = div.find('h4',attrs={'class':'mbdetialt'})
    edu["name"] = (title.text).strip()
    #print(title.text)
    p = div.find('p')
    edu["description"] = p.text
    edu["mname"] = "广西民族博物馆"
    edu["img"] = ""
    #print(p.text)
    return edu

url = "https://baike.sogou.com/v256393.htm?fromTitle=%E5%B9%BF%E8%A5%BF%E6%B0%91%E6%97%8F%E5%8D%9A%E7%89%A9%E9%A6%86"
x = get_brief(url)
a = []
a.append(x)
museum_info["1"] = a

print("------展览陈列------")
url = "http://www.amgx.org/exhibimore-483.html"
a = show(url)
museum_info["2"] = []#a
print("\n")

print("------典藏珍品------")
url = "http://www.amgx.org/3dantiques.html"
y = object(url)
museum_info["3"] = []#y
print("\n")

educations = []
print("------教育活动------")
url = "http://www.amgx.org/news-7777.html"
z = education(url)
z["time"] = "时间:2018-06-1"
educations.append(z)
print("\n")
url = "http://www.amgx.org/news-7686.html"
z = education(url)
z["time"] = "时间:2018-04-09"
educations.append(z)
print("\n")
url = "http://www.amgx.org/news-6730.html"
z = education(url)
z["time"] = "时间:2016-02-01"
educations.append(z)
print("\n")

museum_info["4"] = []#educations

print(museum_info)
save_data(museum_info)