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
    src = img["src"]
    print("------参观信息------")
    visit = soup.find('table',class_ ='abstract_tbl')
    info = visit.find_all('tr')
    #for tag in info:
        #title = tag.find('th',class_ = 'base-info-card-title')
        #print(title.text+":",end="")
        #texts = tag.find('div',class_ = 'base-info-card-value').find(text=True).strip()
        #print(texts)
    brief["name"] = "烟台市博物馆"
    brief["img"] = src
    brief["location"] = "烟台市南大街61号"
    brief["number"] = "联系电话：0535-6232976"
    brief["opentime"] = "5月—10月 9：00-17：00（16:30停止入场）    11月—4月 9：00-16：30（16:00停止入场）    每周一闭馆（法定节假日除外） " 
    return brief


def show(url):
    exhibition = {}
    home = "http://www.ytmuseum.com"
    soup = get_soup(url)
    div = soup.find('div',attrs={'class':'wszt'})
    title = div.find('font',attrs={'style':'FONT-SIZE: 20px'})
    #print(title.text)
    exhibition["name"] = title.text
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
        #if i  == 3:
        break
    exhibition["mname"] = "烟台市博物馆"
    return exhibition

def showing(url):
    exhibition = {}
    home = "http://www.ytmuseum.com"
    soup = get_soup(url)
    div = soup.find('div',attrs={'class':'wszt'})
    title = div.find('font',attrs={'style':'FONT-SIZE: 20px'})
    #print(title.text)
    exhibition["name"] = title.text
    span = div.find_all('span',attrs={'style':'line-height: 28px; font-size: 14pt;'})
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
        exhibition["img"] = src
        #print("展览图示:"+src)
        #if i  == 3:
        break
    exhibition["mname"] = "烟台市博物馆"
    return exhibition

def object(url):
    collection = {}
    home = "http://www.ytmuseum.com"
    soup = get_soup(url)
    div = soup.find('div',attrs={'class':'dcxxb2'})
    id = div.find('div',attrs={'id':'InfoTitle'})
    #print(id.text)
    collection["name"] = id.text
    p = div.find_all('p')
    main = ""
    for tag in p:
        main = main+tag.text
    #print(main)
    collection["description"] = main
    img = div.find_all("img")
    for tag in img:
        src = home+tag["src"]
        #print("藏品图片:"+src)
        collection["img"] = src
        break
    collection["mname"] = "烟台市博物馆"
    return collection

def education(url,time):
    home = "http://www.ytmuseum.com"
    edu = {}
    soup = get_soup1(url)
    div = soup.find('div',attrs={'class':'wszt'})
    title = div.find('div',attrs={'id':'InfoTitle'})
    edu["name"] = (title.text).strip()
    span = soup.find_all('span')
    main = ""
    for tag in span:
        main = main+tag.text
    edu["description"] = main
    img = soup.find_all('img',attrs={'alt':''})
    for tag in img:
        src = home+tag["src"]
        edu["img"] = src
        break
    edu["mname"] = "烟台市博物馆"
    edu["time"] = time
    return edu

url = "https://baike.sogou.com/v154448.htm?fromTitle=%E7%83%9F%E5%8F%B0%E5%B8%82%E5%8D%9A%E7%89%A9%E9%A6%86"
x = get_brief(url)
a = []
a.append(x)

print("\n")

exhibitions = []
print("------展览陈列------")
url = "http://www.ytmuseum.com/zhanting/172/Detail.html"
x = show(url)
exhibitions.append(x)
print("\n")
url = "http://www.ytmuseum.com/zhanting/1156/Detail.html"
x = showing(url)
exhibitions.append(x)
print("\n")
url = "http://www.ytmuseum.com/zhanting/1116/Detail.html"
x = showing(url)
exhibitions.append(x)
print("\n")

collections = []
print("------典藏珍品------")
url = "http://www.ytmuseum.com/diancang/270/Detail.html"
y = object(url)
collections.append(y)
print("\n")
url = "http://www.ytmuseum.com/diancang/674/Detail.html"
y = object(url)
collections.append(y)
print("\n")
url = "http://www.ytmuseum.com/diancang/275/Detail.html"
y = object(url)
collections.append(y)
print("\n")
url = "http://www.ytmuseum.com/diancang/678/Detail.html"
y = object(url)
collections.append(y)
print("\n")
url = "http://www.ytmuseum.com/diancang/677/Detail.html"
y = object(url)
collections.append(y)
print("\n")

educational = []

url = "http://www.ytmuseum.com/zixun/8606/Detail.html"
time = "2020年3月28日"
z = education(url,time)
educational.append(z)
url = "http://www.ytmuseum.com/zixun/8622/Detail.html"
time = "2020/4/6 "
z = education(url,time)
educational.append(z)
url = "http://www.ytmuseum.com/zixun/8596/Detail.html"
time = "2020/3/25"
z = education(url,time)
educational.append(z)

museum_info["1"] = []#a
museum_info["2"] = []#exhibitions
museum_info["3"] = []#collections
museum_info["4"] = educational

save_data(museum_info)



