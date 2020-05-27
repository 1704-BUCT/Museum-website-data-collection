import requests
import re
import bs4
from bs4 import BeautifulSoup
import bs4
headers ={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0'
    }
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

def visit(url):
    soup = get_soup(url)
    foot = soup.find('div',attrs={'id':'foot_wz'})
    print(foot.text)

def show(url):
    home = "http://www.kfsbwg.com"
    soup = get_soup(url)
    div = soup.find('div',attrs={'style':'margin-right:10px;'})
    p = div.find_all('p')
    main = ""
    for tag in p:
        main = main+tag.text
    print(main)
    img = div.find_all("img")
    i = 0
    for tag in img:
        i = i+1
        src = home+tag["src"]
        print("展览图示:"+src)
        if i ==3:
            break

def object(url):
    home = "http://www.kfsbwg.com"
    soup = get_soup(url)
    div = soup.find('div',attrs={'class':'show'})
    p = div.find_all('p')
    main = ""
    for tag in p:
        main = main+tag.text
    print(main)
    img = div.find_all("img")
    i = 0
    for tag in img:
        i = i+1
        src = home+tag["src"]
        print("藏品图片:"+src)
        if i ==2:
            break

def education(url):
    home = "http://www.kfsbwg.com"
    soup = get_soup(url)
    r = soup.find('div',attrs={'class':'r'})
    title = r.find('h4',attrs={'class':'show_b'})
    print(title.text)
    div = soup.find('div',attrs={'class':'show'})
    p = div.find_all('p')
    main = ""
    for tag in p:
        main = main+tag.text
    print(main)
    img = div.find_all("img")
    i = 0
    for tag in img:
        i = i+1
        src = home+tag["src"]
        print("活动写照:"+src)
        if i ==2:
            break


url = "https://baike.sogou.com/v5891944.htm?fromTitle=%E5%BC%80%E5%B0%81%E5%B8%82%E5%8D%9A%E7%89%A9%E9%A6%86"
get_brief(url)

url = "http://www.kfsbwg.com/"
visit(url)

print("------展览陈列------")
url = "http://www.kfsbwg.com/html/2020/jbcl_0309/549.html"
show(url)
print("\n")
url = "http://www.kfsbwg.com/html/2016/jbcl_0802/18.html"
show(url)
print("\n")
url = "http://www.kfsbwg.com/html/2016/jbcl_0801/16.html"
show(url)
print("\n")

print("------典藏珍品------")
url = "http://www.kfsbwg.com/html/2016/shuhua_0815/113.html"
object(url)
print("\n")
url = "http://www.kfsbwg.com/html/2016/yuqi_0815/108.html"
object(url)
print("\n")
url = "http://www.kfsbwg.com/html/2016/yuqi_0815/107.html"
object(url)
print("\n")
url = "http://www.kfsbwg.com/html/2016/taoci_0815/100.html"
object(url)
print("\n")
url = "http://www.kfsbwg.com/html/2016/zaxiang_0815/116.html"
object(url)
print("\n")


print("------教育活动------")
url = "http://www.kfsbwg.com/html/2019/xueshu_0121/278.html"
education(url)
print("\n")
url = "http://www.kfsbwg.com/html/2016/hdhg_1021/148.html"
education(url)
print("\n")
url = "http://www.kfsbwg.com/html/2017/hdhg_0531/175.html"
education(url)
print("\n")

