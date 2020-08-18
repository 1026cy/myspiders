#coding:utf-8
import multiprocessing  #分布式进程
import multiprocessing.managers #分布式进程管理器
import random,time  #随机数，时间
from queue import Queue #队列
import threading
import gevent
import gevent.monkey
import selenium.webdriver
import requests
import lxml
from lxml import etree
# gevent.monkey.patch_all()#自动切换


class  QueueManger(multiprocessing.managers.BaseManager):#继承，进程管理共享数据
    pass

def getData(url):
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0"}
    req = requests.get(url, headers=headers)
    html = req.content.decode("utf-8")
    mytree = lxml.etree.HTML(html)
    number = mytree.xpath("//div[@class=\"panel-list news-list\"]//footer//li[7]//text()")[0]
    print("get" + url)
    newUrlList = []
    for i in range(1, int(number) + 1):
        # https: // www.oschina.net / project / zhlist / 11 / devtools?p = 2  # project-list
        newurl = url + "?p=" + str(i) + "#project-list"
        newUrlList.append(newurl)
    return newUrlList



def makeUrlList(urlList,result):
    myUrlList = [[],[],[]]
    N = len(myUrlList)
    for i in range(len(urlList)):
        myUrlList[i%N].append(urlList[i])
    for myList in myUrlList:
        gevent.spawn(returnData, myList,result).join()


def returnData(urlList,result):
    for url in urlList:
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0"}
        req = requests.get(url, headers=headers)
        print("get-----------" + url)
        html = req.content.decode("utf-8")
        mytree = lxml.etree.HTML(html)
        content = mytree.xpath("//div[@class = \"panel-list news-list\"]//a[@class=\"item\"]")
        for text in content:
            url = text.xpath("./@href")[0]
            title = text.xpath(".//div[@class=\"title\"]//text()")[0].strip()
            summary = text.xpath(".//div[@class=\"summary\"]//text()")[0].strip()
            dataDict = {'title':title,'summary':summary,'url':url}
            data = parse_detail(dataDict)
            result.put(data)
            # file.write(title+' - '+summary+' - '+time)
            # dbColl.insert({'title':title,'summary':summary,'time':time})
            # print(childurl, title[0].strip() + title[1].strip() + "---" + summary[0].strip())

def parse_detail(dataDict):
    title = dataDict['title']
    summary = dataDict['summary']
    url = dataDict['url']
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0"}
    req = requests.get(url, headers=headers)
    print("get-----------" + url)
    html = req.content.decode("utf-8")
    myTree = lxml.etree.HTML(html)
    protocol = ""
    protocolList = myTree.xpath("//section[@class = \"list\"]/div[1]/span/a/text()")
    if len(protocolList):
        protocol = protocolList[0]

    langList = myTree.xpath("//section[@class = \"list\"]/div[2]/span//a//text()")
    lang = ""
    for l in langList:
        lang += l + '、'

    sys = ""
    sysList = myTree.xpath("//section[@class = \"list\"]/div[3]/span//text()")
    if len(sysList):
        sys = sysList[0]

    auth=""
    authList = myTree.xpath("//section[@class = \"list\"]/div[4]/a//text()")
    if len(authList):
        auth = authList[0]

    myStr = ""
    contentList = myTree.xpath('//div[@class="detail editor-viewer all"]//p/text()')
    for content in contentList:
        myStr += content
    myStr = myStr.replace("\xa0", "")
    myStr = myStr.replace("\n", "")
    myStr = myStr.replace("\t", "")
    myStr = myStr.replace(", ", "")
    data = {'title': title, 'summary': summary, 'protocol': protocol, 'sys': sys, 'auth': auth, 'content': myStr}
    return data

if __name__=="__main__":
    QueueManger.register("get_task")  # 注册函数调用服务器
    QueueManger.register("get_result")
    manger = QueueManger(address=("127.0.0.1", 8111), authkey=123456)
    manger.connect()  # 链接服务器
    task = manger.get_task()
    result = manger.get_result()  # 任务，结果
    #
    for  i  in range(150):
        url = task.get()
        newUrlList = getData(url)
        makeUrlList(newUrlList,result)
    #
    #
