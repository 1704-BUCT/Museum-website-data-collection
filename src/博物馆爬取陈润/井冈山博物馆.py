import requests
import re
import bs4
from bs4 import BeautifulSoup
import bs4
import pymysql

headers = {
     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'    
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
    brief["name"] = "井冈山博物馆"
    brief["img"] = src
    brief["location"] = " 地址：江西省井冈山茨坪红军南路"
    brief["number"] = "电话:0796-6552248/6555625"
    brief["opentime"] = "" 
    return brief

def get_education(url,temp): #教育活动
    soup = get_soup1(url)
    edu = {}
    education = soup.find('div',attrs={'class':'subBody'})
    title = education.find('div',attrs={'class':'listConts'})
    p = title.find_all('p',class_ ='MsoNormal')
    main = ""
    for tag in p:
        main = main+tag.text.strip()
    edu["description"] = main
    edu["name"] = temp
    edu["mname"] = "井冈山博物馆"
    edu["img"] = ""
    return edu

#展馆陈列
def show(url,temp):
    exhibition = {}
    home = "http://www.jgsgmbwg.com"
    soup = get_soup1(url)
    table = soup.find('div',attrs={'class':'listConts'})
    main = table.find('span',attrs={'class':'style1'})
    print("展览介绍:")
    #print(main.text) #展览介绍
    exhibition["description"] = main.text
    img = table.find('img')
    src = home + img["src"] #图片链接
    #print("展览图示:"+src)
    exhibition["img"] = src
    exhibition["name"] = temp
    exhibition["mname"] = "井冈山博物馆"
    return exhibition
    
def objects(url,temp):
    home = "http://www.jgsgmbwg.com"
    collection = {}
    soup = get_soup1(url)
    main = ""
    p = soup.find_all('p')
    for tag in p:
        main = main+tag.text
    collection["description"] = main
    img = soup.find('img',attrs={'alt':''})
    src = home+img["src"]
    collection["name"] = temp
    collection["img"] = src
    collection["mname"] = "井冈山博物馆"
    return collection

url = "https://baike.sogou.com/v6815002.htm?fromTitle=%E4%BA%95%E5%86%88%E5%B1%B1%E9%9D%A9%E5%91%BD%E5%8D%9A%E7%89%A9%E9%A6%86"
x = get_brief(url)
a = []
a.append(x)

#展览陈列
exhibitions = []
print("------展览陈列------")
url = "http://www.jgsgmbwg.com/productshow.php?cid=6&id=28"
temp = "红四五军会师"
b = show(url,temp)
exhibitions.append(b)
url = "http://www.jgsgmbwg.com/productshow.php?cid=6&id=27"
temp = "身先士卒"
b = show(url,temp)
exhibitions.append(b)
url = "http://www.jgsgmbwg.com/productshow.php?cid=6&id=26"
temp = "消灭尹道一"
b = show(url,temp)
exhibitions.append(b)
url = "http://www.jgsgmbwg.com/productshow.php?cid=6&id=25"
temp = "挑粮"
b = show(url,temp)
exhibitions.append(b)
url = "http://www.jgsgmbwg.com/productshow.php?cid=6&id=23"
temp = "碧血丹心"
b = show(url,temp)
exhibitions.append(b)
print("\n")

collections = []
url = "http://www.jgsgmbwg.com/newsshow.php?cid=71&id=6244"
temp = "清铜质挂式针灸盒"
y = objects(url,temp)
collections.append(y)
url = "http://www.jgsgmbwg.com/newsshow.php?cid=71&id=6245"
temp = "1932年8月班长陈贵山使用的《支部工作纲要》"
y = objects(url,temp)
collections.append(y)
url = "http://www.jgsgmbwg.com/newsshow.php?cid=71&id=6296"
temp = "井冈山群众接待习总书记装板栗装鸡蛋的竹匾"
y = objects(url,temp)
collections.append(y)
url = "http://www.jgsgmbwg.com/newsshow.php?cid=71&id=6297"
temp = "习总书记在井冈山打糍粑用过的木槌"
y = objects(url,temp)
collections.append(y)
url = "http://www.jgsgmbwg.com/newsshow.php?cid=71&id=6299"
temp = "中央军委总政治部编印的《什么是托洛斯基主义和托洛斯基派》"
y = objects(url,temp)
collections.append(y)

educational = []
#教育活动
print("-----教育活动------")
url = "http://www.jgsgmbwg.com/newsshow.php?cid=72&id=5600"
temp = "-----井冈山革命博物馆旧居旧址办党支部召开党的群众路线教育实践活动总结会-----\n"
z = get_education(url,temp)
z["time"] = "更新时间：2014-11-13"
educational.append(z)
print("\n")

url = "http://www.jgsgmbwg.com/newsshow.php?cid=72&id=5586"
temp = "-----井冈山革命博物馆召开党的群众路线教育实践活动总结大会-----\n"
z = get_education(url,temp)
z["time"] = "更新时间：2014-10-29"
educational.append(z)
print("\n")

url = "http://www.jgsgmbwg.com/newsshow.php?cid=72&id=5573"
temp = "学习伟人风范 践行群众路线\n"
z = get_education(url,temp)
z["time"] = "更新时间：2014-10-23"
educational.append(z)
print("\n")

museum_info["1"] = a
museum_info["2"] = exhibitions
museum_info["3"] = collections
museum_info["4"] = educational

save_data(museum_info)