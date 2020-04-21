#coding=utf-8
#UDP 协议服务器代码
import socket

s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

s.bind(('127.0.0.1',9999))
print("Bind UDP on port:9999")

while True:
    data,addr=s.recvfrom(1024)
    print("Receive from %s:%s"% addr)
    s.sendto("Hello ".encode()+data,addr)