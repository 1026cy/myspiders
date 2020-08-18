# coding:utf-8
import lxml
from lxml import etree
from selenium.webdriver import DesiredCapabilities

parenturlList = []
import selenium.webdriver
import requests
def download(urllist):
    for url in urllist:
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0"}
        req = requests.get(url, headers=headers)
        html = req.content.decode("utf-8")
        mytree = lxml.etree.HTML(html)
        number = mytree.xpath("//div[@class=\"panel-list news-list\"]//footer//li[7]//text()")[0]
        print("get"+url)
        for i in range(1, int(number) + 1):
            # https: // www.oschina.net / project / zhlist / 11 / devtools?p = 2  # project-list
            newurl = url + "?p=" + str(i) + "#project-list"

            headers = {
                'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0"}
            req = requests.get(newurl, headers=headers)
            print("get-----------"+newurl)
            html = req.content.decode("utf-8")
            mytree = lxml.etree.HTML(html)
            content = mytree.xpath("//div[@class = \"panel-list news-list\"]//a[@class=\"item\"]")
            for text in content:
                childurl = text.xpath("./@href")
                title = text.xpath(".//div[@class=\"title\"]//text()")
                summary = text.xpath(".//div[@class=\"summary\"]//text()")
                time = text.xpath(".//footer//text()")
                print(childurl,title[0].strip()+title[1].strip()+"---"+summary[0].strip())

if __name__ == '__main__':

    url = "https://www.oschina.net/project/zh"
    dcap = dict(DesiredCapabilities.PHANTOMJS)  # 处理无界面浏览器
    dcap["phantomjs.page.settings.userAgent"] = (
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0")
    driver = selenium.webdriver.PhantomJS(
        executable_path=r"F:\qianfeng\codeAll\level3_python\Webpro\phantomjs-2.1.1-windows\bin\phantomjs.exe",
        desired_capabilities=dcap)
    driver.get(url)
    html = driver.page_source
    mytree = lxml.etree.HTML(html)
    titleList = mytree.xpath("//div[@id=\"v-so\"]//a[@class=\"box menu vertical\"]//@title")
    urlList = mytree.xpath("//div[@id=\"v-sort\"]//a[@class=\"box menu vertical\"]//@href")
    parenturlList = []
    for a in urlList:
        newURL = "https://www.oschina.net" + a
        parenturlList.append(newURL)

    download(parenturlList)