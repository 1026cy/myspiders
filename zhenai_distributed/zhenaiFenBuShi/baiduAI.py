#coding:utf-8
#! ‪C:\Developer\python36\python3.exe
import aip
from aip import AipNlp
from aip import AipFace

""" 你的 APPID AK SK """
APP_ID = '**'
API_KEY = '***'
SECRET_KEY = '****'

aipFace = AipFace(APP_ID, API_KEY, SECRET_KEY)

# print('情感极性分类：'+str(result['items'][0]['sentiment']))#
# print('置信度：'+str(result['items'][0]['confidence']))#6
# print('积极类别的概率：'+str(result['items'][0]['positive_prob']))#7
# 读取图片
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

options = {
    'max_face_num': 1,
    'face_fields': "age,beauty",
}
# 调用人脸属性检测接口
result = aipFace.detect(get_file_content('1.jpg'), options)

print('年龄：'+str(int(result['result'][0]['location']['age'])))
print('颜值：'+str(result['result'][0]['location']['beauty']))

print(result)