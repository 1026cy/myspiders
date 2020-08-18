# -*- coding: utf-8 -*-
import multiprocessing.managers #分布式进程管理器
import Queue
import threading
import selenium
import selenium.webdriver
import time
import selenium.webdriver.common.keys
import requests
import lxml
import lxml.etree
import re
import time

'''
add your question
'''

class  QueueManger(multiprocessing.managers.BaseManager):#继承，进程管理共享数据
    pass
def getcookie():
    url = "https://home.taoche.com/login/?returnurl=http%3A%2F%2Fwww.taoche.com%2F"
    driver = selenium.webdriver.Chrome()
    driver.get(url)
    time.sleep(2)
    elem = driver.find_element_by_id("1")
    elem.click()
    elem = driver.find_element_by_id("mobile1")
    elem.send_keys("18377683563")
    elem = driver.find_element_by_id("password")
    elem.send_keys("314251612")
    time.sleep(6)
    elem = driver.find_element_by_id("user-btn1")
    elem.click()
    cookies = driver.get_cookies()  # 抓取全部的cookie
    driver.close()
    return cookies
def  getcontent(cookies,url):
    req = requests.session()
    for cookie in cookies:
        req.cookies.set(cookie["name"], cookie["value"])
    req.headers.clear()  # 清除请求头
    response = req.get(url).text
    mytree = lxml.etree.HTML(response)
    detail = mytree.xpath("//div[@class=\"item_details\"]")
    price=mytree.xpath("//div[@class=\"item_price\"]")
    new= mytree.xpath("//h2[@class=\"heji\"]/text()")  # 现售价
    # print(len(detail))
    datalist=[]

    for t in range(1,len(detail)):
        mystr = ""
        try:
            mystr+= detail[t].xpath(".//h3/a/text()")[0]  # 标题
        except:
            mystr+=u"标题被狗吃了"
        # print mystr
        mystr += "-----"
        mystr += detail[t].xpath(".//ul[@class=\"ul_news\"]/li[1]/i/text()")[0]  # 上牌标签
        mystr += detail[t].xpath(".//ul[@class=\"ul_news\"]/li[1]/text()")[0]  # 上牌时间标签
        mystr += "--"
        mystr += detail[t].xpath(".//ul[@class=\"ul_news\"]/li[2]/i/text()")[0]  # 里程标签
        mystr += detail[t].xpath(".//ul[@class=\"ul_news\"]/li[2]/text()")[0]  # 里程数
        mystr += "--"
        mystr += detail[t].xpath(".//ul[@class=\"ul_news\"]/li[3]/i/text()")[0]  # 所在城市
        mystr+=":"
        try:
            city = detail[t].xpath(".//ul[@class=\"ul_news\"]/li[3]/a/text()")[0]  # 城市
            mystr += city[0]
        except:
            city = detail[t].xpath(".//ul[@class=\"ul_news\"]/li[3]/text()")
            mystr+=city[0]
        mystr += "--"
        mystr += detail[t].xpath(".//ul[@class=\"ul_news\"]/li[4]/i/text()")[0]  # 排放标准
        mystr += detail[t].xpath(".//ul[@class=\"ul_news\"]/li[4]/text()")[0]  # 排放
        mystr += u"#现售价："
        mystr += new[t]  # 现售价
        mystr += "--"
        mystr += price[t].xpath("./p/text()")[0]  # 新车价标签
        try:
            mystr += price[t].xpath("./p/del/text()")[0]  # 新车价
            mystr += price[t].xpath("./p/text()")[1].strip()  # 省钱
        except:
            mystr +=u"新车价居然也被狗吃了"
            mystr+=u"这车不省钱！"
            pass
        print mystr
        datalist.append(mystr)
        for line in datalist:  # 结果队列
            print u"发送给服务端：", line
            result.put(line)

if __name__ == '__main__':
    QueueManger.register("get_task")  # 注册函数调用服务器
    QueueManger.register("get_result")
    manger = QueueManger(address=("192.168.0.101", 8858), authkey="123456")
    manger.connect()  # 链接服务器
    task = manger.get_task()
    result = manger.get_result()  # 任务，结果
    cookie = getcookie()
    while True:
        time.sleep(1)
        try:
            url = task.get()
            print "client get", url
            # datalist=getcontent(cookie,url)
            # for line in datalist:  # 结果队列
            #     print u"发送给服务端：", line
            #     result.put(line)
            t=threading.Thread(target=getcontent,args=(cookie,url))
            t.start()
        except Exception as e:
            print u"异常",e




