from enum import Enum

import numpy as np
import pint
from src.culvertpy.functions import *


class EInletType(Enum):
    THINWALL = 1
    MITERED = 2
    SQRTHEAD = 3
    BEVELED = 4

    def ke(self):
        if self is EInletType.SQRTHEAD:
            return 0.5
        elif self is EInletType.THINWALL:
            return 0.5
        elif self is EInletType.MITERED:
            return 0.7
        else:
            return 0.2

    def KsS(self):
        if self is EInletType.MITERED:
            return +0.01
        else:
            return -0.01

    def Y(self):
        if self is EInletType.THINWALL:
            return 0.53
        elif self is EInletType.MITERED:
            return 0.75
        elif self is EInletType.SQRTHEAD:
            return 0.57
        else:
            return 0.74

    def c(self):
        if self is EInletType.THINWALL:
            return 0.0496
        elif self is EInletType.MITERED:
            return 0.0463
        elif self is EInletType.SQRTHEAD:
            return 0.0496
        else:
            return 0.03

    def M(self):
        if self is EInletType.THINWALL:
            return 1.5
        elif self is EInletType.MITERED:
            return 1.0
        elif self is EInletType.SQRTHEAD:
            return 2.0
        else:
            return 2.5

    def K(self):
        if self is EInletType.THINWALL:
            return 0.0340
        elif self is EInletType.MITERED:
            return 0.0300
        elif self is EInletType.SQRTHEAD:
            return 0.0083
        else:
            return 0.0018


class Culvert:
    def __init__(self, e_inlet: EInletType, diameter: float, slope: float, length: float,
                 invert_e: float, manning_n: float
                 ):
        self.inlet_type = e_inlet
        self.diameter = diameter
        self.length = length
        self.slope = slope
        self.e0 = invert_e
        self.e1 = self.e0 + self.length * self.slope
        self.area = np.pi * self.diameter ** 2 * 0.25
        self.n = manning_n
        pass

    def HW_i(self, flow: float):
        """
        入口高度计算
        :param flow:
        :return:
        """
        # _A = self.area
        _D = self.diameter
        _QAD = self.QAD(flow)
        _dc = c_critical_depth(flow, _D)
        _vc = c_critical_velocity(flow, _D)
        _K = self.inlet_type.K()
        _M = self.inlet_type.M()
        _Ku = 1.811308890005546
        _KsS = self.inlet_type.KsS()
        _Hc = _dc + _vc ** 2 / (2 * 9.806)
        _c = self.inlet_type.c()
        _Y = self.inlet_type.Y()
        unsubmerged = _Hc / _D + _K * (_Ku * _QAD) ** _M + _KsS
        submerged = _c * (_Ku * _QAD) ** 2 + _Y + _KsS
        if unsubmerged < 1.0:
            return unsubmerged
        else:
            return submerged

    def QAD(self, flow: float):
        qcfs = flow
        D = self.diameter
        A = self.area
        x = qcfs / (A * D ** 0.5)
        return x

    def mean_velocity(self, flow: float):
        ke = self.inlet_type.ke()

    def direct_step(self, flow: float, y1: float, y2: float):
        # alpha = 1.0
        g = 9.806
        a1 = c_area_by_depth(y1, self.diameter)
        a2 = c_area_by_depth(y2, self.diameter)
        v1 = flow / a1
        v2 = flow / a2
        r1 = a1 / y1
        r2 = a2 / y2
        a = (a1 + a2) / 2
        r = (r1 + r2) / 2
        de = (y1 + v1 ** 2 / (2 * g)) - (y2 + v2 ** 2 / (2 * g))
        s0 = self.slope
        sf = (flow * self.n / (r ** (2 / 3) * a)) ** 2
        return de / (sf + s0)

    def back_search2(self, flow, Ho: float):
        l_test = 0
        y2 = Ho
        while l_test < self.length:
            y1 = y2 - 0.01
            dl = self.direct_step(flow, y1, y2)
            print(y1, y2, dl, l_test)
            l_test += dl
            y2 = y1
        return

    def back_search(self, flow, y2: float):
        test = self.direct_step(flow, y2 - 0.05, y2)
        npts = int(self.length / 1.0)
        dx = self.length / npts
        l_test = 0
        if test > 0:  # 正向回水
            for n in range(npts):
                y1 = self.backwater(flow, y2, dx)
                print(y1, l_test)
                l_test += dx
                if l_test >= self.length:
                    return y1
                y2 = y1
        else:  # 负回水
            raise NotImplementedError

    def backwater_2(self, flow, y2: float):
        test = self.direct_step(flow, y2 - 0.05, y2)
        if test > 0:  # 正向回水
            cal_y = np.linspace(y2, self.diameter, num=int((self.diameter - y2) / 0.05) + 1)
            deltX = []
            for i in range(len(cal_y) - 1):
                deltX.append(self.direct_step(flow, cal_y[i], cal_y[i + 1]))
            return sum(deltX)
        else:  # 负回水
            raise NotImplementedError

    def backwater(self, flow: float, y2: float, step: float):
        def _error(yy1, yy2, qq, stt):
            return self.direct_step(qq, yy1, yy2) - stt

        return bisect(_error, y2 - 0.06, y2, args=(y2, flow, step))


if __name__ == '__main__':
    dd = 1.0  # Q_(42, 'inch').to('m').m
    q = 0.6  # Q_(55, 'foot**3/s').to('m**3/s').m
    c = Culvert(EInletType.SQRTHEAD, dd, -0.02, 10, 1584.734, manning_n=0.012)

    du = c_uniform_depth(q, 1.0)
    dc = c_critical_depth(q, 1.0)
    print(dc)
    for y in np.linspace(0.01, 0.99, 99):
        s = c.direct_step(q, y, y + 0.01)
        print("%.3f\t%.3f" % (y, s))

    # c.back_search2(q, 0.72)
    # print(s)
#
# ya1 = c.backwater_2(q, 0.72)
# print(ya1)

#     qad = []
#     hwi = []
#     for q in np.linspace(0.1, 3, 30):
#         qad.append(c.QAD(q))
#         hwi.append(c.HW_i(q))

#     import matplotlib.pyplot as plt
#     fig = plt.figure()
#     ax = fig.add_subplot(1, 1, 1)
#     ax.plot(qad, hwi, color='tab:blue')
#     plt.show()
#
