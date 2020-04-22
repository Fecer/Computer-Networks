#coding=utf-8
#UDP 协议服务器代码
import socket
from frame import Frame

#接收方
def dezerocheck(str):
    str=str[8:-8]
    strlist =list(str)
    maxfive=0
    index=0
    while True:
        if strlist[index]=='1':
            maxfive+=1
            if maxfive==5:
                if index+1==len(strlist):
                    strlist.append('0')
                del (strlist[index+1])
                maxfive=0
        else:
            maxfive=0
        index+=1
        if index==len(strlist):
            break
    return ''.join(strlist)

#等待传输
def wait():
    global addr
    data,addr=s.recvfrom(1024)
    data=data.decode()
    data=dezerocheck(data)
    seq=int(data[0])
    #类型转换
    data=data[1:]
    data=[int(x) for x in list(data)]
    r=Frame(seq,data)
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
        r=wait()
        if r!=0:                  #通过crc
            if r.seq==frame_expected:
                frame_expected=1-frame_expected
            else:                 #先前发送的ack丢失了
                print("ack lost!")
            s.sendto(str(1-frame_expected).encode('utf-8'),addr)
            print("got frame ",1-frame_expected)
        else:
            print("frame error!")

        # if(verifyCRC() == True):
        #     # TODO：区分Seq为0 or 1
        #     s.sendto("ACK".encode()+data,addr)
        # else:
        #     s.sendto("NAK".encode() + data, addr)
