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
    brief["name"] = "洛阳博物馆"
    brief["img"] = src
    brief["location"] = " 洛博馆址：河南省洛阳市洛龙区聂泰路"
    brief["number"] = "电话:0379-69901020"
    brief["opentime"] = "周一闭馆，周二至周日9点到17点开放，16点30分清场。" 
    return brief

def visit(url):
    soup = get_soup(url)
    for script in soup.find_all('script'): #去除script标签
        script.extract()
    div = soup.find('div',attrs={'id':'bencandy_box'})
    p = div.find('p')
    print(p.text)

def show(url,href):
    exhibition = {}
    soup = get_soup(url)
    div = soup.find('div',attrs={'id':'bencandy_box'})
    title = div.find('td',attrs={'style':'font-size:18px;font-weight:bold;padding-left:5px;padding-top:2px;color:#693a06;'})
    exhibition["name"] = title.text
    #print(title.text)
    span = div.find('span',attrs={'style':'font-size:16px;'})
    #print(span.text)
    exhibition["description"] = span.text
    soup = get_soup(href)
    img = soup.find("img")
    src = img["src"]
    #print("展览图示:"+src)
    exhibition["img"] = src
    exhibition["mname"] = "洛阳博物馆"
    return exhibition

def object(url):
    collection = {}
    soup = get_soup(url)
    div = soup.find('div',attrs={'id':'bencandy_box'})
    title = div.find('div',attrs={'style':'font-size:16px; font-weight:bold;color:#3c3c3c;'})
    #print(title.text)
    collection["name"] = title.text
    span = div.find_all('span',attrs={'style':'font-size:16px;'})
    main = ""
    for tag in span:
        main = main+tag.text
    #print(main)
    collection["description"] = main
    img = div.find('img')
    src = img["src"]
    #print("藏品图片:"+src)
    collection["img"] = src
    collection["mname"] = "洛阳博物馆"
    return collection

def education(url):
    edu  = {}
    soup = get_soup(url)
    div = soup.find('div',attrs={'id':'bencandy_box'})
    title = div.find('div',attrs={'style':'font-size:16px; font-weight:bold;color:#3c3c3c;'})
    #print(title.text)
    edu["name"] = title.text
    span = div.find_all('span',attrs={'style':'margin: 0px; padding: 0px; font-size: 16px; line-height: 32px;'})
    main = ""
    for tag in span:
        main = main+tag.text
    #print(main)
    edu["description"] = main
    img = div.find('img')
    src = img["src"]
    #print("活动写照:"+src)
    edu["img"] = src
    edu["mname"] = "洛阳博物馆"
    return edu

url = "https://baike.sogou.com/v163124.htm?fromTitle=%E6%B4%9B%E9%98%B3%E5%8D%9A%E7%89%A9%E9%A6%86"
x = get_brief(url)
a = []
a.append(x)

url = "http://www.lymuseum.com/list.php?fid=79"
visit(url)
print("\n")

exhibitions = []
print("------展览陈列------")
url = "http://www.lymuseum.com/bencandy.php?fid=60&id=37"
href = "http://www.lymuseum.com/list.php?fid=60"
x = show(url,href)
exhibitions.append(x)
print("\n")
url = "http://www.lymuseum.com/bencandy.php?fid=61&id=58"
href = "http://www.lymuseum.com/list.php?fid=61"
x = show(url,href)
exhibitions.append(x)
print("\n")
url = "http://www.lymuseum.com/bencandy.php?fid=63&id=1400"
href = "http://www.lymuseum.com/list.php?fid=63"
x = show(url,href)
exhibitions.append(x)
print("\n")

collections = []
print("------典藏珍品------")
url = "http://www.lymuseum.com/bencandy.php?fid=46&id=272"
y = object(url)
collections.append(y)
print("\n")
url = "http://www.lymuseum.com/bencandy.php?fid=44&id=278"
y = object(url)
collections.append(y)
print("\n")
url = "http://www.lymuseum.com/bencandy.php?fid=45&id=302"
y = object(url)
collections.append(y)
print("\n")
url = "http://www.lymuseum.com/bencandy.php?fid=47&id=305"
y = object(url)
collections.append(y)
print("\n")
url = "http://www.lymuseum.com/bencandy.php?fid=49&id=310"
y = object(url)
collections.append(y)
print("\n")

educational = []
print("------教育活动------")
url = "http://www.lymuseum.com/bencandy.php?fid=71&id=1438"
z = education(url)
z["time"] = "发表时间:2020-04-17"
print("\n")

edu1 = {}
url = "http://www.lymuseum.com/bencandy.php?fid=69&id=1434"
soup = get_soup(url)
div = soup.find('div',attrs={'id':'bencandy_box'})
title = div.find('div',attrs={'style':'font-size:16px; font-weight:bold;color:#3c3c3c;'})
#print(title.text)
edu1["name"] = title.text
span = div.find_all('span',attrs={'style':'font-size: 16px;'})
main = ""
for tag in span:
    main = main+tag.text
#print(main)
edu1["description"] = main
img = div.find('img')
src = img["src"]
edu1["img"] = src
edu1["mname"] = "洛阳博物馆"
edu1["time"] = "发表时间:2020-04-15"
#print("活动写照:"+src)
educational.append(edu1)
print("\n")

edu2 = {}
url = "http://www.lymuseum.com/bencandy.php?fid=70&id=801"
soup = get_soup(url)
div = soup.find('div',attrs={'id':'bencandy_box'})
title = div.find('div',attrs={'style':'font-size:16px; font-weight:bold;color:#3c3c3c;'})
#print(title.text)
edu2["name"] = title.text
span = div.find_all('font',attrs={'size':'4'})
main = ""
for tag in span:
    main = main+tag.text
#print(main)
edu2["description"] = main
img = div.find('img')
src = img["src"]
edu2["img"] = src
#print("活动写照:"+src)
edu2["mname"] = "洛阳博物馆"
edu2["time"] = "发表时间:2017-04-01"
educational.append(edu2)
print("\n")

museum_info["1"] = a
museum_info["2"] = exhibitions
museum_info["3"] = collections
museum_info["4"] = educational

save_data(museum_info)