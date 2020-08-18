# coding:utf-8
'''
世纪佳缘抓取头像
→→→→→→→→本程序用分布式链接，程序启动前请先修改本机地址ip(第45行代码）←←←←←←←
→→→→→→→→本程序用无界面浏览器打开网址，程序启动前请先修改无界面浏览器的地址(第50行代码）←←←←←←←
'''
import multiprocessing  # 分布式进程
import multiprocessing.managers  # 分布式进程管理器
import queue  # 队列
import threading
import selenium
import selenium.webdriver
import time
import lxml
import lxml.etree
import requests

task_queue = queue.Queue()  # 任务
result_queue = queue.Queue()  # 结果img
url_queue = queue.Queue()  # 结果url


def return_task():  # 返回任务队列
    return task_queue


def return_result():  # 返回结果队列
    return result_queue


def return_resulturl():  # 返回结果队列
    return url_queue


class QueueManger(multiprocessing.managers.BaseManager):  # 继承，进程管理共享数据
    pass


if __name__ == "__main__":
    multiprocessing.freeze_support()  # 开启分布式支持
    QueueManger.register("get_task", callable=return_task)  # 注册函数给客户端调用
    QueueManger.register("get_result", callable=return_result)
    QueueManger.register("get_resultURL", callable=return_resulturl)

    manger = QueueManger(address=("10.36.132.10", 8848), authkey=123456)  # 创建一个管理器，设置地址与密码
    manger.start()  # 开启
    task, result = manger.get_task(), manger.get_result()  # 任务，结果
    resultURL = manger.get_resultURL()  # 接收url

    path = r"D:\python1701\homework\人人\phantomjs-2.1.1-windows\bin\phantomjs.exe"
    driver = selenium.webdriver.PhantomJS(path)  # 打开无界面浏览器
    driver.get("http://login.jiayuan.com/?channel=200&position=102")
    print("正在获取网页")
    time.sleep(1)

    # 登录
    print("正在登录")
    username = driver.find_element_by_id("login_email")
    username.send_keys("13726542575")
    print("正在输入用户名")
    time.sleep(1)
    password = driver.find_element_by_id("login_password")
    password.send_keys("zhs314159265")
    print("正在输入密码")
    time.sleep(1)
    elem = driver.find_element_by_id("login_btn")
    print("正在确认")
    elem.click()
    time.sleep(3)
    print("登录成功")
    page = 1  # 用于翻页

    # 服务端抓取网页源码给客户端，客户端分析并下载图片
    driver.get(
        "http://search.jiayuan.com/v2/index.php?key=&sex=f&stc=23:1&sn=default&sv=1&p=1&pt=40674&ft=off&f=select&mt=d")
    print("正在转到搜索页面")
    time.sleep(5)
    data = driver.page_source
    task.put(data)
    print("put:1")
    print("---------请开启客户端下载图片---------")
    print("---------请开启客户端下载图片---------")
    print("---------请开启客户端下载图片---------")

    # 循环点击下一页，给客户端发送数据
    while True:
        try:
            page += 1
            next = driver.find_element_by_xpath("/html/body/div[7]/div[1]/div[3]/div[5]/div/ol/li[4]/a")
            next.click()
            print("正在翻页")
            time.sleep(10)
            data = driver.page_source
            task.put(data)
            print("put:",page)
        except:
            print("提取页面失败！")
            continue
