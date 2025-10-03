#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
前端样式定义
Frontend Styles
"""

MODERN_CSS = """
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

/* 录音按钮样式优化 */
.audio-record-btn {
    border-radius: 50% !important;
    width: 48px !important;
    height: 48px !important;
    padding: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}

.audio-recording {
    background: #ef4444 !important;
    animation: pulse 1.5s infinite !important;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
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

/* 音频组件美化 */
.gr-audio {
    border-radius: var(--radius) !important;
    border: 2px solid var(--border-color) !important;
}

.gr-audio:hover {
    border-color: var(--primary-color) !important;
}
"""

