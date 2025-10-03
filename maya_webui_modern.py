#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
麻鸭语音助手 - 现代化 Web UI (ChatGPT/Claude 风格)
Maya Voice Assistant - Modern ChatGPT-style Interface

特性：
- 🎨 现代化聊天界面（对话气泡）
- 🌓 深色/浅色主题
- 📱 响应式布局
- 💬 流式输出
- 🎙️ 语音交互
"""

import gradio as gr
import numpy as np
import torch
import wave
import os
import tempfile
import asyncio
from datetime import datetime
from funasr import AutoModel
from transformers import AutoModelForCausalLM, AutoTokenizer
from modelscope.pipelines import pipeline
from modelscope import snapshot_download
import edge_tts
import pygame
import time
import re
from pypinyin import pinyin, Style
import langid
import json

# ========== 配置 ==========
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

# 全局变量
audio_file_count = 0
chat_history = []

# ========== 工具函数 ==========

def extract_chinese_and_convert_to_pinyin(input_string):
    """提取汉字并转换为拼音"""
    chinese_characters = re.findall(r'[\u4e00-\u9fa5]', input_string)
    chinese_text = ''.join(chinese_characters)
    pinyin_result = pinyin(chinese_text, style=Style.NORMAL)
    pinyin_text = ' '.join([item[0] for item in pinyin_result])
    return pinyin_text

def is_folder_empty(folder_path):
    """检测文件夹是否为空"""
    if not os.path.exists(folder_path):
        return True
    entries = os.listdir(folder_path)
    for entry in entries:
        full_path = os.path.join(folder_path, entry)
        if os.path.isfile(full_path):
            return False
    return True

async def text_to_speech(text, voice="zh-CN-XiaoyiNeural"):
    """异步文字转语音"""
    output_file = tempfile.mktemp(suffix=".mp3")
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)
    return output_file

# ========== 对话记忆类 ==========

class ChatMemory:
    def __init__(self, max_length=2048):
        self.history = []
        self.max_length = max_length

    def add_to_history(self, user_input, model_response):
        self.history.append(f"User: {user_input}")
        self.history.append(f"Assistant: {model_response}")

    def get_context(self):
        context = "\n".join(self.history)
        if len(context) > self.max_length:
            context = context[-self.max_length:]
        return context
    
    def clear(self):
        self.history = []

# ========== 模型管理类 ==========

class MayaModels:
    def __init__(self):
        self.models_loaded = False
        self.asr_model = None
        self.llm_model = None
        self.llm_tokenizer = None
        self.sv_pipeline = None
        self.memory = ChatMemory(max_length=512)
        self.sv_enroll_dir = './SpeakerVerification_DIR/enroll_wav/'
        os.makedirs(self.sv_enroll_dir, exist_ok=True)
        os.makedirs('./output', exist_ok=True)
        
    def load_models(self, progress=gr.Progress()):
        """加载所有模型"""
        if self.models_loaded:
            yield "✅ 模型已加载完成"
            return
        
        try:
            yield "📥 正在加载语音识别模型 (SenseVoice)..."
            progress(0.2)
            self.asr_model = AutoModel(
                model="iic/SenseVoiceSmall",
                trust_remote_code=True
            )
            
            yield "📥 正在加载声纹识别模型 (CAM++)..."
            progress(0.4)
            self.sv_pipeline = pipeline(
                task='speaker-verification',
                model='damo/speech_campplus_sv_zh-cn_16k-common',
                model_revision='v1.0.0'
            )
            
            yield "📥 正在加载大语言模型 (Qwen2.5-1.5B)..."
            progress(0.6)
            model_id = "qwen/Qwen2.5-1.5B-Instruct"
            qwen_local_dir = snapshot_download(model_id=model_id)
            
            yield "🔄 初始化大语言模型..."
            progress(0.8)
            self.llm_model = AutoModelForCausalLM.from_pretrained(
                qwen_local_dir,
                torch_dtype="auto",
                device_map="auto",
                trust_remote_code=True
            )
            self.llm_tokenizer = AutoTokenizer.from_pretrained(
                qwen_local_dir,
                trust_remote_code=True
            )
            
            progress(1.0)
            self.models_loaded = True
            yield "✅ 所有模型加载成功！可以开始对话了"
            
        except Exception as e:
            yield f"❌ 模型加载失败: {str(e)}"

# 创建全局模型实例
maya_models = MayaModels()

# ========== 核心功能函数 ==========

def register_voiceprint(audio_file):
    """声纹注册"""
    if audio_file is None:
        return "❌ 请先录制音频"
    
    try:
        # 检查音频长度
        with wave.open(audio_file, 'rb') as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            duration = frames / float(rate)
        
        if duration < 3:
            return f"❌ 音频时长仅 {duration:.1f} 秒，需要至少 3 秒"
        
        # 保存声纹文件
        enroll_path = os.path.join(maya_models.sv_enroll_dir, "enroll_0.wav")
        import shutil
        shutil.copy(audio_file, enroll_path)
        
        return f"✅ 声纹注册成功！音频时长: {duration:.1f} 秒"
        
    except Exception as e:
        return f"❌ 声纹注册失败: {str(e)}"

def speech_to_text(audio_file):
    """语音识别"""
    if audio_file is None:
        return ""
    
    if not maya_models.models_loaded:
        return ""
    
    try:
        res = maya_models.asr_model.generate(
            input=audio_file,
            cache={},
            language="auto",
            use_itn=False,
        )
        
        text = res[0]['text'].split(">")[-1]
        return text
        
    except Exception as e:
        return f"识别失败: {str(e)}"

def verify_speaker(audio_file, threshold=0.35):
    """声纹验证"""
    if audio_file is None:
        return False, 0.0
    
    if not maya_models.models_loaded:
        return False, 0.0
    
    enroll_file = os.path.join(maya_models.sv_enroll_dir, "enroll_0.wav")
    if not os.path.exists(enroll_file):
        return False, 0.0
    
    try:
        sv_score = maya_models.sv_pipeline(
            [enroll_file, audio_file],
            thr=threshold
        )
        
        score = sv_score.get('score', 0.0)
        result = sv_score.get('text', 'no')
        
        return result == "yes", score
            
    except Exception as e:
        return False, 0.0

def check_wake_word(text, wake_word="站起来"):
    """检查唤醒词"""
    text_pinyin = extract_chinese_and_convert_to_pinyin(text)
    wake_word_pinyin = extract_chinese_and_convert_to_pinyin(wake_word)
    
    wake_word_pinyin = wake_word_pinyin.replace(" ", "")
    text_pinyin = text_pinyin.replace(" ", "")
    
    return wake_word_pinyin in text_pinyin

def chat_respond(message, history, audio_input, settings):
    """
    主对话函数 - 流式输出
    settings 格式: {
        "enable_kws": bool,
        "wake_word": str,
        "enable_sv": bool,
        "sv_threshold": float,
        "enable_tts": bool,
        "system_prompt": str
    }
    """
    global audio_file_count
    
    if not maya_models.models_loaded:
        yield history + [("系统", "❌ 请先在设置中加载模型")], None
        return
    
    # 1. 处理输入（文字或语音）
    user_text = message
    if audio_input is not None:
        asr_text = speech_to_text(audio_input)
        if asr_text:
            user_text = asr_text
    
    if not user_text or user_text.strip() == "":
        yield history, None
        return
    
    # 显示用户消息
    history = history + [(user_text, None)]
    yield history, None
    
    # 2. 关键词唤醒检测
    if settings.get("enable_kws", False):
        wake_word = settings.get("wake_word", "站起来")
        if not check_wake_word(user_text, wake_word):
            error_msg = f"⚠️ 未检测到唤醒词「{wake_word}」"
            history[-1] = (user_text, error_msg)
            yield history, None
            return
    
    # 3. 声纹验证
    if settings.get("enable_sv", False) and audio_input is not None:
        sv_threshold = settings.get("sv_threshold", 0.35)
        sv_pass, sv_score = verify_speaker(audio_input, sv_threshold)
        if not sv_pass:
            error_msg = f"⚠️ 声纹验证失败 (相似度: {sv_score:.2f})"
            history[-1] = (user_text, error_msg)
            yield history, None
            return
    
    # 4. 大语言模型推理
    try:
        context = maya_models.memory.get_context()
        prompt_with_context = f"{context}\nUser: {user_text}\n" if context else user_text
        
        system_prompt = settings.get("system_prompt", "你叫小千，是一个18岁的女大学生，性格活泼开朗，说话俏皮简洁，回答问题不会超过50字。")
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt_with_context},
        ]
        
        text = maya_models.llm_tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )
        
        model_inputs = maya_models.llm_tokenizer([text], return_tensors="pt").to(
            maya_models.llm_model.device
        )
        
        generated_ids = maya_models.llm_model.generate(
            **model_inputs,
            max_new_tokens=512,
        )
        
        generated_ids = [
            output_ids[len(input_ids):]
            for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]
        
        output_text = maya_models.llm_tokenizer.batch_decode(
            generated_ids, skip_special_tokens=True
        )[0]
        
        # 流式显示回复
        history[-1] = (user_text, "")
        for i in range(0, len(output_text), 2):
            history[-1] = (user_text, output_text[:i+2])
            yield history, None
            time.sleep(0.02)
        
        history[-1] = (user_text, output_text)
        
        # 更新记忆
        maya_models.memory.add_to_history(user_text, output_text)
        
        # 5. 语音合成
        audio_output = None
        if settings.get("enable_tts", True):
            language, _ = langid.classify(output_text)
            
            language_speaker = {
                "ja": "ja-JP-NanamiNeural",
                "fr": "fr-FR-DeniseNeural",
                "es": "ca-ES-JoanaNeural",
                "de": "de-DE-KatjaNeural",
                "zh": "zh-CN-XiaoyiNeural",
                "en": "en-US-AnaNeural",
            }
            
            voice = language_speaker.get(language, "zh-CN-XiaoyiNeural")
            audio_file_count += 1
            audio_output = asyncio.run(text_to_speech(output_text, voice))
        
        yield history, audio_output
        
    except Exception as e:
        error_msg = f"❌ 出错了: {str(e)}"
        history[-1] = (user_text, error_msg)
        yield history, None

# ========== 现代化 Gradio 界面 ==========

def create_modern_ui():
    """创建现代化界面"""
    
    # 超级现代化的 CSS
    modern_css = """
    /* 全局样式 */
    :root {
        --primary-color: #10a37f;
        --secondary-color: #19c37d;
        --bg-primary: #ffffff;
        --bg-secondary: #f7f7f8;
        --bg-tertiary: #ececf1;
        --text-primary: #0d0d0d;
        --text-secondary: #676767;
        --border-color: #e5e5e5;
        --shadow: 0 2px 8px rgba(0,0,0,0.1);
        --radius: 12px;
    }
    
    /* 深色模式 */
    .dark {
        --bg-primary: #212121;
        --bg-secondary: #2f2f2f;
        --bg-tertiary: #424242;
        --text-primary: #ececf1;
        --text-secondary: #c5c5d2;
        --border-color: #4e4e4e;
        --shadow: 0 2px 8px rgba(0,0,0,0.3);
    }
    
    /* 主容器 */
    .gradio-container {
        max-width: 1400px !important;
        margin: 0 auto !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }
    
    /* 顶部标题栏 */
    .header-bar {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem 2rem;
        border-radius: var(--radius);
        margin-bottom: 2rem;
        box-shadow: var(--shadow);
    }
    
    .header-title {
        color: white;
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .header-subtitle {
        color: rgba(255,255,255,0.9);
        font-size: 1rem;
        margin-top: 0.5rem;
    }
    
    /* 聊天容器 */
    .chatbot-container {
        background: var(--bg-primary);
        border-radius: var(--radius);
        box-shadow: var(--shadow);
        overflow: hidden;
    }
    
    /* 消息气泡样式 */
    .message {
        display: flex;
        gap: 1rem;
        padding: 1.5rem;
        animation: fadeIn 0.3s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .user-message {
        background: var(--bg-secondary);
        border-left: 4px solid var(--primary-color);
    }
    
    .bot-message {
        background: var(--bg-primary);
        border-left: 4px solid #8e8ea0;
    }
    
    /* 输入区域 */
    .input-container {
        background: var(--bg-secondary);
        border-radius: var(--radius);
        padding: 1.5rem;
        box-shadow: var(--shadow);
    }
    
    /* 按钮样式 */
    .primary-btn {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)) !important;
        border: none !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 0.75rem 2rem !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(16,163,127,0.3) !important;
    }
    
    .primary-btn:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(16,163,127,0.4) !important;
    }
    
    /* 设置面板 */
    .settings-panel {
        background: var(--bg-secondary);
        border-radius: var(--radius);
        padding: 1.5rem;
        box-shadow: var(--shadow);
    }
    
    .settings-section {
        margin-bottom: 1.5rem;
        padding-bottom: 1.5rem;
        border-bottom: 1px solid var(--border-color);
    }
    
    .settings-section:last-child {
        border-bottom: none;
        margin-bottom: 0;
        padding-bottom: 0;
    }
    
    /* 状态指示器 */
    .status-indicator {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.875rem;
        font-weight: 500;
    }
    
    .status-success {
        background: #d1fae5;
        color: #065f46;
    }
    
    .status-loading {
        background: #dbeafe;
        color: #1e40af;
    }
    
    .status-error {
        background: #fee2e2;
        color: #991b1b;
    }
    
    /* 特性卡片 */
    .feature-card {
        background: var(--bg-primary);
        border-radius: var(--radius);
        padding: 1.5rem;
        box-shadow: var(--shadow);
        transition: all 0.3s ease;
        border: 1px solid var(--border-color);
    }
    
    .feature-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
    }
    
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 0.75rem;
    }
    
    .feature-title {
        font-size: 1.125rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }
    
    .feature-description {
        color: var(--text-secondary);
        font-size: 0.875rem;
        line-height: 1.5;
    }
    
    /* 响应式 */
    @media (max-width: 768px) {
        .header-title {
            font-size: 1.5rem;
        }
        
        .message {
            padding: 1rem;
        }
    }
    
    /* 加载动画 */
    .loading-dots {
        display: inline-flex;
        gap: 4px;
    }
    
    .loading-dots span {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: var(--primary-color);
        animation: bounce 1.4s infinite ease-in-out both;
    }
    
    .loading-dots span:nth-child(1) { animation-delay: -0.32s; }
    .loading-dots span:nth-child(2) { animation-delay: -0.16s; }
    
    @keyframes bounce {
        0%, 80%, 100% { transform: scale(0); }
        40% { transform: scale(1); }
    }
    
    /* Gradio 组件覆盖 */
    .gr-button {
        border-radius: 8px !important;
    }
    
    .gr-input, .gr-textarea {
        border-radius: 8px !important;
        border-color: var(--border-color) !important;
    }
    
    .gr-input:focus, .gr-textarea:focus {
        border-color: var(--primary-color) !important;
        box-shadow: 0 0 0 3px rgba(16,163,127,0.1) !important;
    }
    """
    
    with gr.Blocks(css=modern_css, theme=gr.themes.Soft(), title="麻鸭语音助手") as demo:
        
        # 隐藏的设置状态
        settings_state = gr.State({
            "enable_kws": False,
            "wake_word": "站起来",
            "enable_sv": False,
            "sv_threshold": 0.35,
            "enable_tts": True,
            "system_prompt": "你叫小千，是一个18岁的女大学生，性格活泼开朗，说话俏皮简洁，回答问题不会超过50字。"
        })
        
        # 标题栏
        gr.HTML("""
        <div class="header-bar">
            <h1 class="header-title">
                <span>🦆</span>
                <span>麻鸭语音助手</span>
            </h1>
            <p class="header-subtitle">
                Maya Voice Assistant - 基于 SenseVoice + CAM++ + Qwen2.5 + Edge TTS
            </p>
        </div>
        """)
        
        with gr.Row():
            # 左侧 - 主聊天区
            with gr.Column(scale=3):
                # 聊天界面
                chatbot = gr.Chatbot(
                    label="",
                    height=600,
                    show_copy_button=True,
                    bubble_full_width=False,
                    avatar_images=(None, "🦆"),
                    elem_classes="chatbot-container"
                )
                
                # 输入区
                with gr.Row():
                    with gr.Column(scale=4):
                        msg = gr.Textbox(
                            label="",
                            placeholder="💬 输入消息... (支持文字和语音)",
                            show_label=False,
                            container=False
                        )
                    with gr.Column(scale=1, min_width=100):
                        audio_input = gr.Audio(
                            source="microphone",
                            type="filepath",
                            label="🎙️",
                            show_label=False
                        )
                
                with gr.Row():
                    send_btn = gr.Button("📤 发送", variant="primary", size="lg", elem_classes="primary-btn")
                    clear_btn = gr.Button("🗑️ 清空", size="lg")
                
                # 音频播放
                audio_output = gr.Audio(label="🔊 语音回复", autoplay=True, visible=True)
            
            # 右侧 - 设置和功能区
            with gr.Column(scale=1):
                with gr.Tabs():
                    # Tab 1: 快速设置
                    with gr.Tab("⚙️ 设置"):
                        gr.Markdown("### 🎛️ 快速设置")
                        
                        with gr.Group():
                            gr.Markdown("#### 模型加载")
                            load_btn = gr.Button("🚀 加载模型", variant="primary", size="sm")
                            load_status = gr.Markdown("请先加载模型")
                        
                        gr.Markdown("---")
                        
                        with gr.Group():
                            gr.Markdown("#### 对话设置")
                            enable_kws = gr.Checkbox(label="🔑 关键词唤醒", value=False)
                            wake_word = gr.Textbox(
                                label="唤醒词",
                                value="站起来",
                                placeholder="输入唤醒词"
                            )
                            
                            enable_sv = gr.Checkbox(label="👤 声纹验证", value=False)
                            sv_threshold = gr.Slider(
                                minimum=0.1,
                                maximum=0.9,
                                value=0.35,
                                step=0.05,
                                label="验证阈值"
                            )
                            
                            enable_tts = gr.Checkbox(label="🔊 语音合成", value=True)
                        
                        gr.Markdown("---")
                        
                        with gr.Group():
                            gr.Markdown("#### AI 人设")
                            system_prompt = gr.Textbox(
                                label="系统提示词",
                                value="你叫小千，是一个18岁的女大学生，性格活泼开朗，说话俏皮简洁，回答问题不会超过50字。",
                                lines=4
                            )
                    
                    # Tab 2: 声纹注册
                    with gr.Tab("👤 声纹"):
                        gr.Markdown("### 🎙️ 声纹注册")
                        gr.Markdown("录制 3-10 秒清晰语音")
                        
                        voiceprint_audio = gr.Audio(
                            source="microphone",
                            type="filepath",
                            label="录制音频"
                        )
                        register_btn = gr.Button("✅ 注册", variant="primary")
                        register_status = gr.Markdown("")
                    
                    # Tab 3: 帮助
                    with gr.Tab("❓ 帮助"):
                        gr.Markdown("""
                        ### 📖 快速开始
                        
                        #### 1️⃣ 加载模型
                        点击"设置"标签中的"加载模型"
                        
                        #### 2️⃣ 开始对话
                        - **文字**: 直接输入消息
                        - **语音**: 点击麦克风录音
                        
                        #### 3️⃣ 高级功能
                        - **唤醒词**: 需要说出特定词才响应
                        - **声纹**: 仅注册用户可用
                        - **人设**: 自定义AI性格
                        
                        ---
                        
                        ### 💡 使用技巧
                        
                        **快速对话**
                        - 关闭唤醒词和声纹验证
                        - 直接打字即可
                        
                        **语音助手**
                        - 开启唤醒词
                        - 录音说："站起来，今天天气怎么样？"
                        
                        **专属助手**
                        - 注册声纹
                        - 开启声纹验证
                        - 只有你能使用
                        
                        ---
                        
                        ### 🎨 主题
                        支持浅色/深色模式
                        (浏览器右下角切换)
                        """)
        
        # 底部功能特性展示
        gr.Markdown("---")
        gr.Markdown("### ✨ 核心功能")
        
        with gr.Row():
            gr.HTML("""
            <div class="feature-card">
                <div class="feature-icon">🎙️</div>
                <div class="feature-title">语音识别</div>
                <div class="feature-description">SenseVoice 高精度中英文识别</div>
            </div>
            """)
            gr.HTML("""
            <div class="feature-card">
                <div class="feature-icon">🤖</div>
                <div class="feature-title">智能对话</div>
                <div class="feature-description">Qwen2.5 支持上下文记忆</div>
            </div>
            """)
            gr.HTML("""
            <div class="feature-card">
                <div class="feature-icon">👤</div>
                <div class="feature-title">声纹识别</div>
                <div class="feature-description">CAM++ 专属助手验证</div>
            </div>
            """)
            gr.HTML("""
            <div class="feature-card">
                <div class="feature-icon">🔊</div>
                <div class="feature-title">语音合成</div>
                <div class="feature-description">Edge TTS 多语种自然语音</div>
            </div>
            """)
        
        # 页脚
        gr.Markdown("""
        ---
        <div style="text-align: center; color: #666; padding: 1rem;">
            🦆 麻鸭语音助手 v2.0 | Powered by ModelScope & Gradio | Made with ❤️
        </div>
        """)
        
        # ========== 事件绑定 ==========
        
        # 更新设置
        def update_settings(kws, word, sv, threshold, tts, prompt):
            return {
                "enable_kws": kws,
                "wake_word": word,
                "enable_sv": sv,
                "sv_threshold": threshold,
                "enable_tts": tts,
                "system_prompt": prompt
            }
        
        for component in [enable_kws, wake_word, enable_sv, sv_threshold, enable_tts, system_prompt]:
            component.change(
                fn=update_settings,
                inputs=[enable_kws, wake_word, enable_sv, sv_threshold, enable_tts, system_prompt],
                outputs=settings_state
            )
        
        # 发送消息
        send_btn.click(
            fn=chat_respond,
            inputs=[msg, chatbot, audio_input, settings_state],
            outputs=[chatbot, audio_output]
        ).then(
            lambda: ("", None),
            outputs=[msg, audio_input]
        )
        
        msg.submit(
            fn=chat_respond,
            inputs=[msg, chatbot, audio_input, settings_state],
            outputs=[chatbot, audio_output]
        ).then(
            lambda: ("", None),
            outputs=[msg, audio_input]
        )
        
        # 清空对话
        clear_btn.click(
            lambda: ([], None),
            outputs=[chatbot, audio_output]
        )
        
        # 加载模型
        load_btn.click(
            fn=maya_models.load_models,
            outputs=load_status
        )
        
        # 注册声纹
        register_btn.click(
            fn=register_voiceprint,
            inputs=voiceprint_audio,
            outputs=register_status
        )
    
    return demo

# ========== 主函数 ==========

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="麻鸭语音助手 - 现代化 Web UI")
    parser.add_argument("--port", type=int, default=7860, help="端口号")
    parser.add_argument("--share", action="store_true", help="生成公网链接")
    parser.add_argument("--server-name", type=str, default="0.0.0.0", help="服务器地址")
    args = parser.parse_args()
    
    print("""
    ╔════════════════════════════════════════════╗
    ║   🦆 麻鸭语音助手 v2.0 - 现代化界面       ║
    ║   Maya Voice Assistant - Modern UI        ║
    ╚════════════════════════════════════════════╝
    
    🎨 ChatGPT/Claude 风格界面
    🌓 支持深色/浅色主题
    💬 流式对话输出
    📱 响应式布局
    
    """)
    
    demo = create_modern_ui()
    
    # 启用队列以支持流式输出和进度条
    demo.queue(concurrency_count=5, max_size=20)
    
    demo.launch(
        server_name=args.server_name,
        server_port=args.port,
        share=args.share,
        show_error=True,
        inbrowser=True  # 自动打开浏览器
    )

