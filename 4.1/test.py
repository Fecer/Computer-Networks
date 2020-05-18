from winpcapy import WinPcapDevices
from winpcapy import WinPcapUtils

import dpkt
import time
import datetime
from dpkt.compat import compat_ord




def mac(eth):
    # 解析mac层
    type=eth.type
    if type==2048:
        type=str(type)+"(IPv4)"

    print('Ethernet Frame: ')
    print("Source Address:", mac_addr(eth.src))
    print("Destination Address:", mac_addr(eth.dst))
    print("Type:" ,eth.type)
    print("----------------------------------------")
    # 显示src地址，dst地址，type为0x0800标识ipv4

    if isinstance(eth.data, dpkt.ip.IP):
        print("IP packet:")# IP数据包
        packet = eth.data
        ip(packet)
    elif isinstance(eth.data.data,dpkt.ip6.IP6):
        print("IPv6 packet:")
        packet =eth.data
        #ip6(packet)
    elif isinstance(eth.data,dpkt.arp.ARP):
        print("ARP packet:")
        packet=eth.data
        arp(packet)

#udp
def udp(packet):
    sport=packet.sport
    dport=packet.dport
    checksum=packet.sum
    len = packet.ulen

    context={"Source Port":sport,"Destination Port":dport,"Checksum":checksum,"Length:":len}
    print(context)
    print("--------------------------------")
    print()

def arp(packet):
    print()
    hardwaretype=packet.hrd
    if hardwaretype==1:
        hardwaretype=str(hardwaretype)+"(Ethernet)"

    protocol=packet.pro
    if protocol==2048:
        protocol=str(protocol)+"(IPv4)"

    hardwareSize=packet.hln
    protocolSize=packet.pln
    op=packet.op

    sMacAdd=packet.sha
    sIPAdd=packet.spa

    TMacAdd=packet.tha
    TIPAdd=packet.tpa

    print("ARP Frame: ")
    print("Hardware Type: ",hardwaretype)
    print("Protocol: ",protocol)
    print("Hardware Size: ",hardwareSize)
    print("Opcode: ",op)
    print("Sender Mac Address: ",mac_addr(sMacAdd))
    print("Sender IP Address: ",ip_addr(sIPAdd))
    print("Target Mac Address: ",mac_addr(TMacAdd))
    print("Target Mac Address: ",ip_addr(TIPAdd))

def ip(packet):

    # 取出分片信息
    version = packet.v  # ip version
    headlen = packet.hl  # 首部长度    serve=packet.df #service field
    id = packet.id  # identification
    totallen = packet.len  # total length

    df = bool(packet.off & dpkt.ip.IP_DF)
    mf = bool(packet.off & dpkt.ip.IP_MF)
    offset = packet.off & dpkt.ip.IP_OFFMASK

    ttl = packet.ttl
    proto = packet.p  # protocol
    if(int(proto)==1):
        print()
    checksum = packet.sum

    src = packet.src
    dst = packet.dst

    output1={'version': version,'headlen':headlen,'id':id,'totallen':totallen}
    output2 = {'df': df, 'mf': mf, 'offset': offset}
    output3 = {'ttl': ttl, 'protocol': proto, 'checksum': checksum}
    output4 = {'src': ip_addr(src), 'dst': ip_addr(dst)}
    print(output1)
    print(output2)
    print(output3)
    print(output4)
    print("----------------------------------------")

    if isinstance(packet.data,dpkt.udp.UDP):
        print("UDP Packet:")
        packet=packet.data
        udp(packet)
    elif isinstance(packet.data,dpkt.tcp.TCP):
        print("TCP Packet:")
        packet=packet.data
        tcp(packet)
    elif isinstance(packet.data, dpkt.icmp.ICMP):
        print("ICMP Packet")
        packet=packet.data
        icmp(packet)
    else:
        print()


def tcp(packet):

    sport=packet.sport
    dport=packet.dport

    seqnum=packet.seq
    acknum=packet.ack

    headlenth=packet.off*4

    #flags
    URG=int((packet.flags&32)/32)
    ACK=int((packet.flags&16)/16)
    PSH=int((packet.flags&8)/8)
    RST=int((packet.flags&4)/4)
    SYN=int((packet.flags&2)/2)
    FIN=int((packet.flags&1))

    windowssize=packet.win
    checksum=packet.sum
    urgentp=packet.urp

    print("Source Port: ",sport)
    print("Destination Port: ",dport)
    print("Sequence nuber: ",seqnum)
    print("Acknoledgment number: ",acknum)
    print("Header Length: ",headlenth,"bytes")
    print("Flags:")
    print("(URG:",URG,"ACK:",ACK,"PSH:",PSH,"RST:",RST,"SYN:",SYN,"FIN:",FIN,")")
    print("Window size value:",windowssize)
    print("Checksum:",checksum)
    print("Urgent Pointer:",urgentp)

    if packet.opts!=b'':
        print(''.join('%02x' %x for x in packet.opts))

    if packet.data!=b'':
        print()

    try:
        request = dpkt.http.Request(packet.data)
    except (dpkt.dpkt.NeedData, dpkt.dpkt.UnpackError):
            return
    print('HTTP request:',repr(request))



def icmp(packet):
    print()
    type=packet.type;
    code=packet.code;
    checksum=packet.sum;
    #id=packet.data.id;
    #seq=packet.data.seq;
    context={"type":type,"code":code,"checksum":checksum};
    print("ICMP:",context)




def mac_addr(address):
    """Convert a MAC address to a readable/printable string

       Args:
           address (str): a MAC address in hex form (e.g. '\x01\x02\x03\x04\x05\x06')
       Returns:
           str: Printable/readable MAC address
    """
    return ':'.join('%02x' % compat_ord(b) for b in address)

def ip_addr(address):
    return ".".join('%d' %x for x in tuple(address))

def packet_callback(win_pcap, param, header, pkt_data):
    print("Frame income......")
    eth = dpkt.ethernet.Ethernet(pkt_data)
    mac(eth)
    # # 判断是否为IP数据报


if __name__ == '__main__':
    list_device = WinPcapDevices.list_devices()
    print(list_device)
    WinPcapUtils.capture_on_device_name(device_name="\\Device\\NPF_{37D76121-6ADD-4C56-BF7B-25CAA90B2BB7}", callback=packet_callback)
