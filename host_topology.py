from my_solver import CPU, IIO
from queue_model import HNQueue
from queue_scheduling import *
from cache_model import HNCache

from tabulate import tabulate

from tabulate import tabulate


# TODO: 支持多级cache
class HostNetwork:
    def __init__(self, queues, cache, solver):
        assert isinstance(queues, dict)
        assert isinstance(cache, HNCache)

        self.queues = queues
        self.cache = cache
        self.solver = solver
        self.time_length = max(*[q.queue_size for q in self.queues.values()], self.cache.cache_size)

    def initialize(self):
        # 初始化队列
        for q in self.queues.values():
            assert isinstance(q, HNQueue)
            q.add_self_common_constraints()
            q.set_time_length(self.time_length)
        # 初始化cache
        self.cache.add_init_constraints()
        self.cache.set_time_length(self.time_length)


    # 把queues里的各个queue的各个时刻的状态都打印出来
    def prinf_trace(self, show_loc=True):
        if not self.solver.model:
            return
        time_steps = self.queues[0].time_steps

        # 打印队列的cnt状态
        if self.queues is not None and len(self.queues) > 0:
            # 把shadow的队列也打印出来
            for q in self.queues:
                if q.cached:
                    self.queues.append(q.shadow_queue)

            # 首先打印所有cnt值
            self.queues_cnt_map = {
                f'{q.queue_name} ({q.queue_size})': [
                    q.print_cap_cnt_value(),
                    q.print_val_cnt_value(),
                    q.print_deq_cnt_value(),
                    q.print_credit_cnt_value(),
                    q.print_input_cnt_value()
                ]
                for q in self.queues
            }
            headers = ['Queue'] + [f'T{t} (c, v, d, cr, i)' for t in range(time_steps)]
            cnt_rows = []
            for q_name, q_cnts in self.queues_cnt_map.items():
                cnt_row = [q_name]
                for t in range(time_steps):
                    cell = (q_cnts[0][t], q_cnts[1][t], q_cnts[2][t], q_cnts[3][t], q_cnts[4][t])
                    cnt_row.append(cell)
                cnt_rows.append(cnt_row)
            print(tabulate(cnt_rows, headers=headers, tablefmt='grid'))

            # 打印各个队列的所有时刻状态
            print()
            print("=" * 40 + ' QUEUE STATE ' + "=" * 40)
            print()
            for q in self.queues:
                # 每个队列打印一张
                q_state = q.print_queue_state(show_loc)
                headers = [q.queue_name] + [f'T{i} (src, t, loc, hit)' for i in range(time_steps)]
                state_rows = []
                for i in range(q.queue_size):
                    state_row = [f'[{i}]'] + [q_state[t][i] for t in range(time_steps)]
                    state_rows.append(state_row)
                print(tabulate(state_rows, headers=headers, tablefmt='grid'))

        if self.cache is not None:
            c = self.cache
            # 每个队列打印一张状态表：包括地址和替换状态
            c_state = c.print_cache_state(True)
            headers = [c.cache_name] + [f'T{i} (loc, acc, hits, rep)' for i in range(time_steps)]
            state_rows = []
            for i in range(c.cache_size):
                state_row = [f'[{i}]'] + [c_state[t][i] for t in range(time_steps)]
                state_rows.append(state_row)
            print(tabulate(state_rows, headers=headers, tablefmt='grid'))
