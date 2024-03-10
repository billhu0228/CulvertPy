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
    return prob


if __name__ == '__main__':
    data = np.loadtxt('../data/Rainfall.txt')
    data.sort()
    F = observation_prob(data)
    F2 = observation_prob(data, a=0)
    ys = -np.log(-np.log(F))
    ys2 = -np.log(-np.log(F2))

    slop, inter, r_val, p_val, std_err = st.linregress(data, ys)
    slop2, inter2, r_val2, p_val2, std_err2 = st.linregress(data, ys2)
    l, s = gumbel_r.fit(data)

    # ==========================================
    fig = plt.figure(figsize=(6, 3.75))
    ax = fig.add_axes((0.10, 0.14, 0.87, 0.82))
    ax.grid(True, ls='dotted')
    cv = FigureCanvas(fig)
    ax.set_xlabel('Observation Value')
    ax.set_ylabel('-ln(-ln(P)')
    ax.scatter(data, ys, color='C1', s=8, label="a=auto")
    ax.scatter(data, ys2, color='C2', s=8, label="a=0")
    xtest = np.array([30, 150])
    ytest = xtest * slop + inter
    ytest2 = xtest * slop2 + inter2
    ax.plot(xtest, ytest, '--', color='C1', label="y=%.4fx%.4f" % (slop, inter))
    ax.plot(xtest, ytest2, '--', color='C2', label="y=%.4fx%.4f" % (slop2, inter2))
    ax.legend(ncol=1)
    cv.print_figure('./ProbPaper.png', dpi=300)
