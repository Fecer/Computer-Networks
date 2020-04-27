# 生成CRC校验码 拼接成完整帧
def generateCRC(data):
    info = data.copy()      # 待校验信息
    poly = [1, 0, 0, 0,
            1, 0, 0, 0,
            0, 0, 0, 1,
            0, 0, 0, 0, 1]  # CRC-CCITT
    crcSize = 16            # CRC长度

    init = info.copy()
    t = len(info)
    # 补0
    for i in range(crcSize):
        info.append(0)

    # 模除法
    quotient = []
    cnt = crcSize + 1

    for i in range(t):
        if info[i] == 1:
            quotient.append(1)
            for j in range(cnt):
                info[j + i] = info[j + i] ^ poly[j]
        else:
            quotient.append(0)

    remainder = info[-crcSize::]  # 余数
    output = init
    for i in remainder:
        output.append(i)

    # print("Sequence{}:".format(self.seq))
    print('{:10}\t{}'.format('CRC Generate：', remainder))
    print('{:10}\t{}'.format('帧数据：', output))

    return output

def verifyCRC(data):
    info = data  # 待校验信息
    poly = [1, 0, 0, 0,
            1, 0, 0, 0,
            0, 0, 0, 1,
            0, 0, 0, 0, 1]  # CRC-CCITT
    crcSize = 16  # CRC长度

    t = len(info) - crcSize
    quotient = []
    cnt = crcSize + 1

    for i in range(t):
        if info[i] == 1:
            quotient.append(1)
            for j in range(cnt):
                info[j + i] = info[j + i] ^ poly[j]
        else:
            quotient.append(0)

    remainder = info[-crcSize::]  # 余数
    print('{:10}\t{}'.format('CRC Verify：', remainder))

    strlist = [str(x) for x in remainder]
    data = ''.join(strlist)
    if data == '0000000000000000':
        return True
    else:
        return False
