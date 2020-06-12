import socket
import sys

if __name__ == '__main__':
    BUFSIZE=1024
# bind
    ip=sys.argv[1]
    port=sys.argv[2]
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((ip,int(port)))
    print("Bind TCP on port:", port)
    s.listen(5)

    try:
        while True:
            print("服务器正在运行，等待客户端连接...")

            # 阻塞的建立连接，返回值为该TCP连接的socket和ip端口信息
            client_socket, client_address = s.accept()
            print("客户端连接成功：",client_address)

            try:
                while True:
                    # 接收客户端发来的数据，阻塞，直到有数据到来
                    data = client_socket.recv(2048)
                    if data:
                        print('接收到消息 {}({} bytes) 来自 {}'.format(data.decode('utf-8'), len(data), client_address))
                        # 返回响应数据，将客户端发送来的数据转大写
                        str = data.decode()
                        str = str.upper()
                        print("转换为大写：", str)
                        #发送
                        client_socket.send(str.encode())
                        print("发送消息：",str,"到：",client_address)
                    else:
                        #客户端断开了连接
                        break

            finally:
                # 关闭连接
                client_socket.close()
    finally:
        # 关闭lsocket
        s.close()
    '''
    while True:
        data,addr=s.recvfrom(BUFSIZE)
        print("receive from %s:%s"%addr)
        print("data: ",data)

        #转大写
        str=data.decode()
        str=str.upper()
        print("transform to",str)
        s.sendto(str.encode(),addr)

    s.close()
    '''
