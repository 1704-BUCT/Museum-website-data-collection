import requests
import bs4
from bs4 import BeautifulSoup
import re
#import MySQLdb
import pymysql
import time
import datetime
pymysql.install_as_MySQLdb()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
}
def get_all(url):
    re=requests.get(url,headers=headers)
    re.encoding='utf-8'
    soup = BeautifulSoup(re.text, 'html.parser')
    return soup
def get_all_new(url):
    requests.packages.urllib3.disable_warnings()
    res=requests.get(url,headers=headers,verify=False)
    res.encoding='utf-8'
    x = BeautifulSoup(res.text, 'html.parser')
    return x
def get_all_x(url):
    re=requests.get(url,headers=headers)
    re.encoding='GBK'
    soup = BeautifulSoup(re.text, 'html.parser')
    return soup
def gettext(url):
    try:
        r=requests.get(url)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup
    except:
        return ""
#全局变量
global mid,eid,oid
mid=int(0)
eid=int(0)
oid=int(0)
#匹配年
pattern_year = re.compile(r'\b\d{4}年\d{1,2}月\d{1,2}日\b|\b\d{4}年\d{1,2}月\b|\b\d{4}年\b')
#匹配时间
pattern_time = re.compile(r'\d{1,2}:\d{2}|\d{1,2}：\d{2}')
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
        try:
            sql_1 = "insert into museums(name,imgurl,mobile,address,introduction,opentime) values(%s,%s,%s,%s,%s,%s)"
            data_1 = [dict1['1']["name"],dict1['1']["main_image_url"],dict1["1"]['number'],dict1["1"]['location'],dict1['1']['bref'],dict1['1']['opentime']]
            self.cursor.execute(sql_1,data_1)
            self.db.commit() # 提交操作
        except:
            self.db.rollback()
        sql_2 = "insert into exhibitions(name,imgurl,introduction,mname) values(%s,%s,%s,%s)"
        for i in dict1["2"]:
            data_2 = [i["name"],i["img"],i['description'],dict1['1']["name"]]
            try:
                self.cursor.execute(sql_2,data_2)
                self.db.commit() # 提交操作
            except:
                self.db.rollback()
        sql_3 = "insert into collections(name,imgurl,introduction,mname) values(%s,%s,%s,%s)"
        for i in dict1["3"]:
            data_3 = [i["name"],i["img"],i['description'],dict1['1']["name"]]
            try:
                self.cursor.execute(sql_3,data_3)
                self.db.commit() # 提交操作
            except:
                self.db.rollback()

        sql_4 = "insert into educations(name,imgurl,introduction,time,mname) values(%s,%s,%s,%s,%s)"
        for i in dict1["4"]:
            data_4 = [i["name"],i["img"],i['description'],i['time'],dict1['1']["name"]]
            try:
                self.cursor.execute(sql_4,data_4)
                self.db.commit() # 提交操作
            except:
                self.db.rollback()

        self.db.close()

    def dataselect(self,issue,db_table):
        try:
            sql = "SELECT '%s' FROM %s " % (issue, db_table)
            self.cursor.execute(sql)
            self.db.commit() # 提交操作
        except:
            self.db.rollback()
        finally:
            return issue

    def update(self,dict1):
        sql_2 = "insert into exhibitions(name,imgurl,introduction,mname) values(%s,%s,%s,%s)"
        for i in dict1["2"]:
            if(self.dataselect(i["name"],"exhibitions")!=i["name"]):
                data_2 = [i["name"],i["img"],i['description'],dict1['1']["name"]]
                try:
                    self.cursor.execute(sql_2,data_2)
                    self.db.commit() # 提交操作
                except:
                    self.db.rollback()
def save_data(dict_data):
    # 存数据库
    database = ConnMysql()
    database.insert(dict_data)
    #数据更新
    # now = datetime.datetime.now()
    # sched_time = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, now.second) +\
    #         datetime.timedelta(days=14)
    # while True:
    #     now = datetime.datetime.now()
    #     if sched_time < now:
    #         print(now)
    #         database.update(dict_data)
    #         sched_time+=datetime.timedelta(days=14)


def get_jilin_Proviencial_Museum():
    url="http://www.jlmuseum.org"
    url_1="http://jlmuseum.org/description"
    url_2="http://jlmuseum.org/display/"
    url_3="http://jlmuseum.org/collection/"
    url_4="http://jlmuseum.org/activitys/"
    name="吉林省博物院"
    url_s="https://baike.sogou.com/v8827701.htm?fromTitle=吉林省博物院"
    main_img_url=get_all(url_s).find("a",{'class':"ed_image_link"}).find("img")['src']
    hostinfo=get_all(url_1)
    #简介
    opentime="每周二至周日9：30——15：30（15：00停止入馆）；每周一闭馆（国家法定节假日除外）"
    bref=[]
    for i in hostinfo.find_all("p",attrs={'class':{"p","MsoNormal"}}):
        bref=i
        #print(bref.text)  
    #地址与电话
    location=[]
    number=""
    number=get_all(url).find("div",{'class':"footer"}).text
    number=re.search(re.compile(r'电话：\d+-\d+'),str(number)).group()
    for i in hostinfo.find_all("div",attrs={'class':"footer"}):
        for j in i.find_all("p"):
            if(re.search(re.compile(r'长春'),str(j))):
                location=j
    #print(location.text)
    #陈列展览
    exhibition_hall=[]
    info_exh=get_all(url_2)
    for i in info_exh.find_all("div",attrs={'class':"list"}):
        for j in i.find_all("li"):
              a={}
              a["name"]=j.find("a",attrs={'class':"thumb"})['title']
              a["img"]=url+j.find("img",attrs={'class':"lazy"})['_src']
              url_next=url+j.find("a",attrs={'class':"thumb"})['href']
              exh_next=get_all(url_next).find('div',attrs={'class':"pics-cont"}).text
              a["description"]=''.join(exh_next.split())
              #print(a)
              exhibition_hall.append(a)
    #print(exhibition_hall)
    #馆藏精品
    info_projects=get_all(url_3).find("div",{'class':"list-pics"})
    exhibition_projects=[]
    for i in info_projects.find_all("div",attrs={'class':"thumb"}):
        a={}
        a["name"]=i.find("a")["title"]
        a["img"]=url+i.find("img")['src']
        url_next=url+i.find("a")["href"]
        pro_next=get_all(url_next).find("div",attrs={'class':"pics-cont"}).text
        a["description"]=''.join(pro_next.split())
        #print(a)
        exhibition_projects.append(a)
    #print(exhibition_projects)
    #教育活动
    info_edu=get_all(url_4).find("div",attrs={'class':"list-txt"})
    exhibition_edu=[]
    for i in info_edu.find_all("li"):
        a={}
        a["time"]=i.find("span",{'class':"date"}).text
        a["name"]=i.find("a")['title']
        url_next=url+i.a['href']
        a["img"]=url+get_all(url_next).find("div",attrs={'class':"cont"}).find("img")['src']
        move=get_all(url_next).find_all("p",attrs={'class':"MsoNormal"})
        a["description"]=[]
        for j in move:
            j=''.join(j.text.split())
            a["description"].append(j)
        #print(a)
        exhibition_edu.append(a)
    #print(exhibition_edu)
    info_main={}
    info_main["bref"]=bref
    info_main["main_image_url"]=main_img_url
    info_main["opentime"]=opentime
    info_main["name"]=name
    info_main["location"]=location
    info_main["number"]=number
    info_all={}
    info_all["1"]=info_main
    info_all["2"]=exhibition_hall
    info_all["3"]=exhibition_projects
    info_all["4"]=exhibition_edu

    # print(info_all)
    return info_all
#get_jilin_Proviencial_Museum()
def get_Museum_of_Heilongjiang_Province():
        url="http://www.hljmuseum.com"
        url_1="http://www.hljmuseum.com/system/200910/101021.html"
        url_2="http://www.hljmuseum.com/clzl/"
        url_3="http://www.hljmuseum.com/cpgz/"
        url_4="http://www.hljmuseum.com/bwgjy/lbjy/"
        name="黑龙江省博物院"
        main_img_url="https://pic.baike.soso.com/ugc/baikepic2/42136/20161021185731-1769601176.jpg/300"
        hostinfo=get_all(url_1)
        #简介
        ot=get_all("http://www.hljmuseum.com/system/201708/102053.html").find("div",{'class':"duanluo"}).find("p").text
        opentime=''.join(ot.split())
        bref=[]
        for i in hostinfo.find_all("div",attrs={'class':"duanluo"}):
             for j in i.find_all('p',attrs={'class':"MsoNormal"}):
                     bref=j.text
                     #print(bref)
        #地址与电话
        location=""
        number=""
        for i in str(get_all(url).find_all('div',attrs={'id':"foot-bq"})).split("<br/>"):
             if(re.search(re.compile(r'地址：'),i)):
                  mes=''.join(i.split())
                  mes=i.split()
                  location=mes[0]
                  number=mes[1]
        #print(location,number)
        #陈列展览
        exhibition_hall=[]
        info_exh=get_all(url_2)
        for i in info_exh.find_all("div",attrs={'class':"wxd-part fl"}):
            exh=i.find_all("li")
        tag=0
        for j in exh:
            if(tag<10) :
                a={}
                url_next=url+j.a["href"]
                info_next=get_all(url_next)
                a["name"]=info_next.find("h2").text
                a["img"]=url+info_next.find("img")['src']
                detail=info_next.find("div",attrs={'class':"duanluo"}).text
                a["description"]=''.join(detail.split())
                exhibition_hall.append(a)
                #print(a)
            tag=tag+1
        #print(exhibition_hall)
        #馆藏精品
        info_projects=get_all(url_3).find("div",{'class':"wxd-part fl"})
        exhibition_projects=[]
        for i in info_projects.find_all("div",attrs={'class':"wxd-li"}):
            a={}
            url_next=url+i.find("a")['href']
            info_next=get_all(url_next)
            a["name"]=info_next.find('h2').text
            a["img"]=url+info_next.find("img")['src']
            detail=info_next.find("div",attrs={'class':"duanluo"}).text
            a["description"]=''.join(detail.split())
            #print(a)
            exhibition_projects.append(a)
        #print(exhibition_projects)
        #教育活动
        info_edu=get_all(url_4).find("div",attrs={'class':"erji-left fl"})
        exhibition_edu=[]
        for i in info_edu.find_all("li"):
            a={}
            a["time"]=i.find("span").text
            a["name"]=i.find("a").text
            url_next=url+i.a['href']
            a["img"]=url+get_all(url_next).find("div",attrs={'class':"duanluo"}).find("img")['src']
            detail=get_all(url_next).find("div",attrs={'class':"duanluo"}).text
            a["description"]=''.join(detail.split())
            #print(a)
            exhibition_edu.append(a)
        #print(exhibition_edu)
        info_main={}
        info_main["bref"]=bref
        info_main["main_image_url"]=main_img_url
        info_main["opentime"]=opentime
        info_main["name"]=name
        info_main["location"]=location
        info_main["number"]=number
        info_all={}
        info_all["1"]=info_main
        info_all["2"]=exhibition_hall
        info_all["3"]=exhibition_projects
        info_all["4"]=exhibition_edu
        #print(info_all)
        return(info_all)
#get_Museum_of_Heilongjiang_Province()
def get_Shanghai_Luxun_Museum():
    url="http://www.luxunmuseum.cn"
    url_1="http://www.luxunmuseum.cn/lxcl/index.html"
    url_2="http://www.luxunmuseum.cn/cp/index.html"
    url_3="http://www.luxunmuseum.cn/news/index/cid/1.html"
    name="上海鲁迅纪念馆"
    main_img_url="https://pic.baike.soso.com/ugc/baikepic2/50746/20160729010219-467037505.jpg/300"
    hostinfo=get_all(url)
    #简介
    ot=get_all("http://www.luxunmuseum.cn/index/index.html").find("p",{'style':"color:#ccc;"}).text
    opentime=''.join(ot.split())
    bref=[]
    for i in hostinfo.find_all("div",attrs={'class':"am-container"}):
        for j in i.find_all("p",attrs={'style':"text-indent: 4ch;font-size:1.4rem;line-height: 20px;"}):
            j=''.join(j.text.split())
            bref.append(j)
    #print(bref)
    #地址与电话
    location=""
    number=""
    mes=hostinfo.find('footer',attrs={'class':"footer"}).find("p").text
    if(re.search(re.compile(r'地址：[\u4e00-\u9fa5].+号'),str(mes))):
        location=re.search(re.compile(r'地址：[\u4e00-\u9fa5].+号'),str(mes)).group()
    number=re.search('电话：\d+-\d+-\d+',str(mes)).group()
    #print(location)
    #print(number)
    #陈列展览
    exhibition_hall=[]
    info_exh=get_all(url_1).find("div",attrs={'class':"am-u-md-3 am-u-md-pull-9 my-sidebar"})
    for i in info_exh.find_all("a"):
        a={}
        url_next=url+i['href']
        info_next=get_all(url_next).find("div",attrs={'class':"am-cf am-article"})
        a["name"]=info_next.find("h3").text
        a["img"]=info_next.find("img")['src']
        content=get_all(url_next).find("div",attrs={'class':"am-cf am-article"}).texta["description"]=''.join(content.split())
        #print(a)
        exhibition_hall.append(a)
    #print(exhibition_hall)
    #馆藏精品
    info_projects=get_all(url_2).find("div",{'class':"am-g"})
    exhibition_projects=[]
    for i in info_projects.find("div",attrs={'class':"am-g"}).find_all("li"):
        a={}
        url_next=url+i.find("a")['href']
        info_next=get_all(url_next).find("div",attrs={'class':"am-u-md-9 am-u-md-push-3"})
        a["name"]=info_next.find("h2").text
        a["img"]=info_next.find("li")['data-thumb']
        for i in get_all(url_next).find("div",attrs={'class':"am-g am-g-fixed"}).find("div",attrs={'class':"am-u-md-9 am-u-md-push-3"}).find_all("div",attrs={'class':"am-g"}):
            a["description"]=i.find("div",attrs={'class':"am-u-sm-11 am-u-sm-centered"}).text
            a["description"]=''.join(a["description"].split())
        exhibition_projects.append(a)
        #print(a)
    print(exhibition_projects)
    #教育活动
    info_edu=get_all(url_3).find("div",attrs={'class':"am-u-md-9 am-u-md-push-3"})
    exhibition_edu=[]
    for i in info_edu.find_all("div",attrs={'class':"am-article-list"}):
        a={}
        url_next=url+i.a['href']
        if(url_next=="http://www.luxunmuseum.cn/news/page/id/201.html"):
            continue
        elif(url_next=="http://www.luxunmuseum.cn/news/page/id/174.html"):
            continue
        else:
            info_next=get_all(url_next).find("div",attrs={'class':"am-u-md-9 am-u-md-push-3"})
            a["time"]=info_next.find("p").text
            a["name"]=info_next.find("h2").text
            a["img"]=info_next.find("div",attrs={'class':"am-g"}).find("img")['src']
            contents=info_next.find("div",attrs={'class':"am-u-sm-11 am-u-sm-centered"}).text
            a["description"]=''.join(contents.split())
            exhibition_edu.append(a)
            #print(a)
    #print(exhibition_edu)
    info_main={}
    info_main["bref"]=bref
    info_main["main_image_url"]=main_img_url
    info_main["opentime"]=opentime
    info_main["name"]=name
    info_main["location"]=location
    info_main["number"]=number
    info_all={}
    info_all["1"]=info_main
    info_all["2"]=exhibition_hall
    info_all["3"]=exhibition_projects
    info_all["4"]=exhibition_edu

    #print(info_all)
    return(info_all)
#get_Shanghai_Luxun_Museum()
def get_qinhuarijunnanjingdatushayunantongbaojilianguan():
    url="http://www.19371213.com.cn"
    url_1="http://www.19371213.com.cn/about/museum/201608/t20160827_5907664.html"
    url_2="http://www.19371213.com.cn/exhibition/"
    url_3="http://www.19371213.com.cn/collection/featured/"
    url_4="http://www.19371213.com.cn/learn/community/"
    name="侵华日军南京大屠杀遇难同胞纪念馆"
    main_img_url="https://pic.baike.soso.com/ugc/baikepic2/31734/cut-20190522131621-120761876_jpg_394_315_21739.jpg/300"
    hostinfo=get_all(url_1)
    #简介
    ot=get_all("http://www.19371213.com.cn/guide/how/#开放时间").find("div",{'class':"col-md-9"}).text
    opentime=''.join(ot.split())
    bref=[]
    bref=hostinfo.find("div",attrs={'class':"content-main"}).find("div",attrs={'class':"field-items"}).text
    bref=''.join(bref.split())
    #print(bref)
    #地址与电话
    location=""
    number=""
    mes=hostinfo.find('footer',attrs={'class':"poly-5"}).find("div",attrs={'class':"copyright-nj1937 text-right"}).text
    location=re.search(re.compile(r'地址：[\u4e00-\u9fa5].+号'),str(mes)).group()
    number=re.search('电话：\d+-\d+',str(mes)).group()
    #print(location)
    #print(number)
    #陈列展览
    exhibition_hall=[]
    info_exh=get_all(url_2).find("div",attrs={'class':"content-main"})
    for i in info_exh.find("div",attrs={'class':"view-content"}).find_all("section"):
        a={}
        try:
            a["name"]=''.join(i.find("h2").text.split())
            a["img"]=url_2+i.find("img")['src']
            a["description"]=i.find("div",attrs={'class':"body margin-bottom-20"}).text
            a["description"]=''.join(a["description"].split())
            #print(a)
            exhibition_hall.append(a)
        except:
            continue
    #print(exhibition_hall)
    #馆藏精品
    info_projects=get_all(url_3).find("div",attrs={'class':"row",'id':"Data_con"})
    exhibition_projects=[]
    for i in info_projects.find_all("section",attrs={'class':"card"}):
        a={}
        try:
            url_next=url_3+i.find("a")['href']
            info_next=get_all(url_next).find("section",attrs={'class':"content-with-social-wrapper"})
            a["name"]=''.join(info_next.find("h4").text.split())
            a["img"]=url_3+i.find("img")['src']
            a["description"]=info_next.find("p",{'class':"rtejustify rteindent2"}).text
            #print(a)
            exhibition_projects.append(a)
        except:
            continue
    #print(exhibition_projects)
    #教育活动
    info_edu=get_all(url_4).find("div",attrs={'class':"row"})
    exhibition_edu=[]
    for i in info_edu.find_all("section"):
        a={}
        try:
            url_next=url_4+i.find("a")['href']
            info_next=get_all(url_next).find("div",{'class':"content-with-social-content"})
            a["time"]=get_all(url_next).find("section").find("div",{'class':"date"}).text
            a["time"]=''.join(a["time"].split())
            a["name"]=''.join(info_next.find("h4").text.split())
            a["img"]=url_4+"202003/"+info_next.find("img")['src']
            a["description"]=info_next.find("div",{'class':"field-item even"}).text
            a["description"]=''.join(a["description"].split())
            #print(a)
            exhibition_edu.append(a)
        except:
            continue
    #print(exhibition_edu)
    info_main={}
    info_main["bref"]=bref
    info_main["main_image_url"]=main_img_url
    info_main["opentime"]=opentime
    info_main["name"]=name
    info_main["location"]=location
    info_main["number"]=number
    info_all={}
    info_all["1"]=info_main
    info_all["2"]=exhibition_hall
    info_all["3"]=exhibition_projects
    info_all["4"]=exhibition_edu

    #print(info_all)
    return(info_all)
#get_qinhuarijunnanjingdatushayunantongbaojilianguan()
def get_nantong_museum():
    url="http://www.ntmuseum.com"
    url_1="http://www.ntmuseum.com/guide/intro/"
    url_2="http://www.ntmuseum.com/colunm3/col3/"
    url_3="http://www.ntmuseum.com/colunm2/col1/"
    url_4="http://www.ntmuseum.com/colunm4/col2/col4/"
    name="南通博物苑"
    main_img_url="https://pic.baike.soso.com/ugc/baikepic2/24073/20160922011238-693715772.jpg/300"
    hostinfo=get_all(url_1)
    #简介
    opentime=""
    for i in get_all("http://www.ntmuseum.com").find("div",{'class':"intro_word"}).find_all("p"):
        opentime=i.text
    bref=[]
    bref=hostinfo.find("li",{'class':"list_all"}).text
    bref=''.join(bref.split())
    #print(bref)
    #地址与电话
    location=""
    number=""
    mes=hostinfo.find("div",{'class':"l"})
    location=re.search(re.compile(r'地址：[\u4e00-\u9fa5].+号'),str(mes)).group()
    number=re.search('电话：\d.+\d',str(mes)).group()
    #print(location)
    #print(number)
    #陈列展览
    exhibition_hall=[]
    info_exh=get_all(url_2).find("div",attrs={'class':"pic_list"})
    for i in info_exh.find_all("li",{'class':"pic"}):
        a={}
        url_next=i.find("a")['href']
        info_next=get_all(url_next).find("div",{'class':"list_cont"})
        a["name"]=info_next.find("li",{'class':"list_title"}).text
        a["name"]=''.join(a["name"].split())
        try:
            a["img"]=info_next.find("img")['src']
        except:
            a["img"]=""
        a["description"]=info_next.find("li",{'class':"list_all"}).text
        a["description"]=''.join(a["description"].split())
        #print(a)
        exhibition_hall.append(a)
    #print(exhibition_hall)
    #馆藏精品
    info_projects=get_all(url_3).find("div",attrs={'class':"pic_list"})
    exhibition_projects=[]
    for i in info_projects.find_all("li",attrs={'class':"pic"}):
        a={}
        url_next=i.find("a")['href']
        info_next=get_all(url_next).find("div",{'class':"list_cont"})
        a["name"]=info_next.find("li",{'class':"list_title"}).text
        a["name"]=''.join(a["name"].split())
        a["img"]=url+info_next.find("img")['src']
        a["description"]=info_next.find("li",{'class':"list_all"}).text
        a["description"]=''.join(a["description"].split())
        #print(a)
        exhibition_projects.append(a)
    #print(exhibition_projects)
    #教育活动
    info_edu=get_all(url_4).find("div",attrs={'class':"article_list gallery_list1"})
    exhibition_edu=[]
    flag=0
    for i in info_edu.find_all("li"):
        a={}
        if(flag<4):
            url_next=i.find("a")['href']
            info_next=get_all(url_next).find("div",{'class':"list_cont"})
            a["name"]=info_next.find("li",{'class':"list_title"}).text
            a["name"]=''.join(a["name"].split())
            a["time"]=info_next.find("li",{'class':"list_infor"}).text
            a["time"]=''.join(a["time"].split())
            a["img"]=url+info_next.find("img")['src']
            a["description"]=info_next.find("li",{'class':"list_all"}).text
            a["description"]=''.join(a["description"].split())
            flag=flag+1
            #print(a)
            exhibition_edu.append(a)
        else:
            break
    #print(exhibition_edu)
    info_main={}
    info_main["bref"]=bref
    info_main["main_image_url"]=main_img_url
    info_main["opentime"]=opentime
    info_main["name"]=name
    info_main["location"]=location
    info_main["number"]=number
    info_all={}
    info_all["1"]=info_main
    info_all["2"]=exhibition_hall
    info_all["3"]=exhibition_projects
    info_all["4"]=exhibition_edu

    #print(info_all)
    return(info_all)
#get_nantong_museum()
def get_Suzhou_Museum():
    url="http://www.szmuseum.com"
    url_1="http://www.szmuseum.com/News/Index/GZZC"
    url_2="http://www.szmuseum.com/Exhibition/Index"
    url_3="http://www.szmuseum.com/Collection/Index"
    url_4="http://www.szmuseum.com/Activity/Index/jyhd?type=0"
    name="苏州博物馆"
    url_s="https://baike.sogou.com/v154138.htm?fromTitle=苏州博物馆"
    main_img_url=get_all(url_s).find("a",{'class':"ed_image_link"}).find("img")['src']
    hostinfo=get_all(url_1)
    #简介
    ot=get_all("http://www.szmuseum.com/#page4").find("div",{'class':"section4-bg"}).text
    opentime=''.join(ot.split())
    bref=[]
    bref=hostinfo.find("div",{'class':"divContent"}).text
    bref=''.join(bref.split())
    #print(bref)
    #地址与电话
    location=""
    number=""
    mes=hostinfo.find("div",{'class':"bottomcent"})
    location=re.search(re.compile(r'苏州[\u4e00-\u9fa5].+号'),str(mes)).group()
    number=re.search('\d+-\d+',str(mes)).group()
    #print(location)
    #print(number)
    #陈列展览
    exhibition_hall=[]
    info_exh=get_all(url_2).find("div",attrs={'class':"exjblb"})
    for i in info_exh.find_all("li"):
         a={}
         a["name"]=i.find("h1").text
         a["img"]=i.find("img")['src']
         a["description"]=i.find("p").text
         a["description"]=''.join(a["description"].split())
         #print(a)
         exhibition_hall.append(a)
    #print(exhibition_hall)
    #馆藏精品
    info_projects=get_all(url_3).find("div",attrs={'class':"colwrap"})
    exhibition_projects=[]
    url_begin=url+info_projects.find("a")['href']
    info_pro=get_all(url_begin)
    for i in info_pro.find_all("div",{'class':"collectdetailbg"}):
        a={}
        a["name"]=i.find("h1").text
        a["name"]=''.join(a["name"].split())
        a["img"]=i.find("img")['src']
        a["description"]=i.find("div",{'class':"divContent"}).text
        a["description"]=''.join(a["description"].split())
        #print(a)
        exhibition_projects.append(a)
    #print(exhibition_projects)
    #教育活动
    info_edu=get_all(url_4).find("div",attrs={'class':"contright temmin"})
    exhibition_edu=[]
    for i in info_edu.find_all("li",{'class':"clearfix"}):
        a={}
        url_next=url+i.find("a")['href']
        info_next=get_all(url_next).find("div",{'class':"actdetaildiv_p"})
        a["name"]=i.find("a")['title']
        a["time"]=i.find("div",{'class':"actp"}).text
        a["time"]=''.join(a["time"].split())
        a["img"]=i.find("img")['src']
        a["description"]=info_next.text
        a["description"]=''.join(a["description"].split())
        #print(a)
        exhibition_edu.append(a)
    #print(exhibition_edu)
    info_main={}
    info_main["bref"]=bref
    info_main["main_image_url"]=main_img_url
    info_main["opentime"]=opentime
    info_main["name"]=name
    info_main["location"]=location
    info_main["number"]=number
    info_all={}
    info_all["1"]=info_main
    info_all["2"]=exhibition_hall
    info_all["3"]=exhibition_projects
    info_all["4"]=exhibition_edu

    #print(info_all)
    return(info_all)
#get_Suzhou_Museum()
def get_Yangzhou_Museum():
    url="https://www.yzmuseum.com/"
    url_1="https://www.yzmuseum.com/website/aboutyzm/welcome.php"
    url_2="https://www.yzmuseum.com/website/exhibition/basic.php?id=23"
    url_3="https://www.yzmuseum.com/website/treasure/list.php"
    url_4="https://www.yzmuseum.com/website/research/discus.php"
    name="扬州博物馆"
    url_s="https://baike.sogou.com/v163156.htm?fromTitle=扬州博物馆"
    main_img_url=get_all(url_s).find("a",{'class':"ed_image_link"}).find("img")['src']
    hostinfo=get_all_new(url_1)
    #简介
    ot=get_all_new("https://www.yzmuseum.com/website/pages/index.php?forcelang=chinese").find("div",{'id':"open_time"}).text
    opentime=''.join(ot.split())
    bref=[]
    bref=hostinfo.find("div",{'id':"content_body"}).text
    bref=''.join(bref.split())
    #print(bref)
    #地址与电话
    location=""
    number=""
    mes=hostinfo.find("div",{'id':"foot_info"})
    location=re.search(re.compile(r'地址：[\u4e00-\u9fa5].+号'),str(mes)).group()
    number=re.search(re.compile(r'电话：.+\d+-\d+'),str(mes)).group()
    #print(location)
    #print(number)
    #陈列展览
    exhibition_hall=[]
    info_exh=get_all_new(url_2).find("div",attrs={'id':"page_content"})
    for i in info_exh.find("div",{'id':"content_head"}).find_all("div"):
        a={}
        a["name"]=i.find("a").text
        try:
            url_next=url+i.find("a")['href']
        except:
            url_next=url_2
        info_next=get_all_new(url_next).find("div",{'id':"content_body"})
        try:
            x=url+info_next.find("div",{'class':"treasure_list"}).find("a")['href']
            a["img"]=url+get_all_new(x).find("div",{'id':"content_body"}).find("img")['src']
        except:
            a["img"]=""
        a["description"]=info_next.find("div",{'class':"content_text"}).text
        a["description"]=''.join(a["description"].split())
        #print(a)
        exhibition_hall.append(a)
    #print(exhibition_hall)
    #馆藏精品
    info_projects=get_all_new(url_3).find("div",attrs={'id':"content_body"})
    exhibition_projects=[]
    for i in info_projects.find_all("div",{'class':"treasure_item"}):
        a={}
        url_next=url+i.find("a")['href']
        info_next=get_all_new(url_next).find("div",{'id':"content_body"})
        a["name"]=info_next.find("div",{'class':"tresure_detail_head"}).text
        a["img"]=url+info_next.find("img")['src']
        a["description"]=info_next.find("div",{'id':"content_text"}).text
        a["description"]=''.join(a["description"].split())
        #print(a)
        exhibition_projects.append(a)
    #print(exhibition_projects)
    #教育活动
    info_edu=get_all_new(url_4).find("ul",attrs={'class':"content_list"})
    exhibition_edu=[]
    #print(info_edu)
    for i in info_edu.find_all("a"):
        a={}
        url_next=url+i['href']
        info_next=get_all_new(url_next).find("div",{'id':"content_body"})
        a["name"]=info_next.find("h3").text
        a["time"]=i.find("span").text
        try:
            a["img"]=info_next.find("img")['src']
        except:
            a["img"]=""
        a["description"]=info_next.text
        a["description"]=''.join(a["description"].split())
        #print(a)
        exhibition_edu.append(a)
    #print(exhibition_edu
    info_main={}
    info_main["bref"]=bref
    info_main["main_image_url"]=main_img_url
    info_main["opentime"]=opentime
    info_main["name"]=name
    info_main["location"]=location
    info_main["number"]=number
    info_all={}
    info_all["1"]=info_main
    info_all["2"]=exhibition_hall
    info_all["3"]=exhibition_projects
    info_all["4"]=exhibition_edu

    #print(info_all)
    return(info_all)
#get_Yangzhou_Museum()
def get_Changzhou_Museum():
    url="http://www.czmuseum.com/"
    url_1="http://www.czmuseum.com/default.php?mod=article&do=detail&tid=1"
    url_2="http://www.czmuseum.com/default.php?mod=article&fid=13"
    url_3="http://www.czmuseum.com/default.php?mod=c&s=ss3e2cb0e&title=金银器"
    url_4="http://www.czmuseum.com/default.php?mod=article&fid=137"
    name="常州博物馆"
    url_s="https://baike.sogou.com/v163549.htm?fromTitle=常州博物馆"
    main_img_url=get_all(url_s).find("a",{'class':"ed_image_link"}).find("img")['src']
    hostinfo=get_all(url_1)
    #简介
    ot=get_all("http://www.czmuseum.com").find("td",{'class':"link_1"}).find("p").text
    opentime=''.join(ot.split())
    bref=[]
    bref=hostinfo.find("tr",{'class':"mod_box02"}).text
    bref=''.join(bref.split())
    #print(bref)
    #地址与电话
    location=""
    number=""
    mes=get_all(url).find("div",{'id':"ohid_s86505770"}).find("td",{'class':"link_1"})
    location=re.search(re.compile(r'地址：[\u4e00-\u9fa5].+号'),str(mes)).group()
    number=re.search('咨询：\d+.+\d+',str(mes)).group()
    #print(location)
    #print(number)
    #陈列展览
    exhibition_hall=[]
    info_exh=get_all_new(url_2).find("div",attrs={'id':"s12131099_content"}).find("tr")
    for i in info_exh.find_all("td"):
        a={}
        try:
            url_next=url+i.find("tbody").find("tbody").find("a")['href']
            info_next=get_all(url_next).find("div",{'id':"s71343348_c"})
            a["name"]=info_next.find("tr").text
            a["img"]=url+info_next.find("img")['src']
            a["description"]=info_next.find("tr",{'class':"mod_box02"}).text
            a["description"]=''.join(a["description"].split())
            #print(a)
            exhibition_hall.append(a)
        except:
            continue
    #print(exhibition_hall)
    #馆藏精品
    info_projects=get_all(url_3).find("div",attrs={'id':"wen"})
    exhibition_projects=[]
    for i in info_projects.find_all("div"):
        a={}
        try:
            a["name"]=i.find("p").text
            a["name"]=''.join(a["name"].split())
            a["img"]=""
            a["description"]=i.find("div",{'class':"wen_cont_"}).text
            a["description"]=''.join(a["description"].split())
            exhibition_projects.append(a)
        except:
            continue
    flag=0
    for i in get_all(url_3).find("div",{'id':"slides"}).find_all("div"): 
        exhibition_projects[flag]['img']=url+i.find("img")['src']
        flag=flag+1
    #print(exhibition_projects)
    #教育活动
    info_edu=get_all(url_4).find("div",attrs={'id':"s12131099_content"})
    exhibition_edu=[]
    for i in info_edu.find_all("td"):
        a={}
        try:
            url_next=url+i.find("tr").find("tr").find("td").find("a",{'target':"_self"})['href']
            info_next=get_all(url_next).find("div",{'id':"s71343348_c"})
            a["name"]=info_next.find("td",{'class':"mod_font08 mod_bold mod_align link_17"}).text
            a["name"]=''.join(a["name"].split())
            x=info_next.find("td",{'style':"HEIGHT: 25px; FONT-FAMILY: 微软雅黑; VERTICAL-ALIGN: middle; COLOR: #999999; PADDING-BOTTOM: 25px; TEXT-ALIGN: center; PADDING-TOP: 10px"}).text
            a["time"]=re.search(re.compile(r'\d+-\d+-\d+'),str(x)).group()
            a["time"]=''.join(a["time"].split())
            a["img"]=url+info_next.find("img")['src']
            a["description"]=info_next.find("tr",{'class':"mod_box02"}).text
            a["description"]=''.join(a["description"].split())
            #print(a)
            exhibition_edu.append(a)
        except:
            continue
    #print(exhibition_edu)
    info_main={}
    info_main["bref"]=bref
    info_main["main_image_url"]=main_img_url
    info_main["opentime"]=opentime
    info_main["name"]=name
    info_main["location"]=location
    info_main["number"]=number
    info_all={}
    info_all["1"]=info_main
    info_all["2"]=exhibition_hall
    info_all["3"]=exhibition_projects
    info_all["4"]=exhibition_edu

    #print(info_all)
    return(info_all)
#get_Changzhou_Museum()
def get_Nanjingshibowuzongguan():
    url="http://www.njmuseumadmin.com"
    url_1="http://www.njmuseumadmin.com/Stadium/index"
    url_2="http://www.njmuseumadmin.com/Exhibition/index/id/40"
    url_3="http://www.njmuseumadmin.com/Antique/index"
    url_4="http://www.njmuseumadmin.com/Activity/indexTheme/pid/30"
    name="南京市博物总馆"
    url_s="https://baike.sogou.com/v139421052.htm?fromTitle=南京市博物总馆"
    main_img_url=get_all(url_s).find("a",{'class':"ed_image_link"}).find("img")['src']
    hostinfo=get_all(url_1)
    #简介
    ot=get_all("http://www.njmuseumadmin.com/Stadium/index").find("div",{'class':"rright_con_dc_right"}).find("p").text
    opentime=''.join(ot.split())
    bref=[]
    bref=hostinfo.find("div",{'class':"rright_con_dc_left"}).text
    bref=''.join(bref.split())
    #print(bref)
    #地址与电话
    location=""
    number=""
    mes=hostinfo.find("div",{'class':"rright_con_dc_right"})
    location=re.search(re.compile(r'地址：[\u4e00-\u9fa5].+号'),str(mes)).group()
    number=re.search('电话：\d+-\d+',str(mes)).group()
    #print(location)
    #print(number)
    #陈列展览
    exhibition_hall=[]
    info_exh=get_all(url_2).find("div",attrs={'class':"Ex_right_con"})
    for i in info_exh.find_all("div"):
        a={}
        try:
            url_next=url+i.find("a")['href']
            info_next=get_all(url_next).find("div",{'class':"rightcon"})
            a["name"]=info_next.find("span").text
            a["img"]=url+info_next.find("img")['src']
            a["description"]=info_next.find("div",{'class':"Ex_content_bottom"}).text
            a["description"]=''.join(a["description"].split())
            #print(a)
            exhibition_hall.append(a)
        except:
            continue
    #print(exhibition_hall)
    #馆藏精品
    info_projects=get_all(url_3).find("li",attrs={'id':"Big_Slide_0"})
    exhibition_projects=[]
    for i in info_projects.find_all("div"):
        a={}
        url_next=url+i.find("a")['href']
        info_next=get_all(url_next).find("div",{'class':"basicxx_banner"})
        a["name"]=info_next.find("span").text
        a["img"]=url+info_next.find("img")['src']
        a["description"]=info_next.find("div",{'class':"gundongtiao"}).text
        a["description"]=''.join(a["description"].split())
        #print(a)
        exhibition_projects.append(a)
    #print(exhibition_projects)
    #教育活动
    info_edu=get_all(url_4).find("div",attrs={'class':"edu_subdown_ietm"})
    exhibition_edu=[]
    for i in info_edu.find_all("div",{'class':"edu_sublist"}):
        a={}
        try:
            url_next=url+i.find("a")['href']
            info_next=get_all(url_next).find("div",{'class':"rightcon"})
            a["name"]=info_next.find("strong").text
            a["time"]=info_next.find("span").text
            a["img"]=url+info_next.find("img")['src']
            a["description"]=info_next.find("div",{'class':"news_info_con"}).text
            a["description"]=''.join(a["description"].split())
            #print(a)
            exhibition_edu.append(a)
        except:
            continue
    #print(exhibition_edu)
    info_main={}
    info_main["bref"]=bref
    info_main["main_image_url"]=main_img_url
    info_main["opentime"]=opentime
    info_main["name"]=name
    info_main["location"]=location
    info_main["number"]=number
    info_all={}
    info_all["1"]=info_main
    info_all["2"]=exhibition_hall
    info_all["3"]=exhibition_projects
    info_all["4"]=exhibition_edu

    #print(info_all)
    return(info_all)
#get_Nanjingshibowuzongguan()
def get_Zhejiang_Provincial_Museum():   #官网不稳定
    url="http://www.zhejiangmuseum.com"
    url_1="http://www.zhejiangmuseum.com/zjbwg/ZPMbrief/about.html"
    url_2="http://www.zhejiangmuseum.com/zjbwg/exhibition/exhcurrent.html"
    url_3="http://www.zhejiangmuseum.com/zjbwg/collection/treasure.html"
    url_4="http://www.zhejiangmuseum.com/zjbwg/education.html"
    name="浙江省博物馆"
    url_s="https://baike.sogou.com/v9906.htm?fromTitle=浙江省博物馆"
    main_img_url=get_all(url_s).find("a",{'class':"ed_image_link"}).find("img")['src']
    hostinfo=get_all(url_1)
    #简介
    ot=get_all("http://www.zhejiangmuseum.com/zjbwg/index.html").find("div",{'class':"guide"}).find("p").text
    opentime=''.join(ot.split())
    bref=[]
    bref=hostinfo.find("div",{'class':"about"}).text
    bref=''.join(bref.split())
    #print(bref)
    #地址与电话
    location=""
    number=""
    mes=get_all("http://www.zhejiangmuseum.com/zjbwg/service/guide.html").find("div",{'class':"guide_jj"}).text
    location=get_all("https://baike.so.com/doc/5375992-5612104.html").find("p",{'class':"cardlist-value js-ditu-replace"})['title']
    number=re.search('预约电话：   \d+.+\d+[\u4e00-\u9fa5].+区）',str(mes)).group()
    #print(location)
    #print(number)
    #陈列展览
    exhibition_hall=[]
    info_exh=get_all(url_2).find("ul",attrs={'class':"zanlan_list"})
    for i in info_exh.find_all("li"):
        a={}
        url_next=url+"/zjbwg/exhibition/"+i.find("a")['href']
        info_next=get_all(url_next).find("div",attrs={'class':"zanlan_detail"})
        a["name"]=info_next.find("h4").text
        a["name"]=''.join(a["name"].split())
        try:
            a["img"]=url+info_next.find("div",{'class':"zanlan_zs"}).find("img")['src']
        except:
            continue
        a["description"]=info_next.find("div",{'class':"zanlan_zs"}).text
        a["description"]=''.join(a["description"].split())
        #print(a)
        exhibition_hall.append(a)
    #print(exhibition_hall)
    #馆藏精品
    info_projects=get_all(url_3).find("ul",attrs={'class':"treasure"})
    exhibition_projects=[]
    for i in info_projects.find_all("li"):
        a={}
        url_next="http://www.zhejiangmuseum.com/zjbwg/collection/"+i.find("a")['href']
        info_next=get_all(url_next).find("div",attrs={'class':"collect_info"})
        a["name"]=info_next.find("h3").text
        a["img"]=url+get_all(url_next).find("div",attrs={'class':"collect_image_big"}).find("img")['src']
        a["description"]=get_all(url_next).find("div",{'class':"jianjie"}).text
        a["description"]=''.join(a["description"].split())
        #print(a)
        exhibition_projects.append(a)
    #print(exhibition_projects)
    #教育活动
    info_edu=get_all(url_4).find("ul",attrs={'class':"newslist topbder m_t_20 align_r"})
    exhibition_edu=[]
    for i in info_edu.find_all("li"):
        a={}
        atext=[]
        try:
            url_next=url+i.find("a")['href']
            info_next=get_all(url_next).find("div",attrs={'class':"zongjie"})
            a["name"]=i.find("a").text
            a["time"]=re.search(re.compile(r'\d+-\d+-\d+'),i.text).group()
            a["img"]=url+info_next.find("p",{'style':"line-height: 1.75em; text-align: center; text-indent: 0em;"}).find("img")['src']
            for j in info_next.find_all("p"):
                atext.append(j.text)
            a["description"]=''.join(str(atext).split())
            #print(a)
            exhibition_edu.append(a)
        except:
            continue
    #print(exhibition_edu)
    info_main={}
    info_main["bref"]=bref
    info_main["main_image_url"]=main_img_url
    info_main["opentime"]=opentime
    info_main["name"]=name
    info_main["location"]=location
    info_main["number"]=number
    info_all={}
    info_all["1"]=info_main
    info_all["2"]=exhibition_hall
    info_all["3"]=exhibition_projects
    info_all["4"]=exhibition_edu

    #print(info_all)
    return(info_all)
#get_Zhejiang_Provincial_Museum()
def get_China_National_Silk_Museum():
    url="http://www.chinasilkmuseum.com"
    url_2="http://www.chinasilkmuseum.com/zz/list_17.aspx"
    url_3="http://www.chinasilkmuseum.com/zgxd/list_22.aspx"
    url_4="http://www.chinasilkmuseum.com/list_151.aspx"
    name="中国丝绸博物馆"
    main_img_url=""
    #简介
    opentime="9:00—17:00（周一：12:00—17:00，节、假日照常）"
    bref=[]
    bref=get_all("http://www.chinasilkmuseum.com/bwggk/index_3.aspx").find("div",{'class':"about_info"}).text
    bref=''.join(bref.split())
    #print(bref)
    #地址与电话
    location=""
    number=""
    mes=get_all("http://space.baozang.com/303").find("div",{'class':"jgxq_onenr"}).text
    location=re.search(re.compile(r'地址：[\u4e00-\u9fa5].+号'),str(mes)).group()
    number=re.search('电话：\d+-\d+',str(mes)).group()
    #print(location)
    #print(number)
    #陈列展览
    exhibition_hall=[]
    info_exh=get_all(url_2).find("div",attrs={'class':"show_info"})
    for i in info_exh.find_all("li"):
        a={}
        url_next=url+i.find("a")['href']
        info_next=get_all(url_next).find("div",{'class':"detail_body"})
        a["name"]=info_next.find("div",{'class':"detail_h"}).text
        a["name"]=''.join(a["name"].split())
        a["img"]=url+info_next.find("img")['src']
        a["description"]=info_next.find("div",{'class':"detail_text"}).text
        a["description"]=''.join(a["description"].split())
        #print(a)
        exhibition_hall.append(a)
    #print(exhibition_hall)
    #馆藏精品
    info_projects=get_all(url_3).find("div",attrs={'class':"collect_info"})
    exhibition_projects=[]
    for i in info_projects.find_all("li"):
        a={}
        url_next=url+i.find("a")['href']
        info_next=get_all(url_next).find("div",attrs={'class':"detail_body"})
        a["name"]=info_next.find("div",{'class':"detail_h"}).text
        a["name"]=''.join(a["name"].split())
        a["img"]=url+i.find("img")['src']
        a["description"]=info_next.find("div",{'class':"detail_text"}).text
        a["description"]=''.join(a["description"].split())
        #print(a)
        exhibition_projects.append(a)
    #print(exhibition_projects)
    #教育活动
    info_edu=get_all(url_4).find("div",attrs={'class':"public_item"})
    exhibition_edu=[]
    for i in info_edu.find_all("li"):
        a={}
        url_next=url+i.find("a")['href']
        info_next=get_all(url_next).find("div",attrs={'class':"detail_text"})
        a["name"]=i.find("p",{'class':"p"}).text
        a["time"]=i.find("span").text
        a["img"]=url+info_next.find("img")['src']
        a["description"]=info_next.text
        a["description"]=''.join(a["description"].split())
        #print(a)
        exhibition_edu.append(a)
    #print(exhibition_edu)
    info_main={}
    info_main["bref"]=bref
    info_main["main_image_url"]=main_img_url
    info_main["opentime"]=opentime
    info_main["name"]=name
    info_main["location"]=location
    info_main["number"]=number
    info_all={}
    info_all["1"]=info_main
    info_all["2"]=exhibition_hall
    info_all["3"]=exhibition_projects
    info_all["4"]=exhibition_edu

    #print(info_all)
    return(info_all)
#get_China_National_Silk_Museum()
def get_Ningbo_Museum():
    url="http://www.nbmuseum.cn"
    url_1="http://www.nbmuseum.cn/col/col41/index.html"
    url_2="http://www.nbmuseum.cn/col/col23/index.html"
    url_3="http://www.nbmuseum.cn/col/col581/index.html"
    url_4="http://www.nbmuseum.cn/col/col781/index.html"
    name="宁波博物馆"
    url_s="https://baike.sogou.com/v8187600.htm?fromTitle=%E5%AE%81%E6%B3%A2%E5%8D%9A%E7%89%A9%E9%A6%86"
    main_img_url=get_all(url_s).find("a",{'class':"ed_image_link"}).find("img")['src']
    hostinfo=get_all(url_1)
    #简介
    opentime="周二-周日免费开放；周一闭馆（节假日除外）；开馆时间：9:00-17:00（16:00后停止入馆）"
    bref=[]
    bref=hostinfo.find("div",{'id':"zoom"}).text
    bref=''.join(bref.split())
    #print(bref)
    #地址与电话
    location=""
    number=""
    mes=get_all_new("http://www.nbmuseum.cn/script/0/1607101834371691.js").text
    location=re.search(re.compile(r'地　　址：[\u4e00-\u9fa5].+号'),str(mes)).group()
    number=re.search(re.compile(r'电　　话：\d+-\d+'),str(mes)).group()
    #print(location)
    #print(number)
    #陈列展览
    exhibition_hall=[]
    info_exh=get_all(url_2).find("div",attrs={'class':"menu fl_rf"})
    for i in info_exh.find_all("a",{'target':"_BLANK"}):
        a={}
        url_next=url+i['href']
        info_next=get_all(url_next).find("div",{'class':"container"})
        a["name"]=i.text
        a["img"]=info_next.find("img")['src']
        a["description"]=info_next.text
        a["description"]=''.join(a["description"].split())
        #print(a)
        exhibition_hall.append(a)
    #print(exhibition_hall)
    #馆藏精品
    info_projects=get_all(url_3).find("map",attrs={'name':"Map"})
    exhibition_projects=[]
    for i in info_projects.find_all("area"):
        a={}
        url_next=url+i['href']
        info_next=get_all(url_next).find("div",{'class':"list"})
        a["name"]=info_next.find("div",{'class':"title"}).text
        a["name"]=''.join(a["name"].split())
        a["img"]=info_next.find("iframe")['src']
        a["description"]=info_next.find("div",{'id':"zoom"}).text
        a["description"]=''.join(a["description"].split())
        #print(a)
        exhibition_projects.append(a)
    #print(exhibition_projects)
    #教育活动
    info_edu=get_all(url_4).find("ul",attrs={'id':"sjhd_lb"})
    exhibition_edu=[]
    for i in info_edu.find_all("li"):
        a={}
        #url_next=url+i.find("a")['href']
        #info_next=get_all(url_next).find("div",attrs={'class':"detail_text"})
        a["name"]=i.find("a").text
        a["time"]=i.find("p",{'class':"sjhd_nr"}).text
        a["time"]=''.join(a["time"].split())
        a["img"]=""
        a["description"]=i.text
        a["description"]=''.join(a["description"].split())
        #print(a)
        exhibition_edu.append(a)
    #print(exhibition_edu)
    info_main={}
    info_main["bref"]=bref
    info_main["main_image_url"]=main_img_url
    info_main["opentime"]=opentime
    info_main["name"]=name
    info_main["location"]=location
    info_main["number"]=number
    info_all={}
    info_all["1"]=info_main
    info_all["2"]=exhibition_hall
    info_all["3"]=exhibition_projects
    info_all["4"]=exhibition_edu

    #print(info_all)
    return(info_all)
#get_Ningbo_Museum()
def get_Hangzhou_Museum():
    url="http://www.hzmuseum.com/"
    url_1="http://www.hzmuseum.com/about.aspx"
    url_2="http://www.hzmuseum.com/exhibition.aspx"
    url_3="http://www.hzmuseum.com/collection.aspx"
    url_4="http://www.hzmuseum.com/news.aspx"
    name="杭州博物馆"
    url_s="https://baike.sogou.com/v7666157.htm?fromTitle=%E6%9D%AD%E5%B7%9E%E5%8D%9A%E7%89%A9%E9%A6%86"
    main_img_url=get_all(url_s).find("a",{'class':"ed_image_link"}).find("img")['src']
    hostinfo=get_all(url_1)
    #简介
    opentime="9:00-16:30，周一闭馆"
    bref=[]
    bref=hostinfo.find("div",{'id':"aboutmsg"}).text
    bref=''.join(bref.split())
    #print(bref)
    #地址与电话
    location=""
    number=""
    mes=hostinfo.find("div",{'class':"mainfoot"}).text
    location=re.search(re.compile(r'地址：[\u4e00-\u9fa5].+18号'),str(mes)).group()
    number=re.search(re.compile(r'电话：\d+-\d+'),str(mes)).group()
    #print(location)
    #print(number)
    #陈列展览
    exhibition_hall=[]
    info_exh=get_all(url_2).find("div",attrs={'class':"ul_exh"})
    for i in info_exh.find_all("li"):
        a={}
        try:
            url_next=url+i.find("a")['href']
            info_next=get_all(url_next).find("div",{'class':"txt"})
            a["name"]=info_next.find("div",{'class':"biaoti"}).text
            a["name"]=''.join(a["name"].split())
            a["img"]=url+info_next.find("img")['src']
            a["description"]=info_next.text
            a["description"]=''.join(a["description"].split())
            #print(a)
            exhibition_hall.append(a)
        except:
            continue
    #print(exhibition_hall)
    #馆藏精品
    info_projects=get_all(url_3).find("div",attrs={'class':"txt"})
    exhibition_projects=[]
    for i in info_projects.find_all("li"):
        a={}
        url_next=url+i.find("a")['href']
        info_next=get_all(url_next).find("div",{'class':"txt"})
        a["name"]=info_next.find("div",{'class':"biaoti"}).text
        a["name"]=''.join(a["name"].split())
        a["img"]=url+info_next.find("img")['src']
        a["description"]=info_next.text
        a["description"]=''.join(a["description"].split())
        #print(a)
        exhibition_projects.append(a)
    #print(exhibition_projects)
    #教育活动
    info_edu=get_all(url_4).find("div",attrs={'class':"txt"})
    exhibition_edu=[]
    for i in info_edu.find_all("li"):
        a={}
        url_next=url+i.find("a")['href']
        info_next=get_all(url_next).find("div",attrs={'class':"txt"})
        a["name"]=info_next.find("div",{'class':"biaoti"}).text
        a["name"]=''.join(a["name"].split())
        a["time"]=re.search(re.compile(r'\d+-\d+-\d+'),str(info_next.find("div",{'class':"time"}).text)).group()
        a["img"]=url+info_next.find("img")['src']
        a["description"]=info_next.text
        a["description"]=''.join(a["description"].split())
        #print(a)
        exhibition_edu.append(a)
    #print(exhibition_edu)
    info_main={}
    info_main["bref"]=bref
    info_main["main_image_url"]=main_img_url
    info_main["opentime"]=opentime
    info_main["name"]=name
    info_main["location"]=location
    info_main["number"]=number
    info_all={}
    info_all["1"]=info_main
    info_all["2"]=exhibition_hall
    info_all["3"]=exhibition_projects
    info_all["4"]=exhibition_edu

    #print(info_all)
    return(info_all)
#get_Hangzhou_Museum()
def get_Fujian_Museum():
    url="http://museum.fjsen.com"
    url_1="https://baike.so.com/doc/5354945-5590409.html"
    url_2="http://museum.fjsen.com/node_167181.htm"
    url_3="http://museum.fjsen.com/node_167182.htm"
    url_4="http://museum.fjsen.com/node_167189.htm"
    name="福建博物院"
    url_s="https://baike.sogou.com/v156405.htm?fromTitle=福建博物院"
    main_img_url=get_all(url_s).find("a",{'class':"ed_image_link"}).find("img")['src']
    hostinfo=get_all(url_1)
    #简介
    opentime="每周五至周日9：00－16：30（五一期间正常开放）"
    bref=[]
    bref=hostinfo.find("div",{'class':"card_content"}).text
    bref=''.join(bref.split())
    #print(bref)
    #地址与电话
    location=""
    number=""
    location=hostinfo.find("p",{'class':"cardlist-value js-ditu-replace"})['title']
    #print(location)
    #print(number)
    #陈列展览
    exhibition_hall=[]
    info_exh=get_all(url_2).find("div",attrs={'class':"cont-left"})
    for i in info_exh.find("ul",{'class':"list_page"}).find_all("li"):
        a={}
        url_next=i.find("a")['href']
        try:
            info_next=get_all(url_next).find("td",{'id':"new_message_id"})
            a["name"]=i.find("a").text
            a["img"]=info_next.find("img")['src']
            a["description"]=info_next.text
            a["description"]=''.join(a["description"].split())
            #print(a)
            exhibition_hall.append(a)
        except:
            continue
    #print(exhibition_hall)
    #馆藏精品
    info_projects=get_all(url_3).find("div",attrs={'class':"cont-left"})
    exhibition_projects=[]
    for i in info_projects.find("ul",{'class':"list_page"}).find_all("li"):
        a={}
        url_next=i.find("a")['href']
        info_next=get_all(url_next).find("td",{'id':"new_message_id"})
        a["name"]=i.find("a").text
        a["img"]=info_next.find("img")['src']
        a["description"]=info_next.text
        a["description"]=''.join(a["description"].split())
        #print(a)
        exhibition_projects.append(a)
    #print(exhibition_projects)
    #教育活动
    info_edu=get_all(url_4).find("div",attrs={'class':"cont-left"})
    exhibition_edu=[]
    for i in info_edu.find("ul",{'class':"list_page"}).find_all("li"):
        a={}
        try:
            url_next=i.find("a")['href']
            info_next=get_all(url_next).find("td",{'id':"new_message_id"})
            a["name"]=i.find("a").text
            a["time"]=i.find("span").text
            a["img"]=info_next.find("img")['src']
            a["description"]=info_next.text
            a["description"]=''.join(a["description"].split())
            #print(a)
            exhibition_edu.append(a)
        except:
            continue
    #print(exhibition_edu)
    info_main={}
    info_main["bref"]=bref
    info_main["main_image_url"]=main_img_url
    info_main["opentime"]=opentime
    info_main["name"]=name
    info_main["location"]=location
    info_main["number"]=number
    info_all={}
    info_all["1"]=info_main
    info_all["2"]=exhibition_hall
    info_all["3"]=exhibition_projects
    info_all["4"]=exhibition_edu

    #print(info_all)
    return(info_all)
#get_Fujian_Museum()
def get_Gutian_Conference_Memorial_Hall():
    url="http://www.gthyjng.com/"
    url_1="http://www.gthyjng.com/gthyjs/201911/t20191127_543850.htm"
    url_3="http://www.gthyjng.com/gcww/wwjs/tdgmsq/"
    url_4="http://www.gthyjng.com/shjy/jyhd/"
    name="古田会议纪念馆"
    url_s="https://baike.sogou.com/v7133179.htm?fromTitle=古田会议纪念馆"
    main_img_url=get_all(url_s).find("a",{'class':"ed_image_link"}).find("img")['src']
    hostinfo=get_all(url_1)
    #简介
    opentime="8:00－18:00（夏令时）、8:00－17:30（冬令时），全年对外开放，中午不休。特殊闭馆时间请关注官网通知。"
    bref=[]
    bref=hostinfo.find("div",{'class':"TRS_Editor"}).text
    bref=''.join(bref.split())
    #print(bref)
    #地址与电话
    location=""
    number=""
    mes=hostinfo.find("div",{'class':"b_p"}).text
    location=re.search(re.compile(r'地址：[\u4e00-\u9fa5].+号'),str(mes)).group()
    number=re.search(re.compile(r'电话：\d+-\d+'),str(mes)).group()
    #print(location)
    #print(number)
    #陈列展览   暂无展览
    exhibition_hall=[]
    a={}
    a["name"]=""
    a["img"]=""
    a["description"]=""
    #print(a)
    exhibition_hall.append(a)
    #print(exhibition_hall)
    #馆藏精品
    info_projects=get_all(url_3).find("div",attrs={'class':"news_r_img"})
    exhibition_projects=[]
    for i in info_projects.find_all("li"):
        a={}
        url_next=url_3+i.find("a")['href']
        info_next=get_all(url_next).find("div",{'class':"TRS_Editor"})
        a["name"]=get_all(url_next).find("h1").text
        a["img"]=url_3+i.find("img")['src']
        a["description"]=info_next.text
        a["description"]=''.join(a["description"].split())
        #print(a)
        exhibition_projects.append(a)
    #print(exhibition_projects)
    #教育活动
    info_edu=get_all(url_4).find("div",attrs={'class':"tit_ul"})
    exhibition_edu=[]
    for i in info_edu.find_all("li"):
        a={}
        try:
            url_next=i.find("a")['href']
            info_next=get_all(url_next).find("div",{'id':"img-content"})
            a["name"]=info_next.find("h2").text
            a["name"]=''.join(a["name"].split())
            a["time"]=re.search(re.compile(r'\d+-\d+-\d+'),str(i.find("h1").text)).group()
            a["img"]=info_next.find("section",{'data-autoskip':"1"}).find("img",{'data-type':"jpeg"})['data-src']
            a["description"]=info_next.find("section",{'data-autoskip':"1"}).text
            a["description"]=''.join(a["description"].split())
            #print(a)
            exhibition_edu.append(a)
        except:
            continue
    #print(exhibition_edu)
    info_main={}
    info_main["bref"]=bref
    info_main["main_image_url"]=main_img_url
    info_main["opentime"]=opentime
    info_main["name"]=name
    info_main["location"]=location
    info_main["number"]=number
    info_all={}
    info_all["1"]=info_main
    info_all["2"]=exhibition_hall
    info_all["3"]=exhibition_projects
    info_all["4"]=exhibition_edu

    #print(info_all)
    return(info_all)
#get_Gutian_Conference_Memorial_Hall()
def get_Overseas_Chinese_Museum():
    url="http://www.hqbwy.org.cn"
    url_1="http://www.hqbwy.org.cn/aboutus.html"
    url_2="http://www.hqbwy.org.cn/exhibition.html"
    url_3="http://www.hqbwy.org.cn/collection.html"
    url_4="http://www.hqbwy.org.cn/education.html"
    name="华侨博物院"
    url_s="https://baike.sogou.com/v7415918.htm?fromTitle=华侨博物院"
    main_img_url=get_all(url_s).find("a",{'class':"ed_image_link"}).find("img")['src']
    hostinfo=get_all(url_1)
    #简介
    ot=get_all("http://www.hqbwy.org.cn").find("div",{'class':"ind-time"}).find("div").text
    opentime=''.join(ot.split())
    bref=[]
    bref=hostinfo.find("div",{'class':"situ-banner-intro"}).find("div",{'class':"scroll-animate animated"}).text
    bref=''.join(bref.split())
    #print(bref)
    #地址与电话
    location=""
    number=""
    mes=hostinfo.find("div",{'class':"foot-intro"}).text
    location=re.search(re.compile(r'地址:[\u4e00-\u9fa5].+号'),str(mes)).group()
    number=re.search(re.compile(r'电话：\d+-\d+'),str(mes)).group()
    #print(location)
    #print(number)
    #陈列展览
    exhibition_hall=[]
    info_exh=get_all(url_2).find("div",attrs={'class':"show-main"})
    for i in info_exh.find("ul",{'class':"show-ul clear"}).find_all("li"):
        a={}
        url_next=i.find("a")['href']
        info_next=get_all(url_next).find("div",{'class':"peple-top clear"})
        a["name"]=info_next.find("div",{'class':"peple-intro"}).find("p",{'class':"title"}).text
        a["img"]=url+info_next.find("img")['src']
        a["description"]=info_next.find("span").text
        a["description"]=''.join(a["description"].split())
        #print(a)
        exhibition_hall.append(a)
    #print(exhibition_hall)
    #馆藏精品
    info_projects=get_all(url_3).find("div",attrs={'class':"collect-main"})
    exhibition_projects=[]
    for i in info_projects.find("ul").find_all("li"):
        a={}
        url_next=i.find("a")['href']
        info_next=get_all(url_next).find("div",{'class':"peple-detail clear"})
        a["name"]=info_next.find("p",{'class':"title"}).text
        a["img"]=url+i.find("img")['src']
        a["description"]=info_next.find("div",{'class':"peple-detail-intro"}).text
        a["description"]=''.join(a["description"].split())
        #print(a)
        exhibition_projects.append(a)
    #print(exhibition_projects)
    #教育活动
    info_edu=get_all(url_4).find("div",attrs={'class':"news-main"})
    exhibition_edu=[]
    for i in info_edu.find("ul").find_all("li"):
        a={}
        try:
            url_next=i.find("a")['href']
            info_next=get_all(url_next).find("div",{'class':"detail-main"})
            a["name"]=info_next.find("p",{'class':"title"}).text
            a["time"]=info_next.find("p",{'class':"time"}).text
            a["img"]=info_next.find("img")['src']
            a["description"]=info_next.find("div",{'class':"detail-intro"}).text
            a["description"]=''.join(a["description"].split())
            #print(a)
            exhibition_edu.append(a)
        except:
            continue
    #print(exhibition_edu)
    info_main={}
    info_main["bref"]=bref
    info_main["main_image_url"]=main_img_url
    info_main["opentime"]=opentime
    info_main["name"]=name
    info_main["location"]=location
    info_main["number"]=number
    info_all={}
    info_all["1"]=info_main
    info_all["2"]=exhibition_hall
    info_all["3"]=exhibition_projects
    info_all["4"]=exhibition_edu

    #print(info_all)
    return(info_all)
#get_Overseas_Chinese_Museum()
def get_China_Museum_for_FujianTaiwan_Kinship():
    url="http://www.mtybwg.org.cn"
    url_1="http://www.mtybwg.org.cn/about/924.aspx"
    url_2="http://www.mtybwg.org.cn/zhanlan/105-1.aspx"
    url_3="http://www.mtybwg.org.cn/cangpin/164-1.aspx"
    url_4="http://www.mtybwg.org.cn/xuanjiao/117-1.aspx"
    name="中国闽台缘博物馆"
    url_s="https://baike.sogou.com/v154966.htm?fromTitle=中国闽台缘博物馆"
    main_img_url=get_all(url_s).find("a",{'class':"ed_image_link"}).find("img")['src']
    hostinfo=get_all(url_1)
    #简介
    opentime=""
    bref=[]
    bref=hostinfo.find("ul",{'class':"detailcon"}).text
    bref=''.join(bref.split())
    #print(bref)
    #地址与电话
    location=""
    number=""
    mes=get_all("http://www.mtybwg.org.cn/about/detail/249.aspx").find("ul",{'class':"detailcon"}).text
    location=re.search(re.compile(r'福建[\u4e00-\u9fa5].+号'),str(mes)).group()
    number=re.search(re.compile(r'\d+-\d+'),str(mes)).group()
    #print(location)
    #print(number)
    #陈列展览
    exhibition_hall=[]
    info_exh=get_all(url_2).find("div",attrs={'class':"rightcon"})
    for i in info_exh.find("ul",{'id':"container"}).find_all("li"):
        a={}
        try:
            url_next=url+i.find("a")['href']
            info_next=get_all(url_next).find("ul",{'class':"infolist"})
            a["name"]=info_next.find("span").text
            a["img"]=url+info_next.find("img")['src']
            a["description"]=info_next.find("ul",{'class':"detailcon"}).text
            a["description"]=''.join(a["description"].split())
            #print(a)
            exhibition_hall.append(a)
        except:
            continue
    #print(exhibition_hall)
    #馆藏精品
    info_projects=get_all(url_3).find("div",attrs={'class':"rightcon"})
    exhibition_projects=[]
    for i in info_projects.find("ul",{'id':"container"}).find_all("li"):
        a={}
        url_next=url+i.find("a")['href']
        info_next=get_all(url_next).find("ul",{'class':"infolist"})
        a["name"]=info_next.find("h1").text
        a["img"]=url+info_next.find("img")['src']
        a["description"]=info_next.find("ul",{'class':"con"}).text
        a["description"]=''.join(a["description"].split())
        #print(a)
        exhibition_projects.append(a)
    #print(exhibition_projects)
    #教育活动
    info_edu=get_all(url_4).find("ul",attrs={'class':"infolist"})
    exhibition_edu=[]
    for i in info_edu.find("ul").find_all("li"):
        a={}
        try:
            url_next=url+i.find("a")['href']
            info_next=get_all(url_next).find("div",{'id':"img-content"})
            a["name"]=i.find("a").text
            a["time"]=i.find("span").text
            a["img"]=info_next.find("img",{'crossorigin':"anonymous"})['data-src']
            a["description"]=info_next.find("div",{'class':"rich_media_content"}).text
            a["description"]=''.join(a["description"].split())
            #print(a)
            exhibition_edu.append(a)
        except:
            continue
    #print(exhibition_edu)
    info_main={}
    info_main["bref"]=bref
    info_main["main_image_url"]=main_img_url
    info_main["opentime"]=opentime
    info_main["name"]=name
    info_main["location"]=location
    info_main["number"]=number
    info_all={}
    info_all["1"]=info_main
    info_all["2"]=exhibition_hall
    info_all["3"]=exhibition_projects
    info_all["4"]=exhibition_edu

    #print(info_all)
    return info_all
#get_China_Museum_for_FujianTaiwan_Kinship()
def get_Central_Soviet_Area_History_Museum():
    url="http://www.crt.com.cn/hsmx/"
    urls="http://www.crt.com.cn"
    url_1="http://www.crt.com.cn/hsmx/mbjj.html"
    url_2="http://www.crt.com.cn/hsmx/hstd.html"
    url_3="http://www.crt.com.cn/mx/gcww.html"
    url_4="http://www.crt.com.cn/news2007/news/ZYSQMXLSBWGJIAOYUHUOD/ZYSQMXLSBWGJIAOYUHUOD.html"
    name="中央苏区（闽西）历史博物馆"
    url_s="https://baike.sogou.com/v167440924.htm?fromTitle=中央苏区（闽西）历史博物馆"
    main_img_url=get_all(url_s).find("a",{'class':"ed_image_link"}).find("img")['src']
    hostinfo=get_all_x(url_1)
    #简介
    opentime="星期二-星期日（上午8：15-11：45、下午14：45-17：15）每星期一闭馆"
    bref=[]
    bref=hostinfo.find("td",{'align':"left"}).text
    bref=''.join(bref.split())
    #print(bref)
    #地址与电话
    location=""
    number=""
    mes=hostinfo.find("html",{'xmlns':"http://www.w3.org/1999/xhtml"}).find("body").find("tr").text
    mes=''.join(mes.split())
    location=re.search(re.compile(r'地址：[\u4e00-\u9fa5].+号'),str(mes)).group()
    number=re.search(re.compile(r'电话：\d+－\d+'),str(mes)).group()
    #print(location)
    #print(number)
    #陈列展览
    exhibition_hall=[]
    info_exh=get_all_x(url_2).find("div",attrs={'class':"sdmenu"})
    for i in info_exh.find("div",{'class':"first-se"}).find_all("a"):
        a={}
        url_next=i['href']
        x=get_all_x(url_next).find("p",{'class':"jjbt"})
        info_next=x.parent.parent.parent
        a["name"]=x.text
        a["img"]=url+info_next.find("img")['src']
        a["description"]=info_next.find("td",{'align':"left"}).text
        a["description"]=''.join(a["description"].split())
        #print(a)
        exhibition_hall.append(a)
    #print(exhibition_hall)
    #馆藏精品   无法爬取
    info_projects=get_all_x(url_3)
    exhibition_projects=[]
    a={}
    a["name"]=""
    a["img"]=""
    a["description"]=""
    exhibition_projects.append(a)
    #print(exhibition_projects)
    #教育活动
    info_edu=get_all_x(url_4).find("td",attrs={'align':"left",'style':"padding-top:10px; padding-bottom:10px; line-height:25px;"})
    exhibition_edu=[]
    for i in info_edu.find_all("tr"):
        i=i.find("tr")
        a={}
        try:
            url_next=urls+i.find("a")['href']
            info_next=get_all_x(url_next).find("td",{'style':"font-size:15px; padding:0px 8px 0px 8px; color:#000000;"})
            a["name"]=i.find("a").text
            a["name"]=''.join(a["name"].split())
            a["time"]=i.find("td",{'width':"15%"}).text
            a["img"]=info_next.find("img")['src']
            a["description"]=info_next.text
            a["description"]=''.join(a["description"].split())    
            #print(a)
            exhibition_edu.append(a)
        except:
            continue
    #print(exhibition_edu)
    info_main={}
    info_main["bref"]=bref
    info_main["main_image_url"]=main_img_url
    info_main["opentime"]=opentime
    info_main["name"]=name
    info_main["location"]=location
    info_main["number"]=number
    info_all={}
    info_all["1"]=info_main
    info_all["2"]=exhibition_hall
    info_all["3"]=exhibition_projects
    info_all["4"]=exhibition_edu

    #print(info_all)
    return(info_all)
#get_Central_Soviet_Area_History_Museum()
if __name__ == '__main__':
     x_1=get_jilin_Proviencial_Museum()
     x_2=get_Museum_of_Heilongjiang_Province()
     x_3=get_Shanghai_Luxun_Museum()
     x_4=get_qinhuarijunnanjingdatushayunantongbaojilianguan()
     x_5=get_nantong_museum()
     x_6=get_Suzhou_Museum()
     x_7=get_Yangzhou_Museum()
     x_8=get_Changzhou_Museum()
     x_9=get_Nanjingshibowuzongguan()
     x_10=get_Zhejiang_Provincial_Museum()
     x_11=get_China_National_Silk_Museum()
     x_12=get_Ningbo_Museum()
     x_13=get_Hangzhou_Museum()
     x_14=get_Fujian_Museum()
     x_15=get_Gutian_Conference_Memorial_Hall()
     x_16=get_Overseas_Chinese_Museum()
     x_17=get_China_Museum_for_FujianTaiwan_Kinship()
     x_18=get_Central_Soviet_Area_History_Museum()  
     save_data(x_1)
     save_data(x_2)
     save_data(x_3)
     save_data(x_4)
     save_data(x_5)
     save_data(x_6)
     save_data(x_7)
     save_data(x_8)
     save_data(x_9)
     save_data(x_10)
     save_data(x_11)
     save_data(x_12)
     save_data(x_13)
     save_data(x_14)
     save_data(x_15)
     save_data(x_16)
     save_data(x_17)
     save_data(x_18)
