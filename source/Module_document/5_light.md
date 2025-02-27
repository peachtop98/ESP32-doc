# 光敏传感器模块使用说明

```{admonition} 注意：
:class: note
所有类的使用都需要导入库文件：from educator import * 
```

## light.read() - 读取光照强度

```python
value = light.read()
```

### 返回值说明

| 返回值范围 | 类型 | 对应电压范围 | 光照强度关系       |
| ---------- | ---- | ------------ | ------------------ |
| 0-4095     | int  | 0-3.3V       | 值越小表示光照越强 |

### 典型应用示例

```python
# 实时监测光照变化
while True:
    val = light.read()
    print(f"当前光强值: {val}")
    time.sleep(1)

    # 根据光照控制LED
    if light.read() < 1000:  # 环境较暗时
        led.on()
    else:
        led.off()
```

------

## 校准参考表（示例）

| ADC值范围 | 光照强度等级 | 典型场景     |
| --------- | ------------ | ------------ |
| 0 - 500     | 黑暗         | 完全遮蔽     |
| 500 - 1500  | 弱光         | 黄昏/夜灯    |
| 1500 - 3000 | 中等         | 室内灯光     |
| 3000+       | 强光         | 正午阳光直射 |

------

## 使用注意事项

1. 数值处理建议：

```python
while True:
    # 滑动平均滤波（取10次平均值）
    readings = []
    for _ in range(10):
        readings.append(light.read())
        time.sleep(0.01)
    avg = sum(readings) // 10
    print(avg)

```

2. 电压换算公式：

```python
voltage = light.read() * 3.3 / 4095  # 单位：伏特
```

