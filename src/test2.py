import requests,urllib,urllib3
import bs4
import re
from bs4 import BeautifulSoup
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
}
#匹配年
pattern_year = re.compile(r'\b\d{4}年\d{1,2}月\d{1,2}日\b|\b\d{4}年\d{1,2}月\b|\b\d{4}年\b')
#匹配时间
pattern_time = re.compile(r'\d{1,2}:\d{2}|\d{1,2}：\d{2}')
#找简介和时间的函数
def get_Museum_brefandtime(url,name):
    #信息变量名
    bref=""
    opentime=""
    establishtime=""
    main_image_url=""
    #整体的爬取 搜狗百科
    res=requests.get(url,headers=headers)
    soup=BeautifulSoup(res.text,"html.parser")
    info_bref_temp=soup.find(name="div",attrs={'class':"abstract"})
    info_time_temp=soup.find_all(name="div",attrs={'class':"base-info-card-value"})
    info_images_temp=soup.find_all(name="img",attrs={'src':re.compile(r'^http')})
    for i in info_images_temp:
        main_image_url=i["src"]
    #存储图片
    # file_name="C:\\Study\\work\\Museum-website-data-collection\\images\\"
    # file_name=file_name+name+"\\main.jpg"
    # get_image(main_image_url,file_name)
    # print(info_bref.p)
    
    info_bref=info_bref_temp.find_all(name="p")
    
    for i in info_bref:
        bref+=i.get_text()
    bref=re.sub(' ','',bref)
    bref=re.sub(r'\[\d\]','',bref)
    #找开馆时间
    for i in info_time_temp:
        if(re.search( pattern_time,i.get_text())):
            a=0
            s=i.get_text()
            for j in s:
                if(j==' '):
                    break
                a+=1
            opentime=s[0:a]
    #找建立时间
    for i in info_time_temp:
        if(re.search( pattern_year,i.get_text())):
            a=0
            s=i.get_text()
            for j in s:
                if(j==' '):
                    break
                a+=1
            establishtime=s[0:a]
    # print("简介：\n",bref)
    # print("建馆时间：\n",establishtime)
    # print("开放时间：\n",opentime)
    aa={}
    aa["bref"]=bref
    aa["main_image_url"]=main_image_url
    aa["opentime"]=opentime
    print(aa)
#因为格式不同而做的修改
def get_Museum_brefandtime_new(url,name):

    bref=""
    opentime=""
    establishtime=""  
    main_image_url=""

    res=requests.get(url,headers=headers)
    soup=BeautifulSoup(res.text,"html.parser")
    info_bref_temp=soup.find(name="div",attrs={'class':"abstract"})
    info_time_temp=soup.find_all(name="div",attrs={'class':"base-info-card-value"})
    info_images_temp=soup.find_all(name="img",attrs={'src':re.compile(r'^http')})
    for i in info_images_temp:
        main_image_url=i["src"]
    #存储图片
    # file_name="C:\\Study\\work\\Museum-website-data-collection\\images\\"
    # file_name=file_name+name+"\\main.jpg"
    # get_image(main_image_url,file_name)
    #简介
    s=info_bref_temp.get_text()
    s=re.sub(" ",'',s)
    bref=re.sub(r'\[\d\]','',s)
    #找开馆时间
    for i in info_time_temp:
        #注意search和match函数的不同
        if(re.search( pattern_time,i.get_text())):
            a=0
            s=i.get_text()
            for j in s:
                if(j==' '):
                    break
                a+=1
            opentime=s[0:a]
    #找建立时间
    for i in info_time_temp:
        if(re.match( pattern_year,i.get_text())):
            a=0
            s=i.get_text()
            for j in s:
                if(j==' '):
                    break
                a+=1
            establishtime=s[0:a]
    # print("简介：\n",bref)
    #print("建馆时间：\n",establishtime)
    # print("开放时间：\n",opentime)
    aa={}
    aa["bref"]=bref
    aa["main_image_url"]=main_image_url
    aa["opentime"]=opentime
    print(aa)
#下载图片 文件名 url
def get_image(url,file_name):
    try:
        content = requests.get(url, headers=headers).content
        with open(file_name, "wb") as f:
            f.write(content)
        print('图片下载成功')
    except Exception as result:
        print('图片下载失败'+str(result))
#北京
def get_beijing_GG_Museum():
    url="https://baike.sogou.com/v128433719.htm?fromTitle=%E6%95%85%E5%AE%AB%E5%8D%9A%E7%89%A9%E9%99%A2"
    name="故宫博物院"
    get_Museum_brefandtime(url,name)
def get_beijing_ScienceandTechnology_Museum():
    url="https://baike.sogou.com/v154146.htm?fromTitle=%E4%B8%AD%E5%9B%BD%E7%A7%91%E5%AD%A6%E6%8A%80%E6%9C%AF%E9%A6%86"
    name="中国科学技术馆"
    url_1="http://cstm.cdstm.cn/"
    
    get_Museum_brefandtime(url,name)
def get_beijing_dizhi_Museum():
    name="中国地质博物馆"
    url_s="https://baike.sogou.com/v154352.htm?fromTitle=%E4%B8%AD%E5%9B%BD%E5%9C%B0%E8%B4%A8%E5%8D%9A%E7%89%A9%E9%A6%86"
    #这个博物馆格式不同要重新写爬取方法
    get_Museum_brefandtime_new(url_s,name)
def get_beijing_Military_Museum():
    url_s="https://baike.sogou.com/v154160.htm?fromTitle=%E4%B8%AD%E5%9B%BD%E4%BA%BA%E6%B0%91%E9%9D%A9%E5%91%BD%E5%86%9B%E4%BA%8B%E5%8D%9A%E7%89%A9%E9%A6%86"
    name="中国人民革命军事博物馆"
    get_Museum_brefandtime(url_s,name)
def get_beijing_Aviation_Museum():
    url="https://baike.sogou.com/v154394.htm?fromTitle=%E4%B8%AD%E5%9B%BD%E8%88%AA%E7%A9%BA%E5%8D%9A%E7%89%A9%E9%A6%86"
    name="中国航空博物馆"
    get_Museum_brefandtime(url,name)
def get_beijing_LuXun_Museum():
    url_s="https://baike.sogou.com/v154258.htm?fromTitle=%E5%8C%97%E4%BA%AC%E9%B2%81%E8%BF%85%E5%8D%9A%E7%89%A9%E9%A6%86"
    name="北京鲁迅博物馆"
    # 这个博物馆也不一样 还要再改改
    get_Museum_brefandtime_new(url_s,name)
def get_beijing_Capital_Museum():
    url_s="https://baike.sogou.com/v3829772.htm?fromTitle=%E9%A6%96%E9%83%BD%E5%8D%9A%E7%89%A9%E9%A6%86"
    name="首都博物馆"
    #这个开放时间格式也不一样 通过search解决
    get_Museum_brefandtime(url_s,name)
def get_beijing_Nature_Museun():
    url_s="https://baike.sogou.com/v154178.htm?fromTitle=%E5%8C%97%E4%BA%AC%E8%87%AA%E7%84%B6%E5%8D%9A%E7%89%A9%E9%A6%86"
    name="北京自然博物馆"
    #这个问题和鲁迅博物馆一样
    get_Museum_brefandtime(url_s,name)
def get_beijing_KRZZ_Museum():
    url="https://baike.sogou.com/v162942.htm?fromTitle=%E4%B8%AD%E5%9B%BD%E4%BA%BA%E6%B0%91%E6%8A%97%E6%97%A5%E6%88%98%E4%BA%89%E7%BA%AA%E5%BF%B5%E9%A6%86"
    name="中国人民抗日战争纪念馆"
    get_Museum_brefandtime(url,name)

def get_beijing_Planet_Museum():
    url="https://baike.sogou.com/v154404.htm?fromTitle=%E5%8C%97%E4%BA%AC%E5%A4%A9%E6%96%87%E9%A6%86"
    name="北京天文馆"
    get_Museum_brefandtime(url,name)

def get_beijing_ZKDYR_Museum():
    url_s="https://baike.sogou.com/v609824.htm?fromTitle=%E5%91%A8%E5%8F%A3%E5%BA%97%E9%81%97%E5%9D%80%E5%8D%9A%E7%89%A9%E9%A6%86"
    name="周口店猿人遗址博物馆"

    #这个问题和鲁迅博物馆一样
    get_Museum_brefandtime_new(url_s,name)
def get_beijing_Country_Museum():
    url="https://baike.sogou.com/v238096.htm?fromTitle=%E4%B8%AD%E5%9B%BD%E5%9B%BD%E5%AE%B6%E5%8D%9A%E7%89%A9%E9%A6%86"
    name="中国国家博物馆"
    get_Museum_brefandtime(url,name)

def get_beijing_Agrituel_Museum():
    url_s="https://baike.sogou.com/v163062.htm?fromTitle=%E4%B8%AD%E5%9B%BD%E5%86%9C%E4%B8%9A%E5%8D%9A%E7%89%A9%E9%A6%86"
    name="中国农业博物馆"
    get_Museum_brefandtime(url_s,name)

#天津
def get_tianjin_Museum():
    url_s="https://baike.sogou.com/v163086.htm?fromTitle=%E5%A4%A9%E6%B4%A5%E5%8D%9A%E7%89%A9%E9%A6%86"
    name="天津博物馆"
    get_Museum_brefandtime(url_s,name)
    
def get_tianjin_Nature_Museum():
    url_s="https://baike.sogou.com/v1492460.htm?fromTitle=%E5%A4%A9%E6%B4%A5%E8%87%AA%E7%84%B6%E5%8D%9A%E7%89%A9%E9%A6%86"
    name="天津自然博物馆"
    get_Museum_brefandtime(url_s,name)
def get_tianjin_ZNLDYC_Museum():
    url="https://baike.sogou.com/v45887982.htm?fromTitle=%E5%91%A8%E6%81%A9%E6%9D%A5%E9%82%93%E9%A2%96%E8%B6%85%E7%BA%AA%E5%BF%B5%E9%A6%86"
    name="周恩来邓颖超纪念馆"
    get_Museum_brefandtime(url,name)
def get_tianjin_Art_Museum():
    url_s="https://baike.sogou.com/v1492460.htm?fromTitle=%E5%A4%A9%E6%B4%A5%E8%87%AA%E7%84%B6%E5%8D%9A%E7%89%A9%E9%A6%86"
    name="天津美术馆"
    get_Museum_brefandtime(url_s,name)
#河北
def get_hebei_Museum():
    name="河北博物院"
    #这个时间没有
    url_s="https://baike.sogou.com/v75752700.htm?fromTitle=%E6%B2%B3%E5%8C%97%E5%8D%9A%E7%89%A9%E9%99%A2"
    get_Museum_brefandtime(url_s,name)

   #这个博物馆啥也没有算了 
def get_hebei_XBP_Museum():
    url="https://baike.sogou.com/v204552.htm?fromTitle=%E8%A5%BF%E6%9F%8F%E5%9D%A1%E7%BA%AA%E5%BF%B5%E9%A6%86"
    #name="西柏坡纪念馆"
    #这个时间没有
    get_Museum_brefandtime_new(url)

def get_hebei_SJZ_Museum():
    url_s="https://baike.sogou.com/v5189145.htm?fromTitle=%E7%9F%B3%E5%AE%B6%E5%BA%84%E5%B8%82%E5%8D%9A%E7%89%A9%E9%A6%86"
    name="石家庄市博物馆"
    get_Museum_brefandtime_new(url_s,name)
def get_hebei_ZJK_Museum():
    url_s="https://baike.sogou.com/v51113247.htm?fromTitle=%E5%BC%A0%E5%AE%B6%E5%8F%A3%E5%8D%9A%E7%89%A9%E9%A6%86"
    name="张家口博物馆"
    #没有开馆时间
    get_Museum_brefandtime_new(url_s,name)
def get_hebei_HD_Museum():
    url_s="https://baike.sogou.com/v361975.htm?fromTitle=%E9%82%AF%E9%83%B8%E5%B8%82%E5%8D%9A%E7%89%A9%E9%A6%86"
    name="邯郸市博物馆"
    get_Museum_brefandtime(url_s,name)
#山西
def get_shanxi_Museum():
    name="山西博物院"
    url_s="https://baike.sogou.com/v8819218.htm?fromTitle=%E5%B1%B1%E8%A5%BF%E5%8D%9A%E7%89%A9%E9%99%A2"
    get_Museum_brefandtime(url_s,name)
def get_shanxi_MT_Museum():
    name="中国煤炭博物馆"
    url_s="https://baike.sogou.com/v163171.htm?fromTitle=%E4%B8%AD%E5%9B%BD%E7%85%A4%E7%82%AD%E5%8D%9A%E7%89%A9%E9%A6%86"
    get_Museum_brefandtime(url_s,name)
#这个怕不下来
def get_shanxi_BLJTH_Museum():
    #name="八路军太行纪念馆"
    url="https://baike.sogou.com/v75873440.htm?fromTitle=%E5%85%AB%E8%B7%AF%E5%86%9B%E5%A4%AA%E8%A1%8C%E7%BA%AA%E5%BF%B5%E9%A6%86"
    get_Museum_brefandtime(url)
#内蒙古
def get_neimenggu_Museum():
    name="内蒙古博物院"
    url_s="https://baike.sogou.com/v7115658.htm?fromTitle=%E5%86%85%E8%92%99%E5%8F%A4%E5%8D%9A%E7%89%A9%E9%99%A2"
    get_Museum_brefandtime(url_s,name)

def get_neimenggu_ERDS_Museum():
    #name="鄂尔多斯博物馆"
    #没有获取时间
    url="https://baike.sogou.com/v41309396.htm?fromTitle=%E9%84%82%E5%B0%94%E5%A4%9A%E6%96%AF%E5%8D%9A%E7%89%A9%E9%A6%86"
    get_Museum_brefandtime(url)

def get_neimenggu_CF_Museum():
    name="赤峰博物馆"
    url_s="https://baike.sogou.com/v10572874.htm?fromTitle=%E8%B5%A4%E5%B3%B0%E5%8D%9A%E7%89%A9%E9%A6%86"
    get_Museum_brefandtime(url_s,name)

def get_neimenggu_BT_Museum():
    name="包头博物馆"
    url_s="https://baike.sogou.com/v163748.htm?fromTitle=%E5%86%85%E8%92%99%E5%8F%A4%E5%8C%85%E5%A4%B4%E5%8D%9A%E7%89%A9%E9%A6%86"
    get_Museum_brefandtime(url_s,name)

#辽宁
def get_liaoning_Museum():
    #name="辽宁省博物馆"
    #没有获取时间
    url_s="https://baike.sogou.com/v99329.htm?fromTitle=%E8%BE%BD%E5%AE%81%E7%9C%81%E5%8D%9A%E7%89%A9%E9%A6%86"
    get_Museum_brefandtime_new(url_s,name)
def get_liaoning_918_Museum():
    name="九·一八”历史博物馆"
    url_s="https://baike.sogou.com/v4346248.htm?fromTitle=%E4%B9%9D%C2%B7%E4%B8%80%E5%85%AB%E2%80%9D%E5%8E%86%E5%8F%B2%E5%8D%9A%E7%89%A9%E9%A6%86"
    get_Museum_brefandtime(url_s,name)

def get_liaoning_KMYC_Museum():
    #name="抗美援朝纪念馆"
    url_s="https://baike.sogou.com/v334155.htm?fromTitle=%E6%8A%97%E7%BE%8E%E6%8F%B4%E6%9C%9D%E7%BA%AA%E5%BF%B5%E9%A6%86"
    get_Museum_brefandtime_new(url_s,name)
def get_liaoning_LS_Museum():
    name="旅顺博物馆"
    #没有获取时间
    url_s="https://baike.sogou.com/v99521.htm?fromTitle=%E6%97%85%E9%A1%BA%E5%8D%9A%E7%89%A9%E9%A6%86"
    get_Museum_brefandtime_new(url_s,name)
def get_liaoning_DLXD_Museum():
    #name="大连现代博物馆"
    url="https://baike.sogou.com/v163555.htm?fromTitle=%E5%A4%A7%E8%BF%9E%E7%8E%B0%E4%BB%A3%E5%8D%9A%E7%89%A9%E9%A6%86"
    get_Museum_brefandtime_new(url,name)
def get_liaoning_GG_Museum():
    #name="沈阳故宫博物院"
    url="https://baike.sogou.com/v64312764.htm?fromTitle=%E6%B2%88%E9%98%B3%E6%95%85%E5%AE%AB%E5%8D%9A%E7%89%A9%E9%99%A2"
    res=requests.get(url,headers=headers)
    soup=BeautifulSoup(res.text,"html.parser")
    #get_Museum_brefandtime(url)


get_hebei_SJZ_Museum()
get_hebei_ZJK_Museum()