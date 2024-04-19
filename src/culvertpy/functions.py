import numpy as np
from scipy.optimize import bisect


def c_area_by_theta(diameter, theta):
    """
    圆截面流体面积
    :param diameter:
    :param theta:
    :return:
    """
    return (theta - np.sin(theta)) / 8 * diameter ** 2


def c_depth_by_theta(diameter, theta):
    """
    圆截面流体深度
    :param diameter:
    :param theta:
    :return:
    """
    return 0.5 * (1 - np.cos(theta / 2)) * diameter


def c_perimeter_by_theta(diameter, theta):
    """
    圆截面流体湿周长
    :param diameter:
    :param theta:
    :return:
    """
    return theta / 2 * diameter


def c_width_by_theta(diameter, theta):
    """
    圆截面流体宽度
    :param diameter:
    :param theta:
    :return:
    """
    return np.sin(theta / 2) * diameter


def _error(th, dia, discharge):
    return discharge ** 2 / 9.806 - (c_area_by_theta(dia, th) ** 3 / c_width_by_theta(dia, th))


def _error2(th, dia, flow, s0, n):
    wp = c_perimeter_by_theta(dia, th)
    area = c_area_by_theta(dia, th)
    rh = area / wp
    v = 1.0 / n * rh ** (2 / 3) * s0 ** (1 / 2)
    return area * v - flow


def c_froude_num(flow, diameter, s0, n):
    """
    稳流的福禄数
    :param flow:
    :param diameter:
    :param s0:
    :param n:
    :return:
    """
    du = c_uniform_depth(flow, diameter, s0, n)
    th = c_theta_by_depth(du, diameter)
    T = c_width_by_theta(diameter, th)
    A = c_area_by_depth(du, diameter)
    wp = c_perimeter_by_theta(diameter, th)
    dm = A / T
    v = flow / A
    return v / np.sqrt(9.806 * dm)


def c_uniform_depth(flow, diameter, s0, n):
    """
    圆截面的平均流深度
    :param flow:
    :param diameter:
    :param s0:
    :param n:
    :return:
    """
    r = bisect(_error2, a=1e-3 * np.pi, b=2 * np.pi, args=(diameter, flow, s0, n))
    if isinstance(r, float):
        return c_depth_by_theta(diameter, r)
    else:
        raise ValueError("Error.")


def c_critical_depth(Q, diameter):
    """
    圆截面的临界深度
    :param Q:
    :param diameter:
    :return:
    """
    r = bisect(_error, a=1e-3 * np.pi, b=2 * np.pi, args=(diameter, Q))
    if isinstance(r, float):
        return c_depth_by_theta(diameter, r)
    else:
        raise ValueError("Error.")


def c_theta_by_depth(depth, diameter):
    """
    圆截面根据深度计算圆心角
    :param depth:
    :param diameter:
    :return:
    """
    rr = diameter * 0.5
    if depth / diameter > 1:
        raise ValueError
    else:
        if depth < rr:
            theta = 2. * np.arccos((rr - depth) / rr)
        else:
            theta = 2 * np.pi - 2.0 * np.arccos((depth - rr) / rr)
        return theta


def c_area_by_depth(depth, diameter):
    _th = c_theta_by_depth(depth, diameter)
    return c_area_by_theta(diameter, _th)


def c_critical_velocity(Q, diameter):
    _dc = c_critical_depth(Q, diameter)
    _a = c_area_by_depth(_dc, diameter)
    _t = c_width_by_theta(diameter, c_theta_by_depth(_dc, diameter))
    return Q / _a


if __name__ == '__main__':
    A = c_critical_velocity(1, 1)
    WP = c_perimeter_by_theta(1, np.pi)
    du = c_uniform_depth(1, 1, 0.01, 0.012)
    dc = c_critical_depth(1, 1)
    fr = c_froude_num(1.0, 1.0, 0.01, 0.012)
    print(du, dc, fr)
