import pint

ureg = pint.UnitRegistry
Q_ = pint.Quantity

# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    q = Q_(1, 'foot**3/s')
    A = Q_(1, 'foot**2')
    D = Q_(1, 'foot')
    f1 = q / (A * D ** 0.5)
    q = Q_(1, 'm**3/s')
    A = Q_(1, 'm**2')
    D = Q_(1, 'm')
    f2 = q / (A * D ** 0.5)
    print(f2.to("foot**0.5/s"))
