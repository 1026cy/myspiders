#-*- encoding:utf-8 -*-
import re
import lxml
import lxml.etree
import requests
from aip import AipNlp
import gevent
import gevent.monkey
# gevent.monkey.patch_all()

class BaiduStock:
    def __init__(self,stock):
        self.stock = stock
        self.countlist = []
        """ 你的 APPID AK SK """
        APP_ID = '10313738'
        API_KEY = '4LtkGbtP7WDWCmObkl5X2eGG'
        SECRET_KEY = 'nr2ZIyRSGFQSH8sSMIPXxhombIpxnAoG'

        self.aipNlp = AipNlp(APP_ID, API_KEY, SECRET_KEY)

    def get_baidu_numbers(self,url):
        print('获取num中...')
        headers = {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            mytree = lxml.etree.HTML(response.text)
            numsstr = mytree.xpath('//span[@class="nums"]/text()')[0]
            regex = re.compile('找到相关新闻约?(.*?)篇', re.IGNORECASE)
            if regex.findall(numsstr)[0].find(',') != -1:
                num = eval(''.join(regex.findall(numsstr)[0].split(',')))
            else:
                num = eval(regex.findall(numsstr)[0])
            print('获取页码', num)
            return num
        return None

    def get_page_title(self,url):
        print('get_page_title')
        headers = {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)'}
        data = requests.get(url, headers=headers).text
        mytree = lxml.etree.HTML(data)
        linelist = mytree.xpath('//div[@class="result title"]')
        resultlist = []
        for line in linelist:
            try:
                em = line.xpath('./h3/a/em/text()')[0]
                titlelist = line.xpath('./h3/a/text()')
                if len(titlelist) == 1:
                    title = em + line.xpath('./h3/a/text()')[0]
                    resultlist.append(title)
                else:
                    title = line.xpath('./h3/a/text()')[0] + em + line.xpath('./h3/a/text()')[1]
                    resultlist.append(title)
            except:
                print('获取title出错')

        self.countlist.append(resultlist)


    def emotion_count(self,titlelist,emotion):
        for line in titlelist:
            try:
                result = self.aipNlp.sentimentClassify(line)
                if result['items'][0]['sentiment'] == 2:
                    emotion += 1
                elif result['items'][0]['sentiment'] == 0:
                    emotion -= 1
                else:
                    pass
            except Exception as e:
                print(e)
        return emotion


    def baidu_result(self):
        print('执行 baidu_result')
        num = self.get_baidu_numbers('http://news.baidu.com/ns?word=' + self.stock + '&pn=0&cl=2&ct=1&tn=newstitle&rn=20')
        if num > 100:
            geventlist = []
            for i in range(5):
                url = 'http://news.baidu.com/ns?word=' + self.stock + '&pn=' + str(i * 20) + '&cl=2&ct=1&tn=newstitle&rn=20'
                geventlist.append(gevent.spawn(self.get_page_title,url))
        else:
            if num % 20 == 0:
                geventlist = []
                for i in range(num // 20):
                    url = 'http://news.baidu.com/ns?word=' + self.stock + '&pn=' + str(
                        i * 20) + '&cl=2&ct=1&tn=newstitle&rn=20'
                    geventlist.append(gevent.spawn(self.get_page_title, url))
            else:
                geventlist = []
                for i in range(num // 20 + 1):
                    url = 'http://news.baidu.com/ns?word=' + self.stock + '&pn=' + str(
                        i * 20) + '&cl=2&ct=1&tn=newstitle&rn=20'
                    geventlist.append(gevent.spawn(self.get_page_title, url))

        gevent.joinall(geventlist)

        emotion = 0
        for item in self.countlist:
            emotion += self.emotion_count(item,emotion)
        # 得出结果进行情感分析
        print('正在进行情感分析....')
        if emotion > 0:
            mydict = {'百度新闻':'情感分析偏正向'}
        elif emotion < 0:
            mydict = {'百度新闻': '情感分析偏负向'}
        else:
            mydict = {'百度新闻': '情感分析偏中性'}

        print(mydict)
        # q.put(mydict)

if __name__ == '__main__':
    mystock = BaiduStock('平安银行')
    print(mystock.baidu_result())
