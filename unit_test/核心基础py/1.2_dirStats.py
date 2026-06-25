# ### 目录统计工具

# 使用 `pathlib` 编写类 `DirStats`：

# - `__init__(self, dir_path)` 接收目录路径字符串
# - `total_files()` 返回该目录下所有文件数量（递归）
# - `files_by_extension()` 返回字典，按扩展名统计文件数量（如 `{"py": 5, "md": 3}`）
# - `largest_file()` 返回最大文件的路径和大小（元组），目录为空返回 `None`
# - `find_files(pattern)` 使用 glob 查找匹配模式的文件列表

from pathlib import Path

class DirStats:
    def __init__(self, dir_path):
        self.dir = Path(dir_path)

    def __post_init__(self):
        pass

    def total_files(self):
        return sum(1 for p in self.dir.rglob("*") if p.is_file())

    def files_by_extension(self):
        dt = {}
        for p in self.dir.rglob("*"):
            if p.is_file():
                ext = p.suffix.lstrip(".") or "no_ext"
                dt[ext] = dt.get(ext,0) + 1
        return dt

    def largest_file(self):
        fileList = [p for p in self.dir.rglob("*") if p.is_file()]
        if not fileList:
            return None
        
        largeFile = max(fileList,key=lambda fl:fl.stat().st_size)
        return (largeFile,largeFile.stat().st_size)
        
        # largeFile = sorted(fileList,key=lambda fl:fl.stat().st_size,reverse=True)
        # return (largeFile[0],largeFile[0].stat().st_size)

    def find_files(self,pattern):
        return list(self.dir.glob(pattern))
        

stats = DirStats("D:/program/project/python/AgentQuickStart")
print("total_files:",stats.total_files())           # 42
print("files_by_extension:",stats.files_by_extension())    # {"py": 10, "md": 5, ...}
print("largest_file:",stats.largest_file())          # (PosixPath('/path/to/big.py'), 15234)

print("find_files:",stats.find_files("*test.md"))