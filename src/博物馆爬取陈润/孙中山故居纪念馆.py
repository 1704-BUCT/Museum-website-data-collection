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
    #img = div.find('img',attrs={'width':'250'})
    src = "http://www.rjjng.com.cn/cms/resource/img/h000/h01/img201410141655490.jpg"
    print("------参观信息------")
    visit = soup.find('table',class_ ='abstract_tbl')
    info = visit.find_all('tr')
    #for tag in info:
        #title = tag.find('th',class_ = 'base-info-card-title')
        #print(title.text+":",end="")
        #texts = tag.find('div',class_ = 'base-info-card-value').find(text=True).strip()
        #print(texts)
    brief["name"] = "孙中山故居纪念馆"
    brief["img"] = src
    brief["location"] = "广东省中山市翠亨大道93号"
    brief["number"] = "咨询电话：0760—28158366"
    brief["opentime"] = "每天9:00—17:00（16:30停止入场）" 
    return brief

def show(url):
    exhibition = {}
    home = "http://www.sunyat-sen.org"
    soup = get_soup1(url)
    div = soup.find('div',attrs={'class':'ng_box'})
    title = div.find(attrs={'class':'conH3'})
    #print(title.text)
    exhibition["name"] = title.text
    p = div.find('div',attrs={'class':'contentBox'}).find_all('p')
    main = ""
    for tag in p:
        main = main+tag.text
    #print(main)
    exhibition["description"] = main
    img = div.find('img',attrs={'alt':''})
    src = home+img["src"]
    #print("展馆图示:"+src)
    exhibition["img"] = src
    exhibition["mname"] = "孙中山故居纪念馆"
    return exhibition

def object(url,temp):
    collection = {}
    home = "http://www.sunyat-sen.org"
    soup = get_soup1(url)
    content = soup.find('div',attrs={'class':'contentBox'})
    div = content.find_all('div')
    main = ""
    for tag in div:
        main = main+tag.text
    #print(main)
    collection["description"] = main
    img = content.find('img')
    src = home+img["src"]
    #print("藏品图片:"+src)
    collection["img"] = src
    collection["mname"] = "孙中山故居纪念馆"
    collection["name"] = temp
    return collection

url = "https://baike.sogou.com/v564063.htm?fromTitle=%E5%AD%99%E4%B8%AD%E5%B1%B1%E6%95%85%E5%B1%85%E7%BA%AA%E5%BF%B5%E9%A6%86"
x = get_brief(url)
a = []
a.append(x)

exhibitions = []
print("------展览陈列------")
url = "http://www.sunyat-sen.org/index.php?m=content&c=index&a=lists&catid=396"
x = show(url)
exhibitions.append(x)
print("\n")

exhibition = {}
url = "http://www.sunyat-sen.org/index.php?m=content&c=index&a=show&catid=10&id=8"
home = "http://www.sunyat-sen.org"
soup = get_soup1(url)
div = soup.find('div',attrs={'class':'ng_box'})
title = div.find(attrs={'class':'conH3'})
#print(title.text)
exhibition["name"] = title.text
p = soup.find_all('p')
main = ""
for tag in p:
    main = main+tag.text
#print(main)
exhibition["description"] = main
img = div.find('img',attrs={'alt':''})
src = home+img["src"]
#print("展馆图示:"+src)
exhibition["img"] = src
exhibition["mname"] = "孙中山故居纪念馆"
print("\n")
exhibitions.append(exhibition)

def education(url,temp):
    edu = {}
    home = "http://www.sunyat-sen.org"
    soup = get_soup1(url)
    title = soup.find('h3',attrs={'class':'conH3'})
    #print(title.text)
    edu["name"] = title.text
    content = soup.find('div',attrs={'class':'ng_box'})
    p = soup.find_all('p')
    main = ""
    for tag in p:
        main = main+tag.text
    #print(main)
    edu["description"] = main
    img = soup.find_all('img',attrs={'width':'680'})
    i = 0
    for tag in img:
        i = i+1
        src = home+tag["src"]
        edu["img"] = src
        #print("活动写照:"+src)
        #if i == 3:
        break
    edu["mname"] = "孙中山故居纪念馆"
    edu["time"] = temp
    return edu

url = "http://www.sunyat-sen.org/index.php?m=content&c=index&a=show&catid=10&id=4"
x = show(url)
exhibitions.append(x)
print("\n")

collections = []
print("------典藏珍品------")
url = "http://www.sunyat-sen.org/index.php?m=content&c=index&a=show&catid=173&id=463"
temp = "孙中山书赠陆兰谷“博爱”横幅"
y = object(url,temp)
collections.append(y)
print("\n")
url = "http://www.sunyat-sen.org/index.php?m=content&c=index&a=show&catid=173&id=466"
temp = "孙中山在美国使用的电报稿复写本"
y = object(url,temp)
collections.append(y)
print("\n")
url = "http://www.sunyat-sen.org/index.php?m=content&c=index&a=show&catid=173&id=468"
temp = "容闳关于新政府运作等事致孙中山英文函"
y = object(url,temp)
collections.append(y)
print("\n")
url = "http://www.sunyat-sen.org/index.php?m=content&c=index&a=show&catid=173&id=467"
temp = "《美洲金山国民救济局革命军筹饷征信录》"
y = object(url,temp)
collections.append(y)
print("\n")
url = "http://www.sunyat-sen.org/index.php?m=content&c=index&a=show&catid=173&id=471"
temp = "飞南第贺孙中山当选中华民国临时大总统英文函"
y = object(url,temp)
collections.append(y)
print("\n")

educational = []
print("-----教育活动------")
url = "http://www.sunyat-sen.org/index.php?m=content&c=index&a=show&catid=76&id=4071"
temp = "发布时间：2016-11-19"
z = education(url,temp)
educational.append(z)
print("\n")
url = "http://www.sunyat-sen.org/index.php?m=content&c=index&a=show&catid=76&id=4300"
temp = "发布时间：2017-07-22"
z = education(url,temp)
educational.append(z)
print("\n")
url = "http://www.sunyat-sen.org/index.php?m=content&c=index&a=show&catid=76&id=4302"
temp = "发布时间：2017-07-22"
z = education(url,temp)
educational.append(z)
print("\n")


museum_info["1"] = []#a
museum_info["2"] = []#exhibitions
museum_info["3"] = []#collections
museum_info["4"] = educational

save_data(museum_info)