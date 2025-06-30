from z3 import ExprRef, Solver

# A fixed host network topology
import json

from z3 import *
from z3.z3util import get_vars

from tabulate import tabulate

from tabulate import tabulate


def count_occurrences(int_list, target) -> ExprRef:
    # 创建 z3 Int 变量列表，分别代表每个元素是否等于 target（1表示相等，0表示不等）
    is_equal = [If(x == target, 1, 0) for x in int_list]
    # 求和即为出现次数
    return Sum(is_equal)


# nonlocal current_cons_name_map

def concat_name(*args, separator: str = "_") -> str:
    """
    将不定数量的任意类型参数转换为字符串后，用指定分隔符连接, 全部以大写返回。

    Args:
        *args: 不定数量的任意类型参数。
        separator: 分隔符，默认为 "_"。

    Returns:
        连接后的字符串。如果无参数，返回空字符串。
    """
    # 将所有参数转换为字符串
    str_args = [str(arg) for arg in args]
    # 使用 join 连接
    return separator.join(str_args).upper()





# def get_name(*args):
#     if args is None or args.count() == 0:
#         return "unkown_" + str(make_counter())
#     else:
#         name = ""
#         for n in args:
#             name = name + '_' + n
#         return name


def concat_tuple_or_str(*args):
    res = ()
    for arg in args:
        if isinstance(arg, tuple):
            res = res + arg
        else:
            # if arg is True:
            #     arg = 'T'
            # else:
            #     arg = 'F'
            res = res + (arg,)
    return res


import json
import re


def load_model_json(model_path: str) -> dict:
    with open(model_path, 'r') as f:
        model = json.load(f)
    return model


def replace_vars_in_smt2(smt2_path: str, model_dict: dict, output_path: str, non_replace_var_list=[]):
    with open(smt2_path, 'r') as f:
        content = f.read()

    # 按变量长度排序，优先替换长变量名，避免子串污染
    for var in sorted(model_dict.keys(), key=len, reverse=True):
        if var not in non_replace_var_list:
            val = model_dict[var]
            # 避免替换变量名子串，使用正则 word boundary
            pattern = r'\b' + re.escape(var) + r'\b'
            content = re.sub(pattern, val, content)

    with open(output_path, 'w') as f:
        f.write(content)


# # 示例用法
# smt_file = "smt.smt2"  # 输入SMT文件路径
# model_file = "smt_model"  # Model文件路径
# output_file = "output.smt"  # 输出文件路径
#
# non_replace_list = ["cha_index_0_time_4_val"]
#
# model_dict = load_model_json(model_file)
# replace_vars_in_smt2(smt_file, model_dict, output_file, non_replace_list)
# print(f"Replaced SMT2 saved to {output_file}")
