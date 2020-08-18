# -*- coding: utf-8 -*-
import lxml
import scrapy
import lxml.etree
from ganjirentscrapy import items
from  scrapy.linkextractors  import LinkExtractor
from  scrapy.spiders import CrawlSpider,Rule

class RentSpider(CrawlSpider):
    name = 'rent'
    allowed_domains = ['ganji.com']
    start_urls = ['http://sz.ganji.com/fang1/o1p1/']

    pagelinks = LinkExtractor(allow=(r"o\d+p1"))

    rules = [Rule(pagelinks, callback="parse_xpath", follow=True)]

    def parse_xpath(self, response):

        mytree = lxml.etree.HTML(response.body)
        homelist = mytree.xpath("//*[@class=\"f-list-item ershoufang-list\"]")

        datalist = []
        for line in homelist:
            myitems = items.GanjirentscrapyItem()

            home = line.xpath("./dl/dd[1]/a/text()")[0].strip()

            pattern = ""
            patternlist = line.xpath("./dl/dd[2]//span/text()")
            # print(len(addrlist))
            for i in range(len(patternlist)):
                pattern += patternlist[i].strip()
                pattern.strip()
                # print(add)

            addr = ""
            addr1 = line.xpath("./dl/dd[3]/span//a/text()")
            for i in range(len(addr1)):
                addr += addr1[i].strip()

            money = ""
            moneylist = line.xpath("./dl/dd[5]/div[1]//span/text()")
            for i in range(len(moneylist)):
                money += moneylist[i]
            datetime = line.xpath("./dl/dd[5]/div[2]/text()")[0]

            myitems["home"] = home
            myitems["pattern"] = pattern
            myitems["addr"] = addr
            myitems["money"] = money
            myitems["datetime"] = datetime

            # print (home, pattern, addr, money, date)
            yield myitems


        pass
