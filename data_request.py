"""
每个Data request由CPU/RNIC发出，一个cache line大小的读/写请求
TODO: 区分读写请求
"""
from enum import Enum

from z3 import Context, BoolVal, Bool

from util import concat_name


class RequestType(Enum):
    READ = 0
    WRITE = 1

class RequestSource(Enum):
    CPU = "cpu"
    RNIC = "rnic"

class DataRequest:
    def __init__(self, name: str, ctx: Context):
        self.name = name
        self.ctx = ctx
        self.req_type = Bool(concat_name(name, "type"), ctx=ctx)
        # self.req_source = req_source
