"""
queue model是连接队列的组件 (参考 FPerf)
每个 queue model 可以有 n 个 input queues，和 m 个 output queues
可以通过不同的调度算法实现 n input queues --> m output queues 的 transition
"""
from __future__ import annotations

from z3 import Context, Bool, Int, Const, ExprRef, And, Not, Sum, If, Implies, Solver, EnumSort, ModelRef
from my_solver import MySolver, CPU

"""
Queue in the host network (HNQueue): 
    The state of a queue q at time t is represented as q(1:T)[1:L], 
    where L is the length of q, T is the total timestep we try to model 
    The dependency of a queue with others queues is ** the dequeue number **, represented as q_deq_cnt(1:T)

Each element q(t)[i] in the queue consists of (QueueElem):
    isValid: Bool         whether the element exist at time t
    source: Enum       the source of this request, e.g., CPU or IO
    reqLoc: Int            the memory location required by this request
    startTime: Int       the start time of this request
"""
from enum import Enum
from typing import List, Dict, Any, Tuple


class RequestType(Enum):
    READ = 0
    WRITE = 1


class ScheduleAlgo(Enum):
    FIFO = "fifo"
    RoundRobin = "round-robin"


class ReqElem:
    def __init__(self, name: str, ctx: Context, src_sort: EnumSort):
        self.isValid = Bool(name + '_val', ctx)
        self.source = Const(name + '_src', src_sort)
        self.reqLoc = Int(name + '_loc', ctx)
        self.startTime = Int(name + '_stime', ctx)

    def get_eq_constraints(self, elem: 'ReqElem') -> ExprRef:
        return And(elem.isValid == self.isValid,
                   elem.source == self.source,
                   elem.reqLoc == self.reqLoc,
                   elem.startTime == self.startTime)

    def get_invalid_constraints(self) -> ExprRef:
        return Not(self.isValid)

    def print_model_value(self, model: ModelRef, showLoc=False) -> Tuple:
        isVal = model.evaluate(self.isValid)
        src = model.evaluate(self.source)
        st = model.evaluate(self.startTime, model_completion=True)
        loc = model.evaluate(self.reqLoc)

        if model[self.isValid] is not None:
            if isVal:
                if showLoc:
                    return 'T', src, st, loc
                return 'T', src, st
            else:
                if showLoc:
                    return "F", '-', '-', '-'
                return "F", '-', '-'
        else:
            if showLoc:
                return '-', '-', '-', '-'
            return '-', '-', '-'


"""
SourceInput维护着每个时刻的输入数量，与之直连的队列的enqueue值由source决定
"""


class HNQueue:
    def __init__(self, solver: MySolver, queue_name: str, time_steps: int, queue_size: int, cached: bool = False,
                 credit_based: bool = False, lossless: bool = False, src: str = None):

        ctx = solver.ctx
        self.solver = solver
        self.src = self.solver.get_source_const(src)
        # 固定属性 (其值不依赖于其他变量，是确定的)
        self.cached = cached
        # self.credit_based = credit_based
        self.queue_name = queue_name
        self.time_steps = time_steps
        self.queue_size = queue_size

        # 非固定属性 (其值依赖于其他变量, 即相连的队列&调度算法, 或者cache)
        self.deq_cnt = []  # 各个时刻出队的数量
        self.val_cnt = []  # 各个时刻队列里valid的元素的数量
        self.cap_cnt = []  # 各个时刻队列的容量(即最多可以入队的数量)
        # self.enq_cnt = []
        for t in range(self.time_steps):
            name = queue_name + '_deq_cnt_at_time_' + str(t)
            self.deq_cnt.append(Int(name, ctx))
            name = queue_name + '_val_cnt_at_time_' + str(t)
            self.val_cnt.append(Int(name, ctx))
            name = queue_name + '_cap_cnt_at_time_' + str(t)
            self.cap_cnt.append(Int(name, ctx))
            # name = queue_name + '_enq_cnt_at_time_' + str(t)
            # self.enq_cnt.append(Int(name, ctx))

        # 初始化各个时刻的队列状态
        self.queue_states = {}
        for t in range(self.time_steps):
            queue_state = []
            for i in range(queue_size):
                name = queue_name + '_index_' + str(i) + '_time_' + str(t)
                queue_state.append(ReqElem(name=name, ctx=ctx, src_sort=self.solver.ReqSource))
            self.queue_states[t] = queue_state

        # 如果当前队列连接了cache，添加一个辅助队列用来保存cache hit状态
        if self.cached:
            self.hit = {
                t: [Bool(name=f'{queue_name}_hit_index_{i}_at_time_{t}', ctx=ctx) for i in range(queue_size)]
                for t in range(self.time_steps)
            }

        # 对于credit based flow control的额外设置
        if credit_based:  # credit-based flow control的队列必然有source
            assert self.src is not None
        self.lossless = lossless  # 是否允许丢包
        self.credit_based = credit_based
        if credit_based:  # credit-based control等于无损传输
            # 当前时刻的credit数量，当前时刻最多入队的数量小于等于当前时刻的credit
            self.credit_cnt = [Int(name=f'{src}_credit_cnt_at_time_{t}', ctx=ctx) for t in range(self.time_steps)]
            # 每个时刻的请求输入总数（可以是 Int 变量，支持约束建模）
            self.input_cnt = [Int(name=f"{src}_input_cnt_at_time_{t}", ctx=ctx) for t in range(time_steps)]

    def get_hit_cnt(self, t) -> ExprRef:
        assert self.cached
        return Sum(*[If(self.hit[t][i], 1, 0) for i in range(self.queue_size)])

    def get_deq_at_time_t(self, time_step: int) -> Int:
        return self.deq_cnt[time_step]

    # 这里的capacity指的是t时刻其他元素入队前的容量
    # t 时刻队列的容量等于:队列长度 - (t-1时刻的valid元素的数量 - t-1时刻dequeue的数量)
    def get_capacity_at_time(self, t) -> ExprRef:
        assert t > 0
        return self.queue_size - self.val_cnt[t - 1] + self.deq_cnt[t - 1]

    # 获得t时刻【即将】出队/cache命中的元素里，来自于src的数量
    # 这里要区分参数里的cache队列和非cache队列，能否补充credict: cache队列看hit的元素，非cache队列看deq的元素
    def get_replenishment(self, src: Const, t: int) -> ExprRef:
        if self.cached:
            return Sum(*[
                If(And(self.hit[t][i], self.queue_states[t][i].source == src), 1, 0)
                for i in range(self.queue_size)
            ])
        else:
            return Sum(*[
                If(And(i < self.deq_cnt[t], self.queue_states[t][i].source == src), 1, 0) for i in
                range(self.queue_size)
            ])

    """
     Logical topology: tail_queue -> src -> head_queue
     credit-based flow control：
     1. 根据credit replenishment的来源:更新credit值，credit值决定input值
     2. 对当前queue的元素操作：即当前source queue的fifo操作
        step 1: 把head queue里的剩余元素按照其deq数量平移
        step 2: 给head queue输入元素，输入数量由head queue的capacity和credit数量共同决定, 输入后相应的credit也要减少
        step 3: 除了remain和input的元素，剩余的valid置为false
    """

    def add_credit_flow_control_constraints(self, *dst_queues: HNQueue):
        assert self.credit_based

        for t in range(self.time_steps):
            remain = self.queue_size - self.cap_cnt[t]
            for i in range(self.queue_size):
                # step 1: 平移deq数量的元素
                if t > 0:
                    for deq_var in range(self.queue_size + 1):
                        if i + deq_var < self.queue_size:
                            name = f"cons_for_{self.queue_name}_flow_control_1_deq_{deq_var}_index_{i}_at_time_{t}"
                            cons = Implies(
                                And(i < remain, deq_var == self.deq_cnt[t - 1]),
                                self.queue_states[t][i].get_eq_constraints(self.queue_states[t - 1][i + deq_var])
                            )
                            self.solver.add_expr(name, cons)

                # step 2: 根据input值设置入队元素的valid值，但是请求的地址值不做约束
                # for remain_var in range(self.queue_size + 1):
                name = f"cons_for_{self.queue_name}_flow_control_2_index_{i}_at_time_{t}"
                cons = Implies(
                    And(remain <= i, i < remain + self.input_cnt[t]),
                    And(self.queue_states[t][i].isValid,
                        self.queue_states[t][i].source == self.src,
                        self.queue_states[t][i].startTime == t * self.queue_size + i
                        )
                )
                self.solver.add_expr(name, cons)

                # step 3: 剩余元素
                name = f"cons_for_{self.queue_name}_flow_control_3_index_{i}_at_time_{t}"
                cons = Implies(And(remain + self.input_cnt[t] <= i, i < self.queue_size),
                               self.queue_states[t][i].get_invalid_constraints())
                self.solver.add_expr(name, cons)

        # 添加其他时刻的credit值及其约束
        for t in range(self.time_steps - 1):
            credit_replenish_sum = Sum(*[q.get_replenishment(self.src, t) for q in dst_queues])
            name = f'cons_{self.src}_credit_upt_at_time_{t}'
            cons = self.credit_cnt[t + 1] == self.credit_cnt[t] - self.input_cnt[t] + credit_replenish_sum
            self.solver.add_expr(name, cons)

    """
    添加当前队列自身变量间的固定约束:
    We use two auxiliary variables q_remain_cnt(1:T) and q_val_cnt(1:T) 
    to track how many elements persist in a queue q across adjacent time steps, 
    i.e., not dequeued between t-1 and t. For example, for the queue q1:
        q1_remain_cnt(t) == q1_val_cnt(t-1) – q1_deq_cnt(t)
        q1_val_cnt(t-1) == Sum([If(q1(t-1)[i], 1, 0) for i in m)
    """

    def add_self_common_constraints(self):
        # 公共约束：主要是一些count值范围的设置
        self.solver.add_expr(f'cons_{self.queue_name}_deq_cnt_range', And(*[And(self.deq_cnt[t] >= 0,
                                                                                self.deq_cnt[t] <= self.queue_size)
                                                                            for t in range(self.time_steps)]))
        self.solver.add_expr(f'cons_{self.queue_name}_cap_cnt_range', And(*[And(self.cap_cnt[t] >= 0,
                                                                                self.cap_cnt[t] <= self.queue_size)
                                                                            for t in range(self.time_steps)]))
        self.solver.add_expr(f'cons_{self.queue_name}_valid_cnt_range', And(*[And(self.val_cnt[t] >= 0,
                                                                                  self.val_cnt[t] <= self.queue_size)
                                                                              for t in range(self.time_steps)]))
        self.solver.add_expr(f'cons_{self.queue_name}_deq_must_less_valid_cnt', And(*[self.val_cnt[t] >= self.deq_cnt[t]
                                                                                      for t in range(self.time_steps)
                                                                                      ]))
        # t 时刻队列的容量(未入队时）等于: 队列长度 - (t-1时刻的valid元素的数量 - t-1时刻dequeue的数量)
        self.solver.add_expr(f"cons_{self.queue_name}_cap_equation", And(*[self.cap_cnt[t] == self.queue_size - (self.val_cnt[t - 1] - self.deq_cnt[t - 1])
                                                                           for t in range(1, self.time_steps)]))
        for t in range(self.time_steps):
            name = f"cons_{self.queue_name}_valid_cnt_at_time_{t}"
            cons = self.val_cnt[t] == Sum(*[If(self.queue_states[t][i].isValid, 1, 0) for i in range(self.queue_size)])
            self.solver.add_expr(name, cons)

        # 对于队列元素状态的初始化约束
        # credit based flow control 的节点设置credit和input值约束
        if self.credit_based:
            assert self.src is not None
            # 初始化时刻0的credit和deq值，以及input值的range
            name = f'cons_init_source_{self.src}'
            cons = And(
                self.credit_cnt[0] == self.queue_size,
                self.cap_cnt[0] == self.queue_size,
                *[And(self.input_cnt[t] >= 0,
                      self.credit_cnt[t] >= 0,
                      self.input_cnt[t] <= self.credit_cnt[t])
                  for t in range(self.time_steps)]
            )
            self.solver.add_expr(name, cons)

        # 非起点设置初始空状态
        if self.src is None:
            # 非src队列初始状态都为全空
            init_queue_state = self.queue_states[0]
            name = f'cons_init_non_source_queue_{self.queue_name}'
            common_cons = And(
                self.deq_cnt[0] == 0,
                self.val_cnt[0] == 0,
                self.cap_cnt[0] == self.queue_size,
                *[Not(init_queue_state[i].isValid) for i in range(self.queue_size)]
            )
            if self.cached:
                cache_hit = self.hit[0]
                self.solver.add_expr(name, And(common_cons, And(*[Not(cache_hit[i]) for i in range(self.queue_size)])))
            else:
                self.solver.add_expr(name, common_cons)

    # 末端队列的出队约束
    # 手动：指定max or min dequeue number # TODO:待实现
    # 自动：当前队列里所有valid元素出队
    # TODO: 之后可以拓展添加一些target node处理时延的约束
    def add_self_dequeue_constraints(self, fixed_deq=0):
        for t in range(self.time_steps):
            if fixed_deq > 0:
                cons = If(self.val_cnt[t] > 0, self.deq_cnt[t] == 1, self.deq_cnt[0] == 0)
            else:
                # 没指定deq值，每次全部deq
                cons = self.deq_cnt[t] == self.val_cnt[t]
            self.solver.add_expr(f'cons_{self.queue_name}_self_deq_cnt_at_time_{t}', cons)

    # 获得所有时刻的deq值
    def print_deq_cnt_value(self) -> []:
        assert self.solver.model
        return [self.solver.model.evaluate(self.deq_cnt[t]) for t in range(self.time_steps)]

    # 获得所有时刻的valid值
    def print_val_cnt_value(self) -> []:
        assert self.solver.model
        return [self.solver.model.evaluate(self.val_cnt[t]) for t in range(self.time_steps)]

    # 获得所有时刻的capacity值
    def print_cap_cnt_value(self) -> []:
        assert self.solver.model
        return [self.solver.model.evaluate(self.cap_cnt[t]) for t in range(self.time_steps)]

    # 获得所有时刻的credit值
    def print_credit_cnt_value(self) -> []:
        assert self.solver.model
        if hasattr(self, 'credit_cnt'):
            return [self.solver.model.evaluate(self.credit_cnt[t]) for t in range(self.time_steps)]
        else:
            return ['-' for t in range(self.time_steps)]

    # 获得所有时刻的input值
    def print_input_cnt_value(self) -> []:
        assert self.solver.model
        if hasattr(self, 'input_cnt'):
            return [self.solver.model.evaluate(self.input_cnt[t]) for t in range(self.time_steps)]
        else:
            return ['-' for t in range(self.time_steps)]

    def print_queue_state(self, showLoc=False) -> {}:
        assert self.solver.model
        q_states = {
            t: [self.queue_states[t][i].print_model_value(self.solver.model, showLoc) for i in range(self.queue_size)]
            for t in range(self.time_steps)
        }
        return q_states

    # 测试的时候才调用
    def set_init_state_test(self):
        src = self.src if self.src is not None else self.solver.get_source_const(CPU)
        cons = And(
            self.cap_cnt[0] == self.queue_size,
            *[And(self.queue_states[0][i].isValid,
                self.queue_states[0][i].startTime == i,
                self.queue_states[0][i].source == src) for i in range(self.queue_size)
            ])
        self.solver.add_expr(f'test_init_state_for_{self.queue_name}', cons)
