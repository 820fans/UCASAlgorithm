# -*- coding: UTF-8 -*-

import numpy as np


class DualSimplex:
    def run(self, filename):
        # 读取文件内容，文件结构前两行分别为 变量数 和 约束条件个数
        # 接下来是系数矩阵
        # 然后是b数组
        # 然后是约束条件c

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

        x, z = self.DualSimplex(self._A, self._b, self._c)
        self.print_result(x, z)

    @staticmethod
    def print_result(x, z):
        px = ['x[%d] = %f' % (i + 1, x[i]) for i in range(len(x))]
        print(','.join(px))
        print('objective value is : %f' % z)

    def InitializeSimplex(self, A, b):
        """  求取一个初始解  """
        # 添加松弛变量
        slacks = np.eye(self.row)
        A = np.concatenate((A, slacks), axis=1)
        c = np.concatenate((np.zeros(self.var), np.ones(self.row)), axis=0)
        # c [0.  0.  0.  0.  0.  0.  1.  1.  1.]

        b_min, min_pos = (np.min(b), np.argmin(b))  # 得到最小bi

        # 将bi全部转化成正数
        if b_min < 0:
            for i in range(self.row):
                if i != min_pos:
                    A[i] = A[i] - A[min_pos]
                    b[i] = b[i] - b[min_pos]
            A[min_pos] *= -1
            b[min_pos] *= -1

        # 松弛变量全部加入基,初始解为b
        new_B = [i + self.var for i in range(self.row)]

        # 辅助方程的目标函数值
        obj = - np.sum(b)

        c = c - c[new_B].reshape(1, -1).dot(A)
        c = c[0]

        # 入基, 要求ce<0
        e = np.argmin(c)

        while c[e] < 0:
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

            (new_B, A, b, c, obj) = self.PIVOT(new_B, A, b, c, obj, l, e)

            e = np.argmin(c)

        return new_B, A[:, 0:self.var], b

    def DualSimplex(self, A, b, c):

        (B, A, b) = self.InitializeSimplex(A, b)

        # 函数目标值 -cTB-1b
        obj = - np.dot(c[B], b)

        # reshape(1, -1) 让数组c变成一行
        # cT = cT - cTB-1A
        c = c - c[B].reshape(1, -1).dot(A)
        c = c[0]

        # 入基
        e = np.argmin(c)

        # 如果不存在检验数小于0, 则返回
        while c[e] < 0:
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

            e = np.argmin(c)

        x = self._CalculateX(B, A, b, c)
        return x, - obj  # 左上角是负的目标函数

    def _CalculateX(self, B, A, b, c):
        """ 得到完整解 """
        x = np.zeros(self.var, dtype=float)
        x[B] = b
        return x

    # 基变换
    def PIVOT(self, B, A, b, c, z, l, e):
        # l 出基
        # e 入基

        main_elem = A[l][e]
        # scaling the l-th line
        A[l] = A[l] / main_elem
        b[l] = b[l] / main_elem

        # 进行高斯消元
        for i in range(self.row):
            if i != l:
                b[i] = b[i] - A[i][e] * b[l]
                A[i] = A[i] - A[i][e] * A[l]

        # 更新目标值
        z -= b[l] * c[e]
        c -= c[e] * A[l]

        # change the basis
        B[l] = e

        return B, A, b, c, z

if __name__ == "__main__":
    s = DualSimplex()
    s.run('data.txt')