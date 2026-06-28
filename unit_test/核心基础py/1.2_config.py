### JSON 配置管理器
# 使用 `json` 和 `pathlib` 编写类 `ConfigManager`：
# - `__init__(self, config_path)` 接收配置文件路径
# - `load()` 从 JSON 文件加载配置为字典，文件不存在则返回空字典
# - `save()` 将当前配置写入 JSON 文件（格式化输出，支持中文）
# - `get(key, default=None)` 获取配置项，支持点号分隔的嵌套访问（如 `"database.host"`）
# - `set(key, value)` 设置配置项，支持点号分隔的嵌套设置
# - `update(data: dict)` 批量更新配置
from pathlib import Path
import json
"""
{
    "db":{
        "host":"127.0.0.1",
        "port":8080,
        "other":{
            "t1":"ttt",
            "t2":{
                "tt2":"哈哈哈哈"
            },
            "t3":{
                "tt3":8888
            }
        }
    },
    "redis":{
        "host":"localhost",
        "port":3306
    },
    "username":"wangsg",
    "password":"12345"
}
"""
import json
from pathlib import Path
from typing import Any, Optional


class ConfigManager:
    def __init__(self, config_path: str):
        """初始化配置管理器"""
        self.config_path = Path(config_path)
        self._config = {}  # 存储配置的字典

    def load(self) -> dict:
        """从 JSON 文件加载配置，文件不存在则返回空字典"""
        if not self.config_path.exists():
            self._config = {}
            return self._config

        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                self._config = json.load(f)
        except json.JSONDecodeError:
            print(f"警告: {self.config_path} 不是有效的 JSON 文件，使用空配置")
            self._config = {}
        return self._config

    def save(self) -> None:
        """将当前配置写入 JSON 文件（格式化输出，支持中文）"""
        # 确保目录存在
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self._config, f, indent=2, ensure_ascii=False)

    def get(self, key: str, default=None) -> Any:
        """
        获取配置项，支持点号分隔的嵌套访问。
        示例: config.get("database.host") -> 返回 config["database"]["host"]
        """
        keys = key.split(".")
        current = self._config

        for k in keys:
            if isinstance(current, dict) and k in current:
                current = current[k]
            else:
                return default
        return current

    # 核心：使用了python的引用复制 改动current 同步改了_config
    def set(self, key: str, value: Any) -> None:
        """
        设置配置项，支持点号分隔的嵌套设置。
        示例: config.set("database.host", "localhost") -> 自动创建中间层级
        """
        keys = key.split(".")
        current = self._config

        # 遍历到倒数第二层，自动创建中间层级的字典
        for k in keys[:-1]:
            if k not in current or not isinstance(current[k], dict):
                current[k] = {}
            current = current[k]

        # 设置最终值
        current[keys[-1]] = value

    def update(self, data: dict) -> None:
        """
        批量更新配置（递归合并，而不是完全覆盖）
        """
        self._merge(self._config, data)

    def _merge(self, target: dict, source: dict) -> None:
        """
        递归合并字典：将 source 中的键值对合并到 target 中
        """
        for key, value in source.items():
            if (
                isinstance(value, dict)
                and key in target
                and isinstance(target[key], dict)
            ):
                # 如果值也是字典，递归合并
                self._merge(target[key], value)
            else:
                # 否则直接设置
                target[key] = value

    def __repr__(self) -> str:
        return f"ConfigManager({self.config_path})"

    def __str__(self) -> str:
        return json.dumps(self._config, indent=2, ensure_ascii=False)

    def get_all(self) -> dict:
        """返回完整配置字典"""
        return self._config
    
cm = ConfigManager("D:/program/project/python/AgentQuickStart/config.json")

print(cm.load())
print(cm.save())
print(cm.get(key="db.other.t2.tt2"))

print(cm.set(key="db.other.t3.tt3",value="8888888"))