# RGB 模块方法使用说明
```{admonition} 注意：
:class: note
所有类的使用都需要导入库文件：from educator import * 
```
## 1. rgb.write_left() - 设置左侧LED颜色

```python
rgb.write_left(red, green, blue)
```

### 参数说明

| 参数  | 类型 | 范围  | 说明         |
| ----- | ---- | ----- | ------------ |
| red   | int  | 0-255 | 红色分量强度 |
| green | int  | 0-255 | 绿色分量强度 |
| blue  | int  | 0-255 | 蓝色分量强度 |

### 示例

```python
# 设置左侧LED为纯红色
rgb.write_left(255, 0, 0)
time.sleep(1)  # 等待 1 秒
# 设置左侧LED为紫色（混合颜色）
rgb.write_left(128, 0, 255)

```

------

## 2. rgb.write_right() - 设置右侧LED颜色

```python
rgb.write_right(red, green, blue)
```

### 参数说明

| 参数  | 类型 | 范围  | 说明         |
| ----- | ---- | ----- | ------------ |
| red   | int  | 0-255 | 红色分量强度 |
| green | int  | 0-255 | 绿色分量强度 |
| blue  | int  | 0-255 | 蓝色分量强度 |

### 示例

```python
# 设置右侧LED为绿色
rgb.write_right(0, 255, 0)
time.sleep(1)  # 等待 1 秒
# 设置右侧LED为白色（全亮）
rgb.write_right(255, 255, 255)
```

------

## 3. rgb.clear() - 清除所有LED

```python
rgb.clear()
```

### 功能说明

- 立即关闭所有LED灯
- 无需任何参数

### 示例

```python
# 关闭所有LED
rgb.clear()
```

------

## 4. rgb.set_brightness() - 亮度控制

```python
rgb.set_brightness(index, red, green, blue, brightness)
```

### 参数说明

| 参数       | 类型 | 范围  | 说明                          |
| ---------- | ---- | ----- | ----------------------------- |
| index      | int  | 0-2   | LED索引（0=左，1=右，2=扩展） |
| red        | int  | 0-255 | 基础红色分量                  |
| green      | int  | 0-255 | 基础绿色分量                  |
| blue       | int  | 0-255 | 基础蓝色分量                  |
| brightness | int  | 0-255 | 亮度调节（0=最暗，255=最亮）  |

### 示例

```python
# 设置左侧LED为50%亮度的蓝色
rgb.set_brightness(0, 0, 0, 255, 128)
# 设置右侧LED为25%亮度的橙色
rgb.set_brightness(1, 255, 165, 0, 64)
```

------

## 使用注意事项

1. 颜色混合：通过调整RGB分量可实现1600万种颜色组合
2. 亮度衰减：实际亮度 = 基础颜色值 × (brightness/255)
3. 索引范围：
   - 0 = 左侧LED
   - 1 = 右侧LED
   - 2 = 扩展LED（需硬件支持）
4. 硬件限制：长时间保持高亮度可能影响LED寿命
5. 性能优化：
   - 连续操作建议间隔至少50ms
   - 亮度低于15时可能无法点亮LED