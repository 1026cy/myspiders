# -*- coding: utf-8 -*-
import lxml
import scrapy
import lxml.etree
from job51 import items
from  scrapy.linkextractors  import LinkExtractor
from  scrapy.spiders import CrawlSpider,Rule

class JobSpider(CrawlSpider):
    name = 'job'
    allowed_domains = ['search.51job.com']
    start_urls = ['http://search.51job.com/list/040000,000000,0000,00,9,99,python,2,1.html']


    pagelinks=LinkExtractor (allow=(r"\d.html"))

    rules = [Rule (pagelinks,callback="parse_xpath",follow=True)]

 

    def parse_xpath(self, response):
        mytree = lxml.etree.HTML(response.body)

        joblist = mytree.xpath("//*[@id=\"resultList\"]//div[@class=\"el\"]")

        for line in joblist:
            myitems = items.Job51Item()
            job = line.xpath("./p/span/a/text()")[0].strip()
            company = line.xpath("./span[1]/a/text()")[0].strip()
            addr = line.xpath("./span[2]/text()")[0].strip()
            money = line.xpath("./span[3]/text()")
            if len(money) == 0:
                money = ""
            else:
                money = money[0].strip()
            datetime = line.xpath("./span[4]/text()")[0].strip()

            myitems["job"] = job
            myitems["company"] = company
            myitems["addr"] = addr
            myitems["money"] = money
            myitems["datetime"] = datetime

            # print (job, company, addr, money, date)
            yield myitems

        pass
