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
    #img = div.find('img',attrs={'width':'250'})
    #src = img["src"]
    print("------参观信息------")
    visit = soup.find('table',class_ ='abstract_tbl')
    info = visit.find_all('tr')
    for tag in info:
        title = tag.find('th',class_ = 'base-info-card-title')
        #print(title.text+":",end="")
        texts = tag.find('div',class_ = 'base-info-card-value').find(text=True).strip()
        #print(texts)
    brief["name"] = "海南省地质博物馆"
    brief["img"] = "https://pic.baike.soso.com/ugc/baikepic2/21552/cut-20150611152115-159407651.jpg/0"
    brief["location"] = "地址：湖南省长沙市天心区杉木冲西路49号 "
    brief["number"] = "电话:0731-89991350"
    brief["opentime"] = "开放时间：周二至周日9：00至16：30，周一闭馆。" 
    return brief

def visit(url):
    soup = get_soup1(url)
    div = soup.find('div',attrs={'class':'site-infos'})
    visit = div.text
    print(visit)

def show(url):
    exhibition = {}
    home = "http://www.hndzbwg.com"
    soup = get_soup1(url)
    div = soup.find('div',attrs={'id':'imgContent'})
    title = div.find('span',attrs={'class':'imageDescription'})
    #print(title.text)
    exhibition["name"] = (title.text).strip()
    main = soup.find('div',attrs={'class':'detail-body'})
    #print(main.text)
    exhibition["description"] = main.text
    div = soup.find('div',attrs={'id':'smallImgContent'})
    img = div.find_all('img')
    i = 0
    for tag in img:
        i = i+1
        src = home+tag["src"]
        exhibition["img"] = src
        #print("展览图示:"+src)
        #if i == 4:
        break
    exhibition["mname"] = "湖南省地质博物馆"
    return exhibition

def object(url):
    collection = {}
    home = "http://www.hndzbwg.com"
    soup = get_soup1(url)
    div = soup.find('div',attrs={'id':'imgContent'})
    brief = div.find('span',attrs={'class':'imageDescription'})
    collection["description"] = brief.text
    #print(brief.text)
    div = soup.find('div',attrs={'id':'smallImgContent'})
    img = div.find_all('img')
    i = 0
    for tag in img:
        i = i+1
        src = home+tag["src"]
        collection["img"] = src
        #print("藏品图示:"+src)
        #if i == 2:
        break
    collection["mname"] = "湖南省地质博物馆"
    return collection

def education(url):
    edu = {}
    home = "http://www.hndzbwg.com"
    soup = get_soup1(url)
    div = soup.find('div',attrs={'class':'detail-body'})
    main = div.text
    #print(main)
    edu["description"] = main
    img = div.find_all('img')
    i = 0
    for tag in img:
        i = i+1
        src = tag["src"]
        edu["img"] = src
        #print("活动图示:"+src)
        #if i == 3:
        break
    edu["mname"] = "湖南省地质博物馆"
    return edu

url = "https://baike.sogou.com/v8218202.htm?fromTitle=%E6%B9%96%E5%8D%97%E5%9C%B0%E8%B4%A8%E5%8D%9A%E7%89%A9%E9%A6%86"
x = get_brief(url)
a = []
a.append(x)

url = "http://www.hndzbwg.com/"
visit(url)

exhibitions = []
print("------展览陈列------")
url = "http://www.hndzbwg.com/zhanting/detail/262.html"
x = show(url)
exhibitions.append(x)
print("\n")
url = "http://www.hndzbwg.com/zhanting/detail/263.html"
x = show(url)
exhibitions.append(x)
print("\n")
url = "http://www.hndzbwg.com/zhanting/detail/265.html"
x = show(url)
exhibitions.append(x)
print("\n")

collections = []
print("------典藏珍品------")
url = "http://www.hndzbwg.com/product/detail/299.html"
y = object(url)
y["name"] = "萤石"
collections.append(y)
print("\n")
url = "http://www.hndzbwg.com/product/detail/346.html"
y = object(url)
y["name"] = "硫锑铅矿"
collections.append(y)
print("\n")
url = "http://www.hndzbwg.com/product/detail/369.html"
y = object(url)
y["name"] = "赤铜、斑铜"
collections.append(y)
print("\n")
url = "http://www.hndzbwg.com/product/detail/318.html"
y = object(url)
y["name"] = "玻璃陨石"
collections.append(y)
print("\n")
url = "http://www.hndzbwg.com/product/detail/316.html"
y = object(url)
y["name"] = "石陨石"
collections.append(y)
print("\n")

educational = []
print("------教育活动------")
url = "http://www.hndzbwg.com/news/detail/644.html"
z = education(url)
z["name"] = "爱地球·看我的”省地质博物馆开展“422世界地球日”系列活动"
z["time"] = "发布时间：2020-05-06"
educational.append(z)
print("\n")
url = "http://www.hndzbwg.com/news/detail/636.html"
z = education(url)
z["name"] = "省地质博物馆开展地下水防治主题科普宣传系列活动"
z["time"] = "发布时间：2020-04-08"
educational.append(z)
print("\n")
url = "http://www.hndzbwg.com/news/detail/593.html"
z = education(url)
z["name"] = "地质博物馆开展道德讲堂活动"
z["time"] = "发布时间：2019-12-05"
educational.append(z)
print("\n")

museum_info["1"] = a
museum_info["2"] = []#exhibitions
museum_info["3"] = []#collections
museum_info["4"] = []#educational

save_data(museum_info)