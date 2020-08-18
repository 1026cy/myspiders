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


def get_fenghuang_numbers(url):
    print('获取凤凰页码中...')
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        mytree = lxml.etree.HTML(response.text)
        numsstr = mytree.xpath('//p[@class="result"]/text()')[0]
        regex = re.compile('获得约 (.*?)条结果', re.IGNORECASE)
        if regex.findall(numsstr)[0].find(',') != -1:
            num = eval(''.join(regex.findall(numsstr)[0].split(',')))
        else:
            num = eval(regex.findall(numsstr)[0])
        print('获取凤凰页码', num)
        return num
    return None


def get_page_title(url):
    print('get_fenghuangpage_title')
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)'}
    try:
        data = requests.get(url, headers=headers, timeout=300).text
        mytree = lxml.etree.HTML(data)
        linelist = mytree.xpath('//div[@class="searchResults"]')
    except Exception as e:
        print('获取凤凰网失败', e)

    resultlist = []
    for line in linelist:
        try:
            titlelist = line.xpath('./p/a/text()')
            title = ''
            for i in range(len(titlelist)):
                title += titlelist[i]
            contents = line.xpath('.//p[2]/text()')
            content = ''
            for i in range(len(contents)):
                content += contents[i]
            resultlist.append(title)
            resultlist.append(content)
        except Exception as e:
            print('获取凤凰title出错', e)
    return resultlist


def emotion_count(titlelist, emotion):
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
            print('凤凰情感分析失败', e)
    return emotion


def fenghuang_result(stock, q):
    print('执行 sina_result')
    num = get_fenghuang_numbers('http://search.ifeng.com/sofeng/search.action?q=' + stock + '&p=1')
    emotion = 0
    if num > 100:
        for i in range(1, 6):
            url = 'http://search.ifeng.com/sofeng/search.action?q=' + stock + '&p=' + str(i)
            titlelist = get_page_title(url)
            emotion += emotion_count(titlelist, emotion)

    else:
        if num % 20 == 0:
            for i in range(1, num // 20 + 1):
                url = 'http://search.ifeng.com/sofeng/search.action?q=' + stock + '&p=' + str(i)
                titlelist = get_page_title(url)
                emotion += emotion_count(titlelist, emotion)
        else:
            for i in range(1, num // 20 + 2):
                url = 'http://search.ifeng.com/sofeng/search.action?q=' + stock + '&p=' + str(i)
                titlelist = get_page_title(url)
                emotion += emotion_count(titlelist, emotion)
    # 得出结果进行情感分析
    print('正在进行凤凰情感分析....')
    if emotion > 0:
        mydict = {'凤凰财经': '情感分析偏正向'}
    elif emotion < 0:
        mydict = {'凤凰财经': '情感分析偏负向'}
    else:
        mydict = {'凤凰财经': '情感分析偏中性'}
    q.put(mydict)


if __name__ == '__main__':
    q = queue.Queue()
    fenghuang_result('平安银行', q)
    print(q.get())
