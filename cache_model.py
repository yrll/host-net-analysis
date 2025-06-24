"""
每个Data request由CPU/RNIC发出，一个cache line大小的读/写请求
TODO: 区分读写请求
"""
from enum import Enum
from typing import Tuple

from z3 import *

from queue_model import QueueElem, HNQueue
from util import concat_name
from util import make_counter


class CacheElem:
    def __init__(self, name: str, ctx: Context):
        self.isValid = Bool(name + '_val', ctx)
        self.loc = Int(name + '_loc', ctx)
        self.lastAcc = Int(name + '_lastAcc', ctx)
        self.hits = Int(name + '_hits', ctx)


class HNCache:
    def __init__(self, ctx: Context, cache_name: str, time_steps: int, cache_size: int):
        self.cache_name = cache_name
        self.time_steps = time_steps
        self.cache_size = cache_size
        self.cache_states = {}
        # 辅助变量：记录当前时刻，每个cacheline，在下一时刻是否需要被替换
        self.replace_states = {}

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

    def init_time_zero(self) -> dict[str, ExprRef]:
        exprs = {}
        init_cache_state = self.cache_states[0]
        init_replace_state = self.replace_states[0]
        # exprs[f'init_{self.cache_name}_replace_state'] = And(*[And(Not(init_replace_state[i]),
        #                                                            Not(init_cache_state[i].isValid),
        #                                                            init_cache_state[i].lastAcc == 0,
        #                                                            init_cache_state[i].hits == 0) for i in
        #                                                        range(self.cache_size)])
        return exprs

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

    # TODO: 未把cache hit单独当作一个时间步可能存在的问题：
    # - L1/L2 cache 的替换和LLC的完全同步，只是数量不同，实际上可能一个步长内L1/L2应该被替换了不止一次
    # - cache中同一时刻被替换的元素没有先后顺序【等等，如果把cache也换成队列说不定可以，这样LRU的建模就更真了，但是如果一个时刻被替换的cache数量总是很多，这个建模是不是没有意义？】

    def add_cache_replace_constraints(self, queue: HNQueue) -> dict[str, ExprRef]:
        assert self.time_steps == queue.time_steps
        exprs = {}
        for t in range(self.time_steps - 1):
            deq_cnt = queue.deq_cnt[t]
            cache_state = self.cache_states[t]
            cache_state_t_plus_1 = self.cache_states[t + 1]
            replace_state = self.replace_states[t]
            queue_state = queue.queue_states[t]
            # 当前时刻需要替换的cache数量等于queue的dequeue数量, 但当dequeue数量大于cache size时，最多也只能替换cache size那么多个了
            replace_cnt = Sum([If(b, 1, 0) for b in self.replace_states[t]])
            name = f'{self.cache_name}_replace_cnt_at_time_{t}'
            cons = If(deq_cnt > self.cache_size, replace_cnt == self.cache_size, replace_cnt == deq_cnt)
            exprs[name] = cons
            # 如果一个cache被替换，则下一个时刻的loc值等于queue[n-deq_cnt, n]里任意一个，否则等于上i一个时刻的
            for i in range(self.cache_size):
                name = f'cons_{self.cache_name}_replace_index_{i}_at_time_{t}'
                cache_i_eq_any_deq_elem = [If(i + 1 > queue.queue_size - deq_cnt,
                                              And(cache_state_t_plus_1[i].loc == queue_state[j].reqLoc,
                                                  cache_state_t_plus_1[i].lastAcc == t,
                                                  cache_state_t_plus_1[i].isValid),
                                              False)
                                           for j in range(queue.queue_size)]
                cons = If(replace_state[i],
                          Or(*cache_i_eq_any_deq_elem),
                          And(cache_state_t_plus_1[i].isValid == cache_state[i].isValid,
                              cache_state_t_plus_1[i].lastAcc == cache_state[i].lastAcc + 1,
                              cache_state_t_plus_1[i].loc == cache_state[i].loc))
                exprs[name] = cons
            # 所有被替换的cache elem1，以及所有没替换的cache elem2，都存在lru(elem1, elem2)
            for i in range(self.cache_size):
                for j in range(self.cache_size):
                    if i == j:
                        continue
                    prefer_cons = Implies(And(replace_state[i], Not(replace_state[j])),
                                          Not(lru_compare(cache_state[i], cache_state[j])))
                    exclude_cons = Implies(And(replace_state[i], replace_state[j]),
                                           cache_state_t_plus_1[i].loc != cache_state_t_plus_1[j].loc)
            exprs[f'cache_{self.cache_name}_distinct_at_time_{t + 1}'] = Distinct(*[cache_state_t_plus_1[i].loc
                                                                                    for i in range(self.cache_size)])
        return exprs

    """
    constraints for cache hit: filter the hit elements in raw_queue, result in the filtered queue 
    
    cache hit happens within a single time step
    """

    def add_cache_filter_constraints(self, raw_queue: HNQueue, filtered_queue: HNQueue) -> dict[str, ExprRef]:
        exprs = {}
        assert hasattr(raw_queue, 'hit') and raw_queue.queue_size == filtered_queue.queue_size
        for t in range(self.time_steps):
            raw_queue_state = raw_queue.queue_states[t]
            raw_queue_hit_state = raw_queue.hit[t]
            filtered_queue_state = filtered_queue.queue_states[t]
            cache_state = self.cache_states[t]
            for i in range(raw_queue.queue_size):
                # constraints on the hit state
                name = f'cons_{raw_queue.queue_name}_hit_index_{i}_at_time_{t}'
                cons = raw_queue_hit_state[i] == Or(*[And(cache_state[j].loc == raw_queue_state[i].reqLoc,
                                                          cache_state[j].isValid, raw_queue_state[i].isValid)
                                                      for j in range(self.cache_size)])
                exprs[name] = cons
                # 为filtered_queue的元素赋值
                for j in range(filtered_queue.queue_size):
                    if j <= i:
                        name = f'cons_cache_filter_for_{filtered_queue.queue_size}_index_{j}_at_time_{t}'
                        cons = Implies(Sum(*raw_queue_hit_state[:i + 1]) == j + 1,
                                       filtered_queue_state[j].add_eq_constraints(raw_queue_state[i]))
                        exprs[name] = cons
        return exprs


"""
celem1会被替换: return false
celem2会被替换: return true
"""


def lru_compare(celem1: CacheElem, celem2: CacheElem) -> ExprRef:
    # 嵌套 If 模拟条件判断
    lru_expr = If(
        celem1.lastAcc > celem2.lastAcc,
        True,
        If(
            celem1.hits > celem2.hits,
            True,
            If(celem1.loc < celem2.loc, True, False)
        )
    )
    return lru_expr
