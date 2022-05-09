# -*- coding: utf-8 -*-
# @Time    : 2022/4/24
# @Author  :Eric Wan
# 获取抖音直播间数据流
import uuid
import live_url as liveUrl
import os
import shutil

from playwright.sync_api import sync_playwright as playwright


# 请求直播间获取数据流
def filterResponse(response):
    if 'https://live.douyin.com/webcast/im/fetch/' in response.url:
        with open('./douyinLiveFile/' + uuid.uuid4().hex, 'wb') as file:
            print("url数据写入:", response.url)
            file.write(response.body())
    else:
        # print("--", response.url)
        pass
    return response


# 打印请求url
def log_request(intercepted_request):
    print("a request was made:", intercepted_request.url)


# 新建浏览器页面
def run(pw):
    browser = pw.webkit.launch(headless=True)
    page = browser.new_page()

    page.on("response", filterResponse)
    # 直播间 地址  你们自己写
    page.goto(liveUrl.url())
    return page


# 开始请求数据流
def startMonitoring():
    with playwright() as pw:
        page = run(pw)
        # 直播间停留时间 单位ms 需要你们自己敲定  也可以永久驻留
        page.wait_for_timeout(100000000)


# 主程序
if __name__ == '__main__':
    # 判断文件夹
    if not os.path.exists("douyinLiveFile"):
        os.mkdir("douyinLiveFile")
    else:
        shutil.rmtree("douyinLiveFile")
        os.mkdir("douyinLiveFile")

    startMonitoring()
    # https://live.douyin.com/webcast/im/fetch/
