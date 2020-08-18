# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class Tie12306Pipeline(object):


    def __init__(self):
        self.file=open("1.txt",'wb')
    def __del__(self):
        self.file.close()

    def process_item(self, item, spider):

        self.file.write(str(item).encode()+'\n'.encode())
