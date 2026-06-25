# 设计一个 `BankAccount` 类：

# - `__init__(self, owner, balance=0)` 初始化账户名和余额
# - `deposit(amount)` 存款，金额为正数，否则抛出 `ValueError`
# - `withdraw(amount)` 取款，金额不能超过余额，否则抛出 `ValueError`
# - `transfer(other_account, amount)` 转账给另一个账户
# - `__str__()` 返回 `"BankAccount(owner=xxx, balance=xxx)"`
# - 使用 `@property` 保护 `balance` 属性，不允许外部直接修改

class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self._balance = balance

    @property
    def balance(self):
        return self._balance
    
    def deposit(self,amount):
        if amount < 0:
            raise ValueError("金额为正数")
        self._balance += amount
        
    def withdraw(self,amount):
        if self._balance < amount:
            raise ValueError("金额不能超过余额")
        self._balance -=amount

    def transfer(self,other_account, amount):
        #转账后自己的
        self.withdraw(amount)
        #转账后他人的
        other_account.deposit(amount)

    def __str__(self):
        return f"BankAccount(owner={self.owner}, balance={self._balance})"


# 示例
a1 = BankAccount("Alice", 1000)
a2 = BankAccount("Bob", 500)
a1.transfer(a2, 200)
print(a1)  # BankAccount(owner=Alice, balance=800)
print(a2)  # BankAccount(owner=Bob, balance=700)