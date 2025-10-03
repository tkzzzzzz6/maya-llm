# 📁 项目结构说明

## 🎯 重构目标

将单文件项目重构为**前后端分离**的模块化架构，提高：
- ✅ 代码可维护性
- ✅ 团队协作效率
- ✅ 功能扩展性
- ✅ 测试便利性

---

## 📂 目录结构

```
maya-llm/
├── src/                          # 源代码目录
│   ├── backend/                  # 后端模块
│   │   ├── __init__.py          # 模块初始化
│   │   ├── config.py            # 配置文件（路径、参数）
│   │   ├── models.py            # 模型加载和管理
│   │   ├── inference.py         # 推理逻辑
│   │   ├── audio_utils.py       # 音频处理工具
│   │   └── memory.py            # 对话记忆管理
│   │
│   └── frontend/                 # 前端模块
│       ├── __init__.py          # 模块初始化
│       ├── ui.py                # Gradio UI界面
│       └── styles.py            # CSS样式定义
│
├── app.py                        # 主入口文件 ⭐
├── start_app.bat                 # Windows 启动脚本
├── start_app.sh                  # Linux/Mac 启动脚本
│
├── docs/                         # 文档目录
│   ├── Project_Structure.md     # 项目结构说明（本文件）
│   ├── API_Reference.md         # API参考文档
│   └── ...
│
├── output/                       # 输出目录（音频、视频）
├── SpeakerVerification_DIR/     # 声纹数据目录
└── requirements.txt              # 依赖列表
```

---

## 🔧 模块详解

### 1. Backend 后端模块

#### `config.py` - 配置管理
```python
# 用途：集中管理所有配置参数
- 环境变量配置
- 路径配置
- 模型配置
- 默认设置
- TTS语音映射

# 优势
- 一处修改，全局生效
- 避免硬编码
- 便于环境切换
```

#### `models.py` - 模型管理
```python
# 用途：模型加载、管理、状态维护
class MayaModels:
    - 加载 ASR 模型（SenseVoice）
    - 加载 LLM 模型（Qwen2.5）
    - 加载 SV 模型（CAM++）
    - 管理对话记忆
    - 提供模型状态查询

# 优势
- 单例模式，避免重复加载
- 统一的模型接口
- 便于添加新模型
```

#### `inference.py` - 推理引擎
```python
# 用途：核心业务逻辑
class InferenceEngine:
    - 声纹注册
    - 语音识别
    - 声纹验证
    - 对话生成（流式）
    - 多模态融合

# 优势
- 业务逻辑独立
- 易于单元测试
- 支持多种推理模式
```

#### `audio_utils.py` - 音频工具
```python
# 用途：音频处理相关工具函数
- 拼音转换
- 唤醒词检测
- 音频时长获取
- 文件夹检查
- TTS 语音合成
- 语种检测

# 优势
- 工具函数复用
- 独立测试
- 易于维护
```

#### `memory.py` - 记忆管理
```python
# 用途：对话历史管理
class ChatMemory:
    - 添加对话
    - 获取上下文
    - 清空历史
    - 历史列表查询

# 优势
- 独立的记忆模块
- 可扩展（数据库存储）
- 灵活的上下文控制
```

---

### 2. Frontend 前端模块

#### `ui.py` - 用户界面
```python
# 用途：Gradio UI界面构建
def create_modern_ui():
    - 创建聊天界面
    - 创建设置面板
    - 创建声纹注册页面
    - 事件绑定
    - 状态管理

# 优势
- UI 与逻辑分离
- 易于界面调整
- 便于 A/B 测试
```

#### `styles.py` - 样式定义
```python
# 用途：CSS样式定义
MODERN_CSS = """
    - 全局样式
    - 组件样式
    - 响应式布局
    - 动画效果
"""

# 优势
- 样式集中管理
- 便于主题切换
- 易于品牌定制
```

---

### 3. 主入口 `app.py`

```python
# 用途：应用启动入口
def main():
    - 参数解析
    - 创建 UI
    - 启用队列
    - 启动服务

# 优势
- 清晰的启动流程
- 统一的入口点
- 便于部署
```

---

## 🔄 数据流

### 完整对话流程

```
用户输入（文字/语音）
    ↓
【前端】ui.py
    ├─ 接收输入
    ├─ 调用后端
    └─ 显示结果
    ↓
【后端】inference.py
    ├─ 语音识别 (audio_utils.py)
    ├─ 唤醒词检测 (audio_utils.py)
    ├─ 声纹验证 (models.py)
    ├─ LLM推理 (models.py)
    ├─ 记忆更新 (memory.py)
    └─ TTS合成 (audio_utils.py)
    ↓
返回结果
    ├─ 文字回复
    └─ 语音文件
    ↓
【前端】ui.py
    ├─ 流式显示文字
    └─ 播放语音
```

---

## 🆚 对比：单文件 vs 模块化

### 旧版（单文件）
```python
maya_webui_modern.py (900+ 行)
├─ 全局变量
├─ 工具函数
├─ 模型类
├─ 推理函数
├─ UI创建
└─ 主函数

❌ 代码耦合度高
❌ 难以测试
❌ 维护困难
❌ 团队协作冲突多
```

### 新版（模块化）
```python
src/
├─ backend/
│   ├─ config.py      (100行)
│   ├─ models.py      (150行)
│   ├─ inference.py   (200行)
│   ├─ audio_utils.py (100行)
│   └─ memory.py      (50行)
│
└─ frontend/
    ├─ ui.py          (250行)
    └─ styles.py      (150行)

✅ 模块独立
✅ 易于测试
✅ 职责清晰
✅ 便于协作
```

---

## 🚀 使用方式

### 启动应用

**方式1：直接运行**
```bash
python app.py
```

**方式2：使用脚本**
```bash
# Windows
start_app.bat

# Linux/Mac
sh start_app.sh
```

**方式3：命令行参数**
```bash
# 指定端口
python app.py --port 8080

# 生成公网链接
python app.py --share

# 指定服务器地址
python app.py --server-name 0.0.0.0
```

---

### 开发使用

#### 1. 修改后端逻辑
```python
# 修改 src/backend/inference.py
# 例如：添加新的推理模式

class InferenceEngine:
    def new_inference_method(self):
        # 你的代码
        pass
```

#### 2. 修改前端界面
```python
# 修改 src/frontend/ui.py
# 例如：添加新的UI组件

def create_modern_ui():
    # 添加新组件
    new_component = gr.Something()
```

#### 3. 修改样式
```python
# 修改 src/frontend/styles.py
# 例如：调整颜色主题

MODERN_CSS = """
/* 修改主色调 */
--primary-color: #your-color;
"""
```

#### 4. 修改配置
```python
# 修改 src/backend/config.py
# 例如：更换模型

MODEL_CONFIG = {
    "llm": {
        "model_id": "your/new-model",
        ...
    }
}
```

---

## 🧪 测试

### 单元测试

```python
# tests/test_audio_utils.py
import pytest
from src.backend.audio_utils import check_wake_word

def test_wake_word_detection():
    assert check_wake_word("站起来，你好", "站起来") == True
    assert check_wake_word("你好", "站起来") == False

# tests/test_memory.py
from src.backend.memory import ChatMemory

def test_memory():
    memory = ChatMemory()
    memory.add_to_history("hello", "hi")
    assert len(memory.history) == 2
```

### 运行测试
```bash
pytest tests/
```

---

## 📦 部署

### Docker 部署
```dockerfile
# Dockerfile
FROM python:3.10

WORKDIR /app
COPY src/ /app/src/
COPY app.py /app/
COPY requirements.txt /app/

RUN pip install -r requirements.txt

CMD ["python", "app.py"]
```

### 构建镜像
```bash
docker build -t maya-voice-assistant .
docker run -p 7860:7860 maya-voice-assistant
```

---

## 🔮 扩展方向

### 1. 添加新后端模块
```python
src/backend/
└── database.py      # 数据库操作
└── cache.py         # 缓存管理
└── api.py           # API接口
```

### 2. 添加新前端页面
```python
src/frontend/
└── admin_ui.py      # 管理界面
└── mobile_ui.py     # 移动端界面
```

### 3. 微服务拆分
```
maya-llm/
├── asr-service/     # 语音识别服务
├── llm-service/     # 大模型服务
├── tts-service/     # 语音合成服务
└── web-ui/          # Web前端
```

---

## 📊 性能优化

### 后端优化
- 模型缓存
- 批量推理
- 异步处理
- 队列管理

### 前端优化
- 流式输出
- 懒加载
- 缓存策略
- CDN加速

---

## 🤝 团队协作

### 开发分工

**后端开发**
- 负责 `src/backend/` 目录
- 实现业务逻辑
- 优化模型性能

**前端开发**
- 负责 `src/frontend/` 目录
- 设计用户界面
- 优化用户体验

**全栈开发**
- 负责 `app.py` 集成
- 协调前后端对接
- 系统部署运维

### Git 工作流
```bash
# 后端开发分支
git checkout -b feature/backend-xxx

# 前端开发分支
git checkout -b feature/frontend-xxx

# 合并到主分支
git checkout main
git merge feature/xxx
```

---

## 📚 相关文档

- **API参考**: `docs/API_Reference.md`
- **部署指南**: `docs/Deployment_Guide.md`
- **开发规范**: `docs/Development_Guide.md`
- **版本对比**: `docs/UI_Comparison.md`

---

## ✅ 总结

**重构优势**
- ✨ 代码更清晰
- ✨ 维护更容易
- ✨ 扩展更灵活
- ✨ 协作更高效

**项目特点**
- 🎯 职责分明
- 🔧 模块独立
- 📦 易于部署
- 🚀 便于扩展

🦆 **欢迎参与项目开发！**

