import copy

import numpy as np
import scipy.stats as st
from scipy.optimize import minimize

from bib.GumbelFitPlot import observation_prob
import matplotlib.pyplot as plt
import pylab
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

# -------------------------------------------------------------------------------
# 绘图参数设置
# -------------------------------------------------------------------------------
pylab.mpl.rcParams['font.sans-serif'] = ['SimHei']
pylab.mpl.rcParams['axes.unicode_minus'] = False
pylab.mpl.rcParams['font.size'] = 10
pylab.mpl.rcParams['legend.fontsize'] = u'small'
pylab.mpl.rcParams['xtick.labelsize'] = u'small'
pylab.mpl.rcParams['ytick.labelsize'] = u'small'


def idf_a(return_period, location, scale):
    """
    IDF 曲线的a参数 IDF=a(T)/b(d)
    :param return_period:
    :param location: 位置参数
    :param scale: 尺度参数
    :return:
    """
    return location - scale * np.log(-np.log(1 - 1 / return_period))


def rain_intensity(d, a, theta, eta):
    """
    降雨烈度
    :param d: 持续时间,hr
    :param a:
    :param theta:
    :param eta:
    :return: 将于强度, mm/hr
    """
    return a / (d + theta) ** eta


def error(X, obv, cal_a):
    b24 = (24 + X[0]) ** X[1]
    i_obv = np.array([o / 24 for o in obv])
    i_pred = np.array([a / b24 for a in cal_a])
    ei = 1 - i_pred / i_obv
    return sum(ei ** 2)


def gringorten(data):
    ordered_obs = copy.deepcopy(data)
    ordered_obs.sort()
    npts = len(ordered_obs)
    idx = np.linspace(1, npts, npts)
    prob = (idx + 0.12) / (npts - 0.44)
    return ordered_obs, prob


def err2(X, obv):
    F, _ = observation_prob(obv)
    F = np.array(F)
    part1 = X[0] - X[1] * np.log(-np.log(F))
    part2 = (24 + X[2]) ** X[3]
    pred = part1 / part2
    e = np.log(pred / obv)
    return sum(e ** 2) / len(obv)


if __name__ == '__main__':
    data = np.loadtxt('../data/Rainfall.txt')
    data.sort()
    e = err2([60, 30, 0.3, 0.9], data)

    bnds = ((30, 80), (10, 60), (0, 1), (0, 1))
    res = minimize(err2, x0=[60, 30, 0.3, 0.9], args=(data,), method='SLSQP', bounds=bnds)

    print(res)
#     T = gringorten(data)
#     fig = plt.figure(figsize=(6, 3.75))
#     ax = fig.add_axes((0.10, 0.14, 0.87, 0.82))
#     ax.grid(True, ls='dotted')
#     cv = FigureCanvas(fig)
#     ax.scatter(T[0], T[1])
#     cv.print_figure('./Test.png', dpi=300)
#
#     print(T)
#
#     F, aa = observation_prob(data)
#
#     ys = -np.log(-np.log(F))
#     slop, inter, r_val, p_val, std_err = st.linregress(data, ys)
#     s = 1 / slop
#     l = (np.euler_gamma - inter) * s
#     print(s, l)
#     return_p = [1 / (1 - p) for p in F]
#     a_cal = [idf_a(t, l, s) for t in return_p]
#     # r = error([0.2, 0.95], data, a_cal)
#     bnds = ((0, 10), (0, 1))
#     res = minimize(error, x0=[0.2, 0.9], args=(data, a_cal), method='SLSQP', bounds=bnds)
#     print(res)
#     print(return_p)
#
