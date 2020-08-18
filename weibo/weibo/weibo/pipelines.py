# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class WeiboPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient(host="10.36.132.181", port=27017)
        weibo = self.client.weibo
        self.weibo_relations = weibo.weibo_relation_scrapy

    def __del__(self):
        self.client.close()

    def process_item(self, item, spider):
        focus_dict = {}
        focus_dict["username"] = item["username"]
        info = ["name", "img", "link", "intro"]
        for i in range(len(info)):
            focus_dict[info[i]] = item[info[i]]

        # focus 为 True 为关注，False 为 粉丝
        focus_dict["focus"] = True if item["focus"] else False

        self.weibo_relations.insert(focus_dict)

        self.weibo_relations.insert({"username":item["username"],"infos":item["infos"]})
        print("insert")
        return item
