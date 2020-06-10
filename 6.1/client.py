import socket
import sys

if __name__ == '__main__':
    BUFSIZE = 1024

    ip = sys.argv[1]
    port = sys.argv[2]
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #client.bind(ip,int(port))

    msg = sys.argv[3]
    ip_port = (ip,int(port))
    client.sendto(msg.encode('utf-8'), ip_port)

    data, server_addr = client.recvfrom(BUFSIZE)
    print("receive from server ", server_addr,": ", data.decode())

    client.close()