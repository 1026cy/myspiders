# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
class GanjirentscrapyPipeline(object):
    def __init__(self):
        self.file = open("ganjimsg.txt", "w")
        # conn = pymongo.MongoClient(host="127.0.0.1", port=27017)
        # self.db = conn["ganjidb"]

        pass

    def process_item(self, item, spider):
        self.file.write(str(item) + "\r\n")
        self.file.flush()

        # self.db["ganjidb"].insert({
        #     "home":item["home"],
        #     "pattern":item["pattern"],
        #     "addr":item["addr"],
        #     "money":item["money"],
        #     "datetime":item["datetime"]
        # })



        return item

    def __del__(self):
        self.file.close()
        pass

