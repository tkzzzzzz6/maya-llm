#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对话记忆管理
Chat Memory Management
"""

class ChatMemory:
    """对话记忆类"""
    
    def __init__(self, max_length=2048):
        """
        初始化对话记忆
        
        Args:
            max_length: 最大记忆长度
        """
        self.history = []
        self.max_length = max_length

    def add_to_history(self, user_input, model_response):
        """
        添加对话到历史记录
        
        Args:
            user_input: 用户输入
            model_response: 模型回复
        """
        self.history.append(f"User: {user_input}")
        self.history.append(f"Assistant: {model_response}")

    def get_context(self):
        """
        获取拼接后的对话上下文
        
        Returns:
            str: 对话上下文
        """
        context = "\n".join(self.history)
        # 截断上下文，使其不超过 max_length
        if len(context) > self.max_length:
            context = context[-self.max_length:]
        return context
    
    def clear(self):
        """清空对话历史"""
        self.history = []
    
    def get_history_list(self):
        """
        获取对话历史列表
        
        Returns:
            list: [(user_msg, bot_msg), ...]
        """
        result = []
        for i in range(0, len(self.history), 2):
            if i + 1 < len(self.history):
                user = self.history[i].replace("User: ", "")
                assistant = self.history[i+1].replace("Assistant: ", "")
                result.append((user, assistant))
        return result

