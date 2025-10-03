#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
前端UI界面
Frontend UI
"""

import gradio as gr
from .styles import MODERN_CSS
from ..backend.models import maya_models
from ..backend.inference import inference_engine
from ..backend.config import DEFAULT_SETTINGS

def create_modern_ui():
    """创建现代化界面"""
    
    with gr.Blocks(css=MODERN_CSS, theme=gr.themes.Soft(), title="麻鸭语音助手") as demo:
        
        # 隐藏的设置状态
        settings_state = gr.State(DEFAULT_SETTINGS.copy())
        
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
                        # 修复：使用 Gradio 3.x 兼容的参数
                        audio_input = gr.Audio(
                            source="microphone",
                            type="filepath",
                            label="🎙️ 录音",
                            elem_classes="audio-record-btn"
                        )
                
                with gr.Row():
                    send_btn = gr.Button("📤 发送", variant="primary", size="lg", elem_classes="primary-btn")
                    clear_btn = gr.Button("🗑️ 清空", size="lg")
                
                # 音频播放
                audio_output = gr.Audio(label="🔊 语音回复", autoplay=True, visible=True)
                
                # 使用提示
                gr.Markdown("""
                💡 **使用提示**: 
                - 文字输入：直接打字即可
                - 语音输入：点击🎙️录音按钮，说话后再次点击停止，然后点击发送
                - 如需唤醒词/声纹验证，请在右侧设置中启用
                """)
            
            # 右侧 - 设置和功能区
            with gr.Column(scale=1):
                with gr.Tabs():
                    # Tab 1: 快速设置
                    with gr.Tab("⚙️ 设置"):
                        gr.Markdown("### 🎛️ 快速设置")
                        
                        with gr.Group():
                            gr.Markdown("#### 模型加载")
                            load_btn = gr.Button("🚀 加载模型", variant="primary", size="sm")
                            load_status = gr.Markdown("⏳ 请先加载模型")
                        
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
                                value=DEFAULT_SETTINGS["system_prompt"],
                                lines=4
                            )
                    
                    # Tab 2: 声纹注册
                    with gr.Tab("👤 声纹"):
                        gr.Markdown("### 🎙️ 声纹注册")
                        gr.Markdown("录制 3-10 秒清晰语音\n\n建议说：\"你好，我是[你的名字]，这是我的声纹\"")
                        
                        voiceprint_audio = gr.Audio(
                            source="microphone",
                            type="filepath",
                            label="录制音频"
                        )
                        register_btn = gr.Button("✅ 注册声纹", variant="primary")
                        register_status = gr.Markdown("")
                    
                    # Tab 3: 帮助
                    with gr.Tab("❓ 帮助"):
                        gr.Markdown("""
                        ### 📖 快速开始
                        
                        #### 1️⃣ 加载模型
                        点击"设置"→"🚀 加载模型"
                        
                        #### 2️⃣ 开始对话
                        **文字对话**（最简单）
                        - 直接输入文字
                        - 点击"发送"
                        
                        **语音对话**
                        - 点击🎙️录音按钮
                        - 说话（自动开始录音）
                        - 再次点击按钮停止
                        - 点击"发送"
                        
                        #### 3️⃣ 高级功能
                        **唤醒词**
                        - 开启后需说"站起来，[问题]"
                        - 可自定义唤醒词
                        
                        **声纹验证**
                        - 先在"声纹"标签注册
                        - 开启后仅注册用户可用
                        
                        ---
                        
                        ### 💡 常见问题
                        
                        **Q: 录音没反应？**
                        - 检查麦克风权限
                        - 浏览器需允许录音
                        - 点击🎙️开始，再次点击停止
                        
                        **Q: 没有声音回复？**
                        - 检查是否开启"语音合成"
                        - 检查系统音量
                        
                        **Q: 模型加载慢？**
                        - 首次需下载约2-3GB
                        - 耐心等待1-3分钟
                        """)
        
        # 底部功能特性展示
        gr.Markdown("---")
        gr.Markdown("### ✨ 核心功能")
        
        with gr.Row():
            gr.HTML('<div class="feature-card"><div class="feature-icon">🎙️</div><div class="feature-title">语音识别</div><div class="feature-description">SenseVoice 高精度识别</div></div>')
            gr.HTML('<div class="feature-card"><div class="feature-icon">🤖</div><div class="feature-title">智能对话</div><div class="feature-description">Qwen2.5 上下文记忆</div></div>')
            gr.HTML('<div class="feature-card"><div class="feature-icon">👤</div><div class="feature-title">声纹识别</div><div class="feature-description">CAM++ 专属验证</div></div>')
            gr.HTML('<div class="feature-card"><div class="feature-icon">🔊</div><div class="feature-title">语音合成</div><div class="feature-description">Edge TTS 多语种</div></div>')
        
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
            settings = DEFAULT_SETTINGS.copy()
            settings.update({
                "enable_kws": kws,
                "wake_word": word,
                "enable_sv": sv,
                "sv_threshold": threshold,
                "enable_tts": tts,
                "system_prompt": prompt
            })
            return settings
        
        for component in [enable_kws, wake_word, enable_sv, sv_threshold, enable_tts, system_prompt]:
            component.change(
                fn=update_settings,
                inputs=[enable_kws, wake_word, enable_sv, sv_threshold, enable_tts, system_prompt],
                outputs=settings_state
            )
        
        # 发送消息
        send_btn.click(
            fn=inference_engine.chat_respond,
            inputs=[msg, chatbot, audio_input, settings_state],
            outputs=[chatbot, audio_output]
        ).then(
            lambda: ("", None),
            outputs=[msg, audio_input]
        )
        
        msg.submit(
            fn=inference_engine.chat_respond,
            inputs=[msg, chatbot, audio_input, settings_state],
            outputs=[chatbot, audio_output]
        ).then(
            lambda: ("", None),
            outputs=[msg, audio_input]
        )
        
        # 清空对话
        def clear_history():
            maya_models.clear_memory()
            return [], None
        
        clear_btn.click(
            fn=clear_history,
            outputs=[chatbot, audio_output]
        )
        
        # 加载模型
        load_btn.click(
            fn=maya_models.load_models,
            outputs=load_status
        )
        
        # 注册声纹
        register_btn.click(
            fn=inference_engine.register_voiceprint,
            inputs=voiceprint_audio,
            outputs=register_status
        )
    
    return demo

