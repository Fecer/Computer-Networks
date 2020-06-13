import socket
import sys

if __name__ == '__main__':
    BUFSIZE = 1024

    ip = sys.argv[1]
    #ip=socket.gethostname()
    port = sys.argv[2]
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #tcp
    #client.bind(ip,int(port))
    #与服务器连接
    ip_port = (ip, int(port))
    client.connect(ip_port)
    msg = sys.argv[3]

    client.send(msg.encode('utf-8'))

    #data, server_addr = client.recvfrom(BUFSIZE)
    #print("从服务器端返回了 : ", data.decode())

    client.close()