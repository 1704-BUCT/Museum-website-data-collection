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
    src = img["src"]
    print("------参观信息------")
    visit = soup.find('table',class_ ='abstract_tbl')
    info = visit.find_all('tr')
    for tag in info:
        title = tag.find('th',class_ = 'base-info-card-title')
        #print(title.text+":",end="")
        texts = tag.find('div',class_ = 'base-info-card-value').find(text=True).strip()
        #print(texts)
    brief["name"] = "河南博物院"
    brief["img"] = src
    brief["location"] = "中国•河南省郑州市农业路8号"
    brief["number"] = "预约电话：0371-63511237、63511239"
    brief["opentime"] = "每周二至周日9：00—17：30（冬季开放时间为9：00—17：00）闭馆前1小时停止发放门票" 
    return brief

def show(url):
    exhibition = {}
    home = "http://www.chnmus.net"
    soup = get_soup(url)
    div = soup.find('div',attrs={'class':'fenye_con'})
    title = div.find('div',attrs={'class':'cms-article-tit'})
    exhibition["name"] = title.text
    #print(title.text)
    main = ""
    p = div.find_all('p')
    for tag in p:
        main = main+tag.text
    #print(main)
    exhibition["description"] = main
    img = div.find_all("img")
    for tag in img:
         src = home+tag["src"]
         exhibition["img"] = src
         #print("展览图示:"+src)
         break
    exhibition["mname"] = "河南博物院"
    return exhibition

def object(url):
    collection = {}
    home = "http://www.chnmus.net"
    soup = get_soup(url)
    div = soup.find('div',attrs={'class':'article-detail'})
    p = div.find_all('p')
    main = ""
    for tag in p:
        main = main+tag.text
    #print(main)
    collection["description"] = main
    img = div.find('img')
    src = home+img["src"]
    collection["img"] = src
    collection["mname"] = "河南博物院"
    return collection
    #print("典藏图片:"+src)

def education(url):
    edu = {}
    home = "http://www.chnmus.net"
    soup = get_soup(url)
    title = soup.find('div',attrs={'class':'cms-article-tit'})
    edu["name"] = (title.text).strip()
    #print(title.text)
    div = soup.find('div',attrs={'class':'article-detail'})
    p = div.find_all('p')
    main = ""
    for tag in p:
        main = main+tag.text
    #print(main)
    edu["description"] = main
    img = div.find('img')
    src = home+img["src"]
    edu["img"] = src
    edu["mname"] = "河南博物院"
    return edu
    #print("活动写照:"+src)

url = "https://baike.sogou.com/v154572.htm?fromTitle=%E6%B2%B3%E5%8D%97%E5%8D%9A%E7%89%A9%E9%99%A2"
x = get_brief(url)
a = []
a.append(x)


url = "http://www.chnmus.net/sitesources/hnsbwy/page_pc/index.html"
soup = get_soup(url)
serve = soup.find('div',attrs={'class':'serve'})
p = serve.find_all('p')
main = ""
for tag in p:
    main = main+tag.text
print(main)

exhibitions = []
print("-----展览陈列------")
url = "http://www.chnmus.net/sitesources/hnsbwy/page_pc/clzl/jbcl/article002d7515354c450e856bd18beaffb31b.html"
x = show(url)
exhibitions.append(x)
print("\n")
url = "http://www.chnmus.net/sitesources/hnsbwy/page_pc/clzl/jbcl/article3cddca58e4b7478cb9015e4722aad850.html"
x = show(url)
exhibitions.append(x)
print("\n")
url = "http://www.chnmus.net/sitesources/hnsbwy/page_pc/clzl/jbcl/articlee6d24ddc29894645bc1a9167423ce63a.html"
x = show(url)
exhibitions.append(x)
print("\n")

collections = []
print("------典藏珍品------")
url = "http://www.chnmus.net/sitesources/hnsbwy/page_pc/dzjp/zyzb/article492822bf0c494d6a80aa86ba5f7d74e6.html"
y = object(url)
y["name"] = "云纹铜禁"
collections.append(y)
print("\n")
url = "http://www.chnmus.net/sitesources/hnsbwy/page_pc/dzjp/zyzb/articlee741d1d8b69c414a8fa991cda1087847.html"
y = object(url)
y["name"] = "贾湖骨笛"
collections.append(y)
print("\n")
url = "http://www.chnmus.net/sitesources/hnsbwy/page_pc/dzjp/zyzb/article98cd402c5069437393e9b94265147fe1.html"
y = object(url)
y["name"] = "玉柄铁剑"
collections.append(y)
print("\n")
url = "http://www.chnmus.net/sitesources/hnsbwy/page_pc/dzjp/zyzb/article39894039da684cc69a3528a41f93acfc.html"
y = object(url)
y["name"] = "莲鹤方壶"
collections.append(y)
print("\n")
url = "http://www.chnmus.net/sitesources/hnsbwy/page_pc/dzjp/zyzb/articlef765a934c73342d1a1648e9eaddb678d.html"
y = object(url)
y["name"] = "武则天金简"
collections.append(y)
print("\n")

educational = []
print("------教育活动------")
url = "http://www.chnmus.net/sitesources/hnsbwy/page_pc/ppjy/zylswhxjt/xjtdt/article76f8fc6727d74d32bc8655114fea3822.html"
z = education(url)
z["time"] = "发布日期：2019-04-22"
educational.append(z)
print("\n")
url = "http://www.chnmus.net/sitesources/hnsbwy/page_pc/ppjy/sjhd/article758c1ff1792f4cc68808267daad9f5e9.html"
z = education(url)
z["time"] = "发布日期：2017-11-09"
educational.append(z)
print("\n")
url = "http://www.chnmus.net/sitesources/hnsbwy/page_pc/ppjy/sqsehdj/articleba2d393d05814f4388396ba3ba8f8c24.html"
z = education(url)
z["time"] = "发布日期：2019-07-22"
educational.append(z)
print("\n")

museum_info["1"] = a
museum_info["2"] = []#exhibitions
museum_info["3"] = []#collections
museum_info["4"] = []#educational

save_data(museum_info)