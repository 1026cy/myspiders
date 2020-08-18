# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
from datetime import datetime
import pymongo
class ExamplePipeline(object):
    def __init__(self):
        client = pymongo.MongoClient('mongodb://zone:111111@10.36.132.179:27017')
        self.db = client
        self.users = self.db['kaiyuanChina']

    def process_item(self, item, spider):
        self.users['kaiyuan'].insert({'project_title': item['project_title'], 'project_url': item['project_url'],'project_value': item['project_value'],'project_collection': item['project_collection'],'project_infopath': item['project_infopath']})
        return item

    def __del__(self):
        self.db.close()  # 关闭数据库