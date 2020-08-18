from scrapy_redis.spiders import RedisSpider
import scrapy
import lxml
import lxml.etree
from selenium.webdriver import DesiredCapabilities
import selenium
import selenium.webdriver
from example import items
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0"
}

class MySpider(CrawlSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    name = 'osChinaRedis'
    allowed_domains = ['dmoz.org']
    # redis_key = 'osChinaRedis:start_urls'

    def start_requests(self):
        url = "https://www.oschina.net/project/zh"
        dcap = dict(DesiredCapabilities.PHANTOMJS)  # 处理无界面浏览器
        dcap["phantomjs.page.settings.userAgent"] = (
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0")
        driver = selenium.webdriver.PhantomJS(
            executable_path=r"D:\phantomjs-2.1.1-windows\bin\phantomjs.exe",
            desired_capabilities=dcap)
        # driver = selenium.webdriver.Chrome()
        driver.get(url)
        driver.implicitly_wait(5)
        print('go Url')
        html = driver.page_source
        mytree = lxml.etree.HTML(html)
        itemList = mytree.xpath('//div[@id="v-sort"]/div[@class="menus"]//div[@class="item"]')
        requestList = []
        for item in itemList:
            a = item.xpath("./a/@href")[0]
            newURL = "http://www.oschina.net" + a
            requestList.append(scrapy.Request(newURL,headers=headers,callback=self.parse_page))
        return requestList


    def parse_page(self, response):
        mytree = lxml.etree.HTML(response.body)
        number = mytree.xpath("//div[@class=\"panel-list news-list\"]//footer//li[7]//text()")[0]
        url = response.url
        for i in range(1, int(number) + 1):
            # https: // www.oschina.net / project / zhlist / 11 / devtools?p = 2  # project-list
            newurl = url + "?p=" + str(i) + "#project-list"
            yield scrapy.Request(newurl,headers=headers,callback=self.parse_content)

    def parse_content(self, response):
        mytree = lxml.etree.HTML(response.body)
        content = mytree.xpath("//div[@class = \"panel-list news-list\"]//a[@class=\"item\"]")
        for text in content:
            item = items.OschinaItem()
            url = text.xpath("./@href")[0]
            title = text.xpath(".//div[@class=\"title\"]//text()")[0].strip()
            summary = text.xpath(".//div[@class=\"summary\"]//text()")[0].strip()
            item['title'] = title
            item['summary'] = summary
            yield scrapy.Request(url,headers=headers,meta={'meta':item},callback=self.parse_detail)

            #dataDicy = {'title': title, 'summary': summary, 'time': time}
    def parse_detail(self,response):
        item = response.meta['meta']
        myTree = lxml.etree.HTML(response.body)
        protocol = ""
        protocolList = myTree.xpath("//section[@class = \"list\"]/div[1]/span/a/text()")
        if len(protocolList):
            protocol = protocolList[0]
        item['protocol'] = protocol

        langList = myTree.xpath("//section[@class = \"list\"]/div[2]/span//a//text()")
        lang = ""
        for l in langList:
            lang += l + '、'
        item['lang'] = lang

        sys = ""
        sysList = myTree.xpath("//section[@class = \"list\"]/div[3]/span//text()")
        if len(sysList):
            sys = sysList[0]
        item['sys'] = sys

        auth=""
        authList = myTree.xpath("//section[@class = \"list\"]/div[4]/a//text()")
        if len(authList):
            auth = authList[0]
        item['auth'] = auth

        myStr = ""
        contentList = myTree.xpath('//div[@class="detail editor-viewer all"]//p/text()')
        for content in contentList:
            myStr += content
        myStr = myStr.replace("\xa0", "")
        myStr = myStr.replace("\n", "")
        myStr = myStr.replace("\t", "")
        myStr = myStr.replace(", ", "")
        item['content'] = myStr

        yield item
