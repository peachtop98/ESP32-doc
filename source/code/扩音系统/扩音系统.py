from educator import *  # 导入库文件

'''
音量调节基于环境噪音的智能系统
功能描述：
该程序用于根据环境噪音的大小自动调整 MP3 播放器的音量。
当检测到的噪音低于 700，则保持较低音量；否则，提高音量，以便于在嘈杂环境中也能听到音乐。

'''
mp3_player = Port2.init_mp3()  # 初始化 MP3 模块

time.sleep(1)
# 初始化当前音量
mp3_player.setVolume(10)
#初始化噪音大小的变量
noise_level=0  
# 定时器的中断的回调函数
def fun(tim):
    global noise_level
    # 读取当前麦克风的声音值
    noise_level = mic.read()
    oled.print(4, 2, "sound: %d" % noise_level, 1)

# 初始化并启动定时器
tim = Timer(1)
tim.init(period=50, mode=Timer.PERIODIC, callback=fun)

mp3_player.play()  # 播放音频
while(1):
        # 根据噪音水平设置音量
    if noise_level < 700:
        mp3_player.setVolume(10)  # 设置新的音量
    else:
        mp3_player.setVolume(25)  # 设置新的音量
        time.sleep(2)
    

# 暂停音频
# mp3_player.pause()  # 暂停音乐

time.sleep(1)
# 获取当前播放状态并打印
mp3_player.getPlayState()