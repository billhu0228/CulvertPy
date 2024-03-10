import numpy as np
from scipy.stats import gumbel_r

if __name__ == '__main__':
    data = np.loadtxt('../data/Rainfall.txt')
    l, s = gumbel_r.fit(data)
    print(l, s)
