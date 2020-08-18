import queue

import lxml.etree
import re
import requests
from aip import AipNlp


""" 你的 APPID AK SK """
APP_ID = '10313738'
API_KEY = '4LtkGbtP7WDWCmObkl5X2eGG'
SECRET_KEY = 'nr2ZIyRSGFQSH8sSMIPXxhombIpxnAoG'

aipNlp = AipNlp(APP_ID, API_KEY, SECRET_KEY)

def get_sina_numbers(url):
    print('获取新浪页码中...')
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        mytree = lxml.etree.HTML(response.text)
        numsstr = mytree.xpath('//div[@class="l_v2"]/text()')[0]
        regex = re.compile('找到相关新闻约?(.*?)篇', re.IGNORECASE)
        if regex.findall(numsstr)[0].find(',') != -1:
            num = eval(''.join(regex.findall(numsstr)[0].split(',')))
        else:
            num = eval(regex.findall(numsstr)[0])
        print('获取新浪页码', num)
        return num
    return None


def get_page_title(url):
    print('get_sinapage_title')
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)'}
    data = requests.get(url, headers=headers).text
    mytree = lxml.etree.HTML(data)
    linelist = mytree.xpath('//div[@class="r-info r-info2"]')
    resultlist = []
    for line in linelist:
        try:
            span = line.xpath('./h2/a/span/text()')[0]
            titlelist = line.xpath('./h2/a/text()')
            if len(titlelist) == 1:
                title = span + titlelist[0]
                resultlist.append(title)
            else:
                title = titlelist[0] + span + titlelist[1]
                resultlist.append(title)
            content= line.xpath('./p/text()')[0]
            resultlist.append(content)
        except:
            print('获取新浪title出错')
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
        except Exception as e:
            print('新浪情感分析失败',e)
    return emotion

def sina_result(stock):
    print('执行 sina_result')
    num = get_sina_numbers('http://search.sina.com.cn/?q='+stock+'&range=title&c=news&sort=time&page=1')
    emotion = 0
    if num > 100:
        for i in range(1,6):
            url = 'http://search.sina.com.cn/?q='+stock+'&range=title&c=news&sort=time&page='+str(i)
            titlelist = get_page_title(url)
            emotion += emotion_count(titlelist, emotion)

    else:
        if num % 20 == 0:
            for i in range(1,num // 20+1):
                url = 'http://search.sina.com.cn/?q='+stock+'&range=title&c=news&sort=time&page='+str(i)
                titlelist = get_page_title(url)
                emotion += emotion_count(titlelist, emotion)
        else:
            for i in range(1,num // 20 + 2):
                url = 'http://search.sina.com.cn/?q='+stock+'&range=title&c=news&sort=time&page='+str(i)
                titlelist = get_page_title(url)
                emotion += emotion_count(titlelist, emotion)
    # 得出结果进行情感分析
    print('正在进行新浪情感分析....')
    if emotion > 0:
        return '情感分析偏正向'
    elif emotion < 0:
        return '情感分析偏负向'
    else:
        return '情感分析偏中性'

if __name__ == '__main__':
    q = queue.Queue()
    sina_result('平安银行',q)
    print(q.get())