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

url = 'https://www.oschina.net/p/tankwar'
req = requests.get(url, headers=headers)
html = req.content.decode("utf-8")
# print(html)
myTree = lxml.etree.HTML(html)
# protocol = ""
# protocolList = myTree.xpath("//section[@class = \"list\"]/div[1]/span/a/text()")
# if len(protocolList):
#     protocol = protocolList[0]
# print(protocol)
#
# langList = myTree.xpath("//section[@class = \"list\"]/div[2]/span//a//text()")
# lang = ""
# for l in langList:
#     lang+=l+'、'
# print(lang)
#
# sysList = myTree.xpath("//section[@class = \"list\"]/div[3]/span//text()")[0]
# print(sysList)
#
# authList = myTree.xpath("//section[@class = \"list\"]/div[4]/a//text()")[0]
# print(authList)
myStr = ""
contentList = myTree.xpath('//div[@class="detail editor-viewer all"]//p/text()')
for content in contentList:
    myStr+=content
myStr = myStr.replace("\xa0","")
myStr = myStr.replace(", ","")
print(myStr)
    # if len(protocolList):
    #     protocol = protocolList[0]
    # print(protocol)

#     print(divList[i].xpath('./ul//li[2]/a/text()'))
#     print(divList[i].xpath('./ul//li[3]/text()'))
#     print(divList[i].xpath('./div/a/img/@src'))
#     print(divList[i].xpath('./div/a/@href'))

    # name = div.xpath('./ul//li[1]/a/text()')
    # price = div.xpath('./ul//li[2]/a/text()')
    # info = div.xpath('./ul//li[3]/text()')
    # imgUrl = div.xpath('./div/a/img/@src')
    # print(name,price,info,imgUrl)