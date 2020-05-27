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
    img = div.find('img',attrs={'width':'250'})
    src = img["src"]
    src = "http://www.rjjng.com.cn/cms/resource/img/h000/h01/img201410141655490.jpg"
    print("------参观信息------")
    visit = soup.find('table',class_ ='abstract_tbl')
    info = visit.find_all('tr')
    #for tag in info:
        #title = tag.find('th',class_ = 'base-info-card-title')
        #print(title.text+":",end="")
        #texts = tag.find('div',class_ = 'base-info-card-value').find(text=True).strip()
        #print(texts)
    brief["name"] = "山东博物馆"
    brief["img"] = src
    brief["location"] = "馆址：济南市经十路11899号"
    brief["number"] = "预约电话: 0531-85058202"
    brief["opentime"] = "周二至周日9:00—17:00开馆，16:00停止入馆 （除国家法定节假日）闭馆" 
    return brief

def show(url):
    exhibition = {}
    home = "http://www.sdmuseum.com/"
    soup = get_soup(url)
    div = soup.find('div',attrs={'class':'zl3-con'})
    title = div.find('div',attrs={'class':'zl3-title'})
    #print(title.text)#展览主题
    exhibition["name"] = title.text
    main = ""
    p = div.find_all('p')
    for tag in p:
        main = main+tag.text
    #print(main)
    exhibition["description"] = main
    li = div.find_all('li')
    for tag in li:
        img = tag.find("img")
        src = home+img["src"]
        exhibition["img"] = src
        #print("展览图示:"+src)
        break
    exhibition["mname"] = "山东博物馆"
    return exhibition

def object(url,temp):
    collection = {}
    home = "http://www.sdmuseum.com/"
    soup = get_soup(url)
    div = soup.find('div',attrs={'class':'zx-c_r'})
    title = div.find('hl',attrs={'class':'zx-dis_title'})
    main = ""
    p = div.find_all('p')
    for tag in p:
        main = main+tag.text
    #print(main)
    collection["description"] = main
    img = div.find("img")
    src = home+img["src"]
    #print("典藏图片:"+src)
    collection["img"] = src
    collection["mname"] = "山东博物馆"
    collection["name"] = temp
    return collection

def education(url,temp,time):
    edu = {}
    soup = get_soup(url)
    td = soup.find_all('td',attrs={'width':'100%'})
    main = ""
    for tag in td:
        main = main+tag.text
    #print(main)
    edu["description"] = main
    edu["mname"] = "山东博物馆"
    edu["name"] = temp
    edu["time"] = time
    edu["img"] = ""
    return edu

url = "https://baike.sogou.com/v168021938.htm?fromTitle=%E5%B1%B1%E4%B8%9C%E5%8D%9A%E7%89%A9%E9%A6%86"
x = get_brief(url)
a = []
a.append(x)
print("\n")

exhibitions = []
print("------展览陈列------")
url = "http://www.sdmuseum.com/channels/ch00037/"
x = show(url)
exhibitions.append(x)
print("\n")
url = "http://www.sdmuseum.com/channels/ch00029/"
x = show(url)
exhibitions.append(x)
print("\n")
url = "http://www.sdmuseum.com/channels/ch00021/"
x = show(url)
exhibitions.append(x)
print("\n")

collections = []
#典藏珍品
print("------典藏珍品------")
url = "http://www.sdmuseum.com/articles/ch00079/201705/34d8818a-222a-48b5-ab73-a898e340564e.shtml"
temp = "红陶兽形器"
y = object(url,temp)
collections.append(y)
print("\n")
url = "http://www.sdmuseum.com/articles/ch00081/201707/5e534a35-4c6b-4154-859b-0f8eaa33f517.shtml"
temp = "元钧窑三足炉"
y = object(url,temp)
collections.append(y)
print("\n")
url = "http://www.sdmuseum.com/articles/ch00083/201705/496cd6f5-ee45-449b-9dd9-674fe6dad822.shtml"
temp = "祖辛方鼎"
y = object(url,temp)
collections.append(y)
print("\n")
url = "http://www.sdmuseum.com/articles/ch00099/201705/5dfc4796-2406-4ae7-a821-dcd38992d0fa.shtml"
temp = "董其昌行草书轴"
y = object(url,temp)
collections.append(y)
print("\n")
url = "http://www.sdmuseum.com/articles/ch00101/201705/a7e9aefd-64be-4c86-8c40-bdcacd7dfc56.shtml"
temp = "张舜咨苍鹰竹梧图轴"
y = object(url,temp)
collections.append(y)
print("\n")

educational = []
#教育活动
print("------教育活动------")
url = "http://www.sdmuseum.com/articles/ch00129/201910/0398ac00-7650-42c6-85f1-0f8dd6553864.shtml"
temp = "“穿”越千年——文质彬彬做君子 "
time = "2019年11月3日、10日、17日、24日上午10：00——11：00"
z = education(url,temp,time)
educational.append(z)
print("\n")
url = "http://www.sdmuseum.com/articles/ch00131/201911/838efed7-ec54-4cc6-8493-fc202a422c6b.shtml"
temp = "“穿”越千年——织经编纬 "
time = "2019年11月3日、17日、30日下午14：00——15：00"
z = education(url,temp,time)
educational.append(z)
print("\n")
url = "http://www.sdmuseum.com/articles/ch00133/201911/4d4c7735-5f7e-467a-baa1-5830eac71136.shtml"
temp = "“穿”越千年——华服美裳 "
time = "2019年11月2日、9日、16日、23日下午14：00——15：00"
z = education(url,temp,time)
educational.append(z)
print("\n")

museum_info["1"] = []#a
museum_info["2"] = []#exhibitions
museum_info["3"] = []#collections
museum_info["4"] = educational

save_data(museum_info)