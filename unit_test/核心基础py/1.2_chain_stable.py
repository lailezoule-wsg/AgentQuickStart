### 链表节点类
# 设计一个简易的单向链表：
# - 定义 `Node(value, next_node=None)` 类
# - 定义 `LinkedList` 类，包含以下方法：
#   - `append(value)` 在尾部添加节点
#   - `prepend(value)` 在头部添加节点
#   - `find(value)` 查找第一个匹配的节点，返回索引，未找到返回 -1
#   - `remove(value)` 删除第一个匹配的节点，不存在则抛出 `ValueError`
#   - `__len__()` 返回节点数量
#   - `__iter__()` 使链表可迭代，依次产出每个节点的值


"""
单向链表三要素：节点、链、头节点（起始点）
"""
class Node:
    def __init__(self, value, next_node=None):
        self.value = value
        self.next = next_node

class LinkedList:
    def __init__(self):
        self._head = None
        self._size = 0

    def append(self, value):
        new_node = Node(value)
        if self._head is None:
            self._head = new_node
        else:
            current = self._head
            while current.next:
                current = current.next
            current.next = new_node
        self._size += 1

    def prepend(self, value):
        new_node = Node(value)
        new_node.next = self._head
        self._head = new_node
        self._size += 1 

    def find(self, value):
        current = self._head
        index = 0
        while current:
            if current.value == value:
                return index
            else:
                current = current.next
                index += 1
            return -1


    def remove(self, value):
        if self._head is None:
            raise ValueError(f"{value} is not found")
        
        if self._head.value == value:
            self._head = self._head.next
            self._size -= 1
            return 
        current = self._head
        while current.next:
            if current.next.value == value:
                current.next = current.next.next
                self._size -= 1
                return
            current = current.next
        raise ValueError(f"{value} not found")


    def __len__(self):
        return self._size

    def __iter__(self):
        current = self._head
        while current:
            yield current.value
            current = current.next
# 示例
ll = LinkedList()
ll.append(1)
ll.append(2)
ll.append(3)
ll.prepend(0)
print(list(ll))    # [0, 1, 2, 3]
print(len(ll))     # 4
print(ll.find(2))  # 2
ll.remove(2)
print(list(ll))    # [0, 1, 3]

# 使用 `dataclass` 定义一个简单的数学表达式树：
# - `Number(value: float)` 表示数字
# - `BinaryOp(op: str, left, right)` 表示二元运算（`+`、`-`、`*`、`/`）
# - 实现函数 `evaluate(expr)` 递归计算表达式的值
# - 实现函数 `to_string(expr)` 将表达式转为可读字符串

from dataclasses import dataclass
from typing import Union

@dataclass
class Number:
    value:float

@dataclass
class BinaryOp:
    op:str
    left:Union[Number,'BinaryOp']
    right:Union[Number,'BinaryOp']

def evaluate(expr):
    if isinstance(expr,Number):
        return float(expr.value)
    elif isinstance(expr,BinaryOp):
        l = evaluate(expr.left)
        r = evaluate(expr.right)
        try:
            if expr.op == "+":
                return l + r
            elif expr.op == "-":
                return l - r
            elif expr.op == "*":
                return l * r
            elif expr.op == "/":
                return l / r
            else:
                raise ValueError(f"Unknown operator: {expr.op}")
        except Exception as e:
            raise ValueError(f"Unknown operator: {e}")

def to_string(expr):
    if isinstance(expr, Number):
        return str(float(expr.value))
    elif isinstance(expr, BinaryOp):
        l = to_string(expr.left)
        r = to_string(expr.right)
        return f"({l} {expr.op} {r})"

# 示例：表示 (3 + 5) * 2
expr = BinaryOp("*", BinaryOp("+", Number(3), Number(5)), Number(2))
print(evaluate(expr))    # 16.0
print(to_string(expr))   # "((3.0 + 5.0) * 2.0)"
