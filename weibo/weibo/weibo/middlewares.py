# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium import webdriver  # 代表模拟浏览器
from  scrapy.http import HtmlResponse  # 网页信息
import time


class LoginMiddleware(object):
    # 替换掉原来的函数，process_request
    def process_request(self, request, spider):
        if spider.name == "weiborela":  # 指定仅仅处理这个名称的爬虫
            if request.url.find("login") != -1:  # 判断是否登陆页面
                spider.browser.get(request.url)  # 爬虫访问链接
                time.sleep(3)
                print("login访问", request.url)
                username = spider.browser.find_element_by_id("loginname")
                password = spider.browser.find_element_by_xpath("//div[@class=\"input_wrap\"]/input[@type=\"password\"]")
                login = spider.browser.find_element_by_xpath("//div[@class=\"info_list login_btn\"]/a")
                username.send_keys("491636682@qq.com")
                time.sleep(1)
                password.send_keys("zxc350047")
                time.sleep(2)
                login.click()
                print("123\n")
                time.sleep(15)

            else:
                time.sleep(5)
                print(">>>>>>>>>>>>>>>>>>>>>>>>fuck<<<<<<<<<<<<<<<<<<<<<<<<<<")
                # request.访问，调用selenium cookie

            return HtmlResponse(url=spider.browser.current_url,  # 当前连接
                                body=spider.browser.page_source,  # 源代码
                                encoding="utf-8")  # 返回页面信息


class WeiboSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
