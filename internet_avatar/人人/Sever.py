# coding:utf-8
'''
由于人人网系统默认设置，无法查看好友的好友的好友列表
→→→→→→→→本程序用分布式链接，程序启动前请先修改本机地址ip(第58行代码）←←←←←←←
→→→→→→→→本程序用无界面浏览器打开网址，程序启动前请先修改无界面浏览器的地址(第68行代码）←←←←←←←
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

# 下载图片
def getimgfromclient(result):
    while True:
        res = result.get()
        imgurl = res[0]
        title = res[1]
        print("get data", res)
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'  # 模拟浏览器
        headers = {'User-Agent': user_agent}
        print("下载图片：", imgurl)
        req = requests.get(imgurl, headers=headers).content
        with open("img/%s.png" % title, "wb") as file:
            file.write(req)


if __name__ == "__main__":
    multiprocessing.freeze_support()  # 开启分布式支持
    QueueManger.register("get_task", callable=return_task)  # 注册函数给客户端调用
    QueueManger.register("get_result", callable=return_result)
    QueueManger.register("get_resultURL", callable=return_resulturl)

    manger = QueueManger(address=("10.36.132.10", 8848), authkey=123456)  # 创建一个管理器，设置地址与密码
    manger.start()  # 开启
    task, result = manger.get_task(), manger.get_result()  # 任务，结果
    resultURL = manger.get_resultURL()  # 接收url
    visitedlist = ["http://www.renren.com/443584012/profile",
                   "http://www.renren.com/profile.do?id=847624154",
                   "http://www.renren.com/profile.do?id=959949488",
                   "http://www.renren.com/profile.do?id=959949716"]

    # 登陆
    path = r"D:\python1701\homework\人人\phantomjs-2.1.1-windows\bin\phantomjs.exe"  # 无界面浏览器位置地址
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

    # 跳转到我的主页
    driver.get("http://www.renren.com/443584012/profile")
    time.sleep(3)
    driver.save_screenshot("renren.png")
    title = (driver.title)  # 标题
    data = driver.page_source
    # print(data) #网页源码
    mytree = lxml.etree.HTML(data)
    imgurl = mytree.xpath("//*[@id=\"userpic\"]/@src")  # 获取主页头像
    imgurl = imgurl[0]
    # print(imgurl)
    friendurl = mytree.xpath("//*[@id=\"frameFixedNav\"]/div/ul/li[7]/a/@href")  # 获取好友列表页面的链接
    friendurl = friendurl[0]
    print(title, imgurl, friendurl)

    driver.get(friendurl)
    time.sleep(3)
    data = driver.page_source
    # print(data) #网页源码
    mytree = lxml.etree.HTML(data)
    friendurllist = mytree.xpath("//*[@class=\"username\"]/a/@href")  # 获取好友的主页链接

    for url in friendurllist:
        print("task add data", url)
        task.put(url)

    threading.Thread(target=getimgfromclient, args=(result,)).start()  # 开启循环接收的线程

    print("waitting for------")

    # 去重
    for i in range(10000):
        resurl = resultURL.get()
        if resurl in visitedlist:
            pass
        else:
            print("get data", resurl)
            task.put(resurl)
            visitedlist.append(resurl)

    manger.shutdown()  # 关闭服务器
