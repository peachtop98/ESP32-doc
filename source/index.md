# 欢迎来到基于 ESP32 芯片项目的文档

本项目以 ESP32 芯片为核心进行开发，此文档将为你详细介绍项目中各类功能模块的使用方法和相关信息，是你深入了解和使用本项目的重要指引。

## 硬件驱动指南

### 显示控制
- [OLED 显示屏](Module_document/1_oled.md) - 支持中英文字符显示、图形绘制及图像渲染
- [RGB 灯带](Module_document/2_rgb.md) - 全彩灯光控制，支持独立颜色设置和亮度调节
- [LED 指示灯](Module_document/3_led.md) - 单色LED基础控制（开关/切换/状态设置）

### 输入设备
- [按钮模块](Module_document/4_button.md) - 支持双按键状态检测与事件处理
- [麦克风模块](Module_document/8_micro.md) - 音频信号采集与强度检测

### 环境感知
- [光照传感器](Module_document/5_light.md) - 0-4095级光强检测（ADC采集）
- [温湿度传感器](Module_document/6_temp_hum.md) - 高精度气候参数监测（I2C协议）
- [六轴传感器](Module_document/9_Six_axis.md) - 加速度/角速度三维运动检测

### 输出控制
- [蜂鸣器模块](Module_document/7_beep.md) - 无源蜂鸣器频率控制与旋律播放

### 系统接口
- [通用端口](Module_document/10_Port.md) - 多功能物理端口配置（支持GPIO/ADC/PWM/UART）


---

## 应用案例

### 基础实验
- [灯光控制](code/灯的控制/index.md) - 按键触发RGB灯光状态切换（GPIO输入/输出基础）
- [音频采集系统](code/扩音系统/index.md) - 麦克风信号放大与ADC采样（模拟信号处理）

### 自动控制
- [智能恒温箱](code/恒温箱实验/index.md) - 温度控制与执行器驱动（闭环控制实现）
- [定时加湿器](code/定时加湿系统/index.md) - 基于RTC的定时任务调度（时间驱动逻辑）

### 物联网应用
- [农场监测平台](code/校园农场/index.md) - 多传感器数据融合（温湿度/光照/土壤监测）
- [云端光照系统](code/智能光照系统_MQTT/index.md) - IoT远程控制（MQTT协议实践）
- [智能加湿系统](code/智能加湿系统/index.md) - 湿度阈值自动调节（条件触发机制）


---


## 开发资源
- [MicroPython API](http://micropython.com.cn) - 核心编程接口参考
- [硬件驱动手册](Module_document/index.md) - 模块方法详解
- [实验案例库](code/index.md) - 分级教学项目
- [常见问题索引](faq/index.rst) - 故障排查指南


```{toctree}
:hidden:
:maxdepth: 2

Module_document/index
```

```{toctree}
:hidden:
:maxdepth: 2
 
code/index
```

```{toctree}
:hidden:
:maxdepth: 2

faq/index
```




如需进一步的学习资源，你可以参考 [MicroPython 官方文档](http://micropython.com.cn/en/latet/index-2.html)，这里有丰富的知识和示例供你探索。希望本文档能帮助你顺利开展基于 ESP32 芯片的开发工作！ 