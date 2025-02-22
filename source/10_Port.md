# 多功能端口模块使用说明

## 全局端口实例

```python
Port1 = Port(1)  # 端口1（GPIO32 & 25）
Port2 = Port(2)  # 端口2（GPIO33 & 26）
Port3 = Port(3)  # 端口3（GPIO18 & 19）
Port4 = Port(4)  # 端口4（GPIO5 & 21）
```

------

## 基础IO操作

### PortX.output_IO(pin, value)

```python
Port1.output_IO(pin=1, value=1)  # 设置端口1的引脚1输出高电平
```

| 参数  | 类型 | 有效范围 | 说明           |
| ----- | ---- | -------- | -------------- |
| pin   | int  | 1-2      | 端口内引脚编号 |
| value | int  | 0-1      | 输出电平值     |

------

### PortX.read_IO(pin)

```python
state = Port2.read_IO(pin=2)  # 读取端口2的引脚2输入状态
```

| 返回值 | 类型 | 说明         |
| ------ | ---- | ------------ |
| 0/1    | int  | 引脚电平状态 |

------

## 模拟信号处理

### PortX.read_ADC(pin)

```python
adc_val = Port3.read_ADC(pin=1)  # 读取端口3引脚1的ADC值(0-4095)
```

| 参数 | 类型 | 有效范围 | 说明        |
| ---- | ---- | -------- | ----------- |
| pin  | int  | 1-2      | ADC引脚编号 |

------

## PWM控制

### PortX.output_PWM(pin, freq, duty)

```python
Port4.output_PWM(pin=2, freq=1000, duty=512)  # 1kHz频率，50%占空比
```

| 参数 | 类型 | 有效范围 | 说明     |
| ---- | ---- | -------- | -------- |
| pin  | int  | 1-2      | PWM引脚  |
| freq | int  | 1-40000  | 频率(Hz) |
| duty | int  | 0-1023   | 占空比   |

------

### PortX.servo_angle(pin, angle)

```python
Port1.servo_angle(pin=1, angle=90)  # 设置舵机到90度位置
```

| 参数  | 类型 | 有效范围 | 说明     |
| ----- | ---- | -------- | -------- |
| angle | int  | 0-180    | 舵机角度 |

------

## 传感器模块

### PortX.DHT11(pin)

```python
temp, humi = Port2.DHT11(pin=1)  # 读取温湿度
```

| 返回值 | 类型  | 说明       |
| ------ | ----- | ---------- |
| temp   | float | 摄氏度     |
| humi   | float | 湿度百分比 |

------

### PortX.read_DS18B20(pin)

```python
temp = Port3.read_DS18B20(pin=2)  # 读取DS18B20温度
```

| 返回值 | 类型  | 精度   |
| ------ | ----- | ------ |
| temp   | float | ±0.5°C |

------

### PortX.get_distance()

```python
distance = Port4.get_distance()  # 超声波测距（单位：厘米）
```

| 有效范围 | 精度 | 最大量程 |
| -------- | ---- | -------- |
| 2-400cm  | ±1cm | 4m       |

------

## RFID模块

### PortX.read_RFID()

```python
uid = Port1.read_RFID()  # 读取卡片UID，如[0x12, 0x34, 0x56, 0x78]
```

| 返回值 | 类型 | 说明     |
| ------ | ---- | -------- |
| uid    | list | 4字节UID |

------

## MP3子模块

### PortX.init_mp3() 方法列表

```python
mp3 = Port2.init_mp3()  # 初始化后调用以下方法：
```

| 方法                 | 参数 | 说明           |
| -------------------- | ---- | -------------- |
| play()               | 无   | 开始播放       |
| pause()              | 无   | 暂停播放       |
| nextTrack()          | 无   | 下一曲         |
| previousTrack()      | 无   | 上一曲         |
| setVolume(vol)       | 0-30 | 音量设置       |
| playInFolder(folder) | 1-99 | 播放指定文件夹 |

示例：

```python
mp3 = Port3.init_mp3()
mp3.setVolume(20)
mp3.playInFolder(5)  # 播放第5文件夹内容
```

------

## 技术参数对照表

| 功能   | 采样率 | 响应时间 | 功耗  |
| ------ | ------ | -------- | ----- |
| ADC    | 1kHz   | <1ms     | 0.1mA |
| PWM    | 40kHz  | 立即响应 | 5mA   |
| DHT11  | 0.5Hz  | 2s       | 2.5mA |
| 超声波 | 10Hz   | 60ms     | 15mA  |

------

## 使用注意事项

1. 引脚冲突：

```python
# ADC2与WiFi冲突示例
Port2.read_ADC(1)  # GPIO33属于ADC2，启用WiFi时不可用
```

1. PWM限制：

```python
# 同时最多使用8路PWM
Port1.output_PWM(1,1000,512)
Port2.output_PWM(2,2000,256)  # 不同端口不冲突
```

1. 传感器供电：

```python
# 给传感器模块供电示例
Port4.output_IO(1,1)  # 引脚1作为电源控制
time.sleep(0.1)       # 等待传感器上电
distance = Port4.get_distance()
```

1. 多设备协同：

```python
# RFID与MP3协同工作
while True:
    if Port1.read_RFID():
        Port1.init_mp3().play()
        break
```

1. 滤波算法：

```python
# ADC滑动平均滤波
samples = [Port3.read_ADC(1) for _ in range(10)]
avg = sum(samples) // len(samples)
```

1. 异常处理：

```python
try:
    Port2.servo_angle(1, 95)
except ValueError as e:
    print("角度超限，自动修正到90度")
    Port2.servo_angle(1, 90)
```