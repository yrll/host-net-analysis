from typing import List

from z3 import *

from my_solver import MySolver
from queue_model import HNQueue


def z3_min(x, y):
    return If(x <= y, x, y)


"""
First-In-First-Out Scheduling
    Topology: q2[1:T][1:n] --> q1[1:T][1:m]
    Goal: Determine each element of q1
    Model: Suppose q1 dequeues k element at time t, where k = q1_deq_cnt(t), 
           then the ith element of q1 at time t (q1(t)[i]) would be:
            ① For 1 <= i <= q1_remain_cnt(t):
            q1(t)[i] == q1(t-1)[i+k]
            
            ② For q1_remain_cnt(t) < i <= q1_remain_cnt(t) + q2_deq_cnt(t):
            q1(t)[i] == q2(t-1)[j], where j = i – q1_remain_cnt(t) 
            
            ② For q1_remain_cnt(t) + q2_deq_cnt(t) < i < m: 
            q1(t)[i].isValid == false
    【注意】 q1不可以是 credit-based flow control的队列，但q2可以是
"""


def add_fifo_constraints(q1: HNQueue, q2: HNQueue, solver: MySolver):
    assert q1.time_steps == q2.time_steps
    # q2是被pull元素的那个，如果q2有cache，实际被pull的队列是保存q2经过cache后的状态的队列(shadow)
    if q2.cached:
        q2 = q2.shadow_queue
    for t in range(1, q1.time_steps):
        # 不由当前函数所决定的变量：
        q1_deq_t_1 = q1.deq_cnt[t - 1]
        q1_cap = q1.cap_cnt[t]
        q2_val_t_1 = q2.val_cnt[t - 1]
        q1_remain = q1.get_remain_cnt(t)
        q2_deq_t_1 = q2.deq_cnt[t - 1]
        # 由当前函数决定的变量：设置q2的dequeue值的约束
        name = f'cons_fifo_add_dequeue_for_{q2.queue_name}_at_time_{t}'
        cons = If(q1_cap - q2_val_t_1 < 0,
                  q2_deq_t_1 == q1_cap,
                  q2_deq_t_1 == q2_val_t_1)
        solver.add_expr(name, cons)
        # 由当前函数决定的变量：使用条件语句设置q1中每一个元素的值
        for nonzero_idx_i in range(1, q1.queue_size + 1):
            # 针对q1不同的dequeue值枚举
            for deq_var in range(q1.queue_size + 1):  # k是q1可能dequeue的数量
                if nonzero_idx_i + deq_var <= q1.queue_size:
                    # For 1 <= i <= q1_remain_cnt(t): q1(t)[i] == q1(t-1)[i+k]
                    cond = And(q1_deq_t_1 == deq_var, nonzero_idx_i <= q1_remain)
                    asgn = q1.queue_states[t][nonzero_idx_i - 1].get_eq_constraints(
                        q1.queue_states[t - 1][nonzero_idx_i + deq_var - 1])
                    name = f'cons_fifo_condition1_for_{q1.queue_name}_index_{nonzero_idx_i}_deq_{deq_var}_at_time_{t}'
                    cons = Implies(cond, asgn)
                    solver.add_expr(name, cons)
            # 针对q1不同的remain值枚举
            for q1_remain_var in range(q1.queue_size + 1):
                if 0 < nonzero_idx_i - q1_remain_var <= q2.queue_size:
                    # For q1_remain_cnt(t) < i <= q1_remain_cnt(t) + q2_deq_cnt(t):
                    # q1(t)[i] == q2(t-1)[j], where j = i – q1_remain_cnt(t)
                    cond = And(q1_remain == q1_remain_var, q1_remain < nonzero_idx_i,
                               nonzero_idx_i <= q1_remain + q2_deq_t_1)
                    asgn = q1.queue_states[t][nonzero_idx_i - 1].get_eq_constraints(
                        q2.queue_states[t - 1][nonzero_idx_i - 1 - q1_remain_var])
                    name = f'cons_fifo_condition2_for_{q1.queue_name}_index_{nonzero_idx_i}_remain_{q1_remain_var}_at_time_{t}'
                    cons = Implies(cond, asgn)
                    solver.add_expr(name, cons)
            # For q1_remain_cnt(t) + q2_deq_cnt(t) < i < m: q1(t)[i].isValid == false
            cond = And(q1_remain + q2_deq_t_1 < nonzero_idx_i, nonzero_idx_i <= q1.queue_size)
            asgn = q1.queue_states[t][nonzero_idx_i - 1].get_invalid_constraints()
            name = f'cons_fifo_condition3_for_{q1.queue_name}_index_{nonzero_idx_i-1}_at_time_{t}'
            cons = Implies(cond, asgn)
            solver.add_expr(name, cons)


"""
Round-Robin Scheduling
    Topology: q2[1:T][1:n] --> q1[1:T][1:m]
              q3[1:T][1:p] --> q1[1:T][1:m]
    Goal: Determine each element of q1
    【注意】 q1不可以是 credit-based flow control的队列，但q2/q3可以是
"""


# TODO: 支持任意数量的输入队列
def add_round_robin_constraints(q1: HNQueue, q2: HNQueue, q3: HNQueue, solver: MySolver):
    for t in range(1, q1.time_steps):
        q1_cap = q1.cap_cnt[t]
        q2_deq_t_1 = q2.deq_cnt[t - 1]
        q3_deq_t_1 = q3.deq_cnt[t - 1]
        q2_val_t_1 = q2.val_cnt[t - 1]
        q3_val_t_1 = q3.val_cnt[t - 1]

        # 添加q2和q3的dequeue数量的约束
        name1 = f'cons_ite_{q1.queue_name}_cap_not_even_at_time_{t}'
        cons1_ite_cap_not_even = If(q1_cap % 2 == 0,
                                    And(q2_deq_t_1 == q1_cap / 2, q3_deq_t_1 == q1_cap / 2),
                                    And(q2_deq_t_1 == q1_cap / 2 + 1, q3_deq_t_1 == q1_cap / 2))
        name2 = f'cons_ite_{q3.queue_name}_val_less_at_time_{t}'
        cons2_ite_q3_val_less = If(q3_val_t_1 <= q1_cap / 2,
                                   And(q3_deq_t_1 == q3_val_t_1, q2_deq_t_1 == q1_cap - q3_deq_t_1),
                                   cons1_ite_cap_not_even)
        name3 = f'cons_ite_{q2.queue_name}_val_less_at_time_{t}'
        cons3_ite_q2_val_less = If(q2_val_t_1 <= q1_cap / 2,
                                   And(q2_deq_t_1 == q2_val_t_1, q3_deq_t_1 == q1_cap - q2_deq_t_1),
                                   cons2_ite_q3_val_less)
        name4 = f'cons_assign_deq_cnt_for_{q2.queue_name}_and_{q3.queue_name}_at_time_{t}'
        cons4_ite_q2_plus_q3_le_q1_cap = If(q2_val_t_1 + q3_val_t_1 <= q1_cap,
                                            And(q2_deq_t_1 == q2_val_t_1, q3_deq_t_1 == q3_val_t_1),
                                            cons3_ite_q2_val_less)
        solver.add_expr(name4, cons4_ite_q2_plus_q3_le_q1_cap)

        # 使用条件语句设置q1中每一个元素的值，condition语句(cond)里都是用非零index做比较，assignment语句(asgn)里将index值统一减一
        q1_deq_t_1 = q1.deq_cnt[t - 1]
        q1_remain = q1.get_remain_cnt(t)
        for idx_i in range(q1.queue_size):
            # 针对q1不同的dequeue值枚举
            for k in range(q1.queue_size + 1):  # k是q1可能dequeue的数量
                if idx_i + k < q1.queue_size:
                    # For 1 <= i <= q1_remain_cnt(t): q1(t)[i] == q1(t-1)[i+k]
                    cond = And(q1_deq_t_1 == k, idx_i >= 0, idx_i < q1_remain)
                    asgn = q1.queue_states[t][idx_i].get_eq_constraints(
                        q1.queue_states[t - 1][idx_i + k])
                    name = f'cons_rr_condition1_for_index_{idx_i}_deq_{k}_at_time_{t}'
                    cons = Implies(cond, asgn)
                    solver.add_expr(name, cons)
            # 针对q1不同的remain值枚举
            for q1_remain_var in range(q1.queue_size + 1):
                j = idx_i - q1_remain_var  # q1_cap_var
                if j < 0:  # j是q1除去剩余元素后的起始index
                    continue
                for q2_deq_var in range(q2.queue_size + 1):
                    for q3_deq_var in range(q3.queue_size + 1):
                        # For q1_remain_cnt(t) < i <= q1_remain_cnt(t) + q2_deq_cnt(t-1) + q3_deq_cnt(t-1):
                        if not (0 <= j < q2_deq_var + q3_deq_var):
                            continue
                        # 当这些变量都等于当前值
                        commenCond = And(q1_remain_var == q1_remain,
                                         q2_deq_var == q2_deq_t_1,
                                         q3_deq_var == q3_deq_t_1)
                        # this if condition is from the following constraints' index, I don't know why actually
                        if j < 2 * min(q2_deq_var, q3_deq_var):
                            # 此时q1的元素等于q2和q3轮流赋值
                            name2 = f'cons_ite_{q1.queue_name}_idx_{idx_i}_q1remain_{q1_remain_var}_q2deq_{q2_deq_var}_q3deq_{q3_deq_var}_not_even_at_time_{t}'
                            cons2_ite_q1_cap_not_even = If(j % 2 == 1,
                                                           q1.queue_states[t][idx_i].get_eq_constraints(
                                                               q3.queue_states[t - 1][j // 2]
                                                           ),
                                                           q1.queue_states[t][idx_i].get_eq_constraints(
                                                               q2.queue_states[t - 1][j // 2]
                                                           )
                                                           )
                            cons = Implies(And(commenCond, idx_i >= q1_remain, j < 2 * z3_min(q2_deq_t_1, q3_deq_t_1)),
                                           cons2_ite_q1_cap_not_even)
                            solver.add_expr(name2, cons)
                        elif j < q2_deq_var + q3_deq_var:
                            # 此时q1的元素要么是q2要么是q3中的
                            name1 = f'cons_ite_{q2.queue_name}_deq_less_{q3.queue_name}_deq_at_time_{t}'
                            cons1_ite_q2_deq_less_q3_deq = If(q2_deq_t_1 < q3_deq_t_1,
                                                              q1.queue_states[t][idx_i].get_eq_constraints(
                                                                  q3.queue_states[t - 1][j - q2_deq_var]
                                                              ),
                                                              q1.queue_states[t][idx_i].get_eq_constraints(
                                                                  q2.queue_states[t - 1][j - q3_deq_var]
                                                              )
                                                              )
                            cons = Implies(And(commenCond, j >= 2 * z3_min(q2_deq_t_1, q3_deq_t_1)),
                                           cons1_ite_q2_deq_less_q3_deq)
                            solver.add_expr(name1, cons)

            # For q1_remain_cnt(t) + q2_deq_cnt(t) < i < m: q1(t)[i].isValid == false
            cond = And(idx_i >= q1_remain + q2_deq_t_1 + q3_deq_t_1)
            asgn = q1.queue_states[t][idx_i].get_invalid_constraints()
            name = f'cons_rr_condition3_for_index_{idx_i}_at_time_{t}'
            cons = Implies(cond, asgn)
            solver.add_expr(name, cons)

