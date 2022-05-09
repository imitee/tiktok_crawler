# -*- coding: utf-8 -*-
# @Time    : 2022/2/18 
# @Author  : Eric W
# 直播数据Socket推送
import os
import time
import socket
import requests as requests
import shutil

from messages import message_pb2
from messages.chat import ChatMessage


def download_img(url, path):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        open(path, 'wb').write(r.content)  # 将内容写入图片
        # print(f"CODE: {r.status_code} download {url} to {path}")  # 返回状态码
        r.close()
        return path
    else:
        print(f"CODE: {r.status_code} download {url} Failed.")
        return "error"


def get_script_dir():
    return os.path.split(os.path.realpath(__file__))[0]


class Socket:
    def send_msg(self):
        address = ('127.0.0.1', 25565)  # Socket服务器地址,根据自己情况修改
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            print("连接服务器")
            s.connect(address)  # 尝试连接服务端
            s.sendall(self.encode())  # 尝试向服务端发送消息
        except Exception:
            print(time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime()) + ' [ERROR] 无法连接到Socket服务器,请检查服务器是否启动')
        s.close()


class Watcher:
    def __init__(self):
        self.monitoringFile = f'{get_script_dir()}/douyinLiveFile'

    def start_watcher(self):
        print("Start Analyze")
        while True:
            files = os.listdir(self.monitoringFile)
            # print(files)
            if files:
                # print("yes")
                for _ in files:
                    filepath = self.monitoringFile + '/' + _

                    with open(filepath, 'rb') as f:
                        # print(f.read())
                        response = message_pb2.Response()
                        response.ParseFromString(f.read())

                    # 获取消息
                    for message in response.messages:
                        if message.method == 'WebcastChatMessage':
                            chat_message = ChatMessage()
                            chat_message.set_payload(message.payload)

                            # userID
                            user_id = chat_message.user().id
                            # user_name
                            user_name = chat_message.user().nickname
                            # 发言
                            content = chat_message.instance.content
                            # 头像
                            user_header_img = chat_message.user().avatarThumb.urlList[0]
                            # 头像下载后的文件地址
                            file_path = download_img(user_header_img, f"{get_script_dir()}/userImages/{user_id}.jpg")
                            data = {
                                "user_id": user_id,
                                "user_name": user_name,
                                "content": content,
                                "user_header_img": user_header_img,
                                "file_path":file_path
                            }
                            # print(user_id, user_name, content, user_header_img)
                            # Socket.send_msg(f"{user_id}\0{content}\0{file_path}")
                            Socket.send_msg(str(data))

                    try:
                        os.remove(filepath)
                    except PermissionError as e:
                        time.sleep(1)
                        os.remove(filepath)

            time.sleep(2)


if __name__ == '__main__':
    if not os.path.isdir(get_script_dir() + "/douyinLiveFile"):
        os.makedirs("douyinLiveFile")
        print("创建视频流文件夹")
    if not os.path.isdir(get_script_dir() + "/userImages"):
        os.makedirs(get_script_dir() + "/userImages")
        print("创建头像文件夹")
    else:
        shutil.rmtree("userImages")
        os.mkdir("userImages")

    Watcher().start_watcher()
