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
    brief["location"] = "武汉市武昌区武珞路1号"
    brief["number"] = "团队预约电话：027-88875305"
    brief["opentime"] = "周二至周日，每天9:00——17:00 （16:00停止入馆） 周一全天闭馆，国家法定节假日例外。" 
    return brief

def show(url):
    exhibition = {}
    soup = get_soup1(url)
    div = soup.find('div',attrs={'class':'maindetail'})
    title = div.find('div',attrs={'class':'title'})
    exhibition["name"] = title.text
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
        #print("展览图示:"+src)
        #if i ==3:
        break
    exhibition["mname"] = "辛亥革命武昌起义纪念馆"
    exhibition["img"] = ""
    return exhibition

def object(url):
    collection = {}
    soup = get_soup1(url)
    div = soup.find('div',attrs={'class':'maindetail'})
    title = div.find('div',attrs={'class':'title'})
    #print(title.text)
    collection["name"] = title.text
    p = div.find_all('p')
    main = ""
    for tag in p:
        main = main+tag.text
    #print(main)
    collection["description"] = main
    img = div.find_all('img')
    i = 0
    for tag in img:
        i = i+1
        src = tag["src"]
        collection["img"] = src
        #print("典藏图片:"+src)
        #if i ==3:
        break
    collection["mname"] = "辛亥革命武昌起义纪念馆"
    return collection

def education(url,temp):
    edu = {}
    soup = get_soup1(url)
    div = soup.find('div',attrs={'class':'maindetail'})
    title = div.find('div',attrs={'class':'title'})
    #print(title.text)
    edu["name"] = title.text
    img = div.find_all('img')
    i = 0
    for tag in img:
        i = i+1
        src = tag["src"]
        edu["img"] = src
        #print("活动写照:"+src)
        #if i == 5:
        break
    edu["time"] = temp
    edu["description"] = ""
    edu["mname"] = "辛亥革命武昌起义纪念馆"
    return edu

url = "https://baike.sogou.com/v156586.htm?fromTitle=%E8%BE%9B%E4%BA%A5%E9%9D%A9%E5%91%BD%E6%AD%A6%E6%98%8C%E8%B5%B7%E4%B9%89%E7%BA%AA%E5%BF%B5%E9%A6%86"
x = get_brief(url)
a = []
a.append(x)

exhibitions = []
print("------展览图示------")
url = "http://www.1911museum.com/Exhibition/Details/jbcl?nid=365"
x = show(url)
exhibitions.append(x)
print("\n")
url = "http://www.1911museum.com/Exhibition/Details/jbcl?nid=364"
x = show(url)
exhibitions.append(x)
print("\n")
url = "http://www.1911museum.com/Exhibition/Details/jbcl?nid=366"
x = show(url)
exhibitions.append(x)
print("\n")

collections = []
print("------典藏珍品------")
url = "http://www.1911museum.com/Collection/Details/zgww?nid=384"
y = object(url)
collections.append(y)
print("\n")
url = "http://www.1911museum.com/Collection/Details/jdmrsh?nid=401"
y = object(url)
collections.append(y)
print("\n")
url = "http://www.1911museum.com/Collection/Details/ghjnww?nid=407"
y = object(url)
collections.append(y)
print("\n")
url = "http://www.1911museum.com/Collection/Details/jdmrjp?nid=413"
y = object(url)
collections.append(y)
print("\n")
url = "http://www.1911museum.com/Collection/Details/shuhua?nid=420"
y = object(url)
collections.append(y)
print("\n")

educational = []
print("------教育活动------")
url = "http://www.1911museum.com/Activity/Details/JYHD?nid=1434"
temp = "时间：2018.01.31"
z = education(url,temp)
educational.append(z)
print("\n")
url = "http://www.1911museum.com/Activity/Details/JYHD?nid=1433"
temp = "时间：2018.01.31"
z = education(url,temp)
educational.append(z)
print("\n")
url = "http://www.1911museum.com/Activity/Details/JYHD?nid=1432"
temp = "时间：2018.01.31"
z = education(url,temp)
educational.append(z)
print("\n")

museum_info["1"] = a
museum_info["2"] = exhibitions
museum_info["3"] = collections
museum_info["4"] = educational

save_data(museum_info)