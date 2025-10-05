#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
前端UI界面 - Claude 风格
Frontend UI - Claude Style
"""

import gradio as gr
from .styles import CLAUDE_CSS
from ..backend.models import maya_models
from ..backend.inference import inference_engine
from ..backend.config import DEFAULT_SETTINGS

def create_claude_ui():
    """创建 Claude 风格界面"""

    # 使用自定义主题
    custom_theme = gr.themes.Soft(
        primary_hue="orange",
        secondary_hue="stone",
        neutral_hue="stone",
        font=[gr.themes.GoogleFont("Inter"), "ui-sans-serif", "system-ui", "sans-serif"],
    ).set(
        body_background_fill="*neutral_50",
        body_background_fill_dark="*neutral_950",
        button_primary_background_fill="#CC785C",
        button_primary_background_fill_hover="#E69A7B",
        button_primary_text_color="white",
        input_background_fill="white",
        input_background_fill_dark="*neutral_800",
    )

    with gr.Blocks(css=CLAUDE_CSS, theme=custom_theme, title="麻鸭语音助手 - Claude 风格") as demo:

        # 隐藏的设置状态
        settings_state = gr.State(DEFAULT_SETTINGS.copy())
        sidebar_visible = gr.State(True)

        # 顶部导航栏
        gr.HTML("""
        <div class="claude-header">
            <div class="header-content">
                <div class="logo-section">
                    <span class="logo-icon">🦆</span>
                    <span class="logo-text">麻鸭语音助手</span>
                </div>
                <div class="header-actions">
                    <span style="font-size: 0.875rem; color: var(--text-secondary);">
                        Claude Style · AI Voice Assistant
                    </span>
                </div>
            </div>
        </div>
        """)

        # 主布局区域
        with gr.Row(elem_classes="main-container"):
            # 左侧 - 聊天区
            with gr.Column(elem_classes="chat-section", scale=3):
                # 聊天记录容器
                chatbot = gr.Chatbot(
                    label="",
                    height=550,
                    show_copy_button=True,
                    bubble_full_width=False,
                    avatar_images=("👤", "🦆"),
                    elem_classes="chat-container"
                )

                # 输入区域
                with gr.Group(elem_classes="input-section"):
                    msg = gr.Textbox(
                        label="",
                        placeholder="发送消息给麻鸭... (支持文字和语音，按 Enter 发送)",
                        show_label=False,
                        container=False,
                        lines=3,
                        max_lines=10,
                        elem_classes="input-box"
                    )

                    with gr.Row(elem_classes="input-actions"):
                        # 左侧控制按钮
                        with gr.Row():
                            audio_input = gr.Audio(
                                source="microphone",
                                type="filepath",
                                label="",
                                elem_id="voice-input",
                                visible=False
                            )
                            record_btn = gr.Button("🎙️ 录音", size="sm", elem_classes="btn-claude btn-secondary")
                            clear_btn = gr.Button("🗑️ 清空", size="sm", elem_classes="btn-claude btn-ghost")

                        # 右侧发送按钮
                        send_btn = gr.Button(
                            "发送 ↑",
                            variant="primary",
                            size="sm",
                            elem_classes="btn-claude btn-primary"
                        )

                # 音频播放区（隐藏式）
                audio_output = gr.Audio(label="", autoplay=True, visible=False)

                # 状态提示
                with gr.Row():
                    status_display = gr.Markdown(
                        '<div class="status-badge status-loading"><span class="status-dot"></span>请先加载模型</div>',
                        elem_classes="mt-sm"
                    )

            # 右侧 - 设置侧边栏
            with gr.Column(elem_classes="sidebar-section", scale=1):
                # 侧边栏头部
                gr.HTML('<div class="sidebar-header"><h3 class="sidebar-title">设置</h3></div>')

                with gr.Column(elem_classes="sidebar-content"):
                    # 模型加载区
                    with gr.Group(elem_classes="settings-group modern-card"):
                        gr.HTML('<div class="settings-label-icon">🚀 模型管理</div>')
                        load_btn = gr.Button(
                            "加载所有模型",
                            variant="primary",
                            elem_classes="btn-claude btn-primary btn-full-width",
                            size="sm"
                        )
                        load_status = gr.Markdown("")

                    # 对话控制
                    with gr.Accordion("🎛️ 对话控制", open=True, elem_classes="settings-accordion"):
                        with gr.Group(elem_classes="settings-inner-group"):
                            enable_kws = gr.Checkbox(
                                label="🔑 关键词唤醒",
                                value=False,
                                info="启用后需说唤醒词才响应",
                                elem_classes="custom-checkbox"
                            )
                            wake_word = gr.Textbox(
                                label="唤醒词",
                                value="yaya",
                                placeholder="例如：yaya",
                                scale=1,
                                elem_classes="modern-input"
                            )

                            enable_sv = gr.Checkbox(
                                label="👤 声纹验证",
                                value=False,
                                info="仅注册用户可使用",
                                elem_classes="custom-checkbox"
                            )
                            sv_threshold = gr.Slider(
                                minimum=0.1,
                                maximum=0.9,
                                value=0.35,
                                step=0.05,
                                label="验证阈值",
                                info="越高越严格",
                                elem_classes="modern-slider"
                            )

                            enable_tts = gr.Checkbox(
                                label="🔊 语音合成",
                                value=True,
                                info="自动播放语音回复",
                                elem_classes="custom-checkbox"
                            )

                    # AI 人设
                    with gr.Accordion("🤖 AI 人设", open=False, elem_classes="settings-accordion"):
                        with gr.Group(elem_classes="settings-inner-group"):
                            system_prompt = gr.Textbox(
                                label="系统提示词",
                                value=DEFAULT_SETTINGS["system_prompt"],
                                lines=5,
                                placeholder="自定义 AI 的性格和行为...",
                                info="定义 AI 的身份和风格",
                                elem_classes="modern-textarea"
                            )

                    # 声纹注册
                    with gr.Accordion("🎤 声纹注册", open=False, elem_classes="settings-accordion"):
                        with gr.Group(elem_classes="settings-inner-group"):
                            gr.Markdown(
                                "📝 录制 3-10 秒清晰语音\n\n💡 建议说：\"你好，我是[名字]，这是我的声纹\"",
                                elem_classes="text-secondary text-sm"
                            )
                            voiceprint_audio = gr.Audio(
                                source="microphone",
                                type="filepath",
                                label="录制音频",
                                elem_classes="modern-audio"
                            )
                            register_btn = gr.Button(
                                "✅ 注册声纹",
                                elem_classes="btn-claude btn-primary btn-full-width",
                                size="sm"
                            )
                            register_status = gr.Markdown("")

                    # 快捷帮助
                    with gr.Accordion("📖 使用指南", open=False, elem_classes="settings-accordion help-accordion"):
                        gr.HTML("""
                        <div class="help-content">
                            <div class="help-section">
                                <h4 class="help-title">⚡ 快速开始</h4>
                                <ol class="help-list">
                                    <li>点击 "加载所有模型"</li>
                                    <li>等待 1-3 分钟完成加载</li>
                                    <li>在输入框输入消息</li>
                                    <li>按 Enter 或点击 "发送 ↑"</li>
                                </ol>
                            </div>

                            <div class="help-section">
                                <h4 class="help-title">🔧 高级功能</h4>
                                <ul class="help-list">
                                    <li><strong>唤醒词</strong>: 说 "yaya，你的问题"</li>
                                    <li><strong>声纹</strong>: 先注册，再启用验证</li>
                                    <li><strong>语音</strong>: 点击 🎙️ 录音按钮</li>
                                </ul>
                            </div>

                            <div class="help-section">
                                <h4 class="help-title">⌨️ 快捷键</h4>
                                <ul class="shortcut-list">
                                    <li><kbd>Enter</kbd> 发送消息</li>
                                    <li><kbd>Shift</kbd> + <kbd>Enter</kbd> 换行</li>
                                    <li><kbd>Ctrl</kbd> + <kbd>K</kbd> 清空对话</li>
                                    <li><kbd>Esc</kbd> 取消当前操作</li>
                                </ul>
                            </div>
                        </div>
                        """)

        # 页脚 - 移到最外层
        with gr.Row():
            gr.HTML("""
            <div style="text-align: center; padding: 2rem; color: var(--text-tertiary); font-size: 0.875rem; width: 100%;">
                <p style="margin: 0;">🦆 麻鸭语音助手 v3.0 · Claude Style Edition</p>
                <p style="margin: 0.5rem 0 0 0;">
                    基于 SenseVoice + Qwen2.5 + CAM++ + Edge TTS |
                    <a href="https://github.com" style="color: var(--claude-orange); text-decoration: none;">GitHub</a>
                </p>
            </div>
            """)
        
        # ========== 事件绑定 ==========

        # 更新设置
        def update_settings(kws, word, sv, threshold, tts, prompt):
            """动态更新设置状态"""
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

        # 清空对话
        def clear_history():
            """清空对话历史"""
            maya_models.clear_memory()
            return [], None, '<div class="status-badge status-success"><span class="status-dot"></span>对话已清空</div>'

        clear_btn.click(
            fn=clear_history,
            outputs=[chatbot, audio_output, status_display]
        )

        # 加载模型 - 增强状态显示
        def load_models_with_status():
            """加载模型并更新状态"""
            for status in maya_models.load_models():
                # 根据状态返回不同的显示
                if "加载中" in status or "正在" in status:
                    yield status, f'<div class="status-badge status-loading"><div class="loading-spinner"></div>{status}</div>'
                elif "成功" in status:
                    yield status, f'<div class="status-badge status-success"><span class="status-dot"></span>{status}</div>'
                elif "失败" in status or "错误" in status:
                    yield status, f'<div class="status-badge status-error">❌ {status}</div>'
                else:
                    yield status, f'<div class="status-badge status-loading"><span class="status-dot"></span>{status}</div>'

        load_btn.click(
            fn=load_models_with_status,
            outputs=[load_status, status_display]
        )

        # 发送消息 - 优化流式输出
        def send_message(user_msg, history, audio, settings):
            """发送消息并获取回复（流式输出）"""
            # 调用推理引擎生成器
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
            lambda: ("", None, '<div class="status-badge status-success"><span class="status-dot"></span>就绪</div>'),
            outputs=[msg, audio_input, status_display]
        )

        # 点击发送按钮
        send_btn.click(
            fn=send_message,
            inputs=[msg, chatbot, audio_input, settings_state],
            outputs=[chatbot, audio_output]
        ).then(
            lambda: ("", None, '<div class="status-badge status-success"><span class="status-dot"></span>就绪</div>'),
            outputs=[msg, audio_input, status_display]
        )

        # 录音按钮切换
        def toggle_recording(visible):
            """切换录音界面"""
            return not visible

        record_btn.click(
            fn=toggle_recording,
            inputs=[audio_input],
            outputs=[audio_input]
        )

        # 注册声纹
        def register_voiceprint_with_feedback(audio):
            """注册声纹并提供反馈"""
            result = inference_engine.register_voiceprint(audio)
            if "成功" in result:
                return result, f'<div class="status-badge status-success">✅ 声纹已注册</div>'
            else:
                return result, f'<div class="status-badge status-error">❌ 注册失败</div>'

        register_btn.click(
            fn=register_voiceprint_with_feedback,
            inputs=voiceprint_audio,
            outputs=[register_status, status_display]
        )

    return demo


# 兼容旧函数名
def create_modern_ui():
    """兼容旧版函数名"""
    return create_claude_ui()

