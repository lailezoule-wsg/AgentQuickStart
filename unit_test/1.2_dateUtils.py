# 编写类 `DateUtils`，包含以下静态方法：

# - `parse(date_str, fmt="%Y-%m-%d")` 将字符串解析为 `date` 对象
# - `format_date(d, fmt="%Y年%m月%d日")` 将 `date` 格式化为字符串
# - `days_between(d1, d2)` 返回两个日期之间的天数差（绝对值）
# - `is_weekend(d)` 判断是否为周末
# - `add_business_days(d, n)` 返回从 `d` 开始加 `n` 个工作日后的日期

from datetime import datetime,timedelta,date

class DateUtils:
    @staticmethod
    def parse(date_str, fmt="%Y-%m-%d"):
        return datetime.strptime(date_str,fmt).date()
    @staticmethod
    def format_date(d, fmt="%Y年%m月%d日"):
        return d.strftime(fmt) 
    @staticmethod
    def days_between(d1, d2):
        return abs((d1-d2).days)
    @staticmethod
    def is_weekend(d):
        return d.weekday() >= 5
    @staticmethod
    def add_business_days(d, n):
        added = 0
        current = d
        while added < n:
            current += timedelta(days=1)
            if current.weekday() < 5:
                added += 1
        return current
    @staticmethod
    def add_business_days2(d, n):
        # 遇到周末就跳
        current = d
        add = 0
        while add < n:
            current += timedelta(days=1)
            if current.weekday() < 5:
                add += 1
        return current