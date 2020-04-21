# coding=utf-8
# UDP 客户端代码

import socket
from frame import packet, Frame

if __name__ == '__main__':

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        data = input("请输入内容:")
        s.sendto(data.encode('utf-8'), ('127.0.0.1', 8888))
        print(s.recv(1024))

    s.close()


