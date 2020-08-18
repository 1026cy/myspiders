from scrapy_redis.spiders import RedisSpider
import example.items
import re
import redis
import scrapy
import selenium
import selenium.webdriver
import time
import lxml
import lxml.etree
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup



class StockSpider(RedisSpider):

    name = 'stock'
    redis_key = 'stock:start_urls'

    def __init__(self, *args, **kwargs):

        domain = kwargs.pop('https://gupiao.baidu.com/stock/', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(StockSpider, self).__init__(*args, **kwargs)


    def parse(self,response):
        fundFlowUrlList=[]
        self.fundHrefs = response.xpath("//*[@class=\"f10-menu m-t\"]//a[4]/@href").extract()
        print(self.fundHrefs,"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%5" )
        # StockRedis = redis.Redis(host="127.0.0.1", port=6379, db=0)
        self.fundFlowUrl="https://gupiao.baidu.com" +self.fundHrefs[0]
        fundFlowUrlList.append(self.fundFlowUrl)
        # StockRedis.lpush("stock:fundFlowUrl", fundFlowUrl)
        print(self.fundFlowUrl,"*************************************")
        print(fundFlowUrlList,"&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        url = "https://gupiao.baidu.com"
        driver = selenium.webdriver.Chrome()
        titleList = []
        urlList = []
        driver.get(response.url)
        time.sleep(3)

        # 实现【新闻】【公告】【研报】三栏翻页
        for i in range(1, 4):
            rule = "//*[@id=\"app-wrap\"]/div[4]/div[4]/ul/li[" + str(i) + "]"
            elem = driver.find_element(By.XPATH, rule)
            print(elem, "____________________________")
            elem.click()
            time.sleep(3)

            # 实现每一栏翻页：
            # 1、抓取lastPageNumber
            webdata = driver.page_source
            mytree = lxml.etree.HTML(webdata)
            num = mytree.xpath("//*[@id=\"app-wrap\"]/div[4]/div[5]/div//a[8]/text()")[0]
            print(num)
            # 2、翻页
            for k in range(0, eval(num) - 1):
                nextRule = "//*[@id=\"app-wrap\"]/div[4]/div[5]/div/a[last()-1]"
                next = driver.find_element(By.XPATH, nextRule)
                print(next, "****************************")
                next.click()
                time.sleep(5)

                # 爬取每一栏每一页的【标题】和【url】
                for j in range(0, 10):
                    pagedata = driver.page_source
                    soup = BeautifulSoup(pagedata, "xml")
                    try:
                        newsTitle = soup.find_all('h4', {'class': 'text-ellipsis'})[j].string
                        newsUrl = soup.find_all('h4', {'class': 'text-ellipsis'})[j].a['href']
                        newsUrl = url + newsUrl
                        print(newsTitle, newsUrl)
                        titleList.append(newsTitle)
                        urlList.append(newsUrl)
                    except:
                        pass
        driver.close()
        time.sleep(10)

        print("IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
        print(fundFlowUrlList,"")
        print(titleList)
        print(urlList)
        print("IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")

        for i in range(len(titleList)):
            stockitem = example.items.StockItem()
            if i<len(fundFlowUrlList):
                stockitem["fundFlowUrl"] = fundFlowUrlList[i]
                stockitem["newsTitle"] = titleList[i]
                stockitem["newsUrl"] = urlList[i]
                yield stockitem
            else:
                stockitem["newsTitle"] = titleList[i]
                stockitem["newsUrl"] = urlList[i]
                yield stockitem

