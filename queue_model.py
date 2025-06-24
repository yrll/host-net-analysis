"""
queue model是连接队列的组件 (参考 FPerf)
每个 queue model 可以有 n 个 input queues，和 m 个 output queues
可以通过不同的调度算法实现 n input queues --> m output queues 的 transition
"""

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
from z3 import *

ctx = Context()
solver = Solver(ctx=ctx)
# 定义一个枚举类型 Status，有三个状态 [如果cpu或者iio设备不止一个，也要继续补充这个enumeration]
ReqSource, (cpu, iio) = EnumSort('ReqSource', ['cpu', 'iio'], ctx=ctx)


class RequestType(Enum):
    READ = 0
    WRITE = 1


class ScheduleAlgo(Enum):
    FIFO = "fifo"
    RoundRobin = "round-robin"


class QueueElem:
    def __init__(self, name: str, ctx: Context, start_time: int):

        self.isValid = Bool(name + '_val', ctx)
        self.source = Const(name + '_src', ReqSource)
        self.reqLoc = Int(name + '_loc', ctx)
        self.startTime = Int(name + '_time', ctx)

    def add_eq_constraints(self, elem: 'QueueElem') -> ExprRef:
        return And(elem.isValid == self.isValid,
                   elem.source == self.source,
                   elem.reqLoc == self.reqLoc,
                   elem.startTime == self.startTime)

    def add_invalid_constraints(self) -> ExprRef:
        return Not(self.isValid)


class HNQueue:
    def __init__(self, ctx: Context, queue_name: str, time_steps: int, queue_size: int,
                 cached: bool = False):
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
                queue_state.append(QueueElem(name=name, ctx=ctx, start_time=t))
            self.queue_states[t] = queue_state

        # 如果当前队列连接了cache，添加一个辅助队列用来保存cache hit状态
        if self.cached:
            self.hit = {}
            for t in range(self.time_steps):
                self.hit[t] = [Bool(name=f'{queue_name}_hit_index_{i}_at_time_{t}', ctx=ctx) for i in range(queue_size)]

        # 如果当前队列是credit-based flow control
        # if self.credit_based:
        #     self.credit = [Int(name=f'{queue_name}_credit_at_time_{t}', ctx=ctx) for t in range(self.time_steps)]

        # # 如果当前队列连接了cache，添加一个辅助队列用来保存经过cache后的队列状态（主要作用是去掉hole）
        # # TODO: 经过cache算作一个时刻么？如果不算，那么cache命中的request的实际返回时刻一定早于最后一个队列的出队时刻，但是当前建模中未体现
        # self.raw_queue_states = {}
        # if hasCache:
        #     for t in range(self.time_steps):
        #         raw_queue_state = []
        #         for i in range(queue_size):
        #             name = 'raw_' + queue_name + '_index_' + str(i) + '_time_' + str(t)
        #             raw_queue_state.append(QueueElem(name=name, ctx=ctx, start_time=t))
        #         self.raw_queue_states[t] = raw_queue_state

    def get_hit_cnt(self, t):
        assert self.cached
        return Sum(*[If(self.hit[t][i], 1, 0) for i in range(self.queue_size)])

    def get_deq_at_time_t(self, time_step: int) -> Int:
        return self.deq_cnt[time_step]

    def init_time_zero(self) -> dict[str, ExprRef]:
        exprs = {}
        init_queue_state = self.queue_states[0]
        name = f'init_{self.queue_name}'
        common_cons = And(
                            *[Not(init_queue_state[i].isValid) for i in range(self.queue_size)],
                            self.cap_cnt[0] == self.queue_size,
                            self.val_cnt[0] == 0,
                        )
        if self.cached:
            cache_hit = self.hit[0]
            exprs[name] = And(common_cons, And(*[Not(cache_hit[i]) for i in range(self.queue_size)]))
        else:
            exprs[name] = common_cons
        #
        return exprs



    """
    添加当前队列自身变量间的固定约束:
    We use two auxiliary variables q_remain_cnt(1:T) and q_val_cnt(1:T) 
    to track how many elements persist in a queue q across adjacent time steps, 
    i.e., not dequeued between t-1 and t. For example, for the queue q1:
        q1_remain_cnt(t) == q1_val_cnt(t-1) – q1_deq_cnt(t)
        q1_val_cnt(t-1) == Sum([If(q1(t-1)[i], 1, 0) for i in m)
    """

    def add_self_constraints(self) -> dict[str, ExprRef]:
        constraints = {}
        # 公共约束：任意时刻的_*_cnt值都必须大于等于零
        constraints[f'cons_{self.queue_name}_all_deq_cnt_ge_0'] = And(*[And(self.deq_cnt[t] >= 0)
                                                                        for t in range(self.time_steps)])

        constraints[f'cons_{self.queue_name}_all_valid_cnt_ge_0'] = And(*[And(self.val_cnt[t] >= 0)
                                                                          for t in range(self.time_steps)])

        constraints[f'cons_{self.queue_name}_all_capacity_cnt_ge_0'] = And(*[And(self.cap_cnt[t] >= 0)
                                                                             for t in range(self.time_steps)])

        # constraints[f'cons_{self.queue_name}_all_deq_cnt_ge_0'] = And(*[And(self.deq_cnt[t] >= 0,
        #                                                                     self.deq_cnt[t] <= self.queue_size)
        #                                                                 for t in range(self.time_steps)])
        # #
        constraints[f'cons_{self.queue_name}_all_valid_cnt_ge_0'] = And(*[And(self.val_cnt[t] >= 0,
                                                                              self.val_cnt[t] <= self.queue_size)
                                                                          for t in range(self.time_steps)])

        constraints[f'cons_{self.queue_name}_all_capacity_cnt_ge_0'] = And(*[And(self.cap_cnt[t] >= 0,
                                                                                 self.cap_cnt[t] <= self.queue_size)
                                                                             for t in range(self.time_steps)])
        constraints[f'cons_{self.queue_name}_deq_must_less_valid_cnt'] = And(*[
            self.val_cnt[t] >= self.deq_cnt[t] for t in range(self.time_steps)
        ])
        for t in range(1, self.time_steps):
            # t 时刻队列的容量等于
            # non-credit-based control: 队列长度 - (t-1时刻的valid元素的数量 - t-1时刻dequeue的数量)
            # credit-based control: credit数量
            name = f"cons_{self.queue_name}_capacity_cnt_at_time_{t}"
            # cons = self.cap_cnt[t] == If(self.credit_based,
            #                              self.credit[t],
            #                              self.queue_size - (self.val_cnt[t - 1] - self.deq_cnt[t - 1]))
            cons = self.cap_cnt[t] == self.queue_size - (self.val_cnt[t - 1] - self.deq_cnt[t - 1])
            constraints[name] = cons

            name = f"cons_{self.queue_name}_valid_cnt_at_time_{t}"
            cons = self.val_cnt[t] == Sum(*[If(self.queue_states[t][i].isValid, 1, 0) for i in range(self.queue_size)])
            constraints[name] = cons

        return constraints


class TargetNode:
    def __init__(self, dst: str, target_queue: HNQueue):
        self.dst = dst
        self.target_queue = target_queue

    # 末端队列的出队约束
    # 手动：指定max or min dequeue number # TODO:待实现
    # 自动：当前队列里所有valid元素出队
    def add_self_dequeue_constraints(self) -> dict[str, ExprRef]:
        exprs = {}
        for t in range(self.target_queue.time_steps):
            cons = self.target_queue.deq_cnt[t] == self.target_queue.val_cnt[t]
            exprs[f'cons_{self.target_queue.queue_name}_self_deq_cnt_at_time_{t}'] = cons
        return exprs

    # TODO: 之后可以拓展添加一些target node处理时延的约束


"""
SourceInput维护着每个时刻的输入数量，与之直连的队列的enqueue值由source决定
"""


class SourceInput:
    def __init__(self, src: ReqSource, ctx: Context, time_steps: int,
                 credit_based: bool = True, lossless: bool = False):

        self.src = src  # 来源名称，如 ''
        self.ctx = ctx  # z3 上下文
        # self.max_input = max_input  # 每个时刻最多可发送的请求数量
        self.time_steps = time_steps  # 时间步总数
        self.lossless = lossless  # 是否允许丢包
        self.credit_based = credit_based
        if credit_based:  # credit-based control等于无损传输
            # 当前时刻的credit数量，当前时刻最多入队的数量小于等于当前时刻的credit
            self.credit_cnt = [Int(name=f'{src}_credit_cnt_at_time_{t}', ctx=ctx) for t in range(self.time_steps)]

        # self.input_states = {}
        # # 初始化各个时刻的队列状态
        # for t in range(self.time_steps):
        #     enqueue_state = []
        #     for i in range(max_enq):
        #         name = src + '_input_' + str(i) + '_time_' + str(t)
        #         enqueue_state.append(QueueElem(name=name, ctx=ctx, start_time=t))
        #     self.input_states[t] = enqueue_state

        # 每个时刻的请求输入总数（可以是 Int 变量，支持约束建模）
        self.input_cnt = [Int(f"input_cnt_{src}_at_time_{t}", ctx) for t in range(time_steps)]

    """
     Logical topology: tail_queue -> src -> head_queue
     credit-based flow control: 
     1. 末端队列(tail queue)的dequeue数量影响发送端(src_input)的credit值, credit值进而决定head的入队值
     2. 中间队列(med queue)的缓存命中数量影响发送端(src_input)的credit值
        step 1: 把head queue里的剩余元素按照其deq数量平移
        step 2: 给head queue输入元素，输入数量由head queue的capacity和credit数量共同决定, 输入后相应的credit也要减少
        ---------前两步类似于head queue的fifo操作------------
        step 3: 根据tail queue的出队元素，更新src的credit
    """

    def add_credit_flow_control_constraints(self, head_queue: HNQueue, tail_queue: HNQueue, *mid_queues: HNQueue) -> dict[str, ExprRef]:
        assert self.credit_based
        exprs = {}
        # 初始化时刻0的credit值
        exprs[f'cons_init_source_{self.src}'] = And(self.credit_cnt[0] == head_queue.queue_size, self.input_cnt[0] == 0)
        # 初始化：所有时刻的input和credit值都必须大于等于0
        exprs[f'cons_{self.src}_all_input_ge_0'] = And(*[self.input_cnt[t] >= 0 for t in range(self.time_steps)])
        exprs[f'cons_{self.src}_all_credit_ge_0'] = And(*[self.credit_cnt[t] >= 0 for t in range(self.time_steps)])

        # 添加其他时刻的credit值及其约束
        for t in range(1, self.time_steps):
            head_queue_deq_cnt_t_1 = head_queue.deq_cnt[t - 1]
            head_queue_remain = head_queue.queue_size - head_queue.cap_cnt[t]
            head_queue_state = head_queue.queue_states[t]
            head_queue_state_t_1 = head_queue.queue_states[t - 1]

            for remain_var in range(0, head_queue.queue_size + 1):
                # step 1: 根据上一时刻dequeue数量平移剩余元素
                for deq_var in range(0, head_queue.queue_size + 1):
                    if remain_var + deq_var > head_queue.queue_size:  # 不可能
                        continue
                    if remain_var > 0:
                        name = f'cons_{head_queue.queue_name}_deq_{deq_var}_remain_{remain_var}_at_time_{t}'
                        cons = Implies(And(head_queue_deq_cnt_t_1 == deq_var, head_queue_remain == remain_var),
                                       And(
                                           *[head_queue_state[i].add_eq_constraints(head_queue_state_t_1[i + deq_var])
                                             for i in range(remain_var)]
                                       )
                                       )
                        exprs[name] = cons
                # step 2: 根据当前时刻credit数量决定enqueue元素
                input_cnt = self.input_cnt[t]
                credit_cnt = self.credit_cnt[t]
                for input_var in range(0, head_queue.queue_size + 1):
                    if input_var + remain_var > head_queue.queue_size:
                        continue
                    # # -------------debug-----------------
                    # print("input_cnt.ctx:", input_cnt.ctx)
                    # print("head_queue_remain.ctx:", head_queue_remain.ctx)
                    # print("credit_cnt.ctx:", credit_cnt.ctx)
                    #
                    # for i in range(remain_var, remain_var + input_var):
                    #     print(f"head_queue_state[{i}].isValid.ctx:", head_queue_state[i].isValid.ctx)
                    #     print(f"head_queue_state[{i}].source.ctx:", head_queue_state[i].source.ctx)
                    #     print(f"head_queue_state[{i}].startTime.ctx:", head_queue_state[i].startTime.ctx)

                    if input_var > 0:  # Implies 的第二个入参不能为空，否则报错ctx mismatch
                        name = f'cons_{head_queue.queue_name}_input_{input_var}_remain_{remain_var}_at_time_{t}'
                        cons = Implies(
                            And(input_var == input_cnt, head_queue_remain == remain_var, input_var <= credit_cnt),
                            And(
                                *[And(head_queue_state[i].isValid,
                                      head_queue_state[i].source == self.src,
                                      head_queue_state[i].startTime == t)
                                  for i in range(remain_var, remain_var + input_var)]
                            )
                        )
                        exprs[name] = cons

                    if remain_var + input_var < head_queue.queue_size:
                        name = f'cons_{head_queue.queue_name}_ending_at_time_{t}'
                        cons = Implies(And(input_var == input_cnt, head_queue_remain == remain_var),
                                       And(
                                           *[Not(head_queue_state[i].isValid)
                                             for i in range(remain_var + input_var, head_queue.queue_size)]
                                       ))
                        exprs[name] = cons

            tail_queue_deq_cnt_t_1 = tail_queue.deq_cnt[t - 1]
            tail_queue_state_t_1 = tail_queue.queue_states[t - 1]
            # step 3:
            name = f'cons_{self.src}_credit_upt_at_time_{t}'
            cons = self.credit_cnt[t] == self.credit_cnt[t - 1] - self.input_cnt[t - 1] + \
                   Sum(
                       *[If(
                           And(
                               i + 1 <= tail_queue_deq_cnt_t_1,
                               tail_queue_state_t_1[i].isValid,
                               tail_queue_state_t_1[i].source == self.src), 1, 0
                       )
                           for i in range(tail_queue.queue_size)]
                   ) + \
                   Sum(
                       *[q.get_hit_cnt(t - 1) for q in mid_queues]
                   )
            exprs[name] = cons

        return exprs
