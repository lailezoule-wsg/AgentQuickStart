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

config_dict = {"name":"wangsg","age":19,"gender":"男"}

import json

with open("config_user.json",'w',encoding="utf-8") as f:
    json.dump(config_dict,f,ensure_ascii=False,indent=2)

with open("config_user.json","r",encoding="utf-8") as f:
    data = json.load(f)
print(data)

import asyncio
import time

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

import os
from pathlib import Path
import logging
from datetime import datetime


class Dog:
    species = "犬科"

    def __init__(self, name):
        self.name = name

d1 = Dog("旺财")
d2 = Dog("小白")
d1.species = "猫科"
print(d1.species, d2.species)

from pathlib import Path
p = Path("/data/report.csv")

print(p.suffix)

from datetime import date
d1 = date(2024, 1, 1)
d2 = date(2024, 3, 1)

print(d2-d1)
print((d2-d1).days)

from dataclasses import dataclass, field

@dataclass
class Config:
    items: list = field(default_factory=list)

c1 = Config()
c2 = Config()
c1.items.append("a")
print(c1.items, c2.items)

import asyncio

async def main():
    await asyncio.sleep(0.1)
    return 42

result = asyncio.run(main())
print(result)

print(Path("a/b/c").parent.name)

from datetime import datetime

dt1 = datetime(2024, 1, 1, 8, 0, 0)
dt2 = datetime(2024, 1, 3, 14, 30, 0)
delta = dt2 - dt1
print(delta.days, delta,delta.seconds,delta.seconds // 3600)

