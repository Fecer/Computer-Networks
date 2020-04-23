#coding=utf-8
#UDP 协议服务器代码
import socket
from frame import Frame

# 掐头去尾
def delHeadTail(str):
    # str = str[8:-8]
    # strlist = list(str)
    # maxfive=0
    # index=0
    # while True:
    #     if strlist[index]=='1':
    #         maxfive+=1
    #         if maxfive==5:
    #             if index+1==len(strlist):
    #                 strlist.append('0')
    #             del (strlist[index+1])
    #             maxfive=0
    #     else:
    #         maxfive=0
    #     index+=1
    #     if index==len(strlist):
    #         break
    return str[8:-8]

# 等待传输
def wait():
    global addr
    data,addr = s.recvfrom(1024)
    data = data.decode()
    data = delHeadTail(data)
    seq = int(data[0])
    # 类型转换
    data = [int(x) for x in list(data)]
    r = Frame(seq,data=data)
    #验证cksum
    if r.verifyCRC() == False:
        return 0
    else:
        return r

if __name__ == '__main__':
    # 建立连接
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.bind(('127.0.0.1',8888))
    print("Bind UDP on port:8888")

    frame_expected = 0
    while True:
        r = wait()
        if r != 0:                  # 通过crc验证
            if r.seq == frame_expected:
                frame_expected = 1 - frame_expected
            else:                   # 先前发送的ack丢失了
                print("Ack lost!")
            s.sendto(str(1 - frame_expected).encode('utf-8'), addr)
            print("Ack frame ",1 - frame_expected)
        else:
            print("Frame error!")   # 接收到的帧有错误

