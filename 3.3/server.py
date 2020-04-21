#coding=utf-8
#UDP 协议服务器代码
import socket

s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

s.bind(('127.0.0.1',8888))
print("Bind UDP on port:8888")

while True:
    data,addr=s.recvfrom(1024)
    print("Receive from %s:%s"% addr)
    s.sendto("ACK".encode()+data,addr)
