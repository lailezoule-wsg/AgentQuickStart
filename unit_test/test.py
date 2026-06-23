
def count_words(text):
    wordDict = {}
    spliteData = text.split()
    for k in spliteData:
        lowerK = k.lower()
        if wordDict.get(lowerK,0) == 0:
            wordDict[lowerK] = 0
        else:
            wordDict[lowerK] +=1
    return wordDict



dictData = {"name":"wangsg","age":18}

print(dictData.keys())

if "name" in dictData.keys():
    print("55")

# 请用**列表推导式**完成以下操作（每个操作一行代码）：
students = [
    {"name": "Alice", "score": 85},
    {"name": "Bob", "score": 62},
    {"name": "Charlie", "score": 90},
    {"name": "Diana", "score": 45},
    {"name": "Eve", "score": 78},
]

# 1. 筛选出及格（>= 60）的学生名字列表
stuList = [student["name"] for student in students if student["score"] >= 60]
print(stuList)
# 2. 将所有学生按成绩从高到低排序
scoreData = sorted(students,key=lambda stu:stu["score"],reverse=True)
print(scoreData)
# 3. 计算所有学生的平均分
avgScore = sum([student["score"] for student in students]) / len(students)
print(avgScore)

# - 正常情况返回 `a / b` 的结果（保留两位小数）
# - `b` 为 0 时返回 `"错误：除数不能为零"`
# - 参数不是数字时返回 `"错误：参数必须是数字"`
# - 无论成功失败，最后都打印 `"计算完成

def safe_divide(a, b):
    try:
        a = float(a)
        b = float(b)
        res = a / b

        print(f"{res:.2f}")
    except (ValueError,TypeError):
        print("错误：参数必须是数字")
    except ZeroDivisionError:
        print("错误：除数不能为零")
    finally:
        print("计算完成")

safe_divide(1,3)


# 编写函数 `build_profile(first, last, **user_info)`：
# - 将 `first` 和 `last` 组合为 `full_name`
# - 将 `full_name` 和 `**user_info` 中的所有键值对合并到一个字典中返回
# 返回 {"full_name": "张 三", "age": 25, "city": "北京"}

def build_profile(first, last, **user_info):
    full_name = str(first) + ' ' + str(last)
    full_name_dict = {"full_name":full_name}
    user = {**full_name_dict,**user_info}
    print(user)
        

build_profile("张", "三", age=25, city="北京")

ls = [1,2,3,4]

print(*ls)

dc = {"full_name": "张 三", "age": 25, "city": "北京"}

dcc = {**dc}
print(dcc)

# 编写函数 `filter_data(data, **filters)`：

# - `data` 是一个列表，元素为字典
# - `**filters` 是任意数量的过滤条件
# - 返回满足**所有**过滤条件的记录列表

products = [
    {"name": "手机", "price": 5000, "brand": "华为"},
    {"name": "电脑", "price": 8000, "brand": "联想"},
    {"name": "平板", "price": 3000, "brand": "华为"},
    {"name": "耳机", "price": 500, "brand": "小米"},
]

def filter_data(data, **filters):
    # print(type(filters),filters["brand"],filters["price"])
    result = []
    # for prod in data:
    #     if filters["brand"] == prod["brand"] and filters["price"] == prod["price"]:
    #         dct = {
    #             "name":prod["name"],
    #             "price":prod["price"],
    #             "brand":prod["brand"]
    #         }
    #         result.append(dct)

    result = [item for item in data if all(item.get(k) == v for k, v in filters.items())]

    # for item in data:
    #     if all(item.get(k) == v for k, v in filters.items()):
    #         result.append(item)

    return result


print(filter_data(products, brand="华为", price=5000))
# 返回 [{"name": "手机", "price": 5000, "brand": "华为"}]

print(sum([num for num in [1, 2, 3, 4, 5] if num % 2 == 0]))

print(sum(x for x in [1,2,3,4,5] if x % 2 == 0))


print(f"{100}")


text = "hello"
counts = {}
for char in text:
    counts[char] = counts.get(char,0) + 1
print(counts)

def print_info(**kwargs):
    print(type(kwargs))
    for key,value in kwargs.items():
        print(f"{key}: {value}")

print_info(name="Alice", age=25)

records = [
    ("Alice", "math", 90),
    ("Bob", "math", 85),
    ("Alice", "english", 88),
    ("Bob", "english", 92),
    ("Alice", "physics", 95),
]

# 编写函数 `organize_scores(records)`，将其转换为嵌套字典：
# # 期望输出
# {
#     "Alice": {"math": 90, "english": 88, "physics": 95},
#     "Bob": {"math": 85, "english": 92},
# }

# ### 
def organize_scores(records):
    dit = {}
    # for dt in records:
    #     # print(dit,"---",dt)
    #     if dt[0] in dit:
    #         if dt[1] not in dit[dt[0]]:
    #             dit[dt[0]][dt[1]] = dt[2]
    #     else:
    #         dit[dt[0]] = {dt[1]:dt[2]}
    for name,subject,score in records:
        if name not in dit:
            dit[name] = {}
        dit[name][subject] = score
    return dit

print(organize_scores(records))

matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

zp = [x for l1 in matrix for x in l1]
print(zp)


lt = []
for i in range(5):
    ft = []
    for j in range(5):
        if i == j:
            ft.append(1)
        else:
            ft.append(0)
    lt.append(ft)

lt = [[1 if i== j else 0 for i in range(5)] for j in range(5)]

print(lt)

# 编写函数 `parse_config(config_str, **defaults)`：
# - 接收一个多行字符串 `config_str`，每行格式为 `key=value`
# - `**defaults` 是默认配置项
# - 返回一个字典，包含所有默认配置，并用 `config_str` 中的值覆盖同名默认项
# - 自动将 value 转换类型：`"true"/"false"` → `bool`，纯数字 → `int`，带小数点 → `float`，其余保持 `str`
# - 忽略空行和以 `#` 开头的注释行

# 示例
config_text = """
# 数据库配置
host=localhost
port=5432
debug=true
max_connections=100
rate=0.75
"""



def parse_config(config_str, **defaults):
    config1 = config_str.strip().splitlines()
    config_dict = {}
    for line in config1:
        if not line or line.startswith("="):
            continue
        if "=" in line:
            lineSplit = line.split("=")
            config_dict[lineSplit[0]] = defaults.get(lineSplit[0],lineSplit[1])
    return config_dict


result = parse_config(config_text, host="127.0.0.1", port=3306, timeout=30)
# 期望返回：
# {
#     "host": "localhost",       # 被覆盖，str
#     "port": 5432,              # 被覆盖，int
#     "timeout": 30,             # 保留默认
#     "debug": True,             # 新增，bool
#     "max_connections": 100,    # 新增，int
#     "rate": 0.75,              # 新增，float
# }

print(result)

def make_counter():
    count = 0
    def counter():
        nonlocal count
        count += 1
        return count
    return counter

c = make_counter()
print(c(), c(), c())

nums = [1, -2, 3, -4, 5]
for key,num in enumerate(nums):
    if num < 0:
        nums[key] = 0
print(nums)  # 期望输出 [1, 0, 3, 0, 5]

num2 = [x if num > 0 else 0 for x in nums ]
print(num2)

ddd = {
    "Alice": {"math": 90, "english": 88, "physics": 95},
    "Bob": {"math": 85, "english": 92},
}

def func_test(**kw):
    print("----",kw)

func_test(**ddd)
