from xml.dom.minidom import parse

def output(routingTable):
    for i in range (len(routingTable)):
        print('路由器' + chr(ord('A') + i) + ':')
        for label in routingTable[i]:
            if label[1] != 99:
                dest = chr(ord('A') + int(label[0]))
                nxtHp = chr(ord('A') + int(label[2]))
                if label[0] != i:
                    print('Destination:' + dest + '  Cost:' + str(label[1]) + '  NextHop:' + nxtHp)


def dijkstra(graph, src):
    unvisited = [i for i in range(len(graph))]
    visited = []
    dist = {src:0}
    if src in unvisited:
        visited.append(src)
        unvisited.remove(src)

    for i in unvisited:
        dist[i] = graph[src][i]

    path = {src: { src:[] } }
    tmp = src
    last = src
    while unvisited.__len__() != 0:
        mDist = float('inf')
        for i in visited:
            for j in unvisited:
                newDist = graph[src][i] + graph[i][j]
                if mDist >= newDist:
                    mDist = newDist
                    graph[src][j] = newDist
                    tmp = j
                    last = i
        dist[tmp] = mDist
        path[src][tmp] = [k for k in path[src][last]]
        path[src][tmp].append(tmp)

        unvisited.remove(tmp)
        visited.append(tmp)

    return dist, path

def printGraph(graph):
    print('拓扑结构为：')
    for i in range (len(graph)):
        print('Router ' + chr( i + ord('A')) + ':')
        for j in range (len(graph)):
            print(chr(j + ord('A')) + ':' + str(graph[i][j]))

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

    printGraph(graph)
    print()

    routingTable = [[],[],[],[],[]]

    for i in range (len(graph)):
        dist, path = dijkstra(graph, i)
        print('To router ' + chr( i + ord('A')) + ':')
        print(dist)
        print(path)
        for j in range (len(dist)):
            if i != j:
                dest = j
                cost = dist[j]
                nextHop = path[i][j][0]
                routingTable[i].append([dest, cost, nextHop])

    print()
    output(routingTable)
