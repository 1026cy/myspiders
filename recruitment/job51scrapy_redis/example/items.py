# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html
import scrapy
from scrapy.item import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join

class job51Item(scrapy.Item):
    # define the fields for your item here like:
    job = scrapy.Field()
    company = scrapy.Field()
    addr = scrapy.Field()
    money = scrapy.Field()
    datetime = scrapy.Field()
    crawled=scrapy.Field()
    spider=scrapy.Field()
    pass


class ExampleItem(Item):
    name = Field()
    description = Field()
    link = Field()
    crawled = Field()
    spider = Field()
    url = Field()


class ExampleLoader(ItemLoader):
    default_item_class = ExampleItem
    default_input_processor = MapCompose(lambda s: s.strip())
    default_output_processor = TakeFirst()
    description_out = Join()
