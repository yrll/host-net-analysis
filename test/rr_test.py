from util import prinf_trace
from my_solver import CPU, IIO
from queue_model import HNQueue
from queue_scheduling import *
from cache_model import HNCache




def rr_test():
    # 自定义主机网络拓扑和配置
    time_steps = 3
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
    add_round_robin_constraints(queues['mc'], queues[IIO], queues[CPU], my_solver)

    # queues[CPU].set_init_state_test()
    # queues[IIO].set_init_state_test()

    # request起点
    queues[CPU].add_credit_flow_control_constraints(queues['mc'])
    queues[IIO].add_credit_flow_control_constraints(queues['mc'])

    # request终点
    queues['mc'].add_self_dequeue_constraints()

    # 设置起点输入
    queues[CPU].set_max_input_constraints()
    queues[IIO].set_max_input_constraints()

    # 添加性能约束
    cons = Sum(
        *[
            queues['mc'].deq_cnt[t] for t in range(time_steps)
        ]
    ) > 5
    my_solver.add_expr('perf', cons)

    my_solver.verify(print_cons=True)
    prinf_trace(my_solver=my_solver, show_loc=True, queues=[q for q in queues.values()])

