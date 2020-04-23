# coding=utf-8
# UDP 客户端代码

import socket
from frame import Frame

def newFrame():
    sendFrame = Frame(seq=next_frame_to_send)   # 记录序列号
    sendFrame.genData()                         # 生成随机数据
    sendFrame.buildMainPart()                   # 合成核心部分
    sendFrame.generateCRC()                     # 生成校验和
    sendFrame.addHeadTail()                     # 添加帧头尾
    return sendFrame

if __name__ == '__main__':
    id=0    # 发送帧编号
    next_frame_to_send = 0  # 下一帧序列号

    # 建立连接
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(2)         # 设置非阻塞recv

    sendFrame = newFrame()
    while True:
        temp = [str(x) for x in sendFrame.getFrame()]
        data = ''.join(temp)        # 生成数据字符串

        s.sendto(data.encode('utf-8'), ('127.0.0.1', 8888))
        print("Send frame", next_frame_to_send)

        try:
            event = s.recv(1024)    # 接受ack
        except socket.timeout:      # 无ack返回，超时重发
            continue
        event = event.decode()

        if event == str(next_frame_to_send):                # 正确送达
            next_frame_to_send = next_frame_to_send ^ 1     # 改变序列号
            sendFrame = newFrame()

    s.close()


