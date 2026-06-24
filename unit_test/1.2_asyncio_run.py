# 使用 `asyncio` 编写一个模拟 API 批量请求的异步程序：

# - 定义异步函数 `fetch_data(url, delay)`，模拟网络请求（用 `asyncio.sleep(delay)` 模拟），返回 `{"url": url, "status": 200}`
# - 编写异步函数 `batch_fetch(urls)`，并发请求所有 URL，返回所有结果
# - 编写异步函数 `batch_fetch_with_limit(urls, concurrency=3)`，限制最大并发数为 3
# - 使用 `asyncio.run()` 运行

import asyncio
from datetime import datetime

async def fetch_data(url, delay=1):
    await asyncio.sleep(delay)
    return {"url":url,"status":200,"time":datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

async def batch_fetch(urls):
    tasks = [fetch_data(url) for url in urls]
    result = await asyncio.gather(*tasks)
    return list(result)

async def batch_fetch_with_limit(urls, concurrency=3):
    semaphore = asyncio.Semaphore(concurrency)

    async def limited_fetch(url):
        async with semaphore:
            return await fetch_data(url)

    tasks = [limited_fetch(url) for url in urls]
    results = await asyncio.gather(*tasks)
    return list(results)


# # 示例
urls = ["api/users", "api/posts", "api/comments"]
results = asyncio.run(batch_fetch(urls))

print(results)
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