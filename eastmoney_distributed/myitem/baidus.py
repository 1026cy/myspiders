#-*- encoding:utf-8 -*-
import re
import lxml
import lxml.etree
import requests
from aip import AipNlp


""" 你的 APPID AK SK """
APP_ID = '10313738'
API_KEY = '4LtkGbtP7WDWCmObkl5X2eGG'
SECRET_KEY = 'nr2ZIyRSGFQSH8sSMIPXxhombIpxnAoG'

aipNlp = AipNlp(APP_ID, API_KEY, SECRET_KEY)

def get_baidu_numbers(url):
    print('获取百度num中...')
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
        print('获取百度页码', num)
        return num
    return None

def get_page_title(url):
    print('get_baidupage_title')
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
            print('获取百度title出错')
    return resultlist


def emotion_count(titlelist,emotion):
    for line in titlelist:
        try:
            result = aipNlp.sentimentClassify(line)
            if result['items'][0]['sentiment'] == 2:
                emotion += 1
            elif result['items'][0]['sentiment'] == 0:
                emotion -= 1
            else:
                pass
        except Exception as e :
            print('百度情感分析失败',e)
    return emotion

def baidu_result(stock,q):
    print('执行 baidu_result')
    num = get_baidu_numbers('http://news.baidu.com/ns?word=' + stock + '&pn=0&cl=2&ct=1&tn=newstitle&rn=20')
    emotion = 0
    if num > 100:
        for i in range(5):
            url = 'http://news.baidu.com/ns?word=' + stock + '&pn=' + str(i * 20) + '&cl=2&ct=1&tn=newstitle&rn=20'
            titlelist = get_page_title(url)
            emotion += emotion_count(titlelist,emotion)
    else:
        if num % 20 == 0:
            for i in range(num // 20):
                url = 'http://news.baidu.com/ns?word=' + stock + '&pn=' + str(
                    i * 20) + '&cl=2&ct=1&tn=newstitle&rn=20'
                titlelist = get_page_title(url)
                emotion += emotion_count(titlelist, emotion)
        else:
            for i in range(num // 20 + 1):
                url = 'http://news.baidu.com/ns?word=' + stock + '&pn=' + str(
                    i * 20) + '&cl=2&ct=1&tn=newstitle&rn=20'
                titlelist = get_page_title(url)
                emotion += emotion_count(titlelist, emotion)
    # 得出结果进行情感分析
    print('正在进行百度情感分析....')
    if emotion > 0:
        mydict = {'百度新闻':'情感分析偏正向'}
    elif emotion < 0:
        mydict = {'百度新闻': '情感分析偏负向'}
    else:
        mydict = {'百度新闻': '情感分析偏中性'}
    q.put(mydict)

if __name__ == '__main__':
    pass
    # mystock = BaiduStock('平安银行')
    # print(mystock.baidu_result())
