#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
前端UI界面 - WebLLM 风格
Frontend UI - WebLLM Style
"""

import gradio as gr
from .styles_webllm import WEBLLM_CSS
from ..backend.models import maya_models
from ..backend.inference import inference_engine
from ..backend.config import DEFAULT_SETTINGS

def create_webllm_ui():
    """创建 WebLLM 风格界面"""

    # 使用自定义主题
    custom_theme = gr.themes.Soft(
        primary_hue="violet",
        secondary_hue="stone",
        neutral_hue="stone",
        font=[gr.themes.GoogleFont("Inter"), "Noto Sans SC", "ui-sans-serif", "system-ui", "sans-serif"],
    ).set(
        body_background_fill="#FFFFFF",
        body_background_fill_dark="#1A1A1A",
        button_primary_background_fill="#6A5CFF",
        button_primary_background_fill_hover="#5646E6",
        button_primary_text_color="white",
        input_background_fill="white",
        input_background_fill_dark="#2A2A2E",
    )

    with gr.Blocks(css=WEBLLM_CSS, theme=custom_theme, title="麻鸭语音助手 - WebLLM 风格") as demo:

        # 隐藏状态
        settings_state = gr.State(DEFAULT_SETTINGS.copy())
        conversations_state = gr.State([{"id": 0, "title": "新的聊天", "messages": 0, "time": "刚刚"}])
        current_conversation_id = gr.State(0)
        sidebar_open = gr.State(False)

        # 主容器
        with gr.Row(elem_classes="app-container"):

            # 左侧边栏
            with gr.Column(elem_classes="sidebar", scale=0, min_width=300):
                # 品牌区
                gr.HTML("""
                <div class="sidebar-brand">
                    <span class="sidebar-brand-icon">🦆</span>
                    <span class="sidebar-brand-text">麻鸭助手</span>
                </div>
                """)

                # 侧边栏操作
                with gr.Row(elem_classes="sidebar-actions"):
                    template_btn = gr.Button("📋 模板", elem_classes="pill-button", size="sm")
                    settings_btn = gr.Button("⚙️ 设置", elem_classes="pill-button", size="sm")

                # 会话列表
                with gr.Column(elem_classes="conversation-list"):
                    gr.HTML("""
                    <div class="conversation-item active">
                        <div class="conversation-title">新的聊天</div>
                        <div class="conversation-meta">0 条消息 · 刚刚</div>
                    </div>
                    """, elem_id="conversation-list-container")

                # 底部工具栏
                gr.HTML("""
                <div class="sidebar-footer">
                    <button class="icon-button" aria-label="语言设置" title="语言">🌐</button>
                    <button class="icon-button" aria-label="主题切换" title="主题">💡</button>
                    <button class="icon-button" aria-label="表情" title="表情">😊</button>
                    <button class="icon-button" aria-label="新建对话" title="新建">➕</button>
                </div>
                """)

            # 右侧主区域
            with gr.Column(elem_classes="main-area", scale=1):

                # 聊天头部
                with gr.Row(elem_classes="chat-header"):
                    with gr.Column(elem_classes="title-block", scale=1):
                        gr.HTML("""
                        <div>
                            <h1 class="chat-title">新的聊天</h1>
                            <p class="chat-meta">共 0 条对话</p>
                        </div>
                        """, elem_id="chat-header-title")

                    with gr.Row(elem_classes="header-actions"):
                        edit_btn = gr.Button("✏️", elem_classes="icon-button", size="sm", min_width=36)
                        share_btn = gr.Button("🔗", elem_classes="icon-button", size="sm", min_width=36)
                        audio_btn = gr.Button("🎵", elem_classes="icon-button", size="sm", min_width=36)
                        expand_btn = gr.Button("⛶", elem_classes="icon-button", size="sm", min_width=36)

                # 消息列表
                chatbot = gr.Chatbot(
                    label="",
                    height=500,
                    show_copy_button=True,
                    bubble_full_width=False,
                    avatar_images=("👤", "🦆"),
                    elem_classes="message-list",
                    container=False
                )

                # 消息输入区
                with gr.Column(elem_classes="composer"):
                    # 工具栏
                    with gr.Row(elem_classes="tool-row"):
                        pen_btn = gr.Button("✏️", elem_classes="icon-button", size="sm", min_width=36)
                        brush_btn = gr.Button("🎨", elem_classes="icon-button", size="sm", min_width=36)
                        mail_btn = gr.Button("📧", elem_classes="icon-button", size="sm", min_width=36)

                        # 模型选择
                        model_selector = gr.Dropdown(
                            choices=["Qwen2.5-1.5B-Instruct", "Qwen2-VL-2B", "CosyVoice-300M"],
                            value="Qwen2.5-1.5B-Instruct",
                            label="",
                            container=False,
                            elem_classes="model-pill",
                            scale=0,
                            min_width=200
                        )

                    # 输入框和发送按钮
                    with gr.Row(elem_classes="composer-form"):
                        msg = gr.Textbox(
                            label="",
                            placeholder="Enter 发送，Shift + Enter 换行 / 触发补全；触发命令",
                            show_label=False,
                            container=False,
                            lines=2,
                            max_lines=8,
                            elem_classes="composer-textarea"
                        )

                        send_btn = gr.Button(
                            "发送 ↑",
                            variant="primary",
                            elem_classes="send-button"
                        )

                # 隐藏的音频组件
                audio_input = gr.Audio(
                    source="microphone",
                    type="filepath",
                    label="",
                    visible=False
                )
                audio_output = gr.Audio(
                    label="",
                    autoplay=True,
                    visible=False
                )

        # 设置面板（可展开的侧边抽屉）
        with gr.Accordion("🛠️ 高级设置", open=False, elem_classes="settings-panel"):
            with gr.Column():
                # 模型加载
                with gr.Group(elem_classes="settings-section"):
                    gr.Markdown("**模型管理**", elem_classes="settings-title")
                    load_btn = gr.Button("🚀 加载所有模型", variant="primary", size="sm")
                    load_status = gr.Markdown("")

                # 对话控制
                with gr.Group(elem_classes="settings-section"):
                    gr.Markdown("**对话控制**", elem_classes="settings-title")

                    enable_kws = gr.Checkbox(
                        label="🔑 关键词唤醒",
                        value=False,
                        info="启用后需说唤醒词才响应"
                    )
                    wake_word = gr.Textbox(
                        label="唤醒词",
                        value="yaya",
                        placeholder="例如：yaya"
                    )

                    enable_sv = gr.Checkbox(
                        label="👤 声纹验证",
                        value=False,
                        info="仅注册用户可使用"
                    )
                    sv_threshold = gr.Slider(
                        minimum=0.1,
                        maximum=0.9,
                        value=0.35,
                        step=0.05,
                        label="验证阈值"
                    )

                    enable_tts = gr.Checkbox(
                        label="🔊 语音合成",
                        value=True,
                        info="自动播放语音回复"
                    )

                # AI 人设
                with gr.Group(elem_classes="settings-section"):
                    gr.Markdown("**AI 人设**", elem_classes="settings-title")
                    system_prompt = gr.Textbox(
                        label="系统提示词",
                        value=DEFAULT_SETTINGS["system_prompt"],
                        lines=5,
                        placeholder="自定义 AI 的性格和行为..."
                    )

                # 声纹注册
                with gr.Group(elem_classes="settings-section"):
                    gr.Markdown("**声纹注册**", elem_classes="settings-title")
                    gr.Markdown("录制 3-10 秒清晰语音", elem_classes="text-sm text-muted")

                    voiceprint_audio = gr.Audio(
                        source="microphone",
                        type="filepath",
                        label="录制音频"
                    )
                    register_btn = gr.Button("✅ 注册声纹", size="sm")
                    register_status = gr.Markdown("")

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

        # 加载模型
        def load_models_with_status():
            for status in maya_models.load_models():
                yield status

        load_btn.click(
            fn=load_models_with_status,
            outputs=load_status
        )

        # 发送消息
        def send_message(user_msg, history, audio, settings):
            for updated_history, audio_response in inference_engine.chat_respond(
                user_msg, history, audio, settings
            ):
                yield updated_history, audio_response

        # Enter 键发送
        msg.submit(
            fn=send_message,
            inputs=[msg, chatbot, audio_input, settings_state],
            outputs=[chatbot, audio_output]
        ).then(
            lambda: ("", None),
            outputs=[msg, audio_input]
        )

        # 点击发送
        send_btn.click(
            fn=send_message,
            inputs=[msg, chatbot, audio_input, settings_state],
            outputs=[chatbot, audio_output]
        ).then(
            lambda: ("", None),
            outputs=[msg, audio_input]
        )

        # 音频按钮切换录音
        def toggle_audio(visible):
            return not visible

        audio_btn.click(
            fn=toggle_audio,
            inputs=audio_input,
            outputs=audio_input
        )

        # 注册声纹
        def register_voiceprint(audio):
            return inference_engine.register_voiceprint(audio)

        register_btn.click(
            fn=register_voiceprint,
            inputs=voiceprint_audio,
            outputs=register_status
        )

    return demo


# 兼容旧函数名
def create_claude_ui():
    """兼容旧版函数名"""
    return create_webllm_ui()

def create_modern_ui():
    """兼容旧版函数名"""
    return create_webllm_ui()
