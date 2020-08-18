'''
每天早上8:30分自动去深圳气象局抓取天气信息,然后自动发邮件
'''

import datetime
import json
import time
import smtplib
from email.mime.text import MIMEText
import re
import requests


def sendmail():
    sender = '1057005371@qq.com'
    password = 'wpgsondujyqjbeaa'
    receivers = ['1057005371@qq.com']#收件人列表

    text = get_weather()
    minetext = MIMEText(text)
    minetext['Subject'] = str(datetime.date.today())+'天气预报'
    minetext['From'] = sender
    minetext['To'] = receivers[0]

    try:
        smtpobj = smtplib.SMTP_SSL()
        smtpobj.connect('smtp.qq.com',465)
        smtpobj.login(sender,password)

        #发送邮件
        smtpobj.sendmail(sender,receivers,minetext.as_string())
        smtpobj.quit()
        print('邮件发送成功')
    except Exception as e:
        print('发送失败',e)

def get_weather():
    # mydata = {'random':'0.510564124'}
    url = 'http://www.szmb.gov.cn/data_cache/szWeather/szShangxiabanTipsNew.js?0.8563467795377686'
    headers = {'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)'}
    data = requests.get(url,headers=headers).text

    regex = re.compile('.*',re.I)
    mylist = regex.findall(data)
    mydict = mylist[8].split('=')[1].split(';')[0].strip()
    myjson = json.loads(mydict)['important']
    text = myjson['prompt']+'\n'
    text += '更新时间:'+myjson['ddatetime']
    return text

def runtime(starttime):
    flag = 0
    while True:
        nowtime = datetime.datetime.now()
        if starttime < nowtime < starttime+datetime.timedelta(seconds=1):
            time.sleep(1)
            sendmail()
            flag = 1
        else:
            if flag == 1:
                starttime += datetime.timedelta(days=1)
                flag = 0

if __name__ == '__main__':
    starttime = datetime.datetime(2017,11,4,8,30,0)#定时器,每天早上8:30去爬数据
    print('start',starttime)
    runtime(starttime)