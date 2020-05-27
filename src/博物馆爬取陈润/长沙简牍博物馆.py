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
    src = "http://112.74.61.33:9999/A02Test/CSJDBWG/%E5%AF%8C%E6%96%87%E6%9C%AC%E7%BC%96%E8%BE%91%E5%99%A8%E6%96%87%E4%BB%B6/EditorImage/20180612/6366442103686269362156521.png"
    print("------参观信息------")
    visit = soup.find('table',class_ ='abstract_tbl')
    info = visit.find_all('tr')
    #for tag in info:
        #title = tag.find('th',class_ = 'base-info-card-title')
        #print(title.text+":",end="")
        #texts = tag.find('div',class_ = 'base-info-card-value').find(text=True).strip()
        #print(texts)
    brief["name"] = "长沙简牍博物馆"
    brief["img"] = src
    brief["location"] = "地址：长沙市天心区白沙路92号"
    brief["number"] = "预约电话：0731-85425680 85425676"
    brief["opentime"] = "星期三——次周星期一上午9:00至下午5:00（下午4:30停止领票进馆）开馆，每周二、除夕、正月初一、初二闭馆。" 
    return brief


def show(url):
    exhibition = {}
    home = "http://www.jhgmuseum.com"
    soup = get_soup1(url)
    div = soup.find('div',attrs={'class':'innercont'})
    title = div.find('div',attrs={'class':'title'})
    #print(title.text)
    exhibition["name"] = (title.text).strip()
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
        exhibition["img"] = src
        #print("展览图示:"+src)
        #if i == 4:
        break
    exhibition["mname"] = "长沙简牍博物馆"
    return exhibition

def object(url):
    collection = {}
    home = "http://www.jhgmuseum.com"
    soup = get_soup1(url)
    div = soup.find('div',attrs={'class':'innercont'})
    title = div.find('div',attrs={'class':'title'})
    #print(title.text)
    collection["name"] = (title.text).strip()
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
        #print("典藏图示:"+src)
        #if i == 4:
        break
    collection["mname"] = "长沙简牍博物馆"
    return collection

def education(url,temp):
    edu = {}
    soup = get_soup1(url)
    div = soup.find('div',attrs={'class':'innercont'})
    title = div.find('div',attrs={'class':'title'})
    #print(title.text)
    edu["name"] = (title.text).strip()
    p = div.find_all('p')
    main = ""
    for tag in p:
        main = main+tag.text
    #print(main)
    edu["description"] = main
    img = div.find_all('img')
    i = 0
    for tag in img:
        i = i+1
        src = tag["src"]
        edu["img"] = src
        #print("活动写照:"+src)
        #if i == 3:
        break
    edu["mname"] = "长沙简牍博物馆"
    edu["time"] = temp
    return edu

url = "https://baike.sogou.com/v7631903.htm?fromTitle=%E9%95%BF%E6%B2%99%E7%AE%80%E7%89%8D%E5%8D%9A%E7%89%A9%E9%A6%86"
x = get_brief(url)
a = []
a.append(x)

exhibitions = []
print("------展览陈列------")
url = "http://www.chinajiandu.cn/News/Details/wwtz?nid=219"
x = show(url)
exhibitions.append(x)
print("\n")
url = "http://www.chinajiandu.cn/News/Details/wwtz?nid=202"
x = show(url)
exhibitions.append(x)
print("\n")
url = "http://www.chinajiandu.cn/News/Details/wwtz?nid=200"
x = show(url)
exhibitions.append(x)
print("\n")

collections = []
print("------典藏珍品------")
url = "http://www.chinajiandu.cn/Collection/Details/wj?nid=246"
y = object(url)
collections.append(y)
print("\n")
url = "http://www.chinajiandu.cn/Collection/Details/wj?nid=243"
y = object(url)
collections.append(y)
print("\n")
url = "http://www.chinajiandu.cn/Collection/Details/xhj?nid=291"
y = object(url)
collections.append(y)
print("\n")
url = "http://www.chinajiandu.cn/Collection/Details/yym?nid=255"
y = object(url)
collections.append(y)
print("\n")
url = "http://www.chinajiandu.cn/Collection/Details/yym?nid=253"
y = object(url)
collections.append(y)
print("\n")

educational = []
print("------教育活动------")
url = "http://www.chinajiandu.cn/News/Details/whjt?nid=740"
temp = "时间：2019-10-14"
z = education(url,temp)
educational.append(z)
print("\n")
url = "http://www.chinajiandu.cn/News/Details/jbjlb?nid=742"
temp = "时间：2019-10-15"
z = education(url,temp)
educational.append(z)
print("\n")
url = "http://www.chinajiandu.cn/News/Details/zyzzj?nid=771"
temp = "时间：2019-10-31"
z = education(url,temp)
educational.append(z)
print("\n")

museum_info["1"] = a
museum_info["2"] = exhibitions
museum_info["3"] = collections
museum_info["4"] = []#educational

save_data(museum_info)



