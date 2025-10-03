# 📷 摄像头配置指南

本指南说明如何为 `14_SenceVoice_QWen2VL_edgeTTS_realTime.py` 配置不同的摄像头输入源。

## 📋 目录

- [快速开始](#快速开始)
- [使用 iPhone/iPad 作为摄像头](#使用-iphoneipad-作为摄像头)
- [使用安卓手机作为摄像头](#使用安卓手机作为摄像头)
- [配置选项详解](#配置选项详解)
- [常见问题](#常见问题)

---

## 🚀 快速开始

在 `14_SenceVoice_QWen2VL_edgeTTS_realTime.py` 文件中找到配置区域（约第37-60行）：

```python
# ========== 摄像头配置 ==========
CAMERA_MODE = "default"  # 修改这里选择模式
# ...
```

### 支持的模式

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| `default` | 使用默认摄像头（索引0） | 有内置摄像头的笔记本 |
| `index` | 使用指定索引的摄像头 | 有多个摄像头设备 |
| `ip` | 使用IP摄像头/手机摄像头 | 台式机通过手机获取视频 |
| `file` | 使用视频文件测试 | 开发测试 |
| `disable` | 禁用视频功能 | 仅需要语音功能 |

---

## 📱 使用 iPhone/iPad 作为摄像头

### 方法 1：Continuity Camera（推荐 - macOS 用户）

**系统要求：**
- macOS Ventura (13.0) 或更高版本
- iOS 16 或更高版本
- 同一 Apple ID 登录

**步骤：**
1. 确保 iPhone 和 Mac 都连接到 WiFi 和蓝牙
2. iPhone 会自动作为摄像头被 Mac 识别
3. 在代码中设置：
   ```python
   CAMERA_MODE = "default"  # 或 "index"
   CAMERA_INDEX = 1  # 如果是第二个摄像头
   ```

### 方法 2：iVCam（推荐 - Windows 用户）

**下载安装：**
- iPhone App Store: 搜索 "iVCam"
- Windows: https://www.e2esoft.com/ivcam/

**配置步骤：**

1. **安装并启动**
   - iPhone 安装 iVCam App
   - PC 安装 iVCam 驱动程序
   - 确保两者在同一 WiFi 网络

2. **连接方式选择**

   **方式A：USB连接（推荐）**
   ```python
   CAMERA_MODE = "index"  # USB连接后iPhone会显示为摄像头设备
   CAMERA_INDEX = 1  # 通常是1，如果不行试试2
   ```

   **方式B：WiFi连接**
   ```python
   CAMERA_MODE = "ip"
   CAMERA_URL = "http://192.168.1.XXX:8080/video"  # 替换为实际IP
   ```

3. **获取iPhone IP地址**
   - 打开 iPhone 设置 → WiFi → 点击已连接的网络
   - 查看 IP 地址（例如：192.168.1.105）
   - 在代码中设置：
     ```python
     CAMERA_URL = "http://192.168.1.105:8080/video"
     ```

### 方法 3：EpocCam

**下载：**
- iOS: App Store 搜索 "EpocCam"
- Windows/Mac: https://www.kinoni.com/

**配置：**
```python
CAMERA_MODE = "index"  # USB模式
CAMERA_INDEX = 1

# 或者使用WiFi模式
CAMERA_MODE = "ip"
CAMERA_URL = "http://iPhone-IP:端口号/video"
```

---

## 🤖 使用安卓手机作为摄像头

### 方法 1：DroidCam（推荐）

**下载安装：**
- Android: Google Play 搜索 "DroidCam"
- Windows: https://www.dev47apps.com/droidcam/windows/
- Linux: https://www.dev47apps.com/droidcam/linux/

**配置步骤：**

1. **安装并连接**
   - 手机和电脑连接同一 WiFi
   - 打开 DroidCam App
   - 记下显示的 IP 和端口（例如：192.168.1.100:4747）

2. **代码配置**
   ```python
   CAMERA_MODE = "ip"
   CAMERA_URL = "http://192.168.1.100:4747/video"
   ```

3. **测试连接**
   ```bash
   # 在浏览器中访问测试
   http://192.168.1.100:4747/video
   ```

### 方法 2：IP Webcam

**下载：** Google Play 搜索 "IP Webcam"

**配置：**
```python
CAMERA_MODE = "ip"
CAMERA_URL = "http://192.168.1.XXX:8080/video"
```

---

## ⚙️ 配置选项详解

### 1. 默认摄像头模式

```python
CAMERA_MODE = "default"
```
自动使用系统默认摄像头（通常是索引 0）

### 2. 指定索引模式

```python
CAMERA_MODE = "index"
CAMERA_INDEX = 1  # 尝试不同的数字：0, 1, 2, 3...
```

**如何找到正确的索引？**

创建测试脚本 `test_camera_index.py`：
```python
import cv2

for i in range(5):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"✓ 摄像头索引 {i} 可用")
        ret, frame = cap.read()
        if ret:
            print(f"  分辨率: {frame.shape[1]}x{frame.shape[0]}")
        cap.release()
    else:
        print(f"✗ 摄像头索引 {i} 不可用")
```

### 3. IP摄像头模式

```python
CAMERA_MODE = "ip"
CAMERA_URL = "http://192.168.1.100:8080/video"  # HTTP流
# 或
CAMERA_URL = "rtsp://192.168.1.100:8554/live"   # RTSP流
```

**支持的URL格式：**
- HTTP: `http://IP:端口/video`
- RTSP: `rtsp://IP:端口/stream`
- MJPEG: `http://IP:端口/mjpeg`

### 4. 视频文件测试模式

```python
CAMERA_MODE = "file"
VIDEO_FILE_PATH = "./test_video.mp4"  # 支持 .mp4, .avi, .mov 等
```

### 5. 禁用视频模式

```python
CAMERA_MODE = "disable"
```
仅使用音频，不启动视频功能。适合：
- 没有摄像头设备
- 只需要语音对话功能
- 减少系统资源占用

---

## 🔧 常见问题

### Q1: "无法打开摄像头或视频源" 错误

**解决方案：**

1. **检查设备连接**
   ```bash
   # Windows: 设备管理器 → 摄像头
   # Linux: 运行命令
   ls /dev/video*
   ```

2. **检查权限**
   - Windows: 设置 → 隐私 → 摄像头 → 允许应用访问
   - macOS: 系统偏好设置 → 安全与隐私 → 摄像头

3. **检查其他程序占用**
   - 关闭 Zoom、Skype、Teams 等视频会议软件
   - 关闭浏览器中使用摄像头的标签页

### Q2: IP摄像头连接失败

**检查清单：**

- [ ] 手机和电脑在同一 WiFi 网络
- [ ] 手机摄像头 APP 已启动
- [ ] IP 地址正确（手机 IP 可能会变化）
- [ ] 端口号正确
- [ ] 防火墙未阻止连接
- [ ] 使用浏览器测试 URL 是否能访问

**测试命令：**
```bash
# 测试能否ping通手机
ping 192.168.1.100

# 使用curl测试URL（Linux/Mac）
curl -I http://192.168.1.100:8080/video
```

### Q3: 画面卡顿或延迟高

**优化方案：**

1. **使用 USB 连接**（iVCam/EpocCam 支持）
   ```python
   CAMERA_MODE = "index"  # USB连接延迟更低
   ```

2. **降低分辨率**
   ```python
   # 在 video_recorder() 函数后添加
   cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
   cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
   ```

3. **使用 5GHz WiFi**（比 2.4GHz 更快）

### Q4: iPhone 作为摄像头但识别不到

**方案1：检查驱动**
- iVCam: 确保安装了 PC 端驱动
- EpocCam: 重启电脑后重新连接

**方案2：尝试不同的索引**
```python
CAMERA_MODE = "index"
CAMERA_INDEX = 1  # 尝试 0, 1, 2, 3...
```

**方案3：使用 IP 模式**
```python
CAMERA_MODE = "ip"
# 在 iVCam APP 中查看显示的 IP
```

### Q5: 台式机完全没有摄像头怎么办？

**推荐方案（按优先级）：**

1. **使用手机作为摄像头**（本文档方法）
2. **购买USB摄像头**（20-50元即可）
3. **禁用视频功能**
   ```python
   CAMERA_MODE = "disable"
   ```

---

## 🎯 推荐配置

### 场景 1：笔记本内置摄像头
```python
CAMERA_MODE = "default"
```

### 场景 2：台式机 + iPhone（iVCam USB连接）
```python
CAMERA_MODE = "index"
CAMERA_INDEX = 1
```

### 场景 3：台式机 + 安卓手机（WiFi）
```python
CAMERA_MODE = "ip"
CAMERA_URL = "http://192.168.1.100:4747/video"  # DroidCam
```

### 场景 4：仅语音对话
```python
CAMERA_MODE = "disable"
```

---

## 📚 相关链接

- **iVCam**: https://www.e2esoft.com/ivcam/
- **DroidCam**: https://www.dev47apps.com/
- **EpocCam**: https://www.kinoni.com/
- **IP Webcam**: https://play.google.com/store/apps/details?id=com.pas.webcam

---

## 💡 提示

1. **首次使用建议先测试摄像头是否可用**
2. **USB连接比WiFi更稳定、延迟更低**
3. **确保手机有足够电量或接入充电**
4. **WiFi连接时保持手机和电脑距离路由器近一些**

如有其他问题，请查看项目 Issues 或提交新的 Issue。

