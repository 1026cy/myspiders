# -*- coding: utf-8 -*-
import scrapy
import lxml
import lxml.etree
from stock import items
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
}

class StockspiderSpider(scrapy.Spider):
    name = 'stockSpider'
    allowed_domains = ['istock.jrj.com.cn','eastmoney.com',]
    # start_urls = ['http://quote.eastmoney.com/stocklist.html']

    def start_requests(self):
        url = 'http://quote.eastmoney.com/stocklist.html'
        html = requests.get(url, headers=headers).content.decode('gbk')
        myTree = lxml.etree.HTML(html)
        liList = myTree.xpath('//div[@id="quotesearch"]//ul//li')
        self.stockList = []
        requestsList = []
        for li in liList[:290]:
            if len(li.xpath('./a/text()'))!=0:
                self.stockList.append(li.xpath('./a/text()')[0])
                num = li.xpath('./a/text()')[0][-7:-1]
                name = li.xpath('./a/text()')[0][:-8]
                if num.startswith('0') or num.startswith('3') or num.startswith('6'):
                    myItem = items.StockItem()
                    myItem['name'] = name
                    myItem['num'] = num
                    requestsList.append(scrapy.Request(url='http://istock.jrj.com.cn/list,'+num+',p1.html',meta={'meta':myItem},headers=headers))
        return requestsList


    def parse(self, response):
        myItem = response.meta['meta']
        myTree = lxml.etree.HTML(response.body)
        trList = myTree.xpath('//tr[@name="titlehb"]')
        print('parse')
        print(response.url)
        for tr in trList:

            title = tr.xpath('./td[@class="tl"]/a/text()')[0]
            url = tr.xpath('./td[@class="tl"]/a/@href')[0]
            myItem['title'] = title
            myItem['url'] = url
            yield scrapy.Request(url=myItem['url'],meta={'meta':myItem},headers=headers,callback=self.parse_comment)

    # def parse_title(self,response):
    #     print(response.url)
    #     myItem = response.meta['meta']
    #     print('parse_title'+myItem['num'])
    #     myTree = lxml.etree.HTML(response.body)
    #     trList = myTree.xpath('//tr[@name="titlehb"]')
    #     for tr in trList:
    #         title = tr.xpath('./td[@class="tl"]/a/text()')[0]
    #         url = tr.xpath('./td[@class="tl"]/a/@href')[0]
    #         myItem['title'] = title
    #         myItem['url'] = url
    #         yield scrapy.Request(url=myItem['url'],meta={'meta2':myItem},headers=headers,callback='parse_comment')

    def parse_comment(self,response):
        myItem = response.meta['meta']
        myTree = lxml.etree.HTML(response.body)
        comment = myTree.xpath('//div[@class="main"]/div/text()')[0]
        myItem['comm'] = comment
        yield myItem

