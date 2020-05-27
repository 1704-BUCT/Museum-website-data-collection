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

def get_soup1(url):
    text = get_text(url)
    soup = BeautifulSoup(text,"html.parser")
    return soup

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
    brief["name"] = "中国地质大学逸夫博物馆"
    brief["img"] = src
    brief["location"] = "地址：武汉洪山鲁磨路（光谷广场以北）"
    brief["number"] = "游客服务咨询电话：（027）67848584   （027）67883347－8666"
    brief["opentime"] = "冬季（10月－4月）上午8：00－12：00 下午14：00－17：00   夏季（5月－9月） 上午8：00－12：00 下午14：30－17：30  双休节假日 9：00－17：00" 
    return brief
    
def visit(url):
    soup = get_soup(url)
    div = soup.find('div',attrs={'class':'jj fl'})
    print(div.text)

def show(url):
    exhibition ={}
    home = "http://mus.cug.edu.cn"
    soup = get_soup(url)
    div =soup.find('div',attrs={'class':'content fl'})
    h3 = div.find('h3')
    #print(h3.text)
    exhibition["name"] = h3.text
    span = div.find_all('span')
    main = ""
    for tag in span:
        main = main+(tag.text).strip()
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
    exhibition["mname"] = "中国地质大学逸夫博物馆"
    return exhibition

def object(url):
    collection = {}
    home = "http://mus.cug.edu.cn"
    soup = get_soup(url)
    div =soup.find('div',attrs={'class':'content fl'})
    h3 = div.find('h3')
    #print(h3.text)
    collection["name"] = h3.text
    span = div.find_all('span')
    main = ""
    for tag in span:
        main = main+tag.text
    #print(main)
    collection["description"] = main
    img = div.find_all('img')
    i = 0
    for tag in img:
        i = i+1
        src =home+tag["src"]
        collection["img"] = src
        #print("典藏图片:"+src)
        #if i == 3:
        break
    collection["mname"] = "中国地质大学逸夫博物馆"
    return collection

url = "https://baike.sogou.com/v5914302.htm?fromTitle=%E4%B8%AD%E5%9B%BD%E5%9C%B0%E8%B4%A8%E5%A4%A7%E5%AD%A6%E9%80%B8%E5%A4%AB%E5%8D%9A%E7%89%A9%E9%A6%86"
x = get_brief(url)
a = []
a.append(x)

url = "http://mus.cug.edu.cn/cgzn1/pwfw.htm"
visit(url)

exhibitions = []
print("------展览陈列------")
url = "http://mus.cug.edu.cn/info/1051/1131.htm"
x = show(url)
exhibitions.append(x)
print("\n")
url = "http://mus.cug.edu.cn/info/1051/1132.htm"
x = show(url)
exhibitions.append(x)
print("\n")
url = "http://mus.cug.edu.cn/info/1051/1133.htm"
x = show(url)
exhibitions.append(x)
print("\n")

#print(exhibitions)

collections = []
print("------典藏珍品------")
url = "http://mus.cug.edu.cn/info/1015/2566.htm"
y = object(url)
collections.append(y)
print("\n")
url = "http://mus.cug.edu.cn/info/1015/2565.htm"
y = object(url)
collections.append(y)
print("\n")
url = "http://mus.cug.edu.cn/info/1015/2563.htm"
y = object(url)
collections.append(y)
print("\n")
url = "http://mus.cug.edu.cn/info/1015/2527.htm"
y = object(url)
collections.append(y)
print("\n")
url = "http://mus.cug.edu.cn/info/1015/2524.htm"
y = object(url)
collections.append(y)
print("\n")

museum_info["1"] = []#a
museum_info["2"] = exhibitions
museum_info["3"] = []#collections
museum_info["4"] = []#educational

save_data(museum_info)

