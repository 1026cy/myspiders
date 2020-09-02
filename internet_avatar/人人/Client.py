# coding:utf-8
'''
由于人人网系统默认设置，无法查看好友的好友的好友列表
→→→→→→→→本程序用分布式链接，程序启动前请先修改本机地址ip(第26行代码）←←←←←←←
→→→→→→→→本程序用无界面浏览器打开网址，程序启动前请先修改无界面浏览器的地址(第33行代码）←←←←←←←
'''
import multiprocessing  # 分布式进程
import multiprocessing.managers  # 分布式进程管理器
import queue  # 队列
import selenium
import selenium.webdriver
import time
import lxml
import lxml.etree
import requests


class QueueManger(multiprocessing.managers.BaseManager):  # 继承，进程管理共享数据
    pass


if __name__ == "__main__":
    QueueManger.register("get_task")  # 注册函数调用服务器
    QueueManger.register("get_result")
    QueueManger.register("get_resultURL")
    manger = QueueManger(address=("10.36.132.10", 8848), authkey=123456)
    manger.connect()  # 链接服务器
    task = manger.get_task()
    result = manger.get_result()  # 任务，结果
    resultURL = manger.get_resultURL()  # 抓取url

    # 登陆
    path = r"D:\python1701\homework\人人\phantomjs-2.1.1-windows\bin\phantomjs.exe"
    driver = selenium.webdriver.PhantomJS(path)  # 打开无界面浏览器
    driver.get("http://www.renren.com/PLogin.do")
    print("正在登录")
    username = driver.find_element_by_id("email")
    username.send_keys("13726542575")
    time.sleep(1)
    username.send_keys(selenium.webdriver.common.keys.Keys.RETURN)
    password = driver.find_element_by_id("password")
    password.send_keys("zhs314159265")
    time.sleep(1)
    password.send_keys(selenium.webdriver.common.keys.Keys.RETURN)
    elem = driver.find_element_by_id("login")
    elem.click()
    time.sleep(3)
    print("登录成功")

    for i in range(1000):
        time.sleep(1)
        try:
            url = task.get()  # 服务器抓取一个url
            print("抓取", url)
            # 跳转主页
            driver.get(url)
            time.sleep(3)
            # driver.save_screenshot("renren.png")
            title = (driver.title)  # 标题
            data = driver.page_source
            # print(data) #网页源码
            mytree = lxml.etree.HTML(data)
            imgurl = mytree.xpath("//*[@id=\"userpic\"]/@src")  # 获取主页头像
            if len(imgurl) != 0:
                imgurl = imgurl[0]
                myput = []
                myput.append(imgurl)
                myput.append(title)
                result.put(myput)  # 返回图片链接和标题

            friendurl = mytree.xpath("//*[@id=\"frameFixedNav\"]/div/ul/li[7]/a/@href")  # 获取好友列表页面的链接
            friendurl = friendurl[0]
            driver.get(friendurl)
            time.sleep(3)
            data = driver.page_source
            # print(data) #网页源码
            mytree = lxml.etree.HTML(data)
            # 获取所有好友的主页链接，有权限的抓不到
            friendurllist = mytree.xpath("//*[@class=\"username\"]/a/@href")
            if len(friendurllist) != 0:
                for url in friendurllist:
                    print("好友链接：", url)
                    resultURL.put(url)
        except:
            pass
