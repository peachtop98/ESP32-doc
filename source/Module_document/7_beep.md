# 蜂鸣器模块使用说明

```{admonition} 注意：
:class: note
所有类的使用都需要导入库文件：from educator import * 
```

## 1. beep.play_melody() - 播放预置旋律

```python
beep.play_melody(gequ[索引号])  # 索引范围 0-4
```

### 预置旋律列表

| 索引 | 曲目名称       | 时长 | 音符数量 |
| ---- | -------------- | ---- | -------- |
| 0    | 简单旋律       | 1.8s | 6        |
| 1    | 《小星星》     | 5.2s | 14       |
| 2    | 《生日快乐》   | 12s  | 24       |
| 3    | 《两只老虎》   | 6.8s | 26       |
| 4    | 《铃儿响叮当》 | 9.6s | 26       |

### 示例

```python
from educator import *  # 导入库文件
import music

# 播放生日快乐歌
beep.play_melody(music.gequ[2])

# 循环播放小星星
while True:
    beep.play_melody(music.gequ[1])
    time.sleep(2)

```

------

## 2. beep.time() - 单音提示

```python
beep.time(duration)
```

### 参数说明

| 参数     | 类型 | 有效范围 | 说明             |
| -------- | ---- | -------- | ---------------- |
| duration | int  | 10-60000 | 持续时间（毫秒） |

### 示例

```python
# 短提示音（系统就绪）
beep.time(150)
time.sleep(3)

# 长错误提示（搭配LED闪烁）
for _ in range(3):
    rgb.write_left(255,0,0)
    beep.time(500)
    rgb.write_left(0,0,0)
    time.sleep(0.3)
```

------

## 预置音符对照表

| 频率 (Hz) | 音名 | 等效钢琴键 |
| --------- | ---- | ---------- |
| 262       | C4   | 中音C      |
| 294       | D4   | D4         |
| 330       | E4   | E4         |
| 349       | F4   | F4         |
| 392       | G4   | G4         |
| 440       | A4   | 标准音A    |
| 523       | C5   | 高音C      |

------

## 使用注意事项

1. 自定义旋律：

```python
# 创建《欢乐颂》片段
huanlesong = (
    (392, 200), (440, 200), (494, 200), (523, 400),
    (494, 200), (440, 200), (392, 400)
)
beep.play_melody(huanlesong)
```

2. 多线程播放：

```python
from educator import *  # 导入库文件
import music
import _thread
def background_music():
    while True:
        beep.play_melody(music.gequ[4])
        time.sleep(10)

_thread.start_new_thread(background_music, ())
```

3. 硬件保护：

- 持续鸣响不要超过30秒
- 避免同时操作多个PWM通道

4. 扩展应用：

```python
# 温度报警旋律
def temp_alarm(current_temp):
    # 计算基准音符，以 262 为基础，根据当前温度与 20°C 的差值进行调整
    # 差值每增加 1°C，基准音符增加 10
    base_note = 262 + int((current_temp-20)*10)
    melody = [
        (base_note, 200), (0, 100),
        (base_note+50, 200), (0, 100),
        (base_note+100, 400)
    ]
    beep.play_melody(melody)

temp1 = 25
print(f"当前温度为 {temp1}°C，触发报警：")
temp_alarm(temp1)
```