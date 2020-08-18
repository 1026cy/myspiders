# -*- coding: utf-8 -*-
import re

import scrapy
from selenium import webdriver
# from  scrapy.xlib.pydispatch import dispatcher #观察者
from  scrapy import signals #信号
import time
from lxml import etree
from queue import Queue
from weibo.items import WeiboItem



class WeiborelaSpider(scrapy.Spider):
    name = 'weiborela'
    allowed_domains = ['weibo.com']
    start_urls = ['http://weibo.com/login.php']

    def __init__(self):
        self.browser = webdriver.Chrome()
        super(WeiborelaSpider,self).__init__()
        self.focus_queue = Queue()  # 关注链接队列
        # dispatcher.connect(self.spider_closed, signals.spider_closed)  # 爬虫关闭通过信号调用我们自己的函数

    # def spider_closed(self,response):#爬虫关闭
    #     print("爬虫关闭")
    #     self.browser.close() #关闭浏览器
    def parse(self, response):
        time.sleep(3)
        print(response.url)

        #  关注人
        focus = self.browser.find_element_by_xpath("//ul[@class=\"user_atten clearfix W_f18\"]/li[@class=\"S_line1\"]")
        focus_num_text = focus.text
        focus_num = re.findall("\d+", focus_num_text)
        # 粉丝
        fans_num_text = self.browser.find_element_by_xpath("//ul[@class=\"user_atten clearfix W_f18\"]//li[@class=\"S_line1\"][2]").text
        fans_num = re.findall("\d+", fans_num_text)
        print(focus_num, "\n", fans_num)
        focus.click()

        myname = self.browser.find_element_by_class_name("username").text
        print(myname)
        while True:
            # class = member_li S_bg1 关注人列表信息
            tree = etree.HTML(self.browser.page_source)
            member_list = tree.xpath("//li[@class=\"member_li S_bg1\"]")

            # 每页的关注人信息
            for member in member_list:
                item = WeiboItem()
                name = member.xpath(".//img/@title")[0]
                img = member.xpath(".//img/@src")[0]
                link_half = member.xpath(".//div[@class=\"mod_info\"]/div/a[1]/@href")[0]
                link = "http://weibo.com/" + link_half
                intro = member.xpath(".//div[@class=\"text W_autocut S_txt2\"]/text()")[0].strip()
                item["username"] =myname
                item["name"] = name
                item["img"] = img
                item["link"] = link
                item["intro"] = intro
                item["focus"] = True
                self.focus_queue.put(link)
                yield item

            time.sleep(5)
            # page next S_txt1 S_line1 下一页，没有下一页的 a 标签时弹出
            try:
                next_page = self.browser.find_element_by_xpath("//a[@class=\"page next S_txt1 S_line1\"]")
                # 滑稽
                js = "window.scrollTo(0,8000)"
                self.browser.execute_script(js)
                # 下一页没有 a 标签蹦出
                next_page.click()
            except:
                print("fuck")
                break

        # 获得别人的关注信息
        while True:

            url = self.focus_queue.get()
            print(url)
            self.browser.get(url)
            time.sleep(10)

            ffn_list = self.browser.find_elements_by_xpath("//table[@class=\"tb_counter\"]//td")
            print(ffn_list)

            flist = []

            # 关注 粉丝 weibo
            for f in ffn_list:
                print(f.text)
                flist.append(re.findall("\d+", f.text))
            tree = etree.HTML(self.browser.page_source)

            # 微博名
            weiboname = self.browser.find_element_by_class_name("username").text

            # 简介
            infos_xpath = tree.xpath("//div[@class=\"PCD_person_info\"]//text()")
            print(infos_xpath)
            infos = "".join([i.strip().replace(" ", "").replace("\t", "") for i in infos_xpath])
            item_info = WeiboItem()
            item_info["username"] = weiboname
            item_info["infos"] = infos
            yield item_info

            time.sleep(5)

            # 关注人列表
            ffn_list[0].click()

            sum = 0
            # 最多只能扒5页
            while sum < 5:
                sum += 1
                # class = follow_item S_line2 其他人的关注人
                tree = etree.HTML(self.browser.page_source)
                member_list = tree.xpath("//li[@class=\"follow_item S_line2\"]")
                for member in member_list:
                    item = WeiboItem()
                    name = member.xpath(".//img/@alt")[0]
                    img = member.xpath(".//img/@src")[0]
                    link_half = member.xpath(".//dd[@class=\"mod_info S_line1\"]/div/a/@href")[0]
                    link = "http://weibo.com/" + link_half
                    intro_xpath = member.xpath(
                        "./dl/dd[@class=\"mod_info S_line1\"]/div[@class=\"info_intro\"]/span/text()")
                    intro = intro_xpath[0].strip() if len(intro_xpath) > 0 else "啥都毛写"
                    print(name, img, link, intro)
                    item["username"] = weiboname
                    item["name"] = name
                    item["img"] = img
                    item["link"] = link
                    item["intro"] = intro
                    item["focus"] = True
                    yield item
                    self.focus_queue.put(link)

                try:
                    next_page = self.browser.find_element_by_xpath("//a[@class=\"page next S_txt1 S_line1\"]")
                    # 滑稽
                    js = "window.scrollTo(0,10000)"
                    self.browser.execute_script(js)
                    next_page.click()
                except:
                    print("fuck")
                    break

