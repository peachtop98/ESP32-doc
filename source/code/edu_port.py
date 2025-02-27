
from machine import Pin, ADC, SoftI2C, UART, PWM
import time, mfrc522_i2c
import dht
from onewire import OneWire
from ds18x20 import DS18X20


# 基于端口号的单例模式
class Port:
    _instances = {}  # 单例实例存储
    # 类级别常量：端口引脚映射（端口号: {引脚1编号, 引脚2编号}）
    _PORT_PIN_MAPPING = {
        1: {1: 32, 2: 25},   # 端口1
        2: {1: 33, 2: 26},   # 端口2
        3: {1: 18, 2: 19},    # 端口3
        4: {1: 5, 2: 21}    # 端口4
    }
    def __new__(cls, port_id):
        """单例模式，确保每个端口唯一实例"""
        if port_id not in cls._instances:
            if port_id not in cls._PORT_PIN_MAPPING:
                raise ValueError(f"port_id 必须是 {list(cls._PORT_PIN_MAPPING.keys())} 中的一个")
            cls._instances[port_id] = super().__new__(cls)
            cls._instances[port_id]._initialized = False
        return cls._instances[port_id]

    def __init__(self, port_id):
        if not self._initialized:
            self.port_id = port_id
            self.pins = {}        # GPIO 引脚
            self.adc_pins = {}    # ADC 引脚
            self.pwm_pins = {}    # PWM 引脚
            self.dht11 = None
            self.ultrasonic_trig = None
            self.ultrasonic_echo = None
            self._initialized = True

    def _cleanup_pin(self, pin):
        """
        清理指定引脚的配置。
        """
        if pin in self.pins:
            del self.pins[pin]
        if pin in self.adc_pins:
            del self.adc_pins[pin]
        if pin in self.pwm_pins:
            self.pwm_pins[pin].deinit()  # 关闭 PWM
            del self.pwm_pins[pin]

    #--------------------------------------------------
    # 工具方法：获取当前端口的引脚映射
    #--------------------------------------------------
    def _get_pin_mapping(self):
        """返回当前端口的引脚映射字典"""
        return self._PORT_PIN_MAPPING[self.port_id]

    #--------------------------------------------------
    # 通用引脚初始化逻辑（供 GPIO/ADC/PWM 共用）
    #--------------------------------------------------
    def _init_pin(self, pin, mode):
        pin_mapping = self._get_pin_mapping()
        if pin not in pin_mapping:
            raise ValueError(f"pin 必须是 {list(pin_mapping.keys())} 中的一个")

        pin_number = pin_mapping[pin]
        if pin not in self.pins:
            self._cleanup_pin(pin) # 清理引脚配置
            if mode == Pin.OUT:
                self.pins[pin] = Pin(pin_number, Pin.OUT) # 输出模式
            elif mode == Pin.IN:
                self.pins[pin] = Pin(pin_number, Pin.IN, Pin.PULL_UP)  # 输入模式（带上拉）
            else:
                raise ValueError("mode 必须是 Pin.OUT 或 Pin.IN")


    def output_IO(self, pin = 1 , value = 1):
        """
        设置 GPIO 输出状态。

        :param pin: 引脚编号（1 或 2）
        :param value: 输出值（0 或 1）
        """
        self._init_pin(pin, Pin.OUT)  # 初始化引脚为输出模式
        self.pins[pin].value(value)

    def read_IO(self, pin = 1):
        """
        读取 GPIO 输入状态。

        :param pin: 引脚编号（1 或 2）
        :return: 引脚状态（0 或 1）
        """
        self._init_pin(pin, Pin.IN)  # 初始化引脚为输入模式
        return self.pins[pin].value()


    def _init_adc(self, pin):
        """ 初始化 ADC 并校验 ESP32 引脚有效性 """
        pin_mapping = self._get_pin_mapping()
        
        # 逻辑引脚校验
        if pin not in pin_mapping:
            raise ValueError(f"逻辑引脚 {pin} 无效，当前端口 {self.port_id} 有效引脚：{list(pin_mapping.keys())}")
        
        physical_pin = pin_mapping[pin]
        
        # 物理引脚 ADC 支持性校验
        adc_block1 = list(range(32,40))  # ADC1: 32-39
        adc_block2 = [0,2,4,12,13,14,15,25,26,27]  # ADC2
        if physical_pin not in adc_block1 + adc_block2:
            raise ValueError(f"物理引脚 {physical_pin} 不支持 ADC，请参考 ESP32 引脚图")
        
        # 初始化 ADC
        if pin not in self.adc_pins:
            self._cleanup_pin(pin)
            try:
                self.adc_pins[pin] = ADC(Pin(physical_pin))
                self.adc_pins[pin].atten(ADC.ATTN_11DB)  # 设置 0-3.6V 量程
                print(f"ADC 初始化成功: Port {self.port_id}, 逻辑引脚 {pin} -> 物理引脚 {physical_pin}")
            except Exception as e:
                raise RuntimeError(f"ADC 初始化失败: {e} (可能 ADC2 与 WiFi 冲突)")

    def read_ADC(self, pin=1):
        """ 读取 ADC 值 (ESP32 的精度为 12-bit 0-4095) """
        self._init_adc(pin)
        return self.adc_pins[pin].read()
    
    
    def _init_pwm(self, pin):
        """
        初始化 PWM 引脚。

        :param pin: 引脚编号（1 或 2）
        """
        pin_mapping = self._get_pin_mapping()
        if pin not in pin_mapping:
            raise ValueError(f"pin 必须是 {list(pin_mapping.keys())} 中的一个")

        if pin not in self.pwm_pins:
            self._cleanup_pin(pin)  # 清理引脚配置
            print('清理引脚配置')
            time.sleep_ms(50)
            self.pwm_pins[pin] = PWM(Pin(pin_mapping[pin]))
          
    def output_PWM(self, pin, freq, duty):
        """
        设置 PWM 波形输出。

        :param pin: 引脚编号（1 或 2）
        :param freq: PWM 频率（Hz）
        :param duty: PWM 占空比（0-1023）
        """
        self._init_pwm(pin)  # 初始化 PWM 引脚
        self.pwm_pins[pin].freq(freq)  # 设置频率
        self.pwm_pins[pin].duty(duty)  # 设置占空比

    def servo_angle(self, pin = 1, angle = 0):
        """
        控制舵机角度。

        :param pin: 引脚编号（1 或 2）
        :param angle: 舵机角度（0-180）
        """
        if angle < 0 or angle > 180:
            raise ValueError("角度必须在 0 到 180 之间")

        # 计算占空比
        # 0 度 -> 2.5% 占空比 -> 0.5ms / 20ms * 1023 = 25.575 ≈ 26
        # 180 度 -> 12.5% 占空比 -> 2.5ms / 20ms * 1023 = 127.875 ≈ 128
        duty = int(26 + (angle / 180) * (128 - 26))

        # 设置 PWM 频率为 50Hz，占空比为计算值
        self.output_PWM(pin, 50, duty)

    def _init_dht11(self, pin=1):
        """
        初始化 DHT11 传感器。

        :param pin: 引脚编号（1 或 2），默认为 1
        """
        pin_mapping = self._get_pin_mapping()
        if pin not in pin_mapping:
            raise ValueError(f"pin 必须是 {list(pin_mapping.keys())} 中的一个")

        # 选择引脚
        dht11_pin_number = pin_mapping[pin]

        # 初始化 DHT11
        try:
            self.dht11 = dht.DHT11(Pin(dht11_pin_number))
#             print(f"DHT11 初始化成功，引脚: {dht11_pin_number}")
        except Exception as e:
            print(f"DHT11 初始化失败: {e}")
            self.dht11 = None

    def DHT11(self, pin=1):
        """
        读取 DHT11 传感器的温度和湿度。

        :param pin: 引脚编号（1 或 2），默认为 1
        :return: 温度, 湿度
        """
        self._init_dht11(pin)  # 初始化 DHT11 传感器
        if self.dht11 is None:
            print("DHT11 未初始化或初始化失败")
            return None, None

        try:
            self.dht11.measure()  # 读取传感器数据
            temp = self.dht11.temperature()  # 获取温度
            hum = self.dht11.humidity()  # 获取湿度
#             print(f"DHT11 读取成功: 温度={temp}°C, 湿度={hum}%")
            return temp, hum
        except OSError as e:
            print("DHT11 读取失败! 请检查硬件连接。")
            return None, None
        except Exception as e:
            print(f"读取 DHT11 时出现未知错误: {e}")
            print(f"错误类型: {type(e).__name__}")
            print(f"错误详情: {str(e)}")
            return None, None

    def _init_ds18b20(self, pin):
        """
        初始化 DS18B20 传感器。

        :param pin: 引脚编号（1 或 2）
        """
        if not hasattr(self, 'ds18b20'):  # 确保只初始化一次
            pin_mapping = self._get_pin_mapping()
            if pin not in pin_mapping:
                raise ValueError(f"pin 必须是 {list(pin_mapping.keys())} 中的一个")

            # 选择引脚
            ds18b20_pin_number = pin_mapping[pin]

            # 初始化 DS18B20
            self.ds18b20_pin = Pin(ds18b20_pin_number)
            self.ds18b20 = DS18X20(OneWire(self.ds18b20_pin))
            self.ds18b20_roms = self.ds18b20.scan()  # 扫描总线上的设备
            if not self.ds18b20_roms:
                raise ValueError("未找到 DS18B20 设备")

    def read_DS18B20(self, pin=1):
        """
        读取 DS18B20 传感器的温度。

        :param pin: 引脚编号（1 或 2）
        :return: 温度值（摄氏度），如果读取失败返回 None
        """
        self._init_ds18b20(pin)  # 确保 DS18B20 已初始化
      
        try:
            self.ds18b20.convert_temp()  # 启动温度转换
            time.sleep_ms(750)  # 等待转换完成（最大 750ms）
            temp = self.ds18b20.read_temp(self.ds18b20_roms[0])  # 读取温度
            return temp
        except Exception as e:
            print(f"读取 DS18B20 时出错: {e}")
            return None
    '''
    超声波
    '''
    def _init_ultrasonic(self):
        if self.ultrasonic_trig is None or self.ultrasonic_echo is None:
            pin_mapping = self._get_pin_mapping()
            trig_pin = pin_mapping[1]  # 引脚1 作为 Trig
            echo_pin = pin_mapping[2]  # 引脚2 作为 Echo
            self.ultrasonic_trig = Pin(trig_pin, Pin.OUT)
            self.ultrasonic_echo = Pin(echo_pin, Pin.IN)

    def get_distance(self):
        """
        获取超声波测距的距离。

        :return: 返回距离，单位为厘米。如果测量失败，返回 None。
        """
        self._init_ultrasonic()  # 确保超声波引脚已初始化

        try:
            # 发送超声波信号
            self.ultrasonic_trig.value(1)  # 触发高电平
            time.sleep_us(20)              # 保持高电平 20 微秒
            self.ultrasonic_trig.value(0)  # 触发低电平

            # 等待 Echo 引脚变为高电平
            while self.ultrasonic_echo.value() == 0:
                pass
            start_time = time.ticks_us()  # 记录开始时间

            # 等待 Echo 引脚变为低电平
            while self.ultrasonic_echo.value() == 1:
                pass
            end_time = time.ticks_us()  # 记录结束时间

            # 计算时间差并转换为距离
            duration = end_time - start_time
            distance = duration * 0.017  # 距离计算，单位：厘米
            return distance
        except Exception as e:
            print(f"超声波测距失败: {e}")
            return None
    def _init_rfid(self):
        """
        初始化 RFID 模块。
        """
        """
        初始化 RFID 模块的 I2C 引脚，基于当前端口的映射。
        """
        if not hasattr(self, 'rfid'):  # 确保只初始化一次
            try:
                # 获取当前端口的引脚映射
                pin_mapping = self._get_pin_mapping()
                sda_pin = pin_mapping[1]  # 引脚1 作为 SDA
                scl_pin = pin_mapping[2]  # 引脚2 作为 SCL

                # 初始化 I2C 总线
                self.i2c = SoftI2C(sda=Pin(sda_pin), scl=Pin(scl_pin))

                # 扫描 I2C 设备
                devices = self.i2c.scan()
                if len(devices) == 0:
                    raise ValueError("未找到 I2C 设备！")

                # 初始化 MFRC522
                self.rfid = mfrc522_i2c.Mfrc522I2c(self.i2c)
            except Exception as e:
                print(f"初始化 RFID 模块时出错: {e}")
                self.rfid = None  # 标记 RFID 模块初始化失败

    def read_RFID(self):
        """
        读取 RFID 卡的 UUID。

        :return: UUID（字节列表），如果未读取到或出错返回 None
        """
        if not hasattr(self, 'rfid'):
            self._init_rfid()  # 初始化 RFID 模块

        if self.rfid is None:
            print("RFID 模块未初始化或初始化失败")
            return None

        try:
            uuid = self.rfid.read_uuid()  # 读取 UUID
            if uuid is not None:
                return uuid
            else:
                return None
        except Exception as e:
            print(f"读取 RFID 时出错: {e}")
            return None
    #--------------------------------------------------
    # 修改后的 MP3 嵌套类（通过类属性获取引脚）
    #--------------------------------------------------
    class ACB_MP3:
        def __init__(self, port):
            """通过 Port 类的映射获取引脚"""
            pin_mapping = port._get_pin_mapping()
            tx_pin = pin_mapping[2]  # 引脚2 作为 TX
            rx_pin = pin_mapping[1]  # 引脚1 作为 RX
            self.uart = UART(1, baudrate=9600, bits=8, parity=None, stop=1, tx=tx_pin, rx=rx_pin)

        def play(self):
            """
            播放音频。
            """
            play_cmd = bytearray([0x7E, 0x03, 0x11, 0x12, 0xEF])
            self.uart.write(play_cmd)

        def pause(self):
            """
            暂停音频。
            """
            pause_cmd = bytearray([0x7E, 0x03, 0x12, 0x11, 0xEF])
            self.uart.write(pause_cmd)

        def nextTrack(self):
            """
            切换到下一首曲目。
            """
            next_track_cmd = bytearray([0x7E, 0x03, 0x13, 0x10, 0xEF])
            self.uart.write(next_track_cmd)

        def previousTrack(self):
            """
            切换到上一首曲目。
            """
            previous_track_cmd = bytearray([0x7E, 0x03, 0x14, 0x17, 0xEF])
            self.uart.write(previous_track_cmd)

        def setVolume(self, volume):
            """
            设置音量。

            :param volume: 音量值，范围根据实际设备而定
            """
            checksum = 0x04 ^ 0x31 ^ volume
            set_volume_cmd = bytearray([0x7E, 0x04, 0x31, volume, checksum, 0xEF])
            self.uart.write(set_volume_cmd)

        def playInFolder(self, folder_num):
            """
            在指定文件夹播放音频。

            :param folder_num: 文件夹编号
            """
            checksum = 0x05 ^ 0x42 ^ 0x01 ^ folder_num
            play_in_folder_cmd = bytearray([0x7E, 0x05, 0x42, 0x01, folder_num, checksum, 0xEF])
            self.uart.write(play_in_folder_cmd)

        def getPlayState(self):
            """
            获取当前播放状态，并输出接收到的数据。

            :return: None
            """
            get_play_state_cmd = bytearray([0x7E, 0x03, 0x20, 0x23, 0xEF])
            self.uart.write(get_play_state_cmd)

            comdata = ""
            while True:
                if self.uart.any():  # 检查是否有可用数据
                    byte_data = self.uart.read(1)
                    if byte_data:
                        comdata += chr(byte_data[0])  # 读取一个字节并转换为字符
                        time.sleep(0.002)  # 稍等以获取数据

                        # 根据接收到的数据判断状态（使用包含判断）
                        if "OK0002" in comdata:
                            print("当前播放状态: 播放中")
                            return
                        elif "OK0001" in comdata:
                            print("当前播放状态: 暂停")
                            return
                        elif "STOP" in comdata:
                            print("当前播放状态: 停止")
                            return
                else:
                    # 如果没有可用数据，则可以选择退出循环或继续等待
                    break
            # 输出接收到的数据
            print(comdata)
            # 如果没有接收到任何数据，可以输出相应信息
            if not comdata:
                print("没有接收到数据。")

    def init_mp3(self):
        """
        初始化 MP3 模块。

        :return: ACB_MP3 实例
        """
        if not hasattr(self, 'mp3'):
            self.mp3 = self.ACB_MP3(self)  # 初始化 MP3 模块
        return self.mp3

        
        
        


