# -*- coding: UTF-8 -*-

__INFO__ = False  # 是否输出信息


def iprint(obj, end='\n'):
    """ 输出信息 """
    if __INFO__:
        print(obj, end=end)


def Graph(C, s, t, mat):
    n = len(C)
    F = [[0] * n for i in range(n)] # 网络流图存在F中,F[i][j]当i>j时候代表反向边

    # u -> v 的剩余图是 is C[u][v] - F[u][v]
    height = [0] * n  # 节点高度
    excess = [0] * n  #
    seen = [0] * n  #
    # node 队列
    nodelist = [i for i in range(n) if i != s and i != t]

    # push 操作
    def push(u, v):
        send = min(excess[u], C[u][v] - F[u][v])
        F[u][v] += send
        F[v][u] -= send
        excess[u] -= send
        excess[v] += send

    # relabel 操作
    def relabel(u):
        # 找到可以push的最小高度
        min_height = float('inf')
        for v in range(n):
            if C[u][v] - F[u][v] > 0:
                min_height = min(min_height, height[v])
                height[u] = min_height + 1

    def discharge(u):
        while excess[u] > 0:
            if seen[u] < n:  # 检查邻居
                v = seen[u]
                if C[u][v] - F[u][v] > 0 and height[u] > height[v]:
                    push(u, v)
                else:
                    seen[u] += 1
            else:  # 所有邻居已经检查
                relabel(u)
                seen[u] = 0

    height[s] = n  # 最高高度n
    excess[s] = float("inf")  # 初始时刻流量最大
    for v in range(n):
        push(s, v)

    p = 0
    while p < len(nodelist):
        u = nodelist[p]
        old_height = height[u]
        discharge(u)
        if height[u] > old_height:
            nodelist.insert(0, nodelist.pop(p))
            p = 0
        else:
            p += 1

        iprint("各节点对应高度", end="")
        iprint(height)

    # 从F中提取出graph
    rmat = len(mat)
    cmat = len(mat[0])
    flow_graph = [[0 for y in range(cmat)] for x in range(rmat)]
    offset = rmat+cmat+1
    osize = (rmat + 1) * (cmat + 1)

    for i in range(1, rmat):
        for j in range(offset, osize):
            if F[i][j] == 1:
                idy = j - offset - (i-1)*cmat
                flow_graph[i-1][idy] = 1

    return sum(F[s]), flow_graph


def read_graph(filename):
    with open(filename) as f:
        nm = f.readline().split(' ')
        m, n = int(nm[0]), int(nm[1])
        rows = [int(cell) for cell in f.readline().split(' ')]
        columns = [int(cell) for cell in f.readline().split(' ')]

        # 生成目标图 大小size = m * n + m + n + 2
        # 0 是源点, size - 1是汇点
        size = (m + 1) * (n + 1) + 1
        s, t = 0, size - 1
        r = [i for i in range(1, m+1)]
        c = [i for i in range(m+1, m+n+1)]
        mat = [[x*n+y + m+n+1 for y in range(n)] for x in range(m)]
        graph = [[0 for x in range(size)] for y in range(size)]

        # 源点发出到rows点, columns点发出到t点
        # 1~m 是rows, m+1~m+n  是columns
        for i in range(len(r)):
            graph[s][r[i]] = rows[i]
            for j in range(n):
                graph[r[i]][mat[i][j]] = 1

        for i in range(len(c)):
            graph[c[i]][t] = columns[i]
            for j in range(m):
                graph[mat[j][i]][c[i]] = 1

        return graph, s, t, mat

if __name__ == "__main__":
    C, s, t, mat = read_graph("data9.txt")

    max_flow, flow_graph = Graph(C, s, t, mat)

    for i in range(len(flow_graph)):
        print(flow_graph[i])