# -*- coding: utf-8 -*-
# @Time    : 2022/4/24
# @Author  : Eric W
# 获取抖音直播间数据流

import uuid
import live_url as liveUrl
import os
import shutil

from playwright.sync_api import sync_playwright as playwright


# 请求直播间获取数据流
def filter_response(response):
    if 'https://live.douyin.com/webcast/im/fetch/' in response.url:
        with open('./douyinLiveFile/' + uuid.uuid4().hex, 'wb') as file:
            print("url data:", response.url)
            file.write(response.body())
    else:
        print("--", response.url)
        pass
    return response


# 打印请求url
def log_request(intercepted_request):
    print("a request was made:", intercepted_request.url)


# 新建浏览器页面
def run(pw):
    # 初始化
    browser = pw.webkit.launch(headless=True)
    # 新建页面
    page = browser.new_page()
    # 开始获取
    page.on("response", filter_response)
    # 直播间地址
    page.goto(liveUrl.url())
    return page


# 开始请求数据流
def start_monitoring():
    with playwright() as pw:
        page = run(pw)
        # 直播间停留时间 单位ms 自行确定,也可以永久驻留
        page.wait_for_timeout(100000000)


# 主程序
if __name__ == '__main__':
    # 清空原来数据流
    if not os.path.exists("douyinLiveFile"):
        os.mkdir("douyinLiveFile")
    else:
        shutil.rmtree("douyinLiveFile")
        os.mkdir("douyinLiveFile")

    # 开始获取
    start_monitoring()
    # https://live.douyin.com/webcast/im/fetch/
