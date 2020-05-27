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
    brief["name"] = "海南省博物馆"
    brief["img"] = src
    brief["location"] = "联系地址：中国海南海口市国兴大道68号"
    brief["number"] = "电话：65238880 "
    brief["opentime"] = "开放时间：周二至周日9:00-17:00(16:30停止入馆)，周一闭馆整休。" 
    return brief


def show(url):
    home = "http://www.hainanmuseum.org/"
    exhibitions = {}
    soup = get_soup1(url)
    title = soup.find('div',attrs={'class':'title'})
   # print(title.text)
    span = soup.find_all('span')
    main = ""
    for tag in span:
        main = main+tag.text
   # print(main)
    img = soup.find_all('img',attrs={'alt':''})
    i = 0
    for tag in img:
        i = i+1
        src = home+tag["src"]
        exhibitions["img"] = src
       # print("展览图示:"+src)
        if i == 4:
            break

    exhibitions["name"] = (title.text).strip()
    exhibitions["description"] = main
    exhibitions["mname"] = "海南省博物馆"
    return exhibitions

def objects(url):
    collections = {}
    home = "http://www.hainanmuseum.org/"
    soup = get_soup1(url)
    div = soup.find('div',attrs={'class':'lan fix'})
    p = div.find_all('p')
    main = ""
    for tag in p:
        main = main+tag.text
   # print(main)
    img = soup.find('img',attrs={'alt':''})
    src = home+img["src"]
   # print("藏品图片:"+src)
    collections["name"] = "有孔石刀"
    collections["description"] = main
    collections["img"] = src
    collections["mname"] = "海南省博物馆"
    return collections

def education(url):
    edu = {}
    home = "http://www.hainanmuseum.org"
    soup = get_soup1(url)
    title = soup.find('div',attrs={'class':'title'})
   # print(title.text)
    edu["name"] = (title.text).strip()
    time = soup.find('span',attrs={'class':'time'})
   # print(time.text)
    edu["time"] = (time.text).strip()
    div = soup.find('div',attrs={'class':'article_cont'})
    span = div.find_all('span')
    main = ""
    for tag in span:
        main = main+tag.text
   # print(main)
    edu["description"] = main
    img = div.find_all('img')
    edu["img"] = ""
    i = 0
    for tag in img:
        i = i+1
        src = home+tag["src"]
        edu["img"] = src
       # print("活动写照:"+src)
        if i == 3:
            break
    edu["mname"] = "海南省博物馆"
    return edu

url = "https://baike.sogou.com/v162974.htm?fromTitle=%E6%B5%B7%E5%8D%97%E7%9C%81%E5%8D%9A%E7%89%A9%E9%A6%86"
x = get_brief(url)
a = []
a.append(x)
museum_info["1"] = a


print("------展览陈列------")
exhibition_hall = []
url = "http://www.hainanmuseum.org/zlhd/view/?tag_id=1&aid=9"
a = show(url)
print(a)
exhibition_hall.append(a)
print("\n")
url = "http://www.hainanmuseum.org/zlhd/view/?tag_id=1&aid=8"
a = show(url)
exhibition_hall.append(a)
print("\n")
url = "http://www.hainanmuseum.org/zlhd/view/?tag_id=1&aid=2"
a = show(url)
exhibition_hall.append(a)
print("\n")

museum_info["2"] = []#exhibition_hall

print("------典藏珍品------")
collection = []
url = "http://www.hainanmuseum.org/gcjp/view/?classid=2"
x = objects(url)
collection.append(x)
print("\n")
url = "http://www.hainanmuseum.org/gcjp/view/?classid=3"
x = objects(url)
x["name"] = "唐三彩马"
collection.append(x)
print("\n")
url = "http://www.hainanmuseum.org/gcjp/view/?classid=4"
x = objects(url)
x["name"] = "越王亓北古”错金铭文青铜复合剑"
collection.append(x)
print("\n")
url = "http://www.hainanmuseum.org/gcjp/view/?classid=5"
x = objects(url)
x["name"] = "无款《松鹤图》轴"
collection.append(x)
print("\n")
url = "http://www.hainanmuseum.org/gcjp/view/?classid=7"
x = objects(url)
x["name"] = "巨猿右下第一臼齿化石、猩猩牙齿化石"
collection.append(x)

museum_info["3"] = []#collection

print("------教育活动------")
educations = []
url = "http://www.hainanmuseum.org/xwdt/view/?tag_id=1&aid=571"
y = education(url)
educations.append(y)
print("\n")
url = "http://www.hainanmuseum.org/xwdt/view/?tag_id=1&aid=587"
y = education(url)
educations.append(y)
print("\n")
url = "http://www.hainanmuseum.org/xwdt/view/?tag_id=1&aid=542"
y = education(url)
educations.append(y)
print("\n")

museum_info["4"] = []#educations

#print(museum_info)
save_data(museum_info)