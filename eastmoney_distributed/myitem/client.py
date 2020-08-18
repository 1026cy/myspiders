#-*- encoding:utf-8 -*-
import multiprocessing.managers
import baidus
import fenghuangcaijing
import lxml.etree
import sinacaijing
import time
import threading
import queue

from selenium import webdriver

q = queue.Queue()
class QueueManager(multiprocessing.managers.BaseManager):
    pass
def  get_stock_info(url,q,stock):
    try:
        print('调用浏览器')
        driver = webdriver.PhantomJS()
        driver.get(url)
        time.sleep(10)
        data = driver.page_source
        mytree = lxml.etree.HTML(data)
        info = mytree.xpath('//div[@class="data-middle"]/table/tbody//tr//td/text()')
        q.put({stock:info})
        driver.close()
        print('浏览器关闭')
    except Exception as e:
        print('获取股票信息失败',e)

def mian():
    QueueManager.register('get_task')
    QueueManager.register('get_result')
    manager = QueueManager(address=('10.36.132.35', 1057), authkey=111111)
    manager.connect()
    task, result = manager.get_task(), manager.get_result()
    while True:
        try:
            threadlist = []
            stock,url = task.get(timeout=300)
            print('开始线程')
            stock_thtead = threading.Thread(target=get_stock_info,args=(url,q,stock))
            stock_thtead.start()
            threadlist.append(stock_thtead)

            baidus.baidu_result(stock, q)
            fenghuangcaijing.fenghuang_result(stock, q)
            sinacaijing.sina_result(stock, q)


            # #调用百度新闻
            # baidu_thtead = threading.Thread(target=baidus.baidu_result,args=(stock,q))
            # baidu_thtead.start()
            # threadlist.append(baidu_thtead)
            #
            # #调用凤凰财经
            # fenghuang_thtead = threading.Thread(target=fenghuangcaijing.fenghuang_result,args=(stock,q))
            # fenghuang_thtead.start()
            # threadlist.append(fenghuang_thtead)
            #
            # # 调用新浪财经
            # sina_thtead = threading.Thread(target=sinacaijing.sina_result, args=(stock, q))
            # sina_thtead.start()
            # threadlist.append(sina_thtead)
            #
            for t in threadlist:
                t.join()
            resultlist = []
            for i in range(4):
                resultlist.append(q.get())
            result.put(resultlist)
        except:
            pass

if __name__ == '__main__':
    mian()

