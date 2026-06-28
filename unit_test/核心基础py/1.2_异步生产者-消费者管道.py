### 题目 3：异步生产者-消费者管道 ***

# 使用 `asyncio.Queue` 实现一个多阶段数据处理管道：

# - 阶段 1（生产者）：从数据列表逐个产出数据到 Queue1
# - 阶段 2（处理器）：从 Queue1 取数据，应用转换函数，结果放入 Queue2
# - 阶段 3（收集器）：从 Queue2 取数据，收集到结果列表
# - 编写异步函数 `pipeline(data, transform_func)` 组装管道

import asyncio

async def pipeline(data,transform_func):
    q1 = asyncio.Queue()
    q2 = asyncio.Queue()
    results = []
    async def produce():
        for d in data:
            await q1.put(d)
        await q1.put(None)

    async def process():
        while True:
            item =await q1.get()
            if item is None:
                await q2.put(None)
                break
            await q2.put(transform_func(item))

    async def collect():
        while True:
            item =await q2.get()
            if item is None:
                break
            results.append(item)

    await asyncio.gather(produce(),process(),collect())
    return results


# # 示例
data = [1, 2, 3, 4, 5]
results = asyncio.run(pipeline(data, lambda x: x ** 2))
print(results)  # [1, 4, 9, 16, 25]
