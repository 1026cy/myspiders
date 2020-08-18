# -*- coding: utf-8 -*-
import scrapy
import re
import time

import requests
import urllib
from bs4 import BeautifulSoup
import lxml
import lxml.etree
from urllib import request
import selenium
import selenium.webdriver
from bs4 import BeautifulSoup
from selenium.webdriver import DesiredCapabilities
import threading
import gevent
import gevent.monkey
import biliscrapy.items
class FuckSpider(scrapy.Spider):
    name = 'fuck'
    allowed_domains = ['bilibili.com']
    start_urls = ["https://www.bilibili.com"]

    def parse(self, response):
        data=response.body

        soup = BeautifulSoup(data, "lxml")
        # print(soup)
        fuck = soup.find("ul", class_="nav-menu").find_all("li", class_=re.compile("^nav-item.*"))
        # print(data)
        # mtree = lxml.etree.HTML(data)
        # fuck = mtree.xpath("//li[@class=\"nav-item\"]")
        # print(len(fuck))
        count=-1
        for i in fuck:
            count+=1
            ur = i.a["href"]
            if ur.find("http") == -1:
                ur = "https:" + ur
            yield scrapy.Request(url=ur,callback=self.main,meta={"meta":count})
    def main(self,response):



        fuck=response.url

        i = response.meta["meta"]
        print("start" + str(i)+"||||||||"+fuck)
        data = self.sele(fuck)
        if i == 14:
            print("开始爬14主题————————————————")
            soup = BeautifulSoup(data, "html.parser")
            r = soup.find_all(class_=re.compile("^video-item-biref.*"))
            for i in r:
                item=biliscrapy.items.BiliscrapyItem()

                h = i.a["href"]
                m = i.find_all("img")[0]["src"]
                t = i.find_all(class_="biref-info")[0].get_text()
                if h.find("http") == -1:
                    h = "https:" + h
                if m.find("http") == -1:
                    m = "https:" + m
                item["hef"]=h
                item["title"]=t
                item["img"]=m
                yield item


        if i == 15:
            print("开始爬15主题————————————————————————————")
            print("亲！网络开了小差哦")

        if i == 16:
            print("开始爬16主题————————————————————————")
            mtree = lxml.etree.HTML(data)
            z = mtree.xpath("//*[@class=\"s-imgUnit\"]")

            for i in z:
                item = biliscrapy.items.BiliscrapyItem()
                num = len(i.xpath(".//a"))
                print("ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
                if num > 1:
                    h = i.xpath(".//a")[0].xpath("./@href")[0].strip()
                    m = i.xpath(".//a")[0].xpath(".//img/@src")[0].strip()
                    t = i.xpath(".//a")[1].xpath(".//text()")[0].strip()
                    if h.find("http") == -1:
                        h = "https:" + h
                    if m.find("http") == -1:
                        m = "https:" + m
                    item["hef"] = h
                    item["title"] = t
                    item["img"] = m
                    yield item


        if i == 17:
            print("开始爬17主题————————————————————————————")
            soup = BeautifulSoup(data, "lxml")
            m = soup.find_all("div", {"role": "img"})
            # print(m[0]["style"])
            for i in m:
                item = biliscrapy.items.BiliscrapyItem()
                t = ""

                try:
                    p = i["style"].split("(")[1].split(")")[0]
                    if p.find("http") == -1:
                        p = "https:" + p
                    t += p + "||"
                except:
                    t += "亲！找不到"+"||"
                try:
                    t += i["title"]
                except:
                    t += "亲！找不到"
                item["hef"] = t.split("||")[0]
                item["title"] = t.split("||")[1]
                item["img"] = t.split("||")[0]
                yield item
        if i == 18:
            print("开始爬18主题——————————————————————————————")
            print("亲！网络开了小差哦")

        if i == 2 or i == 3:
            print("开始爬2和3主题——————————————————————————————————")
            soup = BeautifulSoup(data, "html.parser")
            img = []
            img1 = soup.find_all("div", class_=re.compile("^v$"))
            img2 = soup.find_all("div", class_=re.compile("^v .*"))
            img += img2
            img += img1
            for i in img:
                item = biliscrapy.items.BiliscrapyItem()
                h = i.a["href"]
                t = i.a["title"]
                m = i.find_all("img")[0]["src"]
                if h.find("https") == -1:
                    h = "https:" + h
                if m.find("https") == -1 and len(m) != 0:
                    m = "https:" + m
                item["hef"] = h
                item["title"] = t
                item["img"] = m
                yield item

        else:
            print("开始爬其它————————————————————————")
            # print("------------------------------------")
            mtree = lxml.etree.HTML(data)
            h1 = mtree.xpath("//*[@class=\"groom-module\"]/a/@href")
            img1 = mtree.xpath("//*[@class=\"groom-module\"]//img/@src")
            title1 = mtree.xpath("//*[@class=\"groom-module\"]//img/@alt")

            h = mtree.xpath("//*[@class=\"spread-module\"]/a/@href")
            img = mtree.xpath("//*[@class=\"spread-module\"]//img/@src")
            title = mtree.xpath("//*[@class=\"spread-module\"]//img/@alt")
            for i in range(len(h)):
                item = biliscrapy.items.BiliscrapyItem()
                try:
                    if h[i].find("https") == -1:
                        h[i] = "https://www.bilibili.com" + h[i]
                    if img[i].find("https") == -1 and len(img[i]) != 0:
                        img[i] = "https:" + img[i]
                    item["hef"] = h[i]
                    item["title"] = title[i]
                    item["img"] = img[i]
                    yield item
                except Exception as e:
                    print(e)

            for i in range(len(h1)):
                item = biliscrapy.items.BiliscrapyItem()
                try:
                    if h1[i].find("https") != 0:
                        h1[i] = "https://www.bilibili.com" + h1[i]
                    if img1[i].find("https") != 0:
                        img1[i] = "https:" + img1[i]
                    item["hef"] = h1[i]
                    item["title"] = title1[i]
                    item["img"] = img1[i]
                    yield item
                except Exception as e:
                    print(e)

        pass

    def sele(self,url):
        dcap = dict(DesiredCapabilities.PHANTOMJS)  # 处理无界面浏览器
        # dcap["phantomjs.page.settings.userAgent"]=("Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36")
        dcap["phantomjs.page.settings.userAgent"] = (
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0);"
        )
        path = r"D:\PYTHON.XIAO\SZday8\tools\phantomjs-2.1.1-windows\bin\phantomjs.exe"
        driver = selenium.webdriver.PhantomJS(executable_path=path, desired_capabilities=dcap)  # 打开无界面浏览器
        driver.get(url)
        co = 0
        # height=driver.execute_script("document.body.offsetHeight")
        # print(height)
        for co in range(1, 9):
            co = co * 550
            driver.execute_script("window.scrollTo(0," + str(co) + ")")
            time.sleep(2)

        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(1)

        data = driver.page_source
        driver.close()
        return data

