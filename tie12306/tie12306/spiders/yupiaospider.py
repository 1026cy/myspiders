# -*- coding: utf-8 -*-
import scrapy
import time

from bs4 import BeautifulSoup
from scrapy.http import FormRequest
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
import html5lib
from tie12306 import items


class YupiaospiderSpider(scrapy.Spider):
    name = 'yupiaospider'
    allowed_domains = ['12306.cn']
    start_urls = ['https://kyfw.12306.cn/otn/login/init']
    startDate=['2017','十二月','12']

    def __init__(self):
        super(YupiaospiderSpider,self).__init__()
        self.driver=webdriver.Chrome()


        dispatcher.connect(self.spider_close,signals.spider_closed)

    def spider_close(self):
        self.driver.close()
        pass


    def parse(self, response):

        page_source=response.body
        print(page_source)
        soup=BeautifulSoup(page_source,"html5lib")
        print(soup)
        trList=soup.find_all('tbody')[1].find_all('tr')
        for tr in trList:
            if tr.text:
                infoItem=items.Tie12306Item()
                infoItem['entireInfo']=tr.text
                yield infoItem

