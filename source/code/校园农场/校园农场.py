from educator import *  #导入库文件
from machine import Timer
import time

'''
校园农场系统

功能描述：
该程序用于监测温度、湿度和光强，并根据预设的阈值自动控制风扇、加湿器和LED灯的开关状态。
当温度超过设定阈值时，自动关闭风扇；当湿度低于设定阈值时，自动开启加湿器；如果光强低于设定值，则开启LED灯。
'''

# 定义温度和湿度的阈值
TEMP_THRESHOLD = 34.0  # 温度阈值 (单位: 摄氏度)
HUM_THRESHOLD = 40.0   # 湿度阈值 (单位: 百分比)
LIG_THRESHOLD = 1000.0   # 湿度阈值 (单位: 百分比)
port1 = GPIOControl(pin1=0)
port2 = GPIOControl(pin1=2)   

# 初始化光强和温湿度和噪音
light1=light.read()
temp=humiture.read_temp()
hum=humiture.read_hum()
#定时器的中断的回调函数
def fun(tim):
    global light1 , temp ,hum
    # 控制风扇和加湿器,风扇控制连接在 Port1,加湿器控制连接在 Port2
    if temp < TEMP_THRESHOLD:
        port1.set(0)  # 关闭风扇
    else:
        port1.set(1)  # 打开风扇

    if hum < HUM_THRESHOLD:
        port2.set(1)  # 打开加湿器
    else:
        port2.set(0)  # 关闭加湿器
    if light1 < LIG_THRESHOLD:
        led.on() #LED 打开
    else:
        led.off() #LED 关闭
tim = Timer(1)
tim.init(period=1000,mode=Timer.PERIODIC,callback=fun)
oled.print(1, 1, "  校园农场模型", 1)

# RGB灯光闪烁 
rgb.write_left(128, 0, 0) # 左侧灯为红色，全亮度
rgb.write_right(0, 128, 0) # 右侧灯为绿色，半亮度
time.sleep(0.3)
rgb.write_left(64, 0, 64) # 左侧灯为红色，全亮度
rgb.write_right(0, 0, 64) # 右侧灯为绿色，半亮度


while True:
    light1=light.read()
    temp=humiture.read_temp()
    hum=humiture.read_hum()



    oled.print(1,1,"光强:%0.0f "%(light1),1)
    oled.print(1,2,"温度:%0.2f C" %(temp), 1) #获取温度值
    oled.print(1,3,"湿度:%0.2f %%" % (hum),1) #获取湿度值


