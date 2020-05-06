import requests
import re
import bs4
from bs4 import BeautifulSoup
import bs4

headers = {
     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'    
}
def get_all(url): #提取soup
    re=requests.get(url,headers=headers)
    re.encoding='utf-8'
    soup = BeautifulSoup(re.text, 'html.parser')
    return soup

def get_image(url,file_name): #典藏图片
    try:
        content = requests.get(url, headers=headers).content
        with open(file_name, "wb") as f:
            f.write(content)
        print('图片下载成功')
    except Exception as result:
        print('图片下载失败'+str(result))

def get_education(soup,temp): #教育活动
    education = soup.find('div',attrs={'class':'subBody'})
    title = education.find('div',attrs={'class':'listConts'})
    p = title.find_all('p',class_ ='MsoNormal')
    for tag in p:
        temp = temp+tag.text.strip()
    print(temp)

url = "https://baike.sogou.com/v6815002.htm?fromTitle=%E4%BA%95%E5%86%88%E5%B1%B1%E9%9D%A9%E5%91%BD%E5%8D%9A%E7%89%A9%E9%A6%86"
soup = get_all(url)
print("------井冈山博物馆简介------")
brief = soup.find(attrs = {"name":"description"})['content']
print(brief)
print("------参观信息------")
visit = soup.find('table',class_ = 'abstract_tbl')
info = visit.find_all('tr')
for tag in info:
    title = tag.find('th',class_ = 'base-info-card-title')
    print(title.text+":",end="")
    texts = tag.find('div',class_ = 'base-info-card-value').find(text=True).strip()
    print(texts)
url = "http://www.jgsgmbwg.com"
soup = get_all(url)
visited = soup.find('p',attrs={'style':'border-bottom: 1px solid #302B2B; padding-bottom:40px;'})
print(visited.text.lstrip())

#爬取展品简介和图片链接
url_1="http://www.jgsgmbwg.com/"
url="http://www.jgsgmbwg.com/newsshow.php?cid=71&id=6710"
print("------典藏珍品------")
x=get_all(url).find(name="div",attrs={'class':'listConts'})
p = x.find_all('span',attrs={'style':'color:#000000;font-family:SimSun;font-size:16px;'})
object = ""
for tag in p:
    object = object+tag.text
print(object)
y=x.find_all_next(name="img")
num=0
for i in y:
    url=url_1+i["src"]
    print(url)
    #file_name=file_name+str(num)+".jpg"
    #get_image(url,file_name)
    num=num+1
#教育活动
print("-----教育活动------")
url = "http://www.jgsgmbwg.com/newsshow.php?cid=72&id=5600"
temp = "-----井冈山革命博物馆旧居旧址办党支部召开党的群众路线教育实践活动总结会-----\n"
soup = get_all(url)
get_education(soup,temp)

url = "http://www.jgsgmbwg.com/newsshow.php?cid=72&id=5586"
soup = get_all(url)
temp = "-----井冈山革命博物馆召开党的群众路线教育实践活动总结大会-----\n"
get_education(soup,temp)

url = "http://www.jgsgmbwg.com/newsshow.php?cid=72&id=5573"
temp = "学习伟人风范 践行群众路线\n"
soup = get_all(url)
get_education(soup,temp)