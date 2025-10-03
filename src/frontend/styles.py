#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
前端样式定义 - Claude 风格
Frontend Styles - Claude Style
"""

# 保留旧版样式名以兼容
MODERN_CSS = None  # 将在模块加载时设置

CLAUDE_CSS = """
/* ============================================
   Claude 风格主题 - 优雅极简设计
   ============================================ */

/* 全局变量 - 浅色模式 */
:root {
    /* Claude 经典配色 */
    --claude-orange: #CC785C;
    --claude-orange-light: #E69A7B;
    --claude-orange-dark: #B35F44;

    /* 主色调 */
    --primary-color: #CC785C;
    --primary-hover: #E69A7B;
    --primary-active: #B35F44;

    /* 背景色 - Claude 风格渐变 */
    --bg-gradient: linear-gradient(180deg, #F8F3EF 0%, #FEFCFB 100%);
    --bg-primary: #FFFFFF;
    --bg-secondary: #F9F7F5;
    --bg-tertiary: #F0EBE7;
    --bg-hover: #FAF8F6;
    --bg-input: #FFFFFF;

    /* 文字颜色 */
    --text-primary: #1A1A1A;
    --text-secondary: #666666;
    --text-tertiary: #999999;
    --text-white: #FFFFFF;

    /* 边框和分割线 */
    --border-color: #E8E4E0;
    --divider-color: #F0EBE7;

    /* 阴影 */
    --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.06);
    --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.08);
    --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.12);
    --shadow-xl: 0 16px 48px rgba(0, 0, 0, 0.15);

    /* 圆角 */
    --radius-sm: 8px;
    --radius-md: 12px;
    --radius-lg: 16px;
    --radius-xl: 24px;
    --radius-full: 9999px;

    /* 间距 */
    --spacing-xs: 0.5rem;
    --spacing-sm: 1rem;
    --spacing-md: 1.5rem;
    --spacing-lg: 2rem;
    --spacing-xl: 3rem;

    /* 字体 */
    --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", "Oxygen", "Ubuntu", "Cantarell", "Fira Sans", "Droid Sans", "Helvetica Neue", sans-serif;
    --font-mono: "SF Mono", Monaco, "Cascadia Code", "Roboto Mono", Consolas, "Courier New", monospace;
}

/* 深色模式 */
.dark {
    --bg-gradient: linear-gradient(180deg, #1A1A1A 0%, #0F0F0F 100%);
    --bg-primary: #1F1F1F;
    --bg-secondary: #2A2A2A;
    --bg-tertiary: #363636;
    --bg-hover: #2D2D2D;
    --bg-input: #252525;

    --text-primary: #ECECEC;
    --text-secondary: #B0B0B0;
    --text-tertiary: #808080;

    --border-color: #3A3A3A;
    --divider-color: #333333;

    --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.3);
    --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.4);
    --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.5);
    --shadow-xl: 0 16px 48px rgba(0, 0, 0, 0.6);

    --claude-orange: #E69A7B;
    --claude-orange-light: #F0B89A;
    --claude-orange-dark: #CC785C;
}

/* ============================================
   全局容器和布局
   ============================================ */

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    padding: 0;
    font-family: var(--font-sans);
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

.gradio-container {
    background: var(--bg-gradient) !important;
    font-family: var(--font-sans) !important;
    max-width: 100% !important;
    margin: 0 !important;
    padding: 0 !important;
    min-height: 100vh !important;
}

/* ============================================
   顶部导航栏 - Claude 风格
   ============================================ */

.claude-header {
    background: var(--bg-primary);
    border-bottom: 1px solid var(--border-color);
    padding: var(--spacing-sm) var(--spacing-lg);
    position: sticky;
    top: 0;
    z-index: 100;
    backdrop-filter: blur(10px);
    background: rgba(255, 255, 255, 0.95);
}

.dark .claude-header {
    background: rgba(31, 31, 31, 0.95);
}

.header-content {
    max-width: 1400px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.logo-section {
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
}

.logo-icon {
    font-size: 1.75rem;
    transition: transform 0.3s ease;
}

.logo-icon:hover {
    transform: scale(1.1) rotate(5deg);
}

.logo-text {
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--text-primary);
    letter-spacing: -0.02em;
}

.header-actions {
    display: flex;
    gap: var(--spacing-sm);
    align-items: center;
}

/* ============================================
   主内容区 - 左右布局
   ============================================ */

.main-container {
    max-width: 1400px;
    margin: 0 auto;
    display: flex;
    gap: 0;
    height: calc(100vh - 60px);
    position: relative;
}

.chat-section {
    flex: 1;
    display: flex;
    flex-direction: column;
    background: var(--bg-primary);
    border-right: 1px solid var(--border-color);
}

.sidebar-section {
    width: 360px;
    background: var(--bg-secondary);
    overflow-y: auto;
    border-left: 1px solid var(--border-color);
}

/* ============================================
   聊天区域 - Claude 风格对话
   ============================================ */

.chat-container {
    flex: 1;
    overflow-y: auto;
    padding: var(--spacing-lg);
    scroll-behavior: smooth;
}

/* 消息气泡 - Claude 风格 */
.message-wrapper {
    margin-bottom: var(--spacing-lg);
    animation: messageSlideIn 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes messageSlideIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.user-message {
    background: var(--bg-secondary);
    border-radius: var(--radius-lg);
    padding: var(--spacing-md) var(--spacing-lg);
    margin-left: 15%;
    border: 1px solid var(--border-color);
    position: relative;
}

.user-message::before {
    content: "👤";
    position: absolute;
    left: -2.5rem;
    top: var(--spacing-md);
    font-size: 1.5rem;
}

.bot-message {
    background: transparent;
    padding: var(--spacing-md) var(--spacing-lg);
    margin-right: 15%;
    position: relative;
    line-height: 1.7;
    color: var(--text-primary);
}

.bot-message::before {
    content: "🦆";
    position: absolute;
    left: -2.5rem;
    top: var(--spacing-md);
    font-size: 1.5rem;
}

/* 打字机效果 */
.typing-indicator {
    display: inline-flex;
    align-items: center;
    gap: 0.25rem;
    padding: var(--spacing-xs);
}

.typing-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--claude-orange);
    animation: typingBounce 1.4s infinite ease-in-out;
}

.typing-dot:nth-child(1) { animation-delay: -0.32s; }
.typing-dot:nth-child(2) { animation-delay: -0.16s; }
.typing-dot:nth-child(3) { animation-delay: 0s; }

@keyframes typingBounce {
    0%, 80%, 100% {
        transform: scale(0.8);
        opacity: 0.5;
    }
    40% {
        transform: scale(1.2);
        opacity: 1;
    }
}

/* ============================================
   输入区域 - Claude 风格
   ============================================ */

.input-section {
    padding: var(--spacing-lg);
    background: var(--bg-primary);
    border-top: 1px solid var(--border-color);
}

.input-container {
    max-width: 800px;
    margin: 0 auto;
    position: relative;
}

.input-box {
    background: var(--bg-input) !important;
    border: 2px solid var(--border-color) !important;
    border-radius: var(--radius-lg) !important;
    padding: var(--spacing-md) var(--spacing-lg) !important;
    font-size: 1rem !important;
    line-height: 1.5 !important;
    transition: all 0.2s ease !important;
    resize: none !important;
    min-height: 56px !important;
}

.input-box:focus {
    outline: none !important;
    border-color: var(--claude-orange) !important;
    box-shadow: 0 0 0 3px rgba(204, 120, 92, 0.1) !important;
}

.input-actions {
    display: flex;
    gap: var(--spacing-sm);
    margin-top: var(--spacing-sm);
    justify-content: space-between;
    align-items: center;
}

/* ============================================
   按钮系统 - Claude 风格
   ============================================ */

.btn-claude {
    padding: 0.625rem 1.25rem !important;
    border-radius: var(--radius-md) !important;
    font-weight: 500 !important;
    font-size: 0.9375rem !important;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
    border: none !important;
    cursor: pointer !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 0.5rem !important;
}

.btn-primary {
    background: var(--claude-orange) !important;
    color: var(--text-white) !important;
    box-shadow: var(--shadow-sm) !important;
}

.btn-primary:hover {
    background: var(--claude-orange-light) !important;
    transform: translateY(-1px) !important;
    box-shadow: var(--shadow-md) !important;
}

.btn-primary:active {
    background: var(--claude-orange-dark) !important;
    transform: translateY(0) !important;
}

.btn-secondary {
    background: var(--bg-secondary) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-color) !important;
}

.btn-secondary:hover {
    background: var(--bg-hover) !important;
    border-color: var(--claude-orange) !important;
}

.btn-ghost {
    background: transparent !important;
    color: var(--text-secondary) !important;
}

.btn-ghost:hover {
    background: var(--bg-hover) !important;
    color: var(--text-primary) !important;
}

.btn-icon {
    width: 40px !important;
    height: 40px !important;
    padding: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    border-radius: var(--radius-full) !important;
}

/* ============================================
   侧边栏 - 设置面板
   ============================================ */

.sidebar-header {
    padding: var(--spacing-lg);
    border-bottom: 1px solid var(--divider-color);
    background: var(--bg-primary);
}

.sidebar-title {
    font-size: 1.125rem;
    font-weight: 600;
    color: var(--text-primary);
    margin: 0;
}

.sidebar-content {
    padding: var(--spacing-lg);
}

.settings-group {
    margin-bottom: var(--spacing-lg);
    padding-bottom: var(--spacing-lg);
    border-bottom: 1px solid var(--divider-color);
}

.settings-group:last-child {
    border-bottom: none;
}

.settings-label {
    font-size: 0.875rem;
    font-weight: 600;
    color: var(--text-secondary);
    margin-bottom: var(--spacing-sm);
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* ============================================
   状态指示器
   ============================================ */

.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.375rem 0.75rem;
    border-radius: var(--radius-full);
    font-size: 0.8125rem;
    font-weight: 500;
}

.status-success {
    background: #D1FAE5;
    color: #065F46;
}

.dark .status-success {
    background: rgba(16, 185, 129, 0.2);
    color: #6EE7B7;
}

.status-loading {
    background: #DBEAFE;
    color: #1E40AF;
}

.dark .status-loading {
    background: rgba(59, 130, 246, 0.2);
    color: #93C5FD;
}

.status-error {
    background: #FEE2E2;
    color: #991B1B;
}

.dark .status-error {
    background: rgba(239, 68, 68, 0.2);
    color: #FCA5A5;
}

.status-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    animation: statusPulse 2s infinite;
}

@keyframes statusPulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

/* ============================================
   表单控件 - Claude 风格
   ============================================ */

.gr-input, .gr-textarea, .gr-dropdown {
    background: var(--bg-input) !important;
    border: 1.5px solid var(--border-color) !important;
    border-radius: var(--radius-md) !important;
    color: var(--text-primary) !important;
    font-size: 0.9375rem !important;
    transition: all 0.2s ease !important;
}

.gr-input:focus, .gr-textarea:focus, .gr-dropdown:focus {
    border-color: var(--claude-orange) !important;
    box-shadow: 0 0 0 3px rgba(204, 120, 92, 0.1) !important;
    outline: none !important;
}

.gr-checkbox {
    accent-color: var(--claude-orange) !important;
}

.gr-slider input[type="range"] {
    accent-color: var(--claude-orange) !important;
}

/* ============================================
   音频组件美化
   ============================================ */

.audio-player {
    background: var(--bg-secondary) !important;
    border: 1.5px solid var(--border-color) !important;
    border-radius: var(--radius-lg) !important;
    padding: var(--spacing-md) !important;
}

.audio-waveform {
    background: var(--claude-orange) !important;
}

/* ============================================
   Tabs - Claude 风格
   ============================================ */

.gr-tab {
    background: transparent !important;
    border: none !important;
    color: var(--text-secondary) !important;
    font-weight: 500 !important;
    padding: var(--spacing-sm) var(--spacing-md) !important;
    transition: all 0.2s ease !important;
}

.gr-tab:hover {
    color: var(--text-primary) !important;
    background: var(--bg-hover) !important;
}

.gr-tab.selected {
    color: var(--claude-orange) !important;
    border-bottom: 2px solid var(--claude-orange) !important;
}

/* ============================================
   滚动条美化
   ============================================ */

::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: var(--bg-secondary);
}

::-webkit-scrollbar-thumb {
    background: var(--border-color);
    border-radius: var(--radius-full);
}

::-webkit-scrollbar-thumb:hover {
    background: var(--text-tertiary);
}

/* ============================================
   响应式设计
   ============================================ */

@media (max-width: 1024px) {
    .sidebar-section {
        width: 320px;
    }
}

@media (max-width: 768px) {
    .main-container {
        flex-direction: column;
    }

    .sidebar-section {
        width: 100%;
        border-left: none;
        border-top: 1px solid var(--border-color);
    }

    .user-message, .bot-message {
        margin-left: 0;
        margin-right: 0;
    }
}

/* ============================================
   加载动画
   ============================================ */

.loading-spinner {
    border: 2px solid var(--bg-tertiary);
    border-top: 2px solid var(--claude-orange);
    border-radius: 50%;
    width: 20px;
    height: 20px;
    animation: spin 0.8s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* ============================================
   辅助类
   ============================================ */

.text-center { text-align: center; }
.text-right { text-align: right; }
.flex { display: flex; }
.flex-col { flex-direction: column; }
.items-center { align-items: center; }
.justify-between { justify-content: space-between; }
.gap-sm { gap: var(--spacing-sm); }
.gap-md { gap: var(--spacing-md); }
.mt-sm { margin-top: var(--spacing-sm); }
.mt-md { margin-top: var(--spacing-md); }
.mb-sm { margin-bottom: var(--spacing-sm); }
.mb-md { margin-bottom: var(--spacing-md); }
.text-sm { font-size: 0.875rem; }
.text-secondary { color: var(--text-secondary); }
"""

# 兼容旧版变量名
MODERN_CSS = CLAUDE_CSS

