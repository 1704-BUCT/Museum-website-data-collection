import requests
import re
import bs4
from bs4 import BeautifulSoup
import bs4
import pymysql

headers = {
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

museum_info = {}
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
    img = div.find('img',attrs={'title':'安源路矿工人运动纪念馆'})
    src = img["src"]
    print("------参观信息------")
    visit = soup.find('table',class_ ='abstract_tbl')
    info = visit.find_all('tr')
    for tag in info:
        title = tag.find('th',class_ = 'base-info-card-title')
        #print(title.text+":",end="")
        texts = tag.find('div',class_ = 'base-info-card-value').find(text=True).strip()
        #print(texts)
    brief["name"] = "安源路矿工人运动纪念馆"
    brief["img"] = src
    brief["location"] = "江西省萍乡市安源区安源镇"
    brief["number"] = "服务热线：0799-7101123"
    brief["opentime"] = "开放日期：星期二至星期日   星期一闭馆检修 参观时间：夏季9:00——17:30（17:00停止入内） 冬季9:00——17:00（16:30停止入内）" 
    return brief

def show(url):
    exhibition = {}
    soup = get_soup(url)
    main = ""
    div = soup.find_all('div',attrs={'class':'newsDetail'})
    for tag in div:
        for x in tag.find_all('p'):
            main =main+x.text
    exhibition["description"] = main
    #print(main)
    p = soup.find('p',attrs={'style':'line-height:1.9em;text-indent:0em;text-align:center;'})
    img = p.find('img')
    src = img["src"]
    exhibition["img"] = src
    exhibition["mname"] = "安源路矿工人运动纪念馆"
    exhibition["name"] = ""
    #print("展览图示:"+src)
    return exhibition

def object(url):
    collection = {}
    soup = get_soup(url)
    title = soup.find('title')
    collection["name"] = (title.text).strip()
    #print(title.text)
    main = ""
    div = soup.find_all('div',attrs={'class':'newsDetail'})
    for tag in div:
        for x in tag.find_all('p'):
            main =main+x.text
    collection["description"] = main
    #print(main)
    p = soup.find('p',attrs={'style':'line-height:1.9em;text-indent:0em;text-align:center;'})
    img = p.find('img')
    src = img["src"]
    collection["img"] = src
    collection["mname"] = "安源路矿工人运动纪念馆"
    #print("典藏图片:"+src)
    return collection
    
def education(url):
    edu = {}
    soup = get_soup(url)
    title = soup.find('title')
    edu["name"] = (title.text).strip()
    #print(title.text)
    main = ""
    div = soup.find_all('div',attrs={'class':'newsDetail'})
    for tag in div:
        for x in tag.find_all('p'):
            main =main+x.text
    #print(main)
    edu["description"] = main
    edu["img"] = ""
    edu["mname"] = "安源路矿工人运动纪念馆"
    return edu

url = "https://baike.sogou.com/v4570962.htm?fromTitle=安源路矿工人运动纪念馆"
x = get_brief(url)
a = []
a.append(x)

exhibition_hall = []
#展览陈列
print("------展览陈列------")
url = "http://www.aymuseum.com/nd.jsp?id=765#_jcp=4_77"
x = show(url)
x["name"] = "安源路矿工人运动纪念馆陈列大楼"
exhibition_hall.append(x)
print("\n")
url = "http://www.aymuseum.com/nd.jsp?id=756#_jcp=4_77"
x = show(url)
x["name"] = "安源路矿工人大罢工谈判处旧址 ——萍乡煤矿公务总汇"
exhibition_hall.append(x)
print("\n")
url = "http://www.aymuseum.com/nd.jsp?id=757#_jcp=4_77"
x = show(url)
x["name"] = "秋收起义军事会议旧址暨中共安源地委党校旧址"
exhibition_hall.append(x)
print("\n")

print(exhibition_hall)

#典藏珍品
collections = []
print("------典藏珍品------")
url = "http://www.aymuseum.com/nd.jsp?id=770#_jcp=4_2"
y = object(url)
collections.append(y)
print("\n")
url = "http://www.aymuseum.com/nd.jsp?id=769#_jcp=4_2"
y = object(url)
collections.append(y)
print("\n")
url = "http://www.aymuseum.com/nd.jsp?id=768#_jcp=4_2"
y = object(url)
collections.append(y)
print("\n")
url =("http://www.aymuseum.com/nd.jsp?id=767#_jcp=4_2")
y = object(url)
collections.append(y)
print("\n")
url = "http://www.aymuseum.com/nd.jsp?id=766#_jcp=4_2"
y = object(url)
collections.append(y)
print("\n")


educations = []
print("------教育活动------")
url = "http://www.aymuseum.com/nd.jsp?id=1473#_jcp=4_4"
z = education(url)
z["time"] = "2020-3-4"
educations.append(z)
print("\n")
url = "http://www.aymuseum.com/nd.jsp?id=1235#_jcp=4_4"
z = education(url)
z["time"]  = "2020-2-26"
educations.append(z)
print("\n")
url = "http://www.aymuseum.com/nd.jsp?id=1141#_jcp=4_4"
z = education(url)
z["time"] = "2019-12-13"
educations.append(z)
print("\n")

museum_info["1"] = a
museum_info["2"] = []#exhibition_hall
museum_info["3"] = []#collections
museum_info["4"] = []#educations

save_data(museum_info)