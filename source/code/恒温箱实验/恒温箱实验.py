from educator import *  # 导入库文件

'''
功能描述：
该程序用于控制温度恒温箱的加热器，保持环境温度在设定的范围内。
程序通过读取环境中的当前温度值，与目标温度进行比较，以自动调节加热器的开关状态。
'''

# 目标温度
target_temperature = 35.0

while True:
    # 读取当前温度
    current_temp = humiture.read_temp()
    
    # 控制加热器
    if current_temp < target_temperature:
        Port2.output_IO(1, 1)  # 打开加热器
        print("加热片设置高电平")
    else:
        Port2.output_IO(1, 1)  # 关闭加热器
        print("加热片设置低电平")
    # 显示当前温度
    oled.print(3, 2, "温度:%0.2f C" % current_temp, 1)  # 显示温度值

    time.sleep_ms(100)  # 延时 100 毫秒

