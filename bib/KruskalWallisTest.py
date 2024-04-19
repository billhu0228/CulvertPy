from random import sample

import numpy as np
from scipy import stats

if __name__ == '__main__':
    data = np.loadtxt('../data/Rainfall.txt')
    x = sample(list(data), 30)
    y = sample(list(data), 30)
    r = stats.kruskal(x, y)
    print(r)
