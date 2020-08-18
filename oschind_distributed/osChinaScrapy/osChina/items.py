# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class OschinaItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    summary = scrapy.Field()
    time = scrapy.Field()
    protocol = scrapy.Field()
    lang = scrapy.Field()
    sys = scrapy.Field()
    auth = scrapy.Field()
    content = scrapy.Field()
    pass
