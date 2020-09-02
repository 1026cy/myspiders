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
    # print(p)
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

def login(webdriver):
    loginBtn = webdriver.find_element_by_css_selector("body > header > div > div.operate > a.button.loginBtn")
    loginBtn.send_keys(Keys.ENTER)
    time.sleep(1)
    webdriver.find_element_by_css_selector("#mobile").send_keys("***")
    time.sleep(3)
    webdriver.find_element_by_css_selector("#pwd").send_keys("*****")
    time.sleep(1)

    webdriver.find_element_by_css_selector("#xingyun_Login").click()

    pass


def getFocus(webdriver):
    allFocus = webdriver.find_elements_by_css_selector("#btnWrap > a")
    print(allFocus)

    for f in allFocus:
        print(f)
        f.click()


def sendMessages(html):
    pass


def go(url):

    myWebdriver = selenium.webdriver.Chrome()
    myWebdriver.get(url)
    try:

        for i in range(1, 39):
            numList = []
            geventList = []
            print("第%s页" % (str(i)))
            getPageUrl(myWebdriver, i)
            # print(p.text)
            time.sleep(10)
            # getName(myWebdriver)
            getAllUrl(myWebdriver)
            # getIntro(myWebdriver)
            login(myWebdriver)
            tempNum = len(urlList)

            for i in range(tempNum):

                url = urlList.pop(0)
                myWebdriver.get(url)
                getFocus(myWebdriver)

    except:
        pass


    # myWebdriver.close()

def myGevent(num):
    # if len(urlList) != 0:
        # for i in range(len(urlList)):

    temp =  num

    name = allNameList.pop(0) + "_" + allIntroList.pop(0)
    path = "./" + name
    os.mkdir(path)
    myUrl = urlList.pop(0)
    xinyunImgSpider.webDiver(myUrl, name)



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
