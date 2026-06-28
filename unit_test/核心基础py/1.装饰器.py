from functools import wraps
from typing import Any

# 简单装饰器
def my_decorator(func):
    def wrapper():
        print("函数执行前")
        func()
        print("函数执行后")
    return wrapper

@my_decorator
def say_hello():
    print("say hello")

#`@my_decorator` 等价于 `say_hello = my_decorator(say_hello)`，这是一种语法糖
# say_hello = my_decorator(say_hello)
# say_hello()

# say_hello()

# 装饰器
def logger2(func):
    def wrapper(*args,**kwargs):
        print(f"调用 {func.__name__}，参数: {args}, {kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} 执行完毕，返回: {result}")
        return result
    return wrapper
@logger2
def add(a, b):
    """
        两数之和
    """
    return a + b

# print(add(3, 5))
# print(add.__name__)
# print(add.__doc__)

# 装饰器-进阶   @wraps(func)： 保留原函数 元数据
def logger3(func):
    @wraps(func)  # 保留原函数 元数据
    def wrapper(*agrs,**kwags):
        return func(*agrs,**kwags)
    return wrapper

@logger3
def add2(x,y):
    """
        两数之和
    """
    return x + y

# print(add2(3,4))
# print(add2.__name__)
# print(add2.__doc__)

# 装饰器-进阶  装饰器本身需要参数，就要再嵌套一层：外层接收参数，中层接收函数，内层执行逻辑
def repeat_name(times):
    def outName(func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            result = None
            for _ in range(times):
                result = func(*args,**kwargs)
            return result
        return wrapper
    return outName


@repeat_name(4)
def pt_name(name):
    print(f"Hi {name}")

pt_name("wangsg")

# 装饰器-进阶 类装饰器  类装饰器适合需要**维护状态**的场景（如计数、缓存）
class CountCalls:
    def __init__(self,func):
        wraps(func)(self)
        self.func = func
        self._count = 0
    
    def __call__(self, *args, **kwds):
        self._count += 1
        print(f"{self.func.__name__}已被调用{self._count}")
        return self.func(*args, **kwds)
    
@CountCalls
def say_hl():
    print(f"Hi!")

say_hl()
say_hl()

# 装饰器-进阶 用装饰器装饰类
def wrapClass(cls):
    cls.new_method = lambda self: f"我是 {self.__class__.__name__} 的新方法"
    return cls
@wrapClass
class MyClass:
    pass

obj = MyClass()
print(obj.new_method())   # 我是 MyClass 的新方法

## 常见内置装饰器
# | 装饰器                 | 作用                               |
# | ---------------------- | ---------------------------------- |
# | `@staticmethod`        | 定义静态方法，无需实例             |
# | `@classmethod`         | 定义类方法，第一个参数是类本身     |
# | `@property`            | 把方法变成属性访问                 |
# | `@functools.lru_cache` | 自动缓存函数结果                   |
# | `@dataclass`           | 自动生成 `__init__`、`__repr__` 等 |

from functools import lru_cache

## 自动为函数添加一个缓存字典（字典的键是参数，值是返回值）
@lru_cache(maxsize=128)
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

print(fib(100))   # 极快，结果被缓存

class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def area(self):
        import math
        return math.pi * self._radius ** 2

c = Circle(5)
print(c.area)   # 像属性一样访问，无需括号

## 案例 1：计时器
import time

def timer(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        start = time.perf_counter()
        res = func(*args,**kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__}耗时{elapsed:.4f}秒")
        return res
    return wrapper

@timer
def slow_num(n):
    return sum(range(n))

print(slow_num(1_000_000))

# 案例 2：日志记录
import logging
from datetime import datetime

logging.basicConfig(level=logging.DEBUG,format="%(asctime)s - %(levelname)s - %(message)s")

logger = logging.getLogger(__name__)

def logg(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{ts}] 调用 {func.__name__}(args={args}, kwargs={kwargs})")
        try:
            res = func(*args,**kwargs)
            logger.debug(f"{func.__name__}执行结束,返回{res}")
            return res
        # except ZeroDivisionError:
        #     raise ZeroDivisionError("分母不能为0")
        except Exception as e:
            print(f"[{ts}] {func.__name__} 抛出异常: {e}")
            raise
    return wrapper

@logg
def divide(a, b):
    return a / b

divide(1,2)

current_user = {"name": "alice", "role": "guest"}
# 案例 3：权限校验
def require_role(role):
    def role_check(func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            if current_user.get("role") != role:
                raise PermissionError(f"需要 {role} 权限，当前为 {current_user.get('role')}")
            res = func(*args,**kwargs)
            return res
        return wrapper
    return role_check


@require_role("admin")
def delete_user(user_id):
    print(f"已删除用户 {user_id}")

# delete_user(1)   # guest 角色会抛 PermissionError

import random
# 案例 4：自动重试
def retry(times,delay):
    def fetch(func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            last_except = None
            for t in range(1,times+1):
                try:
                    return func(*args,**kwargs)
                except Exception as e:
                    print(f"第 {t} 次失败: {e}")
                    last_except = e
                    if t < times:
                        time.sleep(delay)
            raise last_except
        return wrapper
    return fetch


@retry(times=3, delay=0.5)
def fetch_data():
    if random.random() < 0.7:
        raise ConnectionError("网络波动")
    return "数据获取成功"

print(fetch_data())


# 案例 5：缓存结果
## 手写一个简易缓存装饰器（类似 `lru_cache` 的简化版）
def cache(func):
    _store = {}
    @wraps(func)
    def wrapper(*agrs):
        if agrs not in _store:
            _store[agrs] = func(*agrs)
        return _store[agrs]
    return wrapper

@cache
def square(n):
    print(f"计算 {n} 的平方")
    return n * n

print(square(4))   # 计算并缓存
print(square(4))   # 直接返回缓存
print(square(5))   # 计算并缓存

# 案例 6：限流
## 限制函数在一段时间内的调用次数。
# 双端队列  比普通list更快
from collections import deque
def rate_limit(calls,period):
    def rate_msg(func):
        history = deque()
        @wraps(func)
        def wrapper(*args,**kwargs):
            now = time.time()
            while history and history[0] < now - period:
                history.popleft()
            if len(history) >= calls:
                raise RuntimeError(f"超过限流：{calls} 次 / {period} 秒")
            history.append(now)
            return func(*args,**kwargs)
        return wrapper
    return rate_msg

@rate_limit(calls=3, period=10)
def send_msg(msg):
    print(f"发送: {msg}")

for i in range(5):
    try:
        send_msg(f"消息{i}")
    except RuntimeError as e:
        print(e)


# 装饰器叠加
## 多个装饰器可叠加使用，**执行顺序从下到上装饰，从上到下执行**。
"""
1. 装饰的顺序：从下往上（离函数最近的最先执行）。
2. 执行的顺序：从上往下（先外层后内层，但在函数调用时是从内到外环绕）。
"""
def dec_a(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("A 前")
        result = func(*args, **kwargs)
        print("A 后")
        return result
    return wrapper

def dec_b(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("B 前")
        result = func(*args, **kwargs)
        print("B 后")
        return result
    return wrapper

@dec_a
@dec_b
def hello():
    print("hello")

hello()

# 要点总结
"""
1. 装饰器 = 接收函数、返回函数的函数，用 `@` 语法应用。
2. 用 `*args, **kwargs` 让 wrapper 适配任意函数签名。
3. **永远加 `@wraps(func)`** 保留原函数元信息。
4. 带参数的装饰器需要三层嵌套：参数层 → 函数层 → wrapper 层。
5. 类装饰器靠 `__call__`，适合维护状态。
6. 装饰器可叠加，顺序：装饰从下到上，执行从外到内。
7. 常用场景：日志、计时、缓存、权限、重试、限流。
建议按顺序敲一遍以上代码，理解后再尝试自己写一个装饰器。
"""