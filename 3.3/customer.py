# coding=utf-8
# UDP 客户端代码

import socket


if __name__ == '__main__':

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    for data in ["chenshan", "yuanhui", "chendianqiang"]:
        s.sendto(data.encode(), ('127.0.0.1', 9999))
        print(s.recv(1024))

    s.close()


