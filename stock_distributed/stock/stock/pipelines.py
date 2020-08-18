# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

class StockPipeline(object):
    def __init__(self):
        myCon = pymongo.MongoClient(host='127.0.0.1',port=27017)
        db = myCon['stock']
        self.col = db['data']
        self.file = open('stock.txt','w')


    def process_item(self, item, spider):
        self.col.insert({'title':item['title'],'summary':item['summary'],'sentiment':item['sentiment'],'confidence':item['confidence'],'positive_prob':item['positive_prob'],'negative_prob':item['negative_prob']})
        # print(len(item['comm']))
        # if len(item['comm'])==99:
        self.file.write(str(item))
        self.file.write('\n----------')

        return item
    def __del__(self):
        self.file.close()
