# coding:utf-8
import re

import lxml
import lxml.etree
import requests


def geturllist(url):
    headers = {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0);"}
    response = requests.get(url, headers=headers).content.decode("gbk")
    mytree = lxml.etree.HTML(response)
    number = mytree.xpath("//div[@class=\"rt\"]/text()")[0].strip()
    restr = re.compile("(\d+)",re.IGNORECASE)
    num = restr.findall(number)[0]

    print eval(num)

def pagexpath(url):
    headers = {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0);"}
    response = requests.get(url, headers=headers).content.decode("gbk")
    # print(response)
    mytree = lxml.etree.HTML(response)

    joblist = mytree.xpath("//*[@id=\"resultList\"]//div[@class=\"el\"]")
    datalist = []
    for line in joblist:
        mystr = ""
        job = line.xpath("./p/span/a/text()")[0].strip()
        company = line.xpath("./span[1]/a/text()")[0].strip()
        addr = line.xpath("./span[2]/text()")[0].strip()

        monney = line.xpath("./span[3]/text()")
        if len(monney)==0:
            monney=""
        else:
            monney=monney[0].strip()
        datetime = line.xpath("./span[4]/text()")[0].strip()

        print  job,company,addr,monney,datetime

url = "http://search.51job.com/list/040000,000000,0000,00,9,99,python,2,1.html"
# geturllist(url)
pagexpath(url)