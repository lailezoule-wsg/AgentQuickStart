# **(1)** 使用 `dataclass` 定义 `Course` 类和 `Student` 类：

# - `Course`：`code: str`、`name: str`、`credits: int`
# - `Student`：`name: str`、`courses: list`（默认空列表）
# - 实现 `Student.add_course(course)` 添加课程
# - 实现 `Student.total_credits()` 返回总学分

from dataclasses import dataclass,field

@dataclass
class Course:
    code: str
    name: str
    credits: int


@dataclass
class Student:
    name: str
    courses: list[Course] = field(default_factory=list)

    """
    dataclass 中一个极其重要但容易被忽视的防御性编程措施
    是为了防止外部调用时显式传入 None 导致程序崩溃
    __post_init__ 是 dataclass 在 __init__ 执行完后自动调用的一个钩子方法。
    你可以在里面做额外的初始化校验或修正。
    """
    def __post_init__(self):
        if self.courses is None:
            self.courses = []

    def __str__(self):
        course_names = [c.name for c in self.courses]
        return f"学生：{self.name}，已选课程：{', '.join(course_names) if course_names else '无'}"

    def add_course(self,course:Course) -> None:
        self.courses.append(course)

    def total_credits(self):
        # 使用生成器方式 节省内存
        return sum(credits.credits for credits in self.courses)

c1 = Course(code="1001",name="数学",credits=3)
c2 = Course(code="1002",name="英语",credits=2)

print(c1)
s1 = Student("lisi")
s1.add_course(c1)
s1.add_course(c2)
print(s1,s1.total_credits())

# **(2)** 使用 Pydantic `BaseModel` 定义 `Product` 类：

# - 字段：`name: str`、`price: float`、`quantity: int`（默认 1）、`tags: list`（默认空列表）
# - 验证 `price > 0`、`quantity >= 0`
# - 实现方法 `total_price()` 返回 `price * quantity`

"""
@field_validator 必须配合 @classmethod 或 @staticmethod 使用，否则会直接报 TypeError。 
这是 Pydantic V2 的强制性语法要求，不是可选项。如果你看到别人的代码里没加，
那可能是 V1 的写法，迁移到 V2 时必须补上。
"""

from pydantic import BaseModel,field_validator

class Product(BaseModel):
    name: str
    price: float
    quantity: int = 1
    tags: list = field(default_factory=list)

    def __post_init__(self):
        if self.tags is None:
            self.tags = []

    @field_validator("price")
    @classmethod
    def check_price(cls,v):
        if v <= 0:
            raise ValueError("price error")
        return v
    
    @field_validator("quantity")
    @classmethod
    def check_quantity(cls,v):
        if v < 0:
            raise ValueError("quantity error")
        return v
    
    def total_price(self):
        return self.price * self.quantity




# 示例
c1 = Course("CS101", "Python 入门", 3)
s = Student("Alice")
s.add_course(c1)
print(s.total_credits())  # 3
