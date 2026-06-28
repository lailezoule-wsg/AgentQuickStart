### 题目 2：异步限流批量请求

# 编写异步函数 `batch_fetch(urls, concurrency=5)`：

# - 使用 `asyncio.Semaphore` 限制最大并发数为 `concurrency`
# - 每个请求之间添加 0.1 秒延迟（避免过快）
# - 返回所有结果列表
# - 使用 `httpx.AsyncClient` 发送请求

import httpx
import asyncio

async def batch_fetch(urls, concurrency=5):
    sem = asyncio.Semaphore(concurrency)
    async def fetch_one(client,url):
        async with sem:
            try:
                response = await client.get(url,timeout=10.0)
                result = {"url": url, "status": response.status_code, "body": response.text[:100]}
            except Exception as e:               
                result = {"url": url, "status": 0, "error": str(e)}

            await asyncio.sleep(0.1)
            return result

    async with httpx.AsyncClient() as client:
        fetchList = [fetch_one(client,url) for url in urls]
        results = await asyncio.gather(*fetchList)
        return list(results)

# 示例
urls = [f"https://httpbin.org/get?id={i}" for i in range(20)]
results = asyncio.run(batch_fetch(urls, concurrency=5))
print(f"成功: {sum(1 for r in results if r['status'] == 200)}")

