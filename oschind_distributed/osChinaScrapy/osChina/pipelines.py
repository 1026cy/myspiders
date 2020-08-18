# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class OschinaPipeline(object):
    # def __init__(self):
        # self.conn = pymongo.MongoClient(host='127.0.0.1',port=27017)
        # self.db = self.conn['osChingR']
        # self.myColl = self.db['data']
    def process_item(self, item, spider):
        # self.myColl.insert({'title': item['title'], 'summary': item['summary'], 'time': item['time'],
        #                     'protocol': item['protocol'], 'lang': item['lang'],
        #                     'sys': item['sys'], 'auth': item['auth']})
        return item
