# **(1)** 编写函数 `setup_logger(name, log_file, level=logging.INFO)`：

# - 创建一个 logger
# - 同时添加 `FileHandler`（写入 `log_file`）和 `StreamHandler`（输出到控制台）
# - 格式统一为 `"%(asctime)s - %(name)s - %(levelname)s - %(message)s"`
# - 返回配置好的 logger

import asyncio
import logging


class setupLogger:
    def __init__(self,name,log_file,level=logging.INFO):
        self.name = name
        self.log_file = log_file
        self.level = level
        self.logger = logging.getLogger(name)
    
    def stLog(self):
        self.logger.setLevel(self.level)
        # 设置log格式
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        # 添加写入文件句柄 FileHandler
        fh = logging.FileHandler(filename=self.log_file,encoding="utf-8")
        fh.setFormatter(formatter)

        # 添加输出到控制台句柄 StreamHandler
        sh = logging.StreamHandler()
        sh.setFormatter(formatter)

        # 追加句柄到logger对象
        self.logger.addHandler(fh)
        self.logger.addHandler(sh)
        return self.logger

sl = setupLogger(__name__,"app.log")
logger = sl.stLog()

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
