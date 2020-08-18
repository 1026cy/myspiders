# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import time

from PIL import Image
from scrapy import signals
from scrapy.http.response.html import HtmlResponse
from selenium.webdriver.common.action_chains import ActionChains
import requests


true=True
file_name = './1.png'
goDate=['2017','11','30']
fromStation='深圳'
toStation='邯郸'


def main(api_username, api_password, file_name, api_post_url, yzm_min, yzm_max, yzm_type, tools_token,positionList=None):
    '''
            main() 参数介绍
            api_username    （API账号）             --必须提供
            api_password    （API账号密码）         --必须提供
            file_name       （需要打码的图片路径）   --必须提供
            api_post_url    （API接口地址）         --必须提供
            yzm_min         （验证码最小值）        --可空提供
            yzm_max         （验证码最大值）        --可空提供
            yzm_type        （验证码类型）          --可空提供
            tools_token     （工具或软件token）     --可空提供
    '''
    # api_username =
    # api_password =
    # file_name = 'c:/temp/lianzhong_vcode.png'
    # api_post_url = "http://v1-http-api.jsdama.com/api.php?mod=php&act=upload"
    # yzm_min = '1'
    # yzm_max = '8'
    # yzm_type = '1303'
    # tools_token = api_username

    # proxies = {'http': 'http://127.0.0.1:8888'}
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
        # 'Content-Type': 'multipart/form-data; boundary=---------------------------227973204131376',
        'Connection': 'keep-alive',
        'Host': 'v1-http-api.jsdama.com',
        'Upgrade-Insecure-Requests': '1'
    }

    files = {
        'upload': (file_name, open(file_name, 'rb'), 'image/png')
    }

    data = {
        'user_name': api_username,
        'user_pw': api_password,
        'yzm_minlen': yzm_min,
        'yzm_maxlen': yzm_max,
        'yzmtype_mark': yzm_type,
        'zztool_token': tools_token
    }
    s = requests.session()
    # r = s.post(api_post_url, headers=headers, data=data, files=files, verify=False, proxies=proxies)
    r = s.post(api_post_url, headers=headers, data=data, files=files, verify=False)
    print(r.text)
    coordinateList=eval(r.text)['data']['val'].split('|')

    for coordinate in coordinateList:

        positionList.append((coordinate.split(',')[0],coordinate.split(',')[1]))




class LoginMiddleware(object):
    def process_request(self, request, spider):
        if spider.name == 'yupiaospider':
            if request.url.find('login') != -1:

                spider.driver.get(request.url)
                print("正在访问登录界面")
                spider.driver.find_element_by_id('username').send_keys("*****")
                spider.driver.find_element_by_id('password').send_keys("*****")
                time.sleep(2)
                while True:

                    print('''准备下载图片
                    ************************************************
                    ************************************************
                    ************************************************
                    ************************************************
                    ''')
                    spider.driver.get_screenshot_as_file('./2.png')
                    img=Image.open('./2.png')
                    cropImg=img.crop((345,274,710,512))
                    cropImg.save('./1.png')
                    print('''图片下载完成
                    ************************************************
                    ************************************************
                    ************************************************
                    ************************************************
                    ''')
                    positionList = []

                    main('yincheng_0755',
                         'yinchengak47.OK',
                         './1.png',
                         "http://v1-http-api.jsdama.com/api.php?mod=php&act=upload",
                         '1',
                         '8',
                         '1303',
                         '',
                         positionList)


                    print('-------------------------------------------------------------------')
                    imgelement = spider.driver.find_element_by_class_name('touclick-image')

                    for position in positionList:
                        mouse=ActionChains(spider.driver)
                        mouse.move_to_element_with_offset(imgelement,str(eval(position[0])*4//5),str(eval(position[1])*4//5)).click().perform()


                    spider.driver.find_element_by_id('loginSub').click()
                    time.sleep(3)
                    try:
                        if spider.driver.find_element_by_id('my12306page'):
                            print('登录成功-----------------------------------------------------------------------------')
                            break

                    except Exception as e:
                        print(e)
                        print('登录失败，正在重试==================================================================')

            spider.driver.find_element_by_link_text('客运首页').click()
            time.sleep(0.1)
            spider.driver.find_element_by_name("leftTicketDTO.from_station_name").clear()
            spider.driver.find_element_by_name("leftTicketDTO.from_station_name").send_keys(fromStation)
            spider.driver.find_element_by_id("citem_0").click()

            spider.driver.find_element_by_name("leftTicketDTO.to_station_name").clear()
            spider.driver.find_element_by_name("leftTicketDTO.to_station_name").send_keys(toStation)
            spider.driver.find_element_by_id("citem_0").click()
            #选择出行日期
            spider.driver.find_element_by_name("leftTicketDTO.train_date").click()  # 点击出发日期
            time.sleep(0.1)
            spider.driver.find_element_by_xpath('/html/body/div[7]/div[1]/div[1]/div[2]/input').click()#点击年份选择按钮
            time.sleep(0.1)
            spider.driver.find_element_by_xpath('/html/body/div[7]/div[1]/div[1]/div[2]/div/ul/li[text()='+goDate[0]+']').click()  # 点击年份
            time.sleep(0.1)
            spider.driver.find_element_by_xpath('/html/body/div[7]/div[1]/div[1]/div[1]/input').click()#点击月份选择按钮
            time.sleep(0.1)
            spider.driver.find_element_by_xpath('/html/body/div[7]/div[1]/div[1]/div[1]/ul/li['+goDate[1]+']').click()  # 点击月份
            time.sleep(0.1)
            spider.driver.find_element_by_xpath('/html/body/div[7]/div[1]/div[2]/div['+goDate[2]+']').click()#点击日期选择按钮


            # spider.driver.find_element_by_name("back_train_date").click()
            spider.driver.find_element_by_id('a_search_ticket').click()
            time.sleep(5)
            return HtmlResponse(url=spider.driver.current_url, body=spider.driver.page_source,
                                encoding='utf-8')


class Tie12306SpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
