import requests
import bs4
import re
from bs4 import BeautifulSoup
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
}
def get_all(url):
    re=requests.get(url,headers=headers)
    re.encoding='utf-8'
    soup = BeautifulSoup(re.text, 'html.parser')
    return soup

def get_image(url,file_name):
    try:
        content = requests.get(url, headers=headers).content
        with open(file_name, "wb") as f:
            f.write(content)
        print('图片下载成功')
    except Exception as result:
        print('图片下载失败'+str(result))
url_1="http://www.jgsgmbwg.com/"
url="http://www.jgsgmbwg.com/newsshow.php?cid=71&id=6710"
x=get_all(url).find(name="div",attrs={'class':'listConts'})
y=x.find_all_next(name="img")
num=0
for i in y:
    file_name="C:\\Study\\work\\Museum-website-data-collection\\"
    url=url_1+i["src"]
    file_name=file_name+str(num)+".jpg"
    get_image(url,file_name)
    num=num+1
