#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WebLLM 风格样式定义
WebLLM Style CSS
"""

WEBLLM_CSS = """
/* ============================================
   WebLLM 风格主题 - 两栏聊天应用
   ============================================ */

/* CSS 变量 - 浅色模式 */
:root {
    /* 主色调 - 紫色系 */
    --accent: #6A5CFF;
    --accent-hover: #5646E6;
    --accent-light: rgba(106, 92, 255, 0.1);
    --accent-focus: rgba(106, 92, 255, 0.24);

    /* 背景色 */
    --bg: #FFFFFF;
    --sidebar-bg: #F3F2F9;
    --card-bg: #FFFFFF;
    --bubble-bg: #F5F6F8;
    --bubble-user-bg: #6A5CFF;
    --hover-bg: #F8F8FC;

    /* 文字颜色 */
    --text-primary: #1A1A1A;
    --text-secondary: #5F6368;
    --text-muted: #9AA0B4;
    --text-white: #FFFFFF;

    /* 边框和分割线 */
    --border-color: rgba(0, 0, 0, 0.06);
    --divider-color: rgba(0, 0, 0, 0.08);

    /* 阴影 */
    --shadow-sm: 0 1px 4px rgba(0, 0, 0, 0.04);
    --shadow-md: 0 4px 16px rgba(15, 15, 15, 0.06);
    --shadow-lg: 0 4px 20px rgba(107, 92, 255, 0.12);
    --shadow-focus: 0 0 0 3px var(--accent-focus);

    /* 圆角 */
    --radius-sm: 8px;
    --radius-md: 12px;
    --radius-lg: 16px;
    --radius-full: 999px;

    /* 间距 */
    --spacing-xs: 6px;
    --spacing-sm: 12px;
    --spacing-md: 16px;
    --spacing-lg: 24px;
    --spacing-xl: 32px;

    /* 字体 */
    --font-sans: "Inter", "Noto Sans SC", -apple-system, BlinkMacSystemFont, sans-serif;
    --font-mono: "SF Mono", Monaco, "Cascadia Code", monospace;
}

/* 深色模式 */
.dark {
    --bg: #1A1A1A;
    --sidebar-bg: #242428;
    --card-bg: #2A2A2E;
    --bubble-bg: #323236;
    --bubble-user-bg: #6A5CFF;
    --hover-bg: #2E2E32;

    --text-primary: #E8E8E8;
    --text-secondary: #B8B8B8;
    --text-muted: #808080;

    --border-color: rgba(255, 255, 255, 0.08);
    --divider-color: rgba(255, 255, 255, 0.1);

    --shadow-sm: 0 1px 4px rgba(0, 0, 0, 0.3);
    --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.4);
}

/* ============================================
   全局重置
   ============================================ */

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    margin: 0;
    font-family: var(--font-sans);
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    background: var(--bg);
    color: var(--text-primary);
}

.gradio-container {
    max-width: 100% !important;
    margin: 0 !important;
    padding: 20px !important;
    background: var(--bg) !important;
    font-family: var(--font-sans) !important;
    min-height: 100vh !important;
}

/* ============================================
   主应用布局 - Grid 两栏
   ============================================ */

.app-container {
    display: grid;
    grid-template-columns: 300px 1fr;
    gap: var(--spacing-lg);
    height: calc(100vh - 40px);
    max-width: 100%;
}

/* ============================================
   左侧边栏
   ============================================ */

.sidebar {
    background: var(--sidebar-bg);
    border-radius: var(--radius-lg);
    padding: var(--spacing-md);
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

/* 品牌区 */
.sidebar-brand {
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
    padding: var(--spacing-sm);
    margin-bottom: var(--spacing-md);
}

.sidebar-brand-icon {
    font-size: 1.5rem;
}

.sidebar-brand-text {
    font-size: 1.125rem;
    font-weight: 600;
    color: var(--text-primary);
}

/* 侧边栏操作按钮 */
.sidebar-actions {
    display: flex;
    gap: var(--spacing-xs);
    margin-bottom: var(--spacing-md);
}

.pill-button {
    flex: 1;
    height: 36px;
    padding: 0 var(--spacing-md);
    background: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-full);
    font-size: 0.875rem;
    font-weight: 500;
    color: var(--text-secondary);
    cursor: pointer;
    transition: all 0.2s ease;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
}

.pill-button:hover {
    background: var(--hover-bg);
    color: var(--text-primary);
    transform: translateY(-1px);
    box-shadow: var(--shadow-sm);
}

.pill-button.active {
    background: var(--accent);
    color: var(--text-white);
    border-color: var(--accent);
}

/* 会话列表 */
.conversation-list {
    flex: 1;
    overflow-y: auto;
    padding: var(--spacing-xs);
}

.conversation-item {
    background: var(--card-bg);
    border-radius: var(--radius-md);
    padding: var(--spacing-sm);
    margin-bottom: var(--spacing-sm);
    border: 1px solid transparent;
    box-shadow: var(--shadow-sm);
    cursor: pointer;
    transition: all 0.2s ease;
}

.conversation-item:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
}

.conversation-item.active {
    border-left: 3px solid var(--accent);
    box-shadow: var(--shadow-lg);
    background: var(--bg);
}

.conversation-title {
    font-size: 0.9375rem;
    font-weight: 500;
    color: var(--text-primary);
    margin-bottom: 4px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.conversation-meta {
    font-size: 0.75rem;
    color: var(--text-muted);
}

/* 侧边栏底部工具 */
.sidebar-footer {
    display: flex;
    justify-content: space-around;
    padding-top: var(--spacing-md);
    border-top: 1px solid var(--border-color);
    margin-top: var(--spacing-md);
}

.icon-button {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    border: none;
    background: var(--card-bg);
    color: var(--text-secondary);
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.125rem;
}

.icon-button:hover {
    background: var(--hover-bg);
    color: var(--accent);
    transform: scale(1.1);
}

/* ============================================
   右侧主区域
   ============================================ */

.main-area {
    display: flex;
    flex-direction: column;
    background: var(--bg);
    border-radius: var(--radius-lg);
    overflow: hidden;
    box-shadow: var(--shadow-sm);
}

/* 聊天头部 */
.chat-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: var(--spacing-md) var(--spacing-lg);
    border-bottom: 1px solid var(--border-color);
    min-height: 64px;
}

.title-block {
    flex: 1;
}

.chat-title {
    font-size: 1.125rem;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 4px;
}

.chat-meta {
    font-size: 0.8125rem;
    color: var(--text-muted);
}

.header-actions {
    display: flex;
    gap: var(--spacing-xs);
}

/* ============================================
   消息列表区域
   ============================================ */

.message-list {
    flex: 1;
    overflow-y: auto;
    padding: var(--spacing-lg);
    scroll-behavior: smooth;
}

.message {
    display: flex;
    gap: var(--spacing-sm);
    align-items: flex-start;
    margin-bottom: var(--spacing-md);
    animation: messageSlideIn 0.3s ease;
}

@keyframes messageSlideIn {
    from {
        opacity: 0;
        transform: translateY(6px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.message.user {
    flex-direction: row-reverse;
}

.message-avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: var(--accent-light);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.25rem;
    flex-shrink: 0;
}

.message.user .message-avatar {
    background: var(--accent);
    color: var(--text-white);
}

.message-bubble {
    background: var(--bubble-bg);
    padding: 12px 14px;
    border-radius: var(--radius-md);
    max-width: 65%;
    position: relative;
}

.message.user .message-bubble {
    background: var(--bubble-user-bg);
    color: var(--text-white);
}

.message-text {
    font-size: 0.9375rem;
    line-height: 1.5;
    word-wrap: break-word;
}

.message-hint {
    font-size: 0.75rem;
    color: var(--text-muted);
    margin-top: 6px;
    display: block;
}

.message.user .message-hint {
    color: rgba(255, 255, 255, 0.8);
}

/* ============================================
   消息输入区（Composer）
   ============================================ */

.composer {
    border-top: 1px solid var(--border-color);
    padding: var(--spacing-sm);
    background: var(--bg);
}

.tool-row {
    display: flex;
    gap: var(--spacing-xs);
    margin-bottom: var(--spacing-sm);
    padding: 0 var(--spacing-xs);
}

.model-pill {
    display: inline-flex;
    align-items: center;
    gap: var(--spacing-xs);
    padding: 6px 10px;
    background: #F0F0F5;
    border-radius: var(--radius-full);
    font-size: 0.8125rem;
    color: var(--text-secondary);
    cursor: pointer;
    transition: all 0.2s ease;
}

.model-pill:hover {
    background: #E8E8F0;
    color: var(--text-primary);
}

.dark .model-pill {
    background: var(--card-bg);
}

.dark .model-pill:hover {
    background: var(--hover-bg);
}

.composer-form {
    display: flex;
    gap: var(--spacing-sm);
    align-items: flex-end;
}

.composer-textarea {
    flex: 1;
    min-height: 56px !important;
    max-height: 200px !important;
    padding: 12px !important;
    border-radius: var(--radius-md) !important;
    border: 1px solid var(--border-color) !important;
    background: var(--bg) !important;
    font-size: 0.9375rem !important;
    font-family: var(--font-sans) !important;
    resize: vertical !important;
    transition: all 0.2s ease !important;
    line-height: 1.5 !important;
}

.composer-textarea:focus {
    outline: none !important;
    border-color: var(--accent) !important;
    box-shadow: var(--shadow-focus) !important;
}

.send-button {
    height: 56px !important;
    min-width: 72px !important;
    padding: 0 var(--spacing-md) !important;
    background: var(--accent) !important;
    color: var(--text-white) !important;
    border: none !important;
    border-radius: var(--radius-md) !important;
    font-size: 0.9375rem !important;
    font-weight: 600 !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 6px !important;
}

.send-button:hover {
    background: var(--accent-hover) !important;
    transform: translateY(-1px) !important;
    box-shadow: var(--shadow-md) !important;
}

.send-button:active {
    transform: translateY(0) !important;
}

/* ============================================
   设置面板（右侧抽屉）
   ============================================ */

.settings-panel {
    background: var(--card-bg);
    border-radius: var(--radius-md);
    padding: var(--spacing-md);
    margin-bottom: var(--spacing-sm);
}

.settings-section {
    margin-bottom: var(--spacing-md);
    padding-bottom: var(--spacing-md);
    border-bottom: 1px solid var(--border-color);
}

.settings-section:last-child {
    border-bottom: none;
    margin-bottom: 0;
}

.settings-title {
    font-size: 0.875rem;
    font-weight: 600;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: var(--spacing-sm);
}

/* ============================================
   滚动条美化
   ============================================ */

.conversation-list::-webkit-scrollbar,
.message-list::-webkit-scrollbar {
    width: 6px;
}

.conversation-list::-webkit-scrollbar-track,
.message-list::-webkit-scrollbar-track {
    background: transparent;
}

.conversation-list::-webkit-scrollbar-thumb,
.message-list::-webkit-scrollbar-thumb {
    background: var(--border-color);
    border-radius: var(--radius-full);
}

.conversation-list::-webkit-scrollbar-thumb:hover,
.message-list::-webkit-scrollbar-thumb:hover {
    background: var(--text-muted);
}

/* ============================================
   响应式设计
   ============================================ */

/* 平板 (≤ 1024px) */
@media (max-width: 1024px) {
    .app-container {
        grid-template-columns: 260px 1fr;
        gap: var(--spacing-md);
    }
}

/* 移动端 (≤ 768px) */
@media (max-width: 768px) {
    .gradio-container {
        padding: 0 !important;
    }

    .app-container {
        grid-template-columns: 1fr;
        gap: 0;
        height: 100vh;
    }

    .sidebar {
        position: fixed;
        left: -100%;
        top: 0;
        bottom: 0;
        width: 280px;
        z-index: 1000;
        border-radius: 0;
        transition: left 0.3s ease;
    }

    .sidebar.open {
        left: 0;
    }

    .sidebar-overlay {
        position: fixed;
        inset: 0;
        background: rgba(0, 0, 0, 0.5);
        z-index: 999;
        display: none;
    }

    .sidebar-overlay.show {
        display: block;
    }

    .main-area {
        border-radius: 0;
        height: 100vh;
    }

    .message-bubble {
        max-width: 85%;
    }

    .composer {
        position: sticky;
        bottom: 0;
    }

    .composer-textarea {
        font-size: 16px !important; /* 防止 iOS 自动缩放 */
    }
}

/* 手机小屏 (≤ 480px) */
@media (max-width: 480px) {
    .message-bubble {
        max-width: 90%;
        font-size: 0.875rem;
    }

    .chat-header {
        padding: var(--spacing-sm) var(--spacing-md);
    }

    .message-list {
        padding: var(--spacing-md);
    }

    .send-button {
        min-width: 56px !important;
    }
}

/* 触摸设备优化 */
@media (hover: none) and (pointer: coarse) {
    .icon-button,
    .pill-button,
    .send-button {
        min-height: 44px;
        min-width: 44px;
    }
}

/* ============================================
   辅助类
   ============================================ */

.hidden {
    display: none !important;
}

.flex {
    display: flex;
}

.flex-col {
    flex-direction: column;
}

.items-center {
    align-items: center;
}

.justify-between {
    justify-content: space-between;
}

.gap-sm {
    gap: var(--spacing-sm);
}

.text-sm {
    font-size: 0.875rem;
}

.text-muted {
    color: var(--text-muted);
}

.truncate {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
"""
