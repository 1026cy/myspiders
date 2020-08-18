#coding:utf-8
import re
import requests
import lxml
import lxml.etree

def geturllist(url):
    headers = {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0);"}
    response = requests.get(url,headers=headers).content.decode("gbk")

    restr = "<div class=\"rt\">[\s\S]*?共(\d+)条职位[\s\S]*?</div>"
    regex = re.compile(restr, re.IGNORECASE)
    num = eval(regex.findall(response)[0])
    print(num)
    pages = 0
    urllist=[]
    if num % 50 == 0:
        pages = num // 50
    else:
        pages = num // 50 + 1
    for i in range(1, pages + 1):
        urllist.append("http://search.51job.com/list/040000,000000,0000,00,9,99,python,2,"+str(i)+".html")
    return urllist

def pagexpath(url):
    headers = {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0);"}
    response = requests.get(url,headers=headers).content.decode("gbk")
    # print(response)
   	mytree = lxml.etree.HTML(response)

    joblist = mytree.xpath("//*[@id=\"resultList\"]//div[@class=\"el\"]")
    datalist=[]
    for line in joblist:
    	mystr=''
 
        job = line.xpath("./p/span/a/text()")[0].strip()
        company = line.xpath("./span[1]/a/text()")[0].strip()
        addr = line.xpath("./span[2]/text()")[0].strip()
        money = line.xpath("./span[3]/text()")
        if len(money) == 0:
            money = ""
        else:
            money = money[0].strip()
        datetime = line.xpath("./span[4]/text()")[0].strip()


        mystr += str(job)
        mystr += " # "
        mystr += str(company)
        mystr += " # "
        mystr += str(addr)
        mystr += " # "
        mystr += str(money)
        mystr += " # "
        mystr += str(datetime)
        mystr += "\r\n"

        datalist.append(mystr)

    return  datalist

    pass
if __name__ == '__main__':
    url = "http://search.51job.com/list/040000,000000,0000,00,9,99,python,2,3.html"
    mylist = geturllist(url)
    for i in mylist:
        print(i)

    pass