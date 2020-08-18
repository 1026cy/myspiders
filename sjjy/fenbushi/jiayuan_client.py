import multiprocessing.managers
import threading
from lxml import etree
import urllib.request
import queue

class QueueManager(multiprocessing.managers.BaseManager):  # 继承。进程管理共享数据
    pass

# 图像列表，信息集合的列表
def get_info(text):
    global img_queue
    tree = etree.HTML(text)

    # name/age/address/height/img/href
    info_list = tree.xpath("//ul[@class=\"user_list fn-clear\"]//li")
    infos_list = []
    for info in info_list:
        if info.xpath(".//img/@src")[0].find("images1") == -1:
            print("get it!")
            name = info.xpath(".//div[@class=\"user_name\"]/a/@title")[0]
            age, address = info.xpath(".//p[@class=\"user_info\"]/text()")[0].split(" ")
            height = info.xpath(".//p[@class=\"zhufang\"]/span/text()")[0]
            img = info.xpath(".//img/@src")[0]
            href_xpath = info.xpath(".//a[@class=\"openBox os_stat\"]/@href")
            href = href_xpath[0] if len(href_xpath) > 0 else None
            info_list = [name, age, address, height, href,img]
            img_queue.put(img)
            infos_list.append(info_list)
            print(info_list)
    return infos_list

# 下载图片
def write2file():
    global img_queue
    url = img_queue.get()
    filepath = "../pic/" + url.split("/")[-1]
    urllib.request.urlretrieve(url,filepath)
    print("done")
    write2file()


if __name__ == '__main__':
    QueueManager.register("get_task")  # 注册函数调用服务器
    QueueManager.register("get_result")  # 结果队列
    manager = QueueManager(address=("10.36.132.23", 12080), authkey=123456)
    manager.connect()
    task, result = manager.get_task(), manager.get_result()  # 获得任务与结果队列

    img_queue = queue.Queue()
    while True:
        try:
            text = task.get()  # 获得任务队列中的数据
            infos_list = get_info(text)
            for i in range(10):
                t = threading.Thread(target=write2file)
                t.start()
            result.put(infos_list)  # 将结果加入结果队列
        except:
            print("fuck")
