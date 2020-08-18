from scrapy import cmdline
''
if __name__ == '__main__':
    cmdline.execute("scrapy crawl weiborela -o 1.json".split(" "))

