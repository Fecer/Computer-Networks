import numpy as np

class Frame:
    def __init__(self, seq,data=[]):
        self.data = data      # 数据包
        self.seq = seq      # 序列号
        self.frame = []     # 要发送的帧

    def genData(self):
        self.data = list(np.random.randint(0, 2, 8))

    def getFrame(self):
        return self.frame

    def buildMainPart(self):
        self.frame = self.data.copy()
        self.frame.insert(0, self.seq)

    def addHeadTail(self):
        self.frame = [0, 1, 1, 1, 1, 1, 1, 0] + self.frame + [0, 1, 1, 1, 1, 1, 1, 0]

    # 生成CRC校验码 拼接成完整帧
    def generateCRC(self):
        info = self.frame        # 待校验信息
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

        print("------Frame_{}------".format(self.seq))
        print('{:10}\t{}'.format('CRC Generate：', remainder))
        print('{:10}\t{}'.format('帧数据：', output))
        print("-------------------")
        self.frame = output

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

        strlist = [str(x) for x in remainder]
        data = ''.join(strlist)
        if data == '0000000000000000':
            return True
        else:
            return False


    def zerocheck(self):
        strlist=[str(x) for x in self.frame]
        maxfive = 0
        index = 0
        while True:
            if strlist[index] == '1':
                maxfive = maxfive + 1
                if maxfive == 5:
                    strlist.insert(index + 1, '0')
                    index += 1
                    maxfive = 0
            else:
                maxfive = 0
            index += 1
            if index == len(strlist):
                break
        self.frame=[int(x) for x in strlist]
