# -*- coding: utf-8 -*-
import re
import requests
import scrapy
import example.items
import time
from scrapy_redis.spiders import RedisSpider
import lxml.etree
import baidus
import fenghuangcaijing
import sinacaijing
from selenium import webdriver


class StockSpider(RedisSpider):
    name = 'stock_redis'
    redis_key = 'stock:start_urls'


    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(StockSpider, self).__init__(*args, **kwargs)

    def get_stock_info(self,url):
        try:
            print('调用浏览器')
            driver = webdriver.Chrome()
            driver.get(url)
            time.sleep(10)
            data = driver.page_source
            print('获取页面源码')
            mytree = lxml.etree.HTML(data)
            info = mytree.xpath('//div[@class="data-middle"]/table/tbody//tr//td/text()')
            driver.close()
            print('浏览器关闭')
            return info
        except Exception as e:
            print('获取股票信息失败', e)

    def parse(self, response):
        data = response.body
        print(data)
        mytree = lxml.etree.HTML(data)
        stock = mytree.xpath('//title/text()')[0].split('(')[0]
        print(stock)
        url = response.url
        info = self.get_stock_info(url)
        print(info)
        biadunews = baidus.baidu_result(stock)
        print(biadunews)
        fenghuang = fenghuangcaijing.fenghuang_result(stock)
        sina = sinacaijing.sina_result(stock)
        stocktitem=example.items. StockItem()
        stocktitem['stock'] = stock
        stocktitem['info'] = str(info)
        stocktitem['baidunews'] = biadunews
        stocktitem['fenghuang'] = fenghuang
        stocktitem['sina'] = sina
        yield   stocktitem

