# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class Job51Pipeline(object):
    def __init__(self):
        self.file = open("msg.txt","w")
        # conn = pymongo.MongoClient(host="10.36.132.36", port=27017)
        # self.db = conn["job51db"]

        pass
    def process_item(self, item, spider):


        self.file.write(str(item)+"\r\n")
        self.file.flush()

        # self.db["job51db"].insert({
        #     "job":item["job"],
        #     "company":item["company"],
        #     "addr":item["addr"],
        #     "money":item["money"],
        #     "datetime":item["datetime"]
        # })
        # print("mongo",item["job"],item["company"],item["addr"],item["money"],item["datetime"])
        #


        return item
    def __del__(self):
        self.file.close()
        pass