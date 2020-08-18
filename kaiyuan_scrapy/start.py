import scrapy
from scrapy import cmdline

cmdline.execute(["scrapy","runspider",r"./example/spiders/tencent.py"])