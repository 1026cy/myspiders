from scrapy import cmdline
# from selenium import webdriver
from selenium import webdriver

cmdline.execute(['scrapy','crawl','yupiaospider'])
# cmdline.execute(['scrapy','crawl','yupiaospider','-o','cto.xml'])
# cmdline.execute(['scrapy','crawl','yupiaospider','-o','51cto.json'])

# positionList=[(-110,-30),(-40,-30),(30,-30),(100,-30),(-110,40),(-40,40),(30,40),(100,40)]
# for i in range(8):
#     print(positionList[i][0],positionList[i][1])

# true=True

# # coding: utf-8
# import requests
#
# def main(api_username, api_password, file_name, api_post_url, yzm_min, yzm_max, yzm_type, tools_token):
#     '''
#             main() 参数介绍
#             api_username    （API账号）             --必须提供
#             api_password    （API账号密码）         --必须提供
#             file_name       （需要打码的图片路径）   --必须提供
#             api_post_url    （API接口地址）         --必须提供
#             yzm_min         （验证码最小值）        --可空提供
#             yzm_max         （验证码最大值）        --可空提供
#             yzm_type        （验证码类型）          --可空提供
#             tools_token     （工具或软件token）     --可空提供
#     '''
#     # api_username =
#     # api_password =
#     # file_name = './1.png'
#     # api_post_url = "http://v1-http-api.jsdama.com/api.php?mod=php&act=upload"
#     # yzm_min = '1'
#     # yzm_max = '8'
#     # yzm_type = '1303'
#     # tools_token = api_username
#
#     # proxies = {'http': 'http://127.0.0.1:8888'}
#     headers = {
#         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#         'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
#         'Accept-Encoding': 'gzip, deflate',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
#         # 'Content-Type': 'multipart/form-data; boundary=---------------------------227973204131376',
#         'Connection': 'keep-alive',
#         'Host': 'v1-http-api.jsdama.com',
#         'Upgrade-Insecure-Requests': '1'
#     }
#
#     files = {
#         'upload': (file_name, open(file_name, 'rb'), 'image/png')
#     }
#
#     data = {
#         'user_name': api_username,
#         'user_pw': api_password,
#         'yzm_minlen': yzm_min,
#         'yzm_maxlen': yzm_max,
#         'yzmtype_mark': yzm_type,
#         'zztool_token': tools_token
#     }
#     s = requests.session()
#     # r = s.post(api_post_url, headers=headers, data=data, files=files, verify=False, proxies=proxies)
#     r = s.post(api_post_url, headers=headers, data=data, files=files, verify=False)
#
#
#     coordinateList=eval(r.text)['data']['val'].split('|')
#
#
#     print(1)
#     for coordinate in coordinateList:
#         print(coordinate.split(',')[0])
#         print(coordinate.split(',')[1])
#
#
#
#
# def download_vcode():
#     try:
#         url = 'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&0.7286443744110989'
#         headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'}
#         s = requests.session()
#         resp = s.get(url, headers=headers, verify=False)
#         file_name = './1.png'
#         with open(file_name, 'wb') as f:
#             f.write(resp.content)
#     except Exception as e:
#         print(e)
#
#
# if __name__ == '__main__':
#     download_vcode()
#     main('yincheng_0755',
#          'yinchengak47.OK',
#          './1.png',
#          "http://v1-http-api.jsdama.com/api.php?mod=php&act=upload",
#          '1',
#          '8',
#          '1303',
#          '')
#
#     '''
#         main() 参数介绍
#         api_username    （API账号）             --必须提供
#         api_password    （API账号密码）         --必须提供
#         file_name       （需要打码的图片路径）   --必须提供
#         api_post_url    （API接口地址）         --必须提供
#         yzm_min         （验证码最小值）        --可空提供
#         yzm_max         （验证码最大值）        --可空提供
#         yzm_type        （验证码类型）          --可空提供
#         tools_token     （工具或软件token）     --可空提供
#     '''
webdriver.Chrome().get_window_size()