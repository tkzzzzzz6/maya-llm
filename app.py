#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
麻鸭语音助手 - 主入口文件
Maya Voice Assistant - Main Entry Point

项目结构：
- src/backend/  后端逻辑（模型、推理、音频处理）
- src/frontend/ 前端界面（Gradio UI、样式）
- app.py        主入口文件
"""

import argparse
from src.frontend.ui import create_modern_ui

def main():
    """主函数"""
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
    
    📁 项目结构：
    ├── src/backend/   后端逻辑（模型、推理）
    └── src/frontend/  前端界面（UI、样式）
    
    """)
    
    # 创建UI
    demo = create_modern_ui()
    
    # 启用队列以支持流式输出和进度条
    demo.queue(concurrency_count=5, max_size=20)
    
    # 启动服务
    demo.launch(
        server_name=args.server_name,
        server_port=args.port,
        share=args.share,
        show_error=True,
        inbrowser=True  # 自动打开浏览器
    )

if __name__ == "__main__":
    main()

