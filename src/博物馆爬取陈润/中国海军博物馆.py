import requests
import re
import bs4
from bs4 import BeautifulSoup
import bs4
import pymysql

#全局变量
global mid,eid,oid
mid = int(0)
eid = int(0)
oid = int(0)
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
    src = "http://www.hnzzmuseum.com/attached/upload/20190606131110823.jpg"
    print("------参观信息------")
    visit = soup.find('table',class_ ='abstract_tbl')
    info = visit.find_all('tr')
    #for tag in info:
        #title = tag.find('th',class_ = 'base-info-card-title')
        #print(title.text+":",end="")
        #texts = tag.find('div',class_ = 'base-info-card-value').find(text=True).strip()
        #print(texts)
    brief["name"] = "中国海军博物馆"
    brief["img"] = src
    brief["location"] = "地址：中国山东青岛市莱阳路八号"
    brief["number"] = "联系电话：0532-82866784"
    brief["opentime"] = "开放时间: 早8：30-晚17：30" 
    return brief

def show(url):
    exhibtion = {}
    home = "http://www.hjbwg.com/"
    soup = get_soup(url)
    span = soup.find('span',attrs={'class':'style8'})
    print(span.text)
    span1 = soup.find('span',attrs={'class':'style7'})
    print(span1.text)
    p = soup.find('p',attrs={'class':'style7'})
    print(p.text)
    img = soup.find('img',attrs={'width':'260'})
    src = home+img["src"]
    print("展览图示:"+src)

url = "https://baike.sogou.com/v108541.htm?fromTitle=%E4%B8%AD%E5%9B%BD%E6%B5%B7%E5%86%9B%E5%8D%9A%E7%89%A9%E9%A6%86"
x = get_brief(url)
a = []
a.append(x)

home = "http://www.hjbwg.com/"

exhibitions = []
#展览陈列
print("------展览陈列------")
x1 = {}
url = "http://www.hjbwg.com/101.html"
soup = get_soup(url)
span = soup.find('span',attrs={'class':'style8'})
#print(span.text)
x1["name"] = span.text
span1 = soup.find('span',attrs={'class':'style7'})
#print(span1.text)
p = soup.find('p',attrs={'class':'style7'})
#print(p.text)
x1["description"] = span1.text+p.text
img = soup.find('img',attrs={'width':'260'})
src = home+img["src"]
#print("展览图示:"+src)
x1["img"] = src
x1["mname"] = "中国海军博物馆"
print("\n")
exhibitions.append(x1)

x2 = {}
url = "http://www.hjbwg.com/105.html"
soup = get_soup(url)
span = soup.find('div',attrs={'class':'style8'})
#print(span.text)
x2["name"] = span.text
p = soup.find_all('p',attrs={'class':'style6'})
main = ""
for tag in p:
    main = main+tag.text
#print(main)
x2["description"] = main
img = soup.find('img',attrs={'width':'249'})
src = home+img["src"]
#print("展览图示:"+src)
x2["img"] = src
x2["mname"] = "中国海军博物馆"
print("\n")
exhibitions.append(x2)

x3 = {}
url = "http://www.hjbwg.com/008.html"
soup = get_soup(url)
span = soup.find('span',attrs={'class':'style8'})
#print(span.text)
x3["name"] = span.text
p = soup.find_all('p',attrs={'class':'style7'})
main = ""
for tag in p:
    main = main+tag.text
#print(main)
x3["description"] = main
img = soup.find('img',attrs={'width':'310'})
src = home+img["src"]
x3["img"] = src
x3["mname"] = "中国海军博物馆"
#print("展览图示:"+src)
print("\n")
exhibitions.append(x3)

x4 = {}
url = "http://www.hjbwg.com/007.html"
soup = get_soup(url)
span = soup.find('div',attrs={'class':'style8'})
#print(span.text)
x4["name"] = span.text
main = ""
p = soup.find_all('p',attrs={'class':'style10'})
for tag in p:
    main = main+tag.text
#print(main)
x4["description"] = main
img = soup.find('img',attrs={'width':'308'})
src = home+img["src"]
#print("展览图示:"+src)
x4["img"] = src
x4["mname"] = "中国海军博物馆"
print("\n")
exhibitions.append(x4)

museum_info["1"] = []#a
museum_info["2"] = exhibitions
museum_info["3"] = []#collections
museum_info["4"] = []#educational

save_data(museum_info)