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

from pydantic import BaseModel,field_validator,model_validator

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

# **(1)** 定义 `RawRecord(BaseModel)`：
# - 字段：`id: int`、`name: str`、`email: str`、`score: str`（注意 score 是字符串）
# - 使用 validator 验证 email 包含 `@`
# - 使用 validator 将 `score` 自动转为 `float`

    
#  定义 `CleanRecord(BaseModel)`：

# - 字段：`id: int`、`name: str`、`email: str`、`score: float`、`grade: str`
# - `grade` 根据 score 自动计算：>=90 为 A，>=80 为 B，>=70 为 C，>=60 为 D，<60 为 F


# 编写函数 `process(records: list[dict]) -> list[CleanRecord]`：

# - 将原始字典列表转为 `CleanRecord` 列表
# - 跳过验证失败的记录，用 `logging` 记录错误

import logging
from typing import List, Optional
from pydantic import BaseModel, field_validator, model_validator, ValidationError

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# ============ (1) RawRecord 定义 ============
class RawRecord(BaseModel):
    id: int
    name: str
    email: str
    score: str  # 原始输入是字符串

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        """验证 email 包含 @"""
        if "@" not in v:
            raise ValueError(f"无效的邮箱: {v}")
        return v

    @field_validator("score", mode="before")
    @classmethod
    def parse_score(cls, v) -> float:
        """将 score 自动转为 float"""
        if isinstance(v, (int, float)):
            return float(v)
        if isinstance(v, str):
            # 去除可能的百分号、空格
            cleaned = v.strip().replace("%", "")
            try:
                return float(cleaned)
            except ValueError:
                raise ValueError(f"无法解析分数: {v}")
        raise ValueError(f"不支持的分数类型: {type(v)}")


# ============ (2) CleanRecord 定义 ============
class CleanRecord(BaseModel):
    id: int
    name: str
    email: str
    score: float
    grade: str

    @model_validator(mode="after")
    def set_grade(self) -> "CleanRecord":
        """根据 score 自动计算 grade"""
        if self.score >= 90:
            self.grade = "A"
        elif self.score >= 80:
            self.grade = "B"
        elif self.score >= 70:
            self.grade = "C"
        elif self.score >= 60:
            self.grade = "D"
        else:
            self.grade = "F"
        return self


# ============ (3) 数据处理函数 ============
def process(records: List[dict]) -> List[CleanRecord]:
    """
    将原始字典列表转为 CleanRecord 列表
    
    Args:
        records: 原始数据字典列表
        
    Returns:
        验证通过的 CleanRecord 列表
    """
    clean_records = []
    
    for idx, raw_data in enumerate(records):
        try:
            # 先通过 RawRecord 验证原始数据
            raw = RawRecord(**raw_data)
            
            # 再转换为 CleanRecord
            clean = CleanRecord(
                id=raw.id,
                name=raw.name,
                email=raw.email,
                score=raw.score,  # 已经是 float
                grade=""  # 由 model_validator 自动计算
            )
            
            clean_records.append(clean)
            logger.info(f"处理成功: {raw.name} (ID: {raw.id})")
            
        except ValidationError as e:
            # 记录验证失败详情
            error_details = []
            for error in e.errors():
                field = " -> ".join(str(loc) for loc in error["loc"])
                msg = error["msg"]
                error_details.append(f"{field}: {msg}")
            
            logger.warning(
                f"记录 #{idx} 验证失败: {raw_data} | 错误: {'; '.join(error_details)}"
            )
            continue
        
        except Exception as e:
            # 捕获其他未预期的异常
            logger.error(f"记录 #{idx} 处理异常: {raw_data} | {e}")
            continue
    
    logger.info(f"处理完成: 成功 {len(clean_records)} 条，失败 {len(records) - len(clean_records)} 条")
    return clean_records


# ============ 测试 ============
if __name__ == "__main__":
    test_data = [
        {"id": 1, "name": "Alice", "email": "alice@test.com", "score": "92.5"},
        {"id": 2, "name": "Bob", "email": "invalid", "score": "85"},
        {"id": 3, "name": "Charlie", "email": "charlie@test.com", "score": "78%"},
        {"id": 4, "name": "Diana", "email": "diana@test.com", "score": "59.9"},
        {"id": 5, "name": "Eve", "email": "eve@test.com", "score": "95.5"},
        {"id": 6, "name": "Frank", "email": "frank@test", "score": "88"},
        {"id": 7, "name": "Grace", "email": "grace@test.com", "score": "42"},
    ]

    print("=" * 50)
    print("开始处理数据...")
    print("=" * 50)

    result = process(test_data)

    print("\n" + "=" * 50)
    print("处理结果:")
    print("=" * 50)
    for record in result:
        print(f"ID: {record.id}, 姓名: {record.name}, 分数: {record.score}, 等级: {record.grade}")

    print(f"\n统计: 成功 {len(result)} 条")
