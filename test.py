from z3 import *

# 假设 n = 10
n = 10
b = [Bool(f"b{i}") for i in range(n)]
count = Sum([If(bi, 1, 0) for bi in b])

s = Solver()
s.add(count <= 3)  # 比如你要至少3个true
print(s.check())
print(s.model())

x, y = Ints('x y')
s = Solver()
s.add(y != 0, x / y > 3)
print(s.check())
print(s.model())

# --------------------------------------------------
# A fixed host network topology
from z3 import *

from queue_model import *

ctx = Context()
# 定义一个枚举类型 Status，有三个状态 [如果cpu或者iio设备不止一个，也要继续补充这个enumeration]
ReqSource, (cpu, iio) = EnumSort('ReqSource', ['cpu', 'iio'], ctx=ctx)

s = Solver(ctx=ctx)
x, y = Ints('x y', ctx=ctx)
ite1 = If(x>0, y==3, y==-3)
ite2 = If(y>0, x==5, ite1)

# s.assert_and_track(ite1, 'ite1')
s.assert_and_track(ite2, 'ite2')
s.assert_and_track(x == 3, 'x_eq_3')
s.assert_and_track(y == -3, 'y_eq_min3')

print(s.to_smt2())
if s.check() == sat:
    print(s.model())
else:
    print(s.unsat_core())