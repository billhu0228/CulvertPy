import copy
import matplotlib.pyplot as plt
import numpy as np
import pylab
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import scipy.stats as st
from scipy.stats import gumbel_r

# -------------------------------------------------------------------------------
# 绘图参数设置
# -------------------------------------------------------------------------------
pylab.mpl.rcParams['font.sans-serif'] = ['SimHei']
pylab.mpl.rcParams['axes.unicode_minus'] = False
pylab.mpl.rcParams['font.size'] = 10
pylab.mpl.rcParams['legend.fontsize'] = u'small'
pylab.mpl.rcParams['xtick.labelsize'] = u'small'
pylab.mpl.rcParams['ytick.labelsize'] = u'small'


def get_a(num):
    """
    获取超越概率计算参数a: A Plotting Rule for Extreme Probability Paper
    :param num: 样本数量
    :return:
    """
    yy = np.euler_gamma + np.log(num)
    pn = np.exp(-np.exp(-yy))
    val = (pn - num + num * pn) / (2 * pn - 1)
    return val


def observation_prob(obs, a=None):
    ordered_obs = copy.deepcopy(obs)
    ordered_obs.sort()
    npts = len(ordered_obs)
    if a is None:
        a = get_a(npts)
    idx = np.linspace(1, npts, npts)
    prob = (idx - a) / (npts + 1 - 2 * a)
    return prob, a


def plot_scatter(xx, yy, axis, color, mk_size=8, label=""):
    ax.scatter(xx, yy, color=color, s=mk_size, label=label)


if __name__ == '__main__':
    fig = plt.figure(figsize=(6, 3.75))
    ax = fig.add_axes((0.10, 0.14, 0.87, 0.82))
    ax.grid(True, ls='dotted')
    cv = FigureCanvas(fig)
    ax.set_xlabel('Observation Value')
    ax.set_ylabel('-ln(-ln(P)')

    data = np.loadtxt('../data/Rainfall.txt')
    data.sort()

    xtest = np.array([30, 150])
    for i, a in enumerate([None, 0]):
        F, a = observation_prob(data, a)
        ys = -np.log(-np.log(F))
        slop, inter, r_val, p_val, std_err = st.linregress(data, ys)
        ax.scatter(data, ys, color='C%i' % (i + 1), s=8, label="a=%.3f" % a)
        ytest = xtest * slop + inter
        ax.plot(xtest, ytest, '--', color='C%i' % (i + 1), label="y=%.4fx%.4f" % (slop, inter))

    l, s = gumbel_r.fit(data, method='MLE')
    slop3 = 1 / s
    inter3 = np.euler_gamma - l / s
    ytest3 = xtest * slop3 + inter3
    ax.plot(xtest, ytest3, '--', color='k', label="y=%.4fx%.4f" % (slop3, inter3))
    ax.legend(ncol=1)
    cv.print_figure('./ProbPaper.png', dpi=300)
