class Edge(object):
    def __init__(self, u, v, w):
        self.source = u
        self.target = v
        self.capacity = w

    def __repr__(self):
        return "%s->%s:%s" % (self.source, self.target, self.capacity)


class FlowNetwork(object):
    def __init__(self):
        self.adj = {}
        self.flow = {}

    def addVertex(self, vertex):
        self.adj[vertex] = []

    def getEdges(self, v):
        return self.adj[v]

    def editEdge(self, u, v, w=0):
        if u in self.adj.keys():
            for item in self.adj[u]:
                if item.target == v:
                    item.capacity = w

    def addEdge(self, u, v, w=0):
        if u == v:
            raise ValueError("u == v")
        edge = Edge(u, v, w)
        redge = Edge(v, u, 0)
        edge.redge = redge
        redge.redge = edge
        self.adj[u].append(edge)
        self.adj[v].append(redge)
        # Intialize all flows to zero
        self.flow[edge] = 0
        self.flow[redge] = 0

    def FindPath(self, source, target, path):
        if source == target:
            return path
        for edge in self.GetEdges(source):
            residual = edge.capacity - self.flow[edge]
            if residual > 0 and not (edge, residual) in path:
                result = self.FindPath(edge.target, target, path + [(edge, residual)])
                if result is not None:
                    return result

    def MaxFlow(self, source, target):
        path = self.FindPath(source, target, [])
        print('path after enter MaxFlow: %s' % path)
        for key in self.flow:
            print('%s:%s' % (key, self.flow[key]))
        print('-' * 20)
        while path is not None:
            flow = min(res for edge, res in path)
            for edge, res in path:
                self.flow[edge] += flow
                self.flow[edge.redge] -= flow
            for key in self.flow:
                print('%s:%s' % (key, self.flow[key]))
            path = self.FindPath(source, target, [])
            print('path inside of while loop: %s' % path)
        for key in self.flow:
            print('%s:%s' % (key, self.flow[key]))
        return sum(self.flow[edge] for edge in self.GetEdges(source))

    def readBuildGraph(self, filename):
        with open(filename) as f:
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
                self.addVertex(str(pc1))
                self.addVertex(str(pc2))

            # 获取到了所有jobs
            # 添加源点s 终点t
            self.addVertex('s')
            self.addVertex('t')
            for job in jobs:
                self.addEdge('s', str(job[0]), 1)
                self.addEdge(str(job[1]), 't', 0)

            self.editEdge('37', 't', 3)

            print(self.adj)


if __name__ == "__main__":
    g = FlowNetwork()
    g.readBuildGraph("data0.txt")
    exit(0)
    print(g.MaxFlow('s', 't'))
