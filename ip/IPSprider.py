import requests
import time
import pyquery

def getPageData(url):

    headers = {"User-Agent":"Mozilla/5.0 (compatible; MSIE 9.0;Windows NT 6.1; Trident/5.0);"}

    pageData = requests.get(url,headers = headers).text

    pageData = pyquery.PyQuery(pageData)

    return pageData


def getPageUrl(pageData):

    pageNum = pageData.find(".pagination a:nth-last-child(2)").text()
    print(pageNum)

    for i in range(1,11):
        pageUrl = "http://www.xicidaili.com/nn/"+str(i)
        print(pageUrl)
        pageUrlList.append(pageUrl)

def getIpAndPort(pageData,file):

    for table in pageData.find("#ip_list tr.odd").items():

        ip = table.find("td:nth-child(2)").text()
        port = table.find("td:nth-child(3)").text()
        httpTpye = table.find("td:nth-child(6)").text()

        myIP = '"'+ httpTpye + "://" +ip + ":" + port + '"'+'\n'

        file.write(myIP)
        file.flush()

        print(myIP)


    pass


if __name__ == '__main__':
    pageUrlList = []
    ipList = []
    startUrl = r"http://www.xicidaili.com/nn/1"

    pageData = getPageData(startUrl)
    file = open("./代理IP2.txt","a",encoding="utf-8")
    getPageUrl(pageData)
    for url in pageUrlList:
        pageData = getPageData(url)
        getIpAndPort(pageData,file)
    file.close()
