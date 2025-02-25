# 六轴传感器模块使用说明

## 1. snsr.readGyro() - 读取陀螺仪数据

```python
x, y, z = snsr.readGyro()
```

### 返回值说明

| 轴   | 类型  | 单位 | 测量范围 | 分辨率    |
| ---- | ----- | ---- | -------- | --------- |
| X    | float | °/s  | ±256dps  | 0.0078°/s |
| Y    | float | °/s  | ±256dps  | 0.0078°/s |
| Z    | float | °/s  | ±256dps  | 0.0078°/s |

### 应用示例

```python
# 检测设备旋转速度
while True:
    gx, gy, gz = snsr.readGyro()
    print(f"角速度 X:{gx:.2f}°/s Y:{gy:.2f}°/s Z:{gz:.2f}°/s")
    if abs(gz) > 90:  # 检测Z轴旋转
        beep.time(50)  # 快速提示音
    time.sleep(0.1)
```

------

## 2. snsr.readAcce() - 读取加速度数据

```python
x, y, z = snsr.readAcce()
```

### 返回值说明

| 轴   | 类型  | 单位 | 测量范围 | 分辨率   |
| ---- | ----- | ---- | -------- | -------- |
| X    | float | g    | ±8g      | 0.00024g |
| Y    | float | g    | ±8g      | 0.00024g |
| Z    | float | g    | ±8g      | 0.00024g |

### 应用示例

```python
# 简易水平仪检测
while True:
    ax, ay, az = snsr.readAcce()
    roll = math.atan2(ay, az) * 180/math.pi
    pitch = math.atan2(-ax, math.sqrt(ay**2 + az**2)) * 180/math.pi
    print(f"横滚角:{roll:.1f}° 俯仰角:{pitch:.1f}°")
    time.sleep(0.5)
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

1. 传感器校准：

```python
# 自动零偏校准（设备静止放置5秒）
def calibrate_gyro():
    samples = []
    for _ in range(100):
        samples.append(snsr.readGyro())
        time.sleep(0.05)
    return [sum(x)/100 for x in zip(*samples)]

gyro_offset = calibrate_gyro()
corrected_gyro = (gx - gyro_offset[0], gy - gyro_offset[1], gz - gyro_offset[2])
```

1. 运动融合算法：

```python
# 互补滤波实现姿态追踪
angle_x = 0
dt = 0.01  # 10ms采样周期

while True:
    ax, ay, az = snsr.readAcce()
    gx, gy, gz = snsr.readGyro()
  
    # 加速度计角度
    acc_angle = math.atan2(ay, az) * 180/math.pi
  
    # 互补滤波
    angle_x = 0.98*(angle_x + gx*dt) + 0.02*acc_angle
    print(f"融合后横滚角: {angle_x:.1f}°")
    time.sleep(dt)
```

1. 冲击检测：

```python
# 检测瞬时冲击（如敲击检测）
threshold = 2.5  # 2.5g阈值
history = []

while True:
    ax, ay, az = snsr.readAcce()
    total = (ax**2 + ay**2 + az**2)**0.5
    history.append(total)
    if len(history) > 5: history.pop(0)
  
    if max(history) > threshold:
        print("检测到冲击！")
        rgb.write_left(255,0,0)  # 红灯警示
```

1. 安装方向校正：

```python
# 根据实际安装方向调整坐标系
def adjust_orientation(ax, ay, az):
    # 假设传感器倒置安装
    return (-ax, -ay, -az)

ax_adj, ay_adj, az_adj = adjust_orientation(*snsr.readAcce())
```

1. 数据可视化：

```python
# 实时波形绘制（需OLED支持）
import oled
oled.init()

while True:
    ax, ay, az = snsr.readAcce()
    # 在OLED上绘制实时波形
    oled.plot_waveform([ax, ay, az], y_range=(-2,2))
```

1. 低功耗模式：

```python
# 运动唤醒功能实现
while True:
    ax, ay, az = snsr.readAcce()
    if (ax**2 + ay**2 + az**2) > 0.1:  # 0.1g阈值
        print("检测到运动，唤醒系统！")
        led.on()
        time.sleep(10)  # 保持唤醒10秒
    else:
        led.off()
        time.sleep(1)  # 进入低功耗模式
```