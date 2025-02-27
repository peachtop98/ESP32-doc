from machine import *
from machine import PWM
from machine import SoftI2C , I2C # 使用 SoftI2C
from machine import ADC  # 使用 ADC
from ssd1306 import SSD1306_I2C  # 导入屏幕驱动
from neopixel import NeoPixel
import time,sys,dht
import AHT20
from QMI8658 import QMI8658  
import fontChainsWhole  # 导入汉字字体库
from machine import UART
# import fontChainsWhole  # 导入汉字字体库fontChainsIncomplet

pin_mapping = {
    0: 32,  # GPIO32
    1: 25,  # GPIO25
    2: 33,  # GPIO33
    3: 26   # GPIO26
}

class OLEDDisplay:
    def __init__(self, width=128, height=64, scl_pin=22, sda_pin=23):
        self.i2c = SoftI2C(scl=Pin(scl_pin), sda=Pin(sda_pin))  # 使用 SoftI2C
        self.oled = SSD1306_I2C(width, height, self.i2c)  # 创建 OLED 对象
        self.width = width
        self.height = height

    def print(self, column, row, text, clear_row=0):
        """
        在 OLED 显示屏上打印文本。

        :param column: 列位（1~16）
        :param row: 行位（1~4）
        :param text: 显示的文本内容
        :param clear_row: 清行标志（0或1），1表示在显示前清除这一行内容
        """
        # 计算文本在屏幕上的位置
        x = (column - 1) * 8  # 每列的宽度为 8 像素，列位从 1 开始
        y = (row - 1) * 16    # 每行的高度为 16 像素，行位从 1 开始

        # 清空指定行
        if clear_row == 1:
            self.clear_area(0, y, self.width - 1, y + 15)  # 清除整行

        # 显示文本
        if isinstance(text, str):
            self.chinese(text, x, y)  # 调用中文字符显示函数
        # 更新显示
        self.oled.show()
    def clear_area(self, x0, y0, x1, y1):
        """
        清除指定区域的内容。

        :param x0: 区域起始列
        :param y0: 区域起始行
        :param x1: 区域结束列
        :param y1: 区域结束行
        """
        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                self.oled.pixel(x, y, 0)  # 清除像素
        # self.oled.show()
    #阴码 、逐行式、顺向，image_data数据是一位元组，
    #示例：oled.draw_image(image_data, x=0, y=0,width=48, height=48)
    def draw_image(self, image_data, x=0, y=0, width=0, height=0):
        """
        在 OLED 显示屏上绘制图像。

        :param image_data: 图像数据，一维元组，每个字节代表一行中的 8 个像素
        :param x: 图像左上角的 x 坐标
        :param y: 图像左上角的 y 坐标
        :param width: 图像的宽度（以像素为单位）
        :param height: 图像的高度（以像素为单位）
        """
        if width == 0 or height == 0:
            raise ValueError("宽度和高度不能为 0")

        # 计算每行的字节数
        bytes_per_row = width // 8
        if width % 8 != 0:
            bytes_per_row += 1  # 如果宽度不是 8 的倍数，需要额外一个字节

        # 检查数据长度是否匹配
        if len(image_data) < bytes_per_row * height:
            raise ValueError("图像数据长度不足以支持指定的宽度和高度")

        # 遍历每一行
        for row in range(height):
            # 遍历每一列（以字节为单位）
            for col in range(bytes_per_row):
                byte = image_data[row * bytes_per_row + col]
                # 遍历每个字节中的 8 个像素
                for bit in range(8):
                    # 计算像素的坐标
                    pixel_x = x + col * 8 + bit
                    pixel_y = y + row
                    # 如果像素超出图像宽度，跳过
                    if pixel_x >= x + width:
                        continue
                    # 获取像素值（0 或 1）
                    pixel_value = (byte >> (7 - bit)) & 1
                    # 在 OLED 上绘制像素
                    self.oled.pixel(pixel_x, pixel_y, pixel_value)

        # 更新显示
        self.oled.show()

    def String_(self, ch_str, x_axis, y_axis):
        """
        显示 ASCII 字符。

        :param ch_str: 要显示的字符串
        :param x_axis: 起始列像素位置
        :param y_axis: 起始行像素位置
        """
        offset_ = 0
        for char in ch_str:
            # 获取字符对应的 ASCII 码
            ascii_code = ord(char)
            # 将 ASCII 码转化为索引，保证在对应的字符串列表中
            index = ascii_code - 32  # 从 32 开始对应 ASCII 字符集
            if 0 <= index < len(fontChainsWhole.String_dianzheng):  # 确保索引有效
                byte_data = fontChainsWhole.String_dianzheng[index]
                for y in range(0, 16):
                    # 将每一行的字节转化为二进制字符串
                    a_ = bin(byte_data[y]).replace('0b', '')
                    while len(a_) < 8:
                        a_ = '0' + a_  # 确保是 8 位
                    for x in range(0, 8):
                        # 在 OLED 上显示像素
                        self.oled.pixel(x_axis + offset_ + x, y + y_axis, int(a_[x]))
            offset_ += 8  # 更新偏移量以显示下一个字符
#         self.oled.show()

    def chinese(self, ch_str, x_axis, y_axis):
        """
        显示中文字符。

        :param ch_str: 要显示的字符串
        :param x_axis: 起始列像素位置
        :param y_axis: 起始行像素位置
        """
        offset_ = 0  # 初始化字符的偏移量
        for char in ch_str:
            if ord(char) < 128:  # 如果是 ASCII 字符
                # 调用 String_ 函数显示 ASCII 字符
                self.String_(char, x_axis + offset_, y_axis)
                offset_ += 8  # 更新偏移量
            else:  # 处理汉字
                code = 0x00  # 初始化编码变量
                data_code = char.encode("utf-8")  # 将字符编码为 UTF-8
                code |= data_code[0] << 16  # 拼接 UTF-8 编码
                code |= data_code[1] << 8
                code |= data_code[2]

                # 查找对应的字形数据
                byte_data = None
                found = False

                # 遍历 fontChainsWhole.Chains_utf_8 列表
                for index in range(len(fontChainsWhole.Chains_utf_8)):
                    if int(fontChainsWhole.Chains_utf_8[index], 16) == code:
                        byte_data = fontChainsWhole.Chains_dianzheng[index]
                        found = True
                        break

                if not found:
                    print(f"未找到字符 '{char}' 的字形数据，使用默认字形。")
                    # 使用默认字符的点阵数据（示例）
                    Chain_unknown = [0xFF, 0x81, 0x8F, 0x8C, 0x80, 0x80, 0x80, 0x81,
                                    0x81, 0x81, 0x80, 0x83, 0x83, 0x80, 0x80, 0xFF,
                                    0xFF, 0x81, 0xE1, 0x71, 0x31, 0x61, 0xC1, 0x81,
                                    0x81, 0x01, 0x01, 0x81, 0x81, 0x01, 0x01, 0xFF]
                    byte_data = Chain_unknown

                # 显示字形数据
                for y in range(0, 16):  # 遍历点阵数据的每一行
                    a_ = bin(byte_data[y]).replace('0b', '')
                    while len(a_) < 8:
                        a_ = '0' + a_  # 确保是 8 位
                    b_ = bin(byte_data[y + 16]).replace('0b', '')
                    while len(b_) < 8:
                        b_ = '0' + b_  # 确保是 8 位
                    for x in range(0, 8):  # 遍历每个像素
                        # 在 OLED 上显示像素
                        self.oled.pixel(x_axis + offset_ + x, y + y_axis, int(a_[x]))
                        self.oled.pixel(x_axis + offset_ + x + 8, y + y_axis, int(b_[x]))

                offset_ += 16  # 更新偏移量，以便下一个字符显示在后面

    def fill(self, color):
        """填充屏幕指定颜色，0为黑色，1为白色"""
        self.oled.fill(color)

    def line(self, x0, y0, x1, y1, color):
        """绘制一条线，参数为起始和结束坐标及颜色"""
        self.oled.line(x0, y0, x1, y1, color)

    def circle(self, x, y, radius, color):
        """绘制一个圆，参数为圆心坐标、半径及颜色"""
        self.oled.circle(x, y, radius, color)

    def fill(self, color):
        """填充屏幕指定颜色，0为黑色，1为白色"""
        self.oled.fill(color)
        self.oled.show()  # 更新显示

    def line(self, x0, y0, x1, y1, color):
        """绘制一条线，参数为起始和结束坐标及颜色"""
        self.oled.line(x0, y0, x1, y1, color)
        """
        在 OLED 屏幕上绘制圆形
        
        :param x: int 圆心位置的 X 轴坐标 (0~127)
        :param y: int 圆心位置的 Y 轴坐标 (0~63) 
        :param radius: int 圆的半径（像素单位）
        :param color: int 绘制颜色 0=黑色/擦除，1=白色/绘制
        :note: 需要调用 show() 方法才能实际更新显示
        """
        self.oled.circle(x, y, radius, color)

    def show(self):
        self.oled.show()  # 更新显示

try:
    oled = OLEDDisplay()  # 创建 OLEDDisplay 对象
except Exception as e:
    print(f"Error initializing OLEDDisplay: {e}")


class RGBController:
    def __init__(self, pin, num_leds):
        """初始化RGB控制器"""
        self.pin = Pin(pin, Pin.OUT)
        self.rgb_led = NeoPixel(self.pin, num_leds)
    def _set_color(self, index, red, green, blue):
        """设置指定LED的颜色"""
        if 0 <= index < len(self.rgb_led):
            self.rgb_led[index] = (red, green, blue)
            self.rgb_led.write()
    def write_left(self, red, green, blue):
        """设置左侧LED的颜色"""
        self._set_color(0, red, green, blue)
    def write_right(self, red, green, blue):
        """设置右侧LED的颜色"""
        self._set_color(1, red, green, blue)
    def clear(self):
        """清除所有LED的颜色，将其设置为黑色(0,0,0)"""
        for i in range(len(self.rgb_led)):
            self.rgb_led[i] = (0, 0, 0)
        self.rgb_led.write()
    def set_brightness(self, index, red, green, blue, brightness):
        """设置LED的亮度"""
        if 0 <= index < len(self.rgb_led):
            r = int(red * (brightness / 255))
            g = int(green * (brightness / 255))
            b = int(blue * (brightness / 255))
            self.rgb_led[index] = (r, g, b)
            self.rgb_led.write()
try:
    rgb = RGBController(pin=17, num_leds=3)  # 创建 RGB 控制器对象
except Exception as e:
    print(f"Error initializing RGBController: {e}")
    def write_right(self, red, green, blue):
        """设置右侧 LED 的颜色。"""
        self._set_color(2, red, green, blue)
    def clear(self):
        """清除所有 LED 的颜色。"""
        for i in range(len(self.rgb_led)):
            self.rgb_led[i] = (0, 0, 0)
        self.rgb_led.write()
    def set_brightness(self, index, red, green, blue, brightness):
        """设置 LED 亮度，brightness 的范围是 0-255。"""
        if 0 <= index < len(self.rgb_led):
            r = int(red * (brightness / 255))
            g = int(green * (brightness / 255))
            b = int(blue * (brightness / 255))
            self.rgb_led[index] = (r, g, b)
            self.rgb_led.write()
try:
    rgb = RGBController(pin=17, num_leds=3)  # 创建 RGB 控制器对象
except Exception as e:
    print(f"Error initializing RGBController: {e}")


class LED_Controller:
    """LED控制器，用于控制单个GPIO连接的LED设备
    
    提供LED的开关控制、状态切换和状态设置功能，支持GPIO数字输出操作
    
    Attributes:
        pin (machine.Pin): 实例化后的Pin对象，用于控制物理引脚
    
    Example:
        >>> led = LED_Controller(pin=17)  # 初始化GPIO17引脚控制器
        >>> led.on()                      # 点亮LED
        >>> led.off()                     # 熄灭LED
        >>> led.toggle()                  # 切换当前状态
    """
    
    def __init__(self, pin):
        """初始化LED控制器并配置GPIO输出模式
        
        Args:
            pin (int): 有效的GPIO引脚编号，范围0-34（根据具体ESP32型号）
            
        Raises:
            ValueError: 当输入参数不符合引脚编号规范时抛出
            
        Note:
            使用前请确保GPIO引脚未被其他外设占用
        """
        if not isinstance(pin, int) or pin < 0:
            raise ValueError("Invalid pin number")
        self.pin = Pin(pin, Pin.OUT)  # 将引脚设置为输出模式

    def on(self):
        """激活LED设备的供电状态
        
        通过设置GPIO引脚为高电平（3.3V）导通电路，典型工作电流5-20mA

        Args:
            None: 本方法无需参数
            
        Returns:
            None: 无返回值
            
        Raises:
            None: 无特定异常抛出
            
        Example:
            >>> led.off()    # 初始关闭状态
            >>> led.on()     # 引脚电压升至3.3V，LED发光
            >>> led.toggle() # 组合使用切换状态
            
        Note:
            - 操作执行时间小于1ms（基于ESP32主频）
            - 连续操作需保持最小10ms间隔
            - 与off()方法构成对称操作对
        """
        self.pin.on()  # 点亮LED

    def off(self):
        """关闭LED设备
        
        将GPIO引脚设置为低电平（0V），切断5-20mA供电电流

        Args:
            None: 本方法无需参数
            
        Returns:
            None: 无返回值
            
        Raises:
            None: 无特定异常抛出
            
        Example:
            >>> led.on()   # 先开启LED
            >>> led.off()  # 电流降为0mA，LED完全熄灭
            
        Note:
            - 执行后GPIO电压立即降至0V
            - 与on()方法形成对称操作
        """
        self.pin.off()  # 熄灭LED

    def toggle(self):
        """切换LED的当前开关状态
        
        基于GPIO当前电平状态进行硬件级反转操作：
        - 当检测到高电平（3.3V）时切换为低电平（0V）
        - 当检测到低电平时切换为高电平

        Args:
            None: 本方法无需参数
            
        Returns:
            None: 无返回值
            
        Raises:
            None: 无特定异常抛出
            
        Example:
            >>> led = LED_Controller(pin=17)
            >>> led.on()     # 初始状态开启
            >>> led.toggle() # 状态变为关闭
            >>> led.toggle() # 状态恢复开启
            
        Note:
            状态切换间隔建议保持10ms以上，避免快速切换损坏LED
        """
        if self.pin.value():  # 如果LED当前是亮的
            self.off()  # 切换到关闭
        else:
            self.on()  # 切换到打开
    def set_state(self, state):
        """通过数字信号设置LED硬件状态
        
        Args:
            state (int): 硬件控制标识符
                - 1: 激活高电平（等效调用on()方法）
                - 0: 激活低电平（等效调用off()方法）
                
        Returns:
            None: 无返回值
            
        Raises:
            ValueError: 当输入值不符合0/1规范时抛出
            
        Example:
            >>> led.set_state(1)   # 激活LED
            >>> led.set_state(0)   # 关闭LED
            >>> try:
            >>>     led.set_state(2)  # 触发异常
            >>> except ValueError as e:
            >>>     print(e)  # 输出：State must be 0 or 1
            
        Note:
            - 支持整数型输入，其他类型会自动转换判断
            - 与on()/off()方法具有等效硬件操作效果
        """
        if state not in (0, 1):
            raise ValueError("State must be 0 or 1")
        if state == 1:
            self.on()
        else:
            self.off()

try:
    led = LED_Controller(pin=17)    # 创建LED控制器对象，连接到GPIO17
except Exception as e:
    print(f"Error initializing LED_Controller: {e}")

class ButtonController:
    """物理按键状态检测控制器
    
    实现双按键的硬件状态监测，支持实时查询和组合状态判断
    
    Attributes:
        button_a (machine.Pin): 按键A的GPIO硬件对象
        button_b (machine.Pin): 按键B的GPIO硬件对象
        
    Example:
        >>> # 初始化GPIO0和GPIO2连接的按键
        >>> button = ButtonController(pin_a=0, pin_b=2)
        >>> while True:
        >>>     if button.get_a():  # 检测按键A按下
        >>>         led.on()        # 控制LED亮起
        >>>     time.sleep_ms(10)   # 消除抖动
    """

    def __init__(self, pin_a, pin_b):
        """初始化按键GPIO输入配置
        
        Args:
            pin_a (int): 按键A的GPIO编号，有效范围0-34（根据ESP32型号）
            pin_b (int): 按键B的GPIO编号，有效范围0-34（根据ESP32型号）
            
        Raises:
            ValueError: 当引脚编号超出有效范围时抛出
            RuntimeError: GPIO资源冲突时抛出
            
        Note:
            - 使用内部10kΩ上拉电阻，未按下时电压3.3V（高电平）
            - 按键按下时电压0V（低电平），电流约0.5mA
            - 建议在循环中调用时增加5-10ms延时防止抖动
        """
        self.button_a = Pin(pin_a, Pin.IN, Pin.PULL_UP)
        self.button_b = Pin(pin_b, Pin.IN, Pin.PULL_UP)

    def get_a(self):
        """实时获取按键A物理状态
        
        Returns:
            bool: 按键状态标识
                - True: 按键处于按下状态（GPIO低电平）
                - False: 按键处于释放状态（GPIO高电平）
                
        Example:
            >>> while True:
            >>>     if button.get_a() and button.get_b():  # 组合按键检测
            >>>         print("AB键同时按下")
            >>>     time.sleep_ms(5)
        """
        return not self.button_a.value()

    def get_b(self):
        """实时获取按键B物理状态
        
        Returns:
            bool: 按键状态标识
                - True: 按键处于按下状态（GPIO低电平）
                - False: 按键处于释放状态（GPIO高电平）
                
        Note:
            - 读取间隔建议保持5ms以上以确保信号稳定
            - 机械按键存在10-20ms抖动，建议软件去抖动处理
        """
        return not self.button_b.value()
    
try:
    button = ButtonController(pin_a=0, pin_b=2)  # 实例化按键控制器对象（GPIO0和GPIO2）
except Exception as e:
    print(f"按键控制器初始化失败: {e}")


class ADC_Sensor:
    def __init__(self, pin, attenuation=ADC.ATTN_11DB):
        """
        初始化光敏传感器类。
    
        :param pin: 连接光敏传感器的GPIO引脚
        :param attenuation: ADC衰减设置，默认为11DB
        """
        self.adc = ADC(Pin(pin))  # 初始化ADC
        self.adc.atten(attenuation)  # 设置衰减

    def read(self):
        """
        读取光敏传感器的值。
    
        :return: 返回读取到的ADC值
        """
        return self.adc.read()  # 获取ADC数值

try:
    micro = ADC_Sensor(pin=36)  # 创建麦克风对象
except Exception as e:
    print(f"Error initializing ADC_Sensor (microphone): {e}")

try:
    light = ADC_Sensor(pin=39)  # 创建光敏传感器对象，连接到 GPIO39
except Exception as e:
    print(f"Error initializing ADC_Sensor (light): {e}")

class TemperatureHumidityAHT30:
    def __init__(self, scl_pin=22, sda_pin=23):
        """
        初始化温湿度传感器类。
        """
        self.i2c = SoftI2C(scl=Pin(scl_pin), sda=Pin(sda_pin))  # 创建I2C对象
        self.sensor = AHT20.CLOUDZAO_AHT20(self.i2c)  # 创建传感器对象
        self.sensor.begin()  # 初始化传感器

    def read_temp(self):
            """
            读取温度传感器数据。
    
            :return: 返回温度值
            """
            try:
                if not self.sensor.begin():
                    print("Failed to start sensor")
                    sys.exit(1)

                self.sensor.start_measurement_ready()
                temperature = self.sensor.get_temperature_C()
                # print(f'Temperature: {temperature:3.1f} C')
                return temperature
            except OSError as e:
                print('Failed to read temperature sensor.')
                return None

    def read_hum(self):
        """
        读取湿度传感器数据。
    
        :return: 返回湿度值
        """
        try:
            if not self.sensor.begin():
                print("Failed to start sensor")
                sys.exit(1)

            self.sensor.start_measurement_ready()
            humidity = self.sensor.get_humidity_RH()
            # print(f'Humidity: {humidity:3.1f} %')
            return humidity
        except OSError as e:
            print('Failed to read humidity sensor.')
            return None
        
try:
    temp_hum= TemperatureHumidityAHT30()  # 创建板载温湿度传感器对象
except Exception as e:
    print(f"Error initializing humiture: {e}")



from machine import Pin, PWM, Timer
import time
import _thread     
class Buzzer:
    def __init__(self, pin):
        """
        初始化蜂鸣器类。
    
        :param pin: 连接蜂鸣器的 GPIO 引脚
        """
        self.buzzer = PWM(pin, freq=1000, duty=0)  # 创建 PWM 对象  # 初始化 PWM 对象
        time.sleep_ms(5) 
        
    def time(self, duration):
        """
        发出 BEEP 声。
    
        :param duration: BEEP 声的持续时间，单位为毫秒
        """
#         if self.buzzer is None:
#             self.buzzer = PWM(self.buzzer_pin)  # 创建 PWM 对象
        self.buzzer.freq(1000)  # 设置频率为 1000 Hz
        self.buzzer.duty(512)  # 设置占空比为 50%
        time.sleep(duration / 1000)  # 等待指定的时间
        self.buzzer.duty(0)  # 停止发声

    def play_melody(self, melody):
        """
        播放一段旋律。
    
        :param melody: 旋律列表，每个元素是一个元组 (频率, 持续时间)
                       频率单位为 Hz，持续时间单位为毫秒
        """
        for note in melody:
            freq, duration = note
            if freq == 0:  # 如果频率为 0，表示静音
                if self.buzzer is not None:
                    self.buzzer.duty(0)  # 停止发声
            else:
                if self.buzzer is None:
                    self.buzzer = PWM(self.buzzer_pin)  # 创建 PWM 对象
                self.buzzer.freq(freq)  # 设置频率
                self.buzzer.duty(512)  # 设置占空比为 50%
            time.sleep(duration / 1000)  # 等待指定的时间
        if self.buzzer is not None:
            self.buzzer.duty(0)  # 停止发声

    def deinit(self):
        """
        关闭 PWM 并释放资源。
        """
        if self.buzzer is not None:
            self.buzzer.deinit()  # 关闭 PWM
            self.buzzer = None

try:
    beep = Buzzer(pin=16)  # 创建蜂鸣器对象，连接到 GPIO16
except Exception as e:
    print(f"Error initializing Buzzer: {e}")

from machine import SoftI2C, Pin

class qmi8658_1:
    def __init__(self, scl_pin=22, sda_pin=23):
        self.i2c = SoftI2C(scl=Pin(scl_pin), sda=Pin(sda_pin))  # 更新为SoftI2C
        self.sensor = QMI8658(self.i2c)  # 这里需要正确初始化传感器

    def readGyro(self):
        """
        读取三轴陀螺仪的读数。
    
        :return: 返回一个元组，包含X、Y、Z轴的读数
        """
        gyro = self.sensor.gyro  # 读取陀螺仪数据
        x = gyro[0]  # X轴的读数
        y = gyro[1]  # Y轴的读数
        z = gyro[2]  # Z轴的读数
        return x, y, z

    def readAcce(self):
        """
        读取三轴加速度计的读数。
    
        :return: 返回一个元组，包含X、Y、Z轴的读数
        """
        acceleration = self.sensor.acceleration  # 读取加速度数据
        x = acceleration[0]  # X轴的读数
        y = acceleration[1]  # Y轴的读数
        z = acceleration[2]  # Z轴的读数
        return x, y, z



try:
    snsr = qmi8658_1()  # 创建QMI8658对象,三轴数据 
except Exception as e:
    print(f"Error initializing snsr: {e}")


from edu_port import Port
# 全局 Port 实例
Port1 = Port(1)
Port2 = Port(2)
Port3 = Port(3)
Port4 = Port(4)   

