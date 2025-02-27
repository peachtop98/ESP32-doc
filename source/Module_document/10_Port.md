# 多功能端口模块使用说明

```{admonition} 注意：
:class: note
所有类的使用都需要导入库文件：from educator import * 
```

## 全局端口实例

```python
Port1 = Port(1)  # 端口1（GPIO32 & 25）
Port2 = Port(2)  # 端口2（GPIO33 & 26）
Port3 = Port(3)  # 端口3（GPIO18 & 19）
Port4 = Port(4)  # 端口4（GPIO5 & 21）
```

---

## 基础 IO 操作

本小节介绍了`PortX`​对象的两个 IO 控制函数：`output_IO(pin, value)`​用于设置引脚输出高低电平（pin 1-2，value 0/1），可驱动 LED、继电器等设备，驱动能力 12mA/3.3V；`read_IO(pin)`​读取引脚输入状态（返回 0/1），用于按键检测等场景。使用时需注意避免引脚复用冲突，5V 设备需电平转换模块。

### PortX.output\_IO(pin, value)

```python
Port1.output_IO(pin=1, value=1)  # 设置端口1的引脚1输出高电平
```

#### 参数说明

|参数|类型|有效范围|说明|
| -----| ----| --------| --------------|
|pin|int|1-2|端口内引脚编号|
|value|int|0-1|输出电平值|

#### 应用场景

* 控制 LED 灯
* 驱动继电器
* 控制电机使能端
* 数字信号输出

#### 典型示例

```python
# 呼吸灯效果
b, step, interval, direction = 0, 3, 20, 1
max_brightness = 255  # 预定义常量

while True:
    on_time = (b * interval) // 255
    Port1.output_IO(1, 1)
    time.sleep_ms(on_time)
    
    Port1.output_IO(1, 0)
    time.sleep_ms(interval - on_time)
    
    b += step * direction
    if b > max_brightness or b < 0:
        direction = -direction
        b = max(0, min(max_brightness, b))

```

#### 技术参数

|项目|规格|
| --------| --------|
|响应时间|\<1μs|
|驱动能力|12mA|
|输出电压|0-3.3V|
|支持模式|推挽输出|

---

### PortX.read\_IO(pin)

```python
state = Port2.read_IO(pin=2)  # 读取端口2的引脚2输入状态
```

#### 参数说明

|参数|类型|有效范围|默认值|说明|
| ----| ----| --------| ------| --------------|
|pin|int|1-2|1|端口内引脚编号|

#### 返回值

|类型|说明|
| ----| --------------------------------------|
|int|0\=低电平(0-0.8V)\<br\>1\=高电平(2.0-3.3V)|

#### 应用场景

* 按键检测
* 数字传感器状态读取
* 开关量输入检测
* 中断触发源

#### 典型示例

```python
# 按键计数器
count = 0
last_state = 0

while True:
    current = Port3.read_IO(1)
    if current != last_state and current == 0:  # 检测下降沿
        count += 1
        print(f"按键按下次数: {count}")
    last_state = current
    time.sleep(0.05)
```

#### 使用注意事项`

1. **电平转换**：

```python
# 5V设备连接需使用电平转换模块
# 正确连接示意图：
# 外设5V信号 → 电平转换模块 → PortX引脚
#              ↑
#          3.3V供电
```

2. **长线传输**：

```python
# 超过1米的连接线建议：
# - 添加100Ω串联电阻
# - 并联10nF滤波电容
# - 使用双绞线
```

3. **中断优化**：

```python
# 高性能按键检测方案
def btn_callback(pin):
    print(f"Port4 引脚1 触发中断")

Port4._init_pin(1, Pin.IN)  # 初始化引脚为输入模式
# 设置中断，上升沿触发
Port4.pins[1].irq(handler=btn_callback, trigger=Pin.IRQ_RISING)
```

---

## 模拟信号处理

本小节介绍了`PortX.read_ADC(pin)`函数，用于读取端口内模拟输入引脚的电压值（0-3.6V 对应 0-4095 数字量），支持光照强度、电位器、土壤湿度等模拟信号采集。典型应用包括环境监测、传感器数据采集和设备控制（如通过电位器调节 LED 亮度）。使用时需注意 ADC2 通道与 WiFi 功能冲突，建议采用软件滤波、硬件抗干扰措施（如并联电容、屏蔽线）及多通道切换延时优化。函数提供原始值读取和电压换算方法，并支持通过多次采样、线性校准等技术提升测量精度，适用于物联网设备中模拟信号的数字化处理场景。

### PortX.read_ADC(pin) 使用说明

#### 函数原型

```python
adc_value = Port1.read_ADC(pin=1)  # 读取端口1的ADC1引脚
```

#### 参数说明

|参数|类型|有效范围|默认值|说明|
| ----| ----| --------| ------| ----------------------|
|pin|int|1-2|1|端口内模拟输入引脚编号|

#### 返回值

|类型|范围|电压对应关系|
| ----| ------| ---------------------|
|int|0-4095|0 = 0V <br />4095 = 3.6V|

#### 典型应用场景

1. 光照强度传感器（如光敏电阻）
2. 模拟电位器信号采集
3. 土壤湿度传感器
4. 模拟温度传感器
5. 气体浓度检测

#### 使用示例

##### 基础用法

```python
# 读取端口2的ADC2引脚,需要接扩展板的S2
value = Port2.read_ADC(pin=2)
print(f"ADC原始值: {value}, 电压: {value * 3.6 / 4095 :.2f}V")
```

##### 实际应用案例

```python
# 光照强度检测（需接光敏传感器）
def light_level():
    adc_val = Port3.read_ADC(1)
    if adc_val < 1000:
        return "强光"
    elif 1000 <= adc_val < 3000:
        return "中等光照"
    else:
        return "弱光"

# 电位器控制LED亮度（需接可调电阻）
while True:
    pot_val = Port4.read_ADC(2)
    brightness = pot_val // 4  # 转换为0-1023范围
    Port4.output_PWM(1, 1000, brightness)
    time.sleep(0.1)
```

##### 技术参数

|特性|规格说明|
| --------| ------------------------------|
|量程范围|0-3.6V（ATTN\_11DB 模式）|
|分辨率|12-bit（理论精度 0.88mV）|
|采样率|最大 100K samples/s|
|误差范围|±6%（典型值），可通过校准改善|
|输入阻抗|约 100KΩ|

#### 高级使用技巧

##### 软件滤波算法

```python
# 移动平均滤波（10次采样）
def filtered_adc(port, pin):
    samples = []
    for _ in range(10):
        samples.append(port.read_ADC(pin))
        time.sleep_ms(5)
    return sum(sorted(samples)[2:8])//6  # 取中间6个值的平均
```

##### 电压校准方法
三点校准法是一种简单有效的校准方法，它基于这样一个假设：测量系统的输出（如 ADC 读数）与输入电压之间存在线性关系。通过使用标准电压源提供三个不同的已知电压值，并记录对应的 ADC 读数，就可以得到三个校准点
```python
# 三点校准法（需标准电压源）
cal_points = {
    0.5: Port1.read_ADC(1),  # 接0.5V
    2.0: Port1.read_ADC(1),  # 接2.0V
    3.3: Port1.read_ADC(1)   # 接3.3V
}
# 使用线性回归算法计算校准系数
```

##### 注意事项

1. **ADC2 限制**：

```python
# 当使用WiFi功能时，ADC2通道不可用
Port2.read_ADC(1)  
```

2. **多通道切换**：

```python
# 不同ADC通道切换时需要延时
Port1.read_ADC(1)
time.sleep_ms(10)  # 通道切换稳定时间
Port1.read_ADC(2)
```

3. **精度优化**：

```python
# 通过多次采样提升有效位数
def high_res_read(port, pin, times=16):
    return sum(port.read_ADC(pin) for _ in range(times)) // times
```

#### 错误处理

|错误现象|可能原因|解决方案|
| -----------------| -----------------| --------------------------|
|返回值固定为 4095|输入电压超过 3.6V|检查传感器供电电压|
|读数剧烈跳动|电源干扰|增加去耦电容|
|返回 ValueError|引脚配置错误|检查\_PORT\_PIN\_MAPPING 定义|
|ADC 初始化失败|ADC2 与 WiFi 冲突|改用 ADC1 通道或关闭 WiFi|

---

## PWM 控制

### output\_PWM(pin, freq, duty)

**功能**：设置指定引脚的 PWM 波形输出  
**函数定义**：

```python
PortX.output_PWM(pin, freq, duty)
```

**参数说明**：

* `pin`​ (int)：引脚编号，范围 `1`​ 或 `2`​（对应物理端口的两个引脚）
* `freq`​ (int)：PWM 频率（单位：Hz），典型值建议在 50-1000Hz 之间
* `duty`​ (int)：占空比值，范围 `0-1023`​（0 表示 0%，1023 表示 100%）

**特性**：

* 自动初始化 PWM 引脚配置
* 频率范围支持 ESP32 硬件 PWM 的限制（典型 1Hz-40MHz）
* 每次调用会覆盖该引脚之前的 PWM 设置

**示例**：

```python
while True:
    # 渐亮过程
    for duty in range(0, 1024, 4):  # 每次增加4个单位（约0.4%）
        Port1.output_PWM(pin=1, freq=1000, duty=duty)  # 设置真实PWM
        time.sleep_ms(10)
    
    # 渐暗过程
    for duty in range(1023, -1, -4):  # 每次减少4个单位
        Port1.output_PWM(pin=1, freq=1000, duty=duty)
        time.sleep_ms(10)
```

---

### servo\_angle(pin, angle)

**功能**：控制舵机旋转到指定角度  
**函数定义**：

```python
PortX.servo_angle(pin=1, angle=0)
```

**参数说明**：

* `pin`​ (int)：引脚编号，范围 `1`​ 或 `2`​，默认 `1`​
* `angle`​ (int)：目标角度，范围 `0-180`​ 度

**实现特性**：

* 内部自动设置 50Hz 标准舵机频率
* 占空比计算公式：`duty = 26 + (angle/180)*102`​
* 直接对应舵机的标准控制时序（0.5ms-2.5ms脉宽）

**示例**：

```python
# 初始化端口对象（示例为端口2）
# 舵机往复运动（需在循环中执行）
for ang in [0, 90, 180, 90]:
    Port2.servo_angle(pin=1, angle=ang)
    time.sleep(1)

```

---

### 注意事项

1. **硬件限制**：

    * 同一端口的两个引脚可独立输出不同 PWM 信号
    * 不同端口之间没有频率同步机制
2. **典型应用**：

    * `output_PWM`​：LED亮度调节、直流电机调速
    * `servo_angle`​：标准舵机位置控制
3. **错误处理**：

    * 输入超出范围的参数会抛出 `ValueError`​
    * 舵机角度参数超过 0-180 会立即报错
4. **硬件准备**：

    * 舵机需连接至对应端口的引脚1或2
    * 建议外接独立电源供电大功率负载


---

## 传感器模块

本小节介绍了三个用于传感器数据读取及距离测量的函数，它们可用于教学实验指导或供开发者参考。`DHT11(pin = 1)`​函数能读取 DHT11 温湿度传感器的温湿度，自动初始化引脚并检测硬件连接，响应时间约 2 秒，通过`pin`​参数选引脚，返回温湿度元组，读取失败返回`(None, None)`​；`read_DS18B20(pin = 1)`​函数读取 DS18B20 温度传感器的温度值，支持单总线多设备（仅读首个） ，通过`pin`​选引脚，读取失败返回`None`​；`get_distance()`​函数用于超声波模块测距，测距范围 2cm - 400cm，无参数，测量失败返回`None`​。

### DHT11(pin=1)

**功能**：读取 DHT11 温湿度传感器的温度和湿度  
**函数定义**：

```python
temp, humidity = PortX.DHT11(pin=1)
```

**参数说明**：

* `pin`​ (int)：传感器连接的引脚编号 `1`​ 或 `2`​，默认 `1`​

**返回值**：

* 元组 `(temperature, humidity)`​，单位分别为摄氏度和百分比
* 读取失败时返回 `(None, None)`​

**特性**：

* 自动初始化传感器引脚
* 自带硬件连接检测
* 典型响应时间约 2 秒

**示例**：

```python
#传感器接到端口4
temp, hum = Port4.DHT11()
if temp is not None:
    print(f"温度: {temp}℃  湿度: {hum}%")

# 循环监测（间隔需大于2秒）
while True:
    print(Port4.DHT11(pin=1))
    time.sleep(3)
```

---

### read\_DS18B20(pin=1)

**功能**：读取 DS18B20 温度传感器的温度值  
**函数定义**：

```python
temperature = PortX.read_DS18B20(pin=1)
```

**参数说明**：

* `pin`​ (int)：传感器连接的引脚编号 `1`​ 或 `2`​，默认 `1`​

**返回值**：

* 浮点型温度值（摄氏度），读取失败返回 `None`​

**特性**：

* 支持单总线多设备（但当前实现仅读取第一个设备）
* 测量范围 -55℃ \~ +125℃
* ±0.5℃ 精度（-10℃ \~ +85℃）

**示例**：

```python
# DS18B20 接在端口2
# 单次读取
temp = Port2.read_DS18B20()
print(f"当前温度：{temp:.1f}℃")

# 温度监控
while True:
    print(Port2.read_DS18B20(pin=2))  # 指定引脚2
    time.sleep(1)
```

---

### get\_distance()

**功能**：超声波模块测距  
**函数定义**：

```python
distance = PortX.get_distance()
```

**参数**：无

**返回值**：

* 浮点型距离值（厘米），测量失败返回 `None`​

**技术规格**：

* 有效测距范围：2cm \~ 400cm
* 测量角度：\<15°
* 响应时间：约 60ms

**示例**：

```python
# 超声波接在端口3

# 单次测距
dist = Port3.get_distance()
if dist:
    print(f"距离：{dist}cm")

# 连续测距（推荐间隔 >0.1s）
while True:
    print(Port3.get_distance())
    time.sleep(0.2)
```

---

### 综合应用示例

```python
# 环境监测装置（端口4接DHT11，端口2接超声波）

while True:
    # 读取温湿度
    temp, hum = Port4.DHT11()
  
    # 读取障碍物距离
    distance = Port2.get_distance()
  
    # 数据展示
    print(f"温度: {temp}℃ | 湿度: {hum}% | 前方障碍: {distance}cm")
    time.sleep(0.5)
```

---

### 注意事项

1. **典型错误值**：

    * DHT11 返回 (None, None)：引脚接触不良
    * DS18B20 返回 None：总线无设备
    * 超声波返回 0.0：超出测量范围

---

该文档可直接用于教学实验指导或开发者参考，实际应用时需结合具体硬件连接情况。

---

## RFID 模块

本小节介绍了`PortX.read_RFID()`​函数，用于物联网应用开发参考，实际部署建议结合加密验证机制增强安全性。此函数能读取符合 ISO/IEC 14443 协议 13.56MHz 频段 RFID 卡片的唯一标识符（UUID），工作频率 13.56MHz ，有效读取距离 3 - 5cm（因卡片类型而异），响应时间小于 100ms ，返回 4 字节或 7 字节 UID 的十六进制字节序列，未检测到卡片或读取失败返回`None`​。文档给出基础用法、持续监测、门禁系统、校园一卡通、智能储物柜等使用示例，涵盖硬件配置要求（使用引脚 1、2 ，外接 3.3V 电源，避免金属遮挡天线）、错误处理指南、性能优化建议（读取间隔≥200ms ，防多卡冲突，注意环境影响）等注意事项，还列举 MIFARE Classic、NTAG21x、DESFire 等兼容卡片类型。

### PortX.read\_RFID() 使用说明


#### 功能描述

读取 RFID 卡片的唯一标识符（UUID），支持 ISO/IEC 14443 协议的 13.56MHz 频段卡片。

---

#### 函数定义

```python
uuid_bytes = PortX.read_RFID()
```

---

#### 技术参数

|参数项|规格说明|
| --------------| -----------------------------|
|工作频率|13.56MHz|
|有效读取距离|3-5cm（视卡片类型）|
|响应时间|\<100ms|
|数据格式|4字节或7字节UID（十六进制）|

---

#### 使用示例

**基础用法**：

```python
# 初始化端口（RFID 模块接在端口2）
card_id = Port2.read_RFID()
if card_id is not None:
    print("检测到卡片 UUID:", card_id.hex())
else:
    print(f"Port{Port2.port_id} 未读取到 RFID 卡")
```

**持续监测**：

```python
while True:
    uid = Port2.read_RFID()
    if uid:
        print(f"[{time.localtime()}] 刷卡记录: {uid.hex()}")
    time.sleep(0.5)  # 防止高频读取
```

**门禁系统应用**：

```python
valid_cards = {
    b'\x12\x34\x56\x78': "管理员卡",
    b'\x9a\xbc\xde\xf0': "学生卡01",
    b'\x43\x85\xd5\x10': "学生卡02",
}

while True:
    uid = Port2.read_RFID()
    if uid:
        # 将 bytearray 转换为 bytes 类型
        uid = bytes(uid)
        if uid in valid_cards:
            print(f"欢迎 {valid_cards[uid]} 用户")
            # 触发开门动作
            Port1.output_IO(pin=1, value=1)
            time.sleep(3)
            Port1.output_IO(pin=1, value=0)
```

---

#### 返回值说明

|返回值类型|说明|示例|
| ------------| -----------------------| -------------------------------------|
|bytearray|卡片 UUID 的字节序列|bytearray(b'C\x85\xd5\x10')|
|None|未检测到卡片/读取失败|None|


---

#### 注意事项


1. **错误处理指南**

```python
try:
    uid = Port2.read_RFID()
    if not uid:
        print("请将卡片靠近读卡器")
    elif len(uid) not in [4,7]:
        print("异常卡片格式")
except Exception as e:
    print("RFID 系统故障:", str(e))
```

2. **性能优化建议**

    * 读取间隔建议 ≥200ms
    * 多卡片同时出现时可能发生冲突
    * 高温高湿环境可能影响读取距离

---

该文档可直接用于物联网应用开发参考，实际部署时建议结合加密验证机制增强安全性。

---

## MP3 子模块

该文档介绍了 ACB_MP3 子类通过`PortX.init_mp3()`初始化后，可实现播放控制（`play()`/`pause()`/`nextTrack()`/`previousTrack()`）、音量调节（`setVolume(0-30)`）、文件夹播放（`playInFolder(01-99)`）及状态查询（`getPlayState()`）功能，支持 UART 9600bps 通信和 FAT32 格式 TF 卡，典型应用如控制台交互音乐播放器。



#### 1. 模块初始化

```python
# 必须通过 Port 实例调用
mp3 = PortX.init_mp3()  # PortX 需实例化为具体端口号（如 Port2）
```


#### 2. play()

**功能**：开始播放音频  
**协议**：发送 `7E 03 11 12 EF`​ 十六进制指令  
**示例**：

```python
mp3 = Port2.init_mp3()
mp3.play()  # 立即开始播放
```

#### 3. pause()

**功能**：暂停当前播放  
**协议**：发送 `7E 03 12 11 EF`​  
**示例**：

```python
mp3 = Port2.init_mp3()
mp3.play()  # 立即开始播放
time.sleep(2)
mp3.pause()  # 暂停播放
```

#### 4. nextTrack()

**功能**：切换至下一曲目  
**注意**：在循环播放模式下会跳转至列表末尾
**示例**：

```python
mp3 = Port2.init_mp3()
mp3.play()  # 立即开始播放
time.sleep(2)
mp3.nextTrack()  # 切换至下一曲目
```

#### 5. previousTrack()

**功能**：返回上一曲目  
**限制**：不支持播放历史回溯
**示例**：

```python
mp3 = Port2.init_mp3()
mp3.play()  # 立即开始播放
time.sleep(2)
mp3.previousTrack()  # 返回上一曲目
```

---

### 高级控制函数

#### 6. setVolume(volume)

**参数**：

* `volume`​ (int)：0-30 级音量控制（0\=静音，30\=最大）

**示例**：

```python
mp3 = Port2.init_mp3()
mp3.play()  # 立即开始播放
time.sleep(0.05)  # 延时等待模块响应
mp3.setVolume(5)  # 设置音量
time.sleep(3)
mp3.setVolume(20)  # 设置音量
time.sleep(3)
mp3.setVolume(30)  # 设置音量
```

#### 7. playInFolder(folder\_num , music\_num)

**参数**：

* `folder_num`​ (int)：01-99 文件夹编号（需SD卡预存对应文件夹）
* `music_num`​ (int)：01-255 文件夹内第几首歌曲
**文件要求**：

* 文件夹命名格式：`01`​-`99`​
* 音频文件命名：001XXX.MP3-255XXX.MP3，XXX 可以为中文也可以没有，否则会出错无法播放。
**使用示例**：

```python
mp3 = Port2.init_mp3()
mp3.playInFolder(02,03)  # 播放SD卡中02文件夹下的003 xx.mp3
```

#### 8. getPlayState()

**功能**：获取模块状态并解析  
**返回值**：无，直接打印状态信息  
**响应解析**：

* 当前播放状态: 播放中
* 当前播放状态: 暂停
* 当前播放状态: 停止

**使用示例**：

```python
mp3 = Port2.init_mp3()
mp3.play()  # 立即开始播放
time.sleep(0.1)
mp3.getPlayState()
# 控制台输出：当前播放状态: 播放中
```

---

### 技术参数表

|功能项|协议延迟|数据校验方式|硬件要求|
| ------------| ----------| --------------| ---------------------|
|播放控制|50-100ms|异或校验|UART 波特率 9600bps|
|音量调节|80ms|字节累加|支持 TF 卡 ≤32GB|
|文件夹播放|200ms|多项式校验|FAT32 文件系统|
|状态查询|150ms|无|RX/TX 需电平匹配|

---


## 技术参数对照表

|功能|采样率|响应时间|功耗|
| ------| ------| --------| -----|
|ADC|1kHz|\<1ms|0.1mA|
|PWM|40kHz|立即响应|5mA|
|DHT11|0.5Hz|2s|2.5mA|
|超声波|10Hz|60ms|15mA|

---

