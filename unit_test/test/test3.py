from dataclasses import dataclass,field
from typing import List

@dataclass
class User:
    name:str
    age:int
    tags:List[str] = field(default_factory=list)

user = User(name="wangsg",age=18,tags=["subject","phyth"])
user2 = User(name="wangsg2",age=16)
print(user)
print(user2)

# config_dict = {"name":"wangsg","age":19,"gender":"男"}

# import json

# with open("config_user.json",'w',encoding="utf-8") as f:
#     json.dump(config_dict,f,ensure_ascii=False,indent=2)

# with open("config_user.json","r",encoding="utf-8") as f:
#     data = json.load(f)
# print(data)

# import asyncio
# import time

# async def task(name: str, delay: int):
#     print(f"任务 {name} 开始，等待 {delay}s")
#     await asyncio.sleep(delay)  # 模拟 I/O 阻塞
#     print(f"任务 {name} 完成")
#     return f"{name} 结果"

# async def main():
#     # 并发执行多个任务（总耗时约 2s，而非 3s）
#     results = await asyncio.gather(
#         task("A", 2),
#         task("B", 1),
#         task("C", 1.5)
#     )
#     print(f"所有结果: {results}")

# 启动入口（脚本必须用此方法运行）
# asyncio.run(main())

# import os
# from pathlib import Path
# import logging
# from datetime import datetime


# class Dog:
#     species = "犬科"

#     def __init__(self, name):
#         self.name = name

# d1 = Dog("旺财")
# d2 = Dog("小白")
# d1.species = "猫科"
# print(d1.species, d2.species)

# from pathlib import Path
# p = Path("/data/report.csv")

# print(p.suffix)

# from datetime import date
# d1 = date(2024, 1, 1)
# d2 = date(2024, 3, 1)

# print(d2-d1)
# print((d2-d1).days)

# from dataclasses import dataclass, field

# @dataclass
# class Config:
#     items: list = field(default_factory=list)

# c1 = Config()
# c2 = Config()
# c1.items.append("a")
# print(c1.items, c2.items)

# import asyncio

# async def main():
#     await asyncio.sleep(0.1)
#     return 42

# result = asyncio.run(main())
# print(result)

# print(Path("a/b/c").parent.name)

# from datetime import datetime

# dt1 = datetime(2024, 1, 1, 8, 0, 0)
# dt2 = datetime(2024, 1, 3, 14, 30, 0)
# delta = dt2 - dt1
# print(delta.days, delta,delta.seconds,delta.seconds // 3600)

# class Temperature:
#     def __init__(self, celsius=0):
#         self._celsius = celsius

#     @property
#     def fahrenheit(self):
#         return self._celsius * 9 / 5 + 32

#     @fahrenheit.setter
#     def fahrenheit(self, value):
#         self._celsius = (value - 32) * 5 / 9

# t = Temperature(100)
# print(t.fahrenheit)
# t.fahrenheit = 32
# print(t._celsius)

# from datetime import datetime, timedelta

# now = datetime(2024, 6, 15, 14, 30, 0)
# result = now.replace(hour=0, minute=0, second=0) + timedelta(days=1)
# print(result)

# 使用 `dataclass` 定义一个简单的数学表达式树：
# - `Number(value: float)` 表示数字
# - `BinaryOp(op: str, left, right)` 表示二元运算（`+`、`-`、`*`、`/`）
# - 实现函数 `evaluate(expr)` 递归计算表达式的值
# - 实现函数 `to_string(expr)` 将表达式转为可读字符串

from dataclasses import dataclass
from typing import Union

@dataclass
class Number:
    value:float

@dataclass
class BinaryOp:
    op:str
    left:Union[Number,'BinaryOp']
    right:Union[Number,'BinaryOp']

def evaluate(expr):
    if isinstance(expr,Number):
        return float(expr.value)
    elif isinstance(expr,BinaryOp):
        l = evaluate(expr.left)
        r = evaluate(expr.right)

        try:
            if expr.op == "+":
                return l + r
            elif expr.op == "-":
                return l - r
            elif expr.op == "*":
                return l * r
            elif expr.op == "/":
                return l / r
            else:
                raise ValueError(f"Unknown operator: {expr.op}")
        except Exception as e:
            raise ValueError(f"Unknown operator: {e}")
        
def to_string(expr):
    if isinstance(expr,Number):
        return str(float(expr.value))
    elif isinstance(expr,BinaryOp):
        l = to_string(expr.left)
        r = to_string(expr.right)
        return f"({l} {expr.op} {r})"


# 示例：表示 (3 + 5) * 2
expr = BinaryOp("*", BinaryOp("+", Number(3), Number(5)), Number(2))
print(evaluate(expr))    # 16.0
print(to_string(expr))   # "((3.0 + 5.0) * 2.0)"


import asyncio
import time

async def say_after(delay, word):
    print(f"开始等待 {delay}s...")
    await asyncio.sleep(delay)  # 模拟 I/O，如网络请求
    print(word)
    return f"完成: {word}"

# 方式1：直接运行协程（必须用 asyncio.run）
async def main():
    # 注意：如果直接 await 调用，它们是串行执行的
    start = time.perf_counter()

    # await say_after(2, "Hello")
    # await say_after(1, "World")
    # 总耗时：2 + 1 = 3秒

    # 并行执行
    tasks = [
       say_after(2, "Hello"),
       say_after(1, "Hello")
    ]
    await asyncio.gather(*tasks)
    diff = time.perf_counter() - start
    print(f"耗时{diff}")

asyncio.run(main())




