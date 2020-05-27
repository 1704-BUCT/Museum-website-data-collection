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
    brief["name"] = "南昌八一起义纪念馆"
    brief["img"] = src
    brief["location"] = "江西省南昌市中山路380号 "
    brief["number"] = "0791 - 86613806"
    brief["opentime"] = "星期二到星期日，每天9:00 ~ 17:00;星期一闭馆，设备检修。" 
    return brief

def show(url,temp):
    exhibition = {}
    home = "http://www.81-china.com"
    soup = get_soup(url)
    table = soup.find('div',attrs={'class':'detial_txt'})
    span = table.find_all('span')
    main = ""
    for tag in span:
        main = main+tag.text
    #print(main)
    exhibition["description"] = main
    body = soup.find("div",attrs={'class':'bodycon'})
    img = body.find("img")
    src = home+img["src"] #展览连接
    #print("展览图示:"+src)
    exhibition["img"] = src
    exhibition["mname"] = "南昌八一起义纪念馆"
    exhibition["name"] = temp
    return exhibition

def object(url,temp):
    collection = {}
    home = "http://www.81-china.com"
    soup = get_soup(url)
    table = soup.find('div',attrs={'class':'detial_txt'})
    span = table.find_all('p')
    main = ""
    for tag in span:
        main = main+tag.text
    #print(main)
    collection["description"] = main
    body = soup.find("div",attrs={'class':'bodycon'})
    img = body.find("img")
    src = home+img["src"]
    collection["img"] = src
    collection["name"] = temp
    collection["mname"] = "南昌八一起义纪念馆"
    #print("典藏图片:"+src)
    return collection

def education(url,temp,time):
    edu = {}
    home = "http://www.81-china.com"
    soup = get_soup(url)
    table = soup.find('div',attrs={'class':'detial_txt'})
    span = table.find_all('p')
    main = ""
    for tag in span:
        main = main+tag.text
    #print(main)
    edu["description"] = main
    body = soup.find("div",attrs={'class':'bodycon'})
    img = body.find("img")
    src = home+img["src"]
    #print("活动写照:"+src)
    edu["img"] = src
    edu["name"] = temp
    edu["mname"] = "南昌八一起义纪念馆"
    edu["time"] = time
    return edu

url = "https://baike.sogou.com/v2442777.htm?fromTitle=%E5%8D%97%E6%98%8C%E5%85%AB%E4%B8%80%E8%B5%B7%E4%B9%89%E7%BA%AA%E5%BF%B5%E9%A6%86"
x = get_brief(url) #获取博物馆基本信息
a = []
a.append(x)

#展览陈列
exhibitions = []
print("-----展览陈列-----")
url = "http://www.81-china.com/zhanlan/show-206.html"
temp = "危难中愤起"
x = show(url,temp)
exhibitions.append(x)
print("\n")
url = "http://www.81-china.com/zhanlan/show-207.html"
temp = "伟大的决策"
x = show(url,temp)
exhibitions.append(x)
print("\n")
url = "http://www.81-china.com/zhanlan/show-209.html"
temp = "南征下广东"
x = show(url,temp)
exhibitions.append(x)
print("\n")

collections = []
#典藏珍品
print("-----典藏珍品------")
url = "http://www.81-china.com/collect/show-132.html"
temp = "麦秆剪贴书法作品"
y = object(url,temp)
collections.append(y)
print("\n")
url = "http://www.81-china.com/collect/show-131.html"
temp = "方祖岐诗词书法作品一幅 "
y = object(url,temp)
collections.append(y)
print("\n")
url = "http://www.81-china.com/collect/show-129.html"
temp = "抗震救灾纪念章 "
y = object(url,temp)
collections.append(y)
print("\n")
url = "http://www.81-china.com/collect/show-126.html"
temp = " 周恩来送给魔术师的手表"
y = object(url,temp)
collections.append(y)
print("\n")
url = "http://www.81-china.com/collect/show-130.html"
temp = "王玲剪纸作品"
y = object(url,temp)
collections.append(y)
print("\n")

educational = []
print("------教育活动------")
url = "http://www.81-china.com/service/show-432.html"
temp = "南昌八一起义纪念馆寒假高中生社会实践活动"
time = ""
z = education(url,temp,time)
educational.append(z)
print("\n")
url = "http://www.81-china.com/service/show-390.html"
temp = "南昌八一起义纪念馆全国中小学生研学实践基地课程"
time = ""
z = education(url,temp,time)
educational.append(z)
print("\n")
url = "http://www.81-china.com/service/show-449.html"
temp = "4月25日周恩来的故事走进邮政路小学"
time = "2018年4月25日"
z = education(url,temp,time)
educational.append(z)
print("\n")

museum_info["1"] = a
museum_info["2"] = exhibitions
museum_info["3"] = collections
museum_info["4"] = educational

save_data(museum_info)