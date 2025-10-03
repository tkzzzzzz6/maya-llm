# 🎙️ CosyVoice WebUI 使用指南

## 📖 概述

`webui.py` 是 CosyVoice 的图形化界面（Web UI），基于 Gradio 构建，提供了友好的交互界面用于语音合成。

---

## 🚀 快速启动

### 方法1：自动下载模型（推荐）

```bash
# 使用默认模型 (CosyVoice-300M)
python webui.py

# 指定端口
python webui.py --port 8080

# 使用其他模型
python webui.py --model_dir iic/CosyVoice-300M-Instruct
python webui.py --model_dir iic/CosyVoice-300M-SFT
```

### 方法2：使用本地模型

```bash
# 如果已经下载了模型到本地
python webui.py --model_dir ./pretrained_models/CosyVoice-300M --use_local

# 或者直接指定本地路径（会自动检测）
python webui.py --model_dir /path/to/your/local/model
```

---

## 🎯 可用模型

| 模型 ID | 说明 | 支持功能 |
|---------|------|----------|
| `iic/CosyVoice-300M` | 标准版 | 预训练音色、3s极速复刻、跨语种复刻 |
| `iic/CosyVoice-300M-Instruct` | 指令版 | 所有功能 + 自然语言控制 |
| `iic/CosyVoice-300M-SFT` | 微调版 | 预训练音色（更多音色选择） |

### 启动不同模型

```bash
# CosyVoice-300M (默认，支持音色克隆)
python webui.py --model_dir iic/CosyVoice-300M

# CosyVoice-300M-Instruct (支持自然语言控制)
python webui.py --model_dir iic/CosyVoice-300M-Instruct

# CosyVoice-300M-SFT (更多预训练音色)
python webui.py --model_dir iic/CosyVoice-300M-SFT
```

---

## 🎨 四大功能模式

### 1. 预训练音色

**适用场景**：快速生成常见音色的语音

**使用步骤**：
1. 选择"预训练音色"模式
2. 从下拉菜单选择音色（中文女、中文男、日语男、粤语女、英文女、英文男、韩语女）
3. 输入要合成的文本
4. 点击"生成音频"

**示例**：
```
输入文本: "你好，我是CosyVoice语音合成系统"
选择音色: 中文女
```

---

### 2. 3s极速复刻

**适用场景**：用3秒以上的音频样本快速克隆声音

**使用步骤**：
1. 选择"3s极速复刻"模式
2. 上传或录制 prompt 音频（**3-30秒，采样率≥16kHz**）
3. 输入 prompt 文本（**必须与音频内容一致**）
4. 输入要合成的文本
5. 点击"生成音频"

**示例**：
```
Prompt音频: [录制3秒："大家好，我是小明"]
Prompt文本: "大家好，我是小明"
合成文本: "今天天气真不错，适合出去散步"
→ 输出：用小明的声音说"今天天气真不错..."
```

**注意事项**：
- ✅ 音频质量越好，克隆效果越好
- ✅ 3-10秒为最佳时长
- ❌ 避免背景噪音
- ❌ Prompt文本必须准确对应音频内容

---

### 3. 跨语种复刻

**适用场景**：用中文音色说英文，或用英文音色说中文

**使用步骤**：
1. 选择"跨语种复刻"模式
2. 上传 prompt 音频（某种语言）
3. 输入要合成的文本（**不同语言**）
4. 点击"生成音频"

**示例**：
```
Prompt音频: [中文音色："你好，世界"]
合成文本: "Hello, how are you today?"
→ 输出：用中文音色说英文
```

**可用模型**：仅 `iic/CosyVoice-300M`

---

### 4. 自然语言控制

**适用场景**：用自然语言描述想要的语音风格

**使用步骤**：
1. 选择"自然语言控制"模式
2. 选择基础音色
3. 输入 instruct 文本（**描述语音风格**）
4. 输入要合成的文本
5. 点击"生成音频"

**示例**：
```
选择音色: 中文女
Instruct文本: "用激动兴奋的语气说话，语速稍快"
合成文本: "我们终于成功了！"
→ 输出：激动兴奋风格的语音
```

**Instruct 文本示例**：
- "用温柔轻柔的声音说话"
- "用严肃正式的语气"
- "带有笑声，语速较慢"
- "表达悲伤的情绪"

**可用模型**：仅 `iic/CosyVoice-300M-Instruct`

---

## ⚙️ 高级选项

### 流式推理

- **关闭流式**：等待完整音频生成后播放（质量更好）
- **开启流式**：边生成边播放（延迟更低）

### 速度调节

- 范围：0.5x - 2.0x
- 默认：1.0x
- **注意**：仅支持非流式推理模式

### 随机种子

- 点击 🎲 按钮生成随机种子
- 相同的种子 + 相同的输入 = 相同的输出
- 用于复现结果

---

## 🎯 使用场景推荐

| 场景 | 推荐模式 | 推荐模型 |
|------|---------|---------|
| 快速生成标准音色 | 预训练音色 | 300M-SFT |
| 克隆特定人声 | 3s极速复刻 | 300M |
| 多语言播报 | 跨语种复刻 | 300M |
| 情感化播报 | 自然语言控制 | 300M-Instruct |
| 有声书录制 | 3s极速复刻 + 速度调节 | 300M |
| 角色配音 | 自然语言控制 | 300M-Instruct |

---

## 🔧 命令行参数

```bash
python webui.py [参数]

参数说明：
  --port PORT              指定端口号 (默认: 8000)
  --model_dir MODEL_DIR    模型ID或本地路径 (默认: iic/CosyVoice-300M)
  --use_local              强制使用本地路径模式
```

**示例**：

```bash
# 在 8080 端口启动，使用 Instruct 模型
python webui.py --port 8080 --model_dir iic/CosyVoice-300M-Instruct

# 使用本地模型
python webui.py --model_dir ./my_models/CosyVoice-300M --use_local

# 使用本地模型（自动检测）
python webui.py --model_dir E:/Models/CosyVoice-300M
```

---

## 🌐 访问界面

启动后，浏览器访问：
```
http://localhost:8000
```

或从其他设备访问（同一网络）：
```
http://你的电脑IP:8000
```

---

## 📊 模型缓存位置

首次运行会自动下载模型到：
```
~/.cache/modelscope/hub/iic/CosyVoice-300M/
```

Windows 用户：
```
C:\Users\你的用户名\.cache\modelscope\hub\iic\CosyVoice-300M\
```

---

## 💡 最佳实践

### 获得最佳音质

1. **使用高质量 prompt 音频**
   - 采样率 ≥ 16kHz
   - 无背景噪音
   - 清晰的人声

2. **Prompt 文本要准确**
   - 必须与音频内容完全一致
   - 包括标点符号

3. **合适的音频长度**
   - 3s极速复刻：3-10秒最佳
   - 跨语种复刻：5-15秒最佳

4. **选择合适的推理模式**
   - 质量优先：关闭流式推理
   - 速度优先：开启流式推理

### 提高生成速度

1. 使用流式推理
2. 使用 GPU（自动检测）
3. 减少合成文本长度
4. 使用 SFT 模型（更轻量）

---

## ⚠️ 常见问题

### Q1: 启动时提示模型下载失败

**解决方案**：
```bash
# 设置 ModelScope 镜像（可选）
export MODELSCOPE_CACHE=~/.cache/modelscope

# 或手动下载后使用本地路径
python webui.py --model_dir /path/to/model --use_local
```

### Q2: 3s极速复刻效果不好

**检查清单**：
- [ ] Prompt 音频采样率是否 ≥ 16kHz
- [ ] Prompt 文本是否与音频完全一致
- [ ] 音频是否有背景噪音
- [ ] 音频长度是否 3-10 秒
- [ ] 是否使用了正确的模型（300M）

### Q3: 自然语言控制不起作用

**原因**：使用了错误的模型

**解决**：
```bash
# 必须使用 Instruct 模型
python webui.py --model_dir iic/CosyVoice-300M-Instruct
```

### Q4: 跨语种复刻不支持

**原因**：使用了 Instruct 模型

**解决**：
```bash
# 必须使用标准 300M 模型
python webui.py --model_dir iic/CosyVoice-300M
```

### Q5: 生成的音频有杂音

**可能原因**：
1. Prompt 音频质量差
2. 合成文本包含特殊字符
3. 音频后处理问题

**解决方案**：
- 使用高质量的 prompt 音频
- 移除特殊字符和emoji
- 尝试不同的随机种子

---

## 🔄 模型对比

| 特性 | 300M | 300M-SFT | 300M-Instruct |
|------|------|----------|---------------|
| 预训练音色 | ✅ 7种 | ✅ 更多 | ✅ 7种 |
| 3s极速复刻 | ✅ | ❌ | ❌ |
| 跨语种复刻 | ✅ | ❌ | ❌ |
| 自然语言控制 | ❌ | ❌ | ✅ |
| 模型大小 | 约300M | 约300M | 约300M |
| 推荐用途 | 音色克隆 | 标准播报 | 情感化合成 |

---

## 📚 相关链接

- **CosyVoice GitHub**: https://github.com/FunAudioLLM/CosyVoice
- **ModelScope 模型库**: https://www.modelscope.cn/models/iic/CosyVoice-300M
- **Gradio 文档**: https://www.gradio.app/docs

---

## 🎓 进阶使用

### 集成到自己的项目

```python
from cosyvoice.cli.cosyvoice import CosyVoice
from modelscope import snapshot_download

# 下载并加载模型
model_path = snapshot_download('iic/CosyVoice-300M')
cosyvoice = CosyVoice(model_path)

# 使用预训练音色
for i in cosyvoice.inference_sft('你好世界', '中文女', stream=False):
    # i['tts_speech'] 是生成的音频 tensor
    pass

# 使用3s极速复刻
for i in cosyvoice.inference_zero_shot(
    '合成文本', 
    'prompt文本', 
    prompt_speech_16k,  # 16kHz 音频 tensor
    stream=False
):
    pass
```

### 批量处理

创建 `batch_tts.py`：
```python
# 见项目示例代码
```

---

希望这个指南对您有帮助！如有疑问，请查看项目 Issues 或提交新问题。 🚀

