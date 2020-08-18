# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
from datetime import datetime
import redis

class ExamplePipeline(object):
    def __init__(self):
        self.StockRedis = redis.Redis(host="127.0.0.1", port=6379, db=0)
    def __del__(self):
        pass
    def process_item(self, item, spider):
        if spider.name=='stock':
            self.StockRedis.lpush("stock:fundFlowUrl", item["fundFlowUrl"])
            self.StockRedis.lpush("stock:newsTitle", item["newsTitle"])
            self.StockRedis.lpush("stock:newsUrl", item["newsUrl"])
            self.StockRedis.lpush("stock:newsTitle", item["newsTitle"])
            self.StockRedis.lpush("stock:newsUrl", item["newsUrl"])
        elif spider.name=='gupiao':
            self.StockRedis.lpush("stock:name", item["name"])
            self.StockRedis.lpush("stock:totalFundNum", item["totalFundNum"])
            self.StockRedis.lpush("stock:flowRate", item["flowRate"])
            self.StockRedis.lpush("stock:maniFundNum", item["maniFundNum"])
            self.StockRedis.lpush("stock:retailFundNum", item["retailFundNum"])
            self.StockRedis.lpush("stock:mainParticipationRate", item["mainParticipationRate"])

        # elif spider.name=='stocknewsurl':
        #     self.StockRedis.lpush("stock:newsTitle", item["newsTitle"])
        #     self.StockRedis.lpush("stock:newsUrl", item["newsUrl"])
        elif spider.name=='stocknews':
            self.StockRedis.lpush("stock:news", item["news"])

        item["crawled"] = datetime.utcnow()
        item["spider"] = spider.name
        return item
