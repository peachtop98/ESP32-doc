# 温湿度传感器模块使用说明

```{admonition} 注意：
:class: note
所有类的使用都需要导入库文件：from educator import * 
```

## 1. temp_hum.read_temp() - 读取温度

```python
temperature = temp_hum.read_temp()
```

### 返回值说明

| 返回值 | 类型     | 单位 | 说明                    |
| ------ | -------- | ---- | ----------------------- |
| 数值   | float    | ℃    | 摄氏温度值（精度0.01℃） |
| None   | NoneType | -    | 读取失败时返回          |

### 典型应用示例

```python
while True:
    # 温度报警系统
    current_temp = temp_hum.read_temp()
    if current_temp is not None and current_temp > 35:
        beep.time(1000)  # 高温报警
        oled.print(1, 1, f"高温:{current_temp:.1f}℃")
```

------

## 2. temp_hum.read_hum() - 读取湿度

```python
humidity = temp_hum.read_hum()
```

### 返回值说明

| 返回值 | 类型     | 单位 | 说明           |
| ------ | -------- | ---- | -------------- |
| 数值   | float    | %RH  | 相对湿度百分比 |
| None   | NoneType | -    | 读取失败时返回 |

### 典型应用示例

```python
while True:
    # 温湿度综合监测
    temp = temp_hum.read_temp()
    hum = temp_hum.read_hum()
    if temp is not None and hum is not None:
        print(f"环境参数: {temp:.1f}℃/{hum:.1f}%")
```

------

## 技术参数

| 项目     | 温度规格      | 湿度规格      |
| -------- | ------------- | ------------- |
| 测量范围 | -40℃ ~ +85℃   | 0% ~ 100% RH  |
| 测量精度 | ±0.3℃ (25℃时) | ±2% RH        |
| 响应时间 | 8秒 (63%变化) | 8秒 (63%变化) |
| 分辨率   | 0.01℃         | 0.024% RH     |
| 采样间隔 | ≥500ms        | ≥500ms        |

------

## 使用注意事项

1. 复合数据采集：

```python
def read_both():
    """同时获取温湿度数据的推荐方法"""
    temp = temp_hum.read_temp()
    hum = temp_hum.read_hum()
    return (temp, hum) if None not in (temp, hum) else (None, None)
while True:
    temp, hum = read_both()
    if temp is not None and hum is not None:
        print(f"当前温度: {temp}°C，当前湿度: {hum}%")
    else:
        print("无法获取温湿度数据，请检查传感器。")
```

2. 异常处理机制：

```python
# 带错误重试的读取
def safe_read(retries=3):
    for _ in range(retries):
        data = (temp_hum.read_temp(), temp_hum.read_hum())
        if None not in data:
            return data
        time.sleep(1)
    return (None, None)
```

3. 数据校准建议：

```python
# 温度补偿示例（工厂校准参数）
CALIBRATION_OFFSET = -0.5  # 根据实际测试调整
calibrated_temp = temp_hum.read_temp() + CALIBRATION_OFFSET
```

4. 环境要求：

- 避免凝结水汽（湿度>80%时需注意）
- 测量时保持空气流通
- 避免阳光直射传感器

5. 典型应用场景：

```python
# 智能温室控制系统
while True:
    t, h = temp_hum.read_temp(), temp_hum.read_hum()
    if t < 10:
        rgb.write_left(0, 0, 255)  # 低温蓝色提示
    elif h > 50:
        rgb.write_left(255, 255, 0)  # 高湿度黄色提示
    else :
        rgb.write_left(0, 0, 0)  # 高湿度黄色提示
    time.sleep(0.5)  
```