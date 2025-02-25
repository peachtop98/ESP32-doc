from educator import *  # 导入库文件
import time

'''
智能加湿系统
功能描述：
该程序旨在自动控制加湿器，以确保环境湿度保持在舒适范围内。
当湿度低于设定阈值时，加湿器会自动开启；当湿度达到或超过设定阈值时，加湿器会关闭。
'''

# 定义湿度的阈值
HUM_THRESHOLD = 50.0  # 湿度阈值 (单位: 百分比)

# GPIO 控制端口
port2 = GPIOControl(pin1=2)  # 假设加湿器连接在 Port2

# 初始化上一个状态
last_hum_status = None  # 用于跟踪上一个加湿器状态

oled.print(3, 1, "智能加湿系统", 1)

while True:
    # 读取湿度值
    hum = humiture.read_hum()
    oled.print(1, 2, "湿度:%0.2f %%" % (hum), 1)  # 显示湿度
    # 控制加湿器
    if hum < HUM_THRESHOLD:
        current_status = 'ON'
        led.off()
    else:
        current_status = 'OFF'
        led.on()

    # 打印状态变化的信息
    if current_status != last_hum_status:
        port2.set(1)  # 打开加湿器
        time.sleep(0.5)
        port2.set(0)  # 打开加湿器

        last_hum_status = current_status  # 更新上一个状态
        print(f"加湿器已{'开启' if current_status == 'ON' else '关闭'}")
# 

