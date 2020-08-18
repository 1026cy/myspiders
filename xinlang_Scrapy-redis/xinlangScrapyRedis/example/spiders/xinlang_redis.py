import urllib
import re

import scrapy
from scrapy_redis.spiders import RedisSpider
from example import  items
import lxml
import lxml.etree

class MySpider(RedisSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    name = 'xinlang_redis'
    redis_key = 'xinlang:start_urls'

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('news.sina.com', '') #指定搜索域
        self.allowed_domains = filter(None, domain.split(','))
        super(MySpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        data = response.body.decode("gb2312", "ignore")  # 网页
        mytree = lxml.etree.HTML(data)  # 解析页面，
        hlist=mytree.xpath("//ul[@class=\"linkNews\"]//li")
        for item in hlist:
            waritem = items.CtoyaonimeiItem()  # 创建一个item对象
            waritem["url"]= item.xpath(".//a/@href")[0]  # 抓取元素
            waritem["content"] = self.getcontent(waritem["url"])
            waritem["title"] = item.xpath(".//a//text()")[0]
            waritem["time"] =item.xpath(".//span/text()")[0]
            yield waritem



    def getcontent(self,url):
        data = urllib.request.urlopen(url).read().decode("utf-8", "ignore")
        mytree = lxml.etree.HTML(data)  # 解析页面，
        content=mytree.xpath("//div[@id=\"wrapOuter\"]//p//text()")
        content=str(content).replace("'\\u3000\\u3000","").replace("\\n","").replace("\\t","")
        return content


