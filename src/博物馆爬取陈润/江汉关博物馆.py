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
    #img = div.find('img',attrs={'width':'250'})
    #src = img["src"]
    print("------参观信息------")
    visit = soup.find('table',class_ ='abstract_tbl')
    info = visit.find_all('tr')
    for tag in info:
        title = tag.find('th',class_ = 'base-info-card-title')
        #print(title.text+":",end="")
        texts = tag.find('div',class_ = 'base-info-card-value').find(text=True).strip()
        #print(texts)
    brief["name"] = "江汉关博物馆"
    brief["img"] = "http://www.jhgmuseum.com/upload/20180903103310kSns.jpg"
    brief["location"] = "江汉关博物馆，位于武汉市汉口沿江大道129号   武汉国民政府旧址纪念馆（汉口南洋大楼），位于汉口中山大道708号  詹天佑故居博物馆，位于汉口洞庭街65号"
    brief["number"] = " 预约电话：027-82880866"
    brief["opentime"] = "开放时间：周二至周日9:00-17:00(16:30停止入馆)，周一闭馆整休。" 
    return brief

def visit(url):
    soup = get_soup1(url)
    div = soup.find('div',attrs={'class':'screen noteArea'})
    print("------博物馆简介------")
    p = div.find_all('p')
    brief = ""
    for tag in p:
        brief = brief+tag.text
    print(brief)
    print("------参观信息------")
    div = soup.find('div',attrs={'class':'museumInfo'})
    print(div.text)
    visit = "江汉关博物馆，位于武汉市汉口沿江大道129号 武汉国民政府旧址纪念馆（汉口南洋大楼），位于汉口中山大道708号  詹天佑故居博物馆，位于汉口洞庭街65号"
    print(visit)

def show(url):
    exhibition = {}
    home = "http://www.jhgmuseum.com"
    soup = get_soup1(url)
    div = soup.find('div',attrs={'class':'article'})
    p = div.find_all('p')
    main = ""
    for tag in p:
        main = main+tag.text
    exhibition["description"] = main
    #print(main)
    img = div.find_all('img')
    i = 0
    for tag in img:
        i = i+1
        src = home+tag["src"]
        exhibition["img"] = src
        #print("展览图示:"+src)
        #if i == 4:
        break
    exhibition["mname"] = "江汉关博物馆"
    return exhibition

def education(url):
    edu = {}
    home = "http://www.jhgmuseum.com"
    soup = get_soup1(url)
    div = soup.find('div',attrs={'class':'article'})
    p = div.find_all('p')
    main = ""
    for tag in p:
        main = main+tag.text
    edu["description"] = main
    #print(main)
    img = div.find_all('img')
    i = 0
    for tag in img:
        i = i+1
        src = home+tag["src"]
        edu["img"] = src
        #print("活动写照:"+src)
        #if i == 3:
        break
    edu["mname"] = "江汉关博物馆"
    return edu

url = "https://baike.sogou.com/v139691332.htm?fromTitle=%E6%B1%9F%E6%B1%89%E5%85%B3%E5%8D%9A%E7%89%A9%E9%A6%86"
x = get_brief(url)
a = []
a.append(x)

exhibitions = []
print("------展览陈列------")
url = "http://www.jhgmuseum.com/section-50.html"
x = show(url)
x["name"] = "武汉国民政府旧址"
exhibitions.append(x)
print("\n")
url = "http://www.jhgmuseum.com/section-49.html"
x = show(url)
x["name"] = "詹天佑故居"
exhibitions.append(x)
print("\n")
url = "http://www.jhgmuseum.com/section-27.html"
x = show(url)
x["name"] = "《江汉朝宗——武汉城市现代化历程》"
exhibitions.append(x)
print("\n")

educational = []
print("------教育活动------")
url = "http://www.jhgmuseum.com/article-614.html"
z = education(url)
z["name"] = "出彩江汉关 | 踏青迎春度清明，缅怀先祖寄哀思"
z["time"] = "2019年04月08日"
educational.append(z)
print("\n")
url = "http://www.jhgmuseum.com/article-580.html"
z = education(url)
z["name"] = "江汉关博物馆送中秋知识进小学"
z["time"] = "2018年09月21日"
educational.append(z)
print("\n")
url = "http://www.jhgmuseum.com/article-388.html"
z = education(url)
z["name"] = "无诗书 不青春——江汉关博物馆开展“悦读青春·再识鲁迅”五四专题活动"
z["time"] = "2018年05月04日"
educational.append(z)
print("\n")
url = "http://www.jhgmuseum.com/article-390.html"
z = education(url)
z["name"] = "落梅生春度新年"
z["time"] = "2018年01月14日"
educational.append(z)
print("\n")

museum_info["1"] = a
museum_info["2"] = exhibitions
museum_info["3"] = []
museum_info["4"] = educational

save_data(museum_info)