import requests
import bs4
import re
from bs4 import BeautifulSoup
import bs4
import pymysql

headers = { #搜狗百科消息头
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
    src = img["src"]
    print("------参观信息------")
    visit = soup.find('table',class_ ='abstract_tbl')
    info = visit.find_all('tr')
    for tag in info:
        title = tag.find('th',class_ = 'base-info-card-title')
        #print(title.text+":",end="")
        texts = tag.find('div',class_ = 'base-info-card-value').find(text=True).strip()
        #print(texts)
    brief["name"] = "江西省博物馆"
    brief["img"] = src
    brief["location"] = "市1号线滕王阁站下车，至新洲路往北200米。"
    brief["number"] = "咨询电话：0791-88233369"
    brief["opentime"] = "免费开放时间：周二至周日9:00-17:00（16:00停止入馆），周一闭馆（法定节假日除外）。 " 
    return brief

def get_soup(url):
    res = requests.get(url,headers = headers)
    res.encoding = 'utf-8'
    html = res.text
    soup = BeautifulSoup(html,'html.parser')
    return soup 

def show(url): #展览陈列
    exhibition = {}
    soup = get_soup(url)
    table = soup.find('div',attrs = {'class':'maindetail'})
    texts = table.find('div',attrs={'class':'cont'})
    print("展览介绍:")
    exhibition["description"] = texts.text
    #print(texts.text)
    img = table.find("img")
    src = img["src"] #展览照片
    #print("展览照片:"+src)
    exhibition["img"] = src
    exhibition["mname"] = "江西省博物馆"
    return exhibition

def get_object(url): #得到典藏信息
    collection = {}
    soup = get_soup(url)
    object = soup.find('div',attrs={'class':'maindetail'})
    texts = object.find('div',class_= 'cont').text
    #print(object.find('div',class_ ='cont').text)
    collection["description"] = texts
    img = object.find("img")
    src = img["src"] #得到图片链接
    #print("图片链接:"+src)
    collection["img"] = src
    collection["mname"] = "江西省博物馆"
    return collection

def education(url):
    edu = {}
    soup = get_soup(url)
    edu = soup.find('div',class_ ='maindetail')
    main = edu.find('div',attrs={'class':'cont'})
    #print(main.text)
    edu["description"] = main
    img = edu.find("img")
    src = img["src"]
    #print("活动照片:"+src)
    edu["img"] = src
    edu["mname"] = "江西省博物馆"
    return edu

#展览陈列
exhibitions = []
print("------展览陈列------")
url = "http://www.jxmuseum.cn/Exhibition/TempDisplayDetails/10066?cno=jbcl"
x = show(url)
x["name"] = "物华新诗——赣鄱非遗展"
exhibitions.append(x)
print("\n")
url = "http://www.jxmuseum.cn/Exhibition/TempDisplayDetails/10068?cno=jbcl"
x = show(url)
x["name"] = "红色摇篮 ——江西革命史陈列"
exhibitions.append(x)
print("\n")
url = "http://www.jxmuseum.cn/Exhibition/TempDisplayDetails/10047?cno=jbcl"
x = show(url)
x["name"] = "惊世大发现——南昌汉代海昏侯国考古成果展"
exhibitions.append(x)
print("\n")
url = "http://www.jxmuseum.cn/Exhibition/TempDisplayDetails/10048?cno=jbcl"
x = show(url)
x["name"] = "赣风鄱韵——江西古代文明"
exhibitions.append(x)
print("\n")
url = "http://www.jxmuseum.cn/Exhibition/TempDisplayDetails/10049?cno=jbcl"
x = show(url)
x["name"] = "红色摇篮"
exhibitions.append(x)
print("\n")

collections = []
#爬取典藏珍品
print("------典藏珍品------")
url = "http://www.jxmuseum.cn/Collection/Details/59f9c088-5d1b-46c7-94b4-3ef93768f7d6"
y = get_object(url)
y["name"] = "弦纹高足红陶杯"
collections.append(y)
print("\n")
url = "http://www.jxmuseum.cn/Collection/Details/c6c137e4-5695-4367-9dc5-5f38fe3154db"
y = get_object(url)
y["name"] = "圈点纹假腹原始瓷豆"
collections.append(y)
print("\n")
url = "http://www.jxmuseum.cn/Collection/Details/9b7283b5-d70c-4fdf-b95f-efe1a5cee30a"
y = get_object(url)
y["name"] = "云纹兽首提梁黑陶盉"
collections.append(y)
print("\n")
url ="http://www.jxmuseum.cn/Collection/Details/5f168fb3-9e5b-46d2-a3be-d99a8b4f7cb6"
y = get_object(url)
y["name"] = "青瓷水波纹簋"
collections.append(y)
print("\n")
url = "http://www.jxmuseum.cn/Collection/Details/b9e44587-6d8f-4af4-9bed-6ba02905f3c7"
y = get_object(url)
y["name"] = "青瓷多足辟雍砚"
collections.append(y)
print("\n")

educational = []
#教育活动
print("------教育活动------")
url = "http://www.jxmuseum.cn/News/Details/d91e9b3d-47dc-42fb-8c61-396e1dacaf7b"
z = education(url)
z["name"] = "江西历史文化”大讲堂之二：兴学重教，以文化人——江西民办书院的杰出贡献"
z["time"] = "时间：2018.11.10"
educational.append(z)
print("\n")
url = "http://www.jxmuseum.cn/News/Details/197b9b57-9647-4b04-8297-ea0c0f99e00e"
z = education(url)
z["name"] = "首届全国博物馆志愿者培训 我馆志愿者代表参会学习"
z["time"] = "时间：2018.12.26"
educational.append(z)
print("\n")
url = "http://www.jxmuseum.cn/News/Details/e23b471a-c0a5-4433-becb-166ca5d981d4"
z = education(url)
z["name"] = "江西省博物馆2019年“三区专项活动”社教篇——红色文化进校园（四）"
z["time"] = "时间：2019.12.02"
educational.append(z)
print("\n")

url = "https://baike.sogou.com/v163337.htm?fromTitle=%E6%B1%9F%E8%A5%BF%E7%9C%81%E5%8D%9A%E7%89%A9%E9%A6%86"
x = get_brief(url)
a = []
a.append(x)

museum_info["1"] = []#a
museum_info["2"] = exhibitions
museum_info["3"] = []#collections
museum_info["4"] = educational

save_data(museum_info)