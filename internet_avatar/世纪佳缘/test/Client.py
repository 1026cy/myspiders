# coding:utf-8
'''
世纪佳缘抓取头像
→→→→→→→→本程序用分布式链接，程序启动前请先修改本机地址ip(第60行代码）←←←←←←←
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


# 模拟浏览器获取图片下载
def loadimg(imgurl, title):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'  # 模拟浏览器
    headers = {'User-Agent': user_agent}
    print("下载图片：", i, "------", imgurl)
    req = requests.get(imgurl, headers=headers).content
    with open("img/%s.png" % title, "wb") as file:
        file.write(req)

# 分析网页下载图片
def fromdatagetimg(data):
    global i
    mytree = lxml.etree.HTML(data)
    imgurltree = mytree.xpath("//*[@id=\"normal_user_container\"]")  # 全部列表
    imgurllist = imgurltree[0].xpath("//li/div/div[1]/a/img/@src")  # 提取图片
    print("图片长度：", len(imgurllist))

    # 下载图片
    for img in imgurllist:
        # 每次都会重复加载的图片，予以剔除
        nolist = ["http://at2.jyimg.com/5c/cd/0372304815661ff4b8edec317363/037230481_1_avatar_p.jpg",
                  "http://at2.jyimg.com/d1/1c/b7539981b15a78b8803d6ba4f268/b7539981b_1_avatar_p.jpg",
                  "http://at2.jyimg.com/9e/dc/7745330582af27eaqfab507b3197/774533058_1_avatar_p.jpg"
                  "http://images1.jyimg.com/w4/global/i/zwzp_f.jpg"]
        try:
            if img in nolist:
                pass
            else:
                i += 1
                loadimg(img, i)
        except:
            print("下载图片%d失败"%i)


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
    page = 1  # 用于标记翻页
    i = 0  # 用于标记图片

    while True:
        page += 1
        data = task.get()
        print("get!!!")
        fromdatagetimg(data)
        print("------已提取第%d页头像" % page)
