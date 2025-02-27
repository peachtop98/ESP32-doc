# 按键模块方法使用说明

```{admonition} 注意：
:class: note
所有类的使用都需要导入库文件：from educator import * 
```

## 1. button.get_a() - 读取按键A状态

```python
state = button.get_a()
```

### 返回值说明

| 返回值 | 类型 | 说明        |
| ------ | ---- | ----------- |
| True   | bool | 按键A被按下 |
| False  | bool | 按键A未按下 |

### 示例

```python
while True:
    # 检测按键A按下动作
    if button.get_a():
        print("按键A被按下")
        led.on()
    else:
        led.off()
```

------

## 2. button.get_b() - 读取按键B状态

```python
state = button.get_b()
```

### 返回值说明

| 返回值 | 类型 | 说明        |
| ------ | ---- | ----------- |
| True   | bool | 按键B被按下 |
| False  | bool | 按键B未按下 |

### 示例

```python
while True:
    # 双按键组合检测
    if button.get_a() and button.get_b():
        print("AB键同时按下")
        beep.time(1000)  # 触发蜂鸣器
```

------

## 使用注意事项

1. 防抖处理：

```python
# 推荐检测逻辑（50ms防抖）
import time
last_press = 0

while True:
    if button.get_a() and (time.ticks_ms() - last_press) > 50:
        last_press = time.ticks_ms()
        print("有效按键A触发")
    time.sleep_ms(10)
```

2. 异常处理：

```python
try:
    while True:
        print(button.get_a())
except KeyboardInterrupt:
    print("按键检测终止")
```

3. 多任务支持：

```python
# 在_thread中使用的示例
import _thread

def key_monitor():
    while True:
        if button.get_b():
            print("后台检测到B键按下")
        time.sleep(0.1)

_thread.start_new_thread(key_monitor, ())
```