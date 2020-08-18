from scrapy_redis.spiders import RedisSpider
from example import  items
import lxml
import lxml.etree
class MySpider(RedisSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    name = 'job51_redis'
    redis_key = 'job51:start_urls'

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('search.51job.com', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(MySpider, self).__init__(*args, **kwargs)

    def parse(self, response):

        mytree = lxml.etree.HTML(response.body)

        joblist = mytree.xpath("//*[@id=\"resultList\"]//div[@class=\"el\"]")

        for line in joblist:
            myitems = items.job51Item()
            job = line.xpath("./p/span/a/text()")[0].strip()
            company = line.xpath("./span[1]/a/text()")[0].strip()
            addr = line.xpath("./span[2]/text()")[0].strip()
            money = line.xpath("./span[3]/text()")
            if len(money) == 0:
                money = ""
            else:
                money = money[0].strip()
            datetime = line.xpath("./span[4]/text()")[0].strip()

            print("--------",job,datetime)
            myitems["job"] = job
            myitems["company"] = company
            myitems["addr"] = addr
            myitems["money"] = money
            myitems["datetime"] = datetime

            # print (job, company, addr, money, date)
            yield myitems

