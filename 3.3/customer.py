# coding=utf-8
# UDP 客户端代码

import socket
from xml.dom.minidom import parse
from frame import Frame

def newFrame():
    sendFrame = Frame(seq=next_frame_to_send)   # 记录序列号
    sendFrame.genData()                         # 生成随机数据
    sendFrame.buildMainPart()                   # 合成核心部分
    sendFrame.generateCRC()                     # 生成校验和
    sendFrame.addHeadTail()                     # 添加帧头尾
    return sendFrame

if __name__ == '__main__':
    counterErr = 6          # 发送帧编号
    counterLost = 8
    next_frame_to_send = 0  # 下一帧序列号

    # 获取参数
    DOMTree = parse("config.xml")
    collection = DOMTree.documentElement
    port = int(collection.getElementsByTagName('UDPPort')[0].childNodes[0].data)
    filterError = int(collection.getElementsByTagName('FilterError')[0].childNodes[0].data)
    filterLost = int(collection.getElementsByTagName('FilterLost')[0].childNodes[0].data)

    # 建立连接
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(2)         # 设置非阻塞recv

    sendFrame = newFrame()
    while True:


        if counterLost == 9:            # 丢弃一帧
            print("Frame Lost")
            counterLost = 0
        else:                           # 发送一帧
            temp = [str(x) for x in sendFrame.getFrame()]
            if counterErr == 9:         # 出错一帧
                print("Frame Error")
                counterErr = 0
                temp[9] = str( 1 - int(temp[9]) )  # 生成一个错误

            data = ''.join(temp)  # 生成数据字符串
            s.sendto(data.encode('utf-8'), ('127.0.0.1', port))
            print("Send frame", next_frame_to_send)


        try:
            event = s.recv(1024)    # 接受ack
        except socket.timeout:      # 无ack返回，超时重发
            continue
        event = event.decode()

        if event == str(next_frame_to_send):                # 正确送达
            next_frame_to_send = next_frame_to_send ^ 1     # 改变序列号
            counterErr += 1
            counterLost += 1
            sendFrame = newFrame()

    s.close()


