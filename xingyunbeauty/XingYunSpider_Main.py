import requests
import pyquery
import gevent.pool
from xingyunSpider.xingyunNormal import xinyunImgSpider
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import gevent
import time
from gevent import queue,monkey
import os
monkey.patch_all()


'''---------------------------------登录前实现---------------------------------------'''

def getHtml(url):

    html = requests.get(url)
    html = html.text.encode(html.encoding).decode("utf-8")
    html = pyquery.PyQuery(html)



    # html = myWebdriver.get(url)
    #
    # html = myWebdriver.page_source
    # print(html)
    return html
    pass

def getName(myWebdirver):

    nameList = myWebdirver.find_elements_by_css_selector("#userDetailsList > div.userDetailsList2 > div > div.user_name > a")
    print(nameList)
    for name in nameList:
        allNameList.append(name.text)
        # yield name.text
    pass

def getIntro(myWebdirver):

    introList = myWebdirver.find_elements_by_css_selector("#userDetailsList > div.userDetailsList2 > div > div.textEllipsis.text_info")

    for intro in introList:
        allIntroList.append(intro.text)
        # print(intro.text)
        # yield intro.text



def getPageUrl(myWebdriver,num):

    pageUrl = myWebdriver.find_elements_by_class_name("page")[0]
    p=pageUrl.find_element_by_link_text(str(num))
    print(p.text)
    # time.sleep(5)
    p.send_keys(Keys.ENTER)

    return p



def getAllUrl(myWebdriver):

    tempList = myWebdriver.find_elements_by_css_selector("#userDetailsList > div.userDetailsList2 > div > div.user_name > a")

    for u in tempList:
        # if u not in allUrlList:
        url = u.get_attribute("href")
        urlList.append(url)
        allUrlList.append(url)

        # print(url)




'''-------------------------------------登录后实现--------------------------------------'''

def login():
    pass


def getFocus(html):
    pass

def sendMessages(html):
    pass


def go(url):

    myWebdriver = selenium.webdriver.PhantomJS()
    myWebdriver.get(url)
    try:
        for i in range(10,39):

            geventList=[]
            print("第%s页"%(str(i)))
            getPageUrl(myWebdriver,i)
            # print(p.text)
            time.sleep(10)
            getName(myWebdriver)
            # html=getHtml(url)
            getAllUrl(myWebdriver)
            getIntro(myWebdriver)
            print(len(allUrlList))

        if len(urlList) != 0:
            numList = []
            # gevent.joinall([
            #     gevent.spawn(myGevent),
            #     gevent.spawn(myGevent),
            #     gevent.spawn(myGevent),
            #     gevent.spawn(myGevent),
            #     gevent.spawn(myGevent),
            #
            #                 ])
            #

            # for i in range(len(allNameList)):
            #     geventList.append(gevent.spawn(myGevent))
            #
            # gevent.joinall(geventList)
            for i in range(len(urlList)):
                numList.append(i)

            pool = gevent.pool.Pool(50)


            pool.map(myGevent,numList)



    except:
        pass


    myWebdriver.close()

def myGevent(num):
    # if len(urlList) != 0:
        # for i in range(len(urlList)):

    temp =  num
    try:
        name = allNameList.pop(0) + "_" + allIntroList.pop(0)
        path = "./" + name
        os.mkdir(path)
        myUrl = urlList.pop(0)
        xinyunImgSpider.webDiver(myUrl, name)

    except:
        pass




if __name__ == '__main__':

    urlList = []
    pageUrlList = []
    allUrlList = []
    allNameList = []
    allIntroList = []
    allImgList = []
    startUrl = r"http://www.xingyun.cn/elites/1"

    # html = getHtml(startUrl)
    # name = getName(html)
    # intro = getIntro(html)
    # print(name,intro)
    # getPageUrl(startUrl)
    go(startUrl)

    print("Done!")
