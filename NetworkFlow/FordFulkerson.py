# -*- coding: utf-8 -*-


class FordFulkerson:

    def __init__(self, debug):
        self.debug = debug

    def max_flow(self, graph):
        line = len(graph)
        column = len(graph[0])
        # 退货图
        back_matrix = list()
        for i in range(line):
            back_matrix.append([0] * column)
        # 剩余图
        last_matrix = list()
        for i in range(line):
            last_matrix.append(graph[i].copy())
        # 流量图
        flow_matrix = list()
        for i in range(line):
            flow_matrix.append([0] * column)
        max_flow = 0
        # 循环迭代
        while True:
            # 找到一条s到e的路径
            road = [0]
            min_cap, road = self.find_road(last_matrix, back_matrix, road, 10000)
            # 如果找不到了则退出
            if min_cap == 0:
                break
            # 更新矩阵的值
            max_flow += min_cap
            for i in range(len(road)-1):
                s = road[i]
                e = road[i+1]
                if last_matrix[s][e] > 0:
                    last_matrix[s][e] -= min_cap
                    back_matrix[e][s] += min_cap
                    flow_matrix[s][e] += min_cap
                    continue
                if back_matrix[s][e] > 0:
                    last_matrix[e][s] += min_cap
                    back_matrix[s][e] -= min_cap
                    flow_matrix[e][s] -= min_cap
        if self.debug:
            self.print_flow(flow_matrix)
        return max_flow, flow_matrix

    def find_road(self, last_matrix, back_matrix, road, min_cap):
        column = len(last_matrix[0])
        end_node = column - 1
        node = road[-1]
        if node == end_node:
            return min_cap, road
        for i in range(column):
            if i in road:
                continue
            if last_matrix[node][i] > 0:
                road.append(i)
                min_cap = min([min_cap, last_matrix[node][i]])
                cap, r = self.find_road(last_matrix, back_matrix, road, min_cap)
                if cap > 0:
                    return cap, r
                else:
                    road = road[0: -1]
            if back_matrix[node][i] > 0:
                road.append(i)
                min_cap = min([min_cap, back_matrix[node][i]])
                cap, r = self.find_road(last_matrix, back_matrix, road, min_cap)
                if cap > 0:
                    return cap, r
                else:
                    road = road[0: -1]
        return 0, road

    @staticmethod
    def print_flow(flow_matrix):
        line = len(flow_matrix)
        column = len(flow_matrix[0])
        for i in range(line):
            for j in range(column):
                if flow_matrix[i][j] > 0:
                    print(i, '->', j, flow_matrix[i][j])


def read_file(filename):
    file = open(filename, 'r')
    blocks = str(file.readline())[0: -1].split(' ')
    n = int(blocks[0])
    m = int(blocks[1])
    pairs = []
    for block in file:
        blocks = block[0: -1].split(' ')
        if len(blocks) != 2:
            break
        pair = list()
        pair.append(int(blocks[0]))
        pair.append(int(blocks[1]))
        pairs.append(pair)
    return pairs, n, m


def balance(pairs, n, m, debug=False):
    ff = FordFulkerson(debug)
    for pair in pairs:
        if pair[0] > pair[1]:
            temp = pair[0]
            pair[0] = pair[1]
            pair[1] = temp
    matrix = list()
    for i in range(m+2):
        matrix.append([0] * (m + 2))
    for pair in pairs:
        matrix[0][pair[0]] += 1
        matrix[pair[0]][pair[1]] += 1
    down = int((n + m - 1) / m)
    up = n
    while up > down:
        middle = int((up + down) / 2)
        if debug:
            print('try', middle)
        for i in range(1, m+1):
            matrix[i][m+1] = middle
        max_flow, graph = ff.max_flow(matrix)
        if max_flow < n:
            down = middle + 1
            if debug:
                print(middle, 'cannot satisfy.')
        else:
            up = middle
            if debug:
                print(middle, 'can satisfy.')
        if debug:
            print()
    return up


if __name__ == "__main__":
    pairs, n, m = read_file('data0.txt')
    result = balance(pairs, n, m, debug=True)
    print(result)
