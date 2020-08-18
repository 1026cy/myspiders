# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
from datetime import datetime

class ExamplePipeline(object):
    def __init__(self):
        self.file = open("xinlang.txt", "w",encoding="utf-8")
    def __del__(self):
        self.file.close()

    def process_item(self, item, spider):
        text= item["title"]+"\n"+item["time"]+"\n"+item["url"]+"\n"+ item["content"]+ "\r\n"
        self.file.write(text)
        self.file.flush()
        return item

