from util import prinf_trace
from my_solver import CPU, IIO
from queue_model import HNQueue
from queue_scheduling import *
from cache_model import HNCache


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
    queues[CPU].set_max_input_constraints()

    # 添加性能约束
    cons = Sum(
        *[
            queues['mc'].deq_cnt[t] for t in range(time_steps)
        ]
    ) > 6
    # cons = queues[CPU].input_cnt[0] == queues[CPU].queue_size
    # cons = And(
    #     *[
    #         queues['cpu'].input_cnt[t] > 0 for t in range(time_steps)
    #     ]
    # )
    # my_solver.add_expr('perf_spec', cons)

    my_solver.verify()
    prinf_trace(my_solver=my_solver, show_loc=True, queues=[q for q in queues.values()])