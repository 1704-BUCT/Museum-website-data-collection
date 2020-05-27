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
    brief["name"] = "广西壮族自治区博物馆"
    brief["img"] = src
    brief["location"] = "地址：广西南宁市民族大道34号"
    brief["number"] = "咨询电话0771-2707027  预约电话：0771-2707027 "
    brief["opentime"] = "开放时间：每周二至周日9：00-17：00(16:00停止发票，16：50清场)。每周一全天闭馆（国家法定假日除外）整修" 
    return brief

def show(url):
    exhibition = {}
    home = "http://www.gxmuseum.cn"
    soup = get_soup1(url)
    title = soup.find('div',attrs={'class':'title'})
    exhibition["name"] = (title.text).strip()
    #print(title.text)
    div = soup.find('div',attrs={'class':'content'})
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
        src = home+tag["src"]
        exhibition["img"] = src
        #print("展览图示:"+src)
        if i == 4:
            break
    exhibition["mname"] = "广西壮族自治区博物馆"
    return exhibition

def object(url):
    collection = {}
    home = "http://www.gxmuseum.cn"
    soup = get_soup1(url)
    title = soup.find('div',attrs={'class':'title'})
    #print(title.text)
    collection["name"] = (title.text).strip()
    content = soup.find('div',attrs={'class':'content'})
    span = content.find_all('span')
    main = ""
    for tag in span:
        main = main+tag.text
    #collection["description"] = main
    #print(main)
    p = content.find('p')
    #print(p.text)
    collection["description"] = main+p.text
    img = content.find('img')
    src = home+img["src"]
    collection["img"] = src
    collection["mname"] = "广西壮族自治区博物馆"
    #print("藏品图示:"+src)
    return collection

def education(url):
    edu = {}
    home = "http://www.gxmuseum.cn"
    soup = get_soup1(url)
    title = soup.find('div',attrs={'class':'title'})
    edu["name"] = (title.text).strip()
    #print(title.text)
    content = soup.find('div',attrs={'class':'content'})
    p = content.find_all('p')
    main = ""
    for tag in p:
        main = main+tag.text
    edu["description"] = main
    #print(main)
    img = soup.find_all('img',attrs={'width':'600'})
    i = 0
    for tag in img:
        i = i+1
        src = home+tag["src"]
        edu["img"] = src
        #print("活动写照:"+src)
        if i == 3:
            break
    edu["mname"] = "广西壮族自治区博物馆"
    return edu

url = "https://baike.sogou.com/v163930.htm?fromTitle=%E5%B9%BF%E8%A5%BF%E5%A3%AE%E6%97%8F%E8%87%AA%E6%B2%BB%E5%8C%BA%E5%8D%9A%E7%89%A9%E9%A6%86"
x = get_brief(url)
a = []
a.append(x)


exhibition_hall = []
print("------展览陈列------")
url = "http://www.gxmuseum.cn/a/exhibition/11/2010/82.html"
x = show(url)
exhibition_hall.append(x)
print("\n")
url = "http://www.gxmuseum.cn/a/exhibition/11/2016/7045.html"
x = show(url)
exhibition_hall.append(x)
print("\n")
url = "http://www.gxmuseum.cn/a/exhibition/11/2018/7959.html"
x = show(url)
exhibition_hall.append(x)
print("\n")

collections = []
print("------典藏珍品------")
url = "http://www.gxmuseum.cn/a/antique/16/2019/8339.html"
y = object(url)
collections.append(y)
print("\n")
url = "http://www.gxmuseum.cn/a/antique/16/2019/8338.html"
y = object(url)
collections.append(y)
print("\n")
url = "http://www.gxmuseum.cn/a/antique/17/2020/8411.html"
y = object(url)
collections.append(y)
print("\n")
url = "http://www.gxmuseum.cn/a/antique/18/2019/8346.html"
y = object(url)
collections.append(y)
print("\n")
url = "http://www.gxmuseum.cn/a/antique/19/2017/7588.html"
y = object(url)
collections.append(y)
print("\n")

educations = []
print("------教育活动------")
url = "http://www.gxmuseum.cn/a/education/55/2016/7077.html"
z = education(url)
z["time"] = "时间:2016-07-30"
educations.append(z)
print("\n")
url = "http://www.gxmuseum.cn/a/education/55/2016/7093.html"
z = education(url)
z["time"] = "时间:2016-08-21"
educations.append(z)
print("\n")
url = "http://www.gxmuseum.cn/a/education/55/2016/7109.html"
z = education(url)
z["time"] = "时间:2016-09-01"
educations.append(z)
print("\n")

museum_info["1"] = a
museum_info["2"] = []#exhibition_hall
museum_info["3"] = []#collections
museum_info["4"] = []#educations

#print(museum_info)
save_data(museum_info)