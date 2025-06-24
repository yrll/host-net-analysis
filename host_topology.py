# A fixed host network topology
import json

from z3 import *
from z3.z3util import get_vars

from queue_model import *
from queue_scheduling import *
from cache_model import *

ctx
solver
current_cons_name_map = {}


def save_model(model: ModelRef, filename: str):
    model_dict = {}
    for d in model.decls():
        var_name = d.name()
        value = model[d]
        model_dict[var_name] = str(value)

    with open(filename, "w") as f:
        json.dump(model_dict, f, indent=2)


def add_cons_with_no_conflict(cons_dict: dict[str, ExprRef], solver: Solver, printf: bool = False):
    for name, cons in cons_dict.items():
        if name in current_cons_name_map.keys():
            print('CONFLICT NAME: ' + name)
            assert False
        else:
            current_cons_name_map[name] = cons
            solver.assert_and_track(cons, name)
            if printf:
                print(name)
            # print(cons)


# 自定义主机网络拓扑和配置
time_steps = 3
src_inputs = {
    'cpu': SourceInput(src=cpu, ctx=ctx, time_steps=time_steps, credit_based=True, lossless=False),
    'rnic': SourceInput(src=iio, ctx=ctx, time_steps=time_steps, credit_based=True, lossless=False)
}
queues = {
    'lfb_raw': HNQueue(ctx=ctx, queue_name='lfb_raw', time_steps=time_steps, queue_size=3, cached=True),
    'lfb_filtered': HNQueue(ctx=ctx, queue_name='lfb_filtered', time_steps=time_steps, queue_size=3, cached=False),
    'cha_raw': HNQueue(ctx=ctx, queue_name='cha_raw', time_steps=time_steps, queue_size=5, cached=True),
    'cha_filtered': HNQueue(ctx=ctx, queue_name='cha_filtered', time_steps=time_steps, queue_size=5, cached=False),
    'iio': HNQueue(ctx=ctx, queue_name='iio', time_steps=time_steps, queue_size=4, cached=False),
    'mc': HNQueue(ctx=ctx, queue_name='mc', time_steps=time_steps, queue_size=6, cached=False),
}
dsts = {
    'mem': TargetNode(dst='mem', target_queue=queues['mc'])
}
caches = {
    'l1': HNCache(ctx=ctx, cache_name='l1', time_steps=time_steps, cache_size=3),
    'llc': HNCache(ctx=ctx, cache_name='llc', time_steps=time_steps, cache_size=5),
}

# 初始化
for q in queues.values():
    # add_cons_with_no_conflict(q.init_time_zero(), solver)
    add_cons_with_no_conflict(q.add_self_constraints(), solver)
for c in caches.values():
    add_cons_with_no_conflict(c.init_time_zero(), solver)
    add_cons_with_no_conflict(c.add_cache_replace_constraints(queues['mc']), solver)

# 添加建模约束
add_cons_with_no_conflict(
    add_fifo_constraints(queues['mc'], queues['cha_filtered']), solver)
add_cons_with_no_conflict(
    add_round_robin_constraints(queues['cha_raw'], queues['iio'], queues['lfb_filtered']), solver)
add_cons_with_no_conflict(
    caches['l1'].add_cache_filter_constraints(raw_queue=queues['lfb_raw'], filtered_queue=queues['lfb_filtered']),
    solver)
add_cons_with_no_conflict(
    caches['llc'].add_cache_filter_constraints(raw_queue=queues['cha_raw'], filtered_queue=queues['cha_filtered']),
    solver)
add_cons_with_no_conflict(
    src_inputs['cpu'].add_credit_flow_control_constraints(queues['lfb_raw'], queues['mc'], queues['lfb_raw'],
                                                          queues['cha_raw']), solver)
add_cons_with_no_conflict(
    src_inputs['rnic'].add_credit_flow_control_constraints(queues['iio'], queues['mc'], queues['cha_raw']), solver)
add_cons_with_no_conflict(
    dsts['mem'].add_self_dequeue_constraints(), solver
)

# 添加性能约束
cons = Sum(
    *[
        queues['mc'].deq_cnt[t] for t in range(time_steps)
    ]
) > 10
solver.assert_and_track(cons, 'perf_spec')
current_cons_name_map['perf_spec'] = cons

with open("smt.smt2", "w") as f:
    f.write(solver.to_smt2())

if solver.check() == sat:
    print('SAT')
    save_model(solver.model(), 'smt_model')
    for decl in solver.model().decls():
        var_name = decl.name()  # 获取变量名
        if 'deq_cnt' in str(var_name):  # 检查是否包含特定字符串
            print(f"{var_name} = {solver.model()[decl]}")  # 输出变量名和值
    # for ass in solver.assertions():
    #     z3_vars = get_vars(ass)
    #     for var in z3_vars:
    #         print(solver.model().evaluate(var, model_completion=True))
else:
    print('UNSAT')
    for name in solver.unsat_core():
        cons = current_cons_name_map.get(str(name), None)
        if cons is not None:
            print(f"{name} → {cons}")
        else:
            print(f"{name} → <no mapping found>")
