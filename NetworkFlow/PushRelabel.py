# -*- coding: utf-8 -*-

class PushRelabel:

    def __init__(self, debug=False):
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
        # 初始化s节点的边
        for i in range(column):
            flow_matrix[0][i] = last_matrix[0][i]
            last_matrix[0][i] = 0
            back_matrix[i][0] = flow_matrix[0][i]
        height = [0] * line
        height[0] = line
        # 循环迭代
        count = 0
        while True:
            count += 1
            print(count)
            node = self.find_node(flow_matrix)
            if node == -1:
                break
            height_enough = False
            for i in range(column):
                if height[node] <= height[i]:
                    continue
                if last_matrix[node][i] > 0:
                    height_enough = True
                    flow = min([self.bottleneck(flow_matrix, node), last_matrix[node][i]])
                    flow_matrix[node][i] += flow
                    last_matrix[node][i] -= flow
                    back_matrix[i][node] += flow
                    continue
                if back_matrix[node][i] > 0:
                    height_enough = True
                    flow = min([self.bottleneck(flow_matrix, node), back_matrix[node][i]])
                    flow_matrix[i][node] -= flow
                    last_matrix[i][node] += flow
                    back_matrix[node][i] -= flow
            if height_enough is False:
                height[node] += 1
        if self.debug:
            self.print_flow(flow_matrix)
        return self.bottleneck(flow_matrix, column-1), flow_matrix

    def find_node(self, flow_matrix):
        line = len(flow_matrix)
        column = len(flow_matrix[0])
        for i in range(column - 1):
            flow = self.bottleneck(flow_matrix, i)
            if flow > 0:
                return i
        return -1

    def bottleneck(self, flow_matrix, node):
        flow = 0
        for i in range(len(flow_matrix)):
            flow += flow_matrix[i][node]
            flow -= flow_matrix[node][i]
        return flow

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
    blocks = str(file.readline()).strip().split(' ')
    n = int(blocks[0])
    m = int(blocks[1])
    blocks = str(file.readline()).strip().split(' ')
    lines = [int(block) for block in blocks]
    blocks = str(file.readline()).strip().split(' ')
    columns = [int(block) for block in blocks]
    return n, m, lines, columns


def fill(sum_lines, sum_columns, line, column, debug=False):
    matrix = list()
    count_node = line * column + line + column + 2
    for i in range(count_node):
        matrix.append([0] * count_node)
    for i in range(1, line+1):
        matrix[0][line*column+i] = sum_lines[i-1]
    for i in range(1, column+1):
        matrix[line*column+line+i][count_node-1] = sum_columns[i-1]
    for i in range(1, line+1):
        for j in range(1, column+1):
            matrix[line*column+i][(i-1)*column+j] = 1
            matrix[(i-1)*column+j][line*column+line+j] = 1
    pr = PushRelabel(debug=debug)
    max_flow, graph = pr.max_flow(matrix)
    sum_values = sum(sum_lines)
    if max_flow < sum_values:
        return None
    result_matrix = list()
    for i in range(line):
        result_matrix.append([0] * column)
        for j in range(column):
            result_matrix[i][j] = graph[line*column+i+1][i*column+j+1]
    return result_matrix


if __name__ == "__main__":
    n, m, sum_lines, sum_columns = read_file('data1')
    result = fill(sum_lines, sum_columns, n, m, debug=True)
    for line in result:
        print(line)
