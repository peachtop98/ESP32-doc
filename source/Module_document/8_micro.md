# 麦克风模块使用说明

```{admonition} 注意：
:class: note
所有类的使用都需要导入库文件：from educator import * 
```

## mic.read() - 读取声音强度

```python
value = mic.read()
```

### 返回值说明

| 返回值范围 | 类型 | 对应电压范围 | 声音强度关系       |
| ---------- | ---- | ------------ | ------------------ |
| 0-4095     | int  | 0-3.3V       | 值越大表示声音越强 |

### 典型应用示例

```python
# 实时声压监测
while True:
    db = mic.read()  # 获取原始ADC值
    print(f"当前声强值: {db}")
    time.sleep(0.1) 
```

------

## 声音特征参考表

| ADC波动范围 | 声音场景 | 典型应用        |
| ----------- | -------- | --------------- |
| ±50         | 安静环境 | 图书馆/夜间监测 |
| 50-300      | 正常谈话 | 语音识别触发    |
| 300-1000    | 乐器演奏 | 音频采集        |
| 1000+       | 尖锐噪音 | 警报检测        |

------

## 使用注意事项

1. 动态基线校准：

```python
# 自动校准环境底噪
def auto_calibrate(duration=3):
    readings = []
    start = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), start) < duration*1000:
        readings.append(mic.read())
        time.sleep_ms(10)
    return sum(readings)//len(readings)
```

2. 波形采集示例：

```python
# 录制1秒音频（44.1kHz采样率需要约44KB内存）
audio_data = []
start = time.ticks_ms()
while time.ticks_diff(time.ticks_ms(), start) < 1000:
    audio_data.append(mic.read())
    time.sleep_us(227)  # 约4.4kHz采样率
```

3. 噪声过滤技巧：

```python
# 数字滤波处理
def noise_filter(raw):
    filtered = 0.8*filtered + 0.2*raw  # 一阶低通滤波
    return int(filtered)
```