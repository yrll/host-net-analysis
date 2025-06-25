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

import sys
print(sys.version)
name = f"test_{1}"
print(name)

from queue_model import *

ctx = Context()
# 定义一个枚举类型 Status，有三个状态 [如果cpu或者iio设备不止一个，也要继续补充这个enumeration]
ReqSource, (cpu, iio) = EnumSort('ReqSource', ['cpu', 'iio'], ctx=ctx)

# 示例：嵌套 Sum 和 If
queues = ['cha_raw', 'mc']
time_steps = 2
solver = Solver()

# 创建 Z3 变量
credits = [[Int(f"credit_{q}_at_time_{t}") for q in queues] for t in range(time_steps)]
active = [[Int(f"active_{q}_at_time_{t}") > 0 for q in queues] for t in range(time_steps)]

# 嵌套 Sum(If(...))
total_credit = Sum(*[Sum(*[If(active[t][i], credits[t][i], 0) for i in range(len(queues))]) for t in range(time_steps)])

# 添加约束
solver.add(total_credit >= 0)
print(solver.check())  # sat
print(solver.model())  # 示例模型