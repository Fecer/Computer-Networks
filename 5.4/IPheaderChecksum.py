from xml.dom.minidom import parse

def printLine():
    print('------------------------------------------')

if __name__ == '__main__':
    # 获取参数
    DOMTree = parse("config.xml")
    collection = DOMTree.documentElement

    header = collection.getElementsByTagName('header')[0].childNodes[0].data
    printLine()

    print('Header:\n', header)
    printLine()

    version = header[:1]
    print('Version:\n', version)
    printLine()

    headerLen = header[1:2]
    print('Header Length:\n', headerLen)
    printLine()

    service = header[2:4]
    print('Differentiated Services Field:\n', service)
    printLine()

    totalLen = header[4:8]
    totalLen = int(totalLen, 16)
    print('Total Length:\n', totalLen)
    printLine()

    id = header[8:12]
    id = int(id, 16)
    print('Identification:\n', id)
    printLine()

    flags = header[12:16]
    flags = int(flags, 16)
    print('Flags and Offset:\n', flags)
    printLine()

    ttl = header[16:18]
    ttl = int(ttl, 16)
    print('Time to live:\n', ttl)
    printLine()

    protocol = header[18:20]
    protocol = int(protocol, 16)
    print('Protocol:\n', protocol)
    printLine()

    checksum = header[20:24]
    checksum = int(checksum, 16)
    print('Checksum in header:\n', checksum, '(' + header[20:24] + ')')
    printLine()

    source = header[24:32]
    a = str(int(source[0:2], 16))
    b = str(int(source[2:4], 16))
    c = str(int(source[4:6], 16))
    d = str(int(source[6:8], 16))
    print('Source IP:\n', a+'.'+b+'.'+c+'.'+d)
    printLine()

    dest = header[32:40]
    a = str(int(dest[0:2], 16))
    b = str(int(dest[2:4], 16))
    c = str(int(dest[4:6], 16))
    d = str(int(dest[6:8], 16))
    print('Destination IP:\n', a + '.' + b + '.' + c + '.' + d)
    printLine()

    a = int(header[0:4], 16)
    b = int(header[4:8], 16)
    c = int(header[8:12], 16)
    d = int(header[12:16], 16)
    e = int(header[16:20], 16)
    f = int(header[24:28], 16)
    g = int(header[28:32], 16)
    h = int(header[32:36], 16)
    i = int(header[36:40], 16)

    res1 = hex(a + b + c + d + e + f + g + h + i)
    opnd1 = str(res1)[2:3]
    opnd2 = str(res1)[3:7]

    res2 = int(opnd1, 16) + int(opnd2, 16)
    all = int('ffff', 16)
    res2 = all - res2
    checksum2 = res2
    print('Checksum by calculated:')
    print('0x%04x' % checksum2)
