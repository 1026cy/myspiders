#-*- encoding:utf-8 -*-
import queue
import multiprocessing  #分布式进程
import multiprocessing.managers #分布式进程管理器
import requests
import lxml
import lxml.etree

task_queue = queue.Queue()
result_queue = queue.Queue()

def return_task():
    return task_queue
def return_result():
    return result_queue

class QueueManager(multiprocessing.managers.BaseManager):
    pass

def get_stock_list(url):
    data = requests.get(url).content.decode('gbk')
    mytree = lxml.etree.HTML(data)
    linelist = mytree.xpath('//div[@id="quotesearch"]//ul//li')
    stocklist = []
    urllist = []
    for line in linelist:
        stocks = line.xpath('./a/text()')[0]
        url = line.xpath('./a/@href')[0]
        stock = stocks.split('(')[0]
        stocklist.append((stock,url))

    return stocklist[36:]


if __name__ == '__main__':
    url = 'http://quote.eastmoney.com/stocklist.html'
    stock_tuples = get_stock_list(url)

    multiprocessing.freeze_support()#开启分布式支持
    QueueManager.register('get_task',callable=return_task)#注册2个函数给客户端使用
    QueueManager.register('get_result',callable=return_result)

    #创建一个管理器,设置地址和密码
    manager = QueueManager(address=('10.36.132.35',1057),authkey=111111)
    manager.start()

    task,result = manager.get_task(),manager.get_result()#任务和结果

    # task.put(('平安银行','http://quote.eastmoney.com/sz000001.html'))
    for stock in stock_tuples:
        task.put(stock)
        print('task add %s'%(str(stock)))

    print('等待结果中-------------------')

    savefile = open('stock.txt','wb')
    while True:
        reslist = result.get(timeout=1000)
        print('result ',reslist)
        savefile.write(str(reslist).encode('utf-8','ignore'))
        savefile.flush()

    savefile.close()
    manager.shutdown()