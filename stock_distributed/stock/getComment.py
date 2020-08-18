# coding:utf-8
# ! ‪C:\Developer\python36\python3.exe

import requests
import lxml
import lxml.etree
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
}

url = 'http://istock.jrj.com.cn/article,600000,367642.html'
html = requests.get(url, headers=headers).content.decode('gbk')
soup = BeautifulSoup(html,'html5lib')
mainDiv = soup.find('div',class_='main')
comment = mainDiv.find('div').get_text()


# myTree = lxml.etree.HTML(html)
# comment = myTree.xpath('//div[@class="main"]/div/text()')[0]

print(comment)


