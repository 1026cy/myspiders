import re


if __name__ == '__main__':
    file = open("1.txt", "r", encoding="utf8")
    text = file.read()

    # url = '''<a bpfilter="page_frame" href="/1962742591/follow?rightmod=1&amp;wvr=6" class="S_txt1"><strong node-type="follow">211</strong><span class="S_txt2">关注</span></a>'''
    # <a bpfilter=\"page_frame\" href=\"\/1962742591\/fans?rightmod=1&wvr=6\" class=\"S_txt1\">
    # a = re.findall("<a bpfilter=\"page_frame\" href=\\\\\"(.*?)\"",text)
    # text = r'''<li class=\"S_line1\"><a bpfilter=\"page_frame\" href=\"\/1962742591\/follow?rightmod=1&wvr=6\" '''

    # http://weibo.com/u/1962742591/home
    # \\/1962742591\\/follow?rightmod=1&wvr=6\\
    # 挖出关注人的正则
    a = re.findall(r"<a bpfilter=\\\"page_frame\\\" href=\\\"\\(.*?)\\\"", text)

    for i in a:
        if i.find("follow") != -1:
            b = i
            print(b)

    # url = "http://" + a if a.startswith("weibo") else "http://weibo.com" + a
    print(a)
    print(b)
