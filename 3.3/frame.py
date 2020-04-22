import numpy as np

class Frame:
    def __init__(self, seq, frame):
        self.data = np.random.randint(0, 2, 8)  # 数据包
        self.seq = seq      # 序列号
        self.frame = frame  # 要发送的帧

    # 生成CRC校验码 拼接成完整帧
    def generateCRC(self):
        info = self.data        # 待校验信息
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

        print('{:10}\t{}'.format('CRC Generate：', remainder))
        print('{:10}\t{}'.format('发送帧：', output))
        return output # 返回Data + CheckSum

    def verifyCRC(self):
        info = self.data  # 待校验信息
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
        # TODO：判断是否余数为0，帧发送是否正确


