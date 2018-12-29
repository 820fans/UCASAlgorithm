# -*- coding: UTF-8 -*-


class Graph:

    def __init__(self, graph):
        self.graph = graph  # residual graph
        self.row = len(graph)

    '''Returns true if there is a path from source 's' to sink 't' in
    residual graph. Also fills parent[] to store the path '''
    def BFS(self, s, t, parent):

        # Mark all the vertices as not visited
        visited = [False] * self.row

        # Create a queue for BFS
        queue = [s]

        # Mark the source node as visited and enqueue it
        visited[s] = True

        # Standard BFS Loop
        while queue:

            # Dequeue a vertex from queue and print it
            u = queue.pop(0)

            # Get all adjacent vertices of the dequeued vertex u
            # If a adjacent has not been visited, then mark it
            # visited and enqueue it
            for ind, val in enumerate(self.graph[u]):
                if visited[ind] == False and val > 0:
                    queue.append(ind)
                    visited[ind] = True
                    parent[ind] = u

        # If we reached sink in BFS starting from source, then return
        # true, else false
        return True if visited[t] else False

    # Returns tne maximum flow from s to t in the given graph
    def FordFulkerson(self, source, sink):

        # This array is filled by BFS and to store path
        parent = [-1] * (self.row)

        max_flow = 0  # There is no flow initially

        # Augment the flow while there is path from source to sink
        while self.BFS(source, sink, parent):

            # Find minimum residual capacity of the edges along the
            # path filled by BFS. Or we can say find the maximum flow
            # through the path found.
            path_flow = float("Inf")
            s = sink
            while s != source:
                path_flow = min(path_flow, self.graph[parent[s]][s])
                s = parent[s]

            # Add path flow to overall flow
            max_flow += path_flow

            # update residual capacities of the edges and reverse edges
            # along the path
            v = sink
            while v != source:
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = parent[v]

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

        graph = [[0 for x in range(m+2)] for y in range(m+2)]
        for job in jobs:
            graph[0][job[0]] += 1
            graph[job[0]][job[1]] += 1

        return graph

if __name__ == "__main__":
    graph = read_graph("data0.txt")

    g = Graph(graph)
    source = 0
    sink = 3

    print("The maximum possible flow is %d " % g.FordFulkerson(source, sink))