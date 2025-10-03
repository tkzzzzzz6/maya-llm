# 🔧 故障排除指南

## 模型加载失败

### 错误：`list index out of range`

**可能原因**：
1. ASR 模型返回空结果
2. 模型未正确加载
3. 网络问题导致模型下载不完整

**解决方案**：

#### 1. 运行诊断脚本
```bash
python test_model_loading.py
```

这会逐步测试每个组件，帮助定位问题。

#### 2. 检查模型缓存
```bash
# 查看 ModelScope 缓存
ls -lh ~/.cache/modelscope/hub/

# 查看 HuggingFace 缓存
ls -lh ~/.cache/huggingface/hub/
```

#### 3. 清空缓存重新下载
```bash
# 清空 ModelScope 缓存
rm -rf ~/.cache/modelscope/

# 清空 HuggingFace 缓存
rm -rf ~/.cache/huggingface/

# 重新启动应用
python app.py
```

#### 4. 手动下载模型

如果自动下载失败，可以手动下载：

```python
from modelscope import snapshot_download

# 下载 SenseVoice
snapshot_download('iic/SenseVoiceSmall', cache_dir='./models')

# 下载 Qwen2.5
snapshot_download('qwen/Qwen2.5-1.5B-Instruct', cache_dir='./models')

# 下载 CAM++
snapshot_download('damo/speech_campplus_sv_zh-cn_16k-common', cache_dir='./models')
```

### 错误：网络连接超时

**解决方案**：

1. **使用镜像源**（已在代码中配置）：
```python
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
```

2. **使用代理**：
```bash
export HTTP_PROXY=http://your-proxy:port
export HTTPS_PROXY=http://your-proxy:port
python app.py
```

3. **离线模式**：
   - 先在有网络的机器上下载模型
   - 复制到目标机器的缓存目录
   - 启动应用

---

## 界面显示问题

### 页脚位置错误

**现象**：页脚信息出现在侧边栏或其他错误位置

**原因**：Gradio Row/Column 嵌套问题

**解决方案**：
已在最新版本中修复。更新代码：
```bash
git pull
```

### 样式不生效

**解决方案**：

1. **清空浏览器缓存**：
   - Chrome: `Ctrl + Shift + Delete`
   - Firefox: `Ctrl + Shift + Delete`
   - 选择"缓存的图片和文件"

2. **强制刷新**：
   - `Ctrl + F5` (Windows)
   - `Cmd + Shift + R` (Mac)

3. **检查 CSS 加载**：
   - F12 打开开发者工具
   - 查看 Console 是否有 CSS 错误

---

## 语音功能问题

### 录音无反应

**检查清单**：
- [ ] 麦克风权限已授予浏览器
- [ ] 使用 HTTPS 或 localhost
- [ ] 浏览器支持 WebRTC（Chrome/Edge 推荐）
- [ ] 麦克风设备正常工作

**测试麦克风**：
```bash
# Linux
arecord -d 3 test.wav
aplay test.wav

# Windows (PowerShell)
# 使用系统录音机测试
```

### 语音识别失败

**可能原因**：
1. 音频格式不支持
2. ASR 模型未加载
3. 音频质量差

**解决方案**：
```python
# 检查模型是否加载
from src.backend.models import maya_models
print(f"模型已加载: {maya_models.is_loaded()}")
print(f"ASR 模型: {maya_models.asr_model}")
```

### TTS 无声音

**检查清单**：
- [ ] "语音合成"选项已开启
- [ ] 系统音量不为 0
- [ ] 浏览器允许自动播放音频
- [ ] 网络连接正常（Edge TTS 需联网）

---

## 性能问题

### 模型加载慢

**优化方案**：

1. **使用 SSD 存储模型**
2. **增加系统内存**
3. **使用量化模型**：
```python
# 修改 config.py
MODEL_CONFIG = {
    "llm": {
        "model_id": "qwen/Qwen2.5-1.5B-Instruct-GPTQ-Int4",  # 量化版本
        ...
    }
}
```

### 推理速度慢

**优化方案**：

1. **使用 GPU**：
```python
# 检查 CUDA
import torch
print(torch.cuda.is_available())
print(torch.cuda.get_device_name(0))
```

2. **减少 max_new_tokens**：
```python
DEFAULT_SETTINGS = {
    "max_new_tokens": 256,  # 从 512 减少到 256
    ...
}
```

3. **启用流式输出**：
   - 已默认启用
   - 提升感知速度

---

## 常见错误代码

### ImportError: No module named 'xxx'

**解决方案**：
```bash
# 安装缺失的包
pip install xxx

# 或重新安装所有依赖
pip install -r requirements.txt
```

### CUDA out of memory

**解决方案**：

1. **减少批处理大小**
2. **使用 CPU**：
```python
MODEL_CONFIG = {
    "llm": {
        "device_map": "cpu",  # 改为 CPU
        ...
    }
}
```

3. **使用小模型**：
   - Qwen2.5-0.5B-Instruct（更小更快）

### Permission denied

**解决方案**：
```bash
# 给予执行权限
chmod +x start_maya_modern.sh

# 或使用管理员权限
sudo python app.py
```

---

## 获取帮助

如果以上方法都无法解决问题：

1. **运行诊断脚本**：
```bash
python test_model_loading.py > diagnostic.log 2>&1
```

2. **收集日志**：
```bash
python app.py --debug 2>&1 | tee app.log
```

3. **提交 Issue**：
   - GitHub Issues: [链接]
   - 附上诊断日志
   - 说明操作系统和 Python 版本

---

## 调试技巧

### 查看详细日志

```bash
# 启用调试模式
python app.py --debug

# 或设置环境变量
export GRADIO_DEBUG=1
python app.py
```

### Python 交互式测试

```python
# 启动 Python 解释器
python

# 测试导入
>>> from src.backend.models import maya_models
>>> maya_models.is_loaded()
False

# 测试加载
>>> for status in maya_models.load_models():
...     print(status)
```

### 查看 Gradio 日志

F12 打开浏览器开发者工具 → Console 标签

---

## 环境要求

### 最低配置
- CPU: 4 核
- RAM: 8GB
- 磁盘: 10GB 可用空间
- Python: 3.8+

### 推荐配置
- CPU: 8 核
- RAM: 16GB
- GPU: NVIDIA GPU (4GB+ VRAM)
- 磁盘: 20GB SSD
- Python: 3.10

---

更多问题？查看 [CLAUDE.md](./CLAUDE.md) 或 [CLAUDE_UI_README.md](./CLAUDE_UI_README.md)
