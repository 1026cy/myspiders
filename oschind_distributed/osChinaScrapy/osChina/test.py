#coding:utf-8
#! ‪C:\Developer\python36\python3.exe
import requests
import selenium
import selenium.webdriver
import lxml
import lxml.etree
import urllib.request
import urllib

headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0"
}

url = 'https://www.oschina.net/project/zhlist/309/web-devel'
req = requests.get(url, headers=headers)
html = req.content.decode("utf-8")
print(html)
myTree = lxml.etree.HTML(html)
content = myTree.xpath("//div[@class = \"panel-list news-list\"]//a[@class=\"item\"]")
for text in content:
    url = text.xpath("./@href")[0]
    print(url)
#     print(divList[i].xpath('./ul//li[2]/a/text()'))
#     print(divList[i].xpath('./ul//li[3]/text()'))
#     print(divList[i].xpath('./div/a/img/@src'))
#     print(divList[i].xpath('./div/a/@href'))

    # name = div.xpath('./ul//li[1]/a/text()')
    # price = div.xpath('./ul//li[2]/a/text()')
    # info = div.xpath('./ul//li[3]/text()')
    # imgUrl = div.xpath('./div/a/img/@src')
    # print(name,price,info,imgUrl)