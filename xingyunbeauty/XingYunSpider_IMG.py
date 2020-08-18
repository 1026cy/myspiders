import re


import request
import time
from selenium import webdriver
from  urllib import request
from xingyunSpider.xingyunNormal import xinyunNormal

urlList = []
imgList = []
newUrlList = []
hasImgList = []
relurlList = []


def getUrl(html):
    try:
        urlList = re.findall(r"<div.*(http://.*?)\/", html, flags=re.I)

        newUrlList.extend(urlList)
    except Exception as e:
        print(e)
        pass


def getrelativeUrl(html):
    path = ""
    #<a href="/u/500200894721" target="_blank" class="textEllipsis name" title="MuL晓青-">MuL晓青-</a>
    try:
        tempList = re.findall(r"<a.*(/u.*?)\"",html,flags=re.I)
        # print("tempList",tempList)
        for url in tempList:
            path = r"http://www.xingyun.cn"+url
            relurlList.append(path)
        print(relurlList)
        urlList.extend(relurlList)
        newUrlList.extend(relurlList)
        return path

    except Exception as e:
        print(e)
        pass


#http://image.baidu.com/search/index?ct=201326592&cl=2&st=-1&lm=-1&nc=1&ie=utf-8&tn=baiduimage&ipn=r&rps=1&pv=&fm=rs3&word=%E7%BE%8E%E5%BE%97%E8%AE%A9%E4%BA%BA%E7%AA%92%E6%81%AF%E7%9A%84%E9%A3%8E%E6%99%AF&oriquery=%E9%A3%8E%E6%99%AF&ofr=%E9%A3%8E%E6%99%AF&sensitive=0

#<input type="hidden" id="msg_1113190_3304854" xypicid="3304854" xytag="xypic" xyindex="2" src="http://piccdn.xingyun.cn/media/users/xingyu/330/48/200201239474_3304854_500.jpg"
def webDiver(url,name):
    try:
        driver = webdriver.PhantomJS()
        driver.get(url)
        driver.implicitly_wait(5)
        #设置执行脚本:滚动屏幕
        driver.execute_script("window.scrollBy(0,10000)")
        time.sleep(3)
        driver.execute_script("window.scrollBy(0,20000)")
        time.sleep(3)
        driver.execute_script("window.scrollBy(0,30000)")
        time.sleep(3)
        driver.execute_script("window.scrollBy(0,40000)")
        time.sleep(5)

        #获取所有html
        html = driver.page_source
        # inputTag = driver.__getattribute__("hidden")
        # print(html)
        # src=.*(http://.*640\.jpg) #<input.*(http://.*500\.jpg)
        # print("imgHtml",html)
        imgList = re.findall(r'<input.*(http://.*500\.jpg)\"', html, flags=re.I)

        print("imgList", imgList)

        if len(imgList) != 0:

            for i in range(len(imgList)):
                print("imgUrl", imgList[i])

                imgName = re.search("http://.*\/(.*\.jpg)", imgList[i], flags=re.I).group(1)
                print(imgName)

                # if imgList[i] not in hasImgList:
                request.urlretrieve(imgList[i], r"./%s/%s" %(name,imgName))

                print(i)

    except Exception as e:
        print(e)
        pass

if __name__ == '__main__':


    myUrl = ""
    #
    # webDiver(myUrl)