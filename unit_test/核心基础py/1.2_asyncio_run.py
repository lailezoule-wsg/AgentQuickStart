# 使用 `asyncio` 编写一个模拟 API 批量请求的异步程序：

# - 定义异步函数 `fetch_data(url, delay)`，模拟网络请求（用 `asyncio.sleep(delay)` 模拟），返回 `{"url": url, "status": 200}`
# - 编写异步函数 `batch_fetch(urls)`，并发请求所有 URL，返回所有结果
# - 编写异步函数 `batch_fetch_with_limit(urls, concurrency=3)`，限制最大并发数为 3
# - 使用 `asyncio.run()` 运行

import asyncio
from datetime import datetime

# async def fetch_data(url, delay=1):
#     await asyncio.sleep(delay)
#     return {"url":url,"status":200,"time":datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

# async def batch_fetch(urls):
#     tasks = [fetch_data(url) for url in urls]
#     result = await asyncio.gather(*tasks)
#     return list(result)

# async def batch_fetch_with_limit(urls, concurrency=3):
#     semaphore = asyncio.Semaphore(concurrency)

#     async def limited_fetch(url):
#         async with semaphore:
#             return await fetch_data(url)

#     tasks = [limited_fetch(url) for url in urls]
#     results = await asyncio.gather(*tasks)
#     return list(results)


# # # 示例
# urls = ["api/users", "api/posts", "api/comments"]
# results = asyncio.run(batch_fetch(urls))

# print(results)
# # 返回 [{"url": "api/users", "status": 200}, ...]

# 获取本地配置
# API_KEY = os.getenv("API_KEY","test_key_api")

# # 设置日志格式
# logging.basicConfig(level=logging.INFO,format="%(asctime)s - %(message)s")
# logger = logging.getLogger(__name__)

# async def fetch_data():
#     start = datetime.now()
#     logger.info(f"开始请求，API Key: {API_KEY[:4]}***")

#     # 模拟异步请求
#     await asyncio.sleep(1.5)
#     mock_response = {"status": "ok", "data": [1, 2, 3]}

#     ## 处理返回结果为json
#     json_str = json.dumps(mock_response,indent=2)
#     logger.info(f"收到响应：\n{json_str}")

#     elapsed = (datetime.now() - start).total_seconds()
#     logger.info(f"请求完成，耗时 {elapsed:.2f}s")
#     return mock_response
# if __name__ == "__main__":
#     asyncio.run(fetch_data())


### 异步生产者-消费者模型
# 使用 `asyncio` 编写一个简单的生产者-消费者模型：
# - 定义异步函数 `producer(name, count, queue)`，生产 `count` 个数据放入队列，
# 每个数据格式为 `{"producer": name, "value": i}`，每次生产间隔 `asyncio.sleep(0.1)`

# - 定义异步函数 `consumer(name, queue)`，持续从队列取数据并处理（打印），当收到 `None` 时停止

# - 编写异步函数 `main()` 创建 2 个生产者和 1 个消费者，使用 `asyncio.Queue` 通信
import asyncio
async def producer(name, count, queue):
    for i in range(count):
        data = {"producer": name, "value": i}
        await queue.put(data)
        print(f"{name} 生产: {data}")
        await asyncio.sleep(0.1)

async def consumer(name, queue):
    while True:
        data = await queue.get()
        if data is None:
            print(f"{name} 结束")
            break
        print(f"{name} 收到: {data}")
        queue.task_done()

async def main():
    # 创建独立的队列对象
    queue = asyncio.Queue()

    p1 = asyncio.create_task(producer("P1", 3, queue))
    p2 = asyncio.create_task(producer("P2", 3, queue))

    c = asyncio.create_task(consumer("C1", queue))

    await p1
    await p2
    await queue.put(None)
    await c

    #  另一种写法
    # # 启动所有任务
    # producers = [
    #     asyncio.create_task(producer("P1", 3, queue)),
    #     asyncio.create_task(producer("P2", 3, queue)),
    # ]
    # consumer_task = asyncio.create_task(consumer("C1", queue))

    # # 等待所有生产者完成
    # await asyncio.gather(*producers)

    # # 发送停止信号
    # await queue.put(None)

    # # 等待消费者完成
    # await consumer_task

if __name__ == "__main__":
    asyncio.run(main())



# 示例输出（顺序可能不同）
# Consumer 收到: {'producer': 'P1', 'value': 0}
# Consumer 收到: {'producer': 'P2', 'value': 0}
# ...
# Consumer 结束