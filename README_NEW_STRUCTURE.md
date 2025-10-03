# 🦆 麻鸭语音助手 v2.0 - 前后端分离版

## 🎉 重大更新

项目已重构为**前后端分离**架构！

---

## ✨ 新特性

### 1. 模块化架构
```
src/
├── backend/   # 后端逻辑（Python）
└── frontend/  # 前端界面（Gradio）
```

### 2. 录音功能优化 ✅
- 🎙️ **修复录音按钮** - 点击开始，再次点击停止
- 💡 **使用提示** - 界面上有详细说明
- 🔄 **状态反馈** - 录音状态可见

### 3. 代码质量提升
- ✅ 职责分离
- ✅ 易于测试
- ✅ 便于维护
- ✅ 团队协作友好

---

## 🚀 快速开始

### 方式1：一键启动（推荐）

**Windows:**
```bash
start_app.bat
```

**Linux/Mac:**
```bash
chmod +x start_app.sh
sh start_app.sh
```

### 方式2：Python 命令
```bash
python app.py
```

### 方式3：自定义参数
```bash
# 指定端口
python app.py --port 8080

# 生成公网链接
python app.py --share
```

---

## 📁 项目结构

```
maya-llm/
├── 📂 src/                      源代码
│   ├── 📂 backend/              后端模块
│   │   ├── config.py           配置管理
│   │   ├── models.py           模型加载
│   │   ├── inference.py        推理引擎
│   │   ├── audio_utils.py      音频工具
│   │   └── memory.py           对话记忆
│   │
│   └── 📂 frontend/             前端模块
│       ├── ui.py               界面定义
│       └── styles.py           样式管理
│
├── 📄 app.py                    主入口 ⭐
├── 🚀 start_app.bat             Windows启动
├── 🚀 start_app.sh              Linux/Mac启动
│
├── 📂 docs/                     文档目录
│   ├── Project_Structure.md   项目结构说明
│   ├── Maya_WebUI_Guide.md    使用指南
│   └── UI_Comparison.md       版本对比
│
├── 📂 output/                   输出目录
├── 📂 SpeakerVerification_DIR/ 声纹目录
└── 📄 requirements.txt          依赖列表
```

---

## 🎯 核心改进

### 后端模块化

| 模块 | 功能 | 文件大小 |
|------|------|---------|
| `config.py` | 配置管理 | ~100行 |
| `models.py` | 模型加载 | ~150行 |
| `inference.py` | 推理逻辑 | ~200行 |
| `audio_utils.py` | 音频处理 | ~100行 |
| `memory.py` | 对话记忆 | ~50行 |

**优势：**
- ✅ 每个模块职责单一
- ✅ 易于单元测试
- ✅ 便于并行开发

### 前端模块化

| 模块 | 功能 | 文件大小 |
|------|------|---------|
| `ui.py` | 界面构建 | ~250行 |
| `styles.py` | CSS样式 | ~150行 |

**优势：**
- ✅ UI与逻辑分离
- ✅ 样式独立管理
- ✅ 易于主题切换

---

## 🔧 录音功能说明

### 问题修复

**旧版问题：**
❌ 录音按钮点击无反应
❌ 无法暂停/停止录音
❌ 没有状态提示

**新版改进：**
✅ 点击开始录音
✅ 再次点击停止
✅ 录音后点击"发送"
✅ 界面有使用提示

### 使用步骤

```
1. 点击 🎙️ 录音按钮
   → 开始录音（可能会有红点指示）

2. 说话
   → 录制你的语音

3. 再次点击 🎙️ 按钮
   → 停止录音

4. 点击 📤 发送
   → 开始处理
```

### 浏览器权限

首次使用需要允许麦克风权限：
- Chrome: 设置 → 隐私和安全 → 网站设置 → 麦克风
- Firefox: 设置 → 隐私与安全 → 权限 → 麦克风
- Edge: 类似 Chrome

---

## 📖 使用指南

### 1. 加载模型
```
1. 打开浏览器访问 http://localhost:7860
2. 点击右侧"⚙️ 设置"标签
3. 点击"🚀 加载模型"
4. 等待1-3分钟（首次需下载）
```

### 2. 开始对话

#### 文字对话（最简单）
```
1. 在底部输入框输入："你好"
2. 点击"📤 发送"
3. 等待回复（流式显示）
```

#### 语音对话
```
1. 点击 🎙️ 录音按钮
2. 说话："站起来，今天天气怎么样？"
3. 再次点击 🎙️ 停止
4. 点击"📤 发送"
5. 收到文字和语音回复
```

### 3. 声纹注册（可选）
```
1. 点击"👤 声纹"标签
2. 录制3-10秒清晰语音
3. 点击"✅ 注册声纹"
4. 在设置中开启"声纹验证"
```

---

## 🆚 版本对比

| 特性 | 旧版（单文件） | 新版（模块化） |
|------|---------------|---------------|
| **文件结构** | 1个文件 900+行 | 多模块 ~150行/个 |
| **代码组织** | 耦合 | 解耦 |
| **可维护性** | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| **可扩展性** | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| **团队协作** | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| **录音功能** | ❌ 有问题 | ✅ 已修复 |
| **功能** | 完整 | 完整 + 更好 |

---

## 🔄 迁移指南

### 从旧版迁移

**旧版文件：**
- `maya_webui_modern.py` - 单文件版本

**新版文件：**
- `app.py` - 新入口
- `src/backend/` - 后端模块
- `src/frontend/` - 前端模块

**迁移步骤：**
1. ✅ 旧版仍然可用（保留作为参考）
2. ✅ 新版独立运行（不冲突）
3. ✅ 使用 `app.py` 启动新版
4. ✅ 配置和数据目录共享

---

## 🛠️ 开发指南

### 修改后端逻辑
```python
# 编辑 src/backend/inference.py
class InferenceEngine:
    def new_feature(self):
        # 添加新功能
        pass
```

### 修改前端界面
```python
# 编辑 src/frontend/ui.py
def create_modern_ui():
    # 修改UI布局
    new_component = gr.Something()
```

### 修改样式
```python
# 编辑 src/frontend/styles.py
MODERN_CSS = """
/* 自定义样式 */
--primary-color: #your-color;
"""
```

### 修改配置
```python
# 编辑 src/backend/config.py
MODEL_CONFIG = {
    "llm": {
        "model_id": "your/model",
        ...
    }
}
```

---

## 🧪 测试

### 运行测试
```bash
# 安装测试依赖
pip install pytest

# 运行测试
pytest tests/

# 测试覆盖率
pytest --cov=src tests/
```

### 单元测试示例
```python
# tests/test_audio_utils.py
from src.backend.audio_utils import check_wake_word

def test_wake_word():
    assert check_wake_word("站起来你好", "站起来") == True
```

---

## 📦 部署

### Docker 部署
```bash
# 构建镜像
docker build -t maya-voice-assistant .

# 运行容器
docker run -p 7860:7860 maya-voice-assistant
```

### 云服务部署
详见：`docs/Deployment_Guide.md`

---

## 🐛 故障排除

### 问题1：模块导入错误
```
ModuleNotFoundError: No module named 'src'
```

**解决：**
```bash
# 确保在项目根目录运行
cd maya-llm
python app.py
```

### 问题2：录音不工作
```
点击录音按钮没反应
```

**解决：**
1. 检查浏览器麦克风权限
2. 刷新页面重试
3. 尝试不同浏览器（推荐Chrome）
4. 查看浏览器控制台错误

### 问题3：模型加载失败
```
❌ 模型加载失败
```

**解决：**
1. 检查网络连接
2. 查看磁盘空间（需要5GB+）
3. 重启程序重试

---

## 📚 文档

- 📘 **项目结构**: `docs/Project_Structure.md`
- 📗 **使用指南**: `docs/Maya_WebUI_Guide.md`
- 📙 **版本对比**: `docs/UI_Comparison.md`
- 📕 **快速开始**: `MODERN_QUICKSTART.md`

---

## 🤝 贡献

欢迎贡献代码！

### 贡献流程
```bash
# 1. Fork 项目
# 2. 创建分支
git checkout -b feature/your-feature

# 3. 提交代码
git commit -m "Add: your feature"

# 4. 推送分支
git push origin feature/your-feature

# 5. 创建 Pull Request
```

### 代码规范
- Python: PEP 8
- 注释: 中英文混合
- 文档: Markdown
- 提交: Conventional Commits

---

## 📊 性能

| 指标 | 数值 |
|------|------|
| 首次启动 | 1-3分钟 |
| 后续启动 | <10秒 |
| 语音识别 | ~2秒 |
| LLM推理 | ~3-5秒 |
| 语音合成 | ~2秒 |
| 总响应时间 | ~7-9秒 |

---

## 📄 许可证

MIT License

---

## 🎉 总结

### 重点改进
1. ✅ **模块化架构** - 前后端分离
2. ✅ **录音功能修复** - 可以正常使用
3. ✅ **代码质量** - 更易维护和扩展
4. ✅ **开发体验** - 更好的协作支持

### 推荐使用
- 🌟 **日常使用** → `python app.py`
- 🔧 **开发调试** → 模块化结构更方便
- 👥 **团队协作** → 清晰的目录结构

---

## 🦆 开始使用

```bash
# 启动应用
python app.py

# 浏览器访问
http://localhost:7860
```

**祝您使用愉快！** 🎉

