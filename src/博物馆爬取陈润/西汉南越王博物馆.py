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
    brief["name"] = "西汉南越王博物馆"
    brief["img"] = src
    brief["location"] = "广州市解放北路867号"
    brief["number"] = "36182920"
    brief["opentime"] = "全年开放，2月28日、8月31日闭馆检修。  周一至周四：9:00- 17:30（16:45停止售票及进场）、周五至周日：9:00- 21:00（20:00停止售票；20:10停止进场" 
    return brief

def visit(url):
    soup = get_soup1(url)
    div = soup.find('div',attrs={'class':'index-action-content-view'})
    visit = div.text
    print(visit)

def show(url):
    exhibition = {}
    home = "https://www.gznywmuseum.org"
    soup = get_soup1(url)
    div = soup.find('div',attrs={'class':'wltm-detail-view'})
    span = div.find('span',attrs={'class':'wltm-detail-title-text'})
    #print(span.text)
    exhibition["name"] = (span.text).strip()
    main = div.find('div',attrs={'class':'wltm-detail-content-text'})
    #print(main.text)
    exhibition["description"] = main.text
    img = div.find('img',attrs={'class':'wltm-detail-content-img'})
    src = home+img["src"]
    #print("展览图示:"+src)
    exhibition["img"] = src
    exhibition["mname"] = "西汉南越王博物馆"
    return exhibition

def object(url):
    collection = {}
    home = "https://www.gznywmuseum.org"
    soup = get_soup1(url)
    div = soup.find('div',attrs={'class':'cz-list-detail-view-info'})
    title = div.find('p',attrs={'class':'cz-list-detail-view-info-title'})
    #print(title.text)
    collection["name"] = (title.text).strip()
    span = div.find_all('span')
    main = ""
    for tag in span:
        main = main+tag.text
    #print(main)
    collection["description"] = main
    div = soup.find('div',attrs={'class':'cz-list-content-view'})
    img = div.find_all('img',attrs={'width':'200'})
    i = 0
    for tag in img:
        i = i+1
        src = home+tag["src"]
        collection["img"] = src
        #print("藏品图示:"+src)
        #if i == 1:
        break
    collection["mname"] = "西汉南越王博物馆"
    return collection

def education(url,temp):
    edu = {}
    soup = get_soup1(url)
    div = soup.find('div',attrs={'class':'nbsp-sp-content-view'})
    title = soup.find('p',attrs={'class':'nbsp-sp-detail-title'})
    #print(title.text)
    edu["name"] = (title.text).strip()
    content = div.find_all('div',attrs={'class':'wltm-detail-content-text'})
    main = ""
    for tag in content:
        main = main+tag.text
    #print(main)
    edu["description"] = main
    img = div.find_all('img',attrs={'class':'wltm-detail-content-img'})
    i = 0
    for tag in img:
        i = i+1
        if i == 1:
            continue
        src = tag["src"]
        #print("活动写照:"+src)
        edu["img"] = src
        if i == 2:
            break
    edu["mname"] = "西汉南越王博物馆"
    edu["time"] = temp
    return edu

url = "https://baike.sogou.com/v584410.htm?fromTitle=%E8%A5%BF%E6%B1%89%E5%8D%97%E8%B6%8A%E7%8E%8B%E5%8D%9A%E7%89%A9%E9%A6%86"
x = get_brief(url)
a = []
a.append(x)

url = "https://www.gznywmuseum.org/"
visit(url)

exhibitions = []
print("------南越文王墓------")
url = "https://www.gznywmuseum.org/nywwm/index.jhtml"
x = show(url)
exhibitions.append(x)
print("\n")

collections = []
print("------典藏珍品------")
url = "https://www.gznywmuseum.org/yx/90.jhtml"
y = object(url)
collections.append(y)
print("\n")
url = "https://www.gznywmuseum.org/yq/153.jhtml"
y = object(url)
collections.append(y)
print("\n")
url = "https://www.gznywmuseum.org/yq/153.jhtml"
y = object(url)
collections.append(y)
print("\n")
url = "https://www.gznywmuseum.org/jyq/163.jhtml"
y = object(url)
collections.append(y)
print("\n")
url = "https://www.gznywmuseum.org/jtq/164.jhtml"
y = object(url)
collections.append(y)
print("\n")

educational = []
print("------教育活动------")
url = "https://www.gznywmuseum.org/nbzx/53.jhtml"
temp = "2017-11-18 11:28:18"
z = education(url,temp)
educational.append(z)
print("-------------------\n")
url = "https://www.gznywmuseum.org/nbzx/192.jhtml"
temp = "2017-11-18 04:24:31"
z = education(url,temp)
educational.append(z)
print("-------------------\n")
url = "https://www.gznywmuseum.org/nbzx/191.jhtml"
temp = "2017-11-18 04:17:41"
z = education(url,temp)
educational.append(z)
print("\n")

museum_info["1"] = a
museum_info["2"] = exhibitions
museum_info["3"] = collections
museum_info["4"] = educational

save_data(museum_info)