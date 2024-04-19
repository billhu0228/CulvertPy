import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pylab
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.pyplot import MultipleLocator
from matplotlib import ticker

from src.culvertpy.culvert import Culvert, EInletType

# -------------------------------------------------------------------------------
# 绘图参数设置
# -------------------------------------------------------------------------------
pylab.mpl.rcParams['font.sans-serif'] = ['SimHei']
pylab.mpl.rcParams['axes.unicode_minus'] = False
pylab.mpl.rcParams['font.size'] = 10
pylab.mpl.rcParams['legend.fontsize'] = u'small'
pylab.mpl.rcParams['xtick.labelsize'] = u'small'
pylab.mpl.rcParams['ytick.labelsize'] = u'small'

if __name__ == "__main__":
    dd = 1.0  # Q_(42, 'inch').to('m').m
    q = 0.55  # Q_(55, 'foot**3/s').to('m**3/s').m
    c = Culvert(EInletType.SQRTHEAD, dd, -0.01, 10, 1584.734)
    qad = []
    hwi = []
    for q in np.linspace(0.1, 3, 30):
        qad.append(c.QAD(q))
        hwi.append(c.HW_i(q))
    fig = plt.figure(figsize=(6, 3.75))
    ax = fig.add_axes((0.10, 0.14, 0.87, 0.82))
    ax.grid(True, ls='dotted')
    cv = FigureCanvas(fig)
    ax.set_xlabel('Q/(AD$^{0.5}$)')
    ax.set_ylabel('HWi/D')
    ax.plot(qad, hwi, color='C0', ls='solid', linewidth=1.2, label="入口控制水位计算")
    ax.legend(ncol=1)
    cv.print_figure('./QAD-HWi.png', dpi=300)
