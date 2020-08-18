# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class BiliscrapyPipeline(object):
    def __init__(self):
        self.mfile=open("result.txt","wb")
    def __del__(self):
        self.mfile.close()
    def process_item(self, item, spider):
        t=item["hef"]+"||"+item["title"]+"||"+item["img"]+"\r\n"
        self.mfile.write(t.encode("utf-8"))
        return item
