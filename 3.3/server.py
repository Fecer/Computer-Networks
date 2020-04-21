#coding=utf-8
#UDP 协议服务器代码
import socket

if __name__ == '__main__':
    # 建立连接
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.bind(('127.0.0.1',8888))
    print("Bind UDP on port:8888")

    while True:
        data,addr=s.recvfrom(1024)
        print("Receive from %s:%s"% addr)

        # if(verifyCRC() == True):
        #     # TODO：区分Seq为0 or 1
        #     s.sendto("ACK".encode()+data,addr)
        # else:
        #     s.sendto("NAK".encode() + data, addr)
