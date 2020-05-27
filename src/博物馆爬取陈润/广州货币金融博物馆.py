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
    brief["name"] = "广州货币金融博物馆"
    brief["img"] = src
    brief["location"] = "博物馆地址：广州市天河区龙洞广东金融学院图书馆5、6楼 "
    brief["number"] = "联系电话：020-37216839 020-37216805"
    brief["opentime"] = "周一到周五（寒暑假除外）8：00--16：30 个人参观请于每个月的免费开放日前来参观" 
    return brief

def show(url):
    exhibition = {}
    soup = get_soup1(url)
    title = soup.find('div',attrs={'class':'tit'})
    exhibition["name"] = (title.text).strip()
    #print(title.text)
    div = soup.find('div',attrs={'class':'p'})
    exhibition["description"] = div.text
    exhibition["mname"] = "广州货币金融博物馆"
    exhibition["img"] = ""
    return exhibition
    #print(div.text)

def object(url):
    collection = {}
    home = "https://hbg.gduf.edu.cn"
    soup = get_soup1(url)
    div = soup.find('div',attrs={'class':'cen'})
    collection["name"] = div.text
    #print(div.text)
    img = soup.find('img',attrs={'alt':''})
    src = home+img["src"]
    collection["img"] = src
    #print("藏品图示:"+src)
    collection["description"] = ""
    collection["mname"] = "广州货币金融博物馆"
    return collection

def education(url):
    edu = {}
    home = "https://hbg.gduf.edu.cn"
    soup = get_soup1(url)
    div = soup.find('div',attrs={'class':'cen'})
    edu["name"] = div.text
    #print(div.text)
    span = soup.find_all('span')
    main = ""
    for tag in span:
        main = main+tag.text
    edu["description"] = main
    #print(main)
    img = soup.find_all('img',attrs={'alt':''})
    i = 0
    for tag in img:
        i = i+1
        src = home+tag["src"]
        edu["img"] = src
        #print("活动写照:"+src)
        #if i == 3:
        break
    edu["mname"] = "广州货币金融博物馆"
    return edu

url = "https://baike.sogou.com/v10498064.htm?fromTitle=%E5%B9%BF%E5%B7%9E%E8%B4%A7%E5%B8%81%E9%87%91%E8%9E%8D%E5%8D%9A%E7%89%A9%E9%A6%86"
x = get_brief(url)
a = []
a.append(x)

exhibitions = []
print("------展馆陈列------")
url = "https://hbg.gduf.edu.cn/zpzs/zggdhbzt1/ghq.htm"
x = show(url)
exhibitions.append(x)
print("\n")

collections = []
print("-----馆藏珍品------")
url = "https://hbg.gduf.edu.cn/info/1046/1233.htm"
y = object(url)
collections.append(y)
print("\n")
url = "https://hbg.gduf.edu.cn/info/1006/1113.htm"
y = object(url)
collections.append(y)
print("\n")
url = "https://hbg.gduf.edu.cn/info/1007/1153.htm"
y = object(url)
collections.append(y)
print("\n")
url = "https://hbg.gduf.edu.cn/info/1006/1112.htm"
y = object(url)
collections.append(y)
print("\n")
url = "https://hbg.gduf.edu.cn/info/1012/1223.htm"
y = object(url)
collections.append(y)
print("\n")

educational = []
print("------教育活动------")
url = "https://hbg.gduf.edu.cn/info/1003/1385.htm"
z = education(url)
z["time"] = "发布时间: 2019/11/28"
educational.append(z)
print("\n")
url = "https://hbg.gduf.edu.cn/info/1003/1383.htm"
z = education(url)
z["time"] = "发布时间: 2019/11/21"
educational.append(z)
print("\n")

edu = {}
url = "https://hbg.gduf.edu.cn/info/1003/1026.htm"
home = "https://hbg.gduf.edu.cn"
soup = get_soup1(url)
div = soup.find('div',attrs={'class':'cen'})
#print(div.text)
edu["name"] = div.text
p = soup.find_all('p')
main = ""
for tag in p:
    main = main+tag.text
#print(main)
edu["description"] = main
img = soup.find_all('img',attrs={'alt':''})
i = 0
for tag in img:
    i = i+1
    src = home+tag["src"]
    edu["img"] = src
    #print("活动写照:"+src)
    #if i == 3:
    break
edu["mname"] = "广州货币金融博物馆"
edu["time"] = "发布时间: 2018/05/23"
print("\n")

educational.append(edu)

museum_info["1"] = a
museum_info["2"] = []#exhibitions
museum_info["3"] = []#collections
museum_info["4"] = []#educational

save_data(museum_info)