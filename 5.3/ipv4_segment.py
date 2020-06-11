from xml.dom.minidom import parse


if __name__ == '__main__':
    # 获取参数
    DOMTree = parse("config.xml")
    collection = DOMTree.documentElement

    BigIPTotalLen = int(collection.getElementsByTagName('BigIPTotalLen')[0].childNodes[0].data)
    IDTotal = int(collection.getElementsByTagName('IDTotal')[0].childNodes[0].data)
    MTU = int(collection.getElementsByTagName('MTU')[0].childNodes[0].data)
    FragNum = int(collection.getElementsByTagName('FragNum')[0].childNodes[0].data)
    TotalLen = [int(x) for x in str(collection.getElementsByTagName('TotalLen')[0].childNodes[0].data).split(',')]
    ID = [int(x) for x in str(collection.getElementsByTagName('ID')[0].childNodes[0].data).split(',')]
    FragMF = [int(x) for x in str(collection.getElementsByTagName('FragMF')[0].childNodes[0].data).split(',')]
    FragOffset = [int(x) for x in str(collection.getElementsByTagName('FragOffset')[0].childNodes[0].data).split(',')]

    print('-------开始分片-------')
    print('Big Data Frame:')
    print('TotalLen =',BigIPTotalLen)
    print('ID =', IDTotal)
    print('DF = 0')
    print('MF = 0')
    print('Offset = 0')
    print('MTU =', MTU)
    print()

    print('Total Length / MTU =', BigIPTotalLen / MTU)
    num = int(BigIPTotalLen / MTU) + 1
    print('So we need', num, 'fragments')
    segLen = [1500, 1500, BigIPTotalLen - 1480 * 2 + 20]
    print()

    for i in range (num):
        print('----Fragment', i + 1, '----')
        print('TotalLen =', segLen[i])
        print('ID =', IDTotal)
        print('DF = 0')
        print('MF =', FragMF[i])
        print('Offset =', FragOffset[i])
    print()
    print()

    print('-------开始重装-------')

    BigIPTotalLen = 0
    for i in range (num):
        print('----Fragment', i + 1, '----')
        print('TotalLen =', TotalLen[i])
        BigIPTotalLen += (TotalLen[i] - 20)
        print('ID =', ID[i])
        print('DF = 0')
        print('MF =', FragMF[i])
        print('Offset =', FragOffset[i])
    print()

    print('Big Data Frame:')
    print('TotalLen =', BigIPTotalLen)
    print('ID =', ID[0])
    print('DF = 0')
    print('MF = 0')
    print('Offset = 0')
