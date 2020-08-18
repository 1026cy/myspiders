import redis
from fake_useragent import UserAgent
def geturllist(url):
    offset = 0
    urllist=[]
    for i in range(1,2238):
        newurl = 'http://www.oschina.net/project/list?company=0&sort=score&lang=0&recommend=false&p=' +str(i)
        urllist.append(newurl)
    return urllist


myredis=redis.Redis(host='10.36.132.179',password='111111',port=6379)
print(myredis.info())

star_url=['http://www.oschina.net/project/list?company=0&sort=score&lang=0&recommend=false&p=1']
urllist=geturllist(star_url[0])
for url in urllist:
    print(url)
    myredis.lpush("kaiyuanChina_redis:start_urls",url)