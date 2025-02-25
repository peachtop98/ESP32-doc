from educator import *  #导入库文件
from machine import *

# 定义初始状态
state = False  # 变量的初始状态
port2 = GPIOControl(pin1=2, pin2=3)

# 定义定时器的回调函数
def change_state(tim):
    global state
    state = not state  # 切换状态
    print("状态已更改:", state)

# 初始化定时器
tim = Timer(1)  # 创建定时器实例
tim.init(period=10000, mode=Timer.PERIODIC, callback=change_state)  # 设置为每10秒调用一次

last_state = state  # 跟踪上一个状态
# 主循   
while True:
    if state != last_state:  # 检查状态是否改变
        if state:
            port2.set(1)  # 打开加湿器
            print("已经打开加湿器")
        else:
            port2.set(0)  # 关闭加湿器
            print("已经关闭加湿器")
            
        last_state = state  # 更新上一个状态

