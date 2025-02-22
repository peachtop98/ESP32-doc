# 麦克风模块使用说明

## micro.read() - 读取声音强度

```python
value = micro.read()
```

### 返回值说明

| 返回值范围 | 类型 | 对应电压范围 | 声音强度关系       |
| ---------- | ---- | ------------ | ------------------ |
| 0-4095     | int  | 0-3.3V       | 值越大表示声音越强 |

### 典型应用示例

```python
# 实时声压监测
while True:
    db = micro.read()  # 获取原始ADC值
    print(f"当前声强值: {db}")
    time.sleep(0.1)

# 声控LED开关
base = micro.read()    # 获取环境底噪
while True:
    if abs(micro.read() - base) > 500:  # 检测显著声音变化
        led.toggle()
        time.sleep(0.5)
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

1. 信号处理建议：

```python
# 快速傅里叶变换采样（需导入FFT库）
import ulab.numpy as np
samples = [micro.read() for _ in range(256)]
fft_result = np.fft.fft(samples)
```

2. 动态基线校准：

```python
# 自动校准环境底噪
def auto_calibrate(duration=3):
    readings = []
    start = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), start) < duration*1000:
        readings.append(micro.read())
        time.sleep_ms(10)
    return sum(readings)//len(readings)
```

3. 电气特性：

- 采样频率：最高6kHz
- 信噪比：≥60dB
- 频率响应：20Hz-20kHz (±3dB)

4. 波形采集示例：

```python
# 录制1秒音频（44.1kHz采样率需要约44KB内存）
audio_data = []
start = time.ticks_ms()
while time.ticks_diff(time.ticks_ms(), start) < 1000:
    audio_data.append(micro.read())
    time.sleep_us(227)  # 约4.4kHz采样率
```

5. 噪声过滤技巧：

```python
# 数字滤波处理
def noise_filter(raw):
    filtered = 0.8*filtered + 0.2*raw  # 一阶低通滤波
    return int(filtered)
```