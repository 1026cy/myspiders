import multiprocessing.managers
import queue
import threading
from selenium import webdriver
import time
import gevent
import pymongo

task_queue = queue.Queue()
result_queue = queue.Queue()


def return_task():  # 返回任务队列
    return task_queue

def return_result():
    return result_queue

class QueueManager(multiprocessing.managers.BaseManager):  # 继承。进程管理共享数据
    pass

def write2mongodb(result,info_dbss):
    infos_list =result.get()
    info_list = ["name", "age", "address", "height", "href","img"]
    for line in infos_list:
        info_dict = {}
        for i in range(len(info_list)):
            info_dict[info_list[i]] = line[i]
        info_dbss.insert(info_dict)


if __name__ == "__main__":
    multiprocessing.freeze_support()  # 开启分布式支持
    QueueManager.register("get_task", callable=return_task)  # 注册函数给客户端调用
    QueueManager.register("get_result",callable = return_result)
    manager = QueueManager(address=("10.36.132.23", 12080), authkey=123456)
    manager.start()  # 开启服务器
    task, result = manager.get_task(), manager.get_result()  # 获得任务与结果队列

    client = pymongo.MongoClient(host="10.36.132.181",port=27017)
    jiayuan = client.jiayuan
    info_dbss = jiayuan.info_dbss

    # 登录操作
    url = "http://login.jiayuan.com/"
    browser = webdriver.Chrome()
    browser.get(url)
    time.sleep(5)
    username = browser.find_element_by_id("login_email")
    password = browser.find_element_by_id("login_password")
    login = browser.find_element_by_id("login_btn")
    time.sleep(3)
    username.send_keys("13622307188")
    time.sleep(1)
    password.send_keys("samsung123fuck")
    time.sleep(1)
    login.click()
    time.sleep(5)

    # 切换页面
    url = "http://search.jiayuan.com/v2/index.php?key=&sex=f&stc=1:44,2:18.24,23:1,3:155.260&sn=default&sv=1&p=1&pt=575&ft=off&f=select&mt=d"
    browser.get(url)
    time.sleep(5)

    print("waiting for client connecting...")
    while True:
        try:
            text = browser.page_source
            task.put(text)  # 抛出任务

            next_page = browser.find_elements_by_xpath("//div[@class=\"pageclass\"]//li")[-1]
            js = "window.scrollTo(0,10000)"
            browser.execute_script(js)
            next_page.click()
            time.sleep(5)

            threading.Thread(target=write2mongodb, args=(result, info_dbss)).start() # 获取结果数据，存在阻塞
        except:
            print("fuck")
            browser.refresh()


    manager.shutdown()  # 关闭服务器
