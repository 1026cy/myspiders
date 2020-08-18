# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Job51Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    job = scrapy.Field()
    company=scrapy.Field()
    addr = scrapy.Field()
    money = scrapy.Field()
    datetime = scrapy.Field()
    pass
