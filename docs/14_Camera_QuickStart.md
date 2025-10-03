# 📷 14号文件摄像头快速配置

## 适用文件
`14_SenceVoice_QWen2VL_edgeTTS_realTime.py` - 多模态视觉+语音助手

---

## 🎯 快速配置（3步搞定）

### 台式机无摄像头用户

#### 方案1：使用iPhone（推荐）

**第1步：下载iVCam**
- iPhone: App Store搜索 "iVCam"
- 电脑: https://www.e2esoft.com/ivcam/

**第2步：连接**
- USB连接iPhone和电脑
- 打开iVCam App
- 电脑会自动识别

**第3步：修改配置**
```python
# 在 14_SenceVoice_QWen2VL_edgeTTS_realTime.py 第44行
CAMERA_MODE = "index"
CAMERA_INDEX = 1  # iPhone通常是索引1
```

#### 方案2：使用安卓手机

**第1步：下载DroidCam**
- 手机: Google Play搜索 "DroidCam"
- 电脑: https://www.dev47apps.com/

**第2步：连接WiFi**
- 确保手机和电脑在同一WiFi
- 打开DroidCam App
- 记下显示的IP地址（如：192.168.1.100）

**第3步：修改配置**
```python
# 在 14_SenceVoice_QWen2VL_edgeTTS_realTime.py 第44行
CAMERA_MODE = "ip"
# 第56行修改IP为你的手机IP
CAMERA_URL = "http://192.168.1.100:4747/video"
```

#### 方案3：暂时不用视频功能

```python
# 在 14_SenceVoice_QWen2VL_edgeTTS_realTime.py 第44行
CAMERA_MODE = "disable"
```

---

## 🔍 如何找到摄像头索引？

运行测试脚本：
```bash
python test_camera_index.py
```

输出示例：
```
✓ 摄像头索引 0 可用
  分辨率: 1280x720
  帧率: 30.0 FPS

✓ 摄像头索引 1 可用  ← iPhone/外接摄像头
  分辨率: 1920x1080
  帧率: 30.0 FPS
```

然后在代码中使用对应的索引。

---

## 📱 各种手机APP对比

| APP | 平台 | 连接方式 | 延迟 | 画质 | 价格 |
|-----|------|---------|------|------|------|
| iVCam | iOS/Android | USB/WiFi | 低 | 高 | 免费版够用 |
| DroidCam | Android | USB/WiFi | 中 | 中 | 免费 |
| EpocCam | iOS/Android | USB/WiFi | 低 | 高 | 有免费版 |
| IP Webcam | Android | WiFi | 中 | 中 | 免费 |

**推荐：**
- iPhone用户 → iVCam（USB连接）
- Android用户 → DroidCam（WiFi连接）

---

## ⚠️ 常见问题速查

### 问题1：提示"无法打开摄像头"

**解决：**
```bash
# 1. 运行测试脚本找到正确索引
python test_camera_index.py

# 2. 关闭占用摄像头的程序
# - 关闭Zoom、Skype、Teams
# - 关闭浏览器中的视频会议页面

# 3. 检查权限
# Windows: 设置 → 隐私 → 摄像头 → 允许
```

### 问题2：IP摄像头连接失败

**检查清单：**
```bash
# ✓ 同一WiFi网络
# ✓ 手机APP已启动
# ✓ IP地址正确（设置→WiFi→查看IP）
# ✓ 防火墙未阻止

# 测试连接：在浏览器访问
http://你的手机IP:端口/video
```

### 问题3：画面卡顿

**优化方案：**
- 使用USB连接（比WiFi快）
- 使用5GHz WiFi（比2.4GHz快）
- 降低分辨率

---

## 📖 详细文档

完整配置教程和高级选项请查看：
👉 [docs/Camera_Setup_Guide.md](./Camera_Setup_Guide.md)

---

## 💡 小贴士

1. **首次使用先测试**：运行 `python test_camera_index.py` 确认摄像头可用
2. **USB优先**：USB连接比WiFi更稳定、延迟更低
3. **保持充电**：手机作为摄像头时保持充电状态
4. **网络稳定**：WiFi模式下尽量靠近路由器

---

祝您使用愉快！🎉

