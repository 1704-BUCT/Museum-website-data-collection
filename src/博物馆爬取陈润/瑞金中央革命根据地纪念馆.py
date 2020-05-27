import requests
import bs4
import re
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
    src = "http://www.rjjng.com.cn/cms/resource/img/h000/h01/img201410141655490.jpg"
    print("------参观信息------")
    visit = soup.find('table',class_ ='abstract_tbl')
    info = visit.find_all('tr')
    #for tag in info:
        #title = tag.find('th',class_ = 'base-info-card-title')
        #print(title.text+":",end="")
        #texts = tag.find('div',class_ = 'base-info-card-value').find(text=True).strip()
        #print(texts)
    brief["name"] = "瑞金中央革命根据地纪念馆"
    brief["img"] = src
    brief["location"] = "江西省瑞金市城西龙珠路1号"
    brief["number"] = "电话：0797-2522063"
    brief["opentime"] = "8:30 ----- 17:30（夏季） 8:30 ----- 17:00（冬季） （旧址景区全年开放，博物馆星期一闭馆检修，法定节假日除外）" 
    return brief

def visit(url):
    print("-----参观信息------")
    soup = get_soup(url)
    div = soup.find('div',attrs={'class':'lyzn'})
    h3 = div.find('h3')
    print(h3.text,end=" ")
    p = div.find('p')
    print(p.text)
    visit = "地址：江西省瑞金市城西龙珠路1号\n"
    visit = visit+"电话：0797-2522063\n传真：0797-2508358\nE-mail：jngxjb@163.com "
    print(visit)

def show(url,temp):
    exhibition = {}
    soup = get_soup(url)
    div = soup.find('div',attrs={'class':'mainbar_content'})
    img = div.find_all('img')
    i = 0
    for tag in img:
        i = i+1
        src = tag["src"]
        exhibition["img"] = src
        #print("展览图示:"+src)
        #if i == 4:
        break
    exhibition["description"] = ""
    exhibition["mname"] = "瑞金中央革命根据地纪念馆"
    exhibition["name"] = temp
    return exhibition

def object(url,temp):
    collection = {}
    soup = get_soup(url)
    div = soup.find('div',attrs={'class':'mainbar_content'})
    p = div.find('p')
    #print(p.text)
    collection["description"] = p.text
    img = div.find_all('img')
    for tag in img:
        src = tag["src"]
        collection["img"] = src
        #print("藏品图片:"+src)
        break
    collection["name"] = temp
    collection["mname"] = "瑞金中央革命根据地纪念馆"
    return collection

def education(url,temp,time):
    edu = {}
    soup = get_soup(url)
    div = soup.find('div',attrs={'class':'mainbar_content'})
    p = div.find('p')
    #print(p.text)
    edu["description"] = p.text
    img = div.find_all('img')
    i = 0
    for tag in img:
        i = i+1
        src = tag["src"]
        edu["img"] = src
        #print("活动写照:"+src)
        #if i == 3:
        break
    edu["name"] = temp
    edu["time"] = time
    edu["mname"] = "瑞金革命根据地纪念馆"
    return edu

url = "https://baike.sogou.com/v70063481.htm?fromTitle=%E7%91%9E%E9%87%91%E4%B8%AD%E5%A4%AE%E9%9D%A9%E5%91%BD%E6%A0%B9%E6%8D%AE%E5%9C%B0%E7%BA%AA%E5%BF%B5%E9%A6%86"
x = get_brief(url)
a = []
a.append(x)

url = "http://www.rjjng.com.cn/new_index.html"
soup = get_soup(url)
visit(url)

exhibitions = []
print("------展览陈列------")
url = "http://www.rjjng.com.cn/display/2018/19901543369803.html"
temp = "伟大的长征从这里出发"
x = show(url,temp)
exhibitions.append(x)
print("\n")
url = "http://www.rjjng.com.cn/display/2019/20661555916577.html"
temp = "周恩来与文化名人展"
x = show(url,temp)
exhibitions.append(x)
print("\n")
url = "http://www.rjjng.com.cn/display/2018/19961544769262.html"
temp = "守护共和国摇篮——瑞金中央革命根据地纪念馆60周年成就展"
x = show(url,temp)
exhibitions.append(x)
print("\n")

collections = []
print("------典藏珍品------")
url = "http://www.rjjng.com.cn/treasure/2013/5901379907998.html"
temp = "二等铜质红星奖章"
y = object(url,temp)
collections.append(y)
print("\n")
url = "http://www.rjjng.com.cn/treasure/2013/5931379908555.html"
temp = "中央印刷厂石印机"
y = object(url,temp)
collections.append(y)
print("\n")
url = "http://www.rjjng.com.cn/treasure/2013/5921379908524.html"
temp = "纪念赵博生石碑刻"
y = object(url,temp)
collections.append(y)
print("\n")
url = "http://www.rjjng.com.cn/treasure/2013/5881379907838.html"
temp = "二苏大会主席团证章"
y = object(url,temp)
collections.append(y)
print("\n")
url = "http://www.rjjng.com.cn/treasure/2013/5691379906591.html"
temp = "中央执委会电话机"
y = object(url,temp)
collections.append(y)
print("\n")

educational = []
print("------教育活动------")
url = "http://www.rjjng.com.cn/news/2019/21011562727039.html"
temp = "学党章 守初心 强担当——瑞金中央革命根据地纪念馆开展党日活动"
time = "2019年7月5日"
z = education(url,temp,time)
educational.append(z)
print("\n")
url = "http://www.rjjng.com.cn/news/2019/21061565658222.html"
temp = "浙江大学学生在我馆开展社会实践活动"
time = "2019年8月9日—11日"
z = education(url,temp,time)
educational.append(z)
print("\n")
url = "http://www.rjjng.com.cn/news/2019/20931560477446.html"
temp = "我馆开展消防知识培训讲座"
time = "2019年6月13日"
z = education(url,temp,time)
educational.append(z)
print("\n")

museum_info["1"] = a
museum_info["2"] = exhibitions
museum_info["3"] = collections
museum_info["4"] = educational

save_data(museum_info)