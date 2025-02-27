# LED 模块方法使用说明
```{admonition} 注意：
:class: note
所有类的使用都需要导入库文件：from educator import * 
```
## 1. led.on() - 开启LED
```python
led.on()
```

### 功能说明

- 立即点亮连接的LED
- 无需任何参数
- 无返回值

### 示例

```
# 点亮LED
led.on()
```

------

## 2. led.off() - 关闭LED

```
led.off()
```

### 功能说明

- 立即熄灭连接的LED
- 无需任何参数
- 无返回值

### 示例

```
# 关闭LED
led.off()
```

------

## 3. led.toggle() - 切换状态

```
led.toggle()
```

### 功能说明

- 自动反转当前状态（亮→灭 / 灭→亮）
- 无需参数
- 无返回值

### 示例

```
# 创建闪烁效果
for _ in range(5):
    led.toggle()
    time.sleep(0.5)
```

------

## 4. led.set_state() - 状态设置

```
led.set_state(state)
```

### 参数说明

| 参数  | 类型 | 允许值 | 说明           |
| :---- | :--- | :----- | :------------- |
| state | int  | 0 或 1 | 0=关闭，1=开启 |

### 异常说明

| 异常类型   | 触发条件          |
| :--------- | :---------------- |
| ValueError | 输入非0/1值时抛出 |

### 示例

```
# 根据条件控制LED
if temperature > 30:
    led.set_state(1)  # 高温报警
else:
    led.set_state(0)
```

------

## 使用注意事项

1. **状态反馈**：

   - 可通过`led.pin.value()`读取当前状态
   - 返回1表示点亮，0表示熄灭

2. **异常处理**：

   ```
   try:
       led.set_state(2)  # 错误值
   except ValueError as e:
       print("错误：", e)
   ```