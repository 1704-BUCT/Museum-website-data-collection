import requests
import bs4
import re
from bs4 import BeautifulSoup
import MySQLdb
import pymysql
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
}
def get_all(url):
    re=requests.get(url,headers=headers)
    re.encoding='utf-8'
    soup = BeautifulSoup(re.text, 'html.parser')
    return soup
class ConnMysql(object):
    def __init__(self):
        # 连接数据库
        self.db = pymysql.connect(host='39.98.107.127',
                                  port=3306,
                                  database='museum',
                                  user='1704',
                                  password='CS1704',
                                  charset='utf8')
        self.cursor = self.db.cursor()
    def insert(self,dict1):
        # 将数据添加到数据库中的movie表中
        sql = "insert into museums(mid,name,imgurl,mobile,address,introduction,opentime) values(%d,%s,%s,%s,%s,%s,%s)"
        data = [dict1['mid'],dict1['name'],dict1['imgurl'],dict1['mobile'],dict1['address'],dict1['introduction'],dict1['opentime'],]
        self.cursor.execute(sql,data)
        self.db.commit() # 提交操作
def save_data(dict_data):
    # 存数据库
    database = ConnMysql()
    database.insert(dict_data)

def get_beijing_ScienceandTechnology_Museum():
    url_1="http://cstm.cdstm.cn/"
    url_2="http://cstm.cdstm.cn/e/action/ListInfo/?classid=171"
    url_3="http://cstm.cdstm.cn/e/action/ListInfo/?classid=184"
    url_4="http://cstm.cdstm.cn/e/action/ListInfo/?classid=263"
    hostinfo=get_all(url_1)
    name="中国科学技术馆"
    #简介
    bref=""
    for i in hostinfo.find_all(name='meta',attrs={'name':"Description"}):
        bref=i['content']
    bref=re.sub(' ','',bref)
    # print(bref)
    #地址
    location=""
    for i in str(hostinfo.find_all(name='p',attrs={'class':"footer-text-cont"})).split("<br/>"):
        if(re.search(re.compile(r'地址：'),i)):
            location=i
    location=location.split('\u3000')
    location=location[0]
    # print(location)
    #电话
    number=""
    for i in str(hostinfo.find_all(name='p',attrs={'class':"footer-text-cont"})).split("<br/>"):
        if(re.search(re.compile(r'投诉电话：'),i)):
            number=i
    # print(number)
    #展览的简介和图片
    exhibition_hall=[]
    info_exh=get_all(url_2)
    for i in info_exh.find_all(name='li',attrs={'class':"w5em"}):
        a={}
        a['name']=i.text
        a['url']=url_1+i.a['href']
        exhibition_hall.append(a)
    del(exhibition_hall[0])
    for i in exhibition_hall:
        if(i["name"]!="科学乐园"):
            info=get_all(i["url"])
            x=info.find(name='div',attrs={'class':"fenzhanqu-docc"})
            #展馆简介
            i["description"]=x.text
            x=info.find(name='img',attrs={'src':re.compile(r'^/d/file/')})
            #图片路径
            i["img"]=url_1+x['src']
            # print(i["img"])
        else:
            info=get_all(i["url"])
            x=info.find(name='div',attrs={'style':"padding:20px;padding-bottom:30px;text-indent:2em;padding-top: 0;margin-top: -60px;"})
            i["description"]=x.text
            # print(i["description"])
            x=info.find(name='div',attrs={'class':"kxly-maps"})
            x=str(x["style"]).split(";")
            for j in x:
                if(re.search(re.compile(r'url'),j)):
                    i["img"]=re.findall(re.compile(r'[(](.*?)[)]', re.S),j)[0]
            # print(i["img"])
    # print(exhibition_hall)
    #博物馆藏品
    info_projects=get_all(url_3)
    exhibition_projects=[]
    x=info_projects.find(name='ul',attrs={'class':"fen-zhanqu-zp-list"})
    for i in x.find_all_next(name="li"):
        a={}
        a["name"]=i.find(name="a",attrs={'class':"fen-zhanqu-zp-name"}).text
        a["img"]=url_1+i.find(name="img")["src"]
        url_next=url_1+i.find(name="a",attrs={'class':"fen-zhanqu-zp-pic"})["href"]
        t=get_all(url_next)
        xx=t.find(name="div",attrs={'class':"fen-info-cont"})
        a["description"]=xx.text
        exhibition_projects.append(a)
    # print(exhibition_projects)
    #教育活动
    info_edu=get_all(url_4).find(name='ul',attrs={'class':"hdyg-list"})
    exhibition_edu=[]
    for i in info_edu.find_all(name="li"):
        a={}
        temp=re.sub('\u3000','',i.text)
        a["time"]=re.findall(re.compile(r'\d{4}-\d{1,2}-\d{1,2}'),i.text)[0]
        a["name"]=temp.strip(a["time"])
        url_next=url_1+i.a["href"]
        move=get_all(url_next).find(name="div",attrs={'class':"fen-info-cont"})
        a["description"]=move.find(name="p").text
        a["img"]=url_1+move.find(name="img")["src"]
        exhibition_edu.append(a)
    #print(exhibition_edu)

def get_beijing_dizhi_Museum():
    name="中国地质博物馆"
    url="http://www.gmc.org.cn/"
    url_1="http://www.gmc.org.cn/contactus.html"
    url_2="http://www.gmc.org.cn/permanent_exhibition.html"
    url_3="http://www.gmc.org.cn/mineral.html"
    url_4="http://www.gmc.org.cn/knowledge.html"
    hostinfo=get_all(url_1)
    #地址和电话
    location=""
    number=""
    for i in hostinfo.find_all(name="div",attrs={"class":"t16"}):
        if(re.search(re.compile(r'地址：'),i.text)):
            location=i.text
        if(re.search(re.compile(r'电话：'),i.text)):
            number=i.text
    # print(location)
    # print(number)
    #展览的简介和图片
    exhibition_hall=[]
    info_exh=get_all(url_2)
    for i in info_exh.find_all(name="div",attrs={"class":"xx"}):
        url_next=url+i.a["href"]
        a={}
        x=get_all(url_next).find(name="div",attrs={'class':"con"})
        y=get_all(url_next).find(name="div",attrs={'class':"clitem"})
        a["name"]=x.find(name="div",attrs={'class':"t28"}).text
        a["description"]=x.find(name="div",attrs={'class':"p"}).text
        a["img"]=url+y.find(name="img")["src"]
        exhibition_hall.append(a)
    # print(exhibition_hall)
    #博物馆藏品
    info_projects=get_all(url_3)
    exhibition_projects=[]
    x=info_projects.find(name="div",attrs={'class':"clist clear"})
    for i in x.find_all_next(name="div",attrs={'class':"li"}):
        a={}
        if(re.search(re.compile(r'/detail'),str(i.a["href"]))):
            url_next=url+i.a["href"]
            temp=get_all(url_next).find(name="div",attrs={'class':"col1"})
            a["name"]=temp.find(name='div',attrs={'class':"t28"}).text
            a["description"]=""
            for j in temp.find_all(name='p'):
                a["description"]+=j.text
            a["img"]=url+temp.find(name="img")["src"]
            exhibition_projects.append(a)
    # print(exhibition_projects)
    #教育活动
    info_edu=get_all(url_4).find_all(name="a",attrs={'class':"clear"})
    exhibition_edu=[]
    flag=0
    for i in info_edu:
        a={}
        #就取4个好吧 因为第5个图片格式太诡异
        if(flag!=4):
            url_next=url+i["href"]
            temp=get_all(url_next)
            a["name"]=temp.find(name='div',attrs={'class':"h24"}).text
            a["time"]=temp.find(name='div',attrs={'class':"info"}).text
            mess=temp.find(name='div',attrs={'class':"article-cont"})
            a["img"]=url+mess.find(name="img")["src"]
            a["description"]=""
            for j in mess.find_all_next(name="p",attrs={'class':"p"}):
                a["description"]+=j.text
            exhibition_edu.append(a)
        flag+=1
    # print(exhibition_edu)

def get_beijing_Military_Museum():
    name="中国人民革命军事博物馆"
    url="http://www.jb.mil.cn/"
    url_1="http://www.jb.mil.cn/cgfw/cgzn/"
    url_2="http://www.jb.mil.cn/zlcl/jbcl/"
    url_3="http://www.jb.mil.cn/was/web/search?token=14.1499419140318.94&channelid=227090"
    url_4="http://www.jb.mil.cn/cyhd/jzhd/"
    hostinfo=get_all(url_1)

    #地址和电话
    location=""
    number=""
    for i in hostinfo.find_all(name="i"):
        if(re.search(re.compile(r'地址：'),i.text)):
            for j in re.split(" |\xa0",i.text):
                if(re.search(re.compile(r'地址：'),j)):
                    location=j
    ####
    for i in get_all(url_1).find_all(name="p"):
        if(re.search(re.compile(r'自助预约及咨询电话：'),i.text)):
            number=i.text
     #展览的简介和图片
    exhibition_hall=[]
    info_exh=get_all(url_2).find(name="div",attrs={"class":"basicList"})
    for i in info_exh.find_all(name="li"):
        a={}
        a["name"]=i.find(name="h3").text
        a["description"]=i.find(name="p").text
        a["img"]=url_2+i.find(name="img")["src"]
        exhibition_hall.append(a)
    # print(exhibition_hall)
    #博物馆藏品
    info_projects=get_all(url_3).find(name="div",attrs={"class":"raAppList"})
    exhibition_projects=[]
    for i in info_projects.find_all_next(name="li"):
        a={}
        a["name"]=i.find(name="span").text
        url_next=i.find(name="a")["href"]
        #为了图片的url要去掉最后一个/之后的字符
        new=url_next.split("/")[0:-1]
        url_new=""
        for k in new:
            url_new+=k+"/"

        a["description"]=""
        info_next=get_all(url_next).find(name="div",attrs={"class":"TRS_Editor"})
        a["img"]=url_new+info_next.find(name="img")["src"]
        for j in info_next.find_all(name="p"):
            a["description"]+=j.text
        exhibition_projects.append(a)
    # print(exhibition_projects)
    #教育活动
    info_edu=get_all(url_4).find(name="div",attrs={"class":"researchList oldActiveList"})
    exhibition_edu=[]
    for i in info_edu.find_all(name="li"):
        a={}
        a["name"]=i.find(name="h3").text
        a["time"]=i.find(name="span").text
        a["img"]=url_4+i.find(name="img")["src"]
        url_next=url_4+i.find(name="a")["href"]
        info_next=get_all(url_next).find(name="div",attrs={"class":"TRS_Editor"})
        a["description"]=""
        for j in info_next.find_all(name="p"):
            a["description"]+=j.text
        exhibition_edu.append(a)
    # print(exhibition_edu)
def get_beijing_LuXun_Museum():
    url="http://www.luxunmuseum.com.cn/"
    url_number="http://www.luxunmuseum.com.cn/canguanxuzhi/"
    url_1="http://www.luxunmuseum.com.cn/zhanlanhuigu/"
    url_2="http://www.luxunmuseum.com.cn/guancangjingpin/"
    url_3="http://www.luxunmuseum.com.cn/xinwenhuajiangtang/"
    name="北京鲁迅博物馆"
    hostinfo=get_all(url).find(name="div",attrs={"class":"daolan"})
    #地址和电话和开放时间
    location=""
    number=""
    opentime=""
    x=hostinfo.find(name="div",attrs={"class":"dl_l"})
    xx=0
    for i in x.find_all(name="p"):
        if(xx<=2):
            opentime+=i.text
        if(xx==3):
            location=i.text
        xx+=1
    y=get_all(url_number).find(name="div",attrs={"class":"content_nr"})
    for i in y.find_all(name="div"):
        if(re.search(re.compile(r'鲁博馆区：'),i.text)):
            t=i.text.split("，")
            number=t[1]
    # print(number)
    #展览的简介和图片
    exhibition_hall=[]
    info_exh=get_all(url_1).find(name="div",attrs={"class":"content_zhanl"})
    for i in info_exh.find_all(name="div",attrs={"class":"list_chenlie"}):
        a={}
        a["name"]=i.find(name="dt").a.text
        a["img"]=url+i.find(name="div",attrs={"class":"list_img"}).a.img["src"]
        url_next=url+i.find(name="dt").a["href"]
        info_next=get_all(url_next).find(name="div",attrs={"class":"content_nr"})
        a["description"]=re.sub('\r|\t|\xa0|\n','',info_next.text)
        exhibition_hall.append(a)
    # print(exhibition_hall)
    #博物馆藏品
    info_projects=get_all(url_2).find(name="div",attrs={"class":"content_shougao"})
    exhibition_projects=[]
    for i in info_projects.find_all_next(name="dl"):
        a={}
        a["img"]=url+i.find(name="dt").div.a.img["src"]
        url_next=url+i.find(name="dd").a["href"]
        info_next=get_all(url_next)
        x=info_next.find(name="div",attrs={"class":"content_nr"})
        a["name"]=info_next.find(name="div",attrs={"class":"content_title"}).text
        a["description"]=re.sub(' |\r|\t|\xa0|\n|\u3000','',x.text)
        exhibition_projects.append(a)
    # print(exhibition_projects)
    #教育活动
    info_edu=get_all(url_3).find(name="div",attrs={"class":"content_zjk"})
    exhibition_edu=[]
    for i in info_edu.find_all(name="dl"):
        a={}
        
        a["img"]=url+i.find(name="dt").a.img["src"]
        url_next=url+i.find(name="dt").a["href"]
        info_next=get_all(url_next)
        x=info_next.find(name="div",attrs={"class":"content_nr"})
        a["description"]=re.sub(' |\r|\t|\xa0|\n|\u3000','',x.text)
        a["name"]=info_next.find(name="div",attrs={"class":"content_title"}).text
        a["time"]=re.sub('\xa0|浏览数：','',info_next.find(name="div",attrs={"class":"content_cs"}).text)
        exhibition_edu.append(a)
    # print(exhibition_edu)
def get_beijing_Capital_Museum():
    url="http://www.capitalmuseum.org.cn/"
    url_1="http://www.capitalmuseum.org.cn/other/foot.htm"
    url_2="http://www.capitalmuseum.org.cn/zlxx/ztyscl.htm"
    url_3="http://www.capitalmuseum.org.cn/jpdc/qtq.htm"
    url_4="http://www.capitalmuseum.org.cn/zjsb/jyhdjs.htm"
    url_5="http://www.capitalmuseum.org.cn/zlxx/"
    url_6="http://www.capitalmuseum.org.cn/jpdc/"
    url_7="http://www.capitalmuseum.org.cn/zjsb/"
    name="首都博物馆"
    hostinfo=get_all(url_1).find(name="td",attrs={ "class":"bai"})
    #地址和电话和开放时间
    location=""
    number=""
    opentime=""
    x=hostinfo.text.split("|")
    for i in x:
        if(re.search(re.compile(r'预约电话：'),i)):
            number=i
        if(re.search(re.compile(r'馆址：'),i)):
            location=i
        if(re.search(re.compile(r'开放时间：'),i)):
            opentime=i
    # print(location+number+opentime)
    #展览的简介和图片
    exhibition_hall=[]
    info_exh=get_all(url_2).find(name="td",attrs={"style":"background-repeat:no-repeat","height":"571"})
    for i in info_exh.find_all(name="table",attrs={"width":"560"}):
        a={}
        a["name"]=i.find(name="td",attrs={"class":"btitle"}).text
        a["img"]=url_5+i.find(name="td",attrs={"width":"200","height":"145","valign":"top"}).img["src"]
        url_next=url_5+i.find(name="a",attrs={"class":"hh"})["href"]
        info_next=get_all(url_next).find(name="td",attrs={"height":"25","align":"left","class":"bai"})
        a["description"]=re.sub('\xa0','',info_next.text)
        exhibition_hall.append(a)
    # print(exhibition_hall)
    #博物馆藏品
    info_projects=get_all(url_3).find(name="table",attrs={"width":"500","border":"0","align":"center","cellpadding":"0","cellspacing":"0"})
    exhibition_projects=[]
    for i in info_projects.find_all_next(name="td",attrs={"width":"500","align":"center","valign":"top"}):
        a={}
        a["img"]=url_6+i.find(name="td",attrs={"height":"108","align":"center","valign":"top"}).a.img["src"]
        a["name"]=i.find(name="td",attrs={"height":"21","align":"center","valign":"top"}).a.text
        url_next=url_6+i.find(name="td",attrs={"height":"21","align":"center","valign":"top"}).a["href"]
        info_next=get_all(url_next).find(name="td",attrs={"height":"74","align":"left","valign":"top"})
        x=info_next.find_all(name="p")
        a["description"]=""
        for j in x:
            a["description"]+=re.sub(' |\r|\t|\xa0|\n|\u3000','',j.text)
        exhibition_projects.append(a)
    # print(exhibition_projects)
    #教育活动
    info_edu=get_all(url_4).find(name="table",attrs={"width":"564","border":"0","align":"center","cellpadding":"0","cellspacing":"0"})
    exhibition_edu=[]
    for i in info_edu.find_all(name="td",attrs={"width":"564"}):
        a={}
        a["name"]=i.find(name="td",attrs={"width":"380","align":"left","valign":"top"}).text
        a["img"]=url_7+i.find(name="img")["src"]
        url_next=url_7+i.find(name="td",attrs={"width":"40","align":"left"}).a["href"]
        info_next=get_all(url_next).find(name="td",attrs={"align":"left"})
        a["description"]=""
        for j in info_next.find_all(name="p"):
            if(re.search(re.compile(r'\b活动时间：'),j.text)):
                pos=j.text.index("活")
                end=j.text.rindex("0")
                a["time"]=j.text[pos:end+1]
            a["description"]+=re.sub('\xa0','',j.text)
        exhibition_edu.append(a)
        #print(exhibition_edu)

def get_beijing_Nature_Museun():#!!!!!
    url="http://www.bmnh.org.cn/"
    url_time="http://www.bmnh.org.cn/cgzx/cgxx/index.shtml"
    url_1="http://www.bmnh.org.cn/zljs/lszl/2019nlszl/list.shtml"
    url_2="http://www.bmnh.org.cn/gzxx/gzbb/11/list.shtml"
    url_3="http://www.bmnh.org.cn/jyhd/list.shtml"
    name="北京自然博物馆"
    ####这个问题和鲁迅博物馆一样
    hostinfo=get_all(url)
    #地址和电话和开放时间
    location=""
    number=""
    opentime=""
    x=hostinfo.find(name="div",attrs={"class":"foot_l2"})
    for i in x.find_all(name="p"):
        if(re.search(re.compile(r'通信地址：'),i.text)):
            pos1=i.text.index("通")
            end1=i.text.rindex("电")
            end2=i.text.rindex("传")
            location=i.text[pos1:end1]
            number=i.text[end1+1:end2]
    # print(location+number)
    x=get_all(url_time).find(name="div",attrs={"class":"single_block"})
    for i in x.find_all(name="p"):
        if(re.search(re.compile(r'开放时间：'),i.text)):
            opentime=i.text[2:]
    # print(opentime)
    #展览的简介和图片
    exhibition_hall=[]
    info_exh=get_all(url_1).find(name="div",attrs={"class":"content_singler singler_exh"})
    for i in info_exh.find_all(name="p"):
        a={}
        a["name"]=re.sub("\n",'',i.text)
        url_next=url+i.find(name="a")["href"]
        a["description"]=""
        info_next=get_all(url_next).find(name="div",attrs={"class":"single_block"})
        for j in info_next.find_all(name="p"):
            a["description"]+=re.sub('\r|\t|\xa0|\n','',j.text)
        a["img"]=url+info_next.find(name="img")["src"]
        exhibition_hall.append(a)
    # print(exhibition_hall)
     #博物馆藏品
    info_projects=get_all(url_2).find(name="div",attrs={"class":"content_shopr"})
    exhibition_projects=[]
    for i in info_projects.find_all_next(name="div",attrs={"class":"col-sm-4"}):
        a={}
        a["name"]=re.sub('\r|\t|\xa0|\n','',i.find(name="div",attrs={"class":"caption"}).text)
        a["description"]=""
        info_next=get_all(url_next).find(name="div",attrs={"class":"TRS_Editor"})
        a["img"]=url+i.find(name="img")["src"]
        exhibition_projects.append(a)
        # print(a)
    # print(exhibition_projects)
    #教育活动
    info_edu=get_all(url_3).find(name="div",attrs={"class":"edu_blockAR"})
    exhibition_edu=[]
    for i in info_edu.find_all(name="div",attrs={"class":"edu_blockAR_list"}):
        if(re.search(re.compile(r'/jyhd'),i.find(name="p",attrs={"class":"edu_blockA_small_text"}).a["href"])):
            a={} 
            a["img"]=url+i.find(name="div",attrs={"class":"edu_blockA_small_img"}).div.img["src"]
            a["name"]=i.find(name="p",attrs={"class":"edu_blockA_small_text"}).text
            a["time"]=i.find(name="span",attrs={"class":"edu_date"}).text
            url_next=url+i.find(name="p",attrs={"class":"edu_blockA_small_text"}).a["href"]
            info_next=get_all(url_next).find(name="div",attrs={"class":"single_block"})
            a["description"]=""
            for j in info_next.find_all(name="p"):
                a["description"]+=re.sub(' |\r|\t|\xa0|\n|\u3000','',j.text)
            exhibition_edu.append(a)
    # print(exhibition_edu)

#xx这个全是js异步加载的 搞不定
def get_beijing_KRZZ_Museum(): 
    url="http://www.1937china.com/kzjng/"
    url_1="http://www.1937china.com/kzjng/views/include/contact.html"
    url_2="http://www.1937china.com/kzslw/views/kzzl/zlzs_zlzx.html"
    name="中国人民抗日战争纪念馆"
    hostinfo=get_all(url_1)
    #地址和电话和开放时间
    location=""
    number=""
    opentime=""
    x=hostinfo.find(name="div",attrs={"class":"body-styles l-container--sm row-outside--md cf"})
    for i in x.find_all(name="p"):
        if(re.search(re.compile(r'本馆地址：'),i.text)):
            location=i.text
        if(re.search(re.compile(r'团体观众参观：'),i.text)):
            number=i.text
    # print(location+number)
    #展览的简介和图片
    exhibition_hall=[]
    info_exh=get_all(url_2).find(name="ul",attrs={"class":"commonlist"})
    for i in info_exh.find_all(name="li",attrs={"data-aos":"fade-up"}):
        print(i.text)
        # a={}
        # a["name"]=re.sub("\n",'',i.text)
        # url_next=url+i.find(name="a")["href"]
        # a["description"]=""
        # info_next=get_all(url_next).find(name="div",attrs={"class":"single_block"})
        # for j in info_next.find_all(name="p"):
        #     a["description"]+=re.sub('\r|\t|\xa0|\n','',j.text)
        # a["img"]=url+info_next.find(name="img")["src"]
        # exhibition_hall.append(a)
    # print(exhibition_hall)

#xx这个也是js写的搞不定
def get_beijing_Planet_Museum():
    url="http://www.bjp.org.cn/"
    url_1="http://www.bjp.org.cn/col/col156/index.html"
    url_2="http://www.bjp.org.cn/col/col27/index.html"
    url_3="http://www.bjp.org.cn/col/col28/index.html"
    name="北京天文馆"
    #教育活动
    info_edu=get_all(url_3).find(name="div",attrs={"class":"278"})
    exhibition_edu=[]
    print(info_edu)
    # for i in info_edu.find_all(name="record"):
    #     # url_next=url+i.find(name="a")["href"]
    #     print(i.text)
        # if(re.search(re.compile(r'/jyhd'),i.find(name="p",attrs={"class":"edu_blockA_small_text"}).a["href"])):
        #     a={} 
        #     a["img"]=url+i.find(name="div",attrs={"class":"edu_blockA_small_img"}).div.img["src"]
        #     a["name"]=i.find(name="p",attrs={"class":"edu_blockA_small_text"}).text
        #     a["time"]=i.find(name="span",attrs={"class":"edu_date"}).text
        #     url_next=url+i.find(name="p",attrs={"class":"edu_blockA_small_text"}).a["href"]
        #     info_next=get_all(url_next).find(name="div",attrs={"class":"single_block"})
        #     a["description"]=""
        #     for j in info_next.find_all(name="p"):
        #         a["description"]+=re.sub(' |\r|\t|\xa0|\n|\u3000','',j.text)
        #     exhibition_edu.append(a)
    # print(exhibition_edu)

def get_beijing_ZKDYR_Museum():
    url="http://www.zkd.cn/"
    url_1="http://www.zkd.cn/jbcl/index.jhtml"
    url_2="http://www.zkd.cn/jpzs/index.jhtml"
    url_3="http://www.zkd.cn/kpty/index.jhtml"
    url_time="http://www.zkd.cn/cgdl/index.jhtml"
    name="周口店猿人遗址博物馆"
    #地址和电话和开放时间
    location="地址：北京城西南房山区周口店龙骨山脚下"
    number="预约电话：010-69301278"
    opentime=re.sub("\r|\t|\xa0|\n",'',get_all(url_time).find(name="div",attrs={"class":"kfsj_text"}).text)
    # print(location+number+opentime)
    #展览的简介和图片
    exhibition_hall=[]
    info_exh=get_all(url_1).find(name="div",attrs={"class":"xszz_list"})
    for i in info_exh.find_all(name="li"):
        a={}
        a["name"]=re.sub("\n",'',i.find(name="div",attrs={"class":"ming2"}).text)
        a["description"]=re.sub("\r|\t|\xa0|\n",'',i.find(name="div",attrs={"class":"jieshao2"}).text)
        a["img"]=url+i.find(name="img")["src"]
        exhibition_hall.append(a)
    #   print(a)
    # print(exhibition_hall)
    #博物馆藏品
    info_projects=get_all(url_2).find(name="div",attrs={"style":"width:200px; height:560px; background-color:#FFFFFF; padding: 40px 20px;display:block;float:right; font-size:12px;"})
    exhibition_projects=[]
    for i in info_projects.find_all_next(name="div",attrs={"class":"iconLabel"}):
        a={}
        a["name"]=re.sub('\r|\t|\xa0|\n','',i.text)
        a["description"]=""
        a["img"]=url+i.find(name="img")["src"]
        exhibition_projects.append(a)
    # print(exhibition_projects)
    #教育活动
    info_edu=get_all(url_3).find(name="div",attrs={"class":"sub_one"})
    exhibition_edu=[]
    for i in info_edu.find_all(name="div",attrs={"class":"kpty_sub"}):
        a={}
        a["name"]=re.sub(' |\r|\t|\xa0|\n|\u3000','',i.find(name="div",attrs={"class":"title_sub"}).text)
        a["img"]=url+i.find(name="div",attrs={"class":"kpty_sub_text"}).a.img["src"]
        url_next=i.find(name="div",attrs={"class":"kpty_sub_text"}).a["href"]
        info_next=get_all(url_next).find(name="div",attrs={"class":"sj_div"})
        a["time"]=get_all(url_next).find(name="div",attrs={"class":"laiyuan"}).span.text
        a["description"]=""
        for j in info_next.find_all(name="p"):
            a["description"]+=re.sub(' |\r|\t|\xa0|\n|\u3000','',j.text)
        exhibition_edu.append(a)
    # print(exhibition_edu)

#xx这个也是js写的搞不定
def get_beijing_Country_Museum():
    url="https://baike.sogou.com/v238096.htm?fromTitle=%E4%B8%AD%E5%9B%BD%E5%9B%BD%E5%AE%B6%E5%8D%9A%E7%89%A9%E9%A6%86"
    name="中国国家博物馆"

#这个没有教育活动
def get_beijing_Agrituel_Museum():
    url="http://nongyebowuguan.meishujia.cn/"
    url_time="http://nongyebowuguan.meishujia.cn/?act=usite&said=360&usid=394"
    url_1="http://nongyebowuguan.meishujia.cn/?act=usite&said=368&usid=394"
    url_2="http://nongyebowuguan.meishujia.cn/?act=usite&said=354&usid=394"
    name="中国农业博物馆"
    #地址和电话和开放时间
    x=get_all(url_time).find(name="dd",attrs={"class":"theme_body_1231159117 theme_body_3728"})
    location=""
    number=""
    # opentime=re.sub("\r|\t|\xa0|\n",'',get_all(url_time).find(name="div",attrs={"class":"kfsj_text"}).text)
    for i in x.find_all(name="tr"):
        if(re.search(re.compile(r'电话:'),i.text)):
            number=re.sub("\r|\t|\xa0|\n",'',i.text)
        if(re.search(re.compile(r'地址:'),i.text)):
            location=re.sub("\r|\t|\xa0|\n",'',i.text)
    # print(number+location)
    #展览的简介和图片
    exhibition_hall=[]
    info_exh=get_all(url_1).find(name="dd",attrs={"class":"theme_body_1231159117 theme_body_3751"})
    for i in info_exh.find_all(name="td",attrs={"align":"center","valign":"middle","height":"130"}):
        a={}
        a["name"]=re.sub("\r|\t|\xa0|\n",'',i.find(name="td",attrs={"height":"25","align":"left","valign":"middle"}).text)
        a["img"]=url+i.find(name="td",attrs={"rowspan":"4","width":"80","height":"110","valign":"middle","align":"center"}).a.img["src"]
        url_next=url+i.find(name="td",attrs={"rowspan":"4","width":"80","height":"110","valign":"middle","align":"center"}).a["href"]
        info_next=get_all(url_next).find(name="ul",attrs={"class":"zl_r_b zl_r_bt"})
        a["description"]=re.sub("\r|\t|\xa0|\n",'',info_next.text)
        exhibition_hall.append(a)
        #print(a)
    # print(exhibition_hall)
    #博物馆藏品
    info_projects=get_all(url_2).find(name="dd",attrs={"class":"theme_body_1231159117 theme_body_3705"})
    exhibition_projects=[]
    for i in info_projects.find_all(name="td",attrs={"height":"170","align":"center","valign":"middle"}):
        a={}
        a["img"]=url+i.find(name="td",attrs={"width":"150","height":"130","align":"center","valign":"middle"}).a.img["src"]
        a["name"]=re.sub("\r|\t|\xa0|\n",'',i.find(name="td",attrs={"height":"25","align":"center","valign":"middle"}).text)
        a["description"]=""
        print(a)
        # exhibition_projects.append(a)
    # print(exhibition_projects)
    
def get_beijing_GWF_Museum():
    url="http://www.pgm.org.cn/pgm/index.shtml"
    url_jian="http://www.pgm.org.cn/pgm/gzzc/201808/5c5995d314464469b85d65fc47c3883d.shtml"
    url_time="http://www.pgm.org.cn/pgm/cgzl/201808/0091ebe1dfe345fa8936574adbb6a4d6.shtml"
    url_1="http://www.pgm.org.cn/pgm/cszl/lm_list.shtml"
    url_2="http://www.pgm.org.cn/newPgm_Collection/findCollectsByCate?cate.id=1&page=1"
    url_3="http://www.pgm.org.cn/pgm/wfdjt/list.shtml"
    url_x="http://www.pgm.org.cn/"
    url_y="http://www.pgm.org.cn/newPgm_Collection/"
    name="文化部恭王府博物馆"
    location=""
    number=""
    bref=""
    opentime=""
    main_image_url="http://pic.baike.soso.com/ugc/baikepic2/2422/20171218105942-1694169716.jpg/0"
    #地址和电话和开放时间
    x=get_all(url_1).find(name="div",attrs={"class":"inBottom fz12 textc"})
    for i in x.find_all(name="p"):
        if(re.search(re.compile(r'地址：'),i.text)):
            temp=i.text.split(" ")
            for j in temp:
                if(re.search(re.compile(r'地址：'),j)):
                    location=j
                if(re.search(re.compile(r'联系电话：'),j)):
                    number=j
    x=get_all(url_jian).find(name="div",attrs={"class":"pages_content"})
    for i in x.find_all(name="p"):
        bref+=re.sub("\r|\t|\xa0|\n",'',i.text)
    # print(bref)
    x=get_all(url_time).find(name="div",attrs={"class":"pages_content"})
    for i in x.find_all(name="p"):
        if(re.search(re.compile(r'时间：'),i.text)):
            opentime+=i.text
    # print(opentime)
    #展览的简介和图片
    exhibition_hall=[]
    info_exh=get_all(url_1).find(name="ul",attrs={"class":"lmlist"})
    for i in info_exh.find_all(name="li"):
        a={}
        a["name"]=re.sub("\r|\t|\xa0|\n",'',i.a.text)
        url_next=url_x+i.a["href"]
        info_next=get_all(url_next).find(name="div",attrs={"class":"zzzcZljj","id":"zzzcZljj"})
        a["img"]=url_x+info_next.find(name="dt",attrs={"class":"fl"}).img["src"]
        a["description"]=re.sub("\r|\t|\xa0|\n",'',info_next.find(name="dd",attrs={"class":"fr"}).text)
        exhibition_hall.append(a)
        # print(a)
    # print(exhibition_hall)
    #博物馆藏品
    info_projects=get_all(url_2).find(name="div",attrs={"class":"bke4 p18 mb40"})
    exhibition_projects=[]
    for i in info_projects.find_all(name="dl",attrs={"class":"lmpic"}):
        a={}
        a["img"]=url_x+i.find(name="dt").a.img["src"]
        url_next=url_y+i.find(name="dt").a["href"]
        info_next=get_all(url_next).find(name="div",attrs={"class":"w1200"})
        a["name"]=re.sub("\r|\t|\xa0|\n",'',i.find(name="dt").a.img["alt"])
        a["description"]=re.sub("\r|\t|\xa0|\n",'',info_next.find(name="table",attrs={"class":"biao wo"}).text)
        # print(a)
        exhibition_projects.append(a)
    # print(exhibition_projects)
    #教育活动
    info_edu=get_all(url_3).find(name="div",attrs={"class":"bke4 p18 mb40"})
    exhibition_edu=[]
    for i in info_edu.find_all(name="li"):
        a={}
        a["name"]=re.sub("\t","",i.a.text)
        a["time"]=i.span.text
        url_next=url_x+i.a["href"]
        info_next=get_all(url_next).find(name="div",attrs={"class":"pages_content"})
        a["description"]=""
        pos=url_next.rindex("/")
        url_temp=url_next[:pos+1]
        a["img"]=url_temp+info_next.find(name="img")["src"]
        for j in info_next.find_all(name="p"):
            a["description"]+=re.sub('\xa0','',j.text)
        # print(a)
        exhibition_edu.append(a)
    # print(exhibition_edu)


#天津
def get_tianjin_Museum():
    url="https://www.tjbwg.com/cn/Index.aspx"
    url_1="https://www.tjbwg.com/cn/Exhibition.aspx"
    url_2="https://www.tjbwg.com/cn/collection.aspx"
    url_3="https://www.tjbwg.com/cn/Events.aspx"
    url_x="https://www.tjbwg.com/cn/"
    name="天津博物馆"
    location=""
    number=""
    #地址和电话和开放时间
    x=get_all(url).find(name="div",attrs={"class":"footer footer1"})
    y=x.find(name="div",attrs={"class":"contact_f"})
    for i in y.find_all(name="div",attrs={"class":"volc"}):
        if(re.search(re.compile(r'地址：'),i.text)):
            location=re.sub("\r|\t|\xa0|\n",'',i.text)
        if(re.search(re.compile(r'电话：'),i.text)):
            number=re.sub("\r|\t|\xa0|\n",'',i.text)
    # print(location+number)
    #展览的简介和图片
    exhibition_hall=[]
    info_exh=get_all(url_1).find(name="div",attrs={"class":"exhList"})
    for i in info_exh.find_all(name="div",attrs={"class":re.compile(r'^item')}):
        a={}
        a["name"]=re.sub(" |\r|\t|\xa0|\n",'',i.find(name="div",attrs={"class":"text"}).a.text)
        a["description"]=re.sub(" |\r|\t|\xa0|\n",'',i.find(name="div",attrs={"class":"text"}).p.text)
        a["img"]=url_x+i.find(name="div",attrs={"class":"img"}).img["src"]
        exhibition_hall.append(a)
        # print(a)
    # print(exhibition_hall)
    #博物馆藏品
    info_projects=get_all(url_2).find(name="div",attrs={"class":"mainC"})
    exhibition_projects=[]
    for i in info_projects.find_all(name="li"):
        a={}
        a["img"]=url_x+i.find(name="div",attrs={"class":"img"}).img["src"]
        a["name"]=re.sub(" |\r|\t|\xa0|\n",'',i.find(name="h3",attrs={"class":"c_h"}).text)
        # a["description"]=re.sub("\r|\t|\xa0|\n",'',info_next.find(name="table",attrs={"class":"biao wo"}).text)
        url_next=url_x+i.find(name="div",attrs={"class":"item"}).a["href"]
        info_next=get_all(url_next).find(name="div",attrs={"class":"d_con"})
        a["description"]=re.sub("\r|\t|\xa0|\n",'',info_next.text)
        # print(a)
        exhibition_projects.append(a)
    # print(exhibition_projects)
    #教育活动
    info_edu=get_all(url_3).find(name="div",attrs={"class":"eventsList3"})
    exhibition_edu=[]
    for i in info_edu.find_all(name="li"):
        a={}
        a["name"]=re.sub(" |\r|\t|\xa0|\n","",i.find(name="div",attrs={"class":"text"}).text)
        a["img"]=url_x+i.find(name="div",attrs={"class":"img"}).img["src"]
        url_next=url_x+i.find(name="div",attrs={"class":"item"}).a["href"]
        info_next=get_all(url_next)
        a["time"]=re.sub(" |\r|\t|\xa0|\n","",info_next.find(name="div",attrs={"class":"time"}).text)
        a["description"]=re.sub(" |\r|\t|\xa0|\n","",info_next.find(name="div",attrs={"class":"newsD_con"}).text)
        # print(a)
        exhibition_edu.append(a)
    # print(exhibition_edu)

def get_all_new(url):
    requests.packages.urllib3.disable_warnings()
    res=requests.get(url,headers=headers,verify=False)
    res.encoding='utf-8'
    x = BeautifulSoup(res.text, 'html.parser')
    return x
#这个博物馆要ssl验证
def get_tianjin_Nature_Museum():
    url="https://www.tjnhm.com/"
    url_x="https://www.tjnhm.com/index.php?p=cgfw&id=11&lanmu=1"
    url_1="https://www.tjnhm.com/index.php?p=zlxx&c_id=5&lanmu=2"
    url_2="https://www.tjnhm.com/index.php?p=kxyj&lanmu=4&c_id=16"
    url_3="https://www.tjnhm.com/index.php?p=jyhd&lanmu=3"
    # name="天津自然博物馆"
    location=""
    number=""
    #地址和电话和开放时间
    x=get_all_new(url_x)
    y=x.find(name="div",attrs={"id":"aboutus_text"})
    for i in y.find_all(name="p"):
        if(re.search(re.compile(r'地'),i.text)):
            location=re.sub(" |\r|\t|\xa0|\n",'',i.text)
        if(re.search(re.compile(r'联系电话：'),i.text)):
            number=re.sub(" |\r|\t|\xa0|\n",'',i.text)
    # print(location+number)
    #展览的简介和图片
    exhibition_hall=[]
    info_exh=get_all_new(url_1).find(name="div",attrs={"id":"news_content"})
    for i in info_exh.find_all(name="div",attrs={"class":"pro"}):
        a={}
        a["name"]=re.sub(" |\r|\t|\xa0|\n",'',i.find(name="a",attrs={"class":"proname"}).text)
        a["img"]=url+i.find(name="img")["src"]
        url_next=url+i.find(name="a",attrs={"class":"proname"})["href"]
        info_next=get_all_new(url_next).find(name="div",attrs={"id":"aboutus_text"})
        a["description"]=re.sub(" |\r|\t|\xa0|\n",'',info_next.text)
        exhibition_hall.append(a)
        # print(a)
    # print(exhibition_hall)
    #博物馆藏品
    info_projects=get_all_new(url_2).find(name="div",attrs={"id":"news_content"})
    exhibition_projects=[]
    for i in info_projects.find_all(name="li"):
        a={}
        a["name"]=re.sub(" |\r|\t|\xa0|\n",'',i.find(name="a").text)
        a["name"]=a["name"][10:]
        url_next=url+i.find(name="a")["href"]
        info_next=get_all_new(url_next).find(name="div",attrs={"id":"aboutus_text"})
        a["img"]=url+info_next.find(name="img")["src"]
        a["description"]=""
        for j in info_next.find_all(name="p"):
            a["description"]+=re.sub("\r|\t|\xa0|\n",'',j.text)
        # print(a)
        exhibition_projects.append(a)
    # print(exhibition_projects)
    #教育活动
    info_edu=get_all_new(url_3).find(name="div",attrs={"id":"news_content"})
    exhibition_edu=[]
    for i in info_edu.find_all(name="li"):
        a={}
        a["name"]=re.sub(" |\r|\t|\xa0|\n",'',i.find(name="a").text)
        a["time"]=a["name"][:9]
        a["name"]=a["name"][10:]
        url_next=url+i.find(name="a")["href"]
        info_next=get_all_new(url_next).find(name="div",attrs={"id":"aboutus_text"})
        a["img"]=url+info_next.find(name="img")["src"]
        a["description"]=""
        for j in info_next.find_all(name="p"):
            a["description"]+=re.sub("\r|\t|\xa0|\n",'',j.text)
        # print(a)
        exhibition_edu.append(a)
    # print(exhibition_edu)

def get_tianjin_Art_Museum():
    name="天津美术馆"
    url="https://www.tjmsg.com/"
    url_bref="https://www.tjmsg.com/ArticleDetail.aspx?SrhClassCode=ACC0024"
    url_1="https://www.tjmsg.com/ArticleList.aspx?SrhClassCode=ACC0005"
    url_2="https://www.tjmsg.com/CollectionList.aspx?SrhClassCode=091a67b1-e176-4111-8abb-31cd8c58ee35"
    url_3="https://www.tjmsg.com/ArticleList.aspx?SrhClassCode=ACC0011"
    bref=""
    location=""
    number=""
    opentime=""
    #地址和电话和开放时间
    x=get_all(url_bref)
    y=x.find(name="div",attrs={"id":"content-box"})
    for i in y.find_all(name="p"):
        bref+=re.sub("\r|\t|\xa0|\n",'',i.text)
    y=x.find_all(name="div",attrs={"class":"msbottomfont2","align":"left"})
    s=""
    for i in y:
        s+=i.text
    opentime=s[s.index("示")+2:s.index("地")]
    location=s[s.index("地"):s.index("电")]
    number=s[s.index("电"):]
    # print(opentime+location+number)
    #展览的简介和图片
    exhibition_hall=[]
    info_exh=get_all(url_1).find(name="div",attrs={"class":"mslistbox3"})
    for i in info_exh.find_all(name="div",attrs={"class":"mslistbox10"}):
        a={}
        a["name"]=re.sub(" |\r|\t|\xa0|\n",'',i.find(name="div",attrs={"class":"mslistfont9"}).a.text)
        url_next=url+i.find(name="div",attrs={"class":"mslistfont9"}).a["href"]
        info_next=get_all(url_next).find(name="div",attrs={"class":"msneirongfont1","id":"content-box"})
        a["description"]=""
        for j in info_next.find_all(name="p"):
            a["description"]+=re.sub(" |\r|\t|\xa0|\n",'',j.text)
        a["img"]=url+i.find(name="img")["src"]
        exhibition_hall.append(a)
        # print(a)
    # print(exhibition_hall)
    #博物馆藏品   这个藏品但是没有介绍
    info_projects=get_all(url_2).find(name="div",attrs={"class":"msgcbox2"})
    exhibition_projects=[]
    for i in info_projects.find_all(name="div",attrs={"class":"msgcbox3"}):
        a={}
        a["img"]=url+i.find(name="img")["src"]
        a["name"]=re.sub(" |\r|\t|\xa0|\n",'',i.find(name="div",attrs={"class":"msgcbox4"}).a.text)
        # a["description"]=re.sub("\r|\t|\xa0|\n",'',info_next.find(name="table",attrs={"class":"biao wo"}).text)
        # url_next=url+i.find(name="div",attrs={"class":"msgcbox4"}).a["href"]
        # info_next=get_all(url_next).find(name="div",attrs={"class":"d_con"})
        a["description"]=""
        # print(a)
        exhibition_projects.append(a)
    # print(exhibition_projects)
    #教育活动
    info_edu=get_all(url_3).find(name="div",attrs={"class":"mslistbox3"})
    exhibition_edu=[]
    for i in info_edu.find_all(name="div",attrs={"class":"mslistbox10"}):
        a={}
        a["name"]=re.sub(" |\r|\t|\xa0|\n","",i.find(name="div",attrs={"class":"mslistfont9"}).a.text)
        a["img"]=url+i.find(name="img")["src"]
        for j in i.find_all(name="td",attrs={"colspan":"2"}):
            if(re.search(re.compile(r'活动时间：'),j.text)):
                a["time"]=re.sub(" |\r|\t|\xa0|\n","",j.text)

        url_next=url+i.find(name="div",attrs={"class":"mslistfont9"}).a["href"]
        info_next=get_all(url_next).find(name="div",attrs={"class":"mslistbox3"})
        a["description"]=""
        for j in info_next.find_all(name="p"):
            a["description"]+=re.sub(" |\r|\t|\xa0|\n","",j.text)
        # print(a)
        exhibition_edu.append(a)
    # print(exhibition_edu)

#河北
def get_hebei_Museum():
    #name="河北博物院"
    #这个时间没有
    url="http://www.hebeimuseum.org.cn/"
    url_1="http://www.hebeimuseum.org.cn/channels/12.html"
    url_2="http://www.hebeimuseum.org.cn/channels/25.html"
    url_3="http://www.hebeimuseum.org.cn/channels/30.html"
    location=""
    number=""
    opentime=""
    #地址和电话和开放时间
    info=get_all(url)
    x=info.find(name="div",attrs={"class":"copyright"})
    for i in x.find_all(name="p"):
        if(re.search(re.compile(r'院址'),i.text)):
            s=re.sub(" |\r|\t|\xa0|\n",'',i.text)
    location=s[s.index("院"):s.index("号")+1]
    number=s[s.index("T"):s.index("开")]
    y=info.find(name="div",attrs={"class":"guide"})
    for i in y.find_all(name="p"):
        if(re.search(re.compile(r'开放时间：'),i.text)):
            opentime=re.sub(" |\r|\t|\xa0|\n",'',i.text)
    # print(opentime+location+number)
    #展览的简介和图片
    exhibition_hall=[]
    info_exh=get_all(url_1).find(name="div",attrs={"class":"list"})
    for i in info_exh.find_all(name="li"):
        a={}
        a["name"]=re.sub(" |\r|\t|\xa0|\n",'',i.find(name="dd").a.text)
        a["img"]=url+i.find(name="img")["src"]
        url_next=url+i.find(name="dd").a["href"]
        info_next=get_all(url_next).find(name="div",attrs={"class":"text"})
        a["description"]=re.sub(" |\r|\t|\xa0|\n|\u3000",'',info_next.text)
        exhibition_hall.append(a)
        # print(a)
    # print(exhibition_hall)
    #博物馆藏品   这个藏品但是没有介绍
    info_projects=get_all(url_2).find(name="div",attrs={"class":"list"})
    exhibition_projects=[]
    for i in info_projects.find_all(name="li"):
        a={}
        a["img"]=url+i.find(name="img")["src"]
        a["name"]=re.sub(" |\r|\t|\xa0|\n",'',i.find(name="dd").a.text)
        url_next=url+i.find(name="dd").a["href"]
        info_next=get_all(url_next).find(name="div",attrs={"class":"photodetail"})
        a["description"]=re.sub(" |\r|\t|\xa0|\n|\u3000",'',info_next.text)
        # print(a)
        exhibition_projects.append(a)
    # print(exhibition_projects)
    #教育活动
    info_edu=get_all(url_3).find(name="div",attrs={"class":"list"})
    exhibition_edu=[]
    for i in info_edu.find_all(name="li"):
        a={}
        a["name"]=re.sub(" |\r|\t|\xa0|\n","",i.find(name="h4").a.text)
        a["img"]=url+i.find(name="img")["src"]
        a["description"]=re.sub(" |\r|\t|\xa0|\n|\u3000",'',i.find(name="div",attrs={"class":"text"}).p.text)
        a["time"]=re.sub(" |\r|\t|\xa0|\n|\u3000",'',i.find(name="span",attrs={"class":"time"}).text)
        # print(a)
        exhibition_edu.append(a)
    # print(exhibition_edu)

def get_all_x(url):
    re=requests.get(url,headers=headers)
    re.encoding='GBK'
    soup = BeautifulSoup(re.text, 'html.parser')
    return soup

def get_hebei_HD_Museum():
    url="http://www.hdmuseum.org/"
    url_1="http://www.hdmuseum.org/product.asp?cd=47"
    url_2="http://www.hdmuseum.org/product.asp?cd=58"
    url_3="http://www.hdmuseum.org/newslist.asp?cd=50"
    #name="邯郸市博物馆"
    location=""
    number=""
    #地址和电话和开放时间
    info=get_all_x(url)
    x=info.find(name="table",attrs={"width":"1025","border":"0","cellspacing":"0","cellpadding":"0","align":"center","style":"height:48px;"})
    xx=x.find(name="td",attrs={"class":"footcopyright"})
    s=re.sub(" |\r|\t|\xa0|\n",'',xx.text)
    location=s[s.index("地"):s.index("电")]
    number=s[s.index("电"):s.index("邮")]
    # print(location+number)
    #展览的简介和图片x
    exhibition_hall=[]
    info_exh=get_all_x(url_1).find(name="table",attrs={"border":"0","cellspacing":"0","cellpadding":"0","style":"margin-top:20px;"})
    for i in info_exh.find_all(name="td",attrs={"align":"center","width":"255","valign":"top"}):
        a={}
        a["name"]=re.sub(" |\r|\t|\xa0|\n",'',i.find(name="a",attrs={"class":"protitle"}).text)
        a["img"]=url+i.find(name="img")["src"]
        url_next=url+i.find(name="a",attrs={"class":"protitle"})["href"]
        info_next=get_all_x(url_next).find(name="td",attrs={"class":"infodetailcontent"})
        s=re.sub(" |\r|\t|\xa0|\n|\u3000",'',info_next.text)
        if(re.search(re.compile("[a-zA-Z]"),s)):
            a["description"]=s[:s.index("W")]
        else:
            a["description"]=s
        exhibition_hall.append(a)
        # print(a)
    # print(exhibition_hall)
    #博物馆藏品   这个藏品有几个没有介绍
    info_projects=get_all_x(url_2).find(name="table",attrs={"border":"0","cellspacing":"0","cellpadding":"0","style":"margin-top:20px;"})
    exhibition_projects=[]
    for i in info_projects.find_all(name="td",attrs={"align":"center","width":"255","valign":"top"}):
        a={}
        a["name"]=re.sub(" |\r|\t|\xa0|\n",'',i.find(name="a",attrs={"class":"protitle"}).text)
        a["img"]=url+i.find(name="img")["src"]
        url_next=url+i.find(name="a",attrs={"class":"protitle"})["href"]
        # a["description"]=re.sub("\r|\t|\xa0|\n",'',info_next.find(name="table",attrs={"class":"biao wo"}).text)
        info_next=get_all_x(url_next).find(name="td",attrs={"class":"infodetailcontent"})
        a["description"]=re.sub(" |\r|\t|\xa0|\n|\u3000",'',info_next.text)
        # print(a)
        exhibition_projects.append(a)
    # print(exhibition_projects)
    #教育活动  弄7个因为第8个没图片
    info_edu=get_all_x(url_3).find(name="td",attrs={"valign":"top","style":"padding-top:7px;"})
    exhibition_edu=[]
    count=0
    for i in info_edu.find_all(name="tr",attrs={"onmouseover":"this.style.backgroundColor='#F1EFEF';"}):
        if(count<7):
            a={}
            a["name"]=re.sub(" |\r|\t|\xa0|\n","",i.find(name="a",attrs={"class":"newslink"}).text)
            a["time"]=re.sub(" |\r|\t|\xa0|\n|\u3000",'',i.find(name="td",attrs={"class":"leftfbdate","width":"200"}).text)
            url_next=url+i.find(name="a",attrs={"class":"newslink"})["href"]
            info_next=get_all_x(url_next).find(name="td",attrs={"class":"infodetailcontent"})
            a["img"]=url+info_next.find(name="img")["src"]
            a["description"]=re.sub(" |\r|\t|\xa0|\n|\u3000",'',info_next.text)
            # print(a)
            count+=1
            exhibition_edu.append(a)
    print(exhibition_edu)

def get_hebei_SJZ_Museum():
    url_s="https://baike.sogou.com/v5189145.htm?fromTitle=%E7%9F%B3%E5%AE%B6%E5%BA%84%E5%B8%82%E5%8D%9A%E7%89%A9%E9%A6%86"
    name="石家庄市博物馆"
    url="http://sjzmuseum.com/"
    url_1="http://sjzmuseum.com/a/case/zhanlanhuigu/"
    url_2="http://sjzmuseum.com/a/products/p3/"
    url_3="http://sjzmuseum.com/a/rongyu/zhiyuanzhezhaomupeixun/"
    location=""
    number=""
    #地址和电话和开放时间
    xx=get_all(url).find(name="div",attrs={"class":"xl12 xs12 xm8 xb8"})
    s=re.sub(" |\r|\t|\xa0|\n",'',xx.text)
    location=s[s.index("地"):s.index("号")+1]
    number=s[s.index("电"):s.index("邮")]
    # print(location+number)
    #展览的简介和图片x
    exhibition_hall=[]
    info_exh=get_all(url_1).find(name="div",attrs={"class":"container padding-big caselist"})
    for i in info_exh.find_all(name="div",attrs={"class":"xl12 xs6 xm4 xb4 casebox"}):
        a={}
        a["name"]=re.sub(" |\r|\t|\xa0|\n",'',i.find(name="div",attrs={"class":"caseitem"}).h3.text)
        a["img"]=url+i.find(name="img")["src"]
        url_next=url+i.find(name="a")["href"]
        info_next=get_all(url_next).find(name="div",attrs={"class":"tab-body"})
        a["description"]=re.sub(" |\r|\t|\xa0|\n|\u3000",'',info_next.text)
        exhibition_hall.append(a)
        # print(a)
    # print(exhibition_hall)
    #博物馆藏品 没有简介
    info_projects=get_all(url_2).find(name="div",attrs={"class":"container padding-big prolist"})
    exhibition_projects=[]
    for i in info_projects.find_all(name="div",attrs={"class":"xl12 xs6 xm4 xb3 proitem"}):
        a={}            
        a["name"]=re.sub(" |\r|\t|\xa0|\n",'',i.find(name="h3").text)
        a["img"]=url+i.find(name="img")["src"]
        url_next=url+re.sub(" ",'',i.find(name="a")["href"])
        a["description"]=""
        exhibition_projects.append(a)
        # print(a)
    # print(exhibition_projects)
    #教育活动 
    exhibition_edu=[]
    info_exh=get_all(url_3).find(name="div",attrs={"class":"newsitem padding-big-top"})
    for i in info_exh.find_all(name="li",attrs={"class":"clearfix"}):
        a={}
        a["name"]=re.sub(" |\r|\t|\xa0|\n",'',i.find(name="div",attrs={"class":"news-bodys"}).h3.text)
        s1=re.sub(" |\r|\t|\xa0|\n",'',i.find(name="div",attrs={"class":"news-date1"}).text)
        s2=re.sub(" |\r|\t|\xa0|\n",'',i.find(name="div",attrs={"class":"news-date2"}).text)
        a["time"]=s2+"/"+s1
        url_next=url+i.find(name="a")["href"]
        info_next=get_all(url_next).find(name="div",attrs={"class":"news-body"})
        a["img"]=info_next.find(name="img")["src"]
        a["description"]=re.sub("\r|\t|\xa0|\n|\u3000",'',info_next.text)
        exhibition_edu.append(a)
        print(a)
    # print(exhibition_edu)
    info_main={}
    info_main=get_Museum_brefandtime_new(url_s,name)
    info_main["name"]=name
    info_main["location"]=location
    info_main["number"]=number
    info_all={}
    info_all["1"]=info_main
    info_all["2"]=exhibition_hall
    info_all["3"]=exhibition_projects
    info_all["4"]=exhibition_edu
    return info_all


def get_hebei_ZJK_Museum():
    url="http://www.zjkmuseum.com/"
    url_1="http://www.zjkmuseum.com/Pic_List.asp?ClassId=7"
    url_2="http://www.zjkmuseum.com/Pic_List.asp?ClassId=5"
    url_3="http://www.zjkmuseum.com/Message_List.asp?ClassId=11"
    url_s="https://baike.sogou.com/v51113247.htm?fromTitle=%E5%BC%A0%E5%AE%B6%E5%8F%A3%E5%8D%9A%E7%89%A9%E9%A6%86"
    name="张家口博物馆"
    #没有开馆时间
    location="张家口市桥东区东兴街14号"
    number="0313-217059"
    opentime="周二 至 周日9:00 至 11:00上午开馆时间2:30 至 4:30下午开馆时间"
    #地址和电话和开放时间
    #展览的简介和图片x
    exhibition_hall=[]
    info_exh=get_all_x(url_1).find(name="div",attrs={"class":"imgList"})
    for i in info_exh.find_all(name="li"):
        a={}
        a["name"]=re.sub(" |\r|\t|\xa0|\n",'',i.find(name="div",attrs={"class":"itemText"}).h3.text)
        a["img"]=url+i.find(name="img")["src"]
        a["description"]=""
        exhibition_hall.append(a)
        # print(a)
    # print(exhibition_hall)
    #博物馆藏品 没有简介
    info_projects=get_all_x(url_2).find(name="div",attrs={"class":"imgList"})
    exhibition_projects=[]
    for i in info_projects.find_all(name="li"):
        a={}
        a["name"]=re.sub(" |\r|\t|\xa0|\n",'',i.find(name="div",attrs={"class":"itemText"}).h3.text)
        a["img"]=url+i.find(name="img")["src"]
        a["description"]=""
        exhibition_projects.append(a)
        # print(a)
    # print(exhibition_projects)
    #教育活动 
    exhibition_edu=[]
    info_exh=get_all_x(url_3).find(name="ul",attrs={"class":"msgList"})
    for i in info_exh.find_all(name="li"):
        a={}
        a["name"]=re.sub(" |\r|\t|\xa0|\n",'',i.find(name="a").text)
        a["time"]=re.sub(" |\r|\t|\xa0|\n",'',i.em.text)
        url_next=url+i.find(name="a")["href"]
        info_next=get_all_x(url_next).find(name="div",attrs={"id":"MsgContent"})
        a["img"]=info_next.find(name="img")["src"]
        a["description"]=re.sub("\r|\t|\xa0|\n|\u3000",'',info_next.text)
        exhibition_edu.append(a)
        # print(a)
    # print(exhibition_edu)
    info_main={}
    # info_main=get_Museum_brefandtime_new(url_s,name)
    info_main["name"]=name
    info_main["location"]=location
    info_main["number"]=number
    info_main["opentime"]=opentime
    info_all={}
    info_all["1"]=info_main
    info_all["2"]=exhibition_hall
    info_all["3"]=exhibition_projects
    info_all["4"]=exhibition_edu
    return info_all

get_hebei_ZJK_Museum()
#山西
def get_shanxi_Museum():
    #name="山西博物院"
    url="http://www.shanximuseum.com/"
    url_1="http://www.shanximuseum.com/htltopics.html"
    url_2="http://www.shanximuseum.com/collection.html"
    url_3="http://www.shanximuseum.com/activity_list.html"
    #地址和电话和开放时间
    location="地址：山西省太原市滨河西路北段13号"
    number="电话：0351-8789188"
    #展览的简介和图片x
    exhibition_hall=[]
    info_exh=get_all(url_1).find(name="div",attrs={"class":"list","id":"datalist"})
    for i in info_exh.find_all(name="div",attrs={"class":"item"}):
        a={}
        a["name"]=re.sub(" |\r|\t|\xa0|\n",'',i.find(name="div",attrs={"class":"h18"}).a.text)
        a["img"]=url+i.find(name="img")["src"]
        a["description"]=re.sub(" |\r|\t|\xa0|\n",'',i.find(name="div",attrs={"class":"p"}).text)
        exhibition_hall.append(a)
        # print(a)
    # print(exhibition_hall)
    #博物馆藏品   这个藏品有几个没有介绍
    info_projects=get_all(url_2).find(name="div",attrs={"class":"waterfall show","id":"datalist"})
    exhibition_projects=[]
    for i in info_projects.find_all(name="div",attrs={"class":"wf-item"}):
        a={}
        a["name"]=re.sub(" |\r|\t|\xa0|\n",'',i.find(name="div",attrs={"class":"tit"}).text)
        a["img"]=url+i.find(name="img")["src"]
        a["description"]=""
        exhibition_hall.append(a)
        # print(a)
    # print(exhibition_projects)
    #教育活动  
    info_projects=get_all(url_3).find(name="div",attrs={"id":"datalist"})
    exhibition_edu=[]
    for i in info_projects.find_all(name="div",attrs={"class":"item"}):
        a={}
        a["name"]=re.sub(" |\r|\t|\xa0|\n",'',i.find(name="div",attrs={"class":"h16"}).text)
        a["time"]=re.sub(" |\r|\t|\xa0|\n",'',i.find(name="div",attrs={"class":"date"}).text)
        a["img"]=url+i.find(name="img")["src"]
        url_next=url+i.find(name="div",attrs={"class":"h16"}).a["href"]
        info_next=get_all(url_next).find(name="div",attrs={"class":"article"})
        a["description"]=re.sub(" |\r|\t|\xa0|\n|\u3000",'',info_next.text)
        exhibition_edu.append(a)
        # print(a)
    # print(exhibition_edu)
							
def get_shanxi_MT_Museum():
    #name="中国煤炭博物馆"
    url="http://www.coalmus.org.cn/"
    url_1="http://www.coalmus.org.cn/html/list_1659.html"
    url_2="http://www.coalmus.org.cn/html/list_1548.html"
    url_3="http://www.coalmus.org.cn/html/list_1657.html"
    #地址和电话和开放时间 
    location="地址：山西省太原市迎泽西大街2号"
    number="电话：0351-6180108"
    #展览的简介和图片x
    exhibition_hall=[]
    info_exh=get_all(url_1).find(name="div",attrs={"id":"LB"})
    for i in info_exh.find_all(name="li"):
        a={}
        a["name"]=re.sub(" |\r|\t|\xa0|\n",'',i.find(name="h2").a.text)
        url_next=i.find(name="h2").a["href"]
        info_next=get_all(url_next).find(name="div",attrs={"id":"MyContent"})
        a["img"]=url+info_next.find(name="img")["src"]
        a["description"]=re.sub(" |\r|\t|\xa0|\n|\u3000",'',info_next.text)
        exhibition_hall.append(a)
        # print(a)
    # print(exhibition_hall)
    #博物馆藏品   这个藏品有几个没有介绍
    info_projects=get_all(url_2).find(name="ul",attrs={"class":"display","id":"c11"})
    exhibition_projects=[]
    for i in info_projects.find_all(name="li"):
        a={}
        a["img"]=i.find(name="img")["src"]
        url_next=i.find(name="a")["href"]
        info_next=get_all(url_next)
        a["name"]=re.sub(" |\r|\t|\xa0|\n",'',info_next.find(name="div",attrs={"class":"title"}).text)
        a["description"]=re.sub(" |\r|\t|\xa0|\n",'',info_next.find(name="div",attrs={"class":"nph_intro"}).text)
        exhibition_projects.append(a)
        # print(a)
    # print(exhibition_projects)
    #教育活动
    exhibition_edu=[]
    info_projects=get_all(url_3).find(name="div",attrs={"id":"LB"})
    for i in info_exh.find_all(name="li"):
        a={}
        a["name"]=re.sub(" |\r|\t|\xa0|\n",'',i.find(name="h2").a.text)
        a["time"]=re.sub(" |\r|\t|\xa0|\n|",'',i.find(name="span",attrs={"class":"date"}).text)
        url_next=i.find(name="h2").a["href"]
        info_next=get_all(url_next).find(name="div",attrs={"id":"MyContent"})
        a["img"]=url+info_next.find(name="img")["src"]
        a["description"]=re.sub(" |\r|\t|\xa0|\n|\u3000",'',info_next.text)
        exhibition_edu.append(a)
        print(a)
    # print(exhibition_edu)

#xx这个博物馆也搞不定。数据就是摘不下来
def get_shanxi_BLJTH_Museum():
    #name="八路军太行纪念馆"
    url="http://www.balujun.cn/"
    url_time="http://www.balujun.cn/e/action/ShowInfo.php?classid=81&id=2338"
    url_1="http://www.balujun.cn/e/action/ListInfo/?classid=8"
    url_2="http://www.coalmus.org.cn/html/list_1548.html"
    url_3="http://www.coalmus.org.cn/html/list_1657.html"
    #地址和电话和开放时间 
    location=""
    number=""
    x=get_all(url_time).find(name="div",attrs={"class":"v_news_content"})
    for i in x.find_all(name="p"):
        if(re.search(re.compile(r'地址：'),i.text)):
            location=re.sub(" |\r|\t|\xa0|\n",'',i.text)
        if(re.search(re.compile(r'电话：'),i.text)):
            number=re.sub(" |\r|\t|\xa0|\n",'',i.text)                       
    # print(location+number)
    #展览的简介和图片x
    exhibition_hall=[]
    info_exh=get_all(url_1)
    num=0
    for i in info_exh.find_all(name="li"):
        if(num>=1):
            a={}
            a["name"]=re.sub(" |\r|\t|\xa0|\n",'',i.find(name="h3").text)
            a["img"]=url+i.find(name="img")["src"]
            url_next=i.find(name="a")["href"]
            info_next=get_all(url_next).find(name="div",attrs={"class":"v_news_content"})
            a["description"]=re.sub(" |\r|\t|\xa0|\n|\u3000",'',info_next.text)
            exhibition_hall.append(a)
            print(a)
        num+=1
        print(num)
    # print(exhibition_hall)

#没有教育活动
def get_shanxi_MS_Museum():
    #name="山西省民俗博物馆"
    url="http://www.sxfam.org.cn/"
    url_time="http://www.sxfam.org.cn/e/action/ShowInfo.php?classid=1&id=33"
    url_1="http://www.sxfam.org.cn/e/action/ListInfo/?classid=10"
    url_2="http://www.sxfam.org.cn/e/action/ListInfo/?classid=16"
    url_3="http://www.coalmus.org.cn/html/list_1657.html"
    #地址和电话和开放时间 
    location=""
    number=""
    bref=""
    opentime=""
    main_image_url="http://www.sxfam.org.cn/d/file/p/2019/06-12/249e628df533afa183fa719dcf4b2814.jpg"
    x=get_all(url_time).find(name="div",attrs={"class":"bd clear"})
    for i in x.find_all(name="p"):
        bref+=re.sub(" |\r|\t|\xa0|\n",'',i.text)
        if(re.search(re.compile(r'地址：'),i.text)):
            location=re.sub(" |\r|\t|\xa0|\n",'',i.text)
        if(re.search(re.compile(r'电话：'),i.text)):
            number=re.sub(" |\r|\t|\xa0|\n",'',i.text)
        if(re.search(re.compile(r'开放时间：'),i.text)):
            opentime=re.sub(" |\r|\t|\xa0|\n",'',i.text) 
    bref=bref[:bref.index("能")+1]                       
    # print(bref+location+number+opentime)
    #展览的简介和图片x
    exhibition_hall=[]
    info_exh=get_all(url_1).find(name="div",attrs={"class":"bd"})
    num=0
    for i in info_exh.find_all(name="li"):
        a={}
        a["name"]=re.sub(" |\r|\t|\xa0|\n",'',i.find(name="h4").text)
        a["img"]=i.find(name="img")["src"]
        if(a["img"][0]!="h"):
            a["img"]=url+a["img"]
        url_next=url+i.find(name="a")["href"]
        info_next=get_all(url_next).find(name="div",attrs={"class":"bd clear"})
        a["description"]=re.sub(" |\r|\t|\xa0|\n|\u3000",'',info_next.text)
        exhibition_hall.append(a)
        # print(a)
    # print(exhibition_hall)  
    #博物馆藏品   这个藏品有几个没有介绍
    info_projects=get_all(url_2).find(name="div",attrs={"class":"bdd"})
    exhibition_projects=[]
    for i in info_projects.find_all(name="li"):
        a={}
        a["name"]=re.sub(" |\r|\t|\xa0|\n",'',i.find(name="h4").text)
        a["img"]=url+i.find(name="img")["src"]
        url_next=url+i.find(name="a")["href"]
        info_next=get_all(url_next).find(name="div",attrs={"class":"bd clear"})
        a["description"]=re.sub(" |\r|\t|\xa0|\n|\u3000",'',info_next.text)
        exhibition_projects.append(a)
        print(a)
    # print(exhibition_projects) 
    #                   

#xx不知道用了什么手段，只能爬取到列表的第一个值
def get_shanxi_YS_Museum():
    #name="山西省艺术博物馆"
    url="http://www.sxam.org.cn/"
    url_time="http://www.sxam.org.cn/e/action/ShowInfo.php?classid=11&id=112"
    url_x="http://www.sxam.org.cn/e/action/ShowInfo.php?classid=11&id=6"
    url_y="http://www.sxam.org.cn/e/action/ShowInfo.php?classid=2&id=5"
    url_1="http://www.sxam.org.cn/e/action/ListInfo/?classid=18"
    url_2="http://www.sxam.org.cn/e/action/ListInfo/?classid=23"
    url_3="http://www.coalmus.org.cn/html/list_1657.html"
    #地址和电话和开放时间 
    location=""
    number=""
    bref=""
    opentime="开放时间：周二至周日正常开馆，周一公休。节假日另行安排。"
    main_image_url="http://www.sxam.org.cn/d/file/p/2020/04-26/4280ba8dd26cd5a9b7dc251ff02b029e.png"
    x=get_all(url_time).find(name="div",attrs={"class":"v_news_content"})
    for i in x.find_all(name="p"):
        if(re.search(re.compile(r'地址：'),i.text)):
            location=re.sub(" |\r|\t|\xa0|\n",'',i.text)
        if(re.search(re.compile(r'电话：'),i.text)):
            number=re.sub(" |\r|\t|\xa0|\n",'',i.text)
    x=get_all(url_x).find(name="div",attrs={"class":"v_news_content"})
    for i in x.find_all(name="p"):
        if(re.search(re.compile(r'每周'),i.text)):
            opentime=re.sub(" |\r|\t|\xa0|\n",'',i.text) 
    x=get_all(url_y).find(name="div",attrs={"class":"v_news_content"})
    for i in x.find_all(name="p"):
        bref+=re.sub(" |\r|\t|\xa0|\n",'',i.text)                 
    # print(bref)
    #展览的简介和图片x
    exhibition_hall=[]
    info_exh=get_all(url_1).find(name="div",attrs={"class":"list fl"}).ul
    for i in info_exh.find_all(name="li"):
        a={}
        a["name"]=re.sub(" |\r|\t|\xa0|\n",'',i.find(name="h3").text)
        a["img"]=i.find(name="img")["src"]
        if(a["img"][0]!="h"):
            a["img"]=url+a["img"]
        url_next=url+i.find(name="a")["href"]
        info_next=get_all(url_next).find(name="div",attrs={"class":"v_news_content"})
        a["description"]=re.sub(" |\r|\t|\xa0|\n|\u3000",'',info_next.text)
        exhibition_hall.append(a)
        # print(a)
    # print(exhibition_hall) 
    #  #博物馆藏品   这个藏品有几个没有介绍
    info_projects=get_all(url_2).find(name="div",attrs={"class":"main"})
    print(info_projects)
    exhibition_projects=[]
    for i in info_projects.find_all(name="li"):
        a={}
        a["name"]=re.sub(" |\r|\t|\xa0|\n",'',i.find(name="h3").text)
        a["img"]=i.find(name="img")["src"]
        if(a["img"][0]!="h"):
            a["img"]=url+a["img"]
        url_next=url+i.find(name="a")["href"]
        info_next=get_all(url_next).find(name="div",attrs={"class":"v_news_content"})
        a["description"]=re.sub(" |\r|\t|\xa0|\n|\u3000",'',info_next.text)
        exhibition_projects.append(a)
        print(a)
    # print(exhibition_projects)  

def get_shanxi_DT_Museum():
    #name="大同市博物馆"
    url="http://www.datongmuseum.com/index.php"
    url_time="http://www.sxam.org.cn/e/action/ShowInfo.php?classid=11&id=112"
    url_1="http://www.datongmuseum.com/exhibition_category.php"
    url_2="http://www.datongmuseum.com/product_category.php"
    url_3="http://www.datongmuseum.com/article_category.php?id=4"
    url_bref="http://www.datongmuseum.com/about.php?id=intro"
    url_time="http://www.datongmuseum.com/page.php?id=20"
    #地址和电话和开放时间 
    location="大同市平城区太和路"
    number="电话：0352-2303518"
    bref=re.sub(" |\r|\t|\xa0|\n",'',get_all(url_bref).find(name="div",attrs={"class":"ins_cont"}).text)
    main_image_url="http://www.datongmuseum.com/data/slide/20160124wurfxy.png"
    opentime=re.sub(" |\r|\t|\xa0|\n",'',get_all(url_time).find(name="div",attrs={"class":"cent_rig"}).text)
    # print( opentime)
    #展览的简介和图片x
    exhibition_hall=[]
    info_exh=get_all(url_1).find(name="div",attrs={"class":"ct_mel clearfix"})
    for i in info_exh.find_all(name="div",attrs={"class":"mel"}):
        a={}
        a["name"]=re.sub(" |\r|\t|\xa0|\n",'',i.find(name="p").text)
        a["img"]=i.find(name="img")["src"]
        url_next=i.find(name="p").a["href"]
        info_next=get_all(url_next).find(name="div",attrs={"class":"ft_cont01"})
        a["description"]=re.sub(" |\r|\t|\xa0|\n|\u3000",'',info_next.text)
        exhibition_hall.append(a)
        # print(a)
    # print(exhibition_hall)
    #博物馆藏品 
    info_projects=get_all(url_2).find(name="ul",attrs={"class":"sc_ul clearfix"})
    exhibition_projects=[]
    for i in info_projects.find_all(name="li"):
        a={}
        a["name"]=re.sub(" |\r|\t|\xa0|\n",'',i.find(name="p").text)
        a["img"]=i.find(name="img")["src"]
        url_next=i.find(name="a")["href"]
        info_next=get_all(url_next).find(name="div",attrs={"class":"sc_pl"})
        a["description"]=re.sub(" |\r|\t|\xa0|\n|\u3000",'',info_next.text)
        exhibition_projects.append(a)
        # print(a)
    # print(exhibition_projects)
    #教育活动 没有图片
    exhibition_edu=[]
    info_exh=get_all(url_3).find(name="ul",attrs={"class":"xs_cb"})
    for i in info_exh.find_all(name="li"):
        a={}
        a["name"]=re.sub(" |\r|\t|\xa0|\n",'',i.find(name="a").text)
        url_next=i.find(name="a")["href"]
        info_next=get_all(url_next)
        s=re.sub("|\r|\t|\xa0|\n|",'',info_next.find(name="div",attrs={"class":"Tow_h3"}).p.text)
        a["time"]=s[s.index("2"):]
        a["description"]=""
        for j in info_next.find(name="div",attrs={"class":"Tow_cont"}).find_all(name="p"):
            a["description"]+=re.sub(" |\r|\t|\xa0|\n|\u3000",'',j.text)
        exhibition_edu.append(a)
        # print(a)
    # print(exhibition_edu)

def get_shanxi_YC_Museum():
    #name="运城博物馆"
    url="http://www.sxycbwg.com/"
    url_1="http://www.sxycbwg.com/list.asp?classid=18"
    url_2="http://www.sxycbwg.com/picall.asp?classid=22"
    url_3="http://www.sxycbwg.com/list.asp?ClassId=61"
    url_bref="http://www.sxycbwg.com/list.asp?ClassId=93"
    url_x="http://www.sxycbwg.com/list.asp?ClassId=96"
    url_y="http://www.sxycbwg.com/list.asp?Classid=54"
    #地址和电话和开放时间 
    bref=re.sub(" |\r|\t|\xa0|\n",'',get_all_x(url_bref).find(name="ul",attrs={"class":"list_box1"}).text)
    # print(bref)
    s=re.sub(" |\r|\t|\xa0|\n",'',get_all_x(url_x).find(name="ul",attrs={"class":"list_box1"}).text)
    location=s[s.index("地"):s.index("处")+1]
    number=s[s.index("电"):s.index("通")-1]
    # print(location+number)
    main_image_url="http://www.sxycbwg.com/images/psu.jpg"
    s=re.sub(" |\r|\t|\xa0|\n",'',get_all_x(url_y).find(name="ul",attrs={"class":"list_box1"}).text)
    opentime=s[s.rindex("开"):]
    #展览的简介和图片x
    exhibition_hall=[]
    info_exh=get_all_x(url_1).find(name="ul",attrs={"class":"list_box1"})
    for i in info_exh.find_all(name="li"):
        a={}
        a["name"]=re.sub(" |\r|\t|\xa0|\n",'',i.find(name="a").text)
        url_next=url+i.find(name="a")["href"]
        info_next=get_all_x(url_next).find(name="div",attrs={"class":"con"})
        a["img"]=url+info_next.find(name="img")["src"]
        a["description"]=re.sub(" |\r|\t|\xa0|\n|\u3000",'',info_next.text)
        # exhibition_hall.append(a)
        # print(a)
    # print(exhibition_hall)
    #博物馆藏品 
    exhibition_projects=[]
    info_projects=get_all_x(url_2).find(name="ul",attrs={"class":"list_box1"})
    for i in info_projects.find_all(name="li"):
        a={}
        a["name"]=re.sub(" |\r|\t|\xa0|\n",'',i.find(name="a").text)
        url_next=url+i.find(name="a")["href"]
        info_next=get_all_x(url_next).find(name="div",attrs={"class":"con"})
        a["img"]=url+info_next.find(name="img")["src"]
        a["description"]=re.sub(" |\r|\t|\xa0|\n|\u3000",'',info_next.text)
        exhibition_projects.append(a)
        # print(a)
    # print(exhibition_projects)
    #教育活动 没有图片
    exhibition_edu=[]
    info_exh=get_all_x(url_3).find(name="ul",attrs={"class":"list_box1"})
    for i in info_exh.find_all(name="li"):
        a={}
        a["name"]=re.sub(" |\r|\t|\xa0|\n",'',i.find(name="a").text)
        a["time"]=re.sub(" |\r|\t|\xa0|\n",'',i.find(name="span").text)
        url_next=url+i.find(name="a")["href"]
        info_next=get_all_x(url_next).find(name="div",attrs={"class":"con"})
        a["img"]=url+info_next.find(name="img")["src"]
        a["description"]=re.sub(" |\r|\t|\xa0|\n|\u3000",'',info_next.text)
        exhibition_edu.append(a)
        # print(a)
    # print(exhibition_edu)

#内蒙古
def get_neimenggu_Museum():
    #name="内蒙古博物院"
    url="http://www.nmgbwy.com/"
    url_1="http://www.nmgbwy.com/zldt/index.jhtml?contentId=154"
    url_2="http://www.nmgbwy.com/lsww/index.jhtml"
    url_3="http://www.nmgbwy.com/sjdt/index.jhtml?contentId=155"
    location=""
    number=""
    #地址和电话和开放时间
    info=get_all(url)
    x=info.find(name="div",attrs={"style":"white-space:nowrap;margin-top:16px;"})
    for i in x.find_all(name="p"):
        if(re.search(re.compile(r'咨询电话：'),i.text)):
            number=re.sub("\r|\t|\xa0|\n",'',i.text)
        if(re.search(re.compile(r'地址'),i.text)):
            location=re.sub("\r|\t|\xa0|\n",'',i.text)
    # print(number+location)
    #展览 爬不了，因为全部是线上展厅的形式
    exhibition_hall=[]
    # print(exhibition_hall)
    #博物馆藏品 没有简介
    exhibition_projects=[]
    info_projects=get_all(url_2).find(name="div",attrs={"class":"row","style":"margin-top:10px;width:90%;margin-bottom: 20px"})
    for i in info_projects.find_all(name="div",attrs={"class":"col-md-3 col-sm-3 col-xs-5"}):
        a={}
        a["name"]=re.sub(" |\r|\t|\xa0|\n",'',i.find(name="div",attrs={"style":"text-align: center;"}).text)
        a["img"]=url+i.find(name="img")["src"]
        a["description"]=""
        exhibition_projects.append(a)
        # print(a)
    # print(exhibition_projects)
    #教育活动 没有图片
    exhibition_edu=[]
    info_exh=get_all(url_3).find(name="div",attrs={"class":"row","style":"margin:20px;"})
    for i in info_exh.find_all(name="div",attrs={"class":"row"}):
        a={}
        a["name"]=re.sub("|\r|\t|\xa0|\n",'',i.find(name="div",attrs={"class":"col-xs-9"}).a.text)
        a["img"]=url+i.find(name="img")["src"]
        url_next=i.find(name="a")["href"]
        info_next=get_all(url_next).find(name="div",attrs={"style":"margin:33px;text-align:left;"})
        a["description"]=""
        for j in info_next.find_all(name="p"):
            if(re.search(re.compile(r'发布时间'),j.text)):
                a["time"]=re.sub(" |\r|\t|\xa0|\n",'',j.text)
            else:
                a["description"]+=re.sub(" |\r|\t|\xa0|\n|\u3000",'',j.text)
        exhibition_edu.append(a)
        # print(a)
    # print(exhibition_edu)

#xx这个博物馆不安全 我也是佛了
def get_neimenggu_ERDS_Museum():
    #name="鄂尔多斯博物馆"
    #没有获取时间
    url="https://baike.sogou.com/v41309396.htm?fromTitle=%E9%84%82%E5%B0%94%E5%A4%9A%E6%96%AF%E5%8D%9A%E7%89%A9%E9%A6%86"

#这个博物馆没有教育活动
def get_neimenggu_CF_Museum():
    #name="赤峰博物馆"
    url="http://chifengbowuguan.meishujia.cn/"
    url_1="http://chifengbowuguan.meishujia.cn/?act=usite&said=368&usid=813"
    url_2="http://chifengbowuguan.meishujia.cn/?act=usite&said=354&usid=813"
    url_time="http://chifengbowuguan.meishujia.cn/?act=usite&said=360&usid=813"
    #地址和电话和开放时间
    x=get_all(url_time).find(name="dd",attrs={"class":"theme_body_1231159117 theme_body_3728"})
    location=""
    number=""
    # opentime=re.sub("\r|\t|\xa0|\n",'',get_all(url_time).find(name="div",attrs={"class":"kfsj_text"}).text)
    for i in x.find_all(name="tr"):
        if(re.search(re.compile(r'电话:'),i.text)):
            number=re.sub("\r|\t|\xa0|\n",'',i.text)
        if(re.search(re.compile(r'地址:'),i.text)):
            location=re.sub("\r|\t|\xa0|\n",'',i.text)
    print(number+location)
    #展览的简介和图片
    exhibition_hall=[]
    info_exh=get_all(url_1).find(name="dd",attrs={"class":"theme_body_1231159117 theme_body_3751"})
    for i in info_exh.find_all(name="td",attrs={"align":"center","valign":"middle","height":"130"}):
        a={}
        a["name"]=re.sub("\r|\t|\xa0|\n",'',i.find(name="td",attrs={"height":"25","align":"left","valign":"middle"}).text)
        a["img"]=url+i.find(name="td",attrs={"rowspan":"4","width":"80","height":"110","valign":"middle","align":"center"}).a.img["src"]
        url_next=url+i.find(name="td",attrs={"rowspan":"4","width":"80","height":"110","valign":"middle","align":"center"}).a["href"]
        info_next=get_all(url_next).find(name="ul",attrs={"class":"zl_r_b zl_r_bt"})
        a["description"]=re.sub("\r|\t|\xa0|\n",'',info_next.text)
        exhibition_hall.append(a)
        #print(a)
    # print(exhibition_hall)
    #博物馆藏品
    info_projects=get_all(url_2).find(name="dd",attrs={"class":"theme_body_1231159117 theme_body_3705"})
    exhibition_projects=[]
    for i in info_projects.find_all(name="td",attrs={"height":"170","align":"center","valign":"middle"}):
        a={}
        a["img"]=url+i.find(name="td",attrs={"width":"150","height":"130","align":"center","valign":"middle"}).a.img["src"]
        a["name"]=re.sub("\r|\t|\xa0|\n",'',i.find(name="td",attrs={"height":"25","align":"center","valign":"middle"}).text)
        a["description"]=""
        # print(a)
        exhibition_projects.append(a)
    # print(exhibition_projects)

def get_neimenggu_BT_Museum():
    #name="包头博物馆"
    url="http://www.nmgbtbwg.cn/"
    url_time="http://www.nmgbtbwg.cn/html/2015/lianxiwomen_0806/312.html"
    url_1="http://www.nmgbtbwg.cn/html/chenliezhanlan/linshizhanlan/"
    url_2="http://www.nmgbtbwg.cn/html/guancangjingpin/lishiwenwu/"
    url_3="http://www.nmgbtbwg.cn/html/shejiaohuodong/shejiaohuodong/"
    
    #地址和电话和开放时间
    s=re.sub("\r|\t|\xa0|\n",'',get_all(url_time).find(name="div",attrs={"class":"content"}).text)
    location=s[s.index("本"):s.index("号")+1]
    number=s[s.index("电"):]
    # print(location+number)
    
    #展览的简介和图片
    exhibition_hall=[]
    info_exh=get_all(url_1).find(name="ul",attrs={"class":"PicNewsList"})
    for i in info_exh.find_all(name="li",attrs={"class":"PicNewsItem"}):
        a={}
        a["name"]=re.sub("\r|\t|\xa0|\n",'',i.find(name="div",attrs={"class":"PicNewsTxtBox"}).text)
        a["img"]=i.find(name="img")["src"]
        url_next=i.find(name="a")["href"]
        info_next=get_all(url_next).find(name="div",attrs={"class":re.compile(r'ontentBox')})
        a["description"]=re.sub("\r|\t|\xa0|\n",'',info_next.text)
        exhibition_hall.append(a)
        # print(a)
    # print(exhibition_hall)

    #博物馆藏品 没有介绍
    info_projects=get_all(url_2).find(name="ul",attrs={"class":"PicNewsList"})
    exhibition_projects=[]
    for i in info_projects.find_all(name="li",attrs={"class":"PicNewsItem"}):
        a={}
        a["img"]=i.find(name="img")["src"]
        a["name"]=re.sub("\r|\t|\xa0|\n",'',i.find(name="div",attrs={"class":"PicNewsTxtBox"}).text)
        a["description"]=""
        # print(a)
        exhibition_projects.append(a)
    # print(exhibition_projects)
    
    #教育活动 没有图片
    exhibition_edu=[]
    num=0
    info_exh=get_all(url_3).find(name="div",attrs={"class":"ListNewsListBox"})
    for i in info_exh.find_all(name="li",attrs={"class":"ItemLi1"}):
        url_next=i.find(name="span",attrs={"class":"InfoTitle"}).a["href"]
        a={}
        if(re.search(re.compile(r'http://www.nmgbtbwg.cn/'),url_next)):
            if(num<=10):
                a["name"]=re.sub("|\r|\t|\xa0|\n",'',i.find(name="span",attrs={"class":"InfoTitle"}).a.text)
                a["time"]=re.sub("|\r|\t|\xa0|\n",'',i.find(name="span",attrs={"class":"inputtime"}).text)
                info_next=get_all(url_next).find(name="div",attrs={"class":"content"})
                a["img"]=info_next.find(name="img")["src"]
                a["description"]=re.sub(" |\r|\t|\xa0|\n|\u3000",'',info_next.text)
                exhibition_edu.append(a)
                # print(a)
            num+=1
    # print(exhibition_edu)

#辽宁  
#没有展览没有简介 和教育活动
def get_liaoning_Museum():
    #name="辽宁省博物馆"
    #没有获取时间
    url="http://www.lnmuseum.com.cn/"
    url_time="http://www.lnmuseum.com.cn/siliuji/?ChannelID=462"
    url_1="http://www.lnmuseum.com.cn/search/?ChannelID=705"
    url_2="http://www.lnmuseum.com.cn/huxing/?ChannelID=508"
    
    #地址和电话和开放时间
    s=re.sub("\r|\t|\xa0|\n",'',get_all_x(url).find(name="td",attrs={"style":"text-align:center","colspan":"2"}).text)
    location=s[s.index("地"):s.index("电")]
    number=s[s.index("电"):s.index("版")]
    # print(location+number)
    opentime="4月1日至10月31日9:00—17:00（16:00停止入场）11月1日至3月31日9:30—16：30（15:30停止入场）。星期一（国家法定假日除外）闭馆，除夕日闭馆"

    #展览的简介和图片 没有简介
    exhibition_hall=[]
    info_exh=get_all_x(url_1).find(name="td",attrs={"class":"wz1"})
    # print(info_exh)
    num=0
    for i in info_exh.find_all(name="table"):
        if(num<=3):
            a={}
            a["name"]=re.sub("\r|\t|\xa0|\n",'',i.find(name="td",attrs={"width":"470"}).a.text)
            a["img"]=url+i.find(name="img")["src"]
            a["description"]=""
            exhibition_hall.append(a)
            # print(a)
        num+=1
    # print(exhibition_hall)
    #博物馆藏品
    info_projects=get_all_x(url_2).find(name="td",attrs={"class":"wz1"})
    exhibition_projects=[]
    for i in info_projects.find_all(name="td",attrs={"style":"padding:0 10px;"}):
        a={}
        a["img"]=url+i.find(name="img")["src"]
        a["name"]=re.sub("\r|\t|\xa0|\n",'',i.find(name="td",attrs={"class":"donwe1"}).a.text)
        url_next=url+i.find(name="td",attrs={"class":"donwe1"}).a["href"]
        info_next=get_all_x(url_next).find(name="td",attrs={"class":"wz1"})
        a["description"]=""
        for j in info_next.find_all(name="p"):
            a["description"]+=re.sub("\r|\t|\xa0|\n",'',j.text)
        # print(a)
        exhibition_projects.append(a)
    # print(exhibition_projects)
    
def get_liaoning_918_Museum():
    name="九·一八”历史博物馆"
    url="http://www.918museum.org.cn/"
    url_1="http://www.918museum.org.cn/index.php/article/listarticle/pid/194/rel/thumb/sidebar/sidebar"
    url_2="http://www.918museum.org.cn/index.php/article/listarticle/pid/126/rel/thumb/sidebar/sidebar"
    url_3="http://www.918museum.org.cn/index.php/article/listarticle/pid/167/rel/null/sidebar/sidebar"
    url_s="https://baike.sogou.com/v4346248.htm?fromTitle=%E4%B9%9D%C2%B7%E4%B8%80%E5%85%AB%E2%80%9D%E5%8E%86%E5%8F%B2%E5%8D%9A%E7%89%A9%E9%A6%86"
    
    #地址和电话和开放时间
    location="地址：辽宁省沈阳市大东区望花南街46号"
    number="024-88338981"
    # print(location+number)
    opentime="每周一闭馆、每周二至周日开馆。法定节假日和特殊情况除外。夏季： 9：00----17:00（16：30停止入馆）冬季： 9：00----16:30（16：00停止入馆）"
    #展览的简介和图片 没有简介
    exhibition_hall=[]
    info_exh=get_all(url_1).find(name="div",attrs={"class":"mypanel-content row museum"})
    # print(info_exh)
    for i in info_exh.find_all(name="div",attrs={"class":"thumbnail"}):
        a={}            
        a["name"]=re.sub(" |\r|\t|\xa0|\n",'',i.find(name="div",attrs={"class":"caption"}).text)
        url_next=url+i.find(name="a")["href"]
        info_next=get_all(url_next).find(name="div",attrs={"class":"article_content"})
        a["img"]=url+info_next.find(name="img")["src"]
        a["description"]=""
        for j in info_next.find_all(name="p"):
            a["description"]+=re.sub("\r|\t|\xa0|\n",'',j.text)
        exhibition_hall.append(a)
        # print(a)
    # print(exhibition_hall)
    #博物馆藏品
    info_projects=get_all(url_2).find(name="div",attrs={"class":"article row"})
    exhibition_projects=[]
    for i in info_projects.find_all(name="div",attrs={"class":"thumbnail"}):
        a={}            
        a["name"]=re.sub(" |\r|\t|\xa0|\n",'',i.find(name="div",attrs={"class":"caption"}).text)
        url_next=url+i.find(name="a")["href"]
        info_next=get_all(url_next).find(name="div",attrs={"class":"article_content"})
        a["img"]=url+info_next.find(name="img")["src"]
        a["description"]=""
        for j in info_next.find_all(name="p"):
            a["description"]+=re.sub("\r|\t|\xa0|\n",'',j.text)
        exhibition_projects.append(a)
        # print(a)
    # print(exhibition_projects)
    
    #教育活动 
    exhibition_edu=[]
    info_exh=get_all(url_3).find(name="div",attrs={"class":"article row"})
    num=0
    for i in info_exh.find_all(name="li"):
        if(num<=5):
            a={}
            a["name"]=re.sub(" |\r|\t|\xa0|\n",'',i.find(name="span",attrs={"class":"title"}).a.text)
            a["time"]=re.sub(" |\r|\t|\xa0|\n",'',i.find(name="span",attrs={"class":"time"}).text)
            url_next=url+i.find(name="span",attrs={"class":"title"}).a["href"]
            info_next=get_all(url_next).find(name="div",attrs={"class":"article_content"})
            a["img"]=url+info_next.find(name="img")["src"]
            a["description"]=""
            for j in info_next.find_all(name="p"):
                a["description"]+=re.sub("\r|\t|\xa0|\n",'',j.text)
            exhibition_edu.append(a)
            num+=1
            # print(a)
    # print(exhibition_edu)
    info_main={}
    info_main=get_Museum_brefandtime(url,name)
    info_main["name"]=name
    info_main["location"]=location
    info_main["number"]=number
    info_main["opentime"]=opentime
    info_all={}
    info_all["1"]=info_main
    info_all["2"]=exhibition_hall
    info_all["3"]=exhibition_projects
    info_all["4"]=exhibition_edu
    return info_all

def get_liaoning_KMYC_Museum():
    name="抗美援朝纪念馆"
    url="http://www.kmycjng.com/"
    url_1="http://www.kmycjng.com/piccata.aspx?c=C089160A22808BDC"
    url_2="http://www.kmycjng.com/imglist.aspx?c=8973CE298374D3F9"
    url_3="http://www.kmycjng.com/pictxtmore.aspx?c=6E3BA1C922AB0E92"
    url_s="https://baike.sogou.com/v334155.htm?fromTitle=%E6%8A%97%E7%BE%8E%E6%8F%B4%E6%9C%9D%E7%BA%AA%E5%BF%B5%E9%A6%86"
    # get_Museum_brefandtime_new(url_s,name)
    #地址和电话和开放时间
    number="0415-2175988"
    location="辽宁省丹东市振兴区山上街7号"
    #展览的简介和图片 没有简介
    exhibition_hall=[]
    info_exh=get_all(url_1).find(name="div",attrs={"id":"main","class":"clearfix"})
    for i in info_exh.find_all(name="dl",attrs={"class":"picCata"}):
        a={}            
        a["name"]=re.sub(" |\r|\t|\xa0|\n",'',i.find(name="dt",attrs={"class":"tit"}).b.text)
        a["img"]=url+i.find(name="img")["src"]
        a["description"]=""
        exhibition_hall.append(a)
        # print(a)
    # print(exhibition_hall)
    #博物馆藏品
    info_projects=get_all(url_2).find(name="div",attrs={"id":"main","class":"clearfix"})
    exhibition_projects=[]
    for i in info_projects.find_all(name="dl",attrs={"class":"imgList"}):
        a={}            
        a["name"]=re.sub(" |\r|\t|\xa0|\n",'',i.find(name="dt",attrs={"class":"tit"}).a.text)
        a["img"]=url+i.find(name="img")["src"]
        a["description"]=""
        exhibition_projects.append(a)
        # print(a)
    # print(exhibition_projects)
    #教育活动 
    exhibition_edu=[]
    info_exh=get_all(url_3).find(name="div",attrs={"id":"main","class":"clearfix"})
    num=0
    for i in info_exh.find_all(name="dl",attrs={"class":"picTxtMore"}):
        a={}         
        a["name"]=re.sub(" |\r|\t|\xa0|\n",'',i.find(name="dt",attrs={"class":"tit"}).a.text)
        a["img"]=url+i.find(name="img")["src"]
        url_next=url+i.find(name="dt",attrs={"class":"tit"}).a["href"]
        info_next=get_all(url_next).find(name="div",attrs={"class":"infocontent"})
        s=re.sub(" |\r|\t|\xa0|\n",'',info_next.text)
        a["time"]=s[:s.index("日")+1]
        a["description"]=s[s.index("日")+1:]
        # print(a)
    # print(exhibition_edu)
    info_main={}
    info_main=get_Museum_brefandtime_new(url_s,name)
    info_main["name"]=name
    info_main["location"]=location
    info_main["number"]=number
    info_all={}
    info_all["1"]=info_main
    info_all["2"]=exhibition_hall
    info_all["3"]=exhibition_projects
    info_all["4"]=exhibition_edu
    return info_all

def get_liaoning_LS_Museum():
    #name="旅顺博物馆"
    url="http://www.lvshunmuseum.org/"
    url_1="http://www.lvshunmuseum.org/Exhibition/?SortID=3"
    url_2="http://www.lvshunmuseum.org/collection/product.aspx?SortID=9"
    url_3="http://www.lvshunmuseum.org/EducationBBS/"
    #没有获取时间
    url_s="https://baike.sogou.com/v99521.htm?fromTitle=%E6%97%85%E9%A1%BA%E5%8D%9A%E7%89%A9%E9%A6%86"
    #地址和电话和开放时间
    s=re.sub(" |\r|\t|\xa0|\n",'',get_all(url).find(name="div",attrs={"class":"guide"}).text)
    number="电话:0411-86383334"
    location=s[s.index("地"):]
    opentime=s[s.index("开"):s.index("知")+1]
    # print(location+number+opentime)
    #展览的简介和图片
    exhibition_hall=[]
    info_exh=get_all(url_1).find(name="ul",attrs={"class":"showcase_list"})
    # print(info_exh)
    for i in info_exh.find_all(name="li"):
        a={}            
        a["name"]=re.sub(" |\r|\t|\xa0|\n",'',i.find(name="div",attrs={"class":"textbox"}).h1.text)
        a["img"]=url+re.sub(" ",'',i.find(name="img")["src"])
        url_next=url+re.sub(" ",'',i.find(name="a")["href"])
        info_next=get_all(url_next).find(name="div",attrs={"class":"textshow"})
        a["description"]=re.sub("\r|\t|\xa0|\n",'',info_next.text)
        exhibition_hall.append(a)
        # print(a)
    # print(exhibition_hall)
    #博物馆藏品
    info_projects=get_all(url_2).find(name="ul",attrs={"class":"showcase_list"})
    exhibition_projects=[]
    for i in info_projects.find_all(name="li"):
        a={}            
        a["name"]=re.sub(" |\r|\t|\xa0|\n",'',i.find(name="div",attrs={"class":"textbox textbox2"}).h1.text)
        a["img"]=url+re.sub(" ",'',i.find(name="img")["src"])
        url_next=url+re.sub(" ",'',i.find(name="a")["href"])
        info_next=get_all(url_next).find(name="div",attrs={"class":"textshow"})
        a["description"]=re.sub("\r|\t|\xa0|\n",'',info_next.text)
        exhibition_projects.append(a)
        # print(a)
    # print(exhibition_projects)
    #教育活动 
    exhibition_edu=[]
    info_exh=get_all(url_3).find(name="ul",attrs={"class":"newslist1"})
    num=0
    for i in info_exh.find_all(name="li"):
        if(num<=2):
            a={}
            a["name"]=re.sub(" |\r|\t|\xa0|\n",'',i.find(name="div",attrs={"class":"newstitle"}).h1.text)
            a["time"]=re.sub(" |\r|\t|\xa0|\n",'',i.find(name="span",attrs={"class":"date"}).text)
            url_next=url+re.sub(" ",'',i.find(name="a")["href"])
            info_next=get_all(url_next).find(name="div",attrs={"class":"newsdetail_content"})
            a["img"]=info_next.find(name="img")["src"]
            a["description"]=""
            for j in info_next.find_all(name="p"):
                a["description"]+=re.sub("\r|\t|\xa0|\n",'',j.text)
            exhibition_edu.append(a)
            # print(a)
            num+=1
    # print(exhibition_edu)
    info_main={}
    info_main=get_Museum_brefandtime_new(url_s,name)
    info_main["name"]=name
    info_main["location"]=location
    info_main["number"]=number
    info_main["opentime"]=opentime
    info_all={}
    info_all["1"]=info_main
    info_all["2"]=exhibition_hall
    info_all["3"]=exhibition_projects
    info_all["4"]=exhibition_edu
    return info_all
    
def get_liaoning_DLXD_Museum():
    name="大连现代博物馆"
    url="https://www.dlmodernmuseum.com/"
    url_1="https://www.dlmodernmuseum.com/exhibition/review/"
    url_2="https://www.dlmodernmuseum.com/collection/"
    url_3="https://www.dlmodernmuseum.com/activity/" 
    url_s="https://baike.sogou.com/v163555.htm?fromTitle=%E5%A4%A7%E8%BF%9E%E7%8E%B0%E4%BB%A3%E5%8D%9A%E7%89%A9%E9%A6%86"
    number="0411-84801025"
    #地址和电话和开放时间
    number="电话:0411-86383334"
    location="辽宁省大连市沙河口区会展路10号"
    # print(location+number+opentime)
    #展览的简介和图片
    exhibition_hall=[]
    info_exh=get_all(url_1).find(name="div",attrs={"class":"showlist contrightlist"})
    # print(info_exh)
    for i in info_exh.find_all(name="li"):
        a={}            
        a["name"]=re.sub(" |\r|\t|\xa0|\n",'',i.find(name="div",attrs={"class":"showtitle"}).h1.text)
        a["img"]=url+re.sub(" ",'',i.find(name="img")["src"])
        url_next=i.find(name="a")["href"]
        info_next=get_all(url_next).find(name="div",attrs={"class":"showlist contrightlist"})
        a["description"]=""
        for j in info_next.find_all(name="p"):
            a["description"]+=re.sub("\r|\t|\xa0|\n",'',j.text)
        exhibition_hall.append(a)
        # print(a)
    # print(exhibition_hall)
    #博物馆藏品
    info_projects=get_all(url_2).find(name="div",attrs={"class":"showlist contrightlist"})
    exhibition_projects=[]
    for i in info_projects.find_all(name="li"):
        a={}            
        a["name"]=re.sub(" |\r|\t|\xa0|\n",'',i.find(name="div",attrs={"class":"showtitle2"}).text)
        a["img"]=url+re.sub(" ",'',i.find(name="img")["src"])
        url_next=i.find(name="a")["href"]
        info_next=get_all(url_next).find(name="div",attrs={"class":"showlist contrightlist"})
        a["description"]=""
        for j in info_next.find_all(name="p"):
            a["description"]+=re.sub("\r|\t|\xa0|\n",'',j.text)
        exhibition_projects.append(a)
        # print(a)
    # print(exhibition_projects)
    #教育活动 
    exhibition_edu=[]
    info_exh=get_all(url_3).find(name="div",attrs={"class":"infolist contrightlist"})
    num=0
    for i in info_exh.find_all(name="li"):
        if(num<=9):
            a={}
            a["name"]=re.sub(" |\r|\t|\xa0|\n",'',i.find(name="a").text)
            a["time"]=re.sub(" |\r|\t|\xa0|\n",'',i.find(name="span").text)
            url_next=i.find(name="a")["href"]
            info_next=get_all(url_next).find(name="div",attrs={"class":"showlist contrightlist"})
            a["img"]=info_next.find(name="img")["src"]
            a["description"]=""
            for j in info_next.find_all(name="p"):
                a["description"]+=re.sub("\r|\t|\xa0|\n",'',j.text)
            exhibition_edu.append(a)
            # print(a)
            num+=1
    # print(exhibition_edu)
    info_main={}
    info_main=get_Museum_brefandtime_new(url_s,name)
    info_main["name"]=name
    info_main["location"]=location
    info_main["number"]=number
    info_main["opentime"]=opentime
    info_all={}
    info_all["1"]=info_main
    info_all["2"]=exhibition_hall
    info_all["3"]=exhibition_projects
    info_all["4"]=exhibition_edu
    return info_all

def get_liaoning_GG_Museum():
    name="沈阳故宫博物院"
    url="http://www.sypm.org.cn/"
    url_1="http://www.sypm.org.cn/products_list2/pmcId=54.html"
    url_2="http://www.sypm.org.cn/products_list3/pmcId=77.html"
    url_3="http://www.sypm.org.cn/news_list3/&newsCategoryId=71&comp_stats=comp-FrontNewsCategory_tree01-shjy.html"
    url_s="https://baike.sogou.com/v64312764.htm?fromTitle=%E6%B2%88%E9%98%B3%E6%95%85%E5%AE%AB%E5%8D%9A%E7%89%A9%E9%99%A2"
    #get_Museum_brefandtime(url_s,name)
    #地址和电话和开放时间
    s=re.sub(" |\r|\t|\xa0|\n",'',get_all(url_1).find(name="div",attrs={"id":"box_footer"}).text)
    number=s[s.index("咨"):s.index("投")]
    location=s[s.index("地"):s.index("号")+1]
    # print(location+number)
    #展览的简介和图片
    exhibition_hall=[]
    info_exh=get_all(url_1).find(name="div",attrs={"id":"box_left_sub3_tem_cplb3"})
    # print(info_exh)
    for i in info_exh.find_all(name="li",attrs={"class":"content column-num4"}):
        a={}            
        a["name"]=re.sub(" |\r|\t|\xa0|\n",'',i.find(name="li",attrs={"class":"code"}).strong.text)
        a["img"]=url+i.find(name="img")["src"]
        url_next=url+i.find(name="a")["href"]
        info_next=get_all(url_next).find(name="div",attrs={"class":"FrontProducts_detail02-0011_htmlbreak"})
        a["description"]=re.sub("\r|\t|\xa0|\n",'',info_next.text)
        exhibition_hall.append(a)
        # print(a)
    print(exhibition_hall)
    #博物馆藏品
    info_projects=get_all(url_2).find(name="div",attrs={"id":"box_left_sub3_tem_cplb3"})
    exhibition_projects=[]
    for i in info_projects.find_all(name="li",attrs={"class":"content column-num4"}):
        a={}            
        a["name"]=re.sub(" |\r|\t|\xa0|\n",'',i.find(name="li",attrs={"class":"code"}).strong.text)
        a["img"]=url+i.find(name="img")["src"]
        url_next=url+re.sub(" ",'',i.find(name="a")["href"])
        info_next=get_all(url_next).find(name="div",attrs={"class":"describe htmledit showtabdiv","id":"FrontProducts_detail02-0012_description"})
        a["description"]=re.sub("\r|\t|\xa0|\n",'',info_next.text)
        exhibition_projects.append(a)
        # print(a)
    print(exhibition_projects)
    #教育活动 
    exhibition_edu=[]
    info_exh=get_all(url_3).find(name="ul",attrs={"class":"comstyle newslist-01"})
    for i in info_exh.find_all(name="li",attrs={"class":"content column-num1"}):
        a={}
        a["name"]=re.sub(" |\r|\t|\xa0|\n",'',i.find(name="li",attrs={"class":"title"}).h3.text)
        a["time"]=re.sub(" |\r|\t|\xa0|\n",'',i.find(name="li",attrs={"class":"date"}).text)
        url_next=url+i.find(name="a")["href"]
        info_next=get_all(url_next).find(name="div",attrs={"class":"describe htmledit","id":"infoContent"})
        a["img"]=info_next.find(name="img")["src"]
        a["description"]=re.sub("\r|\t|\xa0|\n",'',info_next.text)
        exhibition_edu.append(a)
        # print(a)
    print(exhibition_edu)
    info_main={}
    info_main=get_Museum_brefandtime(url_s,name)
    info_main["name"]=name
    info_main["location"]=location
    info_main["number"]=number
    info_all={}
    info_all["1"]=info_main
    info_all["2"]=exhibition_hall
    info_all["3"]=exhibition_projects
    info_all["4"]=exhibition_edu
    # return info_all


get_liaoning_GG_Museum()