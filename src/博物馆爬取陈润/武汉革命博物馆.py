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
    src = "http://www.whgmbwg.com/uploadfiles/201908/02/2019080214145533186691-thumbnail.jpg"
    print("------参观信息------")
    visit = soup.find('table',class_ ='abstract_tbl')
    info = visit.find_all('tr')
    #for tag in info:
        #title = tag.find('th',class_ = 'base-info-card-title')
        #print(title.text+":",end="")
        #texts = tag.find('div',class_ = 'base-info-card-value').find(text=True).strip()
        #print(texts)
    brief["name"] = "武汉革命博物馆"
    brief["img"] = src
    brief["location"] = "馆址：湖北省武汉市武昌区红巷13号 "
    brief["number"] = "027-88850322"
    brief["opentime"] = "" 
    return brief
def show(url,temp):
    exhibition = {}
    home = "http://www.whgmbwg.com"
    soup = get_soup1(url)
    div = soup.find('div',attrs={'class':'gmg_nright'})
    span = div.find_all('span',attrs={'style':'font-size: 16px;'})
    main = ""
    for tag in span:
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
    exhibition["name"] = temp
    exhibition["mname"] = "武汉革命博物馆"
    return exhibition

def object(url,temp):
    collection = {}
    home = "http://www.whgmbwg.com"
    soup = get_soup1(url)
    div = soup.find('div',attrs={'class':'gmg_nright'})
    p = div.find('p')
    #print(p.text)
    collection["description"] = p.text
    img = div.find_all('img')
    i = 0
    for tag in img:
        i = i+1
        src =home+tag["src"]
        collection["img"] = src
        #print("典藏图片:"+src)
        #if i == 3:
        break
    collection["name"] = temp
    collection["mname"] = "武汉革命博物馆"
    return collection

def education(url,temp,time):
    edu = {}
    home = "http://www.whgmbwg.com"
    soup = get_soup1(url)
    div = soup.find('div',attrs={'class':'gmg_nright'})
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
        src =home+tag["src"]
        edu["img"] = src
        #print("活动写照:"+src)
        #if i == 3:
        break
    edu["name"] = temp
    edu["time"] = time
    edu["mname"] = "武汉革命博物馆"
    return edu

url = "https://baike.sogou.com/v58117464.htm?fromTitle=%E6%AD%A6%E6%B1%89%E9%9D%A9%E5%91%BD%E5%8D%9A%E7%89%A9%E9%A6%86"
x = get_brief(url)
a = []
a.append(x)

exhibitions = []
print("------展览陈列------")
url = "http://www.whgmbwg.com/doc/2019/10/01/35244.shtml"
temp = "光辉永存——武昌毛泽东旧居人物展"
x = show(url,temp)
exhibitions.append(x)
print("\n")
url = "http://www.whgmbwg.com/doc/2019/09/11/34752.shtml"
temp = "纪律建设永远在路上——中国共产党纪律建设历史陈列"
x = show(url,temp)
exhibitions.append(x)
print("\n")
url = "http://www.whgmbwg.com/doc/2019/09/06/34669.shtml"
temp = "武汉走出的革命家、军事家、外交家——伍修权生平展"
x = show(url,temp)
exhibitions.append(x)
print("\n")

collections = []
print("-----典藏珍品------")
url = "http://www.whgmbwg.com/doc/2019/03/12/31923.shtml"
temp = "中国国民党中央农民运动讲习所规约"
y = object(url,temp)
collections.append(y)
print("\n")
url = "http://www.whgmbwg.com/doc/2019/03/12/31914.shtml"
temp = "周恩来1958年为武昌农讲所旧址题字"
y = object(url,temp)
collections.append(y)
print("\n")
url = "http://www.whgmbwg.com/doc/2019/03/12/31912.shtml"
temp = "毛泽东1926年著《中国佃农生活举例》"
y = object(url,temp)
collections.append(y)
print("\n")
url = "http://www.whgmbwg.com/doc/2019/03/12/31917.shtml"
temp = "董必武1923年致皮象休的信"
y = object(url,temp)
collections.append(y)
print("\n")
url = "http://www.whgmbwg.com/doc/2019/03/12/31908.shtml"
temp = "1938年美术家冯文志在武汉创作的抗日布旗"
y = object(url,temp)
collections.append(y)
print("\n")

educational = []
print("------教育活动------")
url = "http://www.whgmbwg.com/doc/2019/01/15/30231.shtml"
temp = "农工党中央“不忘合作初心，继续携手前进”专题教育活动在武汉正式启动"
time = "发布时间：2017-04-20"
z = education(url,temp,time)
educational.append(z)
print("\n")
url = "http://www.whgmbwg.com/doc/2019/01/15/30230.shtml"
temp = "武汉基督教青年会秘书处到我馆开展留守儿童爱国主义教育实践活动"
time = "发布时间：2017-09-28"
z = education(url,temp,time)
educational.append(z)
print("\n")
url = "http://www.whgmbwg.com/doc/2019/10/11/35400.shtml"
temp = "北省首部博物馆环境剧—情境党课《历史的回望》即将上演！"
time = "发布时间：2019-06-27 "
z = education(url,temp,time)
educational.append(z)
print("\n")

museum_info["1"] = a
museum_info["2"] = exhibitions
museum_info["3"] = collections
museum_info["4"] = educational

save_data(museum_info)