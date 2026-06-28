### 题目 1：事件系统

# 设计一个简易的事件发布-订阅系统：

# - 定义 `EventEmitter` 类：
#   - `on(event, callback)` 注册事件监听器
#   - `off(event, callback)` 移除指定监听器
#   - `emit(event, *args, **kwargs)` 触发事件，调用所有注册的回调
#   - `once(event, callback)` 注册只触发一次的监听器
#   - `listener_count(event)` 返回某事件的监听器数量

class EventEmitter:
    def __init__(self):
        self._listener = {}  # 可重复注册
        self._once = set()     # 仅触发一次

    def on(self,event, callback):
        if event not in self._listener:
            self._listener[event] = []
        self._listener[event].append(callback)
     
    def off(self,event, callback):
        if event in self._listener:
            self._listener[event].remove(callback)
        
    def emit(self,event, *args, **kwargs):
        if event not in self._listener:
            return
        # 使用copy浅复制
        for callback in self._listener[event].copy():
            callback(*args, **kwargs)
            # id(callback) : 返回对象的唯一标识符（内存地址）
            if id(callback) in self._once:
                self._listener[event].remove(callback)
                self._once.discard(id(callback))

    def once(self,event, callback):
        self.on(event, callback)
        self._once.add(id(callback))

    def listener_count(self,event):
        return len(self._listener.get(event,[]))

# 示例
emitter = EventEmitter()

def greet(name):
    print(f"Hello, {name}!")

emitter.on("join", greet)
emitter.emit("join", "Alice")   # Hello, Alice!
print(emitter.listener_count("join"))  # 1
emitter.off("join", greet)
print(emitter.listener_count("join"))  # 0
