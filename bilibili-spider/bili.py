import threading
from functools import namedtuple
from concurrent import futures
import time
import csv
import pymysql as pymysql
import requests

#'https://www.bilibili.com/video/av+aid+/?from=search&seid=12629984407957967009'
header = ["aid", "view", "danmaku", "reply", "favorite", "coin", "share"]
Video = namedtuple('Video', header)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3236.0 Safari/537.36'
}
total = 1
result = []
lock = threading.Lock() #定义一个线程锁

def main(url):
    global total
    req = requests.get(url, headers=headers, timeout=6).json()
    time.sleep(0.5)     # 延迟，避免太快 ip 被封
    try:
        data = req['data']
        video = Video(
            data['aid'],        # 视频编号
            data['view'],       # 播放量
            data['danmaku'],    # 弹幕数
            data['reply'],      # 评论数
            data['favorite'],   # 收藏数
            data['coin'],       # 硬币数
            data['share']       # 分享数
        )
        with lock:
            result.append(video)
            print(total)
            total += 1
    except:
        pass

def save():
    #保存至csv
    with open("result.csv", "w", encoding="utf-8") as f:
        f_csv = csv.writer(f)
        f_csv.writerow(header)
        f_csv.writerows(result)

if __name__ == "__main__":
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='314251612', db='ganji', charset='utf8')
    cursor = conn.cursor()
    cursor.execute("create table bilibili(id INT PRIMARY KEY AUTO_INCREMENT,aid varchar(20),view1 int (30),danmaku int (10),reply int (10),favorite int (10),coin int (10),share int (10))")
    urls = ["http://api.bilibili.com/archive_stat/stat?aid={}".format(i)
            for i in range(10000)]
    with futures.ThreadPoolExecutor(32) as executor: #开启多线程
        executor.map(main, urls)
    save()
    for d in range(len(result[0])):
        cursor.execute(
            "insert into bilibili(aid,view1,danmaku,reply,favorite,coin,share) values('%s','%s','%s','%s','%s','%s','%s')" % (
                str(result[0][d]), str(result[1][d]), str(result[2][d]),str(result[3][d]),str(result[4][d]),str(result[5][d]),str(result[6][d])))
        # 提交
        conn.commit()
    conn.close()
