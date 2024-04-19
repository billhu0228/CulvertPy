from src.culvertpy.channel import TrapezoidalChannel
from src.culvertpy.culvert import Culvert, EInletType

if __name__ == "__main__":
    # Step-1
    c = TrapezoidalChannel(3.336, 0.125, 0.03, 0.03)
    for q in [0.50, 0.60, 0.88, 1.07, 1.20, 1.45, 1.64, 1.83, 2.02, 2.21, 2.40, ]:
        d = c.steady_depth(q)
        print("%.3f,%.3f" % (q, d))



    dd = 1.0  # Q_(42, 'inch').to('m').m
    c = Culvert(EInletType.SQRTHEAD, dd, -0.01, 10, 1584.734)
    HWi = c.HW_i(0.6) * dd
    print(HWi)
