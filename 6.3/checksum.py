import configparser

def analysisip(ipaddress="255.255.255.255"):
    #解析ip地址到二进制串
    ip_list=ipaddress.split(".")
    ipstring=[bin(int(i))[2:].zfill(8) for i in ip_list]
    return "".join(ipstring)

if __name__ == '__main__':

    config=configparser.ConfigParser()
    config.read("./config.ini")

    tcpheader=config.get("tcpsegment","headerstring")
    tcpsegment=config.get("tcpsegment","segmentstring")

    print(tcpheader)
    print(tcpsegment)

    sip=config.get("ip","Sourceip")
    dip=config.get("ip","Destinationip")

    print("Source IP:",sip)
    print("Destination IP:",dip)
#32位源IP地址、32位目的IP地址、8位保留字节(置0)、8位传输层协议号(TCP是6，UDP是17)、16位报文长度(首部+数据)。
    #pseudo

    pseudo_sip=analysisip(sip)
    pseudo=pseudo_sip

    pseudo_dip=analysisip(dip)
    pseudo=pseudo+pseudo_dip

    pseudo_res="00000000"
    pseudo+=pseudo_res

    pseudo_ptc="00000110"#tcp
    pseudo+=pseudo_ptc

    pseudo_len=bin(int(len(tcpheader+tcpsegment)/2))[2:].zfill(16)
    pseudo+=pseudo_len

    print("--------Pseudo Header---------")
    print("Source IP:",sip,"(",pseudo_sip,")")
    print("Destination IP",dip,"(",pseudo_dip,")")
    print("Reserved:","0","(",pseudo_res,")")
    print("Protocol:","6","(",pseudo_ptc,")")
    print("Total Length:",len(tcpheader+tcpsegment)/2,"(",pseudo_len,")")

    #TCP
    #source port
    source_port=int(tcpheader[:4],16)
    des_port=int(tcpheader[4:8],16)
    seq_number=int(tcpheader[8:16],16)
    ack_number=int(tcpheader[16:24],16)
    header_len=int(tcpheader[24],16)*4
    reserved=0
    #flags
    flags=bin(int(tcpheader[26:28],16))[2:]
    (CWR,ECE,URG,ACK,PSH,RST,SYN,FIN)=list(flags.zfill(8))
    window_size=int(tcpheader[28:32],16)
    checksum=tcpheader[32:36]
    urgent_pointer=int(tcpheader[36:40],16)
    #option=tcpheader[40:len(tcpheader)+1]
    print("---------TCP Header--------")
    print("Source Port:",source_port)
    print("Destination Port:",des_port)
    print("Sequence Number:",seq_number)
    print("Ack number:",ack_number)
    print("Header length:",header_len)
    print("Reserved:",reserved)
    print("---Flags---")
    print("CWR=",CWR," ECE=",ECE," URG=",URG," ACK=",ACK," PSH=",PSH," RST=",RST," SYN=",SYN," FIN=",FIN)
    print("-----------")
    print("Window Size Value:",window_size)
    print("Checksum:",checksum)
    print("Urgent pointer:",urgent_pointer)

    print("---------Checksum--------")
    #checksum to 0
    tcpheader=tcpheader[:32]+"0000"+tcpheader[36:]
    check_str=hex(int(hex(int(pseudo,2))[2:]+tcpheader+tcpsegment,16))[2:] #转换为16进制
    if len(check_str)% 4 !=0:
        check_str+="00"

    sum=0
    l=len(check_str)
    e=len(tcpheader)
    n=len(tcpsegment)
    for i in range(int(len(check_str)/4)):
        sum+=int(check_str[4*i:4*i+4],16)
    while sum>>16:
        high_sum=sum>>16
        sum&=0xffff
        sum+=high_sum

#取反
    sum=65535-sum
    print("checksum: ",hex(sum))



