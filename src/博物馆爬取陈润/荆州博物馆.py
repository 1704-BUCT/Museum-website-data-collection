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
    brief["name"] = "荆州博物馆"
    brief["img"] = src
    brief["location"] = " 地址：湖北省荆州市荆中路166号"
    brief["number"] = "电话：0716-8494808"
    brief["opentime"] = "周二至周日上午 9:00 开馆 16:00 停止发票 17:00 闭馆 周一闭馆" 
    return brief

def visit(url):
    soup = get_soup1(url)
    div = soup.find('div',attrs={'class':'yk_foot'})
    td = div.find('td',attrs={'valign':'middle'})
    visit = td.text
    print(visit)

def show(url):
    exhibition = {}
    home = "http://www.jzmsm.org"
    soup = get_soup1(url)
    div = soup.find('div',attrs={'gbxs'})
    main = ""
    content = div.find_all('div',attrs={'class':'content'})
    for tag in content:
        exhibition["name"] = (tag.text).strip()
        break
    for tag in content:
        main = main+tag.text
    #print(main)
    exhibition["description"] = main
    img = div.find_all('img')
    i = 0
    for tag in img:
        i = i+1
        src =home+tag["src"]
        exhibition["img"] = src
        #print("展览图示:"+src)
        #if i == 3:
        break
    exhibition["mname"] = "荆州博物馆"
    return exhibition

def object(url):
    collection = {}
    home = "http://www.jzmsm.org"
    soup = get_soup1(url)
    div = soup.find('div',attrs={'gbxs'})
    main = ""
    content = div.find_all('p')
    for tag in content:
        collection["name"] = (tag.text).strip()
        break
    for tag in content:
        main = main+tag.text
    #print(main)
    collection["description"] = main
    img = div.find_all('img')
    i = 0
    for tag in img:
        i = i+1
        src =home+tag["src"]
        collection["img"] = src
        #print("藏品图片:"+src)
        #if i == 3:
        break
    collection["mname"] = "荆州博物馆"
    return collection

def education(url):
    edu = {}
    home = "http://www.jzmsm.org"
    soup = get_soup1(url)
    div = soup.find('div',attrs={'gbxs'})
    main = ""
    content = div.find_all('div',attrs={'class':'content'})
    for tag in content:
        edu["name"] = (tag.text).strip()
        break
    for tag in content:
        main = main+tag.text
    #print(main)
    edu["description"] = main
    edu["mname"] = "荆州博物馆"
    img = div.find_all('img')
    i = 0
    for tag in img:
        i = i+1
        src =home+tag["src"]
        edu["img"] = src
        #print("活动写照:"+src)
        #if i == 3:
        break
    return edu

url = "https://baike.sogou.com/v11025957.htm?fromTitle=%E8%8D%86%E5%B7%9E%E5%8D%9A%E7%89%A9%E9%A6%86"
x = get_brief(url)
a = []
a.append(x)

url = "http://www.jzmsm.org/yk/"
visit(url)

exhibitions = []
print("------展览陈列------")
url = "http://www.jzmsm.org/yk/zhanlan/linshizhanlan/2019-11-18/1689.html"
x = show(url)
exhibitions.append(x)
print("\n")
url = "http://www.jzmsm.org/yk/zhanlan/linshizhanlan/2019-05-01/1631.html"
x = show(url)
exhibitions.append(x)
print("\n")
url = "http://www.jzmsm.org/yk/zhanlan/linshizhanlan/2019-05-01/1630.html"
x = show(url)
exhibitions.append(x)
print("\n")

collections = []
print("------典藏珍品------")
url = "http://www.jzmsm.org/yk/cangpin/guobaoxinshang/qingtongqi/2017-08-21/923.html"
y = object(url)
collections.append(y)
print("\n")
url = "http://www.jzmsm.org/yk/cangpin/guobaoxinshang/qingtongqi/2017-08-21/924.html"
y = object(url)
collections.append(y)
print("\n")
url = "http://www.jzmsm.org/yk/cangpin/guobaoxinshang/qingtongqi/2017-08-21/927.html"
y = object(url)
collections.append(y)
print("\n")
url = "http://www.jzmsm.org/yk/cangpin/guobaoxinshang/qingtongqi/2017-08-21/933.html"
y = object(url)
collections.append(y)
print("\n")
url = "http://www.jzmsm.org/yk/cangpin/guobaoxinshang/qingtongqi/2017-08-21/992.html"
y = object(url)
collections.append(y)
print("\n")

educational = []
print("------教育活动------")
url = "http://www.jzmsm.org/yk/huodong1/2019-11-18/1688.html"
z = education(url)
z["time"] = "发布时间：2019-11-18"
educational.append(z)
print("\n")
url = "http://www.jzmsm.org/yk/huodong1/2019-10-16/1679.html"
z = education(url)
z["time"] = "发布时间：2019-10-16"
educational.append(z)
print("\n")
url = "http://www.jzmsm.org/yk/huodong1/2019-07-30/1657.html"
z = education(url)
z["time"] = "发布时间：2019-07-29"
educational.append(z)
print("\n")

museum_info["1"] = []#a
museum_info["2"] = exhibitions
museum_info["3"] = []#collections
museum_info["4"] = educational

save_data(museum_info)