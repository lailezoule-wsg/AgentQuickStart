### 题目 4：异步重试机制

# 编写装饰器 `async_retry(max_retries=3, delay=1.0, backoff=2.0)`：

# - 被装饰的异步函数失败时自动重试
# - 每次重试等待时间按 `backoff` 指数增长（`delay * backoff^n`）
# - 达到最大重试次数后抛出最后一次异常
# - 使用 `logging` 记录每次重试

# 示例
import random
import logging
import asyncio
from functools import wraps

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

def async_retry(max_retries,delay,backoff):
    def async_func(func):
        @wraps(func)
        async def wrapper(*args,**kwargs):
            last_exception = None
            current_delay = delay
            for attempt in range(max_retries+1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries:
                        logger.warning(
                            f"第 {attempt + 1} 次重试 ({current_delay:.1f}s): {e}"
                        )
                        await asyncio.sleep(current_delay)
                        current_delay *= backoff
            raise last_exception
        return wrapper
    return async_func
    

@async_retry(max_retries=3, delay=0.1, backoff=2.0)
async def unstable_api():
    if random.random() < 0.5:
        raise ConnectionError("timeout")
    return {"status": "ok"}

result = asyncio.run(unstable_api())

