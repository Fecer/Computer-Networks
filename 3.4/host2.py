#coding=utf-8
#UDP Host2代码

import socket
from xml.dom.minidom import parse
import numpy as np
import CRC

# 添加头尾
def addHeadTail(str):
    return ([0, 1, 1, 1, 1, 1, 1, 0] + str + [0, 1, 1, 1, 1, 1, 1, 0])

# 掐头去尾
def delHeadTail(str):
    return str[8:-8]

def from_network_layer(buffer, next_frame_to_send, nBuffered):
    buffer[next_frame_to_send] = list(np.random.randint(0, 2, 8))  # 产生数据
    nBuffered += 1

def newFrame(buffer, next_frame_to_send, nBuffered, frame_expected, MAX_SEQ):
    from_network_layer(buffer, next_frame_to_send, nBuffered)

    # 帧属性
    info = buffer[next_frame_to_send]                   # 待发送的信息
    seq = next_frame_to_send                            # 序列号
    ack = (frame_expected + MAX_SEQ) % (MAX_SEQ + 1)    # ACK号

    crc = CRC.generateCRC(info)  # 生成校验和
    data = crc.copy()  # 整合后的数据
    data.insert(0, ack)
    data.insert(0, seq)

    return data

def between(a, b, c):
    if ((a <= b and b < c) or (c < a and a <= b) or (b < c and c < a)):
        return True
    else:
        return False

def inc(data):
    if(data == MAX_SEQ):
        data = 0
    data += 1
    return data

def send_data(frame, timer, next_frame_to_send):
    temp = [str(x) for x in frame]
    data = ''.join(temp)  # 生成数据字符串
    server.sendto(data.encode('utf-8'), addr)
    print('{:10}\t{}'.format("Send frame:  ", frame))
    # 计时
    timer[next_frame_to_send] = 1

def resend_data(frame, t, next_frame_to_send):
    temp = [str(x) for x in frame]
    data = ''.join(temp)  # 生成数据字符串
    server.sendto(data.encode('utf-8'), addr)
    print('{:10}\t{}'.format("Send frame:  ", frame))
    # 重新计时
    t[next_frame_to_send] = 0

# 初始化计时
def initT(t, timer):
    for i in range (MAX_SEQ + 1):
        t.append(0)
        timer.append(0)

# 计时
def calT(totalT, timer, t):
    totalT += 1
    for i in range(MAX_SEQ + 1):
        if timer[i] == 1:
            t[i] += 1           # 时间进行
        else:
            t[i] = 0            # 计时器清零

# 超时重发
def timeout(next_frame_to_send, ack_expected):
    TO = False
    for i in range(MAX_SEQ + 1):
        if MAX_SEQ <= t[i]:     # 第i个超时，重发
            next_frame_to_send = ack_expected
            TO = True

    return TO


if __name__ == '__main__':
    cnt = 1                     # 总帧编号
    counterErr = 10             # 发送帧编号
    counterLost = 8

    next_frame_to_send = 0      # 下一发送帧序列号
    ack_expected = 0            # 等待的ack号
    frame_expected = 0          # 期待的帧编号
    nBuffered = 0               # 暂存的帧数量
    MAX_SEQ = 7                 # 最大序列号
    buffer = ["", "", "", "",
              "", "", "", ""]  # 暂存缓冲区

    totalT = 0                  # 总时间
    t = []
    timer = []
    initT(t, timer)

    # 获取参数
    DOMTree = parse("config.xml")
    collection = DOMTree.documentElement
    port = int(collection.getElementsByTagName('UDPPort')[0].childNodes[0].data)
    filterError = int(collection.getElementsByTagName('FilterError')[0].childNodes[0].data)
    filterLost = int(collection.getElementsByTagName('FilterLost')[0].childNodes[0].data)

    # 建立连接
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip_port = ("127.0.0.1", port)
    server.bind(ip_port)
    server.settimeout(2)         # 设置非阻塞recv

    print("----------Frame{}----------".format(cnt))
    while True:

        # 计时
        calT(totalT, timer, t)

        # Wait for event
        event = ""
        try:
            event, addr = server.recvfrom(1024)         # 接收
        except socket.timeout:                          # 无ack返回，超时重发
            break
        event = event.decode("utf-8")
        # event = delHeadTail(event)            # 去掉头尾
        event = [int(x) for x in list(event)]   # 类型转换
        print('{:10}\t{}'.format("Receive frame:", event))

        curSeq = event[0]
        curACK = event[1]
        curInfo = event[2:]

        # 验证CRC
        if CRC.verifyCRC(curInfo.copy()) == False:    # CRC 错误
            print("Frame CRC error")

        if curSeq == frame_expected:        # 接收到对应的帧
            frame_expected = inc(frame_expected)

        while between(ack_expected, curACK, next_frame_to_send):
            nBuffered -= 1
            timer[ack_expected] = 0         # 停止已接收帧的计时
            ack_expected = inc(ack_expected)

        # 超时处理
        if timeout(next_frame_to_send, ack_expected):
            reSeq = next_frame_to_send
            reACK = (frame_expected + MAX_SEQ) % (MAX_SEQ + 1)
            reInfo = buffer[next_frame_to_send]
            reCRC = CRC.generateCRC(reSeq + reACK + reInfo)
            reFrame = reSeq + reACK + reInfo + reCRC
            resend_data(reFrame, t, next_frame_to_send)
            continue

        print("---------------------------")
        cnt += 1
        print("----------Frame{}----------".format(cnt))
        # 发送
        sendFrame = newFrame(buffer, next_frame_to_send, nBuffered, frame_expected, MAX_SEQ)
        send_data(sendFrame, timer, next_frame_to_send)
        next_frame_to_send = inc(next_frame_to_send)

    print("---------------------------")
    server.close()


