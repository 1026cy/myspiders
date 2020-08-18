import lxml
import lxml.etree
import re
import redis
import requests

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


url = "http://search.51job.com/list/040000,000000,0000,00,9,99,python,2,3.html"
urllist = geturllist(url)

myredis=redis.Redis(host="127.0.0.1",port=6379)
print(myredis.info())
for url in urllist:
    myredis.lpush("job51:start_urls",url)
print("over")