from xml.dom.minidom import parse

# def bellmanFord(graph, start):
#     dist = {}
#     last = {}
#     inf = 16
#     for vertex in graph:
#         dist[vertex] = inf
#         last[vertex] = start
#     dist[start] = 0
#
#     for i in range(len(graph) - 1):
#         for node in graph:
#             for vertex in graph[node]:
#                 if dist[vertex] > graph[node][vertex] + dist[node]:
#                     dist[vertex] = graph[node][vertex] + dist[node]
#                     last[vertex] = node
#
#     # 检查收敛性
#     for node in graph:
#         for vertex in graph[node]:
#             if dist[vertex] > dist[node] + graph[node][vertex]:
#                 return None, None   # 存在环路
#
#     return dist, last   # 到各点的最短距离，目的地的上一个节点
#

def output(routingTable):
    for i in range (len(routingTable)):
        print('路由器' + chr(ord('A') + i) + ':')
        for label in routingTable[i]:
            if label[1] != 99:
                dest = chr(ord('A') + int(label[0]))
                nxtHp = chr(ord('A') + int(label[2]))
                print('Destination:' + dest + '  Cost:' + str(label[1]) + '  NextHop:' + nxtHp)



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

    routingTable = [[],[],[],[],[]]     # 路由表
    cnt = 1
    breakFlag = 1
    source = -1
    dest = -1
    exitFlag = 0

    # 初始化全部路由表
    for i in range(len(graph)):
        for j in range(len(graph)):
            if i != j:
                routingTable[i].append([j, graph[i][j], j])
    print('初始路由表：')
    output(routingTable)
    print()

    curTable = [[], [], [], [], []]
    while True:
        print('--------------', cnt, '--------------')
        breakFlag = 1

        if source != -1 and exitFlag == 1:                          # 按照输入修改拓扑图
            for label in routingTable[source]:
                if label[0] == dest:
                    label[1] = 99
            for label in routingTable[dest]:
                if label[0] == source:
                    label[1] = 99
            graph[source][dest] = 99
            graph[dest][source] = 99
            source = -1

        curTable = [[], [], [], [], []]
        for i in range (len(graph)):
            for label in routingTable[i]:                           # 将每一条原始路由加入新表中
                curTable[i].append([label[0], label[1], label[2]])  # 加入原本的路由表项
            for j in range (len(graph)):
                if graph[i][j] > 0 :                                # 两个路由器间存在路线
                    nbTable = []
                    for label in routingTable[j]:                   # 给j的路由表加上i到j到距离 存放到nbTable中
                        curCost = label[1] + graph[i][j]
                        if curCost > 99:                            # 超距离的不额外计算
                            curCost = 99
                        nbTable.append([label[0], curCost, j])
                    for label in nbTable:
                        tempDest = label[0]
                        find = -1
                        for label2 in curTable[i]:                  #  在新路由表中查找同目的地信息
                            if label2[0] == tempDest:
                                find = curTable[i].index(label2)    # 相同的坐标
                                break
                        if find == -1:                              # 没找到
                            if label[0] != i:                       # dest不是出发点，可以更新
                                curTable[i].append([label[0], label[1], label[2]])
                                breakFlag = 0
                        else:                                       # 找到了
                            if label2[2] != j:                      # 下一跳不是目的地
                                if label[1] < label2[1]:            # 选取更小的路径
                                    label2[1] = label[1]
                                    label2[2] = label[2]
                                    breakFlag = 0
                            else:                                   # 下一跳不是目的地
                                if label2[1] != label[1]:           # 更新距离
                                    label2[1] = label[1]
                                    breakFlag = 0

        output(curTable)
        print()
        routingTable = [[],[],[],[],[]]                             # 刷新并保存路由表
        for i in range (len(graph)):
            for label in curTable[i]:
                routingTable[i].append([label[0], label[1], label[2]])

        if breakFlag == 1:                                          # 路由稳定后
            if exitFlag == 0:                                       # 更改拓扑结构
                # Input：3,4
                print('输入需要断开的链接两端名称：')
                source, dest = map(int, input().split(','))
                exitFlag = 1
                if source >= len(graph) or dest >= len(graph):      # 非法输入越界
                    exit(1)
            else:
                break

        cnt += 1                                                    # 下一个更新间隔



