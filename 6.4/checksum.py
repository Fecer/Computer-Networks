import configparser

def analysisip(ipaddress="255.255.255.255"):
    #解析ip地址到二进制串
    ip_list=ipaddress.split(".")
    ipstring=[bin(int(i))[2:].zfill(8) for i in ip_list]
    return "".join(ipstring)

if __name__ == '__main__':

    config=configparser.ConfigParser()
    config.read("./config.ini")

    UDPheader=config.get("udpsegment","headerstring")
    UDPsegment=config.get("udpsegment","segmentstring")

    print(UDPheader)
    print(UDPsegment)

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

    pseudo_ptc="00010001"#udp
    pseudo+=pseudo_ptc

    pseudo_len=bin(int(len(UDPheader+UDPsegment)/2))[2:].zfill(16)
    pseudo+=pseudo_len

    print("--------Pseudo Header---------")
    print("Source IP:",sip,"(",pseudo_sip,")")
    print("Destination IP",dip,"(",pseudo_dip,")")
    print("Reserved:","0","(",pseudo_res,")")
    print("Protocol:","17","(",pseudo_ptc,")")
    print("Total Length:",int(len(UDPheader+UDPsegment)/2),"(",pseudo_len,")")

    #UDP
    #source port
    source_port=int(UDPheader[:4],16)
    des_port=int(UDPheader[4:8],16)
    total_len=int(UDPheader[8:12],16)
    #flags
    print("---------UDP Header--------")
    print("Source Port:",source_port)
    print("Destination Port:",des_port)
    print("Length:",total_len)

    print("---------Checksum--------")
    #checksum to 0
    UDPheader=UDPheader[:12]+"0000"
    check_str=hex(int(hex(int(pseudo,2))[2:]+UDPheader+UDPsegment,16))[2:] #转换为16进制
    if len(check_str)% 4 !=0:
        check_str+="00"

    sum=0
    for i in range(int(len(check_str)/4)):
        sum+=int(check_str[4*i:4*i+4],16)
    while sum>>16:
        high_sum=sum>>16
        sum&=0xffff
        sum+=high_sum

#取反
    sum=65535-sum
    print("checksum: ",hex(sum))



