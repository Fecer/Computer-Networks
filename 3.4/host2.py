# coding=utf-8
# UDP Host2代码

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

    print("Cur Seq: ", seq)
    print("Cur Ack: ", ack)

    crc = CRC.generateCRC(info)     # 生成校验和
    data = crc.copy()               # 整合后的数据
    data.insert(0, ack)
    data.insert(0, seq)

    return data


def between(a, b, c):
    if ((a <= b and b < c) or (c < a and a <= b) or (b < c and c < a)):
        return True
    else:
        return False


def inc(data):
    if (data == MAX_SEQ):
        data = 0
    data += 1
    return data


def send_data(frame, timer, next_frame_to_send):
    temp = [str(x) for x in frame]
    data = ''.join(temp)  # 生成数据字符串
    server.sendto(data.encode('utf-8'), addr)
    print('{:10}\t{}'.format("Whole frame:  ", frame))
    # 计时
    timer[next_frame_to_send] = 1


def resend_data(frame, t, next_frame_to_send):
    temp = [str(x) for x in frame]
    data = ''.join(temp)  # 生成数据字符串
    server.sendto(data.encode('utf-8'), addr)
    print('{:10}\t{}'.format("Whole frame:  ", frame))
    # 重新计时
    t[next_frame_to_send] = 0


# 初始化计时
def initT(t, timer):
    for i in range(MAX_SEQ + 1):
        t.append(0)
        timer.append(0)


# 计时
def calT(totalT, timer, t):
    totalT += 1
    for i in range(MAX_SEQ + 1):
        if timer[i] == 1:
            t[i] += 1   # 时间进行
        else:
            t[i] = 0    # 计时器清零


# 超时重发
def timeout(next_frame_to_send, ack_expected):
    TO = False
    for i in range(MAX_SEQ + 1):
        if 2 <= t[i]:  # 第i个超时，重发
            next_frame_to_send = ack_expected
            TO = True

    return TO, next_frame_to_send


def outputPara():
    print("Ack expected:", ack_expected)
    print("Next frame to send:", next_frame_to_send)
    print("Frame expected:", frame_expected)


if __name__ == '__main__':
    cnt = 1                     # 总帧编号
    counterErr = 10             # 发送帧编号
    counterLost = 6

    next_frame_to_send = 0      # 下一发送帧序列号
    ack_expected = 0            # 等待的ack号
    frame_expected = 0          # 期待的帧编号
    nBuffered = 0               # 暂存的帧数量
    MAX_SEQ = 7                 # 最大序列号
    buffer = ["", "", "", "",
              "", "", "", ""]   # 暂存缓冲区

    totalT = 0  # 总时间
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
    server.settimeout(1)  # 设置非阻塞recv

    print("----------Frame Pair {}----------".format(cnt))
    while True:

        # 计时
        calT(totalT, timer, t)

        print()
        print("「Receive」")
        # Wait for event
        event = ""
        frameLost = False
        try:
            event, addr = server.recvfrom(1024)     # 接收
        except socket.timeout:                      # 无ack返回，超时重发
            print("Frame Lost")
            frameLost = True

        if event == "":
            if frameLost == False:                  # 全部结束
                break
        else:                                       # 收到帧内容
            event = event.decode("utf-8")
            event = [int(x) for x in list(event)]   # 类型转换
            event = delHeadTail(event)              # 去掉头尾

            curSeq = event[0]
            curACK = event[1]
            curInfo = event[2:]

            print("Frame expected:", frame_expected)
            print("Got Seq: ", curSeq)
            print("Got Ack: ", curACK)
            print('{:10}\t{}'.format("Receive frame:", event))

        if frameLost == False:
            # 验证CRC
            if CRC.verifyCRC(curInfo.copy()) == False:  # CRC 错误
                print("Frame CRC error")
            else:                                       # CRC 正确
                if curSeq == frame_expected:            # 接收到对应的帧
                    frame_expected = inc(frame_expected)

        while between(ack_expected, curACK, next_frame_to_send):
            nBuffered -= 1
            timer[ack_expected] = 0  # 停止已接收帧的计时
            ack_expected = inc(ack_expected)

        print("Timer:", t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7])

        cnt += 1
        # 循环结束
        if cnt == 21:
            break
        print("--------------------------------")
        print("----------Frame Pair {}----------".format(cnt))

        # 超时处理
        TIMEOUT, next_frame_to_send = timeout(next_frame_to_send, ack_expected)
        if TIMEOUT:  # 重传
            print("「ReSend」")
            outputPara()
            reSeq = next_frame_to_send
            reACK = (frame_expected + MAX_SEQ) % (MAX_SEQ + 1)
            reInfo = buffer[next_frame_to_send]
            reCRC = CRC.generateCRC(reInfo)
            data = reCRC.copy()
            data.insert(0, reACK)
            data.insert(0, reSeq)
            reFrame = addHeadTail(data)
            resend_data(reFrame, t, next_frame_to_send)
            t[next_frame_to_send] = 0
            next_frame_to_send = inc(next_frame_to_send)
            # # 未启动双向filter
            # counterLost += 1
            # counterErr += 1
            continue

        # 丢弃一帧
        if counterLost == filterLost:
            print("「Send lost」")
            counterLost = 0
        else:  # 正常发送
            if counterErr == filterError:  # 出错一帧
                print("「Send error」")
                sendFrame = newFrame(buffer, next_frame_to_send, nBuffered, frame_expected, MAX_SEQ)
                sendFrame[2] = sendFrame[2] ^ 1
                counterErr = 0
            else:
                print("「Send」")
                outputPara()
                # 正常发送
                sendFrame = newFrame(buffer, next_frame_to_send, nBuffered, frame_expected, MAX_SEQ)
            sendFrame = addHeadTail(sendFrame)
            send_data(sendFrame, timer, next_frame_to_send)
            next_frame_to_send = inc(next_frame_to_send)

            # # 未启动双向filter
            # counterLost += 1
            # counterErr += 1

    print("--------------------------------")
    server.close()
