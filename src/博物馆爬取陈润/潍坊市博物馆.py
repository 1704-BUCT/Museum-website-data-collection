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
    #img = div.find('img',attrs={'width':'250'})
    src = "http://www.rjjng.com.cn/cms/resource/img/h000/h01/img201410141655490.jpg"
    print("------参观信息------")
    visit = soup.find('table',class_ ='abstract_tbl')
    info = visit.find_all('tr')
    #for tag in info:
        #title = tag.find('th',class_ = 'base-info-card-title')
        #print(title.text+":",end="")
        #texts = tag.find('div',class_ = 'base-info-card-value').find(text=True).strip()
        #print(texts)
    brief["name"] = "潍坊市博物馆"
    brief["img"] = src
    brief["location"] = "馆　址:潍坊市东风东街6616号"
    brief["number"] = "电　话：0536-8865529"
    brief["opentime"] = "周二至周日全天开放；周一闭馆（国家法定节假日除外）" 
    return brief

def show(url,temp):
    exhibition = {}
    home = "http://www.wfsbwg.com"
    soup = get_soup(url)
    div = soup.find('div',attrs={'class':'sb_box br-bg'})
    p = div.find_all('p')
    main = ""
    for tag in p:
        main = main+tag.text
    #print(main)
    exhibition["description"] = main
    img = div.find_all("img")
    i = 0
    for tag in img:
        i = i+1
        src = home+tag["src"]
        exhibition["img"] = src
        #print("展览图示:"+src)
        #if i == 6:
        break
    exhibition["mname"] = "潍坊市博物馆"
    exhibition["name"] = temp
    return exhibition

def object(url,temp):
    collection = {}
    home = "http://www.wfsbwg.com"
    soup = get_soup(url)
    div = soup.find('div',attrs={'class':'sb_box br-bg'})
    img = div.find("img")
    src = home+img["src"]
    #print("典藏图片:"+src)
    collection["img"] = src
    collection["name"] = temp
    collection["description"] =""
    collection["mname"] = "潍坊市博物馆"
    return collection

def education(url,temp,time):
    edu = {}
    home = "http://www.wfsbwg.com"
    soup = get_soup(url)
    div = soup.find('div',attrs={'class':'sb_box br-bg'})
    p = div.find_all('p')
    main = ""
    for tag in p:
        main = main+tag.text
    #print(main)
    edu["description"] = main
    img = div.find_all("img")
    i = 0
    for tag in img:
        i = i+1
        src = home+tag["src"]
        edu["img"] = src
        #print("活动写照:"+src)
        #if i == 3:
        break
    edu["mname"] = "潍坊市博物馆"
    edu["name"] = temp
    edu["time"] = time
    return edu


url = "https://baike.sogou.com/v163430.htm?fromTitle=%E6%BD%8D%E5%9D%8A%E5%B8%82%E5%8D%9A%E7%89%A9%E9%A6%86"
x = get_brief(url)
a = []
a.append(x)

exhibitions = []
print("------展览陈列------")
url = "http://www.wfsbwg.com/content/?1098.html"
temp = "馆藏“同志画社”名家作品展"
x = show(url,temp)
exhibitions.append(x)
print("\n")
url = "http://www.wfsbwg.com/content/?1038.html"
temp = "物华天宝 • 馆藏文物精粹展"
x = show(url,temp)
exhibitions.append(x)
print("\n")
url = "http://www.wfsbwg.com/content/?182.html"
temp = "潍坊简史陈列"
x = show(url,temp)
exhibitions.append(x)
print("\n")

collections = []
print("------典藏图片------")
url = "http://www.wfsbwg.com/content/?425.html"
temp = "大汶口文化红陶盉"
y = object(url,temp)
collections.append(y)
print("\n")
url = "http://www.wfsbwg.com/content/?374.html"
temp = "西周青铜鼎"
y = object(url,temp)
collections.append(y)
print("\n")
url = "http://www.wfsbwg.com/content/?344.html"
temp = "清张士保人物图轴"
y = object(url,temp)
collections.append(y)
print("\n")
url = "http://www.wfsbwg.com/content/?474.html"
temp = "清至民国朱拓唐开元十四年纪泰山铭拓片"
y = object(url,temp)
collections.append(y)
print("\n")
url = "http://www.wfsbwg.com/content/?377.html"
temp = "汉陶人物俑"
y = object(url,temp)
collections.append(y)
print("\n")

educational = []
print("------教育活动------")
url = "http://www.wfsbwg.com/content/?909.html"
temp = "潍坊市博物馆“小书斋•大讲堂”进校园——文物趣味涂鸦课"
time = "2019年3月12日"
z = education(url,temp,time)
educational.append(z)
print("\n")
url = "http://www.wfsbwg.com/content/?1023.html"
temp = "《潍坊人文历史文化》公益讲座走进歌尔集团"
time = "2019年9月7日"
z = education(url,temp,time)
educational.append(z)
print("\n")
url = "http://www.wfsbwg.com/content/?650.html"
temp = "第八期“致青春·敬名师”——金石学专题学习"
time = "2019年9月20日"
z = education(url,temp,time)
educational.append(z)
print("\n")

museum_info["1"] = a
museum_info["2"] = exhibitions
museum_info["3"] = collections
museum_info["4"] = educational

save_data(museum_info)