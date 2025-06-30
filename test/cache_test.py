from main import prinf_trace
from my_solver import CPU, IIO
from queue_model import HNQueue
from queue_scheduling import *
from cache_model import HNCache


def cache_test():
    # 自定义主机网络拓扑和配置
    time_steps = 6
    my_solver = MySolver()

    queues = {
        CPU: HNQueue(solver=my_solver, queue_name=CPU, time_steps=time_steps, queue_size=7, cached=False,
                     credit_based=True, src=CPU),
        'cha': HNQueue(solver=my_solver, queue_name='cha', time_steps=time_steps, queue_size=6, cached=True),
        'mc': HNQueue(solver=my_solver, queue_name='mc', time_steps=time_steps, queue_size=5, cached=False),
    }

    cache = HNCache(solver=my_solver, cache_name='llc', time_steps=time_steps, cache_size=4)

    # 初始化队列
    for q in queues.values():
        q.add_self_common_constraints()
    # 队列调度
    add_fifo_constraints(queues['mc'], queues['cha'], my_solver)
    add_fifo_constraints(queues['cha'], queues[CPU], my_solver)

    cache.add_init_constraints()
    cache.add_cache_replace_constraints(queues['mc'])
    cache.add_cache_filter_constraints(queues['cha'])
    # request起点
    queues[CPU].add_credit_flow_control_constraints([queues['mc'], queues['cha']], time_length=4)
    # request终点
    queues['mc'].add_self_dequeue_constraints(4)

    # 性能约束
    queues[CPU].set_max_input_constraints()
    cache.set_cache_replace_cnt_constraints(11)
    # 添加性能约束
    cons = Sum(
        *[
            queues['mc'].deq_cnt[t] for t in range(time_steps)
        ]
    ) > 10
    # cons = Sum(
    #     *[
    #         cache.get_replace_cnt(t) for t in range(time_steps)
    #     ]
    # ) > 1

    # cons = And(
    #     *[queues['cpu'].deq_cnt[t] > 0 for t in range(time_steps)]
    # )
    # cons = And(
    #     cons,
    #     Sum(*[
    #         queues['cha'].get_hit_cnt(t) for t in range(time_steps)
    #     ]) < 1
    # )
    # my_solver.add_expr('perf_spec', cons)

    my_solver.verify(print_cons=True)
    prinf_trace(my_solver=my_solver, show_loc=True, queues=[q for q in queues.values()], caches=[cache])

def cache_replace_test():
    # 自定义主机网络拓扑和配置
    time_steps = 2
    my_solver = MySolver()

    queue = HNQueue(solver=my_solver, queue_name='cha', time_steps=time_steps, queue_size=7, cached=False, src=CPU)
    queue.add_self_common_constraints()

    cons = And(*[
        And(
            queue.queue_states[0][i].isValid,
            queue.queue_states[0][i].source == my_solver.get_source_const(CPU),
            queue.queue_states[0][i].reqLoc == i % 4
        )
        for i in range(queue.queue_size)
    ])
    my_solver.add_expr("init_q_state_test", cons)

    cache = HNCache(solver=my_solver, cache_name='llc', time_steps=time_steps, cache_size=5)
    cons = And(*[
        cache.cache_states[0][i].isValid for i in range(cache.cache_size)
    ])
    cons = And(
        Distinct(*[cache.cache_states[0][i].loc for i in range(cache.cache_size)]),
        cons
    )
    cons = And(
        Distinct(*[cache.cache_states[0][i].lastAcc for i in range(cache.cache_size)]),
        cons
    )
    my_solver.add_expr("init_cache_state_test", cons)

    cache.add_cache_replace_constraints(queue)
    # cache.add_cache_filter_constraints(queues['cha'])
    # request起点
    # queues[CPU].add_credit_flow_control_constraints(queues['mc'], queues['cha'])
    # request终点
    queue.add_self_dequeue_constraints()

    # 性能约束
    # queue.set_input_req_loc_distinct_constraints()
    # queues[CPU].set_init_state_test()
    # queues[CPU].set_max_input_constraints()

    # 添加性能约束

    my_solver.verify()
    prinf_trace(my_solver=my_solver, show_loc=True, queues=[queue], caches=[cache])

cache_test()


