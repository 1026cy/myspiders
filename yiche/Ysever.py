# coding:utf-8
import multiprocessing  # 分布式进程
import multiprocessing.managers  # 分布式进程管理器
import random, time  # 随机数，时间
import Queue  # 队列
import threading
import gevent
import gevent.monkey
import lxml.etree
import re
import lxml
import lxml.etree
import pymongo as pymongo
import requests
task_queue = Queue.Queue()  # 任务
result_queue = Queue.Queue()  # 结果


def return_task():  # 返回任务队列
    return task_queue


def return_result():  # 返回结果队列
    return result_queue

class QueueManger(multiprocessing.managers.BaseManager):  # 继承，进程管理共享数据
    pass
def getcity():
    cityurl = "http://quanguo.taoche.com/all/"
    req = requests.session()
    response = req.get(cityurl).text
    mytree = lxml.etree.HTML(response)
    city = mytree.xpath("//div[@class=\"header-city-province-text\"]//a/@href")  # 匹配城市连接
    citylist=[]
    for c in city:
        citylist.append("http:"+c+"all/")
    return citylist

def geturl():
    savefile = open("yiche.txt", "w")
    urllist = []
    list=getcity()
    for c in list:
        # 开始抓取第一页
        req = requests.session()
        try:
            response = req.get(c).text
            print("*************************************城市分割线******************************************")
            mytree = lxml.etree.HTML(response)
            totalpage = mytree.xpath("//div[@class=\"the-pages\"]/div/a[last()-1]/text()")#匹配总页数
            # print("》》》》》》》》", totalpage)
            try:
                for i in range(1, eval(totalpage[0]) + 1):
                    url = c+ "?page=" + str(i)
                    print(url)
                    urllist.append(url)
                    task.put(url)
                    time.sleep(3)
                    while True:
                        res = result.get(timeout=30)
                        print u"接受数据：", res
                        savefile.write(res.encode("utf-8", "ignore") + '\r\n')
                        savefile.flush()
                    # write()

            except:
                url = c
                # print(url)
                urllist.append(url)
                # print u"发送任务：", url
                task.put(url)
                time.sleep(1)
                while True:
                    res = result.get(timeout=30)
                    print u"接受数据：", res
                    savefile.write(res.encode("utf-8", "ignore") + '\r\n')
                    savefile.flush()
                # write()
        except Exception as e:
            print e
    savefile.close()

def write():
    savefile=open("yiche.txt", "a")
    while True:
        res = result.get(timeout=30)
        print u"接受数据：", res
        savefile.write(res.encode("utf-8", "ignore") + '\r\n')
        savefile.flush()
    savefile.close()

if __name__ == "__main__":
    multiprocessing.freeze_support()  # 开启分布式支持
    QueueManger.register("get_task", callable=return_task)  # 注册函数给客户端调用
    QueueManger.register("get_result", callable=return_result)
    manger = QueueManger(address=("192.168.0.101", 8858), authkey="123456")  # 创建一个管理器，设置地址与密码
    manger.start()  # 开启
    task, result = manger.get_task(), manger.get_result()  # 任务，结果
    geturl()
    manger.shutdown()  # 关闭服务器
