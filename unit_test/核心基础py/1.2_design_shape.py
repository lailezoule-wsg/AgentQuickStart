# 设计一个图形类层次结构：

# - 基类 `Shape`，包含 `name` 属性和 `area()` 方法（抛出 `NotImplementedError`）
# - 子类 `Circle(radius)`，实现 `area()` 返回圆面积
# - 子类 `Rectangle(width, height)`，实现 `area()` 返回矩形面积
# - 子类 `Triangle(base, height)`，实现 `area()` 返回三角形面积
# - 编写函数 `total_area(shapes)` 接收图形列表，返回总面积

# 示例
# shapes = [Circle(3), Rectangle(4, 5), Triangle(6, 3)]
# print(total_area(shapes))  # 约 47.27

import math

class Shape():
    def __init__(self,name):
        self.name = name

    def area(self):
        raise NotImplementedError("子类必须实现 area() 方法")

class Circle(Shape):
    def __init__(self, radius):
        super().__init__("圆")
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2
    
class Rectangle(Shape):
    def __init__(self, width,height):
        super().__init__("矩形")
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height
    
class Triangle(Shape):
    def __init__(self, base,height):
        super().__init__("三角形")
        self.base = base
        self.height = height

    def area(self):
        return self.base * self.height * 0.5
    
def total_area(shapes):
    return sum(s.area() for s in shapes)
    
shapes = [Circle(3), Rectangle(4, 5), Triangle(6, 3)]
print(total_area(shapes))  # 约 47.27

# **(1)** 使用 `dataclass` 定义 `Student` 类：
# - 字段：`name: str`、`age: int`、`scores: list`（默认空列表）
# - 实现方法 `average()` 返回平均分
# - 实现方法 `is_passed(pass_line=60)` 判断是否全部及格
# **(2)** 使用 Pydantic `BaseModel` 定义 `APIConfig` 类：
# - 字段：`host: str`（必填）、`port: int`（默认 8080）、`debug: bool`（默认 False）、`timeout: float`（默认 30.0）
# - 使用 `@validator` 或 `@field_validator` 验证 `port` 在 1~65535 之间
# # 示例
# config = APIConfig(host="localhost", port=3000, debug=True)
# print(config.host, config.port)  # localhost 3000
from dataclasses import dataclass,field

@dataclass
class Student:
    name:str
    age:int
    scores:list = field(default_factory=list)

    def average(self):
        if not self.scores:
            return 0
        return sum(self.scores) / len(self.scores)
    
    def is_passed(self,pass_line=60):
        # 列表推导式 立即在内存中创建一个完整的列表，包含所有的 True/False。
        # all([s >= pass_line for s in self.scores])

        # 生成器推导式 生成一个生成器对象，不预先存储任何数据 占用内存较少
        return all(s >= pass_line for s in self.scores)
    
        # lst = [1 if ps >= pass_line else 0 for ps in self.scores]
        # if sum(lst) == len(self.scores):
        #     return True
        # return False


# 使用 Pydantic `BaseModel` 定义 `APIConfig` 类：
# - 字段：`host: str`（必填）、`port: int`（默认 8080）、`debug: bool`（默认 False）、`timeout: float`（默认 30.0）
# - 使用 `@validator` 或 `@field_validator` 验证 `port` 在 1~65535 之间

# 实现：test3.py


# 使用 `pathlib` 编写类 `FileAnalyzer`：
# - `__init__(self, path_str)` 接收路径字符串
# - `exists()` 判断文件是否存在
# - `get_extension()` 返回文件扩展名（不含 `.`）
# - `get_size()` 返回文件大小（字节），不存在返回 -1
# - `read_content()` 读取文件内容，不存在返回空字符串
# - `count_lines()` 返回文件行数，不存在返回 0
# - `list_siblings()` 列出同目录下相同扩展名的所有文件

from pathlib import Path

class FileAnalyzer:
    def __init__(self,path_str):
        self.path = Path(path_str)
        # print(self.path)
    
    def exists(self):
        return self.path.exists()
    
    def get_extension(self):
        return self.path.suffix.lstrip(".")
    
    def get_size(self):
        if not self.path.exists():
            return -1
        return self.path.stat().st_size
    
    def read_content(self):
        if not self.path.exists():
            return ""
        return self.path.read_text(encoding="utf-8")
    def count_lines(self):
        if not self.path.exists():
            return 0
        return len(self.path.read_text(encoding="utf-8").splitlines())
    
    def list_siblings(self):
        ext = self.path.suffix
        parent = self.path.parent
        if not parent.exists():
            return []
        return [str(p) for p in parent.glob(f"*{ext}")]

# 示例
# path_str = "D:/software/Pycharm202502/pythonProject/AgentQuickStudy/unit_test/test/test.py"
# analyzer = FileAnalyzer(path_str)
# print(analyzer.exists())
# print(analyzer.get_extension())  # "py"
# print(analyzer.count_lines())    # 42
# # print(analyzer.list_siblings())

# print([str(p) for p in Path(path_str).parent.glob("*py")])



