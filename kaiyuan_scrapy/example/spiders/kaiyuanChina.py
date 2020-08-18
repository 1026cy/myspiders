from fake_useragent import UserAgent
from scrapy_redis.spiders import RedisSpider
import re
from example import items
import time
import selenium
import selenium.webdriver
from fake_useragent import UserAgent
class MySpider(RedisSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    name = 'kaiyuan_redis'
    redis_key = 'kaiyuan_redis:start_urls'
    ua=UserAgent()
    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('http://www.oschina.net/project/list/', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(MySpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        # 项目链接
        project_urllist = response.xpath('//div[@class=\"box item\"]/div[@class=\"box-aw\"]/a/@href').extract()
        # 项目标题
        project_titlelist = []
        # print(response.xpath('//div[@class=\"title\"]/text()').extract())
        tree = response.xpath('//div[@class=\"title\"]')
        for t in tree:
            last = ""
            littleTitle_1 = t.xpath('./span/text()').extract()[0]
            littleTitle_2 = t.xpath('./text()').extract()[0].strip()

            last = littleTitle_1 + '——' + littleTitle_2
            project_titlelist.append(last)

        # 项目评分
        value = response.xpath('//footer[@class=\"related box\"]/span[last()]/text()').extract()
        project_valuelist = []
        for i in value:
            i = re.findall('评分 (.*)', i)[0]
            project_valuelist.append(i)
        # 项目收藏
        collection = response.xpath('//footer[@class=\"related box\"]/span[last()-2]/text()').extract()
        project_collectionlist = []
        for i in collection:
            i = re.findall('收藏 (.*)', i)[0]
            project_collectionlist.append(i)

        for u in range(len(project_urllist)):
            myitem = items.KaiyuanzhongguoItem()
            myitem['project_url'] = project_urllist[u]
            myitem['project_title'] = project_titlelist[u]
            myitem['project_value'] = project_valuelist[u]
            myitem['project_collection'] = project_collectionlist[u]

            imgfile = 'D:/demos/python_spider/scrapy project/kaiyuanChina/项目详情截图/' + myitem['project_title'] + '.png'
            myitem['project_infopath'] = imgfile

            yield myitem

            # yield scrapy.Request(myitem["project_url"],meta={"meta":myitem}, #传递数据
            #                      callback=self.parse_page, #进入下一级页面
            #                      headers={
            #                          'User-Agent': ua.random})

    # 详情截图，但是由于速度太慢，先放弃
    # def parse_page(self, response):
    #     myitem = response.meta['meta']
    #     driver = selenium.webdriver.Edge()
    #     driver.get(response.url)
    #     info = driver.find_element_by_id('v-details')
    #     imgfile = 'D:/demos/python_spider/scrapy project/kaiyuanChina/项目详情截图/' + myitem['project_title'] + '.png'
    #     info.screenshot(imgfile)
    #     driver.close()
    #     myitem['project_infopath'] = imgfile
    #     yield myitem
