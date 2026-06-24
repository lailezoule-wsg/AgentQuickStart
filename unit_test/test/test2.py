# 实现一个命令行通讯录程序，要求：

# 1. 使用 `dict` 存储联系人，格式：`{"name": {"phone": "...", "email": "..."}}`
# 2. 实现以下函数：
#    - `add_contact(contacts, name, phone, email)` - 添加联系人
#    - `find_contact(contacts, name)` - 查找联系人，未找到返回 `"未找到"`
#    - `delete_contact(contacts, name)` - 删除联系人，未找到时友好提示
#    - `list_all(contacts)` - 列出所有联系人，用 f-string 格式化输出
# 3. 所有操作需包含异常处理（如删除不存在的人）
# 4. 编写一个 `main()` 函数演示完整流程

def add_contact(contacts, name, phone, email):
    if name not in contacts:
        contacts[name] = {"phone":phone,"email":email}
    else:
        contacts[name].update({"phone":phone,"email":email})

def find_contact(contacts, name):
    # if name in contacts:
    #     return contacts[name]
    # return "未找到"

    try:
        info = contacts[name]
        return f"{name}: {info['phone']}, {info['email']}"
    except KeyError:
        return "未找到"

def delete_contact(contacts, name):
    # 条件检查（LBYL 风格：先检查，后执行）  此方法：需要一次hash查找
    # if name in contacts:
    #     del contacts[name]
    #     return true
    # return false

    # 异常捕获（EAFP 风格：直接执行，事后捕获）
    try:
        del contacts[name]
        print(f"已删除联系人: {name}")
    except KeyError:
        print(f"联系人 {name} 不存在")

def list_all(contacts):
    if not contacts:
        print("通讯录为空")
        return
    else:
        for name, info in contacts.items():
            print(f"{name}: 电话={info['phone']}, 邮箱={info['email']}")
            

def main():
    contacts = {}
    add_contact(contacts, "Alice", "13800001111", "alice@example.com")
    add_contact(contacts, "Alice", "13800001111", "alice@example.com")
    add_contact(contacts, "Bob", "13900002222", "bob@example.com")
    print(find_contact(contacts, "Alice"))
    print(find_contact(contacts, "Charlie"))
    delete_contact(contacts, "Bob")
    delete_contact(contacts, "Charlie")
    print("--- 所有联系人 ---")
    list_all(contacts)

if __name__ == "__main__":
   
   main()
   