import lxml.etree
import redis
import requests

myredis=redis.Redis(host="localhost",port=6379)
print(myredis.info())
url="http://quote.eastmoney.com/stocklist.html"
data = requests.get(url).content.decode('gbk')
mytree = lxml.etree.HTML(data)
linelist = mytree.xpath('//div[@id="quotesearch"]//ul//li')
for line in linelist:
    url = line.xpath('./a/@href')[0]
    print(url)
    myredis.lpush("stock:start_urls", url)
# url = 'http://quote.eastmoney.com/sz000001.html'
# myredis.lpush("stock:start_urls",url)
# print(url)