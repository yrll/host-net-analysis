# A fixed host network topology
import json

from z3 import *
from z3.z3util import get_vars

from my_solver import CPU, IIO
from queue_model import *
from queue_scheduling import *
from cache_model import *

from tabulate import tabulate


# 把queues里的各个queue的各个时刻的状态都打印出来
def prinf_trace(my_solver: MySolver, showLoc: bool = True, *queues: HNQueue):

    assert len(queues) > 0
    time_steps = queues[0].time_steps

    # 首先打印所有cnt值
    queues_cnt_map = {
        f'{q.queue_name} ({q.queue_size})': [
            q.print_cap_cnt_value(),
            q.print_val_cnt_value(),
            q.print_deq_cnt_value(),
            q.print_credit_cnt_value(),
            q.print_input_cnt_value()
        ]
        for q in queues
    }
    headers = ['Queue'] + [f'T{t} (c, v, d, cr, i)' for t in range(time_steps)]
    cnt_rows = []
    for q_name, q_cnts in queues_cnt_map.items():
        cnt_row = [q_name]
        for t in range(time_steps):
            cell = (q_cnts[0][t], q_cnts[1][t], q_cnts[2][t], q_cnts[3][t], q_cnts[4][t])
            cnt_row.append(cell)
        cnt_rows.append(cnt_row)
    print(tabulate(cnt_rows, headers=headers, tablefmt='grid'))

    # 打印各个队列的所有时刻状态
    print()
    print("="*40 + ' QUEUE STATE ' + "="*40)
    print()
    for q in queues:
        # 每个队列打印一张
        q_state = q.print_queue_state(showLoc)
        headers = [q.queue_name] + [f'T{i}' for i in range(time_steps)]
        state_rows = []
        for i in range(q.queue_size):
            state_row = [f'[{i}]'] + [q_state[t][i] for t in range(time_steps)]
            state_rows.append(state_row)
        print(tabulate(state_rows, headers=headers, tablefmt='grid'))

# def host_net_test1():
#     # 自定义主机网络拓扑和配置
#     time_steps = 6
#     my_solver = MySolver()
#
#     queues = {
#         CPU: HNQueue(solver=my_solver, queue_name=CPU, time_steps=time_steps, queue_size=3, cached=False,
#                        credit_based=True, src=CPU),
#         IIO: HNQueue(solver=my_solver, queue_name=IIO, time_steps=time_steps, queue_size=2, cached=False,
#                        credit_based=True, src=IIO),
#         'cha_raw': HNQueue(solver=my_solver, queue_name='cha_raw', time_steps=time_steps, queue_size=6, cached=True),
#         'cha_filtered': HNQueue(solver=my_solver, queue_name='cha_filtered', time_steps=time_steps, queue_size=6,
#                                 cached=False),
#         'mc': HNQueue(solver=my_solver, queue_name='mc', time_steps=time_steps, queue_size=7, cached=False),
#     }
#
#     llc = HNCache(solver=my_solver, cache_name='llc', time_steps=time_steps, cache_size=5)
#
#     # 初始化队列
#     for q in queues.values():
#         q.add_self_common_constraints()
#
#     # 初始化cache
#     llc.add_init_constraints()
#
#     # 队列调度
#     add_fifo_constraints(queues['mc'], queues['cha_filtered'], my_solver)
#     add_round_robin_constraints(queues['cha_raw'], queues[CPU], queues[IIO], my_solver)
#
#     # cache过滤
#     llc.add_cache_filter_constraints(queues['cha_raw'], queues['cha_filtered'])
#     llc.add_cache_replace_constraints(queues['mc'])
#     # request起点
#     queues[CPU].add_credit_flow_control_constraints(queues['cha_raw'], queues['mc'])
#     queues[IIO].add_credit_flow_control_constraints(queues['cha_raw'], queues['mc'])
#
#     # request终点
#     queues['mc'].add_self_dequeue_constraints()
#
#     # 添加性能约束
#     cons = Sum(
#         *[
#             queues['mc'].deq_cnt[t] for t in range(time_steps)
#         ]
#     ) > 1
#     my_solver.add_expr('perf_spec', cons)
#
#     my_solver.verify()
#
#
# def host_net_test2():
#     # 自定义主机网络拓扑和配置
#     time_steps = 6
#     my_solver = MySolver()
#
#     queues = {
#         CPU: HNQueue(solver=my_solver, queue_name=CPU, time_steps=time_steps, queue_size=3, cached=False,
#                        credit_based=True, src=CPU),
#         IIO: HNQueue(solver=my_solver, queue_name=IIO, time_steps=time_steps, queue_size=2, cached=False,
#                        credit_based=True, src=IIO),
#         'cha': HNQueue(solver=my_solver, queue_name='cha', time_steps=time_steps, queue_size=6, cached=False),
#         'mc': HNQueue(solver=my_solver, queue_name='mc', time_steps=time_steps, queue_size=7, cached=False),
#     }
#
#     # llc = HNCache(solver=my_solver, cache_name='llc', time_steps=time_steps, cache_size=5)
#
#     # 初始化队列
#     for q in queues.values():
#         q.add_self_common_constraints()
#
#     # 初始化cache
#     # llc.add_init_constraints()
#
#     # 队列调度
#     add_fifo_constraints(queues['mc'], queues['cha'], my_solver)
#     add_round_robin_constraints(queues['cha'], queues[CPU], queues[IIO], my_solver)
#
#     # cache过滤
#     # llc.add_cache_filter_constraints(queues['cha_raw'], queues['cha_filtered'])
#     # llc.add_cache_replace_constraints(queues['mc'])
#     # request起点
#     queues[CPU].add_credit_flow_control_constraints(queues['mc'])
#     queues[IIO].add_credit_flow_control_constraints(queues['mc'])
#
#     # request终点
#     queues['mc'].add_self_dequeue_constraints()
#
#     # 添加性能约束
#     cons = Sum(
#         *[
#             queues['mc'].deq_cnt[t] for t in range(time_steps)
#         ]
#     ) > 1
#     # my_solver.add_expr('perf_spec', cons)
#
#     my_solver.verify()

def cache_test():
    # 自定义主机网络拓扑和配置
    time_steps = 6
    my_solver = MySolver()

    queues = {
        CPU: HNQueue(solver=my_solver, queue_name=CPU, time_steps=time_steps, queue_size=7, cached=False,
                       credit_based=True, src=CPU),
        'raw': HNQueue(solver=my_solver, queue_name='raw', time_steps=time_steps, queue_size=6, cached=True),
        'fil': HNQueue(solver=my_solver, queue_name='fil', time_steps=time_steps, queue_size=6, cached=False),
        'mc': HNQueue(solver=my_solver, queue_name='mc', time_steps=time_steps, queue_size=4, cached=False),
    }

    cache = HNCache(solver=my_solver, cache_name='llc', time_steps=time_steps, cache_size=5)

    # 初始化队列
    for q in queues.values():
        q.add_self_common_constraints()
    # 队列调度
    add_fifo_constraints(queues['mc'], queues['fil'], my_solver)
    add_fifo_constraints(queues['raw'], queues[CPU], my_solver)

    cache.add_cache_replace_constraints(queues['mc'])
    cache.add_cache_filter_constraints(queues['raw'], queues['fil'])
    # request起点
    queues[CPU].add_credit_flow_control_constraints(queues['mc'], queues['raw'])

    # request终点
    queues['mc'].add_self_dequeue_constraints()

    # 添加性能约束
    cons = Sum(
        *[
            queues['mc'].deq_cnt[t] for t in range(time_steps)
        ]
    ) > 20
    # my_solver.add_expr('perf_spec', cons)

    my_solver.verify()
    if my_solver.model:
        prinf_trace(my_solver, True, *[q for q in queues.values()])

def rr_test():
    # 自定义主机网络拓扑和配置
    time_steps = 2
    my_solver = MySolver()

    queues = {
        CPU: HNQueue(solver=my_solver, queue_name=CPU, time_steps=time_steps, queue_size=3, cached=False,
                       credit_based=True, src=CPU),
        IIO: HNQueue(solver=my_solver, queue_name=IIO, time_steps=time_steps, queue_size=3, cached=False,
                       credit_based=True, src=IIO),
        'mc': HNQueue(solver=my_solver, queue_name='mc', time_steps=time_steps, queue_size=4, cached=False),
    }

    # 初始化队列
    for q in queues.values():
        q.add_self_common_constraints()
    # 队列调度
    add_round_robin_constraints(queues['mc'], queues[CPU], queues[IIO], my_solver)

    queues[CPU].set_init_state_test()
    queues[IIO].set_init_state_test()

    # request起点
    queues[CPU].add_credit_flow_control_constraints(queues['mc'])
    queues[IIO].add_credit_flow_control_constraints(queues['mc'])

    # request终点
    # queues['mc'].add_self_dequeue_constraints(1)

    # 添加性能约束
    cons = Sum(
        *[
            queues['mc'].deq_cnt[t] for t in range(time_steps)
        ]
    ) > 2
    # my_solver.add_expr('perf_spec', cons)

    my_solver.verify()
    if my_solver.model:
        prinf_trace(my_solver, *[q for q in queues.values()])




def fifo_test():
    # 自定义主机网络拓扑和配置
    time_steps = 5
    my_solver = MySolver()

    queues = {
        CPU: HNQueue(solver=my_solver, queue_name=CPU, time_steps=time_steps, queue_size=3, cached=False,
                       credit_based=True, src=CPU),
        'mc': HNQueue(solver=my_solver, queue_name='mc', time_steps=time_steps, queue_size=2, cached=False),
    }

    # 初始化队列
    for q in queues.values():
        q.add_self_common_constraints()
    # 队列调度
    add_fifo_constraints(queues['mc'], queues[CPU], my_solver)

    # request起点
    queues[CPU].add_credit_flow_control_constraints(queues['mc'])

    # request终点
    queues['mc'].add_self_dequeue_constraints()

    # 添加性能约束
    cons = Sum(
        *[
            queues['mc'].deq_cnt[t] for t in range(time_steps)
        ]
    ) > 5
    my_solver.add_expr('perf_spec', cons)

    my_solver.verify()
    if my_solver.model:
        prinf_trace(my_solver, *[q for q in queues.values()])




cache_test()