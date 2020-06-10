import socket
import sys

if __name__ == '__main__':
    BUFSIZE=1024
# bind
    ip=sys.argv[1]
    port=sys.argv[2]
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.bind((ip,int(port)))
    print("Bind UDP on port:", port);

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
