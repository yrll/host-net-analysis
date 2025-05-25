"""
queue model是连接队列的组件 (参考 FPerf)
每个 queue model 可以有 n 个 input queues，和 m 个 output queues
可以通过不同的调度算法实现 n input queues --> m output queues 的 transition
"""
from enum import Enum

from z3 import Solver, Int, Context, Bool

import data_request
from data_request import DataRequest
from util import concat_name


class ScheduleAlgo(Enum):
    FIFO = "fifo"
    RoundRobin = "round-robin"

"""Host network queue"""
class HNQueue:
    def __init__(self, ctx: Context, queue_name: str, time_slot: int, queue_size: int, max_enqueue_size: int, max_dequeue_size: int):
        self.queue_name = queue_name
        self.time_slot = time_slot
        self.queue_size = queue_size
        self.max_enqueue_size = max_enqueue_size
        self.max_dequeue_size = max_dequeue_size

        # 当前时刻 t 下，在队列里的requests,
        self.inqueue_vec = []
        self.inqueue_valid_vec = []
        for i in queue_size:
            req_name = concat_name(queue_name, i, time_slot)
            self.inqueue_vec.append(DataRequest(name=req_name, ctx=ctx))
            self.inqueue_valid_vec.append(Bool(name=concat_name(req_name, "valid"), ctx=ctx))

        # 当前时刻 t 下，即将入队列的requests (即在t+1时刻会进入队列)
        self.inqueue_vec = []
        self.inqueue_valid_vec = []
        for i in queue_size:
            req_name = concat_name(queue_name, i, time_slot)
            self.inqueue_vec.append(DataRequest(name=req_name, ctx=ctx))
            self.inqueue_valid_vec.append(Bool(name=concat_name(req_name, "valid"), ctx=ctx))
        self.enqueue_vec = [data_request] * max_enqueue_size

    # TODO: 添加入队的约束
    def enqueue(self, enqueue_numver: int):
        return

class QueueModel:
    def __init__(self, solver: Solver, ScheduleAlgo: ScheduleAlgo = ScheduleAlgo.FIFO):
        self.queue = []
        a = Int("x");