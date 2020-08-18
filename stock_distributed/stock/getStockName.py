#coding:utf-8
#! ‪C:\Developer\python36\python3.exe

import requests
import lxml
import lxml.etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
}

url = 'http://quote.eastmoney.com/stocklist.html'
html = requests.get(url,headers=headers).content.decode('gbk')
myTree = lxml.etree.HTML(html)
liList = myTree.xpath('//div[@id="quotesearch"]//ul//li')
numList = []
file = open('stockNameNum.txt', 'w')
for li in liList:
    # print(li.xpath('./a/text()'))
    name = li.xpath('./a/text()')[0][:-8]
    num = li.xpath('./a/text()')[0][-7:-1]
    if num.startswith('0') or num.startswith('3') or num.startswith('6'):
        numList.append(num)
        file.write(name+' # '+num+'\n')
        print(num)
file.close()
# print(len(numList))


