import numpy as np
from scipy.stats import gumbel_r
from scipy import stats
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


def gumbel_r_mom(x):
    """
    Method of moments estimate of the location and scale
    for the Gumbel distribution, based on the *central*
    moments (i.e. the mean and variance).
    """
    _scale = np.sqrt(6) / np.pi * np.std(x)
    _loc = np.mean(x) - np.euler_gamma * _scale
    return _loc, _scale


if __name__ == '__main__':
    X = np.loadtxt('MAR')
    X.sort()
    l, s = gumbel_r_mom(X)
    print(l, s)
    F = gumbel_r.cdf(X, scale=s, loc=l)
    yy = -np.log(-np.log(F))

    #
    npts = 40
    cum_freq, lower_limit, bin_size, ext = stats.cumfreq(X, numbins=npts, defaultreallimits=(0, 144))
    F2 = cum_freq / npts

    fig = plt.figure(figsize=(6, 3.75))
    ax = fig.add_axes([0.11, 0.13, 0.86, 0.82])
    # ax.grid(False, ls='dotted')
    cv = FigureCanvas(fig)
    ax.set_xlabel('Rainfall,X (mm/day)')
    ax.set_ylabel('CumFreq (1)')
    ax.scatter(X, F)
    ax.scatter(np.linspace(1, npts, npts, endpoint=True), F2)
    cv.print_figure('./test.png', dpi=300)
# fig, ax = plt.subplots()
# ax.set_title("PDF from Template")
# ax.hist(X, density=True, bins=100)
# ax.plot(X, p.pdf(X), label='PDF')
# ax.plot(X, p.cdf(X), label='CDF')
# ax.legend()
# plt.show()
