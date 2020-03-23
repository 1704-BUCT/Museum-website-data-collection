import requests
import bs4
import re
from bs4 import BeautifulSoup
#总网址url
url='http://www.chinamuseum.org.cn'
#网站后缀1先通过这个网站链接到所有
backline_1='/plus/list.php?tid=110'
res=requests.get(url+backline_1)
res.encoding='utf-8'
soup=BeautifulSoup(res.text,"html.parser")

test1=soup.dd.find_all(name='a',attrs={'href':re.compile(r'^/plus/list.php')})
print(type(test1))
for i in test1:
    print(i['href'])

