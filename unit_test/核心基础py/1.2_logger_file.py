# **(1)** 编写函数 `setup_logger(name, log_file, level=logging.INFO)`：

# - 创建一个 logger
# - 同时添加 `FileHandler`（写入 `log_file`）和 `StreamHandler`（输出到控制台）
# - 格式统一为 `"%(asctime)s - %(name)s - %(levelname)s - %(message)s"`
# - 返回配置好的 logger

# import asyncio
# import logging


# class setupLogger:
#     def __init__(self,name,log_file,level=logging.INFO):
#         self.name = name
#         self.log_file = log_file
#         self.level = level
#         self.logger = logging.getLogger(name)
    
#     def stLog(self):
#         self.logger.setLevel(self.level)
#         # 设置log格式
#         formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
#         # 添加写入文件句柄 FileHandler
#         fh = logging.FileHandler(filename=self.log_file,encoding="utf-8")
#         fh.setFormatter(formatter)

#         # 添加输出到控制台句柄 StreamHandler
#         sh = logging.StreamHandler()
#         sh.setFormatter(formatter)

#         # 追加句柄到logger对象
#         self.logger.addHandler(fh)
#         self.logger.addHandler(sh)
#         return self.logger

# sl = setupLogger(__name__,"app.log")
# logger = sl.stLog()

# def setup_logger(name, log_file, level=logging.INFO):

#     # 获取logger对象
#     logger = logging.getLogger(name)
#     # 设置log等级
#     logger.setLevel(level)
#     # 设置log格式
#     formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

#     # 添加写入文件句柄 FileHandler
#     fh = logging.FileHandler(filename=log_file,encoding="utf-8")
#     fh.setFormatter(formatter)

#     # 添加输出到控制台句柄 StreamHandler
#     sh = logging.StreamHandler()
#     sh.setFormatter(formatter)

#     # 追加句柄到logger对象
#     logger.addHandler(fh)
#     logger.addHandler(sh)

#     # 返回logger
#     return logger

# logger = setup_logger(__name__,"app.log")
# logger.info("你好")
# logger.warning("你是谁")



# **(1)** 编写日志配置函数 `create_logger(name)`：
# - 创建 logger，级别为 `DEBUG`
# - 添加 `StreamHandler`，格式为 `"[%(levelname)s] %(name)s: %(message)s"`
# - 返回 logger
import logging

# 日志类
def create_logger(name):
    # 获取 logger对象
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    # 设置日志格式
    formatter = logging.Formatter("[%(levelname)s] %(name)s: %(message)s")
    # 设置开发者日志输出
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    #添加sh
    logger.addHandler(sh)
    return logger

logger = create_logger("cache")
_cache = {}

# **(2)** 编写装饰器 `cached(func)`：
# - 使用字典缓存函数的返回值（以参数元组为 key）
# - 每次调用时，如果命中缓存则用 logger 记录 `"cache hit: ..."` 并返回缓存值
# - 如果未命中，调用函数、存入缓存、用 logger 记录 `"cache miss: ..."` 并返回结果
import functools

def cached(func):
    @functools.wraps(func)
    def wrapper(*args):
        if args in _cache:
            result = _cache[args]
            logger.debug(f"cache hit: {args} -> {result}")
            return result
        result = func(*args)
        _cache[args] = result
        logger.debug(f"cache miss: {args} -> {result}")
        return result
    return wrapper

@cached
def expensive_calc(x, y):
    return x + y

expensive_calc(1, 2)   # 日志: cache miss: (1, 2) -> 3
expensive_calc(1, 2)   # 日志: cache hit: (1, 2) -> 3
expensive_calc(3, 4)   # 日志: cache miss: (3, 4) -> 7
