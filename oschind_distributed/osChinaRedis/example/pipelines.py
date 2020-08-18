# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
from datetime import datetime
import pymongo
class ExamplePipeline(object):
    def __init__(self):
        self.conn = pymongo.MongoClient(host='127.0.0.1',port=27017)
        self.db = self.conn['osChingR']
        self.myColl = self.db['data']

    def process_item(self, item, spider):
        item["crawled"] = datetime.utcnow()
        item["spider"] = spider.name
        self.myColl.insert({'title': item['title'], 'summary': item['summary'], 'content': item['content'],
                            'protocol': item['protocol'], 'lang': item['lang'],
                            'sys': item['sys'], 'auth': item['auth']})
        return item
