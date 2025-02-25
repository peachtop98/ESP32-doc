# OLED 模块方法使用说明

## 1. oled.print() - 文本显示

```python
oled.print(column, row, text, clear_row=0)
```

### 参数说明

| 参数      | 类型 | 说明                                |
| --------- | ---- | ----------------------------------- |
| column    | int  | 显示列位（1~16），每列对应8像素宽度 |
| row       | int  | 显示行位（1~4），每行对应16像素高度 |
| text      | str  | 要显示的字符串（支持中英文混合）    |
| clear_row | int  | 是否清空当前行（0=不清理，1=清理）  |

### 示例

```python
# 在第2行第3列显示文字并清空原行
oled.print(3, 2, "温度:25℃", clear_row=1)
```

------

## 2. oled.clear_area() - 区域清除

```python
oled.clear_area(x0, y0, x1, y1)
```

### 参数说明

| 参数 | 类型 | 说明                     |
| ---- | ---- | ------------------------ |
| x0   | int  | 区域左边界X坐标（0~127） |
| y0   | int  | 区域上边界Y坐标（0~63）  |
| x1   | int  | 区域右边界X坐标（>=x0）  |
| y1   | int  | 区域下边界Y坐标（>=y0）  |

### 示例

```python
# 清除屏幕上半部分
oled.clear_area(0, 0, 127, 31)
```

------

## 3. oled.draw_image() - 图像绘制

```python
oled.draw_image(image_data, x=0, y=0, width=0, height=0)
```

### 参数说明

| 参数       | 类型  | 说明                                    |
| ---------- | ----- | --------------------------------------- |
| image_data | tuple | 图像字节数据（每个字节对应8个垂直像素） |
| x          | int   | 图像起始X坐标（0~127）                  |
| y          | int   | 图像起始Y坐标（0~63）                   |
| width      | int   | 图像宽度（像素）                        |
| height     | int   | 图像高度（像素）                        |

### 数据格式示例

```python
# 48x48像素图标（每行6字节 × 48行 = 288字节）
image_data = (
    0x00,0x1E,0x21,0x21,0x1E,0x00,
    0x00,0x1E,0x21,0x21,0x1E,0x00,
    ... # 剩余数据省略
)
oled.draw_image(image_data, x=40, y=8, width=48, height=48)
```

------

## 4. oled.String_() - ASCII字符显示

```python
oled.String_(ch_str, x_axis, y_axis)
```

### 参数说明

| 参数   | 类型 | 说明                      |
| ------ | ---- | ------------------------- |
| ch_str | str  | ASCII字符串（仅支持英文） |
| x_axis | int  | 起始X坐标（像素）         |
| y_axis | int  | 起始Y坐标（像素）         |

### 示例

```python
# 在坐标(32,16)显示"HELLO"
oled.String_("HELLO", 32, 16)
```

------

## 5. oled.chinese() - 中文字符显示

```python
oled.chinese(ch_str, x_axis, y_axis)
```

### 参数说明

| 参数   | 类型 | 说明                             |
| ------ | ---- | -------------------------------- |
| ch_str | str  | 中文字符串（自动处理中英文混合） |
| x_axis | int  | 起始X坐标（像素）                |
| y_axis | int  | 起始Y坐标（像素）                |

### 示例

```python
# 在坐标(0,0)显示"温度传感器"
oled.chinese("温度传感器", 0, 0)
```

------

## 6. 图形绘制方法

### oled.fill() - 全屏填充

```python
oled.fill(color)
```

| 参数 | 说明     |
| ---- | -------- |
| 0    | 黑色填充 |
| 1    | 白色填充 |

### oled.line() - 绘制直线

```python
oled.line(x0, y0, x1, y1, color)
```

| 参数  | 说明     |
| ----- | -------- |
| x0,y0 | 起点坐标 |
| x1,y1 | 终点坐标 |
| 0/1   | 线条颜色 |

### oled.circle() - 绘制圆形

```python
oled.circle(x, y, radius, color)
```

| 参数   | 说明         |
| ------ | ------------ |
| x,y    | 圆心坐标     |
| radius | 半径（像素） |
| 0/1    | 轮廓颜色     |

### oled.show() - 更新显示

```python
oled.show()  # 所有绘制操作必须调用此方法才能生效
```

------

## 使用注意事项

1. 坐标系统：左上角为原点(0,0)，X轴向右延伸，Y轴向下延伸
2. 显示更新：所有绘制操作需调用show()后才会实际更新屏幕
3. 混合显示：
   - print()方法会自动处理中英文混合
   - 汉字占16x16像素，ASCII字符占8x16像素
4. 图像数据：
   - 建议使用PCtoLCD等工具生成图像字节数据
   - 数据格式要求：阴码、逐行扫描、顺向
5. 性能优化：
   - 批量操作完成后调用一次show()
   - 避免频繁全屏刷新