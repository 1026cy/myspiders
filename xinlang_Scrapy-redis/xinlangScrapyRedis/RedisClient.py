
import urllib.request
import urllib
import lxml
import lxml.etree
import re
import redis



def geturllist( url):
    data = urllib.request.urlopen(url).read().decode("gb2312", "ignore")
    mytree = lxml.etree.HTML(data)  # 解析页面，
    url=mytree.xpath("//span[@class=\"pagebox_next\"][1]/a//@href")# 抓取元素
    url=re.findall("\.(/.*?)']",str(url))[0]
    url="http://roll.mil.news.sina.com.cn/col/gjjq"+url
    return url

def pushurl(url):
    print(url)
    url= geturllist(url)  # 压入链接到数据库
    if not url:
        return
    myredis.lpush("xinlang:start_urls", url)
    pushurl(url)

if __name__ == '__main__':
    myredis=redis.Redis(host="localhost",port=6379)
    myredis.flushall()
    start_urls = ['http://roll.mil.news.sina.com.cn/col/gjjq/index_1.shtml']
    #print(geturllist(start_urls[0]))
    # urllist=geturllist(start_urls[0]) #压入链接到数据库
    myredis.lpush("xinlang:start_urls",start_urls[0])
    pushurl(start_urls[0])



