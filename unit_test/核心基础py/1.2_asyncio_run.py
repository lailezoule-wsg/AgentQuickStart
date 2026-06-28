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


# 使用 `asyncio` 编写一个通用的异步重试装饰器：
# - 定义装饰器 `retry(max_retries=3, delay=1.0)`
# - 被装饰的异步函数执行失败（抛出异常）时，自动重试
# - 每次重试前等待 `delay` 秒
# - 达到最大重试次数后，抛出最后一次异常
# - 每次重试时用 `logging` 记录日志：`"第 N 次重试: {异常信息}"`

import asyncio
import logging
from functools import wraps
from typing import Any, Callable, Coroutine, TypeVar

# 配置日志
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

T = TypeVar('T')  # 类型变量，用于类型注解


def retry(max_retries: int = 3, delay: float = 1.0):
    """
    异步重试装饰器
    
    Args:
        max_retries: 最大重试次数（包含第一次尝试）
        delay: 每次重试前的等待时间（秒）
    
    Example:
        @retry(max_retries=3, delay=0.5)
        async def fetch_data():
            # 可能失败的异步操作
            pass
    """
    def decorator(func: Callable[..., Coroutine[Any, Any, T]]) -> Callable[..., Coroutine[Any, Any, T]]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            last_exception = None
            
            for attempt in range(1, max_retries + 1):
                try:
                    # 执行被装饰的异步函数
                    result = await func(*args, **kwargs)
                    # 如果成功，立即返回结果
                    return result
                    
                except Exception as e:
                    last_exception = e
                    
                    # 如果不是最后一次重试，记录日志并等待
                    if attempt < max_retries:
                        logger.warning(f"第 {attempt} 次重试: {e}")
                        await asyncio.sleep(delay)
                    else:
                        # 最后一次尝试失败，记录错误日志
                        logger.error(f"达到最大重试次数 {max_retries}，最后一次异常: {e}")
            
            # 所有重试都失败，抛出最后一次异常
            raise last_exception
        
        return wrapper
    
    return decorator


# ============ 使用示例 ============

import random

@retry(max_retries=5, delay=0.5)
async def unstable_api_call(data: str) -> str:
    """模拟一个不稳定的 API 调用，有 70% 概率失败"""
    await asyncio.sleep(0.2)  # 模拟网络延迟
    
    if random.random() < 0.7:  # 70% 概率失败
        raise ValueError(f"API 调用失败: {data}")
    
    return f"成功处理: {data}"


@retry(max_retries=3, delay=1.0)
async def database_query(query: str) -> list:
    """模拟数据库查询，可能超时或连接失败"""
    await asyncio.sleep(0.1)
    
    # 模拟不同错误
    error_type = random.choice(["timeout", "connection", "success", "success"])
    if error_type == "timeout":
        raise TimeoutError(f"查询超时: {query}")
    elif error_type == "connection":
        raise ConnectionError(f"数据库连接失败: {query}")
    
    return [f"结果1", f"结果2", f"结果3"]


# ============ 运行测试 ============

async def main():
    print("=== 测试不稳定 API ===")
    try:
        result = await unstable_api_call("user_data")
        print(f"API 调用成功: {result}")
    except Exception as e:
        print(f"API 调用最终失败: {e}")
    
    print("\n=== 测试数据库查询 ===")
    try:
        result = await database_query("SELECT * FROM users")
        print(f"查询成功: {result}")
    except Exception as e:
        print(f"查询最终失败: {e}")
    
    print("\n=== 测试并发执行 ===")
    # 多个任务并发执行，每个有自己的重试机制
    tasks = [
        unstable_api_call(f"request_{i}")
        for i in range(3)
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"任务 {i}: 失败 - {result}")
        else:
            print(f"任务 {i}: 成功 - {result}")


if __name__ == "__main__":
    asyncio.run(main())