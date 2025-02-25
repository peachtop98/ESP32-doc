from educator import *  # 导入库文件
# 按键切换RGB的灯光

# 用于记录灯光状态切换的次数，初始化为0
flag = 0
while True:
    # 以下代码块用于检测按键是否被按下，通过判断按键A或者按键B是否为按下状态（值为1表示按下）
    if button.get_a() == 1 or button.get_b() == 1:  
        # 为了消除按键抖动带来的误触发，短暂延时10毫秒，一般机械按键按下瞬间会有电平不稳定的抖动情况
        time.sleep_ms(10)  
        # 再次确认按键是否按下，确保是稳定的按下操作，而非抖动产生的误判
        if button.get_a() == 1 or button.get_b() == 1:
            flag += 1
            # 当切换次数达到5次时，重新从1开始计数，实现循环切换灯光状态的效果
            if flag == 5:  
                flag = 1

            print('灯光状态改变')

            # 根据flag的值来设置不同的灯光颜色，实现多种灯光状态切换效果
            if flag == 1:
                # 设置左侧RGB灯为红色，参数分别对应红、绿、蓝通道的值，255表示该通道满亮度，0表示关闭其他通道
                rgb.write_left(255, 0, 0)  
                # 设置右侧RGB灯为红色，与左侧设置同理
                rgb.write_right(255, 0, 0)  
                print('红灯亮')
            elif flag == 2:
                # 设置左侧RGB灯为绿色，即绿通道满亮度，红、蓝通道关闭
                rgb.write_left(0, 255, 0)  
                # 设置右侧RGB灯为绿色，同样的设置方式
                rgb.write_right(0, 255, 0)  
                print('绿灯亮')
            elif flag == 3:
                # 设置左侧RGB灯为蓝色，蓝通道满亮度，红、绿通道关闭
                rgb.write_left(0, 0, 255)  
                # 设置右侧RGB灯为蓝色，按照对应参数设置
                rgb.write_right(0, 0, 255)  
                print('蓝灯亮')
            elif flag == 4:
                # 将左侧RGB灯各通道值设为0，即熄灭左侧灯
                rgb.write_left(0, 0, 0)  
                # 将右侧RGB灯各通道值设为0，熄灭右侧灯
                rgb.write_right(0, 0, 0)  
                print('RGB灭')

            # 以下代码块用于检测按键是否松开，保持循环等待，直到按键松开
            while button.get_a() == 1 or button.get_b() == 1:
                pass  # 等待按键松开

    # 短暂延时0.1秒，避免过于频繁地读取按键状态，减少不必要的资源消耗和误判情况
    time.sleep(0.1)  