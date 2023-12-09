from operator import add, mul, sub, truediv
from itertools import permutations, combinations_with_replacement
from collections import defaultdict

def merge(x, y):
    return 10*x+y

def judgePoint24(nums, target) -> bool:
    ops = [add, mul, sub, truediv, merge]
    op_char = "+*-/@"
    record = []

    def solve(nums) -> bool:
        if not nums:
            return False
        if target in nums:
            record.append(([target, ''],
                              '', target))
            return True
        n = len(nums)
        if n == 1:
            return round(nums[0], 3) == target
        for i, j in permutations(range(n), 2):
            # 选2个数字
            x, y = nums[i], nums[j]
            newNums = []
            # 选择加减乘除 4 种运算操作之一，用得到的结果取代选出的 2 个数字
            # 先添加未选择的数字
            newNums = [z for k, z in enumerate(nums) if k not in (i, j)]
            for k in range(5):
                if k < 2 and i > j:
                    # 加法和乘法满足交换律,跳过第二种顺序
                    continue
                if k == 3 and (round(y, 3) == 0):
                    # 除法运算除数不能为0
                    continue
                v = ops[k](x, y)
                newNums.append(v)
                record.append(([round(x, 3), round(y, 3)],
                              op_char[k], round(v, 3)))
                if round(v, 3) == target:
                    return True
                if solve(newNums):
                    return True
                newNums.pop()
                record.pop()
        return False
    flag = solve(nums)
    if not flag:
        return False, ""
    cache = defaultdict(list)
    for ns, op, v in record:
        for i in range(2):
            if cache[ns[i]]:
                ns[i] = "("+cache[ns[i]].pop()+")"
        a, b = ns
        cache[v].append(f"{a}{op}{b}")
    return flag, cache[target][0]+"="+f'{target}'


judgePoint24([4,10000], 10000)
