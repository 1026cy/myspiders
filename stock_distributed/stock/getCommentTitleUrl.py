#coding:utf-8
#! ‪C:\Developer\python36\python3.exe

import requests
import lxml
import lxml.etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
}

url = 'http://istock.jrj.com.cn/list,600083.html'
html = requests.get(url,headers=headers).content.decode('gbk')
myTree = lxml.etree.HTML(html)
trList = myTree.xpath('//tr[@name="titlehb"]')
for tr in trList:
    title = tr.xpath('./td[@class="tl"]/a/text()')[0]
    url = tr.xpath('./td[@class="tl"]/a/@href')[0]
    print(tr.xpath('./td[@class="tl"]/a/text()'))
    print(tr.xpath('./td[@class="tl"]/a/@href'))




