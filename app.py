#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
麻鸭语音助手 - 主入口文件 (WebLLM 风格版本)
Maya Voice Assistant - Main Entry Point (WebLLM Style)

项目结构：
- src/backend/  后端逻辑（模型、推理、音频处理）
- src/frontend/ 前端界面（Gradio UI、样式）
- app.py        主入口文件
"""

import argparse
from src.frontend.ui_webllm import create_webllm_ui

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="麻鸭语音助手 - WebLLM 风格 Web UI")
    parser.add_argument("--port", type=int, default=7860, help="端口号 (默认: 7860)")
    parser.add_argument("--share", action="store_true", help="生成公网分享链接")
    parser.add_argument("--server-name", type=str, default="0.0.0.0", help="服务器地址 (默认: 0.0.0.0)")
    parser.add_argument("--debug", action="store_true", help="启用调试模式")
    args = parser.parse_args()

    # 显示启动信息
    share_status = "✅ 开启" if args.share else "❌ 关闭"
    debug_status = "✅ 开启" if args.debug else "❌ 关闭"
    server_display = args.server_name if args.server_name != "0.0.0.0" else "0.0.0.0 (所有网络接口)"

    print(f"""
    ╔═══════════════════════════════════════════════════╗
    ║   🦆 麻鸭语音助手 v3.0 - WebLLM Style Edition   ║
    ║   Maya Voice Assistant - WebLLM Style UI        ║
    ╚═══════════════════════════════════════════════════╝

    ✨ 特性亮点：
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    🎨 WebLLM 紫色主题 - 两栏聊天布局
    🌓 深色/浅色主题切换 - 自动护眼模式
    💬 流式对话输出 - 实时打字效果
    📱 完美响应式布局 - 适配所有设备
    🗂️ 会话列表管理 - 多对话支持
    🎙️ 语音交互支持 - ASR + TTS 集成
    👤 声纹识别验证 - CAM++ 专属验证
    🔑 自定义唤醒词 - 保护隐私安全

    🏗️ 技术栈：
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    • ASR: SenseVoice (高精度语音识别)
    • LLM: Qwen2.5-1.5B (对话理解)
    • SV:  CAM++ (声纹验证)
    • TTS: Edge TTS (多语种合成)
    • UI:  Gradio + WebLLM Style CSS

    📁 项目结构：
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    ├── src/backend/   后端逻辑（模型、推理）
    └── src/frontend/  前端界面（UI、样式）

    🚀 启动配置：
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    • 端口: {args.port}
    • 地址: {server_display}
    • 分享: {share_status}
    • 调试: {debug_status}

    💡 提示：首次运行需下载 2-3GB 模型，请耐心等待...
    ═══════════════════════════════════════════════════

    """)

    # 创建 WebLLM 风格 UI
    print("🎨 正在初始化 WebLLM 风格界面...")
    demo = create_webllm_ui()

    # 启用队列以支持流式输出和进度条
    print("⚙️  配置队列系统...")
    demo.queue(
        concurrency_count=5,
        max_size=20,
        api_open=False
    )

    # 启动服务
    print(f"🚀 启动服务器：http://{args.server_name}:{args.port}")
    print("📱 浏览器将自动打开...\n")

    demo.launch(
        server_name=args.server_name,
        server_port=args.port,
        share=args.share,
        show_error=True,
        inbrowser=True,  # 自动打开浏览器
        quiet=not args.debug,  # 调试模式下显示详细日志
        show_api=args.debug  # 调试模式下显示 API 文档
    )

if __name__ == "__main__":
    main()

