from z3 import ExprRef, Solver


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


def make_counter():
    count = 0

    def counter():
        nonlocal count
        count += 1
        return count

    return counter


def get_name(*args):
    if args is None or args.count() == 0:
        return "unkown_" + str(make_counter())
    else:
        name = ""
        for n in args:
            name = name + '_' + n
        return name



