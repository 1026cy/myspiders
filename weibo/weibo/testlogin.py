
import time
import requests
from selenium import webdriver
import re

focus_regex = r"<a bpfilter=\\\"page_frame\\\" href=\\\"\\(.*?)\\\""
focus = re.compile(focus_regex) # 从中挖出有 follow 的值

# 获得登录后的 cookies 登录获得页面+
def get_session(url,cookies):
    print("开始会话=======" + url)
    req = requests.session()  # 会话
    for cookie in cookies:
        req.cookies.set(cookie['name'], cookie["value"])
    req.headers.clear()  # 清空头
    newpage = req.get(url)
    return newpage.text

def get_login_cookies():
    global browser, cookies
    url = "http://weibo.com/login.php"
    browser = webdriver.Chrome()
    browser.get(url)
    time.sleep(3)
    username = browser.find_element_by_id("loginname")
    password = browser.find_element_by_xpath("//div[@class=\"input_wrap\"]/input[@type=\"password\"]")
    login = browser.find_element_by_xpath("//div[@class=\"info_list login_btn\"]/a")
    username.send_keys("***@qq.com")
    time.sleep(1)
    password.send_keys("***")
    time.sleep(2)
    login.click()
    time.sleep(10)
    cookies = browser.get_cookies()  # 抓取全部的cookie
    return cookies


if __name__ == '__main__':
    cookies = get_login_cookies()
    text = get_session(browser.current_url,cookies)

    url_lst = focus.findall(text)
    # 进入关注人列表的链接
    focus_link = "http://weobo.com" + [link for link in url_lst if link.find("follow") != -1][0]

    text = get_session(focus_link,cookies)
    print(text)



