# -*- coding: UTF-8 -*-

__INFO__ = False  # 是否输出信息


def iprint(obj):
    """ 输出信息 """
    if __INFO__:
        print(obj)


class Graph:
    def __init__(self, graph):
        self.graph = graph  # residual graph
        self.row = len(graph)

    def BFS(self, s, t, parent):

        visited = [False] * self.row

        queue = [s]
        visited[s] = True

        while queue:
            u = queue.pop(0)

            for ind, val in enumerate(self.graph[u]):
                if not visited[ind] and val > 0:
                    queue.append(ind)
                    visited[ind] = True
                    parent[ind] = u

        return True if visited[t] else False

    def FordFulkerson(self, source, sink):
        parent = [-1] * self.row
        max_flow = 0
        while self.BFS(source, sink, parent):
            # 还能找到路
            path_flow = float("Inf")
            s = sink
            while s != source:
                path_flow = min(path_flow, self.graph[parent[s]][s])
                s = parent[s]

            # Add path flow to max_flow
            max_flow += path_flow

            v = sink
            while v != source:
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = parent[v]

        iprint(self.graph)
        return max_flow


def read_graph(name):
    with open(name) as f:
        # N jobs M computer
        nm = f.readline().split(' ')
        n, m = int(nm[0]), int(nm[1])
        jobs = []
        for i in range(n):
            pcs = f.readline().split(' ')
            pc1, pc2 = int(pcs[0]), int(pcs[1])
            if pc1 > pc2:
                pc1, pc2 = pc2, pc1
            jobs.append([pc1, pc2])

        graph = [[0 for x in range(m + 2)] for y in range(m + 2)]
        for job in jobs:
            graph[0][job[0]] += 1
            graph[job[0]][job[1]] += 1

        return n, m, graph


if __name__ == "__main__":
    n, m, graph = read_graph("data.txt")

    source = 0
    target = m + 1

    left = int((n + m - 1) / m)
    right = n
    while left < right:
        # 深拷贝
        tg = [[0 for x in range(m + 2)] for y in range(m + 2)]
        for i in range(m + 2):
            for j in range(m + 2):
                tg[i][j] = graph[i][j]

        # binary search
        mid = int((left + right)/2)
        for i in range(1, m+1):
            tg[i][m+1] = mid

        g = Graph(tg)

        max_flow = g.FordFulkerson(source, target)
        if max_flow < n:  # 任务不能全部完成
            left = mid + 1
            iprint("Flow %d not enough to finish all jobs !" % mid)
        else:
            right = mid
            iprint("Too many flow %d !" % mid)

    print("Minmax Load is %d." % left)