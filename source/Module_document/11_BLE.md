## 蓝牙模块使用说明

```{admonition} 注意：
:class: note
蓝牙的类导入使用： from MicroBLE import BLESlave ,BLEMaster
```

本小节介绍蓝牙模块相关的两个类`BLEMaster`（蓝牙主设备）和`BLESlave`（蓝牙从设备），用于实现设备间的蓝牙低功耗通信，支持命令传输与数据交互，可应用于物联网设备控制、数据采集等场景。

### BLESlave 类（蓝牙从设备）

#### 功能描述
实现蓝牙从设备功能，通过广播让主设备发现并连接，可接收主设备发送的命令，并向主设备发送响应数据。支持自动维护连接状态，在断开连接后会重新广播等待新连接。

#### 初始化方法
```python
ble_slave = BLESlave(target_device_name="ESP32S3", debug=False)
```

|参数|类型|说明|默认值|
| ----| ----| ----| ----|
|target_device_name|str|从设备名称，用于主设备识别，长度限制10字符以内|"CMD-RECEIVER"|
|debug|bool|是否开启调试模式，开启后打印连接状态、命令接收等信息|False|

#### 主要方法

##### BLESlave.send_response(message)
**功能**：向已连接的主设备发送响应数据  
**使用方式**：
```python
# 发送文本响应
success = ble_slave.send_response("LED已开启")
if success:
    print("响应发送成功")
```

|参数|类型|说明|
| ----| ----| ----|
|message|str|要发送的响应内容，长度限制20字符以内|

|返回值|说明|
| ----| ----|
|bool|`True`表示发送成功，`False`表示发送失败（如未连接、发送异常等）|


##### BLESlave.get_received_command()
**功能**：从命令队列中获取主设备发送的命令  
**使用方式**：
```python
# 循环获取命令
while True:
    command = ble_slave.get_received_command()
    if command:
        print(f"收到命令：{command}")
    time.sleep(0.1)
```

|返回值|说明|
| ----| ----|
|str|主设备发送的命令字符串（UTF-8编码）；若为二进制数据则返回`BINARY:十六进制字符串`；队列为空时返回`None`|


##### BLESlave.set_response_handler(handler)
**功能**：设置自定义命令处理器，用于实时处理接收到的命令  
**使用方式**：
```python
# 定义自定义处理器
def handle_command(cmd):
    print(f"处理命令：{cmd}")
    if cmd == "LED_ON":
        ble_slave.send_response("LED已开启")

# 设置处理器
ble_slave.set_response_handler(handle_command)
```

|参数|类型|说明|
| ----| ----| ----|
|handler|function|接收1个字符串参数的函数，用于处理命令|

|返回值|说明|
| ----| ----|
|无|无返回值|


##### BLESlave.is_connected()
**功能**：查询当前与主设备的连接状态  
**使用方式**：
```python
if ble_slave.is_connected():
    print("已连接到主设备")
else:
    print("未连接")
```

|返回值|说明|
| ----| ----|
|bool|`True`表示已连接，`False`表示未连接|


##### BLESlave.maintain_connection()
**功能**：维护连接状态（需定期调用），在未连接且未广播时自动开始广播，并定期进行垃圾回收  
**使用方式**：
```python
# 主循环中定期调用
while True:
    ble_slave.maintain_connection()
    time.sleep(0.5)
```

|返回值|说明|
| ----| ----|
|无|无返回值|


#### 使用示例
```python
# 初始化从设备
ble_slave = BLESlave(target_device_name="MY_SLAVE", debug=True)

# 定义命令处理逻辑
def process_command(cmd):
    print(f"处理命令: {cmd}")
    if cmd == "LED_ON":
        ble_slave.send_response("LED已开启")
    elif cmd == "LED_OFF":
        ble_slave.send_response("LED已关闭")

# 设置命令处理器
ble_slave.set_response_handler(process_command)

# 主循环维护连接
while True:
    ble_slave.maintain_connection()
    time.sleep(0.1)
```

#### 使用注意事项
1. 设备名称长度限制：`target_device_name`参数需控制在10字符以内，超出部分会被自动截断。
2. 数据长度限制：`send_response`方法发送的消息长度需控制在20字符以内，过长会被截断。
3. 连接维护：`maintain_connection`方法需在主循环中定期调用（建议间隔不超过1秒），以确保连接断开后能重新广播。
4. 二进制数据处理：接收到的二进制数据会以`BINARY:十六进制字符串`格式返回，需自行解析处理。
5. 异常处理：发送数据或处理事件时若发生异常，会自动打印堆栈信息，可通过`debug=True`查看详细日志排查问题。


### BLEMaster 类（蓝牙主设备）

#### 功能描述
实现蓝牙主设备功能，可扫描并发现目标从设备，建立连接后向从设备发送命令，并接收从设备的响应数据。支持自动重连，断开连接后会重新扫描并尝试连接。

#### 初始化方法
```python
ble_master = BLEMaster(target_device_name="MY_SLAVE", debug=False)
```

|参数|类型|说明|默认值|
| ----| ----| ----| ----|
|target_device_name|str|目标从设备的名称（用于扫描识别）|无|
|debug|bool|是否开启调试模式，开启后打印扫描、连接、数据传输等详细日志|False|

#### 主要方法

##### BLEMaster.scan()
**功能**：启动扫描以寻找目标从设备，扫描超时时间5秒，未找到时会自动重新扫描  
**使用方式**：
```python
# 启动扫描
ble_master.scan()
```

|返回值|说明|
| ----| ----|
|无|无返回值|


##### BLEMaster.send_command(command)
**功能**：向已连接的从设备发送命令  
**使用方式**：
```python
# 发送命令
if ble_master.is_connected():
    success = ble_master.send_command("LED_ON")
    if success:
        print("命令发送成功")
```

|参数|类型|说明|
| ----| ----| ----|
|command|str|要发送的命令字符串|

|返回值|说明|
| ----| ----|
|bool|`True`表示发送成功，`False`表示发送失败（如未连接、发送异常等）|


##### BLEMaster.get_response()
**功能**：从响应队列中获取从设备发送的响应数据  
**使用方式**：
```python
# 获取响应
response = ble_master.get_response()
if response:
    print(f"收到响应：{response}")
```

|返回值|说明|
| ----| ----|
|str|从设备发送的响应字符串（UTF-8编码）；若为二进制数据则返回`HEX:十六进制字符串`；队列为空时返回`None`|


##### BLEMaster.set_response_handler(handler)
**功能**：设置自定义响应处理器，用于实时处理接收到的从设备响应  
**使用方式**：
```python
# 定义自定义响应处理器
def handle_response(data):
    print(f"收到响应：{data}")

# 设置处理器
ble_master.set_response_handler(handle_response)
```

|参数|类型|说明|
| ----| ----| ----|
|handler|function|接收1个字符串参数的函数，用于处理响应数据|

|返回值|说明|
| ----| ----|
|无|无返回值|


##### BLEMaster.is_connected()
**功能**：查询当前与从设备的连接状态  
**使用方式**：
```python
if ble_master.is_connected():
    print("已连接到从设备")
else:
    print("未连接")
```

|返回值|说明|
| ----| ----|
|bool|`True`表示已连接，`False`表示未连接|


#### 使用示例
```python
# 初始化主设备，目标从设备名称为"MY_SLAVE"
ble_master = BLEMaster(target_device_name="MY_SLAVE", debug=True)

# 启动扫描
ble_master.scan()

# 等待连接建立
import time
while not ble_master.is_connected():
    time.sleep(1)

print("已连接到从设备")

# 定义响应处理器
def handle_response(data):
    print(f"响应处理器收到：{data}")

ble_master.set_response_handler(handle_response)

# 发送命令
ble_master.send_command("LED_ON")
time.sleep(1)
ble_master.send_command("LED_OFF")

# 主循环保持运行
while True:
    time.sleep(1)
```

#### 使用注意事项
1. 目标设备名称：`target_device_name`参数需与从设备设置的名称完全匹配（区分大小写），否则无法发现设备。
2. 扫描机制：`scan()`方法启动后会持续扫描直到找到目标设备，建议在调用后通过`is_connected()`判断连接状态。
3. 命令发送时机：需在`is_connected()`返回`True`后再调用`send_command()`，否则会发送失败。
4. 响应处理：响应数据可能延迟到达，建议通过`set_response_handler`设置回调函数实时处理，或定期调用`get_response()`获取。
5. 自动重连：当连接断开后，主设备会自动重新扫描并尝试连接，无需手动干预。
6. 调试信息：开启`debug=True`可查看详细的扫描、连接和数据传输日志，有助于排查通信问题。


### 技术参数表

|功能项|BLESlave（从设备）|BLEMaster（主设备）|
| ----| ----| ----|
|通信方式|蓝牙低功耗（BLE）|蓝牙低功耗（BLE）|
|响应时间|取决于数据长度（典型<100ms）|取决于数据长度（典型<100ms）|
|调试模式|支持，打印连接/命令日志|支持，打印扫描/连接/数据日志|
|自动重连|断开后自动重新广播|断开后自动重新扫描连接|
|数据格式|UTF-8字符串（二进制数据转为十六进制）|UTF-8字符串（二进制数据转为十六进制）|