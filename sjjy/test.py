import time
from selenium import webdriver
from lxml import etree
from urllib import request

def download(url):
    request.urlretrieve(url,"1.jpg")
# reese
if __name__ == '__main__':
    url = "http://login.jiayuan.com/"
    browser = webdriver.Chrome()

    browser.get(url)
    time.sleep(5)
    username = browser.find_element_by_id("login_email")
    password = browser.find_element_by_id("login_password")
    login = browser.find_element_by_id("login_btn")
    time.sleep(3)
    username.send_keys("13622307188")
    time.sleep(1)
    password.send_keys("samsung123fuck")
    time.sleep(1)
    login.click()

    time.sleep(5)

    url = "http://search.jiayuan.com/v2/index.php?key=&sex=f&stc=1:44,2:18.24,23:1,3:155.260&sn=default&sv=1&p=1&pt=575&ft=off&f=select&mt=d"
    browser.get(url)
    time.sleep(5)

    while True:
        tree = etree.HTML(browser.page_source)
        info_list = tree.xpath("//ul[@class=\"user_list fn-clear\"]//li")

        for info in info_list:
            if info.xpath(".//img/@src")[0].find("images1") == -1 :
                print("get it!")
                name = info.xpath(".//div[@class=\"user_name\"]/a/@title")[0]
                age,address = info.xpath(".//p[@class=\"user_info\"]/text()")[0].split(" ")
                height = info.xpath(".//p[@class=\"zhufang\"]/span/text()")[0]
                img = info.xpath(".//img/@src")[0]
                href_xpath = info.xpath(".//a[@class=\"openBox os_stat\"]/@href")
                href = href_xpath[0] if len(href_xpath) > 0 else None
                info_list = [name,age,address,height,img,href]
                print(info_list)
                print("========================>>>>>>>>")

        next_page = browser.find_elements_by_xpath("//div[@class=\"pageclass\"]//li")[-1]
        js = "window.scrollTo(0,10000)"
        browser.execute_script(js)
        next_page.click()
        time.sleep(10)

    browser.close()

    # F:\PythonLoc\homework\Homework1101\sjjy\pic