### 题目 5：异步任务管理器

# 编写类 `TaskManager`，管理一组异步任务：

# - `submit(name, coro)` 提交任务，返回 Task 对象
# - `cancel(name)` 取消指定任务
# - `status()` 返回所有任务状态的字典（`{"name": "pending"/"running"/"done"/"cancelled"}`）
# - `wait_all()` 等待所有任务完成，返回结果字典（`{"name": result}`），失败的任务值为异常对象
# - `results()` 返回已完成任务的结果字典

import asyncio

class TaskManager:
    def __init__(self):
        self._tasks = {}

    def submit(self,name,coro):
        task = asyncio.create_task(coro)
        self._tasks[name] = task
        return task
    
    def cancel(self,name):
        if name in self._tasks:
            self._tasks[name].cancel()

    def status(self):
        result = {}
        for name, task in self._tasks.items():
            if task.cancelled():
                result[name] = "cancelled"
            elif task.done():
                result[name] = "done"
            else:
                result[name] = "running"
        return result

    async def wait_all(self):
        results = {}
        for name, task in self._tasks.items():
            try:
                results[name] = await task
            except Exception as e:
                results[name] = e
        return results

    def results(self):
        results = {}
        for name, task in self._tasks.items():
            # 判断任务是否执行完成 或者  取消
            if task.done() and not task.cancelled():
                # 任务虽然执行结束 但可能执行失败 需要try获取错误
                try:
                    results[name] = task.result()
                except Exception as e:
                    results[name] = e
        return results

# 示例
async def demo():
    tm = TaskManager()
    tm.submit("fast", asyncio.sleep(0.1, result="done"))
    tm.submit("slow", asyncio.sleep(0.5, result="finished"))
    tm.submit("fail", asyncio.sleep(0.2, result=1/0))  # 会报错

    await asyncio.sleep(0.3)
    print(tm.status())
    # {"fast": "done", "slow": "running", "fail": "done"}

    all_results = await tm.wait_all()
    print(all_results)
    # {"fast": "done", "slow": "finished", "fail": ZeroDivisionError(...)}

asyncio.run(demo())
