import json

from z3 import Context, Solver, EnumSort, ExprRef, Bool, sat, ModelRef

from util import make_counter

# 以下是合法的source起点
CPU = 'cpu'
IIO = 'iio'


"""
注意事项：
1. 变量和约束的命名不能相同，否则会unsat（可能是因为覆盖？或者是什么dependency）
2. 多个条件语句的嵌套（如IF）时，只添加最外层的语句进入solver
"""

class MySolver:
    def __init__(self):
        self.ctx = Context()
        self.solver = Solver(ctx=self.ctx)
        # 定义一个枚举类型 Status，有三个状态 [如果cpu或者iio设备不止一个，也要继续补充这个enumeration]
        self.ReqSource, src_list = EnumSort('ReqSource', [CPU, IIO], ctx=self.ctx)
        self._src_sort_map = {
            str(src): src for src in src_list
        }
        self.constraint_map = {}
        self.model_map = {}

        self.model: ModelRef = None

    def get_source_const(self, src_str):
        return self._src_sort_map[src_str] if src_str in self._src_sort_map.keys() else None

    def add_expr(self, name: str, cons: ExprRef):
        if name in self.constraint_map.keys():
            name = name + f'_*{make_counter()}'
        self.constraint_map[name] = cons
        self.solver.assert_and_track(cons, name)

    def add_bool(self, name: str):
        return Bool(name=name, ctx=self.ctx)

    def verify(self, ifsave=True, print_cons:bool = True):
        if self.solver.check() == sat:
            self.model = self.solver.model()
            print('SAT')
            self.save_model('smt_model')
            for decl in self.model.decls():
                var_name = decl.name()  # 获取变量名
                if 'deq_cnt' in str(var_name):  # 检查是否包含特定字符串
                    print(f"{var_name} = {self.model[decl]}")  # 输出变量名和值
        else:
            print('UNSAT')
            self.prinf_unsat_core()

        self.save_smt2('smt.smt2')

    def save_model(self, filename, only_cnt: bool = True):
        model_dict = {}
        for d in self.model.decls():
            var_name = d.name()
            value = self.model[d]
            self.model_map[var_name] = value
            if only_cnt and ('cons' in var_name or 'index' in var_name):
                continue
            model_dict[var_name] = str(value)

        with open(filename, "w") as f:
            json.dump(model_dict, f, indent=2)

    def save_smt2(self, filename):
        with open("smt.smt2", "w") as f:
            f.write(self.solver.to_smt2())

    def prinf_unsat_core(self):
        for name in self.solver.unsat_core():
            cons = self.constraint_map.get(str(name), None)
            if cons is not None:
                # print(f"{name} → {cons}")
                print(f"{name} -> {cons}")
            else:
                print(f"{name} → <no mapping found>")

