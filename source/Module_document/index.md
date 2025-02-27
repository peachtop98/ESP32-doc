# 集成模块使用说明

以下是本项目涵盖的主要功能类及其对应的文档链接，你可以根据需求点击相应链接查看详细内容。

- [OLED 类](1_oled.md)：OLED屏幕驱动，支持中英文字符显示、图形绘制及图像渲染功能

- [RGB 类](2_rgb.md)：板载双色RGB灯控制，支持独立颜色设置和亮度调节

- [LED 类](3_led.md)：单色LED基础控制，提供开关/切换/状态设置等基础操作

- [BUTTON 类](4_button.md)：双按键状态检测，支持实时查询按键按压状态

- [LIGHT 类](5_light.md)：光敏传感器，检测环境光照强度

- [TEMP_HUM 类](6_temp_hum.md)：高精度温湿度传感器，获取环境温湿度数据

- [BEEPER 类](7_beep.md)：无源蜂鸣器驱动，支持频率调节和简单旋律播放

- [MIC 类](8_micro.md)：麦克风模块，获取声音强度模拟信号

- [Six_axis 类](9_Six_axis.md)：六轴运动传感器，获取加速度和角速度数据

- [PORT 类](10_Port.md)：通用拓展接口管理，提供了最多4个多功能物理端口配置

    ```{admonition} 注意：
    :class: note
    1. 注意板载只有两个PORT端口，需要接扩展板拓展才有四个PORT端口    
    2. 所有类的使用都需要导入库文件：from educator import * 
    ```

    

```{toctree}
:hidden:
:maxdepth: 4
:caption: 模块文档目录
1_oled
2_rgb
3_led
4_button
5_light
6_temp_hum
7_beep
8_micro
9_Six_axis
10_Port
```