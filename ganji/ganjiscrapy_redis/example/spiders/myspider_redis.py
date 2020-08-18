from scrapy_redis.spiders import RedisSpider
from example import  items
import lxml
import lxml.etree
class MySpider(RedisSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    name = 'ganji_redis'
    redis_key = 'ganji:start_urls'

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('ganji.com', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(MySpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        mytree = lxml.etree.HTML(response.body)
        homelist = mytree.xpath("//*[@class=\"f-list-item ershoufang-list\"]")


        for line in homelist:
            myitems = items.ganjiItem()

            home = line.xpath("./dl/dd[1]/a/text()")[0].strip()

            pattern = ""
            patternlist = line.xpath("./dl/dd[2]//span/text()")
            # print(len(addrlist))
            for i in range(len(patternlist)):
                pattern += patternlist[i].strip()
                pattern.strip()
                # print(add)

            addr = ""
            addr1 = line.xpath("./dl/dd[3]/span//a/text()")
            for i in range(len(addr1)):
                addr += addr1[i].strip()

            money = ""
            moneylist = line.xpath("./dl/dd[5]/div[1]//span/text()")
            for i in range(len(moneylist)):
                money += moneylist[i]
            datetime = line.xpath("./dl/dd[5]/div[2]/text()")[0]

            myitems["home"] = home
            myitems["pattern"] = pattern
            myitems["addr"] = addr
            myitems["money"] = money
            myitems["datetime"] = datetime

            # print (home, pattern, addr, money, date)
            yield myitems





