import numpy as np


def aa(return_period, mu, sigma):
    return mu - sigma * np.log(-np.log(1 - 1 / return_period))


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


if __name__ == '__main__':
