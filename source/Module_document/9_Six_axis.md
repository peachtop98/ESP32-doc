# 六轴传感器模块使用说明

```{admonition} 注意：
:class: note
所有类的使用都需要导入库文件：from educator import * 
```

## 1. six_axis.readGyro() - 读取陀螺仪数据

```python
x, y, z = six_axis.readGyro()
```

### 返回值说明

| 轴   | 类型  | 单位 | 测量范围 | 分辨率    |
| ---- | ----- | ---- | -------- | --------- |
| X    | float | °/s  | ±256dps  | 0.0078°/s |
| Y    | float | °/s  | ±256dps  | 0.0078°/s |
| Z    | float | °/s  | ±256dps  | 0.0078°/s |

### 应用示例

```python
from educator import *  # 导入库文件
import math
# 简易水平仪检测
while True:
    gx, gy, gz = six_axis.readGyro()
    roll = math.atan2(gy, gz) * 180/math.pi
    pitch = math.atan2(-gx, math.sqrt(gy**2 + gz**2)) * 180/math.pi
    print(f"横滚角:{roll:.1f}° 俯仰角:{pitch:.1f}°")
    time.sleep(0.5)

```

------

## 2. six_axis.readAcce() - 读取加速度数据

```python
x, y, z = six_axis.readAcce()
```

### 返回值说明

| 轴   | 类型  | 单位 | 测量范围 | 分辨率   |
| ---- | ----- | ---- | -------- | -------- |
| X    | float | g    | ±8g      | 0.00024g |
| Y    | float | g    | ±8g      | 0.00024g |
| Z    | float | g    | ±8g      | 0.00024g |

### 应用示例

```python
# 检测设备旋转速度
while True:
    ax, ay, az = six_axis.readAcce()
    print(f"角速度 X:{ax:.2f}°/s Y:{ay:.2f}°/s Z:{az:.2f}°/s")
    if abs(az) > 90:  # 检测Z轴旋转
        beep.time(50)  # 快速提示音
    time.sleep(0.1)
```

------

## 技术参数对照表

| 特性     | 陀螺仪      | 加速度计  |
| -------- | ----------- | --------- |
| 量程范围 | ±256°/s     | ±8g       |
| 零偏误差 | ±1°/s       | ±0.02g    |
| 非线性度 | 0.1% FS     | 0.2% FS   |
| 带宽     | 100Hz       | 100Hz     |
| 输出噪声 | 0.01°/s/√Hz | 100μg/√Hz |
| 工作电流 | 3.2mA       | 1.8mA     |

------

## 使用注意事项

1. 冲击检测：

```python
# 检测瞬时冲击（如敲击检测）
threshold = 25  # 25g阈值
history = []

while True:
    ax, ay, az = six_axis.readAcce()
    total = (ax**2 + ay**2 + az**2)**0.5
    history.append(total)
    if len(history) > 5: history.pop(0)
  
    if max(history) > threshold:
        print("检测到冲击！")
        rgb.write_left(255,0,0)  # 红灯警示
```

2. 安装方向校正：

```python
# 根据实际安装方向调整坐标系
def adjust_orientation(ax, ay, az):
    # 假设传感器倒置安装
    return (-ax, -ay, -az)

ax_adj, ay_adj, az_adj = adjust_orientation(*six_axis.readAcce())
```

3. 低功耗模式：

```python
# 运动唤醒功能实现
while True:
    ax, ay, az = six_axis.readAcce()
    if (ax**2 + ay**2 + az**2)**0.5 > 25:  # 25g阈值
        print("检测到运动，唤醒系统！")
        led.on()
        time.sleep(3)  # 保持唤醒10秒
    else:
        led.off()
        time.sleep(0.1)  # 进入低功耗模式
```
