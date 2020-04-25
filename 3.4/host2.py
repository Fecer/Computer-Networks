#coding=utf-8
#UDP Host2代码
import socket
from xml.dom.minidom import parse
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
    cnt = 1     # 总帧编号

    # 获取参数
    DOMTree = parse("config.xml")
    collection = DOMTree.documentElement
    port = int(collection.getElementsByTagName('UDPPort')[0].childNodes[0].data)
    # 建立连接
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.bind(('127.0.0.1', port))
    print("Bind UDP on port:", port)

    frame_expected = 0
    while True:
        print("----------Frame{}----------".format(cnt))
        print("Expect frame", frame_expected)
        r = wait()
        print("Got frame", frame_expected)
        if r != 0:                  # 通过crc验证
            print("Frame CRC right")
            if r.seq == frame_expected:
                frame_expected = 1 - frame_expected
            else:                   # 先前发送的ack丢失了
                print("Ack lost!")
            s.sendto(str(1 - frame_expected).encode('utf-8'), addr)
        else:
            print("Frame CRC error")   # 接收到的帧有错误
        print("---------------------------")
        cnt += 1

