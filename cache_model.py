"""
每个Data request由CPU/RNIC发出，一个cache line大小的读/写请求
TODO: 区分读写请求
"""
from enum import Enum
from typing import Tuple

from z3 import *

from my_solver import MySolver
from queue_model import ReqElem, HNQueue
from util import concat_name, concat_tuple_or_str


class CacheElem:
    def __init__(self, name: str, ctx: Context):
        self.isValid = Bool(name + '_valid', ctx)
        self.loc = Int(name + '_loc', ctx)
        self.lastAcc = Int(name + '_lastAcc', ctx)
        self.hits = Int(name + '_hits', ctx)

    def print_model_value(self, model: ModelRef, show_details=False) -> Tuple:
        isVal = model.evaluate(self.isValid)
        lastAcc = model.evaluate(self.lastAcc)
        hits = model.evaluate(self.hits, model_completion=True)
        loc = model.evaluate(self.loc)

        if model[self.isValid] is not None:
            if isVal:
                if show_details:
                    return loc, lastAcc, hits
                return loc
            else:
                return 'Non'
        else:
            return 'Any'


class HNCache:
    def __init__(self, solver: MySolver, cache_name: str, time_steps: int, cache_size: int):
        ctx = solver.ctx
        self.solver = solver
        self.cache_name = cache_name
        self.time_steps = time_steps
        self.cache_size = cache_size
        self.cache_states = {}
        # 辅助变量：记录当前时刻，每个cacheline，在下一时刻是否需要被替换
        self.replace_states = {}
        # self.replace_cnt = [Int(f'')]

        # 初始化各个时刻的队列状态
        for t in range(self.time_steps):
            self.replace_states[t] = [
                Bool(name=f'{cache_name}_replace_index_{i}_at_time_{t}', ctx=ctx)
                for i in range(cache_size)
            ]
            self.cache_states[t] = [
                CacheElem(name=f"{cache_name}_index_{i}_time_{t}", ctx=ctx)
                for i in range(cache_size)
            ]

    # 初始状态没有valid的cache
    def add_init_constraints(self):
        init_cache_state = self.cache_states[0]
        init_replace_state = self.replace_states[0]
        name = f'cons_init_{self.cache_name}_replace_state'
        cons = And(*[And(
            Not(init_cache_state[i].isValid),
            init_cache_state[i].lastAcc == 0,
            init_cache_state[i].hits == 0) for i in
            range(self.cache_size)])
        self.solver.add_expr(name, cons)

    def get_replace_cnt(self, t):
        return Sum(*[self.replace_states[t][i] for i in range(self.cache_size)])

    """
    The next replaced cacheline at time t, let it be rep(t), should satisfied both:
    ⋁_("i" ∈"[1,s] " )▒"rep(t) == c(t)[i] " 
    ⋀_("i" ∈"[1,s]" )▒" LRU(c(t)[i], rep(t)) == True "   // c(t)[i] was used more recently and more frequently than rep(t)
    
    LRU(c(t)[i], rep(t)) --> Bool:
    If c(t)[i].lastAcc > rep(t).lastAcc:
        return true
    else If c(t)[i].hitCnt > rep(t).hitCnt:
        return true
    else If c(t)[i].loc < rep(t).loc:
        return true
    return false
    """
    """
    cache_replace函数：给定一个队列，这个队列每个时刻dequeue的元素，将会替换cache中现有的元素，但dequeue的数量需要小于cache size
    """

    # cache replace也需要一个时间步长：
    # - L1/L2 cache 的替换和LLC的完全同步，只是数量不同，实际上可能一个步长内L1/L2应该被替换了不止一次
    # - cache中同一时刻被替换的元素没有先后顺序【等等，如果把cache也换成队列说不定可以，这样LRU的建模就更真了，但是如果一个时刻被替换的cache数量总是很多，这个建模是不是没有意义？】
    # TODO: 当 deq_cnt > cache_size 且 q[:deq_cnt]里有重复元素时...

    def add_cache_replace_constraints(self, queue: HNQueue, exclusive_replace=True):
        assert self.time_steps == queue.time_steps
        for t in range(self.time_steps - 1):
            cache_state = self.cache_states[t]
            cache_state_t_plus_1 = self.cache_states[t + 1]
            replace_state = self.replace_states[t]
            queue_state = queue.queue_states[t]

            # 首先确定需要替换的cache数量: 要么等于cache size, 要么等于deq的元素中distinct的元素数量
            # 当前时刻需要替换的cache数量等于queue的dequeue数量, 但当dequeue数量大于cache size时，最多也只能替换cache size那么多个了
            deq_cnt = queue.deq_cnt[t]
            name = f'cons_{self.cache_name}_replace_cnt_at_time_{t}'
            # 设置替换的cache总数
            replace_cnt = Sum([If(b, 1, 0) for b in self.replace_states[t]])
            # 选择是否允许重复cache元素出现
            if exclusive_replace:
                # 辅助变量
                deq_distinct_cnt = Int(f'distinct_deq_cnt_{queue.queue_name}_at_time_{t}', ctx=self.solver.ctx)
                self.solver.add_expr(f'cons_distinct_deq_cnt_{queue.queue_name}_at_time_{t}',
                                     queue.get_distinct_deq_cnt_constraints(deq_distinct_cnt, t, queue.queue_size))
                cons = If(deq_distinct_cnt > self.cache_size, replace_cnt == self.cache_size, replace_cnt == deq_distinct_cnt)
            else:
                cons = If(deq_cnt > self.cache_size, replace_cnt == self.cache_size, replace_cnt == deq_cnt)

            self.solver.add_expr(name, cons)
            # 如果一个cache被替换，则下一个时刻的loc值等于queue[n-deq_cnt, n]里任意一个，否则等于上i一个时刻的
            for i in range(self.cache_size):
                name = f'cons_{self.cache_name}_replace_index_{i}_at_time_{t}'
                cache_i_eq_any_deq_elem = Or(*[If(j < deq_cnt,
                                                  And(cache_state_t_plus_1[i].loc == queue_state[j].reqLoc,
                                                      cache_state_t_plus_1[i].lastAcc == t + 1,
                                                      cache_state_t_plus_1[i].isValid,),
                                                  False)
                                               for j in range(queue.queue_size)])
                cons = If(replace_state[i],
                          cache_i_eq_any_deq_elem,
                          And(cache_state_t_plus_1[i].isValid == cache_state[i].isValid,
                              cache_state_t_plus_1[i].lastAcc == cache_state[i].lastAcc,
                              cache_state_t_plus_1[i].loc == cache_state[i].loc))
                self.solver.add_expr(name, cons)
            # 所有被替换的cache elem1，以及所有没替换的cache elem2，都存在lru(elem1, elem2)
            for i in range(self.cache_size):
                for j in range(self.cache_size):
                    if i == j:
                        continue
                    prefer_cons = Implies(And(replace_state[i], Not(replace_state[j])),
                                          Not(lru_compare(cache_state[i], cache_state[j])))
                    exclude_cons = Implies(And(replace_state[i], replace_state[j]),
                                           cache_state_t_plus_1[i].loc != cache_state_t_plus_1[j].loc)
                    self.solver.add_expr(f"cons_{self.cache_name}_prefer", prefer_cons)
                    if exclusive_replace:
                        self.solver.add_expr(f"cons_{self.cache_name}_distinct", exclude_cons)


    """
    constraints for cache hit
    raw queue和filtered queue共同组成每个时刻的队列状态:  
        raw queue中仅是【当前时刻t入队的, 未判断是否cache命中】的元素
        filtered queue中是【当前时刻t及t以前时刻内, 所有入队但还未出队, 且cache未命中】的元素
        
    cache hit happens within a single time step
    """

    def add_cache_filter_constraints(self, raw_queue: HNQueue):
        assert hasattr(raw_queue, 'hit') and hasattr(raw_queue, 'shadow_queue')
        filtered_queue = raw_queue.shadow_queue
        # raw queue每次全部元素出队
        raw_queue.add_self_dequeue_constraints()
        # 设置filtered queue的状态
        for t in range(self.time_steps):
            # 设置raw queue的每个元素的cache hit状态
            raw_queue_state = raw_queue.queue_states[t]
            raw_queue_hit_state = raw_queue.hit[t]
            cache_state = self.cache_states[t]
            for i in range(raw_queue.queue_size):
                # constraints on the hit state
                name = f'cons_{raw_queue.queue_name}_hit_index_{i}_at_time_{t}'
                # 当前队列元素valid再判断cache hit: cache hit的标志是当前元素的loc和任一cache元素的loc一样
                cons = raw_queue_hit_state[i] == If(
                    raw_queue_state[i].isValid,
                    If(
                        Or(
                            *[And(cache_state[j].loc == raw_queue_state[i].reqLoc, cache_state[j].isValid)
                              for j in range(self.cache_size)]
                        ),
                        True,
                        False),
                    False
                )
                self.solver.add_expr(name, cons)

            filtered_remain = filtered_queue.queue_size - filtered_queue.cap_cnt[t]
            filtered_enq = raw_queue.val_cnt[t] - raw_queue.get_hit_cnt(t)
            filtered_queue_state = filtered_queue.queue_states[t]
            # 为【t】时刻 filtered_queue 的index为i 的元素赋值
            for i in range(filtered_queue.queue_size):
                # step 1: 平移deq数量的元素
                if t > 0:
                    for deq_var in range(filtered_queue.queue_size + 1):
                        if i + deq_var < filtered_queue.queue_size:
                            name = f"cons_for_{filtered_queue.queue_name}_deq_{deq_var}_index_{i}_at_time_{t}"
                            cons = Implies(
                                And(i < filtered_remain, deq_var == filtered_queue.deq_cnt[t - 1]),
                                filtered_queue_state[i].get_eq_constraints(
                                    filtered_queue.queue_states[t - 1][i + deq_var])
                            )
                            self.solver.add_expr(name, cons)
                # step 2: 用raw queue中未命中cache的元素填补filtered queue
                filtered_enq_index = i - filtered_remain  # filtered queue里除去剩余元素后的起始index
                for filtered_enq_index_var in range(filtered_queue.queue_size):
                    for k in range(raw_queue.queue_size):  # k是raw queue里元素的index
                        # 同一元素的filtered_enq_index一定不大于在raw queue里的index(避免bubble)
                        if k < filtered_enq_index_var:
                            continue
                        index_cons = And(filtered_remain <= i,
                                         i < filtered_remain + filtered_enq,
                                         filtered_enq_index == filtered_enq_index_var)
                        hit_cnt_cons = Sum(*raw_queue_hit_state[:k + 1]) == k - filtered_enq_index
                        cons = Implies(And(index_cons, hit_cnt_cons),
                                       filtered_queue_state[i].get_eq_constraints(raw_queue_state[k]))
                        name = f'cons_{filtered_queue.queue_name}_non_hit_index_{i}_raw_{k}_at_time_{t}'
                        self.solver.add_expr(name, cons)

                # 剩余元素设置valid为false
                # For filtered_remain + raw_non_hit_cnt < i < queue_size
                cond = And(filtered_remain + filtered_enq <= i)
                asgn = filtered_queue_state[i].get_invalid_constraints()
                name = f'cons_{filtered_queue.queue_name}_invalid_index_{i}_at_time_{t}'
                cons = Implies(cond, asgn)
                self.solver.add_expr(name, cons)

    # 打印cache状态, 包括replacement状态
    def print_cache_state(self, show_details=False) -> {}:
        assert self.solver.model
        c_states = {}
        for t in range(self.time_steps):
            s = []
            for i in range(self.cache_size):
                elem_state = self.cache_states[t][i].print_model_value(self.solver.model, show_details)
                replace_state = self.solver.evaluate(self.replace_states[t][i])
                # 简化True/False
                s.append(concat_tuple_or_str(elem_state, replace_state))
            c_states[t] = s
        return c_states

    # 打印cache替换状态
    def print_cache_replace_state(self) -> {}:
        assert self.solver.model
        c_states = {
            t: [self.solver.evaluate(self.replace_states[t][i]) for i in range(self.cache_size)]
            for t in range(self.time_steps)
        }
        return c_states

    def set_cache_replace_cnt_constraints(self, max_rep_cnt):
        cons = Sum(
            *[
                Sum(*[
                    self.replace_states[t][i] for i in range(self.cache_size)
                ])
                for t in range(self.time_steps)
            ]
        ) >= max_rep_cnt
        self.solver.add_expr(f'set_cache_replace_cnt_for_{self.cache_name}', cons)

"""
celem1会被替换: return false
celem2会被替换: return true 
"""


def lru_compare(celem1: CacheElem, celem2: CacheElem) -> ExprRef:
    # 嵌套 If 模拟条件判断
    lru_expr = If(
        And(celem1.isValid, Not(celem2.isValid)),
        True,
        If(
            celem1.lastAcc > celem2.lastAcc,
            True,
            If(
                celem1.hits > celem2.hits,
                True,
                If(celem1.loc < celem2.loc, True, False)
            )
        )
    )
    return lru_expr
