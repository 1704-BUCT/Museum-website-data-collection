import requests
import re
import bs4
from bs4 import BeautifulSoup
import bs4
headers ={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0'
    }

#全局变量
global mid,eid,oid
mid = int(0)
eid = int(0)
oid = int(0)

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
        try:
            sql_1 = "insert into museums(name,imgurl,mobile,address,introduction,opentime) values(%s,%s,%s,%s,%s,%s)"
            data_1 = [dict1['1']["name"],dict1['1']["main_image_url"],dict1["1"]['number'],dict1["1"]['location'],dict1['1']['brief'],dict1['1']['opentime']]
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

museum_info = {}

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
    soup = get_soup1(url)
    print("------博物馆简介------")
    brief = soup.find('div',id = 'j-shareAbstract',style = 'display: none')
    description = brief.text
    print(description)
    print("------参观信息------")
    visit = soup.find('table',class_ ='abstract_tbl')
    info = visit.find_all('tr')
    for tag in info:
        title = tag.find('th',class_ = 'base-info-card-title')
        print(title.text+":",end="")
        texts = tag.find('div',class_ = 'base-info-card-value').find(text=True).strip()
        print(texts)
    visited = "每周二至周日9：00-17：00\n每日16：30停止入场\n逢周一闭馆（法定节假日和特殊情况除外）\n馆址：广州市越秀区二沙岛烟雨路38号\n前台电话：020-87351468 "
    print(visited)

def show(url):
    exhibition = {}
    home = "http://www.gdmoa.org"
    soup = get_soup1(url)
    p = soup.find('p',attrs={'class':'mt20'})
    print(p.text)
    print("展览作品:")
    x = soup.find_all('div',attrs={'class':'swiper-slide'})
    i = 0
    for tag in x:
        i = i+1
        dt = tag.find('dt',attrs={'class':'mt10 dis-in-b'})
        print(dt.text,end="       ")
        imgs = tag.find('img')
        src = home+imgs["src"]
        print("展品图示:"+src)
        if i == 5:
            break

def education(url):
    edu = {}
    home = "http://www.gdmoa.org"
    soup = get_soup1(url)
    p = soup.find('p',attrs={'class':'mt20'})
    edu["description"] = p.text
    #print(p.text)
    x = soup.find_all('div',attrs={'class':'swiper-slide'})
    i = 0
    for tag in x:
        i = i+1
        imgs = tag.find('img')
        src = home+imgs["src"]
        edu["img"] = src
        #print("活动写照:"+src)
        #if i == 3:
        break
    edu["mname"] = "广东美术馆"
    return edu

url = "https://baike.sogou.com/v154492.htm?fromTitle=%E5%B9%BF%E4%B8%9C%E7%BE%8E%E6%9C%AF%E9%A6%86"
get_brief(url)

print("------展览陈列------")
url = "http://www.gdmoa.org/Exhibition/Current/202004/t20200429_16597.shtml"
show(url)
print("\n")
url = "http://www.gdmoa.org/Exhibition/Current/202004/t20200423_16587.shtml"
show(url)
print("\n")
url = "http://www.gdmoa.org/Exhibition/Current/202004/t20200414_16584.shtml"
show(url)
print("\n")

print("------教育活动------")
url = "http://www.gdmoa.org/Public_Education/Lecture/201909/t20190904_16202.shtml"
education(url)
print("\n")
url = "http://www.gdmoa.org/Public_Education/Lecture/201904/t20190404_16015.shtml"
education(url)
print("\n")
url = "http://www.gdmoa.org/Public_Education/Lecture/201904/t20190424_16050.shtml"
education(url)
print("\n")

