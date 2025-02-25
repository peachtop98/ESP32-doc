from siot import iot
from educator import *  #导入库文件

# 初始化相关模块
i2c = SoftI2C(sda=Pin(23), scl=Pin(22))
oled=SSD1306_I2C(128, 64, i2c)  # 创建OLED对象

                
SERVER = "39.108.114.58"            #MQTT服务器IP
CLIENT_ID = ""                  #CLIENT_ID可以留空
IOT_pubTopic_Light  = 'LB0loqyzE2_vuON-7M4Mp'       #“topic”为“项目名称/设备名称”
IOT_pubTopic_lamp_status  = 'Xvl1xhT3gBa7Dzh_guv-C'       #“topic”为“项目名称/设备名称”
IOT_pubTopic_button  = 'uFmhf0Ya32tiUnFoA7uPq'       #“topic”为“项目名称/设备名称”


IOT_UserName ='scope'            #用户名
IOT_PassWord ='scope@123'         #密码



current_status = False  # 需根据实际情况实现此函数
def sub_cb(topic, msg):
    print((topic, msg))
    global current_status
    if msg == b'{"from":"server","data":"on"}':  
        rgb.write_left(255, 255, 255)   # 左侧灯为白色，全亮度
        rgb.write_right(255, 255, 255)  # 右侧灯为白色，全亮度
        current_status = True
    elif msg == b'{"from":"server","data":"off"}':
        rgb.write_left(0, 0, 0) # 左侧灯关闭
        rgb.write_right(0, 0, 0) # 右侧灯关闭
        current_status = False
          
    oled.clear_area(0,38,120,38+16)
    oled.text(msg, 0, 38)
    oled.show()  # 显示
def timer_cb(msg):
    siot.check_msg()
  
ssid = "Scope_Xiaomi"
password =  "00000000"
siot = iot(CLIENT_ID, SERVER, port=1883,user=IOT_UserName, password=IOT_PassWord)

def WIFIconnect():
    import network
    station = network.WLAN(network.STA_IF)
    if station.isconnected() == True:
        print("Wifi already connected")
        return
    station.active(True)
    station.connect(ssid, password)
    while station.isconnected() == False:
        pass
    print("Connection successful")
    print(station.ifconfig())
WIFIconnect()
siot.connect()
siot.subscribe(IOT_pubTopic_button, sub_cb)

timer = Timer(1)
timer.init(period=50,mode=Timer.PERIODIC, callback=timer_cb)


threshold = 200  # 设置光强的阈值
lamp_status = 0
last_state = lamp_status  # 跟踪上一个状态
while True:
    light_intensity = light.read()  # 获取光强

    oled.clear_area(0, 0, 120, 38)
    oled.text(f"->light: {light_intensity}", 0, 0)
    oled.show()  # 显示

    # 判断光强是否超过阈值
    if light_intensity > threshold:
        lamp_status = 0  # 关灯
    else:
        lamp_status = 1  # 开灯
        
    
    if lamp_status != last_state:  # 检查状态是否改变
        if lamp_status:
            rgb.write_left(255, 255, 255)   # 左侧灯为白色，全亮度
            rgb.write_right(255, 255, 255)  # 右侧灯为白色，全亮度
            print("已经打开灯光")
        else:
            rgb.write_left(0, 0, 0) # 左侧灯关闭
            rgb.write_right(0, 0, 0) # 右侧灯关闭
            print("已经关闭灯光")
            
    last_state = lamp_status  # 跟踪上一个状态
    mqtt1_message = f'{{"key": "{IOT_pubTopic_Light}", "data": {light_intensity}}}'
    mqtt2_message = f'{{"key": "{IOT_pubTopic_lamp_status}", "data": {lamp_status}}}'
    
    siot.publish(IOT_pubTopic_Light, mqtt1_message)
    siot.publish(IOT_pubTopic_lamp_status, mqtt2_message)
    
    print(mqtt1_message, mqtt2_message)
    time.sleep(1)





