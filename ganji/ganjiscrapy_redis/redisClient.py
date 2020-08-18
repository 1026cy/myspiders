import lxml
import lxml.etree
import re
import redis
import requests

def geturllist(url):
    headers = {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0);"}
    response = requests.get(url, headers=headers).content.decode("utf-8")
    # print response
    mytree = lxml.etree.HTML(response)
    restr = re.compile("<span class=\"num\">(\d+)套</span>",re.IGNORECASE)
    num = restr.findall(response)[0]
    num = eval(num)

    # print(num)

    urllist=[]
    pages=0
    if num % 70 == 0:
        pages = num // 70
    else:
        pages = num // 70 + 1
    for i in range(1, pages + 1):
        if i >150:
            break
        urllist.append("http://sz.ganji.com/fang1/o"+str(i)+"p1/")
    # print (urllist)
    return urllist


url = "http://sz.ganji.com/fang1/o1p1/"
urllist = geturllist(url)

myredis=redis.Redis(host="127.0.0.1",port=6379)
print(myredis.info())
for url in urllist:
    myredis.lpush("ganji:start_urls",url)
print("over")