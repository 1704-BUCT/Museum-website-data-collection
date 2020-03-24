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
#print(type(test1)) 

n=0  #统计数量
for i in test1:
    #从网页中找链接
    childnet=requests.get(url+i['href'])
    childnet.encoding='utf-8'
    childsoup=BeautifulSoup(childnet.text,"html.parser")
    #找到有这个字样的后缀
    childtest=childsoup.find_all(name='a',attrs={'href':re.compile(r'^/a/quanguobowuguan/')})
    #print(childtest)
    for childi in childtest:
        if (childi['href']!="/a/quanguobowuguan/"):
            #print(childi['href'])
            next_childnet=requests.get(url+childi['href'])
            next_childnet.encoding='utf-8'
            next_childsoup=BeautifulSoup(next_childnet.text,"html.parser")
            next_childtest=next_childsoup.find_all(name='p')
            for finali in next_childtest:
                temp=finali.get_text()
                matchObj = re.match( r'网址', temp, re.M)
                if matchObj:
                    print(temp)
                    n=n+1
print(n)