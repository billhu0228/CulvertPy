import numpy as np
from scipy.optimize import bisect


class TrapezoidalChannel:
    __slots__ = 'width', 'm', 'manning_n', 'slop'

    def __init__(self, b, m, n, s):
        """
        开口等腰梯形边沟，曼宁系数n,侧壁坡比1/m
        :param b:
        :param m: >0.0 当m=0时为矩形边沟
        :param n:
        """
        self.width = b
        self.manning_n = n
        self.m = m
        self.slop = s

    def wet_area(self, y):
        """
        湿面积
        :param y:
        :return:
        """
        return (self.width + y * self.m) * y

    def wet_perimeter(self, y):
        """
        液面高度为y时的湿周长
        :param y:
        :return:
        """
        return self.width + 2 * y / np.cos((np.arctan(self.m)))

    def steady_velocity(self, y):
        r = self.wet_area(y) / self.wet_perimeter(y)
        return (1.0 / self.manning_n) * r ** (2.0 / 3.0) * self.slop ** (1 / 2.0)

    def steady_flow(self, y):
        return self.steady_velocity(y) * self.wet_area(y)

    def steady_depth(self, Q):
        def _error(y, sumQ):
            return self.steady_flow(y) - sumQ

        return bisect(_error, 0, 50, args=(Q,))


if __name__ == '__main__':
    c = TrapezoidalChannel(3.336, 0.125, 0.03, 0.03)
    for q in [0.50, 0.69, 0.88, 1.07, 1.20, 1.45, 1.64, 1.83, 2.02, 2.21, 2.40, ]:
        d = c.steady_depth(q)
        print("%.3f,%.3f" % (q, d))
