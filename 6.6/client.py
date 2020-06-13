import socket
import sys
import configparser
import random
import string


def ranstr(num):
    str = 'xyz0123456789'

    salt = ''
    for i in range(num):
        salt += "0"

    return salt

if __name__ == '__main__':
    BUFSIZE = 2048

    ip = sys.argv[1]
    #ip=socket.gethostname()
    port = sys.argv[2]
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #tcp
    #client.bind(ip,int(port))
    #与服务器连接
    ip_port = (ip, int(port))
    client.connect(ip_port)

    config = configparser.ConfigParser()
    config.read("./config.ini")

    MSS=int(config.get("Congestion Control","MSS"))
    Threshold = int(config.get("Congestion Control","Threshold"))
    TriACKRound = int(config.get("Congestion Control","TriACKRound"))
    TimeoutRound = int(config.get("Congestion Control","TimeoutRound"))
    EndRound = int(config.get("Congestion Control","EndRound"))

    round=0
    CongWin=1

    print("初始")
    #RTT circle
    while True:
        round+=1

        print("这是第",round,"个round,目前窗口值为",1024*CongWin,"Bytes")

        #发包
        for i in range(CongWin):
            str=ranstr(MSS)
            client.send(str.encode("utf-8"))
            #print("sent:",str)
        print("共发送",CongWin,"个包，共",CongWin*1024,"Bytes.")
        if CongWin < Threshold:
            if 2*CongWin>Threshold:
                CongWin=Threshold
            else:
                CongWin=2*CongWin
        else:
            CongWin+=1

        if round==TriACKRound:
            #todo
            print("发生了3个ACK！d！！")
            Threshold=int(CongWin/2)
            CongWin=Threshold
        elif round==TimeoutRound:
            print("发生超时！！！")
            Threshold=int(CongWin/2)
            CongWin=1
        elif round==EndRound:
            print("结束轮次")
            break

    #data, server_addr = client.recvfrom(BUFSIZE)
    #print("从服务器端返回了 : ", data.decode())

    client.close()