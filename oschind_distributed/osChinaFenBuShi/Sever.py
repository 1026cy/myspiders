#coding:utf-8
import multiprocessing  #分布式进程
import multiprocessing.managers #分布式进程管理器
import random,time  #随机数，时间
from queue import Queue #队列

import pymongo
from selenium.webdriver import DesiredCapabilities
import selenium
import selenium.webdriver
import time
import lxml
import lxml.etree


task_queue=Queue() #任务
result_queue=Queue() #结果

def  return_task(): #返回任务队列
    return task_queue
def return_result(): #返回结果队列
    return   result_queue

class  QueueManger(multiprocessing.managers.BaseManager):#继承，进程管理共享数据
    pass

if __name__=="__main__":
    multiprocessing.freeze_support()#开启分布式支持
    QueueManger.register("get_task",callable=return_task)#注册函数给客户端调用
    QueueManger.register("get_result", callable=return_result)
    manger=QueueManger(address=("127.0.0.1",8111),authkey=123456) #创建一个管理器，设置地址与密码
    manger.start() #开启
    task,result=manger.get_task(),manger.get_result() #任务，结果

    url = "https://www.oschina.net/project/zh"
    myCon = pymongo.MongoClient(host='127.0.0.1', port=27017)
    db = myCon['oschina']
    coll = db['data']
    dcap = dict(DesiredCapabilities.PHANTOMJS)  # 处理无界面浏览器
    dcap["phantomjs.page.settings.userAgent"] = (
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0")
    driver = selenium.webdriver.PhantomJS(
        executable_path=r"D:\phantomjs-2.1.1-windows\bin\phantomjs.exe",
        desired_capabilities=dcap)
    # driver = selenium.webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(5)
    print('go Url')
    html = driver.page_source
    mytree = lxml.etree.HTML(html)
    itemList = mytree.xpath('//div[@id="v-sort"]/div[@class="menus"]//div[@class="item"]')
    # print(str(itemList))
    for item in itemList:
        a = item.xpath("./a/@href")[0]
        newURL = "http://www.oschina.net" + a
        print(newURL)
        task.put(newURL)


    print ("waitting for------")


    for  i  in range(10000):
        res=result.get()
        coll.insert(res)
        print ("get data",res)

    manger.shutdown()#关闭服务器

