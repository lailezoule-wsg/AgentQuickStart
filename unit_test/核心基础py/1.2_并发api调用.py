### 题目 1：并发 API 调用器  ***

# 编写异步函数 `fetch_all(urls)`，使用 `asyncio` 并发请求多个 URL：

# - 定义异步函数 `fetch_one(client, url)`，使用 `httpx.AsyncClient` 发送 GET 请求，返回 `{"url": url, "status": response.status_code, "body": response.text[:100]}`
# - 编写异步函数 `fetch_all(urls)`，创建 `httpx.AsyncClient`，并发请求所有 URL，返回结果列表
# - 如果某个请求失败，返回 `{"url": url, "status": 0, "error": str(e)}`

import httpx
import asyncio

async def fetch_one(client, url):
    try:
        response = await client.get(url)
        return {"url": url, "status": response.status_code, "body": response.text[:100]}
    except Exception as e:
        return {"url": url, "status": 0, "error": str(e)}

async def fetch_all(urls):
    async with httpx.AsyncClient() as client:
        fetchList = [fetch_one(client,url) for url in urls]
        results = await asyncio.gather(*fetchList)
    return list(results)

# 示例
urls = ["https://httpbin.org/get", "https://httpbin.org/delay/1"]
results = asyncio.run(fetch_all(urls))
for r in results:
    print(r["url"], r["status"])
