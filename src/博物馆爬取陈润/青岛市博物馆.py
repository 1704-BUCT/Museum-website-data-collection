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
    brief["name"] = "青岛市博物馆"
    brief["img"] = src
    brief["location"] = "中国山东省 青岛市崂山区梅岭东路51号"
    brief["number"] = "0532-8889 6286"
    brief["opentime"] = "月至10月 Am9：00~Pm17：00（Pm16：30停止入场）  11月至次年4月 Am9：00~16：30（Pm16：00停止入场）  每周一闭馆（法定节假日除外）" 
    return brief

def show(url,temp): #展览
    exhibition = {}
    soup = get_soup(url)
    div = soup.find(name='div',attrs={'class':'hd_n'})
    p = div.find_all('p')
    main = ""
    for tag in p:
        main = main+tag.text
    exhibition["description"] = main
    li = div.find_all('li')
    for tag in li:
        a =tag.find('a')
        src = a["href"]
        #print("展览图示:"+src)
        exhibition["img"] = src
        break
    exhibition["name"] = temp
    exhibition["mname"] = "青岛市博物馆"
    return exhibition

def object(url):
    collection = {}
    soup = get_soup(url)
    div = soup.find(name='div',attrs={'class':'wccp_n'})
    title = div.find('h3',attrs={'text-center'})
    #print(title.text)
    collection["name"] = title.text
    p = div.find_all('p')
    main = ""
    for tag in p:
        main = main+tag.text
    collection["description"] = main
    wrapper = div.find('div',attrs={'class':'wrapper'})
    img = wrapper.find_all('img')
    for tag in img:
        src = tag["src"]
        #print("典藏图片:"+src)
        collection["img"] = src
        break
    collection["mname"] = "青岛市博物馆"
    return collection

def education(url,temp,time): #教育活动
    edu = {}
    soup = get_soup(url)
    div = soup.find(name='div',attrs={'class':'hd_n'})
    p = div.find_all('p')
    main = ""
    for tag in p:
        #print(tag.text)
        main = main+tag.text
    edu["description"] = main
    li = div.find_all('li')
    src = ""
    for tag in li:
        a =tag.find('a')
        src = a["href"]
        #print("活动写照:"+src)
        break
    edu["mname"] = "青岛市博物馆"
    edu["name"] = temp
    edu["time"] = time
    edu["img"] = src
    return edu

url = "https://baike.sogou.com/v154424.htm?fromTitle=%E9%9D%92%E5%B2%9B%E5%B8%82%E5%8D%9A%E7%89%A9%E9%A6%86"
x = get_brief(url)
a = []
a.append(x)

exhibitions = []
#展览图示
print("-----展览陈列------")
url = "http://www.qingdaomuseum.com/exhibition/detail/432"
temp = "青岛史话——青岛地区历史陈列》上部《古韵悠长》"
x = show(url,temp)
exhibitions.append(x)
print("\n")
url = "http://www.qingdaomuseum.com/exhibition/detail/431"
temp = "《青岛史话——青岛地区历史陈列》下部《岁月回眸》"
x = show(url,temp)
exhibitions.append(x)
print("\n")
url = "http://www.qingdaomuseum.com/exhibition/detail/430"
temp = "《彩瓷聚珍——馆藏明清瓷器陈列》"
x = show(url,temp)
exhibitions.append(x)
print("\n")
url = "http://www.qingdaomuseum.com/exhibition/detail/429"
temp = "《古钱今说——馆藏古代钱币陈列》"
x = show(url,temp)
exhibitions.append(x)
print("\n")

collections = []
#典藏珍品
url = "http://www.qingdaomuseum.com/collection/detail/198"
y = object(url)
collections.append(y)
print("\n")
url = "http://www.qingdaomuseum.com/collection/detail/280"
y = object(url)
collections.append(y)
print("\n")
url = "http://www.qingdaomuseum.com/collection/detail/278"
y = object(url)
collections.append(y)
print("\n")
url = "http://www.qingdaomuseum.com/collection/detail/208"
y = object(url)
collections.append(y)
print("\n")
url = "http://www.qingdaomuseum.com/collection/detail/241"
y = object(url)
collections.append(y)
print("\n")

educational = []
#教育活动
print("------教育活动------")
url = "http://www.qingdaomuseum.com/education/detail/490"
temp = "精彩展教 献礼国庆70周年"
time = "2019-09-26"
z = education(url,temp,time)
educational.append(z)
print("\n")
url = "http://www.qingdaomuseum.com/education/detail/486"
temp = "传奇偶戏”点亮青博之夜"
time = "2019-09-01"
z = education(url,temp,time)
educational.append(z)
print("\n")
url = "http://www.qingdaomuseum.com/education/detail/474"
temp = "2019文博研学夏令营之独“剧”匠心营日记（一）"
time = "2019-07-23"
z = education(url,temp,time)
educational.append(z)

museum_info["1"] = []#a
museum_info["2"] = []#exhibitions
museum_info["3"] = []#collections
museum_info["4"] = educational

save_data(museum_info)