from xml.dom.minidom import parse
import copy

def output(routingTable, nextHop):
    for i in range (5):
        print('路由器' + chr(ord('A') + i) + ':')
        for j in range(5):
            if(routingTable[i][j] != 0 and routingTable[i][j] < 99):
                dest = chr(ord('A') + j)
                cost = routingTable[i][j]
                nxtHp = chr(nextHop[i][j] + ord('A'))
                print('Destination:' + dest + ' Cost:', cost ,' Nexthop:' + nxtHp)
    print('-------------------------------')
    print()


if __name__ == "__main__":
    # 获取参数
    DOMTree = parse("config.xml")
    collection = DOMTree.documentElement
    a = [int(x) for x in str(collection.getElementsByTagName('line1')[0].childNodes[0].data).split(" ")]
    b = [int(x) for x in str(collection.getElementsByTagName('line2')[0].childNodes[0].data).split(" ")]
    c = [int(x) for x in str(collection.getElementsByTagName('line3')[0].childNodes[0].data).split(" ")]
    d = [int(x) for x in str(collection.getElementsByTagName('line4')[0].childNodes[0].data).split(" ")]
    e = [int(x) for x in str(collection.getElementsByTagName('line5')[0].childNodes[0].data).split(" ")]
    graph = [a, b, c, d, e]
    path = [['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','','']]
    nxtHp = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
    routingTable = copy.deepcopy(graph)

    for i in range(5):
        for j in range(5):
            nxtHp[i][j] = j
            path[i][j] += (str(i))
            path[i][j] += (str(j))
    print('-----------初始路由表-----------')
    output(routingTable, nxtHp)

    curRoutingTable = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
    initRoutingTable = copy.deepcopy(routingTable)
    cnt = 0

    while True:
        cnt += 1
        breakFlag = 1
        curRoutingTable = copy.deepcopy(routingTable)
        for i in range (5):
            for j in range (5):
                for k in range (5):
                    if curRoutingTable[i][j] > curRoutingTable[i][k] + curRoutingTable[k][j]:
                        if(routingTable[i][j] > routingTable[i][k] + routingTable[k][j]):
                            routingTable[i][j] = routingTable[i][k] + routingTable[k][j]
                            path[i][j] = ''
                            path[i][j] += (path[i][k])
                            path[i][j] += (path[k][j])
                            nxtHp[i][j] = ord(path[i][j][1]) - ord('0')
                            breakFlag = 0

        if breakFlag == 1:
            print('-------------', cnt,'-------------')
            output(routingTable, nxtHp)
            break
        print('-------------', cnt, '-------------')
        output(routingTable, nxtHp)

    print('输入要断开的链接两端名称:')
    dcX, dcY = map(int, input().split(','))
    disconnectX, disconnectY = '', ''
    disconnectX+=(str(dcX))
    disconnectX+=(str(dcY))
    disconnectY+=(str(dcY))
    disconnectY+=(str(dcX))
    routingTable[dcX][dcY] = 99
    routingTable[dcY][dcX] = 99
    initRoutingTable[dcX][dcY] = 99
    initRoutingTable[dcY][dcX] = 99

    for i in range (5):
        for j in range (5):
            breakFlag = 1
            indexX = path[i][j].find(disconnectX)
            indexY = path[i][j].find(disconnectY)
            if indexX != -1:
                routingTable[i][j] = 99
            if indexY != -1:
                routingTable[i][j] = 99

    exitFlag = 1
    while True:
        exitFlag = 1
        for i in range (5):
            for j in range (5):
                breakFlag = 1
                if routingTable[i][j] > initRoutingTable[i][j]:
                    exitFlag = 0
                    breakFlag = 0
                    routingTable[i][j] = initRoutingTable[i][j]
                    path[i][j] = ''
                    path[i][j]+=(str(i))
                    path[i][j]+=(str(j))
                    nxtHp[i][j] = ord(path[i][j][1]) - ord('0')
                for k in range (5):
                    if routingTable[i][j] > routingTable[i][k] + routingTable[k][j]:
                        exitFlag = 0
                        breakFlag = 0
                        routingTable[i][j] = routingTable[i][k] + routingTable[k][j]
                        path[i][j] = ''
                        path[i][j]+=(path[i][k])
                        path[i][j]+=(path[k][j])
                        nxtHp[i][j] = ord(path[i][j][1]) - ord('0')
                if breakFlag == 0:
                    cnt += 1
                    print('-------------', cnt, '-------------')
                    output(routingTable, nxtHp)
        if exitFlag == 1:
            break
