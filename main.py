# A fixed host network topology
import json

from z3 import *
from z3.z3util import get_vars

from host_topology import HostNetwork
from my_solver import CPU, IIO
from queue_model import HNQueue
from queue_scheduling import *
from cache_model import HNCache

from tabulate import tabulate

from tabulate import tabulate


# 把queues里的各个queue的各个时刻的状态都打印出来
def prinf_trace(my_solver: MySolver, show_loc: bool = True, queues: [HNQueue] = None, caches: [HNCache] = None):
    if not my_solver.model:
        return
    time_steps = queues[0].time_steps

    # 打印队列的cnt状态
    if queues is not None and len(queues) > 0:
        # 把shadow的队列也打印出来
        for q in queues:
            if q.cached:
                queues.append(q.shadow_queue)

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
        print("=" * 40 + ' QUEUE STATE ' + "=" * 40)
        print()
        for q in queues:
            # 每个队列打印一张
            q_state = q.print_queue_state(show_loc)
            headers = [q.queue_name] + [f'T{i} (src, t, loc, hit)' for i in range(time_steps)]
            state_rows = []
            for i in range(q.queue_size):
                state_row = [f'[{i}]'] + [q_state[t][i] for t in range(time_steps)]
                state_rows.append(state_row)
            print(tabulate(state_rows, headers=headers, tablefmt='grid'))

    if caches is not None and len(caches) > 0:
        for c in caches:
            # 每个队列打印一张状态表：包括地址和替换状态
            c_state = c.print_cache_state(True)
            headers = [c.cache_name] + [f'T{i} (loc, acc, hits, rep)' for i in range(time_steps)]
            state_rows = []
            for i in range(c.cache_size):
                state_row = [f'[{i}]'] + [c_state[t][i] for t in range(time_steps)]
                state_rows.append(state_row)
            print(tabulate(state_rows, headers=headers, tablefmt='grid'))


def host_net_test1():
    # 自定义主机网络拓扑和配置
    time_steps = 10

    my_solver = MySolver()
    queues = {
        CPU: HNQueue(solver=my_solver, queue_name=CPU, time_steps=time_steps, queue_size=2, credit_based=True, src=CPU),
        IIO: HNQueue(solver=my_solver, queue_name=IIO, time_steps=time_steps, queue_size=5, credit_based=True,
                     src=IIO),
        'cha': HNQueue(solver=my_solver, queue_name='cha', time_steps=time_steps, queue_size=6, cached=True),
        'mc': HNQueue(solver=my_solver, queue_name='mc', time_steps=time_steps, queue_size=4, cached=False),
    }
    llc = HNCache(solver=my_solver, cache_name='llc', time_steps=time_steps, cache_size=8)

    host_net = HostNetwork(queues=queues, cache=llc, solver=my_solver)

    host_net.initialize()

    # 队列调度
    add_fifo_constraints(queues['mc'], queues['cha'], my_solver)
    add_round_robin_constraints(queues['cha'], queues[CPU], queues[IIO], my_solver)

    # cache过滤
    llc.add_cache_filter_constraints(queues['cha'])
    llc.add_cache_replace_constraints(queues['mc'])
    # request起点
    queues[CPU].add_credit_flow_control_constraints([queues['cha'], queues['mc']])
    queues[IIO].add_credit_flow_control_constraints([queues['cha'], queues['mc']])

    # request终点
    queues['mc'].add_self_dequeue_constraints(fixed_deq=host_net.time_length)
    # queues[CPU].set_max_input_constraints()
    # queues[IIO].set_max_input_constraints()

    # 添加性能约束
    cons = And(queues[CPU].get_processed_sum() > queues[IIO].get_processed_sum())
    cons = And(queues[CPU].get_latency_avg() > queues[IIO].get_latency_avg(),
               queues[CPU].get_processed_sum() == queues[IIO].get_processed_sum(),
               queues[IIO].get_processed_sum() > 6)
    my_solver.add_expr('perf_spec', cons)

    my_solver.verify()
    prinf_trace(my_solver, True, list(queues.values()), [llc])


if __name__ == "__main__":
    host_net_test1()
