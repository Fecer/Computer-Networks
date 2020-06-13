from xml.dom.minidom import parse

def outputTable(table):
    for route in table:
        print('Destination: {:>15}'.format(route[0]), ' NextHop: {:>10}'.format(route[1]) )

if __name__ == '__main__':
    # 获取参数
    DOMTree = parse("config.xml")
    collection = DOMTree.documentElement

    line1 = (collection.getElementsByTagName('line1')[0].childNodes[0].data).split()
    line2 = (collection.getElementsByTagName('line2')[0].childNodes[0].data).split()
    line3 = (collection.getElementsByTagName('line3')[0].childNodes[0].data).split()
    line4 = (collection.getElementsByTagName('line4')[0].childNodes[0].data).split()
    table = [line1, line2, line3, line4]

    ipM = ['','','','']     # ip + mask
    for i in range (len(table)):
        ipM[i] = table[i][0].split('/')

    ip = ['','','','']      # ip   ( decimal )
    mask = ['','','','']    # mask ( decimal )
    for i in range (len(ipM)):
        ip[i] = ipM[i][0].split('.')
        mask[i] = ipM[i][1]

    for line in ip:
        for j in range(len(line)):
            if line[j] != '0' or j != 0:
                line[j] = f'{int(line[j]):08b}'     # decimal to 8bits binary

    ipMatch = ['','','','']                         # ip 32bits ( binary )
    for i in range(len(ip)):
        for j in range(len(ip[i])):
            ipMatch[i] += (ip[i][j])

    routingTable = []                               # 匹配用路由表
    for i in range(len(ip)):
        routingTable.append([ipMatch[i], mask[i]])

    # 输出当前路由表
    print('Routing Table:')
    outputTable(table)

    destIP = input('\nPlease input your destination IP:\n')
    destIP = destIP.split('.')

    # 处理输入的IP为32位binary
    binDestIP = ''
    for i in range(4):
        destIP[i] = f'{int(destIP[i]):08b}'
        binDestIP += destIP[i]

    nexthop = 3
    curMask = 0
    print('\nMatching...')
    for i in range(len(routingTable) - 1):
        print('Line', i + 1,':')
        subStr = routingTable[i][0][:int(mask[i])]      # 掩码叠加IP
        success = binDestIP.find(subStr)                # 匹配子串
        if success >= 0:
            print(" Match")
            if int(mask[i]) >= curMask:                 # 匹配最长前缀
                curMask = int(mask[i])
                nexthop = i
        else:
            print(' Not Match')

    print('\nNext Hop:\n', table[nexthop][1])
