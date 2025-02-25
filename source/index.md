# 欢迎来到基于 ESP32 芯片项目的 Sphinx 文档

本项目以 ESP32 芯片为核心进行开发，此文档将为你详细介绍项目中各类功能模块的使用方法和相关信息，是你深入了解和使用本项目的重要指引。

## 目录概览

以下是本项目涵盖的主要功能类及其对应的文档链接，你可以根据需求点击相应链接查看详细内容。

### 显示与照明类
- [OLED 类](Module_document/1_oled.md)：详细介绍 OLED 显示屏的控制和使用方法，助你实现清晰的信息显示。
- [RGB 类](Module_document/2_rgb.md)：了解如何操控 RGB 灯，通过不同颜色组合营造多样化的视觉效果。
- [LED 类](Module_document/3_led.md)：掌握普通 LED 灯的控制逻辑，实现基本的照明和信号指示功能。

### 交互输入类
- [BUTTON 类](Module_document/4_button.md)：学习按钮的使用和事件处理，为项目添加用户交互功能。
- [MICRO 类](Module_document/8_micro.md)：介绍麦克风的应用，可用于语音采集和相关处理。

### 传感器类
- [LIGHTB 类](Module_document/5_light.md)：深入了解光照传感器的工作原理和数据读取方法，用于环境光照监测。
- [TEMP_HUM 类](Module_document/6_temp_hum.md)：掌握温湿度传感器的使用，实时获取环境的温度和湿度信息。
- [Six_axis 类](Module_document/9_Six_axis.md)：这里涵盖了其他通用传感器的相关内容，满足多样化的传感需求。

### 输出与报警类
- [BEEP 类](Module_document/7_beep.md)：了解蜂鸣器的控制方式，实现声音提示和报警功能。

### 端口与模块类
- [PORT 类](Module_document/10_Port.md)：详细说明通用端口的配置和使用，为设备间的连接和通信提供支持。


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