import requests
from bs4 import BeautifulSoup
import datetime
import sys
import os

def printk(value):
    print(value)
    exit()

user = sys.argv[1]

url = "https://blog.csdn.net/{}".format(user)
# 构造请求头
headers={
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
}
# 发送get请求
r=requests.get(url = url,headers=headers,timeout = 5)
# 处理
soup=BeautifulSoup(r.text,'html.parser')

# 获取用户名
div = soup.find("div",class_ = "user-profile-head-name")
username = div.text.split(" ")[0]

# 查找专栏链接
divs = soup.find_all("div",class_ = "aside-common-box-content")
div = divs[1]
lis = div.find_all("li")

titles = []
infos = {}
# 爬取专栏链接及链接名
if os.path.isfile(user+".txt"):
    # 如果文件存在，删除文件
    os.remove(user+".txt")
for li in lis:
    # print("####")
    url = li.find("a").attrs['href']
    title = li.find("span").attrs['title']
    titles.append(title)
    infos[title] = {"url":url}

    # print("[+]"+title+url)
    with open(user+'.txt','a+') as f:    #设置文件对象
        f.write(url)
        f.write('\n')