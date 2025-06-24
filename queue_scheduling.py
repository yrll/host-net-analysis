from typing import List

from z3 import *

from queue_model import HNQueue, SourceInput
from util import make_counter

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


def add_fifo_constraints(q1: HNQueue, q2: HNQueue) -> dict[str, ExprRef]:
    assert q1.time_steps == q2.time_steps
    exprs = {}
    for t in range(1, q1.time_steps):
        q1_deq_t_1 = q1.deq_cnt[t - 1]
        q2_deq_t_1 = q2.deq_cnt[t - 1]
        q1_cap = q1.cap_cnt[t]
        q1_remain = q1.queue_size - q1_cap

        # 使用条件语句设置q1中每一个元素的值，condition语句(cond)里都是用非零index做比较，assignment语句(asgn)里将index值统一减一
        for nonzero_idx_i in range(1, q1.queue_size + 1):
            # 针对q1不同的dequeue值枚举
            for k in range(q1.queue_size + 1):  # k是q1可能dequeue的数量
                if nonzero_idx_i + k <= q1.queue_size:
                    # For 1 <= i <= q1_remain_cnt(t): q1(t)[i] == q1(t-1)[i+k]
                    cond = And(q1_deq_t_1 == k, nonzero_idx_i >= 1, nonzero_idx_i <= q1_remain)
                    asgn = q1.queue_states[t][nonzero_idx_i - 1].add_eq_constraints(
                        q1.queue_states[t - 1][nonzero_idx_i + k - 1])
                    name = f'fifo_condition1_for_index_{nonzero_idx_i}_deq_{k}_at_time_{t}'
                    cons = Implies(cond, asgn)
                    exprs[name] = cons
            # 针对q1不同的remain值枚举
            for q1_remain_var in range(q1.queue_size + 1):
                if 0 < nonzero_idx_i - q1_remain_var <= q2.queue_size:
                    # For q1_remain_cnt(t) < i <= q1_remain_cnt(t) + q2_deq_cnt(t):
                    # q1(t)[i] == q2(t-1)[j], where j = i – q1_remain_cnt(t)
                    cond = And(q1_remain == q1_remain_var, nonzero_idx_i > q1_remain,
                               nonzero_idx_i <= q1_remain + q2_deq_t_1)
                    asgn = q1.queue_states[t][nonzero_idx_i - 1].add_eq_constraints(
                        q2.queue_states[t - 1][nonzero_idx_i - q1_remain_var - 1])
                    name = f'fifo_condition2_for_index_{nonzero_idx_i}_remain_{q1_remain_var}_at_time_{t}'
                    cons = Implies(cond, asgn)
                    exprs[name] = cons
            # For q1_remain_cnt(t) + q2_deq_cnt(t) < i < m: q1(t)[i].isValid == false
            cond = And(nonzero_idx_i > q1_remain + q2_deq_t_1, nonzero_idx_i <= q1.queue_size)
            asgn = q1.queue_states[t][nonzero_idx_i - 1].add_invalid_constraints()
            name = f'fifo_condition3_for_index_{nonzero_idx_i}_at_time_{t}'
            cons = Implies(cond, asgn)
            exprs[name] = cons

        # 设置q2的dequeue值的约束
        q2_val_t_1 = q2.val_cnt[t - 1]
        cond = q1_cap - q2_val_t_1 < 0
        true_asgn = q2_deq_t_1 == q1_cap
        false_asgn = q2_deq_t_1 == q2_val_t_1
        name = f'fifo_add_dequeue_for_{q1.queue_name}_at_time_{t}'
        cons = If(cond, true_asgn, false_asgn)
        exprs[name] = cons
    return exprs


"""
Round-Robin Scheduling
    Topology: q2[1:T][1:n] --> q1[1:T][1:m]
              q3[1:T][1:p] --> q1[1:T][1:m]
    Goal: Determine each element of q1
    【注意】 q1不可以是 credit-based flow control的队列，但q2/q3可以是
"""


# TODO: 支持任意数量的输入队列
def add_round_robin_constraints(q1: HNQueue, q2: HNQueue, q3: HNQueue) -> dict[str, ExprRef]:
    exprs = {}
    for t in range(1, q1.time_steps):
        q1_cap = q1.cap_cnt[t]
        q2_deq_t_1 = q2.deq_cnt[t - 1]
        q3_deq_t_1 = q3.deq_cnt[t - 1]
        q2_val_t_1 = q2.val_cnt[t - 1]
        q3_val_t_1 = q3.val_cnt[t - 1]

        # 添加q2和q3的dequeue数量的约束
        name1 = f'ite_{q1.queue_name}_cap_not_even_at_time_{t}'
        cons1_ite_cap_not_even = If(q1_cap % 2 == 0,
                             And(q2_deq_t_1 == q1_cap / 2, q3_deq_t_1 == q1_cap / 2),
                             And(q2_deq_t_1 == q1_cap / 2 + 1, q3_deq_t_1 == q1_cap / 2))
        name2 = f'ite_{q3.queue_name}_val_less_at_time_{t}'
        cons2_ite_q3_val_less = If(q3_val_t_1 <= q1_cap / 2,
                            And(q3_deq_t_1 == q3_val_t_1, q2_deq_t_1 == q1_cap - q3_deq_t_1),
                            cons1_ite_cap_not_even)
        name3 = f'ite_{q2.queue_name}_val_less_at_time_{t}'
        cons3_ite_q2_val_less = If(q2_val_t_1 <= q1_cap / 2,
                            And(q2_deq_t_1 == q2_val_t_1, q3_deq_t_1 == q1_cap - q2_deq_t_1),
                            cons2_ite_q3_val_less)
        name4 = f'ite_{q2.queue_name}_plus_{q3.queue_name}_le_{q1.queue_name}_at_time_{t}'
        cons4_ite_q2_plus_q3_le_q1_cap = If(q2_val_t_1 + q3_val_t_1 <= q1_cap,
                                     And(q2_deq_t_1 == q2_val_t_1, q3_deq_t_1 == q3_val_t_1),
                                     cons3_ite_q2_val_less)
        exprs[name1] = cons1_ite_cap_not_even
        exprs[name2] = cons2_ite_q3_val_less
        exprs[name3] = cons3_ite_q2_val_less
        exprs[name4] = cons4_ite_q2_plus_q3_le_q1_cap

        # 使用条件语句设置q1中每一个元素的值，condition语句(cond)里都是用非零index做比较，assignment语句(asgn)里将index值统一减一
        q1_deq_t_1 = q1.deq_cnt[t - 1]
        q1_remain = q1.queue_size - q1_cap
        for nonzero_idx_i in range(1, q1.queue_size + 1):
            # 针对q1不同的dequeue值枚举
            for k in range(q1.queue_size + 1):  # k是q1可能dequeue的数量
                if nonzero_idx_i + k <= q1.queue_size:
                    # For 1 <= i <= q1_remain_cnt(t): q1(t)[i] == q1(t-1)[i+k]
                    cond = And(q1_deq_t_1 == k, nonzero_idx_i >= 1, nonzero_idx_i <= q1_remain)
                    asgn = q1.queue_states[t][nonzero_idx_i - 1].add_eq_constraints(
                        q1.queue_states[t - 1][nonzero_idx_i + k - 1])
                    name = f'rr_condition1_for_index_{nonzero_idx_i}_deq_{k}_at_time_{t}'
                    cons = Implies(cond, asgn)
                    exprs[name] = cons
            # 针对q1不同的remain值枚举
            for q1_remain_var in range(q1.queue_size + 1):
                j = nonzero_idx_i - q1_remain_var  # q1_cap_var
                for q2_deq_var in range(q2.queue_size + 1):
                    for q3_deq_var in range(q3.queue_size + 1):
                        # For q1_remain_cnt(t) < i <= q1_remain_cnt(t) + q2_deq_cnt(t-1) + q3_deq_cnt(t-1):
                        if not (0 < j <= q2_deq_var + q3_deq_var):
                            continue
                        # this if condition is from the following constraints' index, I don't know why actually
                        if 0 <= j - q2_deq_var - 1 < q3.queue_size and 0 <= j - q3_deq_var - 1 < q2.queue_size and \
                                j // 2 + 1 < q2.queue_size and j // 2 < q3.queue_size:
                            commenCond = And(q1_remain_var == q1_remain,
                                             q2_deq_var == q2_deq_t_1,
                                             q3_deq_var == q3_deq_t_1)
                            name1 = f'ite_{q2.queue_name}_deq_less_{q3.queue_name}_deq_at_time_{t}_*{make_counter()()}'
                            cons1_ite_q2_deq_less_q3_deq = If(q2_deq_t_1 < q3_deq_t_1,
                                                        q1.queue_states[t][nonzero_idx_i - 1].add_eq_constraints(
                                                            q3.queue_states[t - 1][j - q2_deq_var - 1]
                                                        ),
                                                        q1.queue_states[t][nonzero_idx_i - 1].add_eq_constraints(
                                                            q2.queue_states[t - 1][j - q3_deq_var - 1]
                                                        )
                                                        )
                            name2 = f'ite_{q1.queue_name}_cap_not_even_at_time_{t}_*{make_counter()()}'
                            cons2_ite_q1_cap_not_even = If(j % 2 == 1,
                                                     q1.queue_states[t][nonzero_idx_i - 1].add_eq_constraints(
                                                         q2.queue_states[t - 1][j // 2 + 1]
                                                     ),
                                                     q1.queue_states[t][nonzero_idx_i - 1].add_eq_constraints(
                                                         q3.queue_states[t - 1][j // 2]
                                                     )
                                                     )
                            name3 = f'ite_within_in_turn_at_time_{t}_*{make_counter()()}'
                            cons3_ite_within_in_turn = If(j <= 2 * min(q2_deq_var, q3_deq_var),
                                                    cons2_ite_q1_cap_not_even,
                                                    cons1_ite_q2_deq_less_q3_deq)
                            name4 = f'in_the_all_at_time_{t}_*{make_counter()()}'
                            cons4_in_the_all = Implies(commenCond, cons3_ite_within_in_turn)
                            # add constraints to exprs
                            exprs[name1] = cons1_ite_q2_deq_less_q3_deq
                            exprs[name2] = cons2_ite_q1_cap_not_even
                            exprs[name3] = cons3_ite_within_in_turn
                            exprs[name4] = cons4_in_the_all

            # For q1_remain_cnt(t) + q2_deq_cnt(t) < i < m: q1(t)[i].isValid == false
            cond = And(nonzero_idx_i > q1_remain + q2_deq_t_1 + q3_deq_t_1, nonzero_idx_i <= q1.queue_size)
            asgn = q1.queue_states[t][nonzero_idx_i - 1].add_invalid_constraints()
            name = f'rr_condition3_for_index_{nonzero_idx_i}_at_time_{t}'
            cons = Implies(cond, asgn)
            exprs[name] = cons

    return exprs




