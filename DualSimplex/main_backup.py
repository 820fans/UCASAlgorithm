# -*- coding: UTF-8 -*-

import numpy as np  # python 矩阵操作lib


class Simplex():
    def __init__(self):
        self._A = ""  # 系数矩阵
        self._b = ""  #
        self._c = ''  # 约束
        self._B = ''  # 基变量的下标集合
        self.row = 0  # 约束个数

    def solve(self, filename):
        # 读取文件内容，文件结构前两行分别为 变量数 和 约束条件个数
        # 接下来是系数矩阵
        # 然后是b数组
        # 然后是约束条件c
        # 假设线性规划形式是标准形式（都是等式）

        A = []
        b = []
        c = []
        with open(filename, 'r') as f:
            self.var = int(f.readline())
            self.row = int(f.readline())

            for i in range(self.row):
                x = [int(item) for item in f.readline().strip().split(' ')]
                A.append(x)
            b = [int(item) for item in f.readline().split(' ')]
            c = [int(item) for item in f.readline().split(' ')]

        self._A = np.array(A, dtype=float)
        self._b = np.array(b, dtype=float)
        self._c = np.array(c, dtype=float)
        # self._A = np.array([[3,-1,1,-2,0,0],[2,1,0,1,1,0],[-1,3,0,-3,0,1]],dtype=float)
        # self._b = np.array([-3,4,12],dtype=float)
        # self._c = np.array([-7, 7, -2, -1, -6, 0],dtype=float)
        self._B = list()
        self.var = len(self._c)
        self.row = len(self._b)
        (x, obj) = self.Simplex(self._A, self._b, self._c)
        self.pprint(x, obj, A)

    def pprint(self, x, obj, A):
        px = ['x[%d] = %f' % (i + 1, x[i]) for i in range(len(x))]
        print(','.join(px))
        print('objective value is : %f' % obj)

    # 添加人工变量得到一个初始解
    def InitializeSimplex(self, A, b):

        b_min, min_pos = (np.min(b), np.argmin(b))  # 得到最小bi

        # 将bi全部转化成正数(相当于高斯行变换)
        if b_min < 0:
            for i in range(self.row):
                if i != min_pos:
                    A[i] = A[i] - A[min_pos]
                    b[i] = b[i] - b[min_pos]
            A[min_pos] = A[min_pos] * -1
            b[min_pos] = b[min_pos] * -1

        # 添加松弛变量
        slacks = np.eye(self.row)
        A = np.concatenate((A, slacks), axis=1)
        c = np.concatenate((np.zeros(self.var), np.ones(self.row)),
                           axis=0)
        # A [-7.  7. - 2. - 1. - 6.  0.]
        # c [0.  0.  0.  0.  0.  0.  1.  1.  1.]

        # 松弛变量全部加入基,初始解为b
        new_B = [i + self.var for i in range(self.row)]
        # new_B [6, 7, 8]

        # 辅助方程的目标函数值
        obj = np.sum(b)
        # b [  3.   7.  15.]

        c = c[new_B].reshape(1, -1).dot(A) - c
        c = c[0]
        # c [-8.  7. -3.  4.  1.  1.  0.  0.  0.]
        # entering basis
        e = np.argmax(c)

        while c[e] > 0:
            theta = []
            for i in range(len(b)):
                # b [  3.   7.  15.]
                if A[i][e] > 0:
                    theta.append(b[i] / A[i][e])
                else:
                    theta.append(float("inf"))

            l = np.argmin(np.array(theta))

            if theta[l] == float('inf'):
                print('unbounded')
                return False

            (new_B, A, b, c, obj) = self.PIVOT(new_B, A, b, c, obj, l, e)

            e = np.argmax(c)
        # exit(0)
        # 如果此时人工变量仍在基中，用原变量去替换之
        for mb in new_B:
            if mb >= self.var:
                row = mb - self.var
                i = 0
                while A[row][i] == 0 and i < self.var:
                    i += 1
                (new_B, A, b, c, obj) = self.PIVOT(new_B, A, b, c, obj, new_B.index(mb), i)

        return new_B, A[:, 0:self.var], b

    # 算法入口
    def Simplex(self, A, b, c):
        B = ''
        (B, A, b) = self.InitializeSimplex(A, b)
        # print(B)
        # print(A)
        # print(b)
        # exit(-1)

        # 函数目标值cTB-1b
        obj = np.dot(c[B], b)

        # reshape(1, -1) 让数组c变成一行
        c = np.dot(c[B].reshape(1, -1), A) - c
        c = c[0]
        # print(c)

        # entering basis
        e = np.argmax(c)

        # 找到最大的检验数，如果大于0，则目标函数可以优化
        # 如果不存在检验数小于0, 则返回
        while c[e] > 0:
            theta = []
            for i in range(len(b)):
                if A[i][e] > 0:
                    theta.append(b[i] / A[i][e])
                else:
                    theta.append(float("inf"))

            l = np.argmin(np.array(theta))

            if theta[l] == float('inf'):
                print('unbounded')
                return False

            (B, A, b, c, obj) = self.PIVOT(B, A, b, c, obj, l, e)

            print(c)
            print(obj)
            e = np.argmax(c)

        x = self._CalculateX(B, A, b, c)
        return x, obj

    # 得到完整解
    def _CalculateX(self, B, A, b, c):
        x = np.zeros(self.var, dtype=float)
        x[B] = b
        return x

    # 基变换
    def PIVOT(self, B, A, b, c, z, l, e):
        # main element is a_le
        # l represents leaving basis
        # e represents entering basis

        main_elem = A[l][e]
        # scaling the l-th line
        A[l] = A[l] / main_elem
        b[l] = b[l] / main_elem

        # change e-th column to unit array
        for i in range(self.row):
            if i != l:
                b[i] -= A[i][e] * b[l]
                A[i] -= A[i][e] * A[l]

        # update objective value
        z -= b[l] * c[e]

        c = c - c[e] * A[l]

        # change the basis
        B[l] = e

        return B, A, b, c, z


s = Simplex()
s.solve('data.txt')
