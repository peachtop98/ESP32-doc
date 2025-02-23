# 光敏传感器模块使用说明

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
| 0-500     | 强光         | 正午阳光直射 |
| 500-1500  | 中等         | 室内灯光     |
| 1500-3000 | 弱光         | 黄昏/夜灯    |
| 3000+     | 黑暗         | 完全遮蔽     |

------

## 使用注意事项

1. 硬件连接：
   - 需使用GL5528等光敏电阻模块
   - 模块VCC接3.3V，GND接地，OUT接GPIO39
2. 数值处理建议：

```python
# 滑动平均滤波（取10次平均值）
readings = []
for _ in range(10):
    readings.append(light.read())
    time.sleep(0.01)
avg = sum(readings) // 10
```

1. 电压换算公式：

```python
voltage = light.read() * 3.3 / 4095  # 单位：伏特
```

1. 环境干扰处理：
   - 避免其他光源直射干扰
   - 定期清洁传感器表面
   - 不同颜色物体反射率差异需补偿
2. 特性曲线：
   - 非线性响应（建议实际测试绘制曲线）
   - 响应时间：约20ms（快速变化时需高频采样）